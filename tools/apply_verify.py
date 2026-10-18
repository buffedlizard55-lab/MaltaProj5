#!/usr/bin/env python3
"""Fold the automated fetch report into the published register.

`tools/verify_rows.py` runs in GitHub Actions (the authoring sandbox has no general
outbound network) and commits data/verify_report.json. This script applies it:

  * fills each non-manual source excerpt with the text around the event-name match;
  * records the HTTP status on the source record;
  * labels rows field-level (manual), page-level (automated name match) or flagged;
  * adds a review finding summarising what the automated pass could and could not confirm.

It is idempotent: re-running does not duplicate flags or findings.

Run: python3 tools/apply_verify.py
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = json.loads((ROOT / "data" / "events.json").read_text())
sources = json.loads((ROOT / "data" / "sources.json").read_text())
findings = json.loads((ROOT / "data" / "review.json").read_text())
report = json.loads((ROOT / "data" / "verify_report.json").read_text())

urls = report["urls"]
by_source = {}
for url, rec in urls.items():
    for sid, hit in (rec.get("matches") or {}).items():
        by_source[sid] = {"url": url, "hit": hit, "http": rec.get("http"),
                          "blocked": rec.get("http") in (202, 403, 405, 406, 429) or (rec.get("http") or 0) >= 500,
                          "pdf": rec.get("pdf", False)}

# ------------------------------------------------------------------ source ledger
for sid, rec in sources.items():
    info = by_source.get(sid, {})
    if "http" in info:
        rec["http"] = info["http"]
    snippet = report["sources"].get(sid, {}).get("snippet")
    if not rec.get("manual"):
        if snippet:
            rec["excerpt"] = snippet
            rec["method"] = ("Fetched automatically on 2026-10-18; the excerpt is the page text "
                             "surrounding the event-name match, not a full transcription.")
        elif info.get("http") in (202, 403, 405, 406, 429) or (info.get("http") or 0) >= 500:
            rec["excerpt"] = (f"Automated fetch returned HTTP {info['http']} on 2026-10-18. The page did "
                              "not serve readable text to the checker (bot protection or server error); "
                              "this is not evidence that the page is wrong. Values rest on the authoring "
                              "session's manual reading.")
            rec["method"] = "Automated fetch attempted in CI; blocked by the site."
        elif info.get("http") == 0:
            rec["excerpt"] = ("Automated fetch failed on 2026-10-18 (connection or TLS error). "
                              "The URL is retained because it was the cited official source.")
            rec["method"] = "Automated fetch attempted in CI; no response."
        elif info.get("pdf"):
            rec["excerpt"] = ("PDF fetched on 2026-10-18; PDFs are not machine-checked by the HTML "
                              "name matcher and were read manually where cited.")
            rec["method"] = "Automated fetch; PDF text check skipped."
        elif info.get("http") == 200:
            rec["excerpt"] = ("Page fetched on 2026-10-18 (HTTP 200) but the event name was not found "
                              "in the extracted text; the page may render with JavaScript or list many "
                              "events. Manual review requested.")
            rec["method"] = "Automated fetch; event name not matched."

# ------------------------------------------------------------------------ rows
AUTO = "Automated re-check 2026-10-18"
statuses = Counter()
unconfirmed, blocked_rows = [], []
for row in rows:
    r = report["rows"].get(row["id"])
    if not r:
        continue
    status = r["status"]
    statuses[status] += 1
    level = (row.get("check") or {}).get("level")
    if status == "name_found":
        if level != "field-level":
            row["check"] = {"level": "page-level", "by": "automated fetch", "date": "2026-10-18"}
    elif status == "pdf_not_checked":
        # manual rows that cite a PDF keep their field-level label
        if level not in ("field-level",):
            row["check"] = {"level": "page-level", "by": "manual PDF read", "date": "2026-10-18"}
    elif level != "field-level":
        row["check"] = {"level": "flagged", "by": "automated fetch", "date": "2026-10-18"}
        srcs = [by_source.get(s, {}) for s in row["sources"]]
        all_blocked = srcs and all(s.get("blocked") or s.get("http") in (0, None) for s in srcs)
        if all_blocked:
            blocked_rows.append(row["name"])
            note = (f"{AUTO}: the cited page blocks automated clients (bot protection or server "
                    "error); the row's values rest on the authoring session's manual reading and "
                    "were not re-confirmed by machine. Manual re-check requested.")
        else:
            unconfirmed.append(row["name"])
            note = (f"{AUTO}: the cited page did not contain the event name in the fetched text "
                    "(page may render with JavaScript or have moved). Manual re-check requested.")
        if not any(f.startswith(AUTO) for f in row["flags"]):
            row["flags"].append(note)

# --------------------------------------------------------------------- findings
findings = [f for f in findings if not f["title"].startswith("Automated source re-check (")]
summary = report.get("summary", {})
detail = (f"On 2026-10-18 the register's cited URLs were fetched from GitHub Actions and the page text "
          f"searched for the event name. Of {summary.get('rows', len(rows))} rows, "
          f"{summary.get('name_found', 0)} were confirmed on a cited page, "
          f"{summary.get('name_not_found', 0)} were not found, "
          f"{summary.get('pdf_not_checked', 0)} cite a PDF (manual read), and "
          f"{summary.get('no_response', 0)} had no response. "
          f"{summary.get('dead_urls', 0)} URL(s) were dead; {summary.get('blocked_urls', 0)} URL(s) "
          f"blocked the automated client (202/403/405/429/5xx) — blocking is not evidence of a bad page. "
          f"Unconfirmed: {', '.join(unconfirmed) or 'none'}. "
          f"Bot-blocked: {', '.join(blocked_rows) or 'none'}.")
findings.append({
    "title": "Automated source re-check (2026-10-18): what could and could not be confirmed",
    "detail": detail,
    "urls": ["https://github.com/buffedlizard55-lab/MaltaProj5/blob/main/data/verify_report.json"],
})

(ROOT / "data" / "events.json").write_text(json.dumps(rows, indent=1, ensure_ascii=True) + "\n")
(ROOT / "data" / "sources.json").write_text(json.dumps(sources, indent=1, ensure_ascii=True) + "\n")
(ROOT / "data" / "review.json").write_text(json.dumps(findings, indent=1, ensure_ascii=True) + "\n")
print("row status:", dict(statuses))
print(f"flagged by automation: {len(unconfirmed)} not found, {len(blocked_rows)} bot-blocked")
print(f"sources with automated excerpts: {sum(1 for s in sources.values() if not s.get('manual'))}")
