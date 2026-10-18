#!/usr/bin/env python3
"""Fail-closed publication overlay. Legacy inputs are candidates, never evidence.

Called LAST by consolidate.py. No network, fuzzy name matching, date parsing from
prose/URLs, or inherited verification labels. Each accepted field is an explicit
review decision with exact source quotations. Quotation provenance is testable;
contextual applicability remains a recorded research judgment, not an algorithm.
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
FIELDS = ("name", "schedule", "time", "venue", "price")
KINDS = {"Weekly", "Monthly", "Annual", "Special", "Unverified"}
CATEGORIES = {"Markets & food", "Museums & science", "Festivals & culture", "Community & outdoors"}
SNAPSHOT = "2026-10-18"


def normal(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip()


def captured_text(capture, fmt="text"):
    if fmt == "jsonld":
        return normal(json.dumps(capture.get("structured", []), ensure_ascii=False))
    if fmt != "text":
        raise ValueError(f"Unsupported evidence format: {fmt}")
    return normal(" ".join(capture.get(k, "") for k in ("title", "text", "tool_excerpt")))


def validate_quotes(quotes, captures):
    if not quotes:
        raise ValueError("A nonblank claim needs quotations")
    for quote in quotes:
        url, text = quote["url"], quote["text"]
        if urlsplit(url).scheme != "https" or not normal(text):
            raise ValueError(f"Empty or non-HTTPS quotation: {quote}")
        if url not in captures or normal(text) not in captured_text(captures[url], quote.get("format", "text")):
            raise ValueError(f"Quotation absent from archived evidence: {url}: {text[:120]}")


def iso(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"Not a full ISO event date: {value}")
    return date.fromisoformat(value)


def validate_decision(decision, captures):
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
    for occurrence in decision.get("occurrences", []):
        iso(occurrence["start"])
        if occurrence["end"] and iso(occurrence["end"]) < iso(occurrence["start"]):
            raise ValueError("Reversed occurrence span")
        validate_quotes(occurrence["quotes"], captures)
        quoted = normal(" ".join(q["text"] for q in occurrence["quotes"]))
        months = ("", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
        for value in (occurrence["start"], occurrence["end"]):
            if not value:
                continue
            event_date = iso(value)
            # Provenance guard against supplying a year from a URL or an unrelated
            # inference. Semantic applicability still requires contextual review.
            if str(event_date.year) not in quoted:
                raise ValueError(f"Occurrence year not present in approved quotations: {value}")
            numeric = re.search(rf"(?<![0-9])0?{event_date.month}[/.-]0?{event_date.day}[/.-]{event_date.year}(?![0-9])", quoted)
            named = months[event_date.month].casefold() in quoted.casefold() and re.search(rf"(?<![0-9])0?{event_date.day}(?![0-9])", quoted)
            if not (numeric or named or value in quoted):
                raise ValueError(f"Occurrence month/day not present in approved quotations: {value}")
    if decision.get("date_status", "confirmed") not in {"confirmed", "tentative"}:
        raise ValueError("Invalid date certainty")


def temporal(decision, as_of=SNAPSHOT):
    """Only explicitly approved ISO dates participate. No prose/URL year inference."""
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


def quote_urls(decision):
    quotes = [q for fact in decision["fields"].values() for q in fact["quotes"]]
    if decision.get("recurrence"):
        quotes += decision["recurrence"]["quotes"]
    quotes += decision["geography"]["quotes"]
    quotes += [q for occurrence in decision.get("occurrences", []) for q in occurrence["quotes"]]
    return list(dict.fromkeys(q["url"] for q in quotes))


def compile_register(legacy_rows, legacy_sources, legacy_findings, audit):
    """Pure projection; every candidate must be reviewed, or the build fails."""
    candidates = deepcopy(legacy_rows)
    for extra in audit.get("extra_events", []):
        candidates.append({**deepcopy(extra), "sources": [], "research_origin": "new official-calendar research"})
    ids = [r["id"] for r in candidates]
    decisions, captures = audit["decisions"], audit["captures"]
    if len(ids) != len(set(ids)) or set(ids) != set(decisions):
        raise ValueError(f"Candidate/decision mismatch: missing={set(ids)-set(decisions)}, extra={set(decisions)-set(ids)}")
    # Deduplicate URL records, while retaining every original URL for candidate review.
    by_url = {}
    for key, source in legacy_sources.items():
        by_url.setdefault(source["url"], (key, source))
    for decision in decisions.values():
        validate_decision(decision, captures)
        for url in quote_urls(decision):
            by_url.setdefault(url, ("audit-" + hashlib.sha256(url.encode()).hexdigest()[:12], {}))
    used_urls = set()
    rows = []
    for candidate in candidates:
        rid = candidate["id"]
        d = decisions[rid]
        original_urls = [legacy_sources[s]["url"] for s in candidate.get("sources", [])]
        urls = list(dict.fromkeys(quote_urls(d) + original_urls))
        if not urls:
            raise ValueError(f"No official source link for {rid}")
        used_urls.update(urls)
        missing = [f"{field}: unverified" for field in FIELDS if field not in d["fields"]]
        if d["geography"]["status"] != "confirmed_sf":
            missing.append("geography: unverified; not admitted to city-only directory")
        if not d.get("recurrence"):
            missing.append("recurrence: unverified; no ongoing cadence asserted")
        if not d.get("occurrences") and d["kind"] not in {"Weekly", "Monthly", "Annual"}:
            missing.append("date/year: unverified; no approved ISO occurrence")
        rows.append({
            "id": rid,
            **{field: d["fields"].get(field, {}).get("value", "") for field in FIELDS},
            "candidate_name": candidate["name"],
            "candidate_label": "Unverified inherited identifier" if not candidate.get("research_origin") else "New research identifier",
            "category": candidate["category"],
            "kind": d["kind"],
            "entry_type": d.get("entry_type", "event"),
            "parent": d.get("parent", ""),
            "publication": d["publication"],
            "geography": deepcopy(d["geography"]),
            "recurrence": deepcopy(d.get("recurrence")),
            "occurrences": deepcopy(d.get("occurrences", [])),
            "date_status": d.get("date_status", "confirmed"),
            "temporal_status": temporal(d),
            "as_of": SNAPSHOT,
            "field_evidence": deepcopy(d["fields"]),
            "sources": [by_url[url][0] for url in urls],
            "unverified": missing,
            "flags": [d["reason"]] if d.get("reason") else [],
            "notes": d.get("notes", ""),
            "audit": {"session": audit["session"], "reviewed_at": d["reviewed_at"], "method": "Explicit contextual field decisions; incomplete fields remain blank"},
        })
    # Category/relationship labels are editorial, never inherited venue or date facts.
    row_ids = set(ids)
    for row in rows:
        if row["category"] not in CATEGORIES or row["parent"] and row["parent"] not in row_ids:
            raise ValueError(f"Invalid editorial grouping for {row['id']}")
        seen, current = {row["id"]}, row
        lookup = {r["id"]: r for r in rows}
        while current["parent"]:
            if current["parent"] in seen:
                raise ValueError("Cyclic programme relationship")
            seen.add(current["parent"])
            current = lookup[current["parent"]]
    sources = {}
    for url in sorted(used_urls):
        key, old = by_url[url]
        capture = captures.get(url, {})
        sources[key] = {
            "url": url,
            "publisher": old.get("publisher") or urlsplit(url).netloc.removeprefix("www."),
            "title": capture.get("title") or old.get("publisher") or urlsplit(url).netloc,
            "source_role": "Official cited page; link alone is not a verified fact",
            "captured_at": capture.get("checked_at", ""),
            "http": capture.get("http"),
            "tool_excerpt_available": bool(capture.get("tool_excerpt")),
            "tool_checked_at": capture.get("tool_checked_at") or (SNAPSHOT if capture.get("tool_excerpt") else ""),
            "latest_attempt": capture.get("latest_attempt"),
            "audit_snapshot": "data/audit_95ceac65.json",
            "approved_for_rows": [r["id"] for r in rows if url in quote_urls(decisions[r["id"]])],
        }
    listed = [r for r in rows if r["publication"] == "listed"]
    summary = {
        "as_of": SNAPSHOT, "candidates": len(rows), "inherited_candidates": len(legacy_rows),
        "new_entries": len(audit.get("extra_events", [])), "listed": len(listed),
        "review_only": len(rows) - len(listed), "series": sum(r["entry_type"] == "series" for r in listed),
        "source_urls": len(sources), "domains": len({urlsplit(s["url"]).netloc.removeprefix("www.") for s in sources.values()}),
        "kinds": dict(Counter(r["kind"] for r in listed)),
        "categories": dict(Counter(r["category"] for r in listed)),
        "temporal": dict(Counter(r["temporal_status"] for r in listed)),
        "blank_fields": {field: sum(not r[field] for r in listed) for field in FIELDS},
        "listed_with_blanks": sum(bool(r["unverified"]) for r in listed),
        "supported_field_values": sum(len(r["field_evidence"]) for r in rows),
        "limitation": "Bounded, non-exhaustive research snapshot; entries mix events and programme umbrellas, not a count of unique city events.",
    }
    findings = [
        {"title": "Publication gate and remaining uncertainty", "detail": f"{len(listed)} entries have an approved name, venue and San Francisco geography; {len(rows)-len(listed)} candidates are held off the directory. Every unapproved field is blank. A listed entry is not a claim that every fact is known.", "urls": []},
        {"title": "Dates are a fixed snapshot, not a live calendar", "detail": "Only approved ISO occurrences determine temporal labels relative to 18 October 2026. Yearless dates (Menorah, Cole Valley Nights, Taraval and others) are never promoted to upcoming dates. A 2027 banner does not date unrelated ancillary events; past editions are not moved forward.", "urls": []},
        {"title": "Regional and cross-boundary programmes quarantined", "detail": "Frameline, SF Art Week, SF Climate Week, NEXUS, Bay Area Dance Week, SF Beer Week, the Jewish Film Festival and the full SF Marathon require SF-only components/route evidence. This is not a finding that those events do not exist.", "urls": []},
        {"title": "Known corrections and conflicts", "detail": "Zoo resident day is October 7 (not a monthly first-Tuesday rule); Boo October 31 is 10am–3pm with paid admission/membership. Fiesta en el Parque is August 1. Opera Ball moved to November 12. Bhangra & Beats moved to Yerba Buena. Alemany hours, Secondhand/Muertos street extents and Jewish Film Festival year conflict remain flagged, not guessed. Nihonmachi’s 2027 venue is blank: its Japantown reference is in the prior-edition recap, not the future announcement. Oktoberfest on Front’s admission is now the official page’s explicit “FREE WITH RSVP”; its earlier blank was an unflagged omission. Alemany’s hours stay blank: SF.gov and operator Foodwise both state 7am–2pm while the older SF Environment directory (dated 03/21/2025, before the February 2026 operator changeover, and itself deferring to market websites) says 6am–3pm; the dissent is recorded, not silently resolved.", "urls": []},
        {"title": "Independent re-verification (session 95ceac65)", "detail": "A second audit session re-read a risk-prioritized sample of about sixty live official pages against every registered value: all 13 newest calendar entries, every flagged row, flagship recurring events, each cadence in each category, and the future-dated rows visitors plan around. Sampled values matched their official quotations except one omission (Oktoberfest on Front admission, now populated) and one documented conflict (Alemany hours, still blank with the operator’s corroboration archived). Sunset Mercantile street-extent conflicts persist live today; Rec Park Zumba and Yerba Buena Gardens Festival pages render client-side or behind reCAPTCHA, so their live re-reads are unknowns, not contradictions. Every URL the register actually cites was live at re-read time; no cited source was found dead in this sample.", "urls": []},
        {"title": "Concurrent research retained; Ferry Fest dead URL is historical only", "detail": "The f1fd3c36 audit and 99662c40 repair are preserved unchanged as candidate history, including Alemany Flea Market and Doc Stories. Newly located sources were independently re-read where possible; old field/page labels are not automatic approvals. Ferry Fest’s former https://www.ferrybuildingmarketplace.com/events/ferry-fest/ returned 404 in upstream CI run 39092990628 and is not active evidence. Its surviving SF Travel guide remains a review link; unsupported facts remain blank.", "urls": []},
        {"title": "Evidence and coverage limitations", "detail": "HTTP 200, a page title, a name match, a URL year, free parking, free refreshments, and an organization's domain suffix do not establish event facts, admission or nonprofit status. Blank cells are unverified. Commercial ticketing/JS pages, neighborhood micro-events, civic and faith calendars, sports fixtures and individual arts performances need further coverage. No claim of citywide completeness or ongoing automated fact verification is made.", "urls": []},
    ]
    return rows, sources, findings, summary


def apply_audit(legacy_rows, legacy_sources, legacy_findings):
    audit = json.loads((ROOT / "data/audit_95ceac65.json").read_text())
    rows, sources, findings, summary = compile_register(legacy_rows, legacy_sources, legacy_findings, audit)
    history = {"warning": "UNVERIFIED INHERITED HISTORY. Not current event facts; preserved for audit and must never be used as fallback values.", "events": legacy_rows, "sources": legacy_sources, "review_findings": legacy_findings}
    for filename, value in (("unverified_history.json", history), ("events.json", rows), ("sources.json", sources), ("review.json", findings), ("audit_summary.json", summary)):
        (ROOT / "data" / filename).write_text(json.dumps(value, indent=1, ensure_ascii=False) + "\n")
    print(f"AUDITED publication: {summary['listed']} SF entries; {summary['review_only']} review-only; {summary['new_entries']} new entries. Old field values never used as fallback.")


if __name__ == "__main__":
    raise SystemExit("Run tools/consolidate.py so the audited overlay is always the final stage.")
