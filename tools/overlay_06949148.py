#!/usr/bin/env python3
"""Reconcile two independently re-read official-source findings from stale T32.

This is a final integration overlay, not a replacement for the canonical audit or
for the newer 3adf31d9 / 21f3dd85 / d57e2eeb research overlays. It changes only
existing rows named in data/audit_06949148.json, validates every applied quotation
against its supplemental capture, and preserves unresolved conflicting hours as
blank. No stale generated pages or old validation code are copied into mainline.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlsplit

from audited_register import FIELDS, normal, validate_quotes
from register_3adf31d9 import cost_of, next_date, topic_of

ROOT = Path(__file__).resolve().parents[1]
AUDIT_NAME = "audit_06949148.json"
FOODWISE_URL = "https://foodwise.org/markets/alemany-farmers-market/"
SFE_URL = "https://www.sfenvironment.org/farmers-markets-in-sf"


def _load_audit():
    audit = json.loads((ROOT / "data" / AUDIT_NAME).read_text())
    if audit.get("session") != "06949148" or audit.get("snapshot_date") != "2026-10-18":
        raise ValueError(f"Unexpected scope or snapshot in {AUDIT_NAME}")
    for url, capture in audit.get("captures", {}).items():
        if capture.get("http") is not None:
            raise ValueError(f"A numeric HTTP status was not exposed by the retrieval tool: {url}")
    return audit


def _add_source_reference(source, row_id):
    refs = source.setdefault("approved_for_rows", [])
    if row_id not in refs:
        refs.append(row_id)


def extend(rows, sources, findings, summary):
    """Pure projection: apply only the two explicit audit dispositions."""
    audit = _load_audit()
    captures = audit["captures"]
    changes = {change["row_id"]: change for change in audit["changes"]}
    expected_ids = {"x-oktoberfest-on-front", "b-alemany-farmers-market"}
    if set(changes) != expected_ids:
        raise ValueError(f"Unexpected overlay rows in {AUDIT_NAME}: {sorted(changes)}")

    rows_out = deepcopy(rows)
    sources_out = deepcopy(sources)
    findings_out = deepcopy(findings)
    summary_out = dict(summary)
    by_id = {row["id"]: row for row in rows_out}
    if len(by_id) != len(rows_out):
        raise ValueError("Duplicate row ids before 06949148 integration")
    if not expected_ids <= set(by_id):
        raise ValueError(f"T32 target row missing: {sorted(expected_ids - set(by_id))}")

    # Exact event-host admission wording. This row's approved date is past as of
    # the fixed snapshot, so the correction does not add it to free-upcoming.
    okt = by_id["x-oktoberfest-on-front"]
    price_change = changes["x-oktoberfest-on-front"]
    quote = price_change["quote"]
    validate_quotes([quote], captures)
    if price_change["field"] != "price" or price_change["value"] != quote["text"]:
        raise ValueError("Oktoberfest price must be the exact official quotation")
    if okt["price"] or "price" in okt["field_evidence"]:
        raise ValueError("Refusing to overwrite an existing Oktoberfest price decision")
    if "price: unverified" not in okt["unverified"]:
        raise ValueError("Oktoberfest's original blank price must be marked unverified")
    okt["price"] = price_change["value"]
    okt["field_evidence"]["price"] = {
        "value": price_change["value"],
        "quotes": [deepcopy(quote)],
    }
    okt["unverified"] = [item for item in okt["unverified"] if item != "price: unverified"]
    okt["flags"] = [price_change["row_flag"]]

    # Alemany remains time-blank. Link both the current operator corroboration
    # and the dated City Environment page that carries the disagreeing hours.
    ale = by_id["b-alemany-farmers-market"]
    alemany_change = changes["b-alemany-farmers-market"]
    for context_quote in alemany_change["context_quotes"]:
        validate_quotes([context_quote], captures)
    geography_quote = alemany_change["geography_quote"]
    validate_quotes([geography_quote], captures)
    if alemany_change["field"] != "time" or alemany_change["value"] != "":
        raise ValueError("Alemany's conflicting time must remain blank")
    if ale["time"] or "time" in ale["field_evidence"]:
        raise ValueError("Refusing to silently fill or overwrite Alemany hours")
    if "time: unverified" not in ale["unverified"]:
        raise ValueError("Alemany's unresolved time must remain marked unverified")
    if not any(q.get("url") == geography_quote["url"] and q.get("text") == geography_quote["text"]
               for q in ale["geography"]["quotes"]):
        ale["geography"]["quotes"].append(deepcopy(geography_quote))
    ale["flags"] = [alemany_change["row_flag"]]

    url_to_id = {source["url"]: sid for sid, source in sources_out.items()}
    if len(url_to_id) != len(sources_out):
        raise ValueError("Duplicate source URLs before 06949148 integration")
    if FOODWISE_URL in url_to_id:
        foodwise_id = url_to_id[FOODWISE_URL]
    else:
        foodwise_id = "n-" + hashlib.sha256(FOODWISE_URL.encode()).hexdigest()[:12]
        capture = captures[FOODWISE_URL]
        sources_out[foodwise_id] = {
            "url": FOODWISE_URL,
            "publisher": "foodwise.org",
            "title": capture["title"],
            "source_role": "Official cited page; link alone is not a verified fact",
            "captured_at": "",
            "http": None,
            "tool_excerpt_available": True,
            "tool_checked_at": capture["tool_checked_at"],
            "audit_snapshot": f"data/{AUDIT_NAME}",
            "retrieval": deepcopy(capture["retrieval"]),
            "approved_for_rows": [],
        }
    if SFE_URL not in url_to_id:
        raise ValueError("The cited SF Environment conflict source is missing from the source ledger")
    sfe_id = url_to_id[SFE_URL]
    for sid in (sfe_id, foodwise_id):
        if sid not in ale["sources"]:
            ale["sources"].append(sid)
        _add_source_reference(sources_out[sid], ale["id"])

    finding = deepcopy(audit["review_finding"])
    if any(item.get("title") == finding["title"] for item in findings_out):
        raise ValueError("Duplicate 06949148 review finding")
    findings_out.append(finding)
    sources_sorted = {sid: sources_out[sid] for sid in sorted(sources_out)}

    # Recompute metrics from the projected rows so the free / paid / not-stated
    # counts, blank-field totals, and source ledger remain in sync.
    listed = [row for row in rows_out if row["publication"] == "listed"]
    summary_out.update({
        "candidates": len(rows_out),
        "listed": len(listed),
        "review_only": len(rows_out) - len(listed),
        "series": sum(row["entry_type"] == "series" for row in listed),
        "source_urls": len(sources_sorted),
        "domains": len({urlsplit(source["url"]).netloc.removeprefix("www.")
                         for source in sources_sorted.values()}),
        "kinds": dict(Counter(row["kind"] for row in listed)),
        "categories": dict(Counter(row["category"] for row in listed)),
        "temporal": dict(Counter(row["temporal_status"] for row in listed)),
        "blank_fields": {field: sum(not row[field] for row in listed) for field in FIELDS},
        "listed_with_blanks": sum(bool(row["unverified"]) for row in listed),
        "supported_field_values": summary.get("supported_field_values", 0) + 1,
        "topics": dict(Counter(topic_of(row) for row in listed)),
        "cost": dict(Counter(cost_of(row)[0] for row in listed)),
        "upcoming_dated": sum(1 for row in listed if next_date(row)),
    })
    return rows_out, sources_sorted, findings_out, summary_out


def apply_extension() -> None:
    """Read the current integrated register, apply the audited overlay, write outputs."""
    names = ("events.json", "sources.json", "review.json", "audit_summary.json")
    rows, sources, findings, summary = (
        json.loads((ROOT / "data" / name).read_text()) for name in names
    )
    rows_out, sources_out, findings_out, summary_out = extend(rows, sources, findings, summary)
    for name, value in zip(names, (rows_out, sources_out, findings_out, summary_out)):
        (ROOT / "data" / name).write_text(json.dumps(value, indent=1, ensure_ascii=False) + "\n")
    print(
        "T32 reconciliation: price verified for Oktoberfest on Front; Alemany hours remain blank; "
        f"{len(rows_out)} candidates / {summary_out['listed']} directory / "
        f"{summary_out['review_only']} review-only; {summary_out['source_urls']} source URLs."
    )


if __name__ == "__main__":
    raise SystemExit("Run tools/consolidate.py so all audit overlays are rebuilt in order.")
