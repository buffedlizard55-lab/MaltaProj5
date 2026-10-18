#!/usr/bin/env python3
"""Additive, fail-closed overlay for the d57e2eeb free-first gap research (T37–T38).

It mirrors tools/register_3adf31d9.py exactly — same field rules, same pub tests —
but touches ONLY the new candidates declared in data/audit_d57e2eeb.json: free-first
gaming, music, AI/technology and civic/garden entries inside San Francisco that the
earlier registers did not cover, plus one explicitly Paid event kept distinct.

Rules enforced here, before anything is written (inherited from register_3adf31d9):

  * every approved value carries an exact HTTPS quotation that is present in the
    archived capture text for that URL (whitespace/NFKC-normalised substring test);
  * a blank field never receives a value, and an unapproved field stays blank;
  * Weekly / Monthly / Annual require their own recurrence quotation;
  * an occurrence date must be recoverable from its own quotation (year, month, day);
  * publication to the directory requires an approved name, venue and confirmed
    San Francisco geography;
  * the whole projection is pure and idempotent: extend() applied to the same base
    data always returns byte-identical results, so a rebuild cannot drift;
  * new candidate ids must not collide with any existing register row.

This module never edits a row produced by the earlier audited overlays.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlsplit

from register_3adf31d9 import (  # shared, identical rules
    CATEGORIES,
    FIELDS,
    cost_of,
    next_date,
    quote_urls,
    temporal,
    topic_of,
    validate_decision,
)

ROOT = Path(__file__).resolve().parents[1]
AUDIT_NAME = "audit_d57e2eeb.json"
SESSION = "d57e2eeb"


def extend(rows, sources, findings, summary):
    """Pure projection: base rows + this session's audited entries."""
    audit = json.loads((ROOT / "data" / AUDIT_NAME).read_text())
    captures, decisions, candidates = audit["captures"], audit["decisions"], audit["candidates"]
    if set(candidates) != set(decisions):
        raise ValueError(f"Candidate/decision mismatch in {AUDIT_NAME}")
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
            "as_of": decision["reviewed_at"],
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
    new_sources = dict(sources)
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
    sources_out = {key: new_sources[key] for key in sorted(new_sources)}

    listed = [r for r in combined if r["publication"] == "listed"]
    kinds = Counter(r["kind"] for r in listed)
    blank_fields = {field: sum(not r[field] for r in listed) for field in FIELDS}
    summary_out = dict(summary)
    summary_out.update({
        "candidates": len(combined),
        "new_research_entries": summary.get("new_research_entries", 0) + len(added),
        "listed": len(listed),
        "review_only": len(combined) - len(listed),
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
        "title": "Free-first gap research pass (session d57e2eeb)",
        "detail": (
            f"{len(added)} entries were added from official operator, venue, government and "
            "community pages read on 18 October 2026: the Cable Car Museum, Randall Museum, San "
            "Francisco Railway Museum, Fort Point NHS, Presidio Officers' Club free exhibitions "
            "and Musée Mécanique; the Golden Gate Park gardens' free hours (Japanese Tea Garden "
            "M/W/F hour, Conservatory of Flowers free first Tuesdays, Botanical Garden daily early "
            "entry and free second Tuesdays); free music beyond the big festivals (weekly Noontime "
            "Concerts at Old St. Mary's, Grace Cathedral free Choral Evensong, the annual People in "
            "Plazas series); gaming additions (Gamescape's weekly Board Game Night, plus Musée "
            "Mécanique); recurring SF AI/tech community channels (AI Tinkerers SF, The AI Collective "
            "SF chapter, Noisebridge's Circuit Hacking Mondays and monthly Five Minutes of Fame); "
            "the free SF Shakespeare Festival parks season, Circus Bella's free Union Square "
            "juggling lessons, and the 2026 Bay Area Science Festival at UCSF Mission Bay. One "
            "explicitly paid event — Circus Bella's BRAVURA Big Top — is published with a Paid "
            "badge, kept distinct from the free-first entries. Every value is quoted from the "
            "archived page text; blank cells stay blank and are labelled 'Not stated'. Six "
            "irregularities found on official pages themselves (conflicting season-closing and "
            "tour dates at circusbella.org, a stale next-event link and year mix-up on the "
            "Noisebridge wiki, a year-less upcoming listing on aicollective.com, two-digit years "
            "on gamescapesf.store, and Grace Cathedral's free service vs paid sightseeing) are "
            "quoted verbatim and flagged on the rows rather than silently reconciled. Five pages "
            "were read through the workspace search tool's verbatim result text rather than a "
            "direct fetch (museemecanique.com, streetcar.org/museum, gamescapesf.com, "
            "gracecathedral.org/calendar-events, ucsf.edu news); those captures record no HTTP "
            "status and are labelled as such."
        ),
        "urls": [
            "https://www.cablecarmuseum.org/info.html",
            "https://randallmuseum.org/directions-hours/",
            "https://www.nps.gov/fopo/planyourvisit/fees.htm",
            "https://noontimeconcerts.org/",
            "https://gracecathedral.org/series/choral-evensong/",
            "https://gggp.org/tickets/",
            "https://www.gamescapesf.store/events",
            "https://www.circusbella.org/bigtop",
            "https://sfshakes.org/performance/free-shakes/",
            "https://bayareasciencefestival.org/",
        ],
    }]
    return combined, sources_out, findings_out, summary_out


def apply_extension() -> None:
    """Read the files written by the earlier overlays, extend, write back."""
    names = ("events.json", "sources.json", "review.json", "audit_summary.json")
    rows, sources, findings, summary = (json.loads((ROOT / "data" / name).read_text()) for name in names)
    combined, sources_out, findings_out, summary_out = extend(rows, sources, findings, summary)
    for name, value in zip(names, (combined, sources_out, findings_out, summary_out)):
        (ROOT / "data" / name).write_text(json.dumps(value, indent=1, ensure_ascii=False) + "\n")
    print(f"Extension {SESSION}: +{len(combined) - len(rows)} entries; "
          f"{summary_out['listed']} listed / {summary_out['review_only']} review-only; "
          f"{summary_out['source_urls']} source URLs.")
