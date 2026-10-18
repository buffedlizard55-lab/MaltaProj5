#!/usr/bin/env python3
"""Regression tests for the cost badge when one official sentence mentions both
"free" and money (session 9d0b6c49, T-9d0b-3).

The badge is a label over the *verified admission wording*, so it must follow the
wording that governs entry itself. Before this fix every row whose quoted sentence
contained both a free phrase and a price was forced to "Paid", which contradicted
the sentence printed next to the badge on three rows:

  x-giants-fanfest                  "Free tickets are required …"
  chinese                           "a free event for all to attend but tickets must
                                     be purchased to sit in the bleacher sections."
  x-asian-art-museum-free-sundays   "general admission is free and tickets to our
                                     special exhibitions are offered at a discounted
                                     price of $15"

Rows where the free wording applies only to a subset (members, children) or only
after paying must stay Paid. These tests pin both directions so a future pattern
change cannot silently relabel a genuine price as free.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from register_3adf31d9 import (  # noqa: E402
    FREE_GOVERNS_ENTRY,
    PAID_GOVERNS_ENTRY,
    cost_of,
)

# id -> the exact admission wording already verified from the official page.
FREE_ENTRY_ROWS = {
    "x-giants-fanfest":
        "Free tickets are required for all FanFest Tour stops and the Open House.",
    "chinese":
        "a free event for all to attend but tickets must be purchased to sit in the "
        "bleacher sections.",
    "x-asian-art-museum-free-sundays":
        "general admission is free and tickets to our special exhibitions are offered "
        "at a discounted price of $15",
}

# id -> wording where entry itself costs money, or free applies to a subset only.
PAID_ENTRY_ROWS = {
    "sf-zoo-boo":
        "activities are free with paid daytime admission or Zoo membership.",
    "after-dark":
        "General $22.95 · Daytime & After Dark Members FREE",
    "x-sfmoma-rm-x-sfmoma":
        "This is a surcharged exhibition: $10 weekdays and $12 weekends/holidays. "
        "Free for members.",
    "x-the-haunt-ybca":
        "Tickets: $25 · YBCA Members: $15 · Kids 12 and under free.",
    "h-bravura-circus-bella":
        "Ticketed performances (children 3–12 are $5 off adult ticket prices; "
        "children 2 and under free on an adult's lap)",
}


class CostEntryWordingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {r["id"]: r for r in json.loads((ROOT / "data" / "events.json").read_text())}
        cls.listed = [r for r in cls.rows.values() if r["publication"] == "listed"]

    def test_register_still_carries_the_verified_wording(self):
        """The badge may change; the curated admission text must not."""
        for rid, wording in {**FREE_ENTRY_ROWS, **PAID_ENTRY_ROWS}.items():
            self.assertIn(rid, self.rows, rid)
            self.assertEqual(self.rows[rid]["price"], wording, rid)

    def test_free_entry_wording_badges_free_with_conditions(self):
        for rid in FREE_ENTRY_ROWS:
            badge, conditions = cost_of(self.rows[rid])
            self.assertEqual(badge, "Free", rid)
            self.assertTrue(
                conditions,
                f"{rid}: money is mentioned in the admission wording, so the badge must "
                 "carry the 'Conditions apply — read the exact wording' qualifier",
            )

    def test_paid_entry_wording_still_badges_paid(self):
        for rid in PAID_ENTRY_ROWS:
            self.assertEqual(cost_of(self.rows[rid])[0], "Paid", rid)

    def test_entry_patterns_are_mutually_exclusive_on_the_register(self):
        """No row may match both governing sets — that would be an unresolved reading."""
        import re
        for row in self.listed:
            price = (row.get("price") or "").casefold()
            if not price.strip():
                continue
            free_governs = any(re.search(p, price) for p in FREE_GOVERNS_ENTRY)
            paid_governs = any(re.search(p, price) for p in PAID_GOVERNS_ENTRY)
            self.assertFalse(
                free_governs and paid_governs,
                f"{row['id']}: both entry-governing pattern sets match: {row['price']}",
            )

    def test_blank_admission_is_never_free(self):
        """Unpriced rows stay 'Not stated'; the fix must not leak into them."""
        blank = [r for r in self.listed if not (r.get("price") or "").strip()]
        self.assertTrue(blank, "expected unpriced rows in the directory")
        for row in blank:
            self.assertEqual(cost_of(row), ("Not stated", False), row["id"])

    def test_free_governing_patterns_only_change_the_documented_rows(self):
        """Pin the blast radius.

        Three further rows ("General admission is free" at FAMSF / the de Young /
        Fleet Week) also match FREE_GOVERNS_ENTRY, but they carry no price at all, so
        they were already badged Free and the new precedence cannot touch them. The
        only rows whose reading changes are the ones whose single official sentence
        matches a price pattern AND a free pattern AND the free-entry set.
        """
        import re
        from register_3adf31d9 import FREE_PATTERNS, PAID_PATTERNS
        changed = set()
        for row in self.listed:
            price = (row.get("price") or "").casefold()
            if not price.strip():
                continue
            if not any(re.search(p, price) for p in PAID_PATTERNS):
                continue
            if not any(re.search(p, price) for p in FREE_PATTERNS):
                continue
            if any(re.search(p, price) for p in FREE_GOVERNS_ENTRY) and not any(
                re.search(p, price) for p in PAID_GOVERNS_ENTRY
            ):
                changed.add(row["id"])
        self.assertEqual(changed, set(FREE_ENTRY_ROWS))

    def test_paid_governing_patterns_are_exactly_the_documented_paid_cases(self):
        import re
        matched = {
            r["id"] for r in self.listed
            if any(re.search(p, (r.get("price") or "").casefold()) for p in PAID_GOVERNS_ENTRY)
        }
        self.assertEqual(matched, set(PAID_ENTRY_ROWS))


if __name__ == "__main__":
    unittest.main()
