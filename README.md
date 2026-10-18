# SF Events — an evidence-first city directory

A static, source-linked inventory of recurring gatherings and dated programmes **inside San Francisco city**, with unresolved candidates published separately.

**Site:** https://buffedlizard55-lab.github.io/MaltaProj5/

**Research snapshot:** 18 October 2026. This is **not an exhaustive or live city calendar**.

## Current audited register

| Measure | Count |
|---|---:|
| Candidates assessed | 274 |
| Previously assessed candidates (231 initial + 2 companion + 13 official-calendar) | 246 |
| Session `59f56c24` official-calendar extras | 5 |
| New topic-gap entries added in audit `3adf31d9` (gaming / music / AI) | 15 |
| Free-first entries added in audit `21f3dd85` (free gaming / music / AI first) | 8 |
| Entries admitted to the city-only directory | 191 |
| Candidates held off the directory for review | 83 |
| Weekly / monthly / annual entries | 24 / 11 / 32 |
| Special, dated or cadence-unconfirmed entries | 124 |
| Entries with at least one confirmed future date | 70 |
| Directory rows reading Free / Paid / Not stated | 61 / 19 / 111 |
| Exact cited official-source URLs / distinct domains | 277 / 150 |

The directory includes 16 programme umbrellas and their independently sourced child events. Counts are **entries, not unique city events**. Category and programme relationships are editorial; recurring classifications require their own evidence.

The site is **free-first**: the [dashboard](index.html) executive summary and main section carry **free upcoming events only** (dated entries nearest first, then free recurring patterns), ordered Gaming → Music → AI & technology → everything else. Priced events are collected in the separate [Paid events](paid.html) section; the complete all-cost directory remains on [Focus](focus.html) and [Upcoming](upcoming.html).

- [Dashboard (free-first)](index.html) · [Upcoming](upcoming.html) · [Weekly](weekly.html) · [Monthly](monthly.html) · [Annual](annual.html) · [Special & dated](special.html)
- [Gaming](gaming.html) · [Music](music.html) · [AI & technology](ai.html) · [Free to attend](free.html) · [Paid events](paid.html) · [Focus, one page](focus.html)
- [Markets & food](markets.html) · [Museums & science](museums.html) · [Festivals & culture](culture.html) · [Community & outdoors](community.html)
- [Analysis](analysis.html) · [Flagged for Review](review.html) · [Sources and row-by-row evidence](sources.html)
- [Directory CSV](data/events.csv) · [All review records CSV](data/review.csv) · [Research log for audit `3adf31d9`](data/research/audit-3adf31d9.md) · [Research log for audit `21f3dd85`](data/research/audit-21f3dd85.md)

## What a listing means

An entry needs an approved **name, venue and SF geography** to enter the directory. It does **not** mean every field is verified. Each nonblank factual value has an explicit contextual decision and an exact quotation from an official organizer, venue, museum or government page. Recognized SF venues can be located from their official addresses/directions; a stray city word in unrelated marketing is not geography evidence.

**Unconfirmed values remain genuinely blank**, with missing-field notes. An unverified inherited title can identify a review candidate but is labeled as an identifier, not a confirmed event name. HTTP success, a name match, a copyright/URL year, free parking, or free activities with paid entry cannot approve unrelated facts.

Only explicitly approved ISO occurrences determine temporal status, relative to the fixed snapshot—not the current date. Yearless Menorah, Cole Valley Nights, Taraval and ancillary Bay to Breakers copy are not assigned invented years. A recurring pattern does not generate a next date. A future edition never inherits a previous edition’s venue, hours or admission automatically.

### Important corrections and remaining flags

- Zoo resident free day: **7 October 2026**, not an established monthly first-Tuesday policy. Boo: **31 October, 10am–3pm**, activities included with paid daytime admission or membership.
- Fiesta en el Parque: **1 August 2026**, not August 2. Opera Ball rescheduled to **12 November 2026**; no Opera House performance that evening.
- Bhangra & Beats: 2026 programme at **Yerba Buena Gardens, Jessie Square and Yerba Buena Lane**, not the older Clay/Battery venue.
- Conflicting Alemany hours and Secondhand/Muertos street extents remain blank/flagged rather than reconciled by guessing.
- Regional/mixed-city programmes—including Frameline, NEXUS, SF Art Week, SF Climate Week and the full SF Marathon—are held for SF-specific component/route evidence.
- The 2027 Pride weekend is confirmed, but its old 2026 venue and free-entry policy are not carried forward. Nihonmachi’s 2027 dates are also confirmed, but its venue is blank: the Japantown sentence is in the prior-edition retrospective.
- T29 additions: Outdoor Rec Day (28 Feb 2026, Mission Creek Park); Sunday Fun Days (Sundays at Union Square through 27 Sep 2026); Civic Center Soundtrack and Illuminate LIVE weekly series (no ISO kickoff year in the quoted sentences); Comedy Day listed from organizer FAQ without a printed 2026 date.

