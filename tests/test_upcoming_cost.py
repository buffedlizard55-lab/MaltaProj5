#!/usr/bin/env python3
"""Regressions for the new-requirement presentation layer (sessions 3adf31d9 T34–T36
and 21f3dd85 T38–T39).

These tests guard the parts a reader relies on:

  * the Upcoming page is ordered by approved ISO date, nearest first;
  * the free-first landing page: executive summary and main section carry free
    upcoming entries only, soonest first; paid rows live on the Paid page;
  * a cost badge is only ever a label over the verified admission text, and a
    blank admission cell is never rendered as "Free";
  * every table row keeps a direct official source link, and no local link breaks.

They are structural/provenance checks. They never certify semantic truth.
"""
import json
import re
import sys
import unittest
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from register_3adf31d9 import SNAPSHOT, cost_of, next_date, topic_of  # noqa: E402


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.rows = {}
        self.row_official = {}
        self.in_events = False
        self.row = None
        self.cell = None
        self.cells = None
        self.viewport = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        if tag == "table" and "events" in a.get("class", "").split():
            self.in_events = True
        if self.in_events and tag == "tr" and "id" in a:
            self.row, self.cells = a["id"], []
            self.row_official[self.row] = []
        if self.row and tag in ("td", "th"):
            self.cell = []
        if tag == "a" and "official" in a.get("class", "").split():
            self.row_official.setdefault(self.row, []).append(a["href"])
        for attr in ("href", "src"):
            if attr in a:
                self.links.append(a[attr])
        for value in a.values():
            if isinstance(value, str):
                assert "://localhost" not in value and "://127.0.0.1" not in value

    def handle_endtag(self, tag):
        if self.row and tag in ("td", "th") and self.cell is not None:
            self.cells.append(re.sub(r"\s+", " ", "".join(self.cell)).strip())
            self.cell = None
        if tag == "tr" and self.row:
            self.rows[self.row] = self.cells
            self.row, self.cells = None, None
        if tag == "table":
            self.in_events = False

    def handle_data(self, text):
        if self.cell is not None:
            self.cell.append(text)


class Presentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load("events.json")
        cls.sources = load("sources.json")
        cls.listed = [r for r in cls.rows if r["publication"] == "listed"]
        cls.pages = {}
        for path in sorted(ROOT.glob("*.html")):
            page = Page()
            page.feed(path.read_text())
            cls.pages[path.name] = page

    def pages_named(self):
        return {
            "index.html", "upcoming.html", "weekly.html", "monthly.html", "annual.html", "special.html",
            "gaming.html", "music.html", "ai.html", "free.html", "paid.html", "focus.html", "markets.html", "museums.html",
            "culture.html", "community.html", "analysis.html", "review.html", "sources.html",
        }

    def test_nineteen_pages_with_viewport(self):
        self.assertEqual(set(self.pages), self.pages_named())
        for name, page in self.pages.items():
            self.assertTrue(page.viewport, name)

    def test_upcoming_is_ordered_nearest_first(self):
        page = self.pages["upcoming.html"]
        dated = [r for r in self.listed if next_date(r)]
        expected = [r["id"] for r in sorted(dated, key=lambda r: (next_date(r), r["name"].casefold()))]
        rendered = [rid for rid in page.rows if next_date(next(r for r in self.rows if r["id"] == rid))]
        self.assertEqual(rendered, expected)
        starts = [next_date(next(r for r in self.rows if r["id"] == rid)) for rid in rendered]
        self.assertEqual(starts, sorted(starts))
        # A start before the snapshot is only allowed when the span still covers it
        # (an ongoing exhibition or run). Nothing may end before the snapshot.
        for rid, start in zip(rendered, starts):
            row = next(r for r in self.rows if r["id"] == rid)
            span = next(o for o in row["occurrences"] if o["start"] == start)
            if start < SNAPSHOT:
                self.assertTrue(span["end"] and span["end"] >= SNAPSHOT, rid)

    def test_executive_summary_is_free_and_date_ordered(self):
        """Free-first (21f3dd85, T38): the summary lists the soonest FREE dated entries."""
        page = self.pages["index.html"]
        dated_free = [r for r in self.listed if next_date(r) and cost_of(r)[0] == "Free"]
        expected = [r["id"] for r in sorted(dated_free, key=lambda r: (next_date(r), r["name"].casefold()))]
        links = [href.split("#", 1)[1] for href in page.links if href.startswith("upcoming.html#")]
        self.assertEqual(links[: min(12, len(expected))], expected[:12])
        by_id = {r["id"]: r for r in self.rows}
        for rid in links:
            self.assertEqual(cost_of(by_id[rid])[0], "Free", rid)

    def test_no_row_loses_its_official_source(self):
        urls = {s["url"] for s in self.sources.values()}
        for name, page in self.pages.items():
            for rid, links in page.row_official.items():
                self.assertTrue(links, (name, rid))
                for url in links:
                    self.assertIn(url, urls, (name, rid))
                    self.assertEqual(urlsplit(url).scheme, "https", (name, rid))

    def test_cost_badge_never_invents_free(self):
        for row in self.listed:
            badge, _ = cost_of(row)
            if not row["price"]:
                self.assertEqual(badge, "Not stated", row["id"])
            self.assertIn(badge, {"Free", "Paid", "Not stated", "See source"}, row["id"])

    def test_free_page_only_holds_stated_free_entries(self):
        page = self.pages["free.html"]
        expected = {r["id"] for r in self.listed if cost_of(r)[0] == "Free"}
        self.assertEqual(set(page.rows), expected)
        self.assertTrue(expected)
        for rid in expected:
            row = next(r for r in self.listed if r["id"] == rid)
            self.assertTrue(row["price"], rid)

    def test_paid_page_only_holds_priced_entries(self):
        """Separate Paid section (21f3dd85, T39): priced rows only, never unpriced ones."""
        page = self.pages["paid.html"]
        expected = {r["id"] for r in self.listed if cost_of(r)[0] == "Paid"}
        self.assertEqual(set(page.rows), expected)
        self.assertTrue(expected)
        free_ids = {r["id"] for r in self.listed if cost_of(r)[0] == "Free"}
        self.assertFalse(set(page.rows) & free_ids)
        for rid in expected:
            row = next(r for r in self.listed if r["id"] == rid)
            self.assertTrue(row["price"], rid)

    def test_landing_main_section_is_free_only(self):
        """The landing table carries only free entries with approved upcoming dates."""
        page = self.pages["index.html"]
        free_ids = {r["id"] for r in self.listed if cost_of(r)[0] == "Free"}
        dated_ids = {r["id"] for r in self.listed if next_date(r)}
        expected = free_ids & dated_ids
        self.assertEqual(set(page.rows), expected)
        self.assertTrue(expected)
        # The whole directory survives elsewhere: Upcoming and Focus carry every listed row.
        all_listed = {r["id"] for r in self.listed}
        self.assertEqual(set(self.pages["upcoming.html"].rows), all_listed)
        self.assertEqual(set(self.pages["focus.html"].rows), all_listed)

    def test_expired_or_undated_patterns_never_reach_landing(self):
        page = self.pages["index.html"]
        for rid in ("audit-sunday-fun-days-2026", "f-sfpl-mix-gaming"):
            self.assertNotIn(rid, page.rows)
            self.assertIn(rid, self.pages["free.html"].rows)
        order = json.loads((ROOT / "data/dashboard_order.json").read_text())
        self.assertEqual(order["recurring"], [])
        self.assertEqual(order["dated"], list(page.rows))

    def test_topic_pages_match_the_editorial_tags(self):
        for name, topic in (("gaming.html", "Gaming"), ("music.html", "Music"), ("ai.html", "AI & technology")):
            expected = {r["id"] for r in self.listed if topic_of(r) == topic}
            self.assertEqual(set(self.pages[name].rows), expected, name)
            self.assertTrue(expected, name)

    def test_every_row_has_nine_cells_including_cost(self):
        for name, page in self.pages.items():
            for rid, cells in page.rows.items():
                self.assertEqual(len(cells), 9, (name, rid))
                self.assertTrue(cells[1].startswith(("Free", "Paid", "Not stated", "See source")), (name, rid, cells[1]))

    def test_local_links_resolve(self):
        for name, page in self.pages.items():
            for href in page.links:
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                target = url.path or name
                self.assertFalse(target.startswith("/"), (name, href))
                self.assertTrue((ROOT / target).is_file(), (name, href))

    def test_sources_page_has_an_anchor_for_every_row_and_source(self):
        page = self.pages["sources.html"]
        for row in self.rows:
            self.assertIn(f"e-{row['id']}", page.ids, row["id"])
        for sid in self.sources:
            self.assertIn(f"s-{sid}", page.ids, sid)

    def test_snapshot_date_is_stated_on_every_page(self):
        for name in self.pages:
            self.assertIn("18 October 2026", (ROOT / name).read_text(), name)

    def test_upcoming_excludes_generated_dates(self):
        """A recurring pattern may never produce a date the sources do not approve."""
        dated = {r["id"] for r in self.listed if next_date(r)}
        for row in self.listed:
            if not row["occurrences"]:
                self.assertNotIn(row["id"], dated, row["id"])
            for occurrence in row["occurrences"]:
                self.assertTrue(occurrence["quotes"], row["id"])
                self.assertIsInstance(date.fromisoformat(occurrence["start"]), date)


if __name__ == "__main__":
    unittest.main()
