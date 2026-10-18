#!/usr/bin/env python3
"""Row-by-row source verification for the SF events register.

For every cited source URL this fetches the live page and records:

  * HTTP status (following redirects) and the final URL;
  * whether the page's visible text actually mentions the event it is cited for;
  * a short verbatim snippet around the match, used as the evidence excerpt.

Why this exists: the authoring sandboxes have no general outbound network, so the
checks that need the open web run in GitHub Actions. This is the honest middle
ground between "a link exists" and "a human re-read 200 pages": it proves the
page is live and names the event, and it records the text it matched. It cannot
prove every date/time/price value; rows that were not manually transcribed keep
a 'page-level' verification label on the site.

Usage:
  python3 tools/verify_rows.py [--timeout 25] [--fail-on-dead] [--out data/verify_report.json]

Exit code is 0 unless --fail-on-dead is given and a source returns 404/410 or a
DNS/connection error. Bot-blocking (403/429/5xx) is reported, not treated as dead.
"""
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIMEOUT = 25
if "--timeout" in sys.argv:
    TIMEOUT = int(sys.argv[sys.argv.index("--timeout") + 1])
OUT = ROOT / "data" / "verify_report.json"
if "--out" in sys.argv:
    OUT = Path(sys.argv[sys.argv.index("--out") + 1])

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

rows = json.loads((ROOT / "data" / "events.json").read_text())
sources = json.loads((ROOT / "data" / "sources.json").read_text())


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.title = ""
        self._skip = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self._skip += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self._skip:
            self._skip -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if not self._skip:
            self.parts.append(data)


GENERIC = set("""
san francisco street market festival fest fair parade celebration event events annual
special community center centre city hall free days day week weeks open house show
live tour tours run runs walk race opera symphony ballet season series party block
square gardens garden museum science exhibit exhibition arts art food film comedy
night park parks neighborhood downtown north south east west upper lower outer inner
mission sunset bay area golden gate the and with for from 2026 2027 2028
""".split())


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return s


def tokens(name):
    words = re.findall(r"[a-z0-9]+", norm(name))
    sig = [w for w in words if len(w) >= 5 and w not in GENERIC and not w.isdigit()]
    if not sig:
        sig = [w for w in words if len(w) >= 4 and w not in GENERIC and not w.isdigit()]
    return sig


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read(2_500_000)
            ctype = r.headers.get_content_type() or ""
            is_pdf = raw[:4] == b"%PDF" or ctype == "application/pdf"
            charset = r.headers.get_content_charset() or "utf-8"
            html = raw.decode(charset, "ignore")
            p = Text()
            if not is_pdf:
                p.feed(html)
            text = re.sub(r"\s+", " ", " ".join(p.parts))
            return {"http": r.getcode(), "final_url": r.geturl(), "chars": len(raw),
                    "content_type": ctype, "pdf": is_pdf,
                    "title": re.sub(r"\s+", " ", p.title).strip()[:160], "text": text,
                    "seconds": round(time.time() - t0, 1)}
    except urllib.error.HTTPError as e:
        return {"http": e.code, "final_url": url, "error": f"HTTP {e.code}",
                "seconds": round(time.time() - t0, 1)}
    except Exception as e:
        return {"http": 0, "final_url": url, "error": f"{type(e).__name__}: {str(e)[:120]}",
                "seconds": round(time.time() - t0, 1)}


used = {}
for row in rows:
    for sid in row["sources"]:
        used.setdefault(sid, []).append(row)

urls = {}
for sid in used:
    urls.setdefault(sources[sid]["url"], []).append(sid)

print(f"fetching {len(urls)} unique URLs for {len(rows)} rows "
      f"({len(used)} source records)…", flush=True)
fetched = {}
with ThreadPoolExecutor(max_workers=8) as pool:
    for url, res in zip(urls, pool.map(fetch, urls)):
        fetched[url] = res
print("fetch complete", flush=True)

report = {"checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "timeout_seconds": TIMEOUT, "urls": {}, "sources": {}, "rows": {},
          "dead": [], "blocked": [], "no_response": []}