See [the audit research log](data/research/audit-64f8b973.md) and the official quotations for details. No .org-to-nonprofit or sample-to-citywide inference is made.

## Rebuild and validate

Python 3.10+; no runtime packages or build dependencies:

```sh
python3 tools/consolidate.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
```

`consolidate.py` first reconstructs historical candidates from the preserved research inputs, preserves the newer mainline companion audit (including its two added candidates) in an isolated temporary candidate-history tree, then **must** run the fail-closed `tools/audited_register.py` overlay, the additive fail-closed `tools/register_3adf31d9.py` topic-gap overlay (gaming, music and AI/technology entries) and the additive fail-closed `tools/register_21f3dd85.py` free-first overlay. Every factual field starts blank. Only `data/audit_64f8b973.json` decisions can populate it; an unreviewed candidate or missing quotation stops the build. The old `tools/apply_verify.py` applicator is retired and cannot mutate the audited register.

The validator compares the exact projection, checks quotation provenance (including labeled event JSON-LD), recurrence/year guards, blanks, parent cycles, source references, CSV cell values, all page memberships and every local link/fragment. A second rebuild must be byte-identical. Provenance validation is **not** automatic semantic fact-checking.

### Local preview

```sh
python3 -m http.server 8080 --bind 0.0.0.0
```

All assets and local links are relative, so the site works at a GitHub Pages subpath. No external fonts, browser API, localhost backend or JavaScript is required to read the tables. JavaScript only enhances search and filters.

### Optional browser / accessibility smoke test (Linux, Node 22+)

```sh
npm install --prefix .cache/browser --no-audit --no-fund \
  playwright-core@1.64.1 @sparticuz/chromium@153.0.0 axe-core@4.14.0
NODE_PATH=.cache/browser/node_modules node tests/browser_smoke.cjs --serve
```

Omit `--serve` when a static server already runs on port 8080. This checks 19 pages at desktop/mobile widths, filtering/reset/empty states (including the Cost filter), actual blank cells, cost badges, source/evidence links, the free-first landing tables, upcoming nearest-first ordering, mobile card layout, mobile overflow, no-JavaScript tables, console/asset errors and automated WCAG A/AA findings on seven core page types. Automated accessibility tests are not a complete accessibility certification. Browser binaries, screenshots and package installs stay outside Git.

## Site conventions

* **Upcoming order.** The Upcoming page groups the 70 dated, published entries into six time
  buckets — **Open now · Today · Next 7 days · Next 30 days · Next 90 days · Later** — and sorts
  nearest confirmed date first within each. Only approved 2026/2027 dates are displayed; no date is
  inferred. The canonical nearest-first order for those 70 rows is exported to
  `data/upcoming_order.json`, so the browser pass can assert it rather than re-derive it. An
  occurrence that has started but not finished is grouped under **Open now** rather than being given
  a misleading “in N days” label.
* **Focus ordering.** [Focus, one page](focus.html) carries the whole directory ordered
  **Gaming → Music → AI & technology → everything else**, free and soonest first inside each group.
  The same grouping drives the three topic subpages and the label on every row.
* **Cost labelling.** Each row's Cost column shows a short badge (**Free**, **Paid** or
  **Not stated**) derived from that row's exact approved admission quotation — never inferred. The
  full verified wording stays in the Admission column, and a badge whose free admission is
  conditional carries an explicit *Conditions apply — read the exact wording* hint. A blank price
  always renders **Not stated**: never silently free, never silently paid.
* **Mobile.** Below 820 px every events table reflows into stacked, labelled cards (each cell
  repeats its column header from `data-label`), and every table keeps its own independent search,
  filter and reset controls even on pages that hold several tables.
* **Topics.** Gaming, music and AI/technology have dedicated pages alongside the collections.
  Gaming and AI/technology were added in session `3adf31d9` from official pages only, and session
  `59f56c24` added the combined Focus view plus five official-calendar entries (including a quoted
  GDC price).
* **Overlapping coverage is kept, not silently merged.** Where two sessions independently captured
  the same event from different official pages, both rows are published with their own sources and
  the overlap is stated in the row's review notes — a value is never inherited from another row's
  source.

