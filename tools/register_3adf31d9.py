#!/usr/bin/env python3
"""Additive, fail-closed overlay for the 3adf31d9 new-requirement research (T33–T36).

It mirrors the discipline of tools/audited_register.py but touches ONLY the new
candidates declared in data/audit_3adf31d9.json — gaming, music and AI/technology
gatherings inside San Francisco that the earlier registers did not cover.

Rules enforced here, before anything is written:

  * every approved value carries an exact HTTPS quotation that is present in the
    archived capture text for that URL (whitespace/NFKC-normalised substring test);
  * a blank field never receives a value, and an unapproved field stays blank;
  * Weekly / Monthly / Annual require their own recurrence quotation;
  * an occurrence date must be recoverable from its own quotation (year, month, day);
  * publication to the directory requires an approved name, venue and confirmed
    San Francisco geography;
  * the whole projection is pure and idempotent: extend() applied to the same base
    data always returns byte-identical results, so a rebuild cannot drift.

This module never edits a row produced by the earlier audited overlay.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
AUDIT_NAME = "audit_3adf31d9.json"
SNAPSHOT = "2026-10-18"
FIELDS = ("name", "schedule", "time", "venue", "price")
KINDS = {"Weekly", "Monthly", "Annual", "Special", "Unverified"}
CATEGORIES = {"Markets & food", "Museums & science", "Festivals & culture", "Community & outdoors"}
TOPICS = ("Gaming", "Music", "AI & technology", "Other")

# --------------------------------------------------------------------------
# Editorial topic tags. These are presentation labels derived from the verified
# event name (or, for this session's own entries, from an explicit decision).
# They are NOT a verified field: no topic changes a fact, a date or a source.
# --------------------------------------------------------------------------
TOPIC_OVERRIDES = {
    "audit-illuminate-live-2026": "Music",
    "b-noise-pop-festival": "Music",
    "x-jerry-day": "Music",
    "x-valencia-live": "Music",
    "x-pokemon-world-championships": "Gaming",
    "audit-civic-center-soundtrack-2026": "Music",
}
GAMING_WORDS = (
    "chess", "board game", "game night", "gaming", "pokemon", "pokémon", "esports",
    "gdc festival", "go club", "mahjong", "tabletop", "arcade", "video game",
    "dungeons", "pinball", "jenga", "bingo", "trivia",
)
MUSIC_WORDS = (
    "concert", "music", "jazz", "bluegrass", "opera", "symphony", "band", "choir",
    "folk", "dj ", "k-pop", "piano", "guitar", "blues", "reggae", "salsa", "carol",
    "soundtrack", "a cappella", "song", "bhangra", "orchestra", "chorus", "sing",
)
AI_WORDS = (
    "artificial intelligence", "machine learning", "data + ai", "data and ai",
    "ai engineer", "ai council", "iclr", "tdx", "agentic", "techcrunch",
    "developer conference", "semicon", "cloudflare connect",
)


def topic_of(row) -> str:
    """Editorial topic tag. Explicit decisions win; otherwise the verified name only."""
    explicit = row.get("topic")
    if explicit in TOPICS:
        return explicit
    if row["id"] in TOPIC_OVERRIDES:
        return TOPIC_OVERRIDES[row["id"]]
    name = (row["name"] or "").casefold()
    if any(word in name for word in GAMING_WORDS) or re.search(r"\bgdc\b", name):
        return "Gaming"
    if re.search(r"\bai\b|a\.i\.", name) or any(word in name for word in AI_WORDS):
        return "AI & technology"
    if any(word in name for word in MUSIC_WORDS):
        return "Music"
    return "Other"


# --------------------------------------------------------------------------
# Cost badge. The badge is a LABEL over the verified admission text; the exact
# official wording is always rendered next to it. Nothing is inferred: a blank
# price is "Not stated", never "Free".
# --------------------------------------------------------------------------
PAID_PATTERNS = (
    r"\$\s?\d", r"\d+\s?(?:usd|dollars)", r"ticket[s]?\s+(?:are|is|start)",
    r"paid\s+(?:daytime\s+)?admission", r"paid\s+entry", r"admission\s+is\s+\$",
    r"general\s+admission\s+is\s+\$", r"separate\s+evening\s+ticket",
    r"tickets?\s+(?:required|must)", r"entry\s+fee", r"admission\s+fee",
    r"members\s+only", r"reservation[s]?\s+required", r"cover\s+charge",
)
FREE_PATTERNS = (
    r"\bfree\b", r"no\s+tickets?\s+needed", r"admission[ -]free",
    r"free\s+admission", r"no\s+cover", r"free\s+with\s+rsvp",
)
CONDITION_PATTERNS = (
    r"with\s+paid", r"members", r"membership", r"rsvp", r"registration\s+is\s+required",
    r"residency", r"resident", r"lottery", r"suggested", r"donation",
)

# When one verified admission sentence mentions BOTH "free" and money, the badge must
# follow whichever wording governs *entry itself*. Previously every such row was forced
# to "Paid", which mislabelled three rows whose own quoted official sentence says the
# event is free and the money buys an optional extra. Each pattern below is a literal
# phrase lifted from a quoted official sentence already in the register — the badge
# never reads meaning into text that was not quoted.
FREE_GOVERNS_ENTRY = (
    # "Free tickets are required for all FanFest Tour stops and the Open House."
    # https://www.mlb.com/giants/fans/fanfest — the required ticket costs nothing.
    r"free\s+tickets?\s+(?:are|is)\s+required",
    # "It is a free event for all to attend but tickets must be purchased to sit in
    # the bleacher sections." https://chineseparade.com/faq/ — attendance is free;
    # bleacher seating is an optional purchase.
    r"free\s+event\s+for\s+all\s+to\s+attend",
    # "general admission is free and tickets to our special exhibitions are offered at
    # a discounted price of $15"
    # https://about.asianart.org/ticketing/free-and-reduced-museum-admission/ — entry
    # is free; the special exhibition is an optional extra.
    r"general\s+admission\s+is\s+free",
)
PAID_GOVERNS_ENTRY = (
    r"free\s+with\s+paid",                    # "activities are free with paid daytime admission"
    r"paid\s+admission", r"paid\s+entry",     # entry itself costs money
    r"members\s+free", r"free\s+for\s+members",  # free only for a paying subset
    r"(?:kids|children)[^.]*\bfree\b",        # free only for children
)


def cost_of(row):
    """Return (badge, conditions_flag) for a row's verified admission text."""
    price = (row.get("price") or "").casefold()
    if not price.strip():
        return "Not stated", False
    paid = any(re.search(pattern, price) for pattern in PAID_PATTERNS)
    free = any(re.search(pattern, price) for pattern in FREE_PATTERNS)
    entry_split = False
    if paid and not free:
        badge = "Paid"
    elif free and not paid:
        badge = "Free"
    elif free and paid:
        # Decide from the quoted wording, not from the mere presence of a number.
        entry_free = any(re.search(pattern, price) for pattern in FREE_GOVERNS_ENTRY)
        entry_paid = any(re.search(pattern, price) for pattern in PAID_GOVERNS_ENTRY)
        if entry_free and not entry_paid:
            # Entry is free; the money in the sentence buys an optional extra.
            badge, entry_split = "Free", True
        else:
            # Conservative default, unchanged: e.g. "activities are free with paid
            # daytime admission" — entry is paid. A real price is never relabelled free.
            badge = "Paid"
    else:
        badge = "See source"
    conditions = entry_split or any(re.search(pattern, price) for pattern in CONDITION_PATTERNS)
    return badge, conditions


