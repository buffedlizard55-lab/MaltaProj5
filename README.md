# SF Events — an evidence-first city directory

A static, source-linked inventory of recurring gatherings and dated programmes **inside San Francisco city**, with unresolved candidates published separately.

**Site:** https://buffedlizard55-lab.github.io/MaltaProj5/

**Research snapshot:** 18 October 2026. This is **not an exhaustive or live city calendar**.

## Current audited register

| Measure | Count |
|---|---:|
| Candidates assessed | 246 |
| Prior-main candidates retained (231 initial + 2 companion additions) | 233 |
| New official-calendar entries | 13 |
| Entries admitted to the city-only directory | 167 |
| Candidates held off the directory for review | 79 |
| Weekly / monthly / annual entries | 23 / 7 / 26 |
| Special, dated or cadence-unconfirmed entries | 111 |
| Exact cited official-source URLs / distinct domains | 242 / 140 |

The directory includes 14 programme umbrellas and their independently sourced child events. Counts are **entries, not unique city events**. Category and programme relationships are editorial; recurring classifications require their own evidence.

- [Dashboard](index.html) · [Upcoming — date-sorted](upcoming.html) · [Free first](free.html) · [Gaming · Music · AI focus](focus.html) · [Weekly](weekly.html) · [Monthly](monthly.html) · [Annual](annual.html) · [Special & dated](special.html)
- [Markets & food](markets.html) · [Museums & science](museums.html) · [Festivals & culture](culture.html) · [Community & outdoors](community.html)
- [Analysis](analysis.html) · [Flagged for Review](review.html) · [Sources and row-by-row evidence](sources.html)
- [Directory CSV](data/events.csv) · [All review records CSV](data/review.csv)

## New in this update (T32, snapshot still 18 October 2026)

- **Executive summary** on the dashboard: dated entries running or starting within 30 days of the snapshot, soonest first, each with its cost label.
- **Upcoming page**: approved dated entries sorted soonest-first (running now highlighted), then weekly/monthly recurring entries with **no invented next date**.
- **Cost on every row**: a badge derived only from the audited admission text — `FREE`, `Free with paid parts`, `Paid`, `Cost in admission text`, or `Cost not stated — unverified` (blank is never called free). A Cost filter is in the table tools.
- **Free first page**: the whole directory ordered free → paid → cost-not-stated.
- **Gaming · Music · AI focus page**: groups matched only from audited event names (Gaming: Pokémon World Championships 2026; Music: 11 name-matched entries; **AI: none found — flagged as a coverage gap, nothing invented**), then everything else.
- Regularly occurring (weekly/monthly/annual) vs special/dated split is unchanged and remains on its own pages. Mobile: sticky event column, horizontal table scroll, 2-column cards.

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

`consolidate.py` first reconstructs historical candidates from the preserved research inputs, preserves the newer mainline companion audit (including its two added candidates) in an isolated temporary candidate-history tree, then **must** run the fail-closed `tools/audited_register.py` overlay. Every factual field starts blank. Only `data/audit_64f8b973.json` decisions can populate it; an unreviewed candidate or missing quotation stops the build. The old `tools/apply_verify.py` applicator is retired and cannot mutate the audited register.

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

Omit `--serve` when a static server already runs on port 8080. This checks 12 pages at desktop/mobile widths, filtering/reset/empty states, actual blank cells, source/evidence links, no-JavaScript tables, console/asset errors and automated WCAG A/AA findings on the four core page types. Automated accessibility tests are not a complete accessibility certification. Browser binaries, screenshots and package installs stay outside Git.

## Files and evidence

| Path | Purpose |
|---|---|
| `data/audit_f1fd3c36.json`, `tools/apply_audit.py` | Upstream research/tool retained unchanged; legacy labels are not approvals |
| `tools/upstream_candidates.py`, `data/upstream_refs_64f8b973.json` | Isolated candidate transform and preserved official 2026 Sketchfest reference |
| `data/audit_64f8b973.json` | Finite official evidence captures, selected tool excerpts and explicit field decisions |
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