## Files and evidence

| Path | Purpose |
|---|---|
| `data/audit_f1fd3c36.json`, `tools/apply_audit.py` | Upstream research/tool retained unchanged; legacy labels are not approvals |
| `tools/upstream_candidates.py`, `data/upstream_refs_64f8b973.json` | Isolated candidate transform and preserved official 2026 Sketchfest reference |
| `data/audit_64f8b973.json` | Finite official evidence captures, selected tool excerpts and explicit field decisions |
| `data/audit_3adf31d9.json`, `tools/register_3adf31d9.py` | Additive fail-closed topic-gap overlay and its captures (gaming / music / AI) |
| `data/research/audit-3adf31d9.md` | Research log for that overlay: retrieval methods, approvals and deliberate non-approvals |
| `data/audit_21f3dd85.json`, `tools/register_21f3dd85.py` | Additive fail-closed free-first overlay and its captures (dated free music, free gaming, free AI; one paid tournament) |
| `data/research/audit-21f3dd85.md` | Research log for that overlay, including the SFPL all-programs-free mapping and retrieval honesty |
| `data/upcoming_order.json` | Canonical nearest-first order of the dated directory rows, asserted by the browser pass |
| `data/dashboard_order.json` | The free-first landing page's two main-section orderings (free dated; free recurring), same rationale |
| `data/events.json` | All audited records, including review-only dispositions; not all are published in the directory |
| `data/sources.json` | Exact-URL ledger; statuses and contextual decisions are separate |
| `data/audit_summary.json` | Reproducible counts/blank-field/date summary |
| `data/unverified_history.json` | **Unverified** inherited claims/findings; never a fallback |
| `data/events.csv`, `data/review.csv` | Directory-only export and complete candidate-review export |
| `tools/curation/` | Historical decision-authoring batches, with exact-quote assertions; not an automatic verifier |
| `data/events_*`, `data/events-weekly.json`, `data/events-annual.json`, `data/events-special.json` | Preserved earlier sessions’ research inputs |
| `COORDINATION.md` | Ownership, historical integration records, current checks and actual publication results |

## CI and publication

`Validate site` rebuilds the canonical data/site, runs the regression fixtures and UI smoke test, checks every local link, and **requires committed generated files to match the build**. It also reports every cited URL: definite 404/410 responses fail; challenge, server and transport outcomes stay unknown rather than becoming false verification claims. Reports/screenshots are workflow artifacts, not auto-committed event facts.

GitHub Pages is configured in branch mode: **`main` / root**. Merging validated committed HTML publishes it automatically; the validation workflow itself is not a deployment. Actual PR, merge and successful Pages build records are recorded in `COORDINATION.md` after they occur.

### Confirmed initial publication (PR #22)

Implementation [PR #22](https://github.com/buffedlizard55-lab/MaltaProj5/pull/22)
merged on **18 October 2026 at 03:59:24 UTC** as `bde10dc7b431111c14b602855f4bebc0b6dbc957`.
[PR checks](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39095344809)
and [post-merge validation](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39095524834)
passed, including 29 regressions, browser/accessibility, generated-file consistency
and URL gates. [Pages deployment](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39095524296)
succeeded; the Pages API reports **built** for that exact merge commit at 03:59:45 UTC.
Live dashboard, review and evidence pages were fetched and confirmed to contain the
new 163-directory / 79-held / 242-candidate snapshot. See `COORDINATION.md` for the
full publication record and explicitly unknown source-response outcomes.

### Final contextual tightening

A last source-context review moved the Nihonmachi 2027 candidate off the directory:
its August 7–8 dates are explicit, but the SF Japantown venue sentence belongs to
the prior edition’s recap. Venue remains blank, matching the same no-carryover rule
used for Pride and Fillmore. Current totals are **162 directory / 80 held**; no
candidate or official link was discarded. A dedicated regression prevents this
exception returning. The initial deployment counts above are historical.

The final tightening shipped in [PR #24](https://github.com/buffedlizard55-lab/MaltaProj5/pull/24),
merged **18 October 2026 at 04:15:16 UTC** as `b5e9afca8c6dcb15c59153d1c56137ba2a37c07d`.
Its [30-test PR gate](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39096365405)
and [post-merge validation](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39096451167)
passed. [Pages](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39096451005)
reported **built** for that commit at 04:15:37 UTC. Live dashboard and summary JSON
were fetched and confirmed at the current **162 directory / 80 held** counts.
