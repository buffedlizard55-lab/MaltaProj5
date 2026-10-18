#!/usr/bin/env python3
"""Capture first-party evidence for review; NEVER turn a word match into verification.

Run --capture on an internet-capable runner. The report retains extracted source
text, HTTP status, redirect target, hashes and candidate literal matches. Approved
field transcriptions are separate, explicit decisions made after reading that text.
Network failures never erase a previous capture or claim a page/event is verified.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/audit_64f8b973.json"
USER_AGENT = "Mozilla/5.0 (compatible; SFEventsEvidenceAudit/1.0; +https://github.com/buffedlizard55-lab/MaltaProj5)"
FIELDS = ("name", "schedule", "time", "venue", "price")


def normalized(value):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


class Extract(HTMLParser):
    """Visible block text + first-party links and structured data, not script text."""
    BLOCK = {"address", "article", "br", "dd", "div", "dt", "h1", "h2", "h3", "h4", "li", "p", "section", "td", "th", "tr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.main_parts, self.links, self.structured = [], [], [], []
        self.skip = 0
        self.in_main = 0
        self.in_title = False
        self.title = ""
        self.ld = None
        self.href = None
        self.link_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "main":
            self.in_main += 1
        if tag == "title":
            self.in_title = True
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
            if tag == "script" and attrs.get("type", "").lower() == "application/ld+json":
                self.ld = []
        if tag == "a" and not self.skip:
            self.href = attrs.get("href")
            self.link_text = []
        if tag in self.BLOCK and not self.skip:
            self.parts.append("\n")
            if self.in_main:
                self.main_parts.append("\n")

    def handle_endtag(self, tag):
        if tag == "script" and self.ld is not None:
            try:
                self.structured.append(json.loads("".join(self.ld)))
            except (ValueError, TypeError):
                pass
            self.ld = None
        if tag in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1
        if tag == "title":
            self.in_title = False
        if tag == "a" and self.href:
            self.links.append({"url": self.href, "text": normalized(" ".join(self.link_text))})
            self.href = None
        if tag in self.BLOCK and not self.skip:
            self.parts.append("\n")
            if self.in_main:
                self.main_parts.append("\n")
        if tag == "main" and self.in_main:
            self.in_main -= 1

    def handle_data(self, value):
        if self.in_title:
            self.title += value
        if self.ld is not None:
            self.ld.append(value)
        if not self.skip:
            self.parts.append(value)
            if self.in_main:
                self.main_parts.append(value)
            if self.href:
                self.link_text.append(value)

    def text(self):
        # Preserve lines so a reviewer can distinguish one event card from another.
        parts = self.main_parts if len("".join(self.main_parts).strip()) > 100 else self.parts
        return "\n".join(normalized(line) for line in "".join(parts).splitlines() if normalized(line))


def fetch(url, timeout=25):
    started = time.monotonic()
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = response.read(4_000_001)
                result = {"http": response.status, "final_url": response.url,
                          "content_type": response.headers.get_content_type(),
                          "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                          "sha256": hashlib.sha256(data).hexdigest(),
                          "truncated_response": len(data) > 4_000_000}
                if data.startswith(b"%PDF"):
                    try:
                        from pypdf import PdfReader
                        reader = PdfReader(io.BytesIO(data))
                        text = "\n".join(page.extract_text() or "" for page in reader.pages[:40])
                        result.update(title="Official PDF", text=text, pdf=True, links=[], structured=[])
                    except ImportError:
                        result.update(title="Official PDF", text="", pdf=True, error="PDF text reader unavailable")
                else:
                    parser = Extract()
                    parser.feed(data.decode(response.headers.get_content_charset() or "utf-8", "replace"))
                    result.update(title=normalized(parser.title), text=parser.text(), pdf=False,
                                  links=[{"url": urljoin(response.url, link["url"]), "text": link["text"]}
                                         for link in parser.links if link["text"]], structured=parser.structured)
                result["seconds"] = round(time.monotonic() - started, 2)
                return result
        except urllib.error.HTTPError as error:
            result = {"http": error.code, "final_url": error.url, "error": f"HTTP {error.code}", "text": ""}
            if error.code not in (429, 500, 502, 503, 504):
                break
        except (OSError, ValueError) as error:
            result = {"http": 0, "final_url": url, "error": f"{type(error).__name__}: {str(error)[:180]}", "text": ""}
        if attempt == 0:
            time.sleep(1)
    result["checked_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    result["seconds"] = round(time.monotonic() - started, 2)
    return result


def retain_capture(previous, attempt, locked=False):
    """Never erase usable evidence on failure, or mutate adjudicated evidence.

    A later HTTP response is not a re-approval. Keep the original status/date with
    its text; report the latest request separately so failure cannot look like 200.
    """
    if previous and (previous.get("text") or previous.get("tool_excerpt")):
        if locked or not attempt.get("text") or attempt.get("http") != 200:
            kept = dict(previous)
            kept["latest_attempt"] = {k: v for k, v in attempt.items()
                                      if k not in {"text", "links", "structured"}}
            return kept
        attempt = dict(attempt)
        for key in ("tool_excerpt", "tool_method"):
            if key in previous:
                attempt[key] = previous[key]
    return attempt


def capture(extra_urls=(), timeout=25):
    rows = json.loads((ROOT / "data/events.json").read_text())
    sources = json.loads((ROOT / "data/sources.json").read_text())
    old = json.loads(REPORT.read_text()) if REPORT.exists() else {}
    urls = set(source["url"] for source in sources.values()) | set(extra_urls)
    # A capture is not a crawl: only URLs explicitly in the register/review plan.
    for url in urls:
        if urlsplit(url).scheme != "https":
            raise ValueError(f"Only HTTPS official-source URLs may be captured: {url}")
    captures = dict(old.get("captures", {}))
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(fetch, url, timeout): url for url in sorted(urls)}
        for future in as_completed(futures):
            url, result = futures[future], future.result()
            # Full text is retained as a finite evidence snapshot, not as an event feed.
            text = result.get("text", "")
            result["text_truncated"] = len(text) > 140_000
            result["text"] = text[:140_000]
            result["links"] = result.get("links", [])[:600]
            captures[url] = retain_capture(captures.get(url), result, locked=bool(old.get("decisions")))
            print(f"{result['http']:3} {len(text):6} {url}", flush=True)
    candidates = {}
    for row in rows:
        candidates[row["id"]] = {"name": row["name"], "sources": [sources[s]["url"] for s in row["sources"]], "fields": {}}
        for field in FIELDS:
            value = row.get(field, "")
            matches = [url for url in candidates[row["id"]]["sources"]
                       if value and normalized(value).casefold() in normalized(captures.get(url, {}).get("text", "")).casefold()]
            candidates[row["id"]]["fields"][field] = {"original": value, "literal_match_urls": matches,
                                                        "status": "candidate only — requires contextual review"}
    output = {"schema_version": 1, "session": "64f8b973", "captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "method": "Official-source extracted-text snapshot. Literal matches are candidates, NEVER approvals. Each published nonblank fact needs an explicit field decision and supporting quotation.",
              "captures": dict(sorted(captures.items())), "candidates": old.get("candidates") or candidates, "decisions": old.get("decisions", {}),
              "extra_events": old.get("extra_events", [])}
    REPORT.write_text(json.dumps(output, indent=1, ensure_ascii=False) + "\n")
    print(f"Captured {len(captures)} sources for {len(rows)} rows; no verification decisions generated.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", action="store_true")
    parser.add_argument("--url", action="append", default=[])
    parser.add_argument("--timeout", type=int, default=25)
    args = parser.parse_args()
    if args.capture:
        capture(args.url, args.timeout)
    else:
        parser.error("Use --capture on an internet-capable runner; this tool does not infer values.")


if __name__ == "__main__":
    main()