def normal(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def captured_text(capture) -> str:
    return normal(" ".join(capture.get(key, "") or "" for key in ("title", "text", "tool_excerpt")))


def iso(value: str) -> date:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"Not a full ISO event date: {value}")
    return date.fromisoformat(value)


def validate_quotes(quotes, captures) -> None:
    if not quotes:
        raise ValueError("A nonblank claim needs quotations")
    for quote in quotes:
        url, text = quote["url"], quote["text"]
        if urlsplit(url).scheme != "https" or not normal(text):
            raise ValueError(f"Empty or non-HTTPS quotation: {quote}")
        if url not in captures:
            raise ValueError(f"Quotation cites a URL with no archived capture: {url}")
        if normal(text) not in captured_text(captures[url]):
            raise ValueError(f"Quotation absent from archived evidence: {url}: {text[:120]}")


def validate_decision(decision, captures) -> None:
    if decision["publication"] not in {"listed", "review_only"} or decision["kind"] not in KINDS:
        raise ValueError("Unknown disposition or cadence")
    iso(decision["reviewed_at"])
    if decision["reviewed_at"] > SNAPSHOT:
        raise ValueError("Review date is later than this fixed research snapshot")
    for field, fact in decision["fields"].items():
        if field not in FIELDS or not isinstance(fact["value"], str) or not fact["value"].strip():
            raise ValueError(f"Invalid field decision: {field}")
        validate_quotes(fact["quotes"], captures)
    recurrence = decision.get("recurrence")
    if recurrence:
        if not recurrence.get("value"):
            raise ValueError("Recurrence needs an explicit approved value")
        validate_quotes(recurrence["quotes"], captures)
    if decision["kind"] in {"Weekly", "Monthly", "Annual"} and not recurrence:
        raise ValueError("A recurring classification needs its own recurrence evidence")
    geography = decision["geography"]
    if geography["status"] == "confirmed_sf":
        validate_quotes(geography["quotes"], captures)
        if not geography.get("basis"):
            raise ValueError("City-only judgment needs a contextual basis")
    elif geography["status"] != "unverified":
        raise ValueError("Unknown geography status")
    if decision["publication"] == "listed":
        if geography["status"] != "confirmed_sf" or not all(decision["fields"].get(k) for k in ("name", "venue")):
            raise ValueError("Publication requires approved name, venue and city-only geography")
    months = ("", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    for occurrence in decision.get("occurrences", []):
        iso(occurrence["start"])
        if occurrence["end"] and iso(occurrence["end"]) < iso(occurrence["start"]):
            raise ValueError("Reversed occurrence span")
        validate_quotes(occurrence["quotes"], captures)
        quoted = normal(" ".join(quote["text"] for quote in occurrence["quotes"]))
        for value in (occurrence["start"], occurrence["end"]):
            if not value:
                continue
            event_date = iso(value)
            if str(event_date.year) not in quoted:
                raise ValueError(f"Occurrence year not present in approved quotations: {value}")
            numeric = re.search(rf"(?<![0-9])0?{event_date.month}[/.-]0?{event_date.day}[/.-]{event_date.year}(?![0-9])", quoted)
            named = months[event_date.month].casefold() in quoted.casefold() and re.search(rf"(?<![0-9])0?{event_date.day}(?![0-9])", quoted)
            if not (numeric or named or value in quoted):
                raise ValueError(f"Occurrence month/day not present in approved quotations: {value}")
    if decision.get("date_status", "confirmed") not in {"confirmed", "tentative"}:
        raise ValueError("Invalid date certainty")
    if decision.get("topic") not in TOPICS:
        raise ValueError("Unknown editorial topic tag")


def temporal(decision, as_of=SNAPSHOT) -> str:
    today = iso(as_of)
    spans = decision.get("occurrences", [])
    if decision.get("date_status") == "tentative":
        return "Tentative schedule"
    if not spans:
        return "Recurring pattern; next date unconfirmed" if decision.get("recurrence") else "Date/year unconfirmed"
    if any(iso(x["start"]) <= today and x["end"] and today <= iso(x["end"]) for x in spans):
        return "On snapshot date" if all(x["end"] == x["start"] for x in spans) else "Spans snapshot date"
    if any(iso(x["start"]) > today for x in spans):
        return "Future dated"
    if any(not x["end"] and iso(x["start"]) <= today for x in spans):
        return "Opened; closing unconfirmed"
    return "Past dated"


def next_date(row):
    """Earliest occurrence that has not finished before the snapshot; else None."""
    spans = [(o["start"], o["end"]) for o in row.get("occurrences", [])]
    upcoming = sorted(s for s, e in spans if not e or e >= SNAPSHOT)
    return upcoming[0] if upcoming else None


def quote_urls(decision):
    quotes = [quote for fact in decision["fields"].values() for quote in fact["quotes"]]
    if decision.get("recurrence"):
        quotes += decision["recurrence"]["quotes"]
    quotes += decision["geography"]["quotes"]
    quotes += [quote for occurrence in decision.get("occurrences", []) for quote in occurrence["quotes"]]
    return list(dict.fromkeys(quote["url"] for quote in quotes))


def extend(rows, sources, findings, summary):
    """Pure projection: base rows + this session's audited entries."""
    audit = json.loads((ROOT / "data" / AUDIT_NAME).read_text())
    captures, decisions, candidates = audit["captures"], audit["decisions"], audit["candidates"]
    if set(candidates) != set(decisions):
        raise ValueError("Candidate/decision mismatch in audit_3adf31d9.json")
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
        "new_research_entries": len(added),
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
        "title": "Gaming, music and AI research pass (session 3adf31d9)",
        "detail": (
            f"{len(added)} entries were added from official organizer, venue, library and conference pages: "
            "GDC Festival of Gaming; the San Francisco Scholastic Chess Championship and Mechanics' Institute "
            "chess programmes; San Francisco Public Library chess, board-game and Chinese-chess clubs; the AI "
            "Engineer World's Fair, TDX, ICLR, Data + AI Summit and AI Council conferences; and the Stern Grove "
            "Festival. Every value is quoted from the page that was read on 18 October 2026. Where a page states "
            "no admission, the price cell is blank and labelled 'Not stated' — never 'Free'. Two candidates are "
            "held for review because the captured official text names no venue (Mechanics' Institute Introduction "
            "to Chess) or no venue at all (AI Council 2027). Several sources were read through the workspace "
            "search tool's verbatim result text rather than a full page fetch (sfpl.org's branch navigation and "
            "the Stern Grove contact block); those captures record no HTTP status and are labelled as such."
        ),
        "urls": [
            "https://gdconf.com/",
            "https://www.milibrary.org/chess/tournaments/2026-san-francisco-scholastic-chess-championship",
            "https://www.sterngrove.org/about-us",
            "https://ai.engineer/worldsfair/2027",
            "https://iclr.cc/Conferences/2027/index.html",
        ],
    }, {
        "title": "Topic tags and cost badges are labels, not verified fields",
        "detail": (
            "The Gaming / Music / AI & technology tags are editorial presentation labels derived from the verified "
            "event name (or from this session's explicit decision). A tag never changes a fact, a date or a source, "
            "and it is not evidence that an event belongs to a genre. The Free / Paid / Not stated badge is computed "
            "only from the verified admission text quoted from the official page, and the exact official wording is "
            "always shown next to the badge. A blank admission cell is 'Not stated', never 'Free'."
        ),
        "urls": [],
    }]
    return combined, sources_out, findings_out, summary_out


def apply_extension() -> None:
    """Read the files written by audited_register.apply_audit, extend, write back."""
    names = ("events.json", "sources.json", "review.json", "audit_summary.json")
    rows, sources, findings, summary = (json.loads((ROOT / "data" / name).read_text()) for name in names)
    combined, sources_out, findings_out, summary_out = extend(rows, sources, findings, summary)
    for name, value in zip(names, (combined, sources_out, findings_out, summary_out)):
        (ROOT / "data" / name).write_text(json.dumps(value, indent=1, ensure_ascii=False) + "\n")
    print(f"Extension 3adf31d9: +{len(combined) - len(rows)} entries; "
          f"{summary_out['listed']} listed / {summary_out['review_only']} review-only; "
          f"{summary_out['source_urls']} source URLs.")


if __name__ == "__main__":
    raise SystemExit("Run tools/consolidate.py so the audited overlay is always the final stage.")