for url, res in fetched.items():
    text = res.pop("text", "")
    res["found_any"] = False
    res["matches"] = {}
    for sid in urls[url]:
        row = used[sid][0]
        hay = norm(res.get("title", "") + " " + text)
        toks = tokens(row["name"])
        if not toks:
            toks = [w for w in re.findall(r"[a-z0-9]+", norm(row["name"]))
                    if len(w) >= 4 and not w.isdigit()]
        hit = next((t for t in toks if t in hay), None)
        if not hit:
            full = norm(row["name"])
            if full and len(full) > 10 and full in hay:
                hit = full
        res["matches"][sid] = hit
        res["found_any"] = res["found_any"] or bool(hit)
        if hit:
            i = norm(text).find(norm(hit))
            snippet = text[max(0, i - 160): i + 220].strip()
            report["sources"].setdefault(sid, {})["snippet"] = re.sub(r"\s+", " ", snippet)[:380]
    res["sample_tokens"] = tokens(used[urls[url][0]][0]["name"])
    if res.get("pdf"):
        res.pop("matches", None)
        res["note"] = "PDF fetched; text check skipped (manual read required)."
    report["urls"][url] = res
    if res["http"] in (404, 410, 0):
        report["dead"].append({"url": url, "http": res["http"], "error": res.get("error", "")})
    elif res["http"] != 200:
        report["blocked"].append({"url": url, "http": res["http"], "error": res.get("error", "")})

for row in rows:
    hits = []
    for sid in row["sources"]:
        url = sources[sid]["url"]
        r = report["urls"].get(url, {})
        hit = r.get("matches", {}).get(sid)
        if hit:
            hits.append({"source": sid, "url": url, "match": hit,
                         "snippet": report["sources"].get(sid, {}).get("snippet", ""),
                         "http": r.get("http")})
    statuses = [report["urls"].get(sources[s]["url"], {}) for s in row["sources"]]
    if hits:
        status = "name_found"
    elif any(x.get("pdf") for x in statuses):
        status = "pdf_not_checked"
    elif not any(x.get("http") for x in statuses):
        status = "no_response"
    else:
        status = "name_not_found"
    report["rows"][row["id"]] = {"name": row["name"], "status": status,
                                 "hits": hits[:2],
                                 "sources_checked": len(row["sources"])}

ok = sum(1 for v in report["rows"].values() if v["status"] == "name_found")
notfound = [v for v in report["rows"].values() if v["status"] == "name_not_found"]
noresp = [v for v in report["rows"].values() if v["status"] == "no_response"]
pdfs = [v for v in report["rows"].values() if v["status"] == "pdf_not_checked"]
report["summary"] = {"rows": len(rows), "name_found": ok,
                     "name_not_found": len(notfound), "no_response": len(noresp),
                     "pdf_not_checked": len(pdfs),
                     "dead_urls": len(report["dead"]), "blocked_urls": len(report["blocked"])}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")

print(f"rows: {len(rows)}  name found on a cited page: {ok}  "
      f"not found: {len(notfound)}  no response: {len(noresp)}")
print(f"URLs: {len(urls)}  dead (404/410/DNS): {len(report['dead'])}  "
      f"blocked/5xx: {len(report['blocked'])}")

if report["dead"]:
    print("\nDEAD SOURCE LINKS:")
    for d in report["dead"]:
        print(f"  [{d['http'] or d['error']}] {d['url']}")
    msg = "; ".join(f"{d['http'] or d['error']} {d['url']}" for d in report["dead"])[:6000]
    print(f"::error title=Dead official source links ({len(report['dead'])})::{msg}")
if notfound:
    print("\nPAGES THAT DID NOT MENTION THE EVENT (manual check needed):")
    for v in notfound:
        print(f"  {v['name']}  ({v['sources_checked']} source(s))")
    msg = "; ".join(v["name"] for v in notfound)[:6000]
    print(f"::warning title=Source page did not name the event ({len(notfound)})::{msg}")
if report["blocked"]:
    msg = "; ".join(f"{b['http']} {b['url']}" for b in report["blocked"])[:6000]
    print(f"::warning title=Bot-blocked or server-error source pages ({len(report['blocked'])})::{msg}")

summary_path = Path(__import__("os").environ.get("GITHUB_STEP_SUMMARY", "/dev/null"))
if str(summary_path) != "/dev/null":
    with summary_path.open("a") as fh:
        fh.write("## Row-source verification\n\n")
        fh.write(f"- Rows checked: **{len(rows)}**\n")
        fh.write(f"- Event name found on a cited page: **{ok}**\n")
        fh.write(f"- Not found (manual check): **{len(notfound)}**\n")
        fh.write(f"- No response: **{len(noresp)}**\n")
        fh.write(f"- Dead URLs: **{len(report['dead'])}** · blocked/5xx: **{len(report['blocked'])}**\n\n")
        if report["dead"]:
            fh.write("| Dead URL | Status |\n|---|---|\n")
            for d in report["dead"]:
                fh.write(f"| {d['url']} | {d['http'] or d['error']} |\n")
        if notfound:
            fh.write("\n| Row |\n|---|\n")
            for v in notfound:
                fh.write(f"| {v['name']} |\n")

if "--fail-on-dead" in sys.argv and report["dead"]:
    sys.exit(1)

# trigger
