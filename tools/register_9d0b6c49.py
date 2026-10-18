#!/usr/bin/env python3
"""Additive, fail-closed overlay for the 9d0b6c49 verification + gap pass (T-9d0b-1/2).

It mirrors tools/register_d57e2eeb.py exactly — same field rules, same publication
tests — but touches ONLY the new candidates declared in data/audit_9d0b6c49.json:
free, dated, city-of-San-Francisco entries read from official City, community-district
and organizer pages on 2026-10-18 that the earlier registers did not cover.

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

This module never edits a row produced by the earlier audited overlays. It also
appends two review findings that publish this session's independent re-verification
of already-listed rows and the irregularities it found; findings are documentation
and never mutate a curated field value.
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
AUDIT_NAME = "audit_9d0b6c49.json"
SESSION = "9d0b6c49"


def extend(rows, sources, findings, summary):
    """Pure projection: base rows + this session's audited entries and findings."""
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
        # This pass is reported separately: it is an independent verification +
        # gap pass, not the gaming/music/AI research pass, so its entries must not
        # be folded into that counter and mis-attributed in the published analysis.
        "new_research_entries": summary.get("new_research_entries", 0),
        "verification_pass_entries": len(added),
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
        "title": "Independent re-verification pass (session 9d0b6c49)",
        "detail": (
            "Every row that leads the free-first landing page, and the whole priced section, was re-read "
            "against its own cited official page on 18 October 2026 with the workspace fetch tool; no "
            "value was accepted from memory or from an earlier session's note. Thirteen official pages "
            "were read directly. Result: the quoted date, time, venue and admission wording of the "
            "landing rows is unchanged and correct on noontimeconcerts.org, gracecathedral.org, "
            "litquake.org/litcrawl, dftsf.com, bhangraandbeats.com, downtownsf.org, "
            "sunsetmercantilesf.com, carnavalsanfrancisco.org, the nps.gov Sea Chantey Sing event page "
            "and sfmoma.org. Four irregularities are published rather than silently reconciled. "
            "(1) ybgfestival.org now answers a direct fetch with a reCAPTCHA challenge, so the two Yerba "
            "Buena Gardens Festival rows could only be re-read through the search tool's verbatim text "
            "for that exact official URL; their own event pages name a more precise venue than the "
            "published cell (Great Lawn for the Afro-Filipino Jazz Project, Children's Garden for "
            "Halloween Hoopla) and both are quoted in the research log, but the published venue cell is "
            "left untouched because it is already supported. (2) SFMOMA's Free Family Day page states "
            "'Free with RSVP' and excepts one exhibition — 'RM x SFMOMA: Between You and Me, which "
            "requires a timed ticket' with 'a surcharge of $12 for adults' — so the free badge is right "
            "for the event but the row's quoted wording does not carry that exception. (3) Noontime "
            "Concerts' 12:30 pm time is the wording 'Live Stream Starts at 12:30PM'; the homepage does "
            "not print a separate in-person start time. (4) Lit Crawl's page prints 'all programs from "
            "6:30—7:30 PM' immediately after a list of three venue changes, so its scope is ambiguous "
            "and the row's time cell stays blank rather than adopting it. Reachability of every cited "
            "URL remains a CI gate, not a claim made here."
        ),
        "urls": [
            "https://noontimeconcerts.org/",
            "https://gracecathedral.org/series/choral-evensong/",
            "https://www.litquake.org/litcrawl",
            "https://www.dftsf.com/",
            "https://www.bhangraandbeats.com/",
            "https://downtownsf.org/things-to-do/lets-glow-sf",
            "https://sunsetmercantilesf.com/sunsetholidaymercantile/",
            "https://carnavalsanfrancisco.org/",
            "https://www.nps.gov/planyourvisit/event-details.htm?id=2B52B414-F0EF-9707-2656479F9CAE0CBD",
            "https://www.sfmoma.org/event/free-family-day-k-pop-art-and-beyond/",
            "https://ybgfestival.org/",
            "https://www.mlb.com/giants/fans/fanfest",
            "https://chineseparade.com/faq/",
            "https://about.asianart.org/ticketing/free-and-reduced-museum-admission/",
        ],
    }, {
        "title": "Cost badge corrected: three free events were filed under Paid (session 9d0b6c49)",
        "detail": (
            "The cost badge is a label over the verified admission wording, and its tie-break rule sent "
            "every sentence containing both a free phrase and a price to the Paid section. Three rows "
            "were therefore labelled Paid while the official sentence printed beside the badge says the "
            "event itself is free: Giants FanFest / Open House at Oracle Park ('Free tickets are required "
            "for all FanFest Tour stops and the Open House.'), the San Francisco Chinese New Year Parade "
            "('It is a free event for all to attend but tickets must be purchased to sit in the bleacher "
            "sections.') and the Asian Art Museum's Free First Sunday ('general admission is free and "
            "tickets to our special exhibitions are offered at a discounted price of $15'). All three "
            "pages were re-read on 18 October 2026 and the wording is unchanged. The rule now resolves a "
            "mixed sentence by asking which wording governs entry, using two literal pattern sets drawn "
            "from quoted official sentences; a row matching neither keeps the conservative Paid reading, "
            "so no genuine price was relabelled free. Each corrected row carries the 'Conditions apply — "
            "read the exact wording' qualifier because money is still mentioned. No curated field value "
            "changed. Cost split moves from Free 75 / Paid 20 / Not stated 117 to Free 78 / Paid 17 / "
            "Not stated 117, and the free upcoming landing set from 15 to 16 with the Chinese New Year "
            "Parade on 20 February 2027. Five rows keep a correct Paid badge because their free wording "
            "applies only to a subset or only after paying: Boo at the Zoo, After Dark, RM x SFMOMA, The "
            "Haunt and BRAVURA."
        ),
        "urls": [
            "https://www.mlb.com/giants/fans/fanfest",
            "https://chineseparade.com/faq/",
            "https://about.asianart.org/ticketing/free-and-reduced-museum-admission/",
            "https://www.sfzoo.org/event/boo-at-the-zoo",
            "https://www.sfmoma.org/exhibition/rm-x-sfmoma/",
        ],
    }, {
        "title": "Free-first gap research pass (session 9d0b6c49)",
        "detail": (
            f"{len(added)} free entries were added from official pages read on 18 October 2026: Chess and "
            "Mahjong at United Nations Plaza (City Recreation and Park Department calendar, 'Cost: Free', "
            "with the weekly Friday cadence quoted from the Civic Center Community Benefit District's own "
            "page and a dated 23 October 2026 instance from the City calendar) — the first free gaming "
            "entry in the register with a confirmed upcoming date; the City's Free Dance Fitness Class by "
            "Rae Studios at UN Plaza, with eleven dated free instances and its time cell deliberately "
            "blank because the calendar prints a different start time per date; and two free Community "
            "Music Center concerts at CMC Concert Hall, 544 Capp Street — the Halloween Party & Costume "
            "Parade on 28 October 2026 and From Baroque to Cinema on 8 November 2026, both listed as "
            "'Cost: Free' on sfcmc.org and both tagged Music from the organizer's own description rather "
            "than from their names. Held off this overlay and logged instead: Gamebridge / Showcase "
            "Showdown at Noisebridge, whose official copy conflicts on both weekday and time "
            "(noisebridge.net's tour page says 'Tuesdays @ 7pm', the organizer's own class page says "
            "'6-8PM PST Wednesdays', the meetup listing says '7-9ish PM PST Wednesdays') and whose "
            "venue's continuing operation is the subject of current local reporting, so no cadence, time "
            "or future date is asserted. No new free AI/technology entry with a confirmed upcoming date "
            "was found in this pass; the AI section stays as published and the gap is recorded as an "
            "open research item rather than filled by inference."
        ),
        "urls": [
            "https://www.sfrecpark.org/Calendar.aspx?CID=40",
            "https://sfrecpark.org/Calendar.aspx?EID=10596&month=9&year=2026&day=3&calType=0",
            "https://sfciviccenter.org/event/learn-and-play-chess-at-un-plaza/",
            "https://sfcmc.org/events/",
            "https://www.noisebridge.net/wiki/Tour",
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
