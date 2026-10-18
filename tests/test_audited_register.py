"""Regression fixtures for errors observed in the inherited register.

No network or third-party packages required. These tests establish provenance and
publication behavior, not the semantic truth of arbitrary organizer statements.
"""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from audited_register import compile_register, temporal, validate_decision  # noqa: E402
from register_3adf31d9 import extend as extend_register  # noqa: E402
from register_21f3dd85 import extend as extend_register_21f3dd85  # noqa: E402
from audit_evidence import retain_capture  # noqa: E402


class AuditedRegister(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads((ROOT / 'data/audit_64f8b973.json').read_text())
        cls.history = json.loads((ROOT / 'data/unverified_history.json').read_text())
        cls.rows = json.loads((ROOT / 'data/events.json').read_text())
        cls.by_id = {r['id']: r for r in cls.rows}

    def project(self, audit=None, history=None):
        h = history or self.history
        # The additive overlays always run last, in consolidate.py order:
        # 3adf31d9 (topic gap), then 21f3dd85 (free-first).
        return extend_register_21f3dd85(*extend_register(*compile_register(h['events'], h['sources'], h['review_findings'], audit or self.audit)))

    def test_baseline_retained_and_new_entries_identified(self):
        self.assertEqual(len(self.history['events']), 233)
        self.assertEqual(len(self.audit['candidates']), 231)
        self.assertEqual(len(self.audit['extra_events']), 18)
        # 246 audited (231 candidates + 13 official-calendar extras + 2 companions), then
        # session 59f56c24's 5 official-calendar extras, 3adf31d9's 15 topic-gap entries,
        # and 21f3dd85's 8 free-first entries (6 listed, 2 held for review).
        self.assertEqual(len(self.rows), 274)
        self.assertTrue(set(self.audit['candidates']) <= set(self.by_id))
        self.assertEqual(sum(r['publication'] == 'listed' for r in self.rows), 191)

    def test_upstream_additions_and_source_repair_are_preserved(self):
        self.assertIn('f1-alemany-flea-market', self.by_id)
        self.assertEqual(self.by_id['f1-alemany-flea-market']['publication'], 'listed')
        self.assertEqual(self.by_id['f1-sffilm-doc-stories']['publication'], 'review_only')
        sources = json.loads((ROOT / 'data/sources.json').read_text())
        urls = {s['url'] for s in sources.values()}
        self.assertNotIn('https://www.ferrybuildingmarketplace.com/events/ferry-fest/', urls)
        self.assertIn('https://sfsketchfest2026.sched.com/', urls)
        self.assertEqual(self.by_id['b-lit-crawl']['time'], '')

    def test_exact_projection(self):
        rows, _, _, summary = self.project()
        self.assertEqual(rows, self.rows)
        self.assertEqual(summary['listed'] + summary['review_only'], len(rows))

    def test_legacy_free_admission_cannot_fill_a_blank(self):
        h = deepcopy(self.history)
        old = next(r for r in h['events'] if r['id'] == 'b-ferry-plaza-farmers-market')
        old['price'] = 'Free (unsupported historical claim)'
        old['flags'] = []
        old['check'] = {'level': 'field-level'}
        rows, _, _, _ = self.project(history=h)
        row = next(r for r in rows if r['id'] == old['id'])
        self.assertEqual(row['price'], '')
        self.assertIn('price: unverified', row['unverified'])
        self.assertNotIn('check', row)

    def test_name_only_decision_never_approves_other_fields(self):
        a = deepcopy(self.audit)
        d = a['decisions']['b-ferry-plaza-farmers-market']
        d['fields'] = {'name': d['fields']['name']}
        d['publication'] = 'review_only'
        rows, _, _, _ = self.project(audit=a)
        row = next(r for r in rows if r['id'] == 'b-ferry-plaza-farmers-market')
        self.assertTrue(row['name'])
        for field in ('schedule', 'time', 'venue', 'price'):
            self.assertEqual(row[field], '')
        self.assertEqual(row['publication'], 'review_only')

    def test_unreviewed_candidate_fails_closed(self):
        a = deepcopy(self.audit)
        del a['decisions']['nightlife']
        with self.assertRaisesRegex(ValueError, 'mismatch'):
            self.project(audit=a)

    def test_recurring_kind_needs_recurrence_evidence(self):
        d = deepcopy(self.audit['decisions']['nightlife'])
        d['recurrence'] = None
        with self.assertRaisesRegex(ValueError, 'recurrence evidence'):
            validate_decision(d, self.audit['captures'])

    def test_published_location_must_be_confirmed_sf(self):
        d = deepcopy(self.audit['decisions']['nightlife'])
        d['geography'] = {'status': 'unverified', 'quotes': [], 'basis': 'pending'}
        with self.assertRaisesRegex(ValueError, 'Publication requires'):
            validate_decision(d, self.audit['captures'])

    def test_quote_must_be_archived_and_nonempty(self):
        d = deepcopy(self.audit['decisions']['nightlife'])
        d['fields']['time']['quotes'][0]['text'] = 'A made-up official time that does not appear'
        with self.assertRaisesRegex(ValueError, 'Quotation absent'):
            validate_decision(d, self.audit['captures'])
        d['fields']['time']['quotes'] = []
        with self.assertRaisesRegex(ValueError, 'needs quotations'):
            validate_decision(d, self.audit['captures'])

    def test_yearless_sources_never_become_upcoming(self):
        for rid in ('x-bill-graham-menorah', 'cole', 'taraval', 'b-b2b-shakeout-run-2027', 'b-giants-vs-athletics-b2b-runners-night'):
            with self.subTest(row=rid):
                row = self.by_id[rid]
                self.assertEqual(row['occurrences'], [])
                self.assertNotEqual(row['temporal_status'], 'Future dated')

    def test_cannot_supply_missing_year_from_url_or_weekday(self):
        d = deepcopy(self.audit['decisions']['x-bill-graham-menorah'])
        d['occurrences'] = [{'start': '2026-12-14', 'end': '2026-12-22', 'quotes': d['fields']['schedule']['quotes']}]
        with self.assertRaisesRegex(ValueError, 'year not present'):
            validate_decision(d, self.audit['captures'])

    def test_cannot_move_a_date_to_a_different_month(self):
        d = deepcopy(self.audit['decisions']['sf-zoo-boo'])
        d['occurrences'][0]['start'] = '2026-11-30'
        d['occurrences'][0]['end'] = '2026-11-30'
        with self.assertRaisesRegex(ValueError, 'month/day not present'):
            validate_decision(d, self.audit['captures'])

    def test_observed_date_regressions(self):
        expected = {'sf-zoo-resident-free-day': '2026-10-07', 'sf-zoo-boo': '2026-10-31', 'sf-zoo-member-mornings': '2026-10-03', 'presidio-fiesta-en-el-parque': '2026-08-01', 'b-opera-ball-2026': '2026-11-12'}
        for rid, day in expected.items():
            self.assertEqual(self.by_id[rid]['occurrences'][0]['start'], day)
        self.assertEqual(self.by_id['sf-zoo-boo']['time'], '10:00 AM – 3:00 PM')
        self.assertEqual(self.by_id['sf-zoo-resident-free-day']['kind'], 'Special')
        self.assertEqual(self.by_id['b-opera-ball-2026']['temporal_status'], 'Future dated')

    def test_regional_programmes_not_published_wholesale(self):
        for rid in ('b-frameline', 'b-sf-marathon', 'x-nexus-sf-bay-area-black-art-week', 'x-sf-art-week', 'x-sf-climate-week', 'x-bay-area-dance-week', 'x-sf-jewish-film-festival', 'x-sf-beer-week'):
            self.assertEqual(self.by_id[rid]['publication'], 'review_only', rid)

    def test_conflicting_values_blank_and_flagged(self):
        for rid in ('secondhand', 'muertos'):
            self.assertEqual(self.by_id[rid]['venue'], '')
            self.assertEqual(self.by_id[rid]['publication'], 'review_only')
        self.assertEqual(self.by_id['b-alemany-farmers-market']['time'], '')

    def test_future_edition_does_not_inherit_previous_venue_price(self):
        r = self.by_id['b-sf-pride-celebration']
        self.assertEqual(r['occurrences'][0]['start'], '2027-06-26')
        self.assertEqual(r['venue'], '')
        self.assertEqual(r['price'], '')
        self.assertEqual(r['publication'], 'review_only')
        self.assertEqual(self.by_id['x-sf-decorator-showcase']['venue'], '')

    def test_nihonmachi_retrospective_cannot_locate_2027_edition(self):
        row = self.by_id['b-nihonmachi-street-fair']
        self.assertEqual(row['venue'], '')
        self.assertEqual(row['publication'], 'review_only')
        self.assertEqual(row['geography']['status'], 'unverified')
        self.assertEqual(row['occurrences'][0]['start'], '2027-08-07')
        self.assertEqual(row['occurrences'][0]['end'], '2027-08-08')

    def test_free_virtual_ticket_not_physical_minimum(self):
        r = self.by_id['x-kung-pao-kosher-comedy']
        self.assertNotIn('$30', r['price'])
        self.assertIn('$95', r['price'])
        self.assertIn('$70', r['price'])
        self.assertNotEqual(self.by_id['sf-zoo-boo']['price'], 'Free')

    def test_famsf_venue_split_avoids_duplicate_deyoung_tuesday(self):
        self.assertEqual(self.by_id['de-young-tue']['venue'], 'de Young')
        self.assertEqual(self.by_id['x-famsf-free-tuesdays']['venue'], 'Legion of Honor')
        self.assertEqual(self.by_id['x-juneteenth-on-the-waterfront']['parent'], 'x-pop-ups-on-the-plaza')

    def test_structured_geography_is_explicitly_labeled(self):
        q = self.by_id['family']['geography']['quotes'][0]
        self.assertEqual(q['format'], 'jsonld')
        self.assertIn('addressLocality', q['text'])
        self.assertIn('San Francisco', q['text'])

    def test_unknown_closing_date_is_not_fabricated(self):
        r = self.by_id['x-sfmoma-sarah-sze']
        self.assertEqual(r['occurrences'][0]['start'], '2026-11-21')
        self.assertEqual(r['occurrences'][0]['end'], '')

    def test_temporal_labels_only_use_explicit_iso_occurrences(self):
        def d(start='', end='', **other):
            return {'occurrences': [{'start': start, 'end': end}] if start else [], **other}
        self.assertEqual(temporal(d('2026-10-17', '2026-10-17')), 'Past dated')
        self.assertEqual(temporal(d('2026-10-18', '2026-10-18')), 'On snapshot date')
        self.assertEqual(temporal(d('2026-10-17', '2026-10-19')), 'Spans snapshot date')
        self.assertEqual(temporal(d('2027-06-26', '2027-06-27')), 'Future dated')
        self.assertEqual(temporal(d('2026-10-17')), 'Opened; closing unconfirmed')
        self.assertEqual(temporal(d(schedule='May 2027', name='2027 URL')), 'Date/year unconfirmed')
        self.assertEqual(temporal(d(recurrence={'value': 'Weekly'})), 'Recurring pattern; next date unconfirmed')
        self.assertEqual(temporal(d('2027-03-25', '2027-03-25', date_status='tentative')), 'Tentative schedule')

    def test_session_59f56c24_official_calendar_additions(self):
        """Session 59f56c24's five extras, merged into audit_64f8b973.json, still project."""
        family = self.by_id['audit-sfpl-family-game-time']
        self.assertEqual(family['publication'], 'listed')
        self.assertEqual(family['occurrences'][0]['start'], '2026-10-18')
        self.assertEqual(family['price'], '')
        self.assertEqual(family['venue'], "West Portal Children's Area")
        gdc = self.by_id['audit-gdc-festival-2027']
        self.assertEqual(gdc['occurrences'][0]['start'], '2027-03-01')
        self.assertEqual(gdc['occurrences'][0]['end'], '2027-03-05')
        self.assertEqual(gdc['price'], 'Festival $549')
        current = self.by_id['audit-current-sf-2026']
        self.assertEqual(current['venue'], 'Moscone West')
        self.assertEqual(current['occurrences'][0]['start'], '2026-11-04')
        ignite = self.by_id['audit-microsoft-ignite-2026']
        self.assertEqual(ignite['occurrences'][0]['start'], '2026-11-17')
        self.assertEqual(ignite['occurrences'][0]['end'], '2026-11-20')
        cloudflare = self.by_id['audit-cloudflare-connect-2026']
        self.assertEqual(cloudflare['occurrences'][0]['start'], '2026-10-19')
        self.assertEqual(cloudflare['occurrences'][0]['end'], '2026-10-21')

    def test_parent_cycle_fails(self):
        a = deepcopy(self.audit)
        a['decisions']['after-dark']['parent'] = 'death'
        with self.assertRaisesRegex(ValueError, 'Cyclic'):
            self.project(audit=a)


class CaptureRetention(unittest.TestCase):
    def test_failed_refresh_preserves_prior_evidence_and_original_status(self):
        old = {'http': 200, 'text': 'Good official evidence', 'checked_at': '2026-10-17', 'tool_excerpt': 'Separate read', 'tool_method': 'Retrieval tool'}
        failed = {'http': 403, 'text': '', 'checked_at': '2026-10-18', 'error': 'blocked'}
        got = retain_capture(old, failed)
        self.assertEqual(got['text'], old['text'])
        self.assertEqual(got['http'], 200)
        self.assertEqual(got['checked_at'], '2026-10-17')
        self.assertEqual(got['latest_attempt']['http'], 403)
        self.assertEqual(got['tool_excerpt'], 'Separate read')

    def test_adjudicated_capture_is_immutable_even_on_success(self):
        old = {'http': 200, 'text': 'Approved context'}
        got = retain_capture(old, {'http': 200, 'text': 'Changed context', 'sha256': 'new'}, locked=True)
        self.assertEqual(got['text'], 'Approved context')
        self.assertEqual(got['latest_attempt']['sha256'], 'new')

    def test_successful_unlocked_refresh_preserves_independent_excerpt(self):
        old = {'http': 405, 'text': 'Old text', 'tool_excerpt': 'Independent text', 'tool_method': 'Selected excerpt'}
        got = retain_capture(old, {'http': 200, 'text': 'New text'})
        self.assertEqual(got['text'], 'New text')
        self.assertEqual(got['tool_excerpt'], 'Independent text')


if __name__ == '__main__':
    unittest.main()
