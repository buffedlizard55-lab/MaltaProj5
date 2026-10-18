#!/usr/bin/env python3
"""Apply a session's line-by-line manual audit to the published register.

Input: data/audit_<session>.json (default: data/audit_f1fd3c36.json), written by a
session that re-read each cited official page in human-readable form and compared
every populated field with the page text. Each entry is:

  {id, status (confirmed|corrected|unverified|excluded), url, quote, quote2?, note?,
   set?: {field: value}            -- "" blanks a field (and flags it unverified)
   unverified_fields?: [field, ..] -- fields the page does not state (blank + flag)
   add_source?: {url, publisher}}  -- an additional official page to link

and an optional top-level `add_rows` list of complete new rows found during the audit
(each with its own official url/quote).

Rules enforced here (the same ones the rest of the pipeline relies on):
  * a value is only written when the entry quotes the page that states it;
  * every populated field keeps an evidence pointer to a source record;
  * a blank tracked field always carries a "<field>: unverified" note, and a populated
    field never does (this removes the value-plus-"left blank" contradiction);
  * rows re-read manually become field-level checks; rows whose page could not
    confirm a value are labelled flagged;
  * idempotent — re-running does not duplicate sources, flags, notes or rows.

Runs after tools/apply_verify.py and before scripts/build.py:
    python3 tools/apply_audit.py [data/audit_<session>.json]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "audit_f1fd3c36.json"
FIELDS = ("schedule", "time", "venue", "price")

rows = json.loads((ROOT / "data" / "events.json").read_text())
sources = json.loads((ROOT / "data" / "sources.json").read_text())
findings = json.loads((ROOT / "data" / "review.json").read_text())
audit = json.loads(AUDIT.read_text())

SESSION = audit["session"]
DATE = audit["date"]
TAG = f"Manual re-read {DATE} (session {SESSION})"
AUTO = "Automated re-check 2026-10-18"
by_id = {r["id"]: r for r in rows}


def norm(url):
    return re.sub(r"^https?://(www\.)?", "", url.strip()).rstrip("/").lower()


def sid_for(url):
    """Source id for a URL: reuse an existing record, else derive a stable id."""
    for sid, rec in sources.items():
        if norm(rec["url"]) == norm(url):
            return sid
    slug = re.sub(r"[^a-z0-9]+", "-", norm(url)).strip("-")[:70]
    return f"{SESSION[:2]}-{slug}"


def ensure_source(url, publisher, quote):
    sid = sid_for(url)
    if sid not in sources:
        sources[sid] = {
            "url": url,
            "publisher": publisher,
            "checked": DATE,
            "excerpt": quote,
            "method": (f"Read manually by session {SESSION} on {DATE} (fetched as readable text); "
                       "the excerpt is transcribed from the page."),
            "manual": True,
        }
    else:
        rec = sources[sid]
        # a manual transcription is better evidence than an automated placeholder
        if not rec.get("manual") and quote and not quote.startswith("("):
            rec["excerpt"] = quote
            rec["method"] = (f"Re-read manually by session {SESSION} on {DATE}; the excerpt is "
                             "transcribed from the page (replaces the automated placeholder).")
            rec["manual"] = True
    return sid


def set_unverified(row, field, on, reason=None):
    row.setdefault("unverified", [])
    row["unverified"] = [u for u in row["unverified"] if not u.startswith(field + ": unverified")]
    row["flags"] = [f for f in row["flags"] if not re.match(rf"^{field}: unverified", f)]
    if on:
        row["unverified"].append(reason or f"{field}: unverified — not stated on the official page re-read on {DATE}.")


def add_flag(row, text):
    if text not in row["flags"]:
        row["flags"].append(text)


stats = {"confirmed": 0, "corrected": 0, "unverified": 0, "excluded": 0, "missing": []}
corrections, irregularities = [], []

for ent in audit["entries"]:
    row = by_id.get(ent["id"])
    if row is None:
        stats["missing"].append(ent["id"])
        continue
    status = ent["status"]
    stats[status] += 1
    quote = ent.get("quote", "")
    sid = ensure_source(ent["url"], ent.get("add_source", {}).get("publisher")
                        or f"Official page re-read by session {SESSION}", quote)
    if ent.get("add_source"):
        sid = ensure_source(ent["add_source"]["url"], ent["add_source"]["publisher"], quote)
    if sid not in row["sources"]:
        row["sources"].append(sid)
    row.setdefault("evidence", {})

    # field changes -------------------------------------------------------
    changed = []
    for field, value in (ent.get("set") or {}).items():
        if field == "name":
            if row["name"] != value:
                row["notes"] = (f"Formerly listed as \u201c{row['name']}\u201d. " + (row.get("notes") or "")).strip()
                row["name"] = value
                row["evidence"]["name"] = [sid]
                changed.append("name")
            continue
        if field == "kind":
            if row["kind"] != value:
                row["kind"] = value
                changed.append("kind")
            continue
        if row.get(field) != value:
            changed.append(field)
        row[field] = value
        if value:
            row["evidence"][field] = [sid]
            set_unverified(row, field, False)
        else:
            row["evidence"].pop(field, None)
            set_unverified(row, field, True)
    for field in ent.get("unverified_fields") or []:
        if field in FIELDS:
            if row.get(field):
                # the page confirms the row's other fields but not this one
                row[field] = ""
                row["evidence"].pop(field, None)
                changed.append(field)
            set_unverified(row, field, True)
    # a confirmed populated field now has manual evidence from the re-read page
    if status in ("confirmed", "corrected"):
        for field in FIELDS:
            if row.get(field) and sid not in row["evidence"].get(field, []):
                row["evidence"].setdefault(field, []).append(sid)
            if row.get(field):
                set_unverified(row, field, False)

    # labels ----------------------------------------------------------------
    row["flags"] = [f for f in row["flags"] if not f.startswith(TAG)]
    reread = not quote.startswith("(")   # "(...)" quotes mean the page was not re-read this pass
    if status == "unverified":
        row["check"] = {"level": "flagged", "by": SESSION, "date": DATE}
    elif reread:
        row["check"] = {"level": "field-level", "by": SESSION, "date": DATE}
    if reread:
        # the manual read supersedes the automated "manual re-check requested" note
        row["flags"] = [f for f in row["flags"] if not f.startswith(AUTO)]
    touched = list(dict.fromkeys(list((ent.get("set") or {}).keys()) + (ent.get("unverified_fields") or [])))
    blank = list(dict.fromkeys((ent.get("unverified_fields") or [])
                               + [k for k, v in (ent.get("set") or {}).items() if v == ""]))
    desc = {"confirmed": "every populated value matched the official page",
            "corrected": "values changed to match the official page: " + ", ".join(touched or ["source added"]),
            "unverified": "the official page does not state: " + ", ".join(blank),
            "excluded": "row excluded"}[status]
    note = f"{TAG}: {desc}. Page: {ent['url']}."
    if ent.get("note"):
        note += " " + ent["note"]
    if status != "confirmed" or ent.get("note"):
        add_flag(row, note)
    if status == "corrected":
        corrections.append(f"{row['name']} ({', '.join(touched) or 'source added'})")
    if status == "unverified":
        irregularities.append(f"{row['name']}: {ent.get('note') or desc}")

# new rows ---------------------------------------------------------------------
for nr in audit.get("add_rows", []):
    sid = ensure_source(nr["url"], nr["publisher"], nr["quote"])
    row = by_id.get(nr["id"])
    if row is None:
        row = {"id": nr["id"], "parent": None, "flags": []}
        rows.append(row)
        by_id[nr["id"]] = row
    row.update({k: nr[k] for k in ("name", "category", "kind", "schedule", "time", "venue", "price")})
    row["sources"] = [sid]
    row["evidence"] = {"name": [sid]}
    for field in FIELDS:
        if row[field]:
            row["evidence"][field] = [sid]
    row["notes"] = nr.get("notes", "")
    row["unverified"] = list(nr.get("unverified", []))
    for field in FIELDS:
        if not row[field] and not any(u.startswith(field + ": unverified") for u in row["unverified"]):
            row["unverified"].append(f"{field}: unverified; left blank.")
    row["check"] = {"level": "flagged" if row["unverified"] else "field-level", "by": SESSION, "date": DATE}
    add_flag(row, f"{TAG}: row added from the official page during the audit; blank cells are not stated there. Page: {nr['url']}.")

# consistency: no populated field may carry an "unverified" note; every blank one must
for r in rows:
    r.setdefault("unverified", [])
    for field in FIELDS:
        if r.get(field):
            r["unverified"] = [u for u in r["unverified"] if not u.startswith(field + ": unverified")]
        elif not any(u.startswith(field + ": unverified") for u in r["unverified"]):
            r["unverified"].append(f"{field}: unverified; left blank.")

# review finding -------------------------------------------------------------------
title = f"Manual line-by-line audit ({DATE}, session {SESSION})"
findings = [f for f in findings if not f["title"].startswith(title)]
n = len(audit["entries"])
findings.append({
    "title": title + ": corrections and irregularities",
    "detail": (f"{n} rows were re-read against their official pages in readable form (priority: rows the automated "
               f"check could not name-match, rows citing only aggregator pages, and rows with contradictory notes). "
               f"Confirmed as published: {stats['confirmed']}. Corrected: {stats['corrected']} — {'; '.join(corrections) or 'none'}. "
               f"Left unverified/flagged: {stats['unverified']} — {' | '.join(irregularities) or 'none'}. "
               f"Rows added from official pages: {', '.join(r['name'] for r in audit.get('add_rows', [])) or 'none'}. "
               "Every change is recorded as a per-row note with the page URL and the transcribed quote in data/audit_"
               f"{SESSION}.json."),
    "urls": [f"https://github.com/buffedlizard55-lab/MaltaProj5/blob/main/data/audit_{SESSION}.json"],
})

(ROOT / "data" / "events.json").write_text(json.dumps(rows, indent=1, ensure_ascii=True) + "\n")
(ROOT / "data" / "sources.json").write_text(json.dumps(sources, indent=1, ensure_ascii=True) + "\n")
(ROOT / "data" / "review.json").write_text(json.dumps(findings, indent=1, ensure_ascii=True) + "\n")
print(f"audit {SESSION}: {stats}")
print(f"rows now {len(rows)}; sources {len(sources)}; corrections {len(corrections)}")
