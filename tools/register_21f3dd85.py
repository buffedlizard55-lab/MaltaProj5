#!/usr/bin/env python3
"""Additive, fail-closed overlay for the 21f3dd85 free-first research (T37).

It chains after tools/register_3adf31d9.py with the same discipline and touches
ONLY the new candidates declared in data/audit_21f3dd85.json — free gaming, music
and AI gatherings inside San Francisco first, then other free entries, plus one
paid gaming entry that belongs to the separate Paid section.

The validators are imported, not copied, so the rules cannot drift between
overlays: every approved value carries an exact HTTPS quotation present in the
archived capture text for that URL; a blank field never receives a value;
Weekly / Monthly / Annual require their own recurrence quotation; an occurrence
date must be recoverable from its own quotation (year, month, day); publication
requires an approved name, venue and confirmed San Francisco geography.

One deliberate difference from register_3adf31d9.extend: when a cited URL already
has a source record, the new row id is appended to that record's
approved_for_rows (on a deep copy, so the projection stays pure). The earlier
overlay left reused records untouched, which undercounts the "referenced by N
row decisions" line on the Sources page.

This module never edits a row produced by an earlier overlay.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlsplit

from register_3adf31d9 import (CATEGORIES, FIELDS, SNAPSHOT, cost_of, next_date,
                               quote_urls, temporal, topic_of, validate_decision)

ROOT = Path(__file__).resolve().parents[1]
AUDIT_NAME = "audit_21f3dd85.json"


def extend(rows, sources, findings, summary):
    """Pure projection: rows after the 3adf31d9 overlay + this session's entries."""
    audit = json.loads((ROOT / "data" / AUDIT_NAME).read_text())
    captures, decisions, candidates = audit["captures"], audit["decisions"], audit["candidates"]
    if set(candidates) != set(decisions):
        raise ValueError("Candidate/decision mismatch in audit_21f3dd85.json")
    clash = set(candidates) & {r["id"] for r in rows}
    if clash:
        raise ValueError(f"New candidate id collides with the existing register: {sorted(clash)}")
    for decision in decisions.values():
        validate_decision(decision, captures)

    by_url = {source["url"]: key for key, source in sources.items()}
    new_keys = {}
    for url in sorted({url for decision in decisions.values() for url in quote_urls(decision)}):
        if url not in by_url:
            by_url[url] = "n-" + hashlib.sha256(url.encode()).hexdigest()[:12]
            new_keys[url] = by_url[url]
    source_rows = {url: [] for url in new_keys}

    added = []
    for candidate in candidates.values():
        decision = decisions[candidate["id"]]
        urls = quote_urls(decision)
        if not urls:
            raise ValueError(f"No official source link for {candidate['id']}")
        for url in urls:
            if url in source_rows:
                source_rows[url].append(candidate["id"])
        missing = [f"{field}: unverified" for field in FIELDS if field not in decision["fields"]]
        if decision["geography"]["status"] != "confirmed_sf":
            missing.append("geography: unverified; not admitted to city-only directory")
        if not decision.get("recurrence"):
            missing.append("recurrence: unverified; no ongoing cadence asserted")
        if not decision.get("occurrences") and decision["kind"] not in {"Weekly", "Monthly", "Annual"}:
            missing.append("date/year: unverified; no approved ISO occurrence")
        if decision["publication"] == "review_only" and not decision["fields"].get("venue"):
            missing.append("venue: unverified; not admitted to city-only directory")
        added.append({
            "id": candidate["id"],
            **{field: decision["fields"].get(field, {}).get("value", "") for field in FIELDS},
            "candidate_name": candidate["name"],
            "candidate_label": "New research identifier",
            "category": candidate["category"],
            "kind": decision["kind"],
            "entry_type": decision.get("entry_type", "event"),
            "parent": decision.get("parent", ""),
            "publication": decision["publication"],
            "geography": deepcopy(decision["geography"]),
            "recurrence": deepcopy(decision.get("recurrence")),
            "occurrences": deepcopy(decision.get("occurrences", [])),
            "date_status": decision.get("date_status", "confirmed"),
            "temporal_status": temporal(decision),
            "as_of": SNAPSHOT,
            "field_evidence": deepcopy(decision["fields"]),
            "sources": [by_url[url] for url in urls],
            "unverified": missing,
            "flags": [decision["reason"]] if decision.get("reason") else [],
            "notes": decision.get("notes", ""),
            "topic": decision.get("topic", "Other"),
            "audit": {
                "session": audit["session"],
                "reviewed_at": decision["reviewed_at"],
                "method": "Explicit contextual field decisions; incomplete fields remain blank",
            },
        })

    for row in added:
        if row["category"] not in CATEGORIES:
            raise ValueError(f"Invalid editorial grouping for {row['id']}")
        if row["parent"]:
            raise ValueError("New research entries must be top level")

    combined = list(rows) + added
    new_sources = deepcopy(sources)
    for url, key in new_keys.items():
        capture = captures[url]
        new_sources[key] = {
            "url": url,
            "publisher": urlsplit(url).netloc.removeprefix("www."),
            "title": capture.get("title") or urlsplit(url).netloc,
            "source_role": "Official cited page; link alone is not a verified fact",
            "captured_at": capture.get("checked_at", ""),
            "http": capture.get("http"),
            "tool_excerpt_available": bool(capture.get("tool_excerpt")),
            "tool_checked_at": capture.get("tool_checked_at", ""),
            "latest_attempt": capture.get("latest_attempt"),
            "audit_snapshot": f"data/{AUDIT_NAME}",
            "retrieval": capture.get("retrieval", {}),
            "approved_for_rows": source_rows[url],
        }
    # Keep the ledger count honest for URLs an earlier overlay already recorded:
    # a cited row is referenced whether its source record is new or reused.
    for row in added:
        for key in row["sources"]:
            referenced = new_sources[key].setdefault("approved_for_rows", [])
            if row["id"] not in referenced:
                referenced.append(row["id"])
    sources_out = {key: new_sources[key] for key in sorted(new_sources)}

    listed = [r for r in combined if r["publication"] == "listed"]
    kinds = Counter(r["kind"] for r in listed)
    blank_fields = {field: sum(not r[field] for r in listed) for field in FIELDS}
    summary_out = dict(summary)
    summary_out.update({
        "candidates": len(combined),
        "free_first_entries": len(added),
        "listed": len(listed),
        "review_only": len(combined) - len(listed),
        "series": sum(1 for r in listed if r["entry_type"] == "series"),
        "source_urls": len(sources_out),
        "domains": len({urlsplit(s["url"]).netloc.removeprefix("www.") for s in sources_out.values()}),
        "kinds": dict(kinds),
        "categories": dict(Counter(r["category"] for r in listed)),
        "temporal": dict(Counter(r["temporal_status"] for r in listed)),
        "blank_fields": blank_fields,
        "listed_with_blanks": sum(bool(r["unverified"]) for r in listed),
        "supported_field_values": summary.get("supported_field_values", 0) + sum(len(r["field_evidence"]) for r in added),
        "topics": dict(Counter(topic_of(r) for r in listed)),
        "cost": dict(Counter(cost_of(r)[0] for r in listed)),
        "upcoming_dated": sum(1 for r in listed if next_date(r)),
    })

    findings_out = list(findings) + [{
        "title": "Free-first research pass (session 21f3dd85)",
        "detail": (
            f"{len(added)} entries were added from official organizer, venue, library and "
            "government pages, free gaming/music/AI first: Noontime Concerts (free weekly "
            "classical series with three dated Tuesday concerts), the National Park Service Sea "
            "Chantey Sing (free, monthly, dated 5 December 2026), the Mechanics' Institute Chess "
            "Socials (free, monthly), gaming tournaments at the San Francisco Public Library's "
            "Mix teen space (monthly), and the library's annual Tech Week (free workshops "
            "including AI sessions). One paid gaming entry — the Mechanics' Institute 2026 Winter "
            "Tuesday Night Marathon chess tournament ($70 members / $100 non-members, 3 November "
            "to 15 December 2026) — was collected for the separate Paid section. Every value is "
            "quoted from the page read on 18 October 2026; where a page states no time or date, "
            "the cell stays blank. The Mechanics' Institute chess-classes page lists Chess "
            "Socials dates ('Nov 6, Dec 4') without a year, so no ISO occurrence was approved "
            "from that list."
        ),
        "urls": [
            "https://noontimeconcerts.org/",
            "https://www.nps.gov/planyourvisit/event-details.htm?id=2B52B414-F0EF-9707-2656479F9CAE0CBD",
            "https://www.milibrary.org/chess/chess-classes/",
            "https://www.milibrary.org/chess/tournaments/2026-winter-tuesday-night-marathon",
            "https://sfpl.org/releases/2026/04/24/level-tech-week-san-francisco-public-library",
        ],
    }, {
        "title": "SFPL admission judgment, two holds, and evidence for a held chess class",
        "detail": (
            "For its two new San Francisco Public Library rows this session quotes the library's "
            "official events index — 'All programs and events are free and open to the public.' "
            "(sfpl.org/events) — as admission evidence, applying that explicit all-programmes "
            "statement in context. The seven SFPL gaming rows added by session 3adf31d9 did not "
            "cite the index statement, so their admission cells stay blank ('Not stated'); no "
            "earlier row was edited, and the visible inconsistency is flagged for a future "
            "harmonization decision. Two candidates are held for review: the Internet Archive's "
            "Friday public tours (schedule, time, venue and free admission are all confirmed on "
            "archive.org, but the page gives the programme no title, and this register requires "
            "an approved event name), and Grace Cathedral's Organ Recital Series (official pages "
            "conflict — 'Cost: Free' and 'free organ recital' on some recital pages versus a "
            "Sunday visitor admission fee unless registered in advance on another, with no price "
            "on the fetched series page). Separately, the Mechanics' Institute chess-classes page "
            "now states a venue ('Onsite in the Chess Room at Mechanics'') and member pricing for "
            "the held 'Introduction to Chess' candidate; that evidence is recorded in "
            "data/research/audit-21f3dd85.md for a future corrections pass rather than published "
            "as a duplicate row."
        ),
        "urls": [
            "https://sfpl.org/events",
            "https://archive.org/about/contact",
            "https://gracecathedral.org/series/organ-recital-series/",
        ],
    }]
    return combined, sources_out, findings_out, summary_out


def apply_extension() -> None:
    """Read the files written by register_3adf31d9.apply_extension, extend, write back."""
    names = ("events.json", "sources.json", "review.json", "audit_summary.json")
    rows, sources, findings, summary = (json.loads((ROOT / "data" / name).read_text()) for name in names)
    combined, sources_out, findings_out, summary_out = extend(rows, sources, findings, summary)
    for name, value in zip(names, (combined, sources_out, findings_out, summary_out)):
        (ROOT / "data" / name).write_text(json.dumps(value, indent=1, ensure_ascii=False) + "\n")
    print(f"Extension 21f3dd85: +{len(combined) - len(rows)} entries; "
          f"{summary_out['listed']} listed / {summary_out['review_only']} review-only; "
          f"{summary_out['source_urls']} source URLs.")


if __name__ == "__main__":
    raise SystemExit("Run tools/consolidate.py so the audited overlay is always the final stage.")
