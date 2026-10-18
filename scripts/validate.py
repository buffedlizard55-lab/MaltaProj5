#!/usr/bin/env python3
"""Offline gate: audit projection, quotations, blanks, dates, CSVs and HTML links.

This is structural/provenance validation, never automatic semantic verification.
"""
from __future__ import annotations

import csv
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from audited_register import FIELDS, compile_register, normal  # noqa: E402
from register_3adf31d9 import extend as extend_register, topic_of, cost_of, next_date  # noqa: E402
from register_21f3dd85 import extend as extend_register_21f3dd85  # noqa: E402
from register_d57e2eeb import extend as extend_register_d57e2eeb  # noqa: E402
from register_9d0b6c49 import extend as extend_register_9d0b6c49  # noqa: E402

TOPIC_PAGES = {'gaming.html': 'Gaming', 'music.html': 'Music', 'ai.html': 'AI & technology'}


def load(name):
    return json.loads((ROOT / 'data' / name).read_text())


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.event_rows = [], set(), {}
        self.in_events = False
        self.row = None
        self.cells = None
        self.cell = None
        self.lang = None
        self.title = False
        self.has_title = False
        self.h1 = 0
        self.viewport = False
        self.official_urls = []
        self.row_official = {}
        self.styles = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, ('Duplicate HTML id', a['id'])
            self.ids.add(a['id'])
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'title':
            self.title = True
        if tag == 'h1':
            self.h1 += 1
        if tag == 'meta' and a.get('name') == 'viewport':
            self.viewport = True
        if tag == 'table' and 'events' in a.get('class', '').split():
            self.in_events = True
        if self.in_events and tag == 'tr' and 'id' in a:
            self.row, self.cells = a['id'], []
            self.row_official[self.row] = []
        if self.row and tag in ('td', 'th'):
            self.cell = []
        if tag == 'a' and 'official' in a.get('class', '').split():
            url = a['href']
            assert urlsplit(url).scheme == 'https', ('Official source not HTTPS', url)
            self.official_urls.append(url)
            if self.row:
                self.row_official[self.row].append(url)
        for attr in ('href', 'src'):
            if attr in a:
                self.links.append(a[attr])
        # No browser-facing localhost/backends or inline network dependencies.
        for value in a.values():
            if isinstance(value, str):
                assert '://localhost' not in value and '://127.0.0.1' not in value

    def handle_endtag(self, tag):
        if tag == 'title':
            self.title = False
        if self.row and tag in ('td', 'th') and self.cell is not None:
            self.cells.append(normal(' '.join(self.cell)))
            self.cell = None
        if tag == 'tr' and self.row:
            self.event_rows[self.row] = self.cells
            self.row, self.cells, self.cell = None, None, None
        if tag == 'table':
            self.in_events = False

    def handle_data(self, text):
        if self.title and text.strip():
            self.has_title = True
        if self.cell is not None:
            self.cell.append(text)


