"""Regression tests for the final official-source evidence reconciliation."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from audited_register import normal  # noqa: E402
from register_3adf31d9 import cost_of  # noqa: E402


class T32Reconciliation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads((ROOT / "data/audit_06949148.json").read_text())
        cls.rows = json.loads((ROOT / "data/events.json").read_text())
        cls.sources = json.loads((ROOT / "data/sources.json").read_text())
        cls.review = json.loads((ROOT / "data/review.json").read_text())
        cls.summary = json.loads((ROOT / "data/audit_summary.json").read_text())
        cls.by_id = {row["id"]: row for row in cls.rows}
        cls.by_url = {source["url"]: (sid, source) for sid, source in cls.sources.items()}

    def test_only_captured_quotations_are_used_and_http_is_not_inferred(self):
        for url, capture in self.audit["captures"].items():
            with self.subTest(url=url):
                self.assertIsNone(capture["http"])
        for change in self.audit["changes"]:
            quotes = [change["quote"]] if "quote" in change else change["context_quotes"]
            for quote in quotes:
                capture = self.audit["captures"][quote["url"]]
                text = normal(capture.get("title", "") + " " + capture.get("tool_excerpt", ""))
                self.assertIn(normal(quote["text"]), text)

    def test_official_rsvp_wording_is_free_but_not_upcoming(self):
        row = self.by_id["x-oktoberfest-on-front"]
        self.assertEqual(row["price"], "FREE WITH RSVP")
        self.assertEqual(row["field_evidence"]["price"]["quotes"][0]["url"],
                         "https://downtownsf.org/things-to-do/oktoberfest-on-front")
        self.assertEqual(cost_of(row), ("Free", True))
        self.assertNotIn("price: unverified", row["unverified"])
        self.assertEqual(row["temporal_status"], "Past dated")

    def test_alemany_hours_conflict_stays_blank_and_all_official_pages_link(self):
        row = self.by_id["b-alemany-farmers-market"]
        self.assertEqual(row["time"], "")
        self.assertNotIn("time", row["field_evidence"])
        self.assertIn("time: unverified", row["unverified"])
        self.assertIn("conflicting official statements", row["flags"][0])
        row_urls = {self.sources[sid]["url"] for sid in row["sources"]}
        self.assertTrue({
            "https://www.sf.gov/location--alemany-farmers-market",
            "https://foodwise.org/markets/alemany-farmers-market/",
            "https://www.sfenvironment.org/farmers-markets-in-sf",
        } <= row_urls)
        foodwise = self.by_url["https://foodwise.org/markets/alemany-farmers-market/"][1]
        self.assertIsNone(foodwise["http"])
        self.assertEqual(foodwise["tool_checked_at"], "2026-10-18")

    def test_review_page_finding_links_the_conflict_evidence(self):
        finding = next(item for item in self.review
                       if item["title"] == "Alemany Farmers Market hours: conflicting official pages")
        self.assertEqual(set(finding["urls"]), {
            "https://www.sf.gov/location--alemany-farmers-market",
            "https://foodwise.org/markets/alemany-farmers-market/",
            "https://www.sfenvironment.org/farmers-markets-in-sf",
        })
        self.assertEqual(self.summary["source_urls"], len(self.sources))
        # Cost composition at the 18 October 2026 snapshot, this reconciliation plus the
        # two later integration passes: 76 Free once this overlay quoted Oktoberfest's
        # "FREE WITH RSVP"; +3 Free where the official wording makes the free phrase
        # govern entry and a price only buys an optional extra (session 9d0b6c49's badge
        # fix), so Paid drops 20 -> 17; +4 Free from that pass's verified additions.
        # "Not stated" is 117 minus the Oktoberfest blank this overlay filled, and every
        # later addition quotes an admission price, so it stays 116.
        # scripts/validate.py's exact whole-projection assertion is the structural guard
        # against drift; these absolutes document what the composition should be.
        self.assertEqual(self.summary["cost"]["Free"], 83)
        self.assertEqual(self.summary["cost"]["Paid"], 17)
        self.assertEqual(self.summary["cost"]["Not stated"], 116)


if __name__ == "__main__":
    unittest.main()