def main():
    rows, sources, review, summary = (load(n) for n in ('events.json', 'sources.json', 'review.json', 'audit_summary.json'))
    history, audit = load('unverified_history.json'), load('audit_64f8b973.json')
    assert history['warning'].startswith('UNVERIFIED'), 'Historical claims need an explicit warning'
    expected = compile_register(history['events'], history['sources'], history['review_findings'], audit)
    expected = extend_register(*expected)
    expected = extend_register_21f3dd85(*expected)
    expected = extend_register_d57e2eeb(*expected)
    expected = extend_register_9d0b6c49(*expected)
    assert (rows, sources, review, summary) == expected, 'Canonical data is not the exact fail-closed audit projection plus the additive 3adf31d9, 21f3dd85, d57e2eeb and 9d0b6c49 overlays. Rebuild; never run the old matcher applicator.'
    assert {r['id'] for r in rows} >= set(load('audit_3adf31d9.json')['candidates']), 'New-research candidates were dropped'
    assert {r['id'] for r in rows} >= set(load('audit_21f3dd85.json')['candidates']), 'Free-first candidates were dropped'
    assert {r['id'] for r in rows} >= set(load('audit_d57e2eeb.json')['candidates']), 'Free-first gap candidates were dropped'
    assert {r['id'] for r in rows} >= set(load('audit_9d0b6c49.json')['candidates']), 'Verification-pass candidates were dropped'
    ids = {r['id'] for r in rows}
    assert len(ids) == len(rows)
    assert set(audit['candidates']) <= ids, 'An inherited candidate was silently discarded'
    assert all(r['sources'] and all(s in sources for s in r['sources']) for r in rows)
    assert len({s['url'] for s in sources.values()}) == len(sources), 'Duplicate source URLs'
    listed = [r for r in rows if r['publication'] == 'listed']
    by_id = {r['id']: r for r in rows}
    for row in rows:
        for field in FIELDS:
            assert bool(row[field]) == bool(row['field_evidence'].get(field)), (row['id'], field)
            if not row[field]:
                assert f'{field}: unverified' in row['unverified'], (row['id'], field)
        assert not any(k in row for k in ('check', 'district', 'field-level', 'page-level')), 'Inherited verification metadata leaked'
    for filename, items, is_review in [('events.csv', listed, False), ('review.csv', rows, True)]:
        with (ROOT / 'data' / filename).open(newline='') as f:
            exported = list(csv.DictReader(f))
        assert len(exported) == len(items)
        assert [r['id'] for r in exported] == [r['id'] for r in items]
        for record, row in zip(exported, items):
            assert all(record[field] == row[field] for field in FIELDS)
            assert record['publication'] == row['publication']
            assert record['official_source_urls'] == ' | '.join(sources[s]['url'] for s in row['sources'])
            assert is_review or row['publication'] == 'listed'
    pages = {}
    for path in ROOT.glob('*.html'):
        page = Page()
        page.feed(path.read_text())
        assert page.lang == 'en' and page.has_title and page.h1 == 1 and page.viewport, path.name
        pages[path.name] = page
    assert len(pages) == 19, 'Unexpected page set'
    for name, page in pages.items():
        for href in page.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = unquote(url.path) or name
            assert not target.startswith('/'), ('Subpath-incompatible local URL', name, href)
            destination = (ROOT / target).resolve()
            assert destination.is_relative_to(ROOT) and destination.is_file(), (name, href)
            if url.fragment and target in pages:
                assert unquote(url.fragment) in pages[target].ids, (name, href)
        for rid, cells in page.event_rows.items():
            row = next(r for r in rows if r['id'] == rid)
            assert len(cells) == 9, (name, rid, len(cells))
            assert page.row_official[rid], ('Row missing a direct official source', name, rid)
            assert all(url in {sources[s]['url'] for s in row['sources']} for url in page.row_official[rid])
            badge, conditions = cost_of(row)
            expected_badge = badge + (' Conditions apply — read the exact wording' if conditions else '')
            assert cells[1] == expected_badge, (name, rid, 'cost badge', cells[1], expected_badge)
            for index, field in ((3, 'time'), (4, 'venue'), (5, 'price')):
                assert cells[index] == normal(row[field]), (name, rid, field, cells[index])
            if not row['schedule']:
                assert not cells[2], ('Unsupported schedule rendered', name, rid)
            else:
                assert cells[2].startswith(normal(row['schedule'])), (name, rid, 'schedule')
            if row['name']:
                assert cells[0].startswith(normal(row['name']))
            else:
                assert 'Unverified inherited identifier' in cells[0]
    # A recurrence pattern alone never qualifies an entry as upcoming.
    free_ids = {r['id'] for r in listed if cost_of(r)[0] == 'Free'}
    dated_ids_set = {r['id'] for r in listed if next_date(r)}
    assert set(pages['index.html'].event_rows) == free_ids & dated_ids_set
    assert set(pages['index.html'].event_rows) <= free_ids, 'A non-free row reached the free-first landing page'
    assert set(pages['review.html'].event_rows) == ids
    # Upcoming carries every listed entry: dated first, then recurring, then undated.
    assert set(pages['upcoming.html'].event_rows) == {r['id'] for r in listed}
    for name, topic in TOPIC_PAGES.items():
        assert set(pages[name].event_rows) == {r['id'] for r in listed if topic_of(r) == topic}, name
    assert set(pages['free.html'].event_rows) == {r['id'] for r in listed if cost_of(r)[0] == 'Free'}
    # Separate Paid section (T39): only rows whose quoted admission text is priced.
    assert set(pages['paid.html'].event_rows) == {r['id'] for r in listed if cost_of(r)[0] == 'Paid'}
    # Session 59f56c24's combined focus page: the whole directory, Gaming / Music / AI / Other.
    assert set(pages['focus.html'].event_rows) == {r['id'] for r in listed}
    focus_order = {'Gaming': 0, 'Music': 1, 'AI & technology': 2, 'Other': 3}
    rank = -1
    for rid in pages['focus.html'].event_rows:
        topic = topic_of(by_id[rid])
        assert focus_order[topic] >= rank, f'focus.html out of group order: {rid}'
        rank = focus_order[topic]
    # Date ordering: the Upcoming page must be nearest-first across its dated rows.
    ordered = [rid for rid in pages['upcoming.html'].event_rows if next_date(next(r for r in rows if r['id'] == rid))]
    dated_ids = [r['id'] for r in sorted((r for r in listed if next_date(r)), key=lambda r: (next_date(r), r['name'].casefold()))]
    assert ordered == dated_ids, 'Upcoming page is not ordered nearest-first by approved date'
    # Executive summary (T38): the landing page lists the soonest FREE dated entries,
    # nearest first, before every table. Paid and Not-stated rows never appear there.
    free_dated_ids = [r['id'] for r in sorted((r for r in listed if next_date(r) and cost_of(r)[0] == 'Free'), key=lambda r: (next_date(r), r['name'].casefold()))]
    index_page = pages['index.html']
    summary_links = [href for href in index_page.links if href.startswith('upcoming.html#')]
    assert summary_links[:min(12, len(free_dated_ids))] == ['upcoming.html#' + rid for rid in free_dated_ids[:12]], 'Executive summary is not the soonest free entries by date'
    assert all(cost_of(by_id[href.split('#', 1)[1]])[0] == 'Free' for href in summary_links), 'Executive summary links a non-free row'
    for name, kind in [('weekly.html', 'Weekly'), ('monthly.html', 'Monthly'), ('annual.html', 'Annual'), ('special.html', 'Special')]:
        assert set(pages[name].event_rows) == {r['id'] for r in listed if r['kind'] == kind}
    for name, category in [('markets.html', 'Markets & food'), ('museums.html', 'Museums & science'), ('culture.html', 'Festivals & culture'), ('community.html', 'Community & outdoors')]:
        assert set(pages[name].event_rows) == {r['id'] for r in listed if r['category'] == category}
    assert all(f'e-{rid}' in pages['sources.html'].ids for rid in ids), 'Missing row proof anchor'
    assert all(f's-{sid}' in pages['sources.html'].ids for sid in sources), 'Missing source anchor'
    for name in pages:
        text = (ROOT / name).read_text()
        assert '18 October 2026' in text
        assert 'not a real-time' in text or name in {'analysis.html', 'review.html', 'sources.html'}
        assert 'Page-level check' not in text and 'Field-level check' not in text
    print(f'PASS: {len(rows)} exact audit projections; {len(listed)} SF directory / {len(rows)-len(listed)} review-only; all quote provenance, recurrence/year guards, blanks, CSV values, 19 pages, cost badges, free-upcoming dashboard, separate paid section, date ordering, row sources and local links/fragments.')


if __name__ == '__main__':
    main()
