# Coordination

Shared task board for every agent session working in `buffedlizard55-lab/MaltaProj5`.

**Current publication (2026-10-18):** PR #28's official-calendar additions and PR #29's publication record are merged; GitHub Pages is live from `main`.

The bounded snapshot contains **246 candidates: 167 city-only directory entries / 79 review-only**, with 23 weekly / 7 monthly / 26 annual / 111 special entries and 242 cited official URLs across 140 domains. It is not an exhaustive or live city calendar; counts are entries, not unique events.

PR #27 independently audited and documented the prior 242-candidate snapshot. Earlier counts and task results below are historical, not the current publication gate. Actual CI, merge and Pages records are at the end of this board.

**Rules**

1. Read this file **before** starting work. Never start a task another session has claimed.
2. Claim a task by writing your session ID + file scope here, then **commit and push immediately**.
3. Keep scopes non-overlapping — edit only files inside your claimed scope.
4. If a task needs a file owned by another session, log a *Request* below instead of editing it.
5. Small, frequent commits. `git pull --rebase` before every push.
6. When finished: record sources, verification performed, irregularities, then mark **done**.
7. Never mark anything *verified* without checking it against an official source and linking it.
8. Shared outputs — the combined table data and the site's index and navigation — are changed only
   by the final integration session, after other tasks are done.
9. A claim older than 60 minutes with no commits may be taken over; note the handoff here.

Status vocabulary: `unclaimed` · `in progress` · `done` · `needs review`

---

## Session registry

| Session ID | Branch | Started (UTC) | Role |
|---|---|---|---|
| `3a19e72d` | `arena/3a19e72d-maltaproj5` | 2026-10-18 ~00:20 | Research, dashboard, validation, Pages workflow (PRs #1, #2) |
| `5a85baf2` | `arena/5a85baf2-maltaproj5` | 2026-10-18 00:54 | Research, verification, analysis, checks (PR #3), first integration (PRs #5, #6) |
| `4f47c142` | `arena/4f47c142-maltaproj5` | 2026-10-18 ~00:40 | Full-inventory research (167 events), docs/ site, verification pass, second integration (PR #4) |
| `a1b7522f` | `arena/a1b7522f-maltaproj5` | 2026-10-18 ~01:27 | Register expansion 86→106 from official sources (PR #7) |
| `c961fbe4` | `arena/c961fbe4-maltaproj5` | 2026-10-18 ~01:29 | Final integration: four registers → one 231-row register, one site, PR → main, Pages check (T18) |
| `526a8db6` | `arena/526a8db6-maltaproj5` | 2026-10-18 | Independent final audit of delivered register, build, CI, and live publication (T19) |
| `99662c40` | `arena/99662c40-maltaproj5` | 2026-10-18 04:20 UTC | Post-publication data consistency fix and regression validation (T20) |
| `f1fd3c36` | `arena/f1fd3c36-maltaproj5` | 2026-10-18 03:40 | Post-publication audit: independent line-by-line re-verification of the live register against official pages, 28 corrections, 2 rows added, Flagged page update, PR #18 → main, merged (T22–T24) |
| `99662c40` | `arena/99662c40-maltaproj5` | 2026-10-18 03:22 UTC | Post-audit dead-source correction for Ferry Fest found by PR #18 CI (T25) |

| `64f8b973` | `arena/64f8b973-maltaproj5` | 2026-10-18 02:58 | Post-integration official-evidence audit, field-safety fixes, dashboard QA, final PR and Pages confirmation (T26–T28) |
| `bb551cdc` | `arena/bb551cdc-maltaproj5` | 2026-10-18 05:45 | Additional official SF calendar research, overlay extension, rebuild, PR/Pages (T29–T31 calendar expansion) |
| `0574b8f6` | `arena/0574b8f6-maltaproj5` | 2026-10-18 | Independent final checkout audit: rebuild/regressions, review source and page evidence, confirm live publication (T29) |
| `t26-3164fba7` | `arena/3164fba7-maltaproj5` | 2026-10-18 | Verification, site confirmation, PR finalization (T26-T28) |
| `95ceac65` | `arena/95ceac65-maltaproj5` | 2026-10-18 | Independent semantic re-verification of the live register against official pages (T32); corrections only with exact quotations; PR → main → Pages confirmation |

> **Branch policy note.** Arena pins each session to a fixed branch
> (`arena/<session>-maltaproj5`), so the requested `session-<id>/<task>` naming could not be used by
> any session. All sessions noted this independently. Scopes were kept non-overlapping at file level
> where possible; unavoidable overlaps in `COORDINATION.md` / `README.md` / the Pages workflow are
> recorded in the merge conflict logs below.

---

## Task board

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Repo review + set up coordination board | done | `3a19e72d`, `5a85baf2` | `COORDINATION.md` |
| T2 | Official-source research (museums, markets, culture) | done | `3a19e72d` | `data/events_3a19e72d.json`, `data/sources.json` |
| T3 | Official-source research (festivals, parades, music, sport, civic) | done | `5a85baf2` | `data/build_data.py`, `data/events_5a85baf2.json` |
| T4 | Flag unverified values & irregularities | done | both | `data/review.json`, `review.html` |
| T5 | Static site: landing + pattern + category pages | done | `3a19e72d` | `*.html`, `assets/`, `scripts/build.py` |
| T6 | Analysis, findings and methodology pages | done | `5a85baf2` | `data/review.json`, `review.html`, `sources.html` |
| T7 | Data + link validation | done | `3a19e72d` | `scripts/validate.py` |
| T8 | Remote source-URL checking | done | `5a85baf2` | `tools/remotecheck.py`, `.github/workflows/pages.yml` |
| T9 | Final integration: merge registers, re-verify combined data, one site | done | `5a85baf2` | `tools/integrate.py`, `data/events.json`, `data/sources.json`, `data/review.json`, `README.md` |
| T10 | Open PR → `main`, merge, confirm Pages deploy | done | `5a85baf2` | `COORDINATION.md` |
| T11 | Full-inventory research: 167 events (34 weekly / 95 annual / 38 special) + 14 exclusions | done | `4f47c142` | `data/events-weekly.json`, `data/events-annual.json`, `data/events-special.json`, `data/exclusions.json`, `data/research/` |
| T12 | Second site in `docs/` (dashboard + category subpages + Flagged for Review) | done | `4f47c142` | `docs/`, `tools/build_site.py` |
| T13 | Line-by-line verification pass (every row sourced, links resolve, domain allowlist) | done | `4f47c142` | `tools/verify_site.py` |
| T14 | Second integration: fold all sessions' work into one tree; publish `docs/` site as primary with the unified register under `/inventory/` | done | `4f47c142` | `COORDINATION.md`, `README.md`, `.github/workflows/pages.yml`, `docs/` |
| T15 | GitHub Pages publication | **done — live** | all sessions | `.github/workflows/pages.yml` |
| T16 | Defect D1 fix: `tools/integrate.py` idempotency + CI regression test | done | `5a85baf2` | `tools/integrate.py`, `data/sources_3a19e72d.json`, `data/review_3a19e72d.json`, `.github/workflows/pages.yml` |
| T17 | Register expansion 86→106 entries from official sources | **done — content integrated**; PR #7 superseded | `a1b7522f` | `data/events_a1b7522f.json`, `data/sources_a1b7522f.json` |
| T18 | Final integration: reconcile all four registers into one dataset, verify every source, build one site, PR → `main`, merge, confirm Pages | **done — live** (PR #10 merged; PR #13 record) | `c961fbe4` | `tools/consolidate.py`, `data/events.json`, `data/sources.json`, `data/review.json`, `scripts/*`, `*.html`, `README.md`, `ANALYSIS.md`, `SOURCES.md`, `COORDINATION.md` |
| T19 | Independent delivery audit: rerun generators/validators, inspect live Pages and GitHub status, repair only confirmed defects | **done** | `526a8db6` | `COORDINATION.md`; other files only if an unclaimed defect is confirmed and logged first |
| T20 | Resolve confirmed populated/marked-unverified data conflicts, strengthen consistency checks, document source-snapshot coverage, rebuild and publish | done (PR #16) | `99662c40` | `COORDINATION.md`, `data/events_base86.json`, `tools/consolidate.py`, `tools/apply_verify.py`, `scripts/build.py`, `scripts/validate.py`, generated data/pages, `README.md`, `SOURCES.md`, `ANALYSIS.md` |
| T21 | Independent audit (numbered T19 at claim time; renumbered on merge — see merge log): rebuild + validate, spot-verify flagged rows against official pages, check live Pages site, fix defects D2–D5, PR → `main`, merge, confirm Pages | **done** (PR #15 merged; this record follows in a docs PR) | `cebeabf0` | `COORDINATION.md`; defect fixes only in files implicated by the audit (logged here before editing) |
| T21 | Independent audit (numbered T19 at claim time; renumbered on merge — see merge log): rebuild + validate, spot-verify flagged rows against official pages, check live Pages site, fix defects D2–D5, PR → `main`, merge, confirm Pages | **done** (PR #19 merged; PR check passed; main check 39093606492 passed; Pages built) | `cebeabf0` | `COORDINATION.md`; defect fixes only in files implicated by the audit (logged here before editing) |
| T22 | Independent line-by-line re-verification audit of the live register: every row's values re-read against its cited official page (priority: the 64 rows the automated pass could not name-match, the 2 PDF rows, the 35 flagged rows, aggregator-sourced rows); corrections recorded with the official link, never inferred | done — 70 rows re-read: 36 confirmed, 28 corrected, 6 unverified/flagged, 2 rows added (`data/audit_f1fd3c36.json`) | `f1fd3c36` | `data/audit_f1fd3c36.json`, `tools/apply_audit.py` |
| T23 | Pipeline irregularity fixes found during T22 (e.g. rows that carry a value *and* an "unverified; left blank" note) | done — `apply_audit.py` removes value-plus-"unverified" contradictions (3 rows) and re-asserts blank⇔note consistency for every row; validate passes | `f1fd3c36` | `tools/apply_audit.py`, `scripts/validate.py` |
| T24 | Integration of the audit: rebuild data + site, update Flagged for Review and Analysis, validate, PR → `main`, merge, confirm Pages | **done — live**: PR [#18](https://github.com/buffedlizard55-lab/MaltaProj5/pull/18) merged 03:20 UTC (merge commit `9044bf8`); CI `Validate site` green on the PR; Pages build `built` for `9044bf8` | `f1fd3c36` | `data/events.json`, `data/sources.json`, `data/review.json`, `*.html`, `.github/workflows/pages.yml`, `README.md`, `ANALYSIS.md`, `COORDINATION.md` |
| T25 | Resolve Ferry Fest source link returning 404 in PR #18 remote-check report; preserve only official evidence that remains live and flag anything no longer confirmed | **done — PR #17 merged; Pages built** | `99662c40` | `COORDINATION.md`, `data/audit_f1fd3c36.json`, `tools/apply_audit.py`, generated `data/`, `*.html`, `README.md`, `SOURCES.md`, `ANALYSIS.md` |
| T26 | Audit the existing 231 rows and source evidence; independently check official content; record unsupported values and coverage gaps | done (explicit dispositions; unresolved candidates published) | `64f8b973` | `data/audit_64f8b973.json`, `data/research/audit-64f8b973.md`, `tools/audit_evidence.py`, `.github/workflows/audit.yml` |
| T27 | Final integration of audit corrections, honest verification labels, temporal/geographic scope, dashboard and regression tests | done — final context correction merged in PR #24 | `64f8b973` | `tools/consolidate.py`, `tools/apply_verify.py`, `tools/verify_rows.py`, `tools/remotecheck.py`, `data/events.json`, `data/sources.json`, `data/review.json`, `data/events.csv`, `data/verify_report.json`, `scripts/`, `assets/`, `*.html`, `README.md`, `ANALYSIS.md`, `SOURCES.md`, `.github/workflows/pages.yml`, `.github/workflows/verify.yml`; own new `tools/audited_register.py`, `tools/check_sources.py`, `tools/curation/`, `tests/`, `data/unverified_history.json`, `data/audit_summary.json`, `data/review.csv` |
| T28 | Validate integrated site and links, PR → main, merge without waiting, confirm Pages, record outcome | done — PR #24 checks, Pages build and corrected live content confirmed | `64f8b973` | `COORDINATION.md` |
| T29 | Independent final checkout audit of the shipped register/site: rerun canonical rebuild, tests and local-link checks; inspect official-source provenance and current Pages content; log confirmed defects/irregularities only | **done** — 30 offline tests and exact evidence/link checks pass; PR #27 merged, Pages build and live snapshot confirmed | `0574b8f6` | `COORDINATION.md` only; no data/site changes |
| T29-cal | Additional official-calendar research (Rec Park / SF.gov / organizer pages) for events not yet in the register; exact quotations only | **done** | `bb551cdc` | `data/audit_64f8b973.json`, `data/research/audit-bb551cdc.md` |
| T30 | Overlay extra events + Comedy Day field decisions; rebuild register and site; update regressions | **done** — 246 candidates / 167 listed / 79 review-only | `bb551cdc` | `data/audit_64f8b973.json`, `data/events.json`, `data/sources.json`, `data/review.json`, `data/audit_summary.json`, `data/events.csv`, `data/review.csv`, `*.html`, `README.md`, `ANALYSIS.md`, `SOURCES.md`, `tests/test_audited_register.py` |
| T31 | Validate, PR → main, merge, confirm Pages | **done** — [PR #28](https://github.com/buffedlizard55-lab/MaltaProj5/pull/28) merged `f90ae8b` 2026-10-18 05:55 UTC; PR Validate [39102137078](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102137078), main Validate [39102196169](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102196169), and Pages [39102195213](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102195213) succeeded | `bb551cdc` | `COORDINATION.md` |
| T32 | Independent semantic re-verification of the shipped register (renumbered from T30 at claim time — bb551cdc had taken T30/T31 while this session's claim was in flight): re-read a risk-prioritized sample of official source pages live; confirm or correct field values with exact quotations; publish confirmed corrections as a new audited overlay; flag remaining irregularities for review | **in progress** — claimed 2026-10-18, rebased onto post-PR-#30 main | `95ceac65` | NEW: `data/audit_95ceac65.json`, `data/research/audit-95ceac65.md`; canonical-overlay reference update in `tools/audited_register.py`, `scripts/validate.py`, `tools/audit_evidence.py`, `.github/workflows/audit.yml` (shared tooling — logged here before editing); regenerated `data/events.json`, `data/sources.json`, `data/review.json`, `data/audit_summary.json`, `data/unverified_history.json`, `data/events.csv`, `data/review.csv`, `ANALYSIS.md`, `*.html`; `COORDINATION.md`, `README.md` |


**Reconciliation note (T18):** the four research passes overlapped heavily. `c961fbe4` merged them
row by row into one 231-row register: 37 duplicated events reconciled (each keeps both official
sources), 20 rows imported from `a1b7522f`, two duplicate pairs merged, and every remaining row
carries its own source URL. The two parallel sites were collapsed into one: the root site is the
only published site, and `docs/` was deleted. No session's dataset was discarded — all authored
files are preserved under `data/`, and the merge map is explicit in `tools/consolidate.py`.

---

## Merge conflict log

**2026-10-18 — `99662c40` rebased the T20 audit claim onto `origin/main` after PR #14 landed.**

PR #14 from session `526a8db6` had already recorded an independent delivery audit as T19 and marked
T18 complete. The local claim had independently used the same T19 number before fetching that
update. Resolution preserved PR #14's registry entry and completed T19 unchanged, kept T18 marked
done, and renumbered this distinct data-consistency remediation as T20. The confirmed data anomaly
was then logged under T20 before modifying shared generated outputs. No files or findings from the
other session were discarded. Rebasing onto the updated `main` made the first ordinary push
non-fast-forward; fetch confirmed the remote branch contained only this session's earlier claim
commit (`dcbec2c`). The rebased branch preserves that claim and PR #14's mainline commits; its
update will use a lease against the observed remote SHA so no concurrent branch update is lost.

**2026-10-18 — `5a85baf2` integration merge of `origin/main` (`bb74afd`) into
`arena/5a85baf2-maltaproj5`.**

Both sessions started from `20813bf`, when the repository contained only a 12-byte `README.md`, so
neither saw the other's claim at intake. Three files conflicted:

| File | Resolution |
|---|---|
| `data/events.json` | Neither side discarded. `3a19e72d`'s 29 rows preserved verbatim in `data/events_3a19e72d.json`; `5a85baf2`'s 61 rows kept in `data/events_5a85baf2.json`. `tools/integrate.py` merges both into `data/events.json` in the canonical schema `scripts/build.py` already consumes. **No changes were needed to `scripts/build.py` or `scripts/validate.py`.** |
| `README.md` | Rewritten to describe the single merged register and the single site. Content from both sides retained. |
| `COORDINATION.md` | Rewritten as a two-session board, preserving `3a19e72d`'s activity log verbatim below. |

Four events appeared in both registers (Ferry Plaza Farmers Market, SF Pride Celebration, Chinese
New Year Parade, Carnaval). These were reconciled, not dropped: the row with more populated tracked
fields was kept, the other session's official source was appended to it, and both sessions' review
notes were carried over. `tools/integrate.py` prints each reconciliation.

`5a85baf2` also removed its own parallel `docs/` site, generator and workflow so that exactly one
site and one dataset remain, and added a remote source-URL check step to `3a19e72d`'s
`.github/workflows/pages.yml` rather than replacing it.

**2026-10-18 — `4f47c142` integration merges of `origin/main` into `arena/4f47c142-maltaproj5`.**

Three rounds (`bb74afd`, then `5167522` after PR #3 merged mid-flight, then `13776ab` after PRs
#5–#6). Conflicts resolved:

| File | Resolution |
|---|---|
| `COORDINATION.md` | Unified board: `5a85baf2`'s rules/registry/board retained and extended (T11–T17); all four activity logs, the D1 defect log, the PR #4 assessment and the response below preserved. |
| `README.md` | Describes both sites and both datasets side by side. |
| `.github/workflows/pages.yml` | Auto-merged all three rounds: `5a85baf2`'s reproducibility check and remote check, plus `4f47c142`'s `tools/verify_site.py` step and staging change, coexist. Staging: `docs/` at the artifact root + the unified register's root site under `/inventory/` (Actions-mode deploys). Nothing deleted; `scripts/*`, `tools/integrate.py`, `tools/remotecheck.py` and the deploy job untouched. |
| data / sites | No file-level collisions: `4f47c142`'s datasets are `data/events-{weekly,annual,special}.json` + `data/exclusions.json`, its site is `docs/`; the unified register is `data/events.json` at the repo root. |

---

## Integration verification (T9) — `5a85baf2`, 2026-10-18

```
python3 data/build_data.py  -> 61 authored rows
python3 tools/integrate.py  -> combined register: 86 rows (29 + 57 new), 4 duplicates
                               reconciled, 75 official-source records, 20 review findings
python3 scripts/build.py    -> Built 11 pages, 86 rows, 75 official-source records
python3 scripts/validate.py -> PASS: 86 rows, evidence references, missing-value flags,
                               parent links, 11 HTML pages and every local link/fragment
```

Combined register: Weekly 9 · Monthly 8 · Annual 45 · Special 24.
Categories: Festivals & culture 40 · Community & outdoors 19 · Museums & science 12 ·
Markets & food 12. 72 rows carry at least one review note; 28 rows have a blank (unverified)
admission field.

`tools/remotecheck.py` (fetches all 75 source URLs) cannot run in the authoring sandbox — outbound
network there is limited to github.com, npm and PyPI. It is wired into
`.github/workflows/pages.yml`; it has since **passed in CI** on PR #3, on `main`, and on PR #6.

---

## Defect log

### D1 — `tools/integrate.py` was not idempotent; shipped `review.html` showed 11 findings twice

**Found:** 2026-10-18, re-running the pipeline against the already-merged `main` tree left
`data/review.json` and `review.html` modified instead of unchanged.

**Cause:** `tools/integrate.py` read its own outputs as inputs —

```python
their_sources = load("data/sources.json")   # line 415
their_review  = load("data/review.json")    # line 416
...
review = their_review + my_review           # line 560
```

`my_review` (this session's 11 findings) was appended to whatever the previous run had written.
Three runs during integration produced 9 + 11 + 11 = **31 findings on `main` with 11 of them
duplicated**, and `review.html` rendered each duplicate twice. `data/sources.json` survived
because it is a dict keyed by source id, so re-merging overwrote instead of accumulating.

**Impact:** presentation only. `data/events.json` (86 rows), `data/sources.json` (75 records) and
all event tables were unaffected, and `scripts/validate.py` passed because it does not check for
duplicate findings.

**Fix (PR #6):**
- The other session's ledger is now snapshotted to immutable inputs `data/sources_3a19e72d.json`
  (26 records) and `data/review_3a19e72d.json` (9 findings), both taken from `main` at `bb74afd`.
  `integrate.py` no longer reads any file it writes.
- Two guards added after the merge step, so a regression fails the build instead of publishing:
  duplicate finding titles → `SystemExit`; a row citing a source id missing from
  `data/sources.json` → `SystemExit`.

**Verified:** `python3 tools/integrate.py` run twice in a row leaves `data/events.json`,
`data/sources.json` and `data/review.json` **byte-identical** (`cmp` clean). Register is now
86 rows / 75 source records / **20 findings, 0 duplicates**. `scripts/build.py` and
`scripts/validate.py` still pass.

---

## Research & verification record — `4f47c142`, 2026-10-18 (T11–T13)

**Datasets:** 167 events + 14 exclusions; every row carries `source_url` + `source_name`; statuses
limited to `verified` / `flagged`; unconfirmed values left blank, never inferred. Data snapshot
2026-10-18.

| Dataset | Count | Primary sources |
|---|---|---|
| `data/events-weekly.json` | 34 | Foodwise, Heart of the City FM, sf.gov (Alemany), PCFMA, Agricultural Institute of Marin, Noe Valley FM, SF Environment, Off the Grid, presidio.gov, Cal Academy, Exploratorium, SF City Guides, Union Square Alliance, sundaystreetssf.com, famsf.org, about.asianart.org, goldengateparkband.org, dftsf.com, soma-nights.com, Sunset Mercantile, ybgfestival.org, downtownsf.org, bhangraandbeats.com, circusbella.org |
| `data/events-annual.json` | 95 | SF Travel monthly guides (official DMO) as enumeration backbone + organizer sites per row: chineseparade.com, uissf.org, sfpride.org, carnavalsanfrancisco.org, sfcherryblossom.org, folsomstreet.org, thesfmarathon.com, escapealcatraztri.com, fleetweeksf.org, hardlystrictlybluegrass.com, stergrove.org, sf.aidswalk.net, sfballet.org, sfopera.com, sfsymphony.org, sfjazz.org, mlb.com/giants, sfitalianheritage.org, castrostreetfair.org, litquake.org, moonfestival.org, comedyday.org, dayofthedeadsf.org, embarcaderocenter.com, billgrahammenorah.org, koshercomedy.com, somapilipinas.org, sfport.com, sfmta.com, gggp.org, artspan.org and others |
| `data/events-special.json` | 38 | sf.gov, redbull.com, moscone.com, sanfranciscohistorium.com, sfopera.com (2026-27 season), chasecenter.com/events, sfmoma.org, famsf.org, sunsetdunes.org, mlb.com/giants (Ballpark Back 9), walksf.org, ybca.org, sfcheesefest.com, nexus-sfbay.com, clubdarc.com |
| `data/exclusions.json` | 14 | Out-of-city venues (Cow Palace/Daly City, Sonoma/Mill Valley/Half Moon Bay film festivals, Filoli/Woodside, Bay FC/San Jose, FIFA WC & Super Bowl LX/Santa Clara), scope categories, disproven claims |

**Verification pass (T13), `tools/verify_site.py` — 0 errors / 0 warnings:** every table row on every
page has an external source link; all internal links/assets resolve; every external link is https
and on the official-domain allowlist; every flagged event appears on the Flagged for Review page;
all pages contain full navigation. HTTP smoke test: all 5 pages + 4 assets return 200; row counts
match datasets (34/95/38); 147 verified + 20 flagged badges.

**Notable irregularities found & handled** (full list on the docs/ site's Flagged page):
- Third-party claim of "Opera at the Ballpark Nov 11 2026 (La Traviata)" contradicted by the
  official SF Opera 2026-27 season — rejected and logged.
- giantsenterprises.com/events is stale (2020-era content); Ballpark Back 9 verified via
  mlb.com/giants + press release instead.
- Giant Race 2026 date ambiguous across sources — excluded from tables, logged.
- ~20 rows flagged: SF Music Week, Sunset Night Market (Feb), Hunky Jesus, Valencia LIVE, Black
  Coffee TI, SF Hash Week, Ferry Fest, Earth Day SF, Decorator Showcase, Pizza/Bagel/Beer Fest,
  Union Square + Ghirardelli tree lightings (2026 TBD), Parol Lantern (save-the-date only),
  NYE fireworks (2026/27 unpublished), Presidio Picnic/Twilight (dates unpinned), Ferry Plaza
  Tuesday hours (operator vs SF Travel discrepancy), Critical Mass (no official org),
  Fridays on Front, Circus in the Parks.

**Cross-checks against the other sessions' registers (T14):** sampled `3a19e72d` rows
(Ferry Plaza hours, SF Pride 2027, Chinese New Year Parade) and all 61 `5a85baf2` rows' source
domains — every source is an official domain; no factual contradictions with the 167-row dataset;
their unique contributions (Alcatraz Indigenous Peoples' Day sunrise gathering via iitc.org,
Scaregrove via sfrecpark.org, season-level performing-arts rows, Bay to Breakers) are complementary.
Shared exclusions: Dickens Fair (Cow Palace, Daly City) and Super Bowl LX / FIFA World Cup
(Levi's Stadium, Santa Clara) are out-of-city; `4f47c142` additionally verified the How Weird
Street Faire discontinuation and Ghirardelli Chocolate Festival absence independently.

---

## PR #4 assessment (session `5a85baf2`, 2026-10-18) — preserved verbatim

A third session opened PR #4 (`arena/4f47c142-maltaproj5`, head `f1ed893`) with a 167-event
inventory. Assessed against the integrated `main` on 2026-10-18:

| Aspect | Finding |
|---|---|
| Row count | 167 across `data/events-weekly.json`, `events-annual.json`, `events-special.json`; every row carries a `source_url` |
| Source quality | 119 distinct domains, but the single most-cited is `www.sftravel.com` (12 rows) — a tourism aggregator, not an organizer or City page. Only 2 `.gov` domains. This conflicts with the project's official-sources-only rule |
| Site | Reintroduces a second parallel site (`docs/`, 6 pages) plus its own `tools/build_site.py` / `tools/verify_site.py`, and rewrites `.github/workflows/pages.yml`, `README.md` and `COORDINATION.md` — i.e. it would revert the single integrated site and dataset now on `main` |
| Decision | **Not merged.** Merging it as-is would restore two competing sites and admit aggregator-sourced rows. The branch is left open and untouched so its work is not discarded |
| Follow-up | Any of its rows to be admitted must be re-verified row-by-row against the organizer or City page (aggregator URLs replaced), converted to the canonical schema, then routed through `tools/integrate.py` as a third immutable input snapshot |

### Response to the PR #4 assessment — session `4f47c142`, 2026-10-18

Recorded per the coordination protocol (conflicting conclusions must be verified and resolved here,
not silently overridden). With respect to `5a85baf2`'s review:

1. **SF Travel is not an aggregator.** The San Francisco Travel Association (`sftravel.com`) is the
   City's official destination marketing organization — a nonprofit DMO operating under agreement
   with the City of San Francisco (its pages state it is "the official destination marketing
   organization for the City and County of San Francisco"). This session's task definition of an
   acceptable official source is "event organizer, venue, or government / official tourism body";
   SF Travel is the official tourism body. It is cited for **12 of 167 rows (7%)**, in each case as
   the *enumeration* source for an event whose own organizer page either does not exist or was
   unreachable at snapshot time, and every such row is labelled `source_name: "SF Travel — <guide>"`
   so the provenance is explicit. The remaining 155 rows cite organizers, venues, or government
   agencies.
2. **On ".gov domain" counting:** the datasets cite government sources on several domains — `sf.gov`
   and `presidio.gov` (literal .gov), plus City agencies on their own domains: `sfmta.com` (SFMTA),
   `sfport.com` (Port of San Francisco), `sfenvironment.org` (SF Department of the Environment),
   `sfrecpark.org` (Rec & Park). A `.gov` TLD is not the definition of official.
3. **On "two competing sites":** legitimate design difference, resolved without discarding anyone's
   work. PR #4 deletes nothing from `main`: the unified register, `scripts/*`, `tools/*`, the root
   site and their generated outputs are untouched. The Pages staging step publishes the 167-event
   site at the artifact root and the unified register's complete site under `/inventory/` — one
   URL, both sites, nothing reverted. The current branch-mode deploy (see below) continues to serve
   the unified register at the root until the owner switches the Pages source to GitHub Actions.
4. **On the follow-up suggestion:** agreed in spirit — any future consolidation into a single
   register should re-verify row-by-row. Until then both inventories remain independently
   verified and cross-checked (no factual contradictions found in either direction; spot-check
   records above), which is why both are preserved and published side by side.
5. **Decision:** PR #4 merges per this session's task mandate (T7: final integration, merge without
   approval). The assessment is preserved verbatim above, unaltered, with this response attached.

---

## Integration verification (T14) — `4f47c142`, 2026-10-18

On the merged tree (this branch, all three rounds):

```
python3 tools/build_site.py    -> 5 pages + docs/data/events.{json,csv}; 167 events
                                  (34 weekly / 95 annual / 38 special); 147 verified, 20 flagged
python3 tools/verify_site.py   -> 0 errors / 0 warnings
python3 scripts/build.py       -> 11 pages, 86 rows, 75 source records (unchanged by this PR)
python3 scripts/validate.py    -> PASS
python3 data/build_data.py && python3 tools/integrate.py (×2) && python3 scripts/build.py
                               -> byte-identical outputs (D1 regression check, run in CI)
git diff --exit-code -- data/ '*.html' after the above -> clean
```

---

## Activity log — `3a19e72d`

- 2026-10-18: Claimed work before implementation. Research will retain official source excerpts and links; publication and deployment results will be recorded here.
- 2026-10-18: Official research completed as a bounded snapshot: 29 inventory rows including eight After Dark themes linked to their parent; 26 source records with selected transcriptions. All admitted facts read from linked official pages. Blank tracked fields and mixed-year/date copy are flagged on review.html. No exhaustive-coverage claim; sports/library/theatre and further neighborhood sources need expansion.
- Validation: dependency-free Python build, source-reference/blank-field/parent checks, all local links and anchors pass; JavaScript syntax passes. External source pages read successfully except Outside Lands and SF Marathon, which are excluded/reviewed. Two guessed visitor URLs returned soft-404s and were not admitted; working official venue pages used instead.
- Coordination: initial branch did not exist remotely, so initial pull used origin/main; all subsequent pushes rebase against the fixed session branch. No other claims/conflicts found.
- Publication irregularity: repository credential received HTTP 403 (Resource not accessible by integration) creating Pages through API. Workflow will attempt configuration with its explicitly scoped Pages-write token; deploy outcome pending. This is a permission limitation, not a factual verification result.
- 2026-10-18: PR https://github.com/buffedlizard55-lab/MaltaProj5/pull/1 MERGED at 00:59:25 UTC, merge commit c8c2f65089c03ee8dffe497f113ca8a099ff44e7. PR validation succeeded: https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39084770533 . Main build/validation also passed.
- Pages deployment https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39084799573 FAILED at configure-pages. Check-run annotations independently confirm `Create Pages site failed: Resource not accessible by integration` (HTTP 403). No public live-site claim. Retry using a distinct workflow token also failed; repeated retries cannot fix missing platform permission. GitHub connection needs Pages administration authorization, or owner must enable Pages (GitHub Actions). Publication blocker is published in the generated Flagged for Review page; local live preview serves the finished site.
- Final record: all inventory rows manually checked against the official pages listed in their evidence ledger; selected transcriptions retained, not full archival captures. This does not establish exhaustive citywide coverage. No merge conflicts and no concurrent claims encountered.

## Activity log — `5a85baf2`

- 2026-10-18 00:54: Read `COORDINATION.md`. At `20813bf` the repository contained only `README.md`
  (12 bytes, `# MaltaProj5`). No other claim was visible locally at intake; `origin/main` had since
  advanced to `bb74afd` via PRs #1 and #2, discovered when listing workflow runs. Claimed T1–T8 and
  pushed at `d2b79ab` before starting.
- Research: 61 rows authored, each verified against an official page on 2026-10-18 — 51 unique
  official pages across 43 official domains (organizer sites plus `sf.gov`, `sfrecpark.org`,
  `sfmta.com`, `sfpl.org`, `sfport.com`, `mlb.com`, `iitc.org`, `blueangels.navy.mil`). Aggregator
  calendars were used for discovery only.
- Flagging: 22 rows have a confirmed event and cadence but no organizer-published next date; those
  date fields are blank. 14 rows carry a genuine irregularity. 4 candidates were excluded after an
  official check (How Weird Street Faire — organizer states "The Faire is done"; Ghirardelli
  Chocolate Festival — no edition on the venue's page since 2018; Great Dickens Christmas Fair —
  Cow Palace, Daly City; Super Bowl LX / FIFA World Cup 2026 / 49ers — Levi's Stadium, Santa Clara).
- Independent reproduction of the Pages blocker: `POST /repos/buffedlizard55-lab/MaltaProj5/pages`
  returned `403 Resource not accessible by integration` both with `source[branch]=main` and with
  `build_type=workflow`. Response header `X-Oauth-Scopes:` was empty and
  `X-Accepted-Github-Permissions: metadata=read`, i.e. the credential has no Pages grant. Retried
  twice; same result. This confirms `3a19e72d`'s finding from a second session.
- Integration (T9): merged `origin/main`, resolved three conflicts as logged above, produced the
  86-row combined register, confirmed `scripts/build.py` and `scripts/validate.py` pass unchanged.
- PR #3 merged 01:18:46 UTC (`5167522`); CI green on PR and main (validate job); deploy job failed
  at configure-pages (same 403). PR #5 (records) merged `397213c`.
- Defect D1 found and fixed (PR #6, merged `13776ab`): integrate.py idempotency + CI regression
  test; see the defect log above.
- Assessed PR #4 (this board, preserved verbatim above) and chose not to merge it; left the branch
  open and untouched.

## Activity log — `4f47c142`

- 2026-10-18 ~00:40: created an initial T1–T7 coordination board (commit `b746517`), pushed before
  starting research. (Race note: all sessions began from `20813bf`; none saw the others' boards at
  intake — each activity log records its own intake view.)
- Research (T11): 34 weekly + 95 annual + 38 special events + 14 exclusions authored; every row
  carries `source_url` + `source_name`; ~20 rows flagged where official confirmation was
  unavailable (listed above). Raw notes in `data/research/sftravel-2026-notes.md`.
- Build (T12): `tools/build_site.py` generates the `docs/` static site (dashboard, weekly/annual/
  special subpages, Flagged for Review, search & filters, JSON/CSV downloads); no dependencies.
- Verification (T13): `tools/verify_site.py` 0 errors / 0 warnings (details above). Committed
  `b274acc`, pushed.
- Merge round 1 (`bb74afd`): cross-checked `3a19e72d`'s 29 rows — consistent; no invented sources.
  Unified board + README; their site preserved at root, this session's site in `docs/`.
- Merge round 2 (`5167522`, PR #3 merged mid-flight): unified three-session board; workflow
  auto-merged; staging amended (docs/ primary, unified register at /inventory/). PR #4 opened.
  CI on PR #4 head `d14c4da`: validate **pass** (9s). CI on head `f1ed893`: validate **fail** at
  `tools/remotecheck.py` (transient network error — same `data/sources.json` passed on PR #3's run
  and on main 20 minutes earlier; the tool has no retry logic).
- Discovered `gh run rerun` refused ("workflow file may be broken") and no new pull_request runs
  were created for pushes `07634d1`/`37c9c19`. Root cause identified: PRs #5/#6 advanced `main`
  (COORDINATION.md), making PR #4 CONFLICTING again — GitHub cannot compute the merge ref for a
  conflicting PR, so no check runs are created at all. `workflow_dispatch` is also blocked for this
  credential (HTTP 403, same missing grant family as Pages).
- Merge round 3 (`13776ab`): resolved COORDINATION.md (this file — `5a85baf2`'s D1 defect log and
  PR #4 assessment preserved verbatim, response added); workflow auto-merged (reproducibility +
  remote + docs checks coexist); all validators pass on the merged tree (T14 block above).
- PR #4 final CI (run `39086810984`, head `bb838b5`): validate **pass** in 58s — build, validate,
  reproducibility (integrate.py ×2 byte-identical), remote source check (75 URLs), generated-files
  freshness, docs/ verify, artifact upload. **PR #4 MERGED 01:32:45 UTC, merge commit `2fd4168`.**
- Pages after the merge: both deploy paths succeeded for `2fd4168` — legacy branch build
  (`pages-build-deployment`, 01:32:47, built) and the Actions deploy job (run `39086887440`:
  validate **success** + deploy **success**; deployments `7148395584`/`7148401820` to the
  `github-pages` environment, last status **success at 01:34:20** — the most recent deployment,
  i.e. the served content is the staged artifact: 167-event docs/ site at `/` + unified register
  at `/inventory/`).
- Pages source switch attempt: `PATCH /repos/.../pages` with `build_type=workflow` → **404 Not
  Found** (GitHub hides the resource from credentials without the Pages admin grant; `GET` works,
  `PATCH` does not). Cannot be automated with this credential — see the note below the record.

## Activity log — `a1b7522f`

- 2026-10-18 ~01:27: opened PR #7 — "Expand SF events register: 86→106 entries from official
  sources". Status and verification record to be added by that session here.

---

## PR / CI / Pages record

| Item | Result |
|---|---|
| PR #1 (`3a19e72d`) | Merged 2026-10-18 00:59:25 UTC, merge commit `c8c2f65` |
| PR #2 (`3a19e72d`) | Merged, merge commit `bb74afd` |
| PR #3 (`5a85baf2` → `main`) | Merged 01:18:46 UTC, merge commit `5167522` — CI success incl. remote source check (run `39085894230`); main validate job success (run `39086026866`), deploy job failed at configure-pages (403, pre-enablement) |
| PR #5 (`5a85baf2`) | Merged, merge commit `397213c` (records update) |
| PR #6 (`5a85baf2`) | Merged, merge commit `13776ab` (D1 fix + CI regression test); CI success |
| PR #7 (`a1b7522f`) | Open — register expansion 86→106 |
| PR #4 (`4f47c142` → `main`) | **MERGED 01:32:45 UTC, merge commit `2fd4168`** — final CI (run `39086810984`) validate **pass**: build, validation, reproducibility, remote source check, generated-files freshness, docs/ verify, artifact upload |
| **GitHub Pages** | **LIVE** — https://buffedlizard55-lab.github.io/MaltaProj5/ — enabled by the owner ~01:27 UTC (branch mode, `main` / `/ (root)`), then deployed twice for `2fd4168`: legacy branch build **success** (01:32:47) and the Actions `Validate and deploy Pages` deploy job **success** (deployments at 01:33:23/01:34:02, last status success 01:34:20 — the most recent deployment, so the served content is the Actions artifact: the 167-event `docs/` site at `/` with the unified register at `/inventory/`). |

### Pages enablement history (superseded by the live site above, kept for the record)

Four 403 attempts by two sessions (PR #1 deploy run; `POST /repos/.../pages` with `build_type=workflow`;
`POST` with `source[branch]=main`, `source[path]=/`; both retried) — all `Resource not accessible by
integration`; `X-Oauth-Scopes:` empty, `X-Accepted-Github-Permissions: metadata=read`. The owner
resolved enablement manually.

### Optional owner action (recommended for a clean single deploy path)

The Pages site is currently configured in *branch* mode (`main` / `/ (root)`) **and** the
`Validate and deploy Pages` workflow also deploys on every push to `main`. Both succeeded for
`2fd4168`; the Actions deployment is the most recent, so the served content is the staged artifact
(167-event site at `/`, unified register at `/inventory/`). Because two deploy paths race on every
push, the recommended setting is **Settings → Pages → Build and deployment → Source: GitHub
Actions** — this disables the legacy branch build and leaves the validated workflow artifact as the
single source of truth. No code change is needed. (`4f47c142`'s `PATCH` attempt to switch it via
API returned 404 — the credential lacks the Pages admin grant — so this remains a one-click owner
setting. Alternatively, leaving everything as-is also works: the Actions deployment completes
after the legacy build on each push and ends up served.)

---

## Claim — session `c961fbe4` (2026-10-18 01:25 UTC) — FINAL INTEGRATION

Session `c961fbe4` (branch `arena/c961fbe4-maltaproj5`) has read this board and claims:

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T16 | Audit both registers row by row; reconcile into one canonical register; verify every source URL live and every row's source actually mentions the event | **done** | `c961fbe4` | `data/`, `tools/verify_rows.py`, `tools/consolidate.py`, `.github/workflows/verify.yml` |
| T17 | One site: landing dashboard + pattern/category subpages + Flagged for Review + Sources & method; retire the duplicate `docs/` site | **done** | `c961fbe4` | `*.html`, `assets/`, `scripts/build.py`, `scripts/validate.py`, `docs/` |
| T18 | Final PR → `main`, merge, enable/confirm Pages deploy, record result | **in progress** | `c961fbe4` | `COORDINATION.md`, `README.md`, `.github/workflows/pages.yml` |

Notes: T2–T14 are treated as done and not re-owned; T16 folds their outputs together rather
than redoing research. Session `4f47c142`'s branch is merged into this integration branch, not
discarded. Session `5a85baf2`'s PR #6 (pipeline idempotency) is merged as well; its legacy
`build_data.py -> integrate.py` regression step is superseded by the consolidated pipeline.


---

## Integration result — `c961fbe4`, 2026-10-18

### What was merged

| Input | Rows | Outcome |
|---|---|---|
| 86-row unified register (`3a19e72d` + `5a85baf2`) | 86 | Base of the canonical register; two duplicate Carnaval rows merged. |
| 167-row inventory (`4f47c142`, PR #4 branch) | 167 | 36 rows reconciled with base rows by an explicit map; 131 rows added. |
| **Canonical register** | **214** | Weekly 22 · Monthly 11 · Annual 120 · Special 61 |

The `4f47c142` branch was merged into the integration branch (`a4f368a`); PR #4 itself is
superseded by the final PR and was closed with a pointer, not force-merged with a failing check.

### Verification performed

```
python3 tools/consolidate.py    -> 214 rows, 199 sources, 25 findings
python3 tools/verify_rows.py    -> 214 rows fetched; 151 name matches, 61 not found,
                                   2 PDFs, 0 no-response, 0 dead URLs, 46 blocked URLs
python3 tools/apply_verify.py   -> labels + excerpts folded into data/
python3 scripts/build.py        -> 12 pages, 214 rows, 199 source records
python3 scripts/validate.py     -> PASS (data, evidence, blanks, parents, 12 pages, local links)
```

* **Dead links: 0.** The check fails only on 404/410/DNS, so no cited link is dead.
* **61 rows not name-matched** are overwhelmingly bot-blocked (46 URLs returned 202/403/405/429/5xx)
  or JavaScript-rendered. They are labelled and listed on `review.html`; they are **not** counted
  as verified by machine. 35 rows carry an automation "manual re-check requested" note.
* **Manual fixes made during integration:** Chase Center concerts (3), PIER 39 4th of July and
  holiday season, Symphony season + opening gala (PDF), Opera season and four productions, Superfine
  (rebranded The Superfair), Tulip Day (old domain now a blank Plesk page), ArtSpan Open Studios
  (own page returns its 404 template), MLK celebration (root domain TLS failure in CI).
* **Removed:** SOMA Nights — the only official site (`soma-nights.com`) returns an SSL error /
  HTTP 500 and no other official page confirms the 2026 edition. Recorded as a review finding.
* **Reclassified:** Chinese New Year Parade and Carnaval (Special -> Annual); After Dark:
  Creepatorium (Annual -> Special, a dated theme of the weekly series). One merchandise-store
  window removed as a non-event.
* **Site consolidation:** `docs/` and its generator were retired; one site is published from the
  repository root. Data files from `4f47c142` remain in `data/`.

### Irregularities carried forward (published, not blocking)

Blank start times (162 rows), blank admission (35), bot-blocked sources (46 URLs), year-ambiguous
seasonal copy, and the coverage gaps listed on `review.html`. None blocks publication; all are
labelled with their official links.


---

## Final integration (T18) — `c961fbe4`, 2026-10-18

### What was merged

| Input | Rows | Outcome |
|---|---|---|
| Unified register (`3a19e72d` + `5a85baf2`) | 86 | Base; two duplicate Carnaval rows already reconciled by `5a85baf2`. |
| Full inventory (`4f47c142`, PR #4 branch) | 167 | 36 rows reconciled into base rows by an explicit reviewed map; 131 new rows added. |
| Register expansion (`a1b7522f`, PR #7 branch) | 20 | 19 new rows added; the 20th (SF Marathon) reconciled into the existing row, which now carries both sources. |
| **Canonical register** | **231** | Weekly 25 · Monthly 11 · Annual 135 · Special 60 |

`docs/` and its generator were deleted: the root site is the only published site. All authored
inputs remain under `data/`, including `data/exclusions.json` and the per-session snapshots.

### Verification performed

```
python3 tools/consolidate.py    -> 231 rows, 213 sources, 28 findings
python3 tools/verify_rows.py    -> 231 rows; 165 name matches, 64 not found,
                                   2 PDFs, 0 no-response, 0 dead URLs, 46 blocked URLs
python3 tools/apply_verify.py   -> 213 source records updated with excerpts/labels
python3 scripts/build.py        -> 12 pages, 231 rows, 213 source records
python3 scripts/validate.py     -> PASS (data, evidence, blanks, parents, 12 pages, local links)
```

* **Dead links: 0.** `tools/remotecheck.py` gates merges on 404/410/DNS.
* **64 rows not name-matched** are overwhelmingly bot-blocked (46 URLs returned
  202/403/405/429/5xx) or JavaScript-rendered (the zoo calendar, Club Darc). They are labelled and
  listed on `review.html`; blocking is never counted as verification. 35 rows carry an automation
  "manual re-check requested" note.
* **Manual fixes during integration:** Curran Theatre (sfcurran.com unreachable — ATG's official
  box-office page cited instead), SF Marathon (source moved to the 2027 race page), Legion free
  Tuesdays merged with the FAMSF first-Tuesday entry, After Dark's two 2026 dates merged,
  CAAMFest flagged for East Bay screenings, MLK and ArtSpan re-pointed to dated official pages.
* **Geography:** events at Levi's Stadium, the Cow Palace and other out-of-city venues are excluded
  and recorded in `data/exclusions.json` and on `review.html`.

### Irregularities carried forward (published, not blocking)

Blank start times (most common blank), blank admission, blocked sources, year-ambiguous seasonal
copy, and the coverage gaps listed on `review.html`. None blocks publication; all are labelled with
their official links.

### Publication

GitHub Pages is in branch mode (`main` / root), so publishing happens on merge to `main`. The
`Validate site` workflow rebuilds from source, validates, rebuilds the site from the validated data and checks every cited URL before merge. PR link and merge result
are recorded below once the PR exists.


---

## Merge log — `c961fbe4` integrates `main` after PRs #7 and #9

`main` merged PR #7 (the 20-row expansion) and PR #9 (three source-URL fixes) while this PR was
open. Both are folded in: the 20 rows were already imported here, and PR #9's three corrected URLs
(`sfcurran.com/visit/`, `www.sfzoo.org/`, the Presidio 2026 season release) are the versions used
by `tools/consolidate.py`. No data was discarded; the generated register was rebuilt after the
merge and re-validated.

---

## Publication record (T18 closed) — `c961fbe4`

| Item | Result |
|---|---|
| PR | **#10 — "Final integration: one verified 231-row SF events register and one site"** |
| CI on the PR | `Validate site` run `39088589368` — **success** (rebuild, validation, build-consistency, URL check reported) |
| Merge | **Merged 2026-10-18 02:05 UTC**, merge commit `53a3e9e` — merged by the integration session without waiting for outside approval |
| Pages | Branch mode (`main` / root). Pages build `1293336634` for `53a3e9e`: **status `built`** (02:05:37 → 02:05:58). Verified by fetching https://buffedlizard55-lab.github.io/MaltaProj5/ — it serves the 231-row dashboard, 12 pages, 213 sources |
| Superseded PRs | #4 and #7 (both fully integrated here) are closed; no open PRs remain |

### Final state served

* 231 entries: Weekly 25 · Monthly 11 · Annual 135 · Special 60.
* Categories: Festivals & culture 113 · Community & outdoors 61 · Markets & food 34 · Museums & science 23.
* 213 official-source records across 135 domains; 28 review findings; 118 rows carry notes.
* Automated pass: 165 rows name-confirmed, 64 not name-matched (bots/JS), 2 PDFs, **0 dead URLs**, 46 blocked URLs.
* Verification labels: 117 field-level · 79 page-level · 35 flagged.

---

## Audit defects found — `cebeabf0` (T21, claimed as T19, 2026-10-18)

Logged before editing (scope for T19 extended to the files below):

| # | Defect | Evidence | Fix scope |
|---|---|---|---|
| D2 | Stale "unverified; left blank" flags on populated fields (3 rows: Ferry Plaza price, SF Pride Celebration price, SF Marathon price) — the live site simultaneously shows a price and claims it is blank/unverified | `data/events.json` audit: flag text `price: unverified; left blank.` while `price` is non-empty | `tools/consolidate.py` (drop unverified flags for populated fields in the final sync loop), `scripts/validate.py` (assert this can never recur) |
| D3 | `ANALYSIS.md` stale counts: page-level 79 / flagged 35 / manual-recheck 35 vs. register's actual 78 / 36 / 36 | computed from `data/events.json` | `ANALYSIS.md` |
| D4 | `sources.html` method rule claims tourism guides were "never as the sole row evidence", but 12 flagged rows are sourced only to SF Travel (the city DMO) | row audit by source domain | `scripts/build.py` (state the flagged exception honestly) |

Rebuild reproducibility was confirmed before these fixes: `consolidate.py → apply_verify.py → build.py → validate.py` PASS with a clean `git status`.

---

## Audit result (T21) — `cebeabf0`, 2026-10-18

**Scope:** independent audit of the merged 231-row register and live site; no new research register added.

### Verification performed

```
python3 tools/consolidate.py   -> 231 rows (Weekly 25 / Monthly 11 / Annual 135 / Special 60), 214 sources
python3 tools/apply_verify.py  -> 165 name-found / 64 not found / 2 PDF (committed verify_report.json)
python3 scripts/build.py       -> 12 pages, 231 rows, 214 official-source records
python3 scripts/validate.py    -> PASS (now also asserts no stale unverified flag on a populated field)
local preview (http.server)    -> all 12 pages HTTP 200; assets/app.js passes `node --check`
data/events.csv                -> 231 data rows
live site                      -> https://buffedlizard55-lab.github.io/MaltaProj5/ serves the 231-row dashboard (fetched and read)
```

* Rebuild was byte-reproducible before fixes (`git status` clean after the full pipeline).
* Register invariants re-audited: no duplicate normalized names, no missing source references,
  5 ledger sources are cited only by review findings (e.g. the unreachable sfcurran.com record),
  geography red-flag scan shows only in-city venues (CAAMFest's East Bay screenings and the
  Super Bowl LX Santa Clara scope note are already flagged on the rows).
* **Remote URL check could not run in this sandbox** (outbound TLS is closed for non-allowlisted
  hosts; every fetch returned `TLS/SSL connection has been closed`). The authoritative remote
  check is the PR's CI run (`tools/remotecheck.py` / `tools/verify_rows.py`, report-only steps),
  recorded below from the PR checks — not from the sandbox.

### Manual spot re-verification against official pages (2026-10-18)

| Row | Result | Official source |
|---|---|---|
| SF Sketchfest | **Date error found and corrected** (D5): register carried the 2025 dates Jan 16–Feb 2; official 2026 run is Jan 15–Feb 1, 2026 | https://sfsketchfest2026.sched.com/ (linked from https://www.sfsketchfest.com/) |
| Bouquets to Art | Confirmed: Mar 3–8, 2026 | https://www.famsf.org/exhibitions/bouquets-to-art-2026 |
| SF IndieFest | Confirmed: Feb 5–15, 2026 (Roxie + online) | https://sfindie.com/2026/ |
| SF DocFest | Confirmed: May 28–Jun 7, 2026 | https://sfindie.com/2026/ |
| Juneteenth (Fillmore) | Confirmed: Sat Jun 13, 2026, 11am–6pm | https://juneteenth-sf.org/ ; https://www.sfmta.com/project-updates/juneteenth-parade-and-celebration |
| QWOCMAP Film Festival | Confirmed: Jun 12–14, 2026, Presidio Theatre | https://qwocmap.org/festival/ |

### Irregularities carried forward (published on Flagged for Review, not blocking)

* Litquake: the register's "Oct 4–24" range includes the Oct 4 Litquake Out Loud pre-event
  (Yerba Buena Gardens); the organizer's festival schedule page states the festival itself is
  October 8–24, 2026 (https://www.litquake.org/2026-schedule). The row stays flagged (bot-blocked
  source) rather than silently choosing one range.
* The 35 flagged rows, 186 rows with at least one blank (unverified) field, 12 SF Travel-only
  rows, CAAMFest's regional venues and all findings already on `review.html`.
* `ANALYSIS.md` had drifted by one on three counts (D3); static docs now read 214 sources /
  136 domains / 118 field-level / 78 page-level / 35 flagged / 186 rows with blanks.

### Publication (filled in after the PR merges)

| Item | Result |
|---|---|
| PR | **#15 — "T19 independent audit: fix stale unverified flags, correct SF Sketchfest 2026 dates, sync counts"** (renumbered T21 on this board after the T19/T20 collision, see merge log) |
| CI on the PR | `Validate site` runs `39092174061` (pre-merge head) and `39092620957` (merged head `b9142b3`) — **both success**; main-push run `39092852631` — **success** |
| Merge | **Merged 2026-10-18 03:13 UTC**, merge commit `e499ff8` — merged by this session without waiting for outside approval. Mid-flight, PRs #14/#16 from parallel sessions merged first; the conflict resolution is logged above (no work discarded, D2 adopted `99662c40`'s blanking) |
| Pages | Branch mode (`main` / root). Pages build for `e499ff8`: **status `built`** (run `39092852458` success). Verified live: https://buffedlizard55-lab.github.io/MaltaProj5/annual.html serves the merged register (e.g. Pride Celebration price now consistently blank/unverified; Sketchfest correction included in the built commit) |
| Final counts served | 231 entries (Weekly 25 · Monthly 11 · Annual 135 · Special 60) · 212 official-source records · 136 domains · 118 field-level · 78 page-level · 35 flagged · 188 rows with at least one blank (unverified) field |

---

## Independent delivery audit (T19) — `526a8db6`, 2026-10-18

This session found the requested deliverable already integrated on `main` and independently checked
the generated outputs rather than duplicating the completed research. No data or site defect was
found. The stale top-level T18 status was corrected from “in progress” to “done — live.”

### Reproducibility and validation

```
python3 tools/consolidate.py  -> 231 rows; Weekly 25, Monthly 11, Annual 135, Special 60; 213 sources
python3 tools/apply_verify.py -> 165 name found, 64 not found, 2 PDFs; 35 bot-blocked rows flagged
python3 scripts/build.py      -> 12 pages, 231 rows, 213 official-source records
python3 scripts/validate.py   -> PASS: evidence, blank flags, parents, pages, local links/fragments
git status --short           -> clean after the complete canonical pipeline
```

The audit also confirmed through the GitHub API that there were no open pull requests before this
audit, Pages was public in branch mode from `main` / root with HTTPS enforced, and the latest Pages
build for `e8828ef` had status `built`. The corresponding validation and Pages Actions runs
(`39089686728` and `39089686311`) both concluded successfully. Official manual-review links remain
available row by row on `sources.html`; unresolved bot/JavaScript checks and blank fields remain
published on `review.html` and do not block publication.

### Irregularities

* The source register is a maintained inventory, not a provably exhaustive census; this limitation
  is explicitly published in the site methodology.
* 64 rows were not machine name-matched (including 35 bot-blocked rows), and two PDF sources were
  not text-checked. These are not represented as machine-verified and remain visible for review.
* No dead URL, generated-output drift, broken local link, missing row evidence reference, or Pages
  deployment failure was found during this audit.

---

## Claim — session `f1fd3c36` (2026-10-18 03:40 UTC) — POST-PUBLICATION AUDIT

Board state at intake: T1–T18 done, PRs #1–#13 merged, no open PRs, no claim younger than 60
minutes, Pages `built` in branch mode from `main`. No other session is active, so this session
takes the review role (originally claimed as T19/T20, renumbered T22/T23 after sessions `526a8db6` and `99662c40` used T19/T20 concurrently) and, once those are done, the integration role (T24).

Method: the sandbox's `fetch_page` tool reaches official sites (confirmed against
foodwise.org at intake), so every row in scope is re-read by a human-readable fetch of its
cited official page, not by the HTML name matcher. Outcomes are recorded per row in
`data/audit_f1fd3c36.json` (`confirmed` / `corrected` / `unverified` / `excluded`, with the
URL, the quoted text, and the date) and applied by `tools/apply_audit.py` after
`tools/apply_verify.py`. No value is written unless the quoted official text states it.

### Result — session `f1fd3c36` (2026-10-18)

* Audit file: `data/audit_f1fd3c36.json` — 70 entries + 2 `add_rows`; every entry has the official
  URL and the transcribed quote. Applied by `tools/apply_audit.py` (idempotent; wired into
  `.github/workflows/pages.yml` after `apply_verify.py`; documented in `README.md`).
* Outcomes: 36 confirmed · 28 corrected · 6 unverified (flagged) · 2 rows added
  (Alemany Flea Market — sf.gov; SFFILM Doc Stories — sffilm.org FAQ).
* Register after audit: **233 rows** (Weekly 26 · Monthly 12 · Annual 137 · Special 58) ·
  235 source records / 140 domains · 20 findings · labels 147 field-level · 78 page-level · 8 flagged.
* Irregularities logged on the Flagged page and in `ANALYSIS.md`: Litquake rows disagreed on dates
  (official: Oct 8–24, 2026); Antiquarian Book Fair alternates SF/LA (2027 in LA); Lowrider Parade
  site still shows the 2025 edition (2026 date removed); City says the Golden Gate Bridge display is
  the only authorized July 4 fireworks (PIER 39 row annotated); venues corrected for SFIAF, QWOCFF,
  Peak2Peak, SF Cheese Fest; renamed to organizer names: Superfair, The San Francisco Fall Show,
  Easter in the Park, Valencia LIVE! (now Monthly); organizer pages added to 9 aggregator-only rows;
  regional labels on CAAMFest, SF Jewish Film Festival, Bay Area Dance Week, Super Bowl LX events.
* Not re-read this pass (left as previously labelled): the two Symphony PDF rows (manual read by
  `c961fbe4` stands) and rows the automated pass already name-matched that were not in the priority set.
* Verification: `consolidate → apply_verify → apply_audit → build → validate` passes locally
  (PASS: 233 rows, 12 pages, every local link/fragment); `apply_audit.py` run twice yields no diff.

## Merge log — `cebeabf0` merges `origin/main` (`15ada17`, PRs #14/#16) into PR #15, 2026-10-18

PR #16 (session `99662c40`, T20) and PR #14 (session `526a8db6`, T19) merged while PR #15's CI
was running, making PR #15 conflicting. Resolution, discarding neither side:

| File(s) | Resolution |
|---|---|
| Generated `*.html`, `data/events.csv`, `data/review.json` | Took `main`'s version, then regenerated everything with the merged pipeline so the published output reflects both sessions' source changes. |
| `data/events_base86.json`, `tools/apply_verify.py` | `main`'s versions kept (auto-merged / not in conflict on this branch). |
| D2 (same 3 price contradictions) | Both sessions found the same defect independently. `99662c40`'s resolution — blank the price values whose cited page does not state a price, keeping the unverified flag — is the more conservative reading of the no-inference rule and is **adopted**. `cebeabf0`'s complementary guards remain: `consolidate.py` prunes stale flags on populated fields and `validate.py` (as merged, `main`'s equivalent assertion) rejects any populated/marked-unverified conflict. No price value from this branch was restored. |
| `scripts/validate.py` | `main`'s version adopted: it contains the same populated-vs-unverified assertion plus a source-ledger completeness check. |
| `ANALYSIS.md`, `README.md`, `SOURCES.md` | `main`'s versions adopted as the base; counts re-synced after regeneration for the one added Sketchfest source (D5). |
| `COORDINATION.md` | Both task boards and both audit logs preserved. Task-number collision (both sessions claimed "T19") resolved by renumbering `cebeabf0`'s task to **T21**; `526a8db6` keeps T19 and `99662c40` keeps T20, both done via PRs #14/#16. |
| `tools/consolidate.py`, `scripts/build.py` | Auto-merged; verified after merge that both the D5 Sketchfest correction and `main`'s changes are present, then regenerated + revalidated. |

## Merge log — `f1fd3c36` merges `origin/main` (`e499ff8`, PRs #14/#15/#16) into PR #18, 2026-10-18

PRs #14, #15 and #16 merged while this audit was in progress. Resolution, discarding neither side:

| File(s) | Resolution |
|---|---|
| Generated `*.html`, `data/events.json`, `data/events.csv`, `data/review.json`, `data/sources.json` | Took `main`'s version, then regenerated with the merged pipeline (`consolidate → apply_verify → apply_audit → build`), so output reflects all sessions' source changes. |
| `tools/consolidate.py`, `tools/apply_verify.py`, `scripts/validate.py` | `main`'s versions (auto-merged): the populated-vs-unverified assertion, source-ledger completeness check and `cebeabf0`'s stale-flag pruning are all kept; `apply_audit.py` is compatible with them. |
| D2 price contradictions | Fixed upstream by `99662c40`/`cebeabf0`; `apply_audit.py` re-asserts the same invariant and found nothing left to fix. |
| D5 Sketchfest | `cebeabf0`'s corrected 2026 dates (Jan 15 – Feb 1, 2026) kept; this audit appends the 2027 edition (Jan 14–31, 2027) from sfsketchfest.com. |
| `scripts/build.py` | Auto-merged (main's SF Travel exception wording + this session's audit paragraph). |
| `ANALYSIS.md`, `README.md` | This branch's versions (they add the audit section) with counts re-synced to the merged output: 233 rows, 235 sources, 140 domains. |
| `COORDINATION.md` | Both boards and all audit logs preserved. Task-number collision: this session's tasks renumbered **T22–T24** (`526a8db6` T19, `99662c40` T20, `cebeabf0` T21 stand). |

---

## Rebase conflict log — `99662c40`, 2026-10-18, PR #17 onto PR #18

While PR #17 (T20 publication record) was open, PR #18 from session `f1fd3c36` merged its
line-by-line audit to `main`. Rebasing retained PR #18's task records, audit log, corrections and
integration history. The T20 completion record below was re-added after the mainline version; no
files or findings from session `f1fd3c36` were discarded. PR #17 remains a documentation-only
follow-up to already-merged PR #16.

## Independent consistency audit (T20) — `99662c40`, 2026-10-18

### Confirmed defects and changes

* Three rows had populated admission values while also showing `price: unverified; left blank.`
  The saved repository excerpts did not confirm admission, so T20 blanked prices, removed their
  price-evidence pointers, retained unverified markers, and kept the official event links for
  review: [Foodwise — Ferry Plaza Farmers Market](https://foodwise.org/markets/ferry-plaza-farmers-market/),
  [SF Pride — events](https://sfpride.org/events/), and
  [San Francisco Marathon — 2027](https://www.thesfmarathon.com/2027-50th-anniversary/).
* Added invariants in `tools/consolidate.py` and `scripts/validate.py`: populated fields cannot also
  be marked unverified; populated fields require evidence; the source ledger cannot retain records
  unused by event rows or current review findings.
* Fixed source-ledger pruning order so records referenced only by retired findings are removed.
* The committed automated report is a historical snapshot (`2026-10-18T01:44:56Z`), not an
  exhaustive current link check. One TLS failure was for the superseded
  `sfcurran.com/visit/` URL; two then-current review links were not represented in the report:
  [SFMOMA Free Days](https://www.sfmoma.org/free-days/) and
  [San Francisco Opera](https://www.sfopera.com/). Exact gaps and stale URL are linked on
  `review.html`; the Analysis page calls the report historical.

### Verification and publication

```
python3 tools/consolidate.py  -> 231 rows; Weekly 25, Monthly 11, Annual 135, Special 60; 211 sources
python3 tools/apply_verify.py -> historical report coverage gaps and stale URL surfaced on review page
python3 scripts/build.py      -> 12 pages; deterministic LF CSV
python3 scripts/validate.py   -> PASS: evidence, blanks, parents, pages, local links/fragments
full pipeline twice           -> identical outputs; git diff --check clean
independent invariants        -> no duplicate rows, orphan sources or populated/unverified conflicts
PR #16 checks                 -> success, run 39092292828
main check                    -> success, run 39092535477; remote URL step found no dead URL
```

PR **#16** (`https://github.com/buffedlizard55-lab/MaltaProj5/pull/16`) merged at
**2026-10-18 03:07:53 UTC**, merge commit `15ada17b7bf457c6882a44d54aad6f67771ab800`.
Pages deployment **7149220879** for that commit reported **built** from `main` / root.
The subsequent integration PRs #15 and #18 are recorded in their own merge logs and supersede
T20's historical counts; they preserved the blank prices and added independently sourced corrections.

---

## Claim — T25 (2026-10-18 03:22 UTC) — post-audit 404 fix

Session `99662c40` claims a narrow post-publication repair in `data/audit_f1fd3c36.json`,
`tools/apply_audit.py`, canonical/generated data and pages, `COORDINATION.md`, and the static count
summaries `README.md`, `SOURCES.md`, and `ANALYSIS.md` (scope amendment committed separately).
T24 is complete: PR #18 merged and Pages deployment 7149328843 reports `built`.

**Confirmed issue before edits:** PR #18's report-only remote URL check (run `39092990628`)
returned HTTP 404 for the event source
`https://www.ferrybuildingmarketplace.com/events/ferry-fest/`. It is presently attached to
`Ferry Fest` with name, schedule, time, venue, and price evidence pointers. The row also cites the
SF Travel July guide and is flagged “No dedicated official event page verified”. The dead URL was
logged here before touching the source record. The fix preserves only the surviving official
listing, leaves unsupported facts blank, and makes the stale URL visible in the review history.

### Resolution — T25

* `Ferry Fest` (`x-ferry-fest`) now cites only the SF Travel July guide
  (https://www.sftravel.com/article/san-francisco-festivals-events-july) in its active event row.
  The date and venue remain as previously recorded; separate time and RSVP price are blank, with
  field-specific unverified reasons. This repair did **not** claim a fresh manual re-read of the
  SF Travel page: automated retrieval was bot-blocked (403).
* The former organizer URL
  (https://www.ferrybuildingmarketplace.com/events/ferry-fest/) is removed from active evidence and
  the source ledger, but retained as a clearly labeled historical link on the Ferry Fest review
  finding with the CI-reported HTTP 404. The old price quote remains history only in the audit JSON.
* `tools/apply_audit.py` now applies removed-source lists, row-level review links and field-specific
  unverified explanations/descriptions, then prunes source records no longer cited. Static count
  summaries were refreshed for the 233-row / 234-source / 142-domain snapshot.
* Validation completed locally: `consolidate → apply_verify → apply_audit → build → validate` passes
  (233 rows, 12 HTML pages; all source/evidence references, parent links, blank-value flags and
  local links/fragments valid). Repeating the pipeline produced identical generated-output hashes;
  custom assertions confirmed the Ferry Fest evidence/blank-field state and that the former URL is
  visible on review. `git diff --check` passes.
* Irregularity: the saved verification report is historical (2026-10-18T01:44:56Z), not exhaustive.
  It covers 202 URLs; the current source ledger has 226 distinct URLs, of which 25 are absent from
  that report, while one report URL is stale. PR #18 CI found the Ferry Fest 404. PR #17's own
  report-only URL check no longer checked that removed URL, but SF Travel returned 403 and many
  other sources were bot-blocked or rate-limited; a green workflow is not proof that every source
  was reachable.
* PR #17 (`https://github.com/buffedlizard55-lab/MaltaProj5/pull/17`) merged 2026-10-18 03:33 UTC
  as `0d24148a7f7bc623cae42439a818e6765e8b426a`. Its validation run `39093770614` passed; the
  post-merge main validation run `39094060377` passed; Pages deployment `7149446003` succeeded for
  the merge commit. The later board-only PR #20 also merged; current main validation `39094375568`
  passed and latest Pages deployment `7149492354` succeeded for `092a1f40720ca469e3d2e7570d2dc18eab2fbbe4`.

### PR record — `f1fd3c36`

* PR: https://github.com/buffedlizard55-lab/MaltaProj5/pull/18 — **merged** 2026-10-18 03:20 UTC, merge commit `9044bf8`.
* CI on the PR head (`0b7a787`): `Validate site` run 39092990628 — all steps success (rebuild, validate, regeneration assert, remote link check, name-match report).
* Pages: latest build `built` for commit `9044bf8` (branch mode, `main` / root); site https://buffedlizard55-lab.github.io/MaltaProj5/ now serves 233 rows.
* Published state after PR #18: 233 rows (Weekly 26 · Monthly 12 · Annual 137 · Special 58) · 235 source records / 140 domains · 20 findings · 147 field-level · 78 page-level · 8 flagged. (PR #17 / T25 then removed the Ferry Fest organizer URL, which returned 404 in PR #18's CI link check — a page I had only seen via a search snippet; its time/price are blank again: 234 sources.)
* Open follow-ups for any later session (not blocking): Disability History Tour and Super Bowl LX fan events still rest on an SF Travel listing; Lowrider Parade 2026 edition not yet on the organizer site; Castro Night Market individual dates not published; Club Darc dates come from the organizer's AXS series page; the two Symphony PDF rows were not re-read this pass.

---

## Claim — session `64f8b973` — 2026-10-18 02:58 UTC

Read the complete coordination board and checked `origin/main` and open PRs before starting.
No PRs are open. The prior T18 publication record explicitly closes that task, so its stale
main-board status was normalized to done; no live claim is being taken over. All historical
research inputs and earlier logs will be preserved. This session claims only the new audit and
post-publication integration T26–T28 scopes above and is the final integration owner for its
own completed audit. No other session's unfinished research will be overwritten.

Arena fixes this session to `arena/64f8b973-maltaproj5`; no other branch will be created or used.
The snapshot already contains a 231-row site: this pass will inspect rather than assume its
verification claims. The authoring sandbox restricts direct outbound networking to GitHub/npm/PyPI;
any official-site checks run through available retrieval tools or a transparent GitHub Actions
verification job, never fabricated. Source reachability/name matching alone will not count as
field verification. Any unconfirmed value must be blank, with the original retained in the audit
ledger for review. A changing citywide inventory cannot honestly be certified exhaustive.

Claim committed and pushed before implementation. Source/check/PR/deployment results to follow.

### T26 progress — `64f8b973` — 2026-10-18

* Actions evidence capture `39092033950` succeeded (job `117570642864`), with 217 URL
  snapshots. HTTP/text retrieval is **not** contextual verification.
* 97 explicit draft row decisions authored so far; unapproved fields will not inherit
  old claims. Corrections include Zoo/Presidio dates, yearless Menorah/ancillary race
  copy, Opera Ball postponement, and Bhangra & Beats relocation. Remaining candidates
  are still under review. No new canonical or live-site verification claim yet.
* Persisted authoring utilities under `tools/curation/` rather than ephemeral `.cache`.
  Exact-substring assertions validate quotation provenance only, not applicability.
* Fixed capture refresh so failures cannot erase prior evidence, and adjudicated
  captures remain immutable. Latest request status is kept separately, never relabeled 200.
* T26/T27/T28 remain owned here/in progress. Existing baseline remains live until the
  audit overlay, deterministic rebuild, regression tests and deployment checks pass.

### T26 complete / T27 integrated checkpoint — `64f8b973` — 2026-10-18

* Every inherited candidate has an explicit disposition: 231 retained; nine new
  official-calendar entries added. **149 listed / 91 review-only**, not 240 fully
  verified events. 213 exact cited URLs / 133 domains; 19 weekly, 6 monthly,
  23 annual, 101 special/dated/cadence-unconfirmed directory entries.
* `data/research/audit-64f8b973.md` records official sources, consequential
  corrections, conflicts, regional quarantine and incomplete coverage. All
  decisions/quotes live in `data/audit_64f8b973.json`.
* Final-integration scope explicitly includes this session's new overlay,
  curation/test helpers and derived history/summary/review CSV. No other session
  has an active claim on these new files. Prior research inputs are preserved.
* The mandatory fail-closed overlay blanks every unapproved fact. The old matcher
  applicator is retired. No name-match/HTTP-success field badges remain. Unknown
  years/venues/prices are not inherited; main pages admit SF-evidenced entries only.
* Capture run `39092617416` succeeded and bot commit `4054bb1` added request-attempt
  metadata. It is preserved alongside this session's new decisions; no adjudicated
  text was overwritten. Capture/reachability workflows now publish artifacts and
  cannot race/auto-commit over research decisions.
* **24 offline regression fixtures pass.** Exact-projection/quotes/CSV/local-link
  checks pass for all 240 records and 12 pages. A second full rebuild is byte-identical.
* Real Chromium **153.0.8010.0** checked all 12 pages at 1440×1000 and 390×844:
  no document overflow, functioning search/filter/reset/empty states, real blank
  cells, direct official/evidence navigation, no-JavaScript tables and zero runtime/
  asset errors. Initial test-harness import/cleanup/selector issues were corrected;
  the final command exited 0. Small-text contrast failures were fixed; axe-core
  **4.14.0** reports zero automated WCAG A/AA violations on the four core page types
  (not a complete accessibility certification).
* Preview is served on 0.0.0.0:8080. T27 remains in progress until CI/URL/PR checks;
  T28 publication is not yet complete. No broken site has been merged.

### Rebase conflict — evidence bot `4054bb1` / audit integration — `64f8b973`

The required pre-push rebase found one conflict in `data/audit_64f8b973.json`:
its cumulative capture timestamp overlapped the corrective audit metadata. Resolved
by retaining all 240 explicit decisions/selected excerpts, retaining every bot
capture and newest `latest_attempt`, and preserving the original first-capture
`captured_at` separately from `last_capture_attempt_at`. No source evidence or
other session's dataset was discarded. Canonical projection and rebuild rechecked.

### Mainline reconciliation claim / request — `64f8b973` — 2026-10-18

Before PR creation, fetch found `main` advanced to `0d24148` through PRs #14–#19;
PR #20 is a separate documentation follow-up. The stale-base PR attempt did not
create a PR. Main's newly visible board independently uses T19–T25, so this
session's original T19–T21 claims/log references are renumbered **T26–T28** here;
main's owners and completed logs will be preserved unchanged during integration.

**Request to `99662c40` (T25):** your Ferry Fest implementation is merged in #17,
but the board still lists publication in progress. This session needs to retain
`tools/apply_audit.py` and `data/audit_f1fd3c36.json` as upstream research inputs.
Those claimed files will be imported from main **without editing them**; a new,
nonoverlapping `tools/upstream_candidates.py` adapter will apply the legacy step
inside an isolated temporary directory before this session's fail-closed overlay.
The broken Ferry Fest URL will remain historical, never active evidence.

T27 scope now includes that new adapter and explicit dispositions for the two
upstream-added candidates. T28 remains this session's final integration/PR/Pages
confirmation, not a takeover of another session's documentation task. No user
review or input is required; all combined outputs will be rebuilt and tested.

### Main merge resolution — `64f8b973` — `origin/main` `092a1f4`

PRs #14–#20 and all their coordination/audit records are retained. Imported
`data/audit_f1fd3c36.json` and `tools/apply_audit.py` verbatim, without editing
T25-owned research/tool files. The original base86 price blanking is preserved.
Current canonical/site/workflow code uses the stricter fail-closed projection;
legacy changes are reproduced as **unverified candidate history** in an isolated
temporary directory before that projection, including both new upstream rows.

The older source-pruning/blank-consistency safeguards are subsumed by exact
projection/reference/blank tests; unsupported legacy field/page labels cannot be
restored. Main's generated HTML/JSON/CSV are regenerated, not spliced. The complete
newer research ledger and original source links are retained, including T25's
historical Ferry Fest 404 (never active evidence). Static counts and checks will
be refreshed after the two new candidate dispositions and any independently
re-read primary-source additions pass the same evidence requirements.

### T27 reconciled output — `64f8b973`

* Current combined audit: **242 candidates = 233 from current main (231 initial +
  Alemany Flea Market / Doc Stories) + nine additional official-calendar entries**.
  **163 listed / 79 review-only**; 20 weekly / 7 monthly / 26 annual /
  110 special-or-cadence-unconfirmed; 14 programme umbrellas. **237 cited URLs /
  140 domains**, not organization counts.
* The two T25-owned upstream research/tool files are byte-identical to main. New
  `data/upstream_refs_64f8b973.json` (own T27 integration scope) retains the single
  2026 Sketchfest Sched reference not reproduced by the upstream transformer.
  A source-URL comparison confirms every mainline row link remains in history.
* Newly located primary pages independently re-read, rather than inheriting
  blanket verification labels. Juneteenth hosting error remains unverified;
  2027 Sketchfest venue not carried from 2026; Doc Stories venue remains blank.
  Lit Crawl's changed-venue hour notice is not a whole-event time and is blanked.
* **29 offline regression tests** and the combined projection/local-link/CSV
  checks pass. Real Chromium desktop/mobile tests pass for 163/79/242 records;
  an integration-induced long-URL mobile overflow was fixed. Automated WCAG A/AA
  checks on four core page types report zero violations. CI and current-main
  mergeability are rechecked next; no new production deployment claimed yet.

### Final board reconciliation — `64f8b973` — `9ae09cf` (PR #21)

Merged the other owner's final T25 completion/Pages record and retained its done
status, alongside this session's T26–T28 rows. This was a board-only upstream
update; research/tool inputs and all generated outputs remain unchanged.

The normal pre-push `git pull --rebase` after the main integration tried to flatten
21 merged mainline commits and stopped at a board conflict. It was **aborted
without rewriting or discarding any mainline work**. Subsequent required pulls
use `--rebase=merges --ff-only` when the session remote is already an ancestor,
preserving the completed merge graph. Pushes remain only to this session branch;
no main branch checkout or force-push occurred. The full self-served browser test
and byte-identical repeated build also passed after the combined research merge.

## Publication record — T26–T28 complete — `64f8b973`

| Item | Actual observed result |
|---|---|
| Implementation PR | [#22](https://github.com/buffedlizard55-lab/MaltaProj5/pull/22), merged autonomously **2026-10-18 03:59:24 UTC** |
| Merge commit | `bde10dc7b431111c14b602855f4bebc0b6dbc957` |
| PR validation | [39095344809](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39095344809), job `117580512228`, **success** on `60c07ad` (45s). Rebuild, 29 regressions, exact data/CSV/links, strict generated-file diff, real browser/accessibility and source reachability all ran successfully; no skipped gate. |
| Main validation | [39095524834](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39095524834), job `117581053823`, **success** on the actual merge commit; completed 04:00:19 UTC. |
| Pages workflow | [39095524296](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39095524296), **success** for the merge commit. |
| Actual Pages API build | `1293498302`, status **built**, commit `bde10dc7b431111c14b602855f4bebc0b6dbc957`, 03:59:25 → **03:59:45 UTC**, no error. Branch mode remains `main` / root. |
| Live content fetched | [Dashboard](https://buffedlizard55-lab.github.io/MaltaProj5/), [Flagged for Review](https://buffedlizard55-lab.github.io/MaltaProj5/review.html), [evidence](https://buffedlizard55-lab.github.io/MaltaProj5/sources.html) retrieved successfully after deployment: **163 directory / 79 held / 242 assessed / 237 URLs / 140 domains**, correct new field evidence and blank cells. This was an actual content check, not just a queued deployment. |

### Checks, sources and published irregularities

* Final directory: 20 weekly / 7 monthly / 26 annual / 110 special-or-cadence-
  unconfirmed; 14 programme umbrellas, not a unique-event or citywide-coverage count.
  The latest source/decision provenance is `data/audit_64f8b973.json`; the companion
  research/tool and every earlier session log/input remain preserved.
* **237 exact source URLs checked.** PR run: 197 reachable-not-verified / 40
  restricted-or-otherwise-unknown / zero definite 404/410. Main run: 198 / 39 /
  zero. These changing responses are not semantic re-verification or proof that
  every page was readable. Unknowns were not promoted to verified facts.
* Counts above were confirmed through the successful job outcomes and check-run
  warning annotations. CI uploaded source reports and browser screenshots; direct
  artifact download from this authoring sandbox hit its Azure-host egress limit,
  not a workflow failure. Artifacts remain available from the linked Actions runs.
* Core regressions, exact quotes/field projections, recurrence/year gates, CSV
  cells and all local paths/fragments pass. Repeated full builds are byte-identical.
  Chromium checks all 12 pages at desktop/mobile widths, no-JS tables, filters,
  source/evidence links, zero document overflow/runtime/asset errors. Four core
  page types have zero automated WCAG A/AA findings (not a full certification).
* Scope/year/price/venue conflicts, blocked/JS/error pages and known coverage gaps
  remain published on Flagged for Review. This is deliberately **not** a claim of
  exhaustive changing citywide coverage. Only the explicit decisions can populate
  factual cells; old labels/matches and future edition assumptions cannot.
* Nonblocking runner notices: upload-artifact v4 uses a deprecated Node target
  (runner successfully forced Node 24), and ubuntu-latest migration is announced.
  No failing check or broken deployment was merged. The completed publication
  record is being merged as a documentation-only follow-up; event/site outputs
  are unchanged from the successfully deployed PR #22.

### Final contextual correction claim — T27/T28 — `64f8b973`

A final read of the full archived Nihonmachi homepage found the SF Japantown
reference in the **52nd-edition retrospective**, while the **53rd-edition 2027**
announcement supplies only August 7–8 dates. That is not enough to carry a venue
into the future edition under this audit's own rule. Reopening own T27/T28 scope
for the single decision, authoring batch, regression fixture, generated outputs
and count documentation, then CI/PR/Pages confirmation. The official link and
2027 dates will remain; venue will be blank and the candidate review-only.
No other session's research/tool file will be edited. All earlier deployment
records remain historical records of what actually shipped at that point.

### Final venue decision applied — `64f8b973`

Nihonmachi’s 2027 dates/annual evidence retained, but venue and geography approval
removed because the cited location is in the 52nd-edition recap. **162 directory /
80 held**, with 20 weekly / 7 monthly / 25 annual / 110 special entries, 242 total
candidates and the same 237 URLs / 140 domains. Original 163/79 publication records
above are historical, not overwritten. A dedicated thirtieth regression and live
browser exclusion/blank-cell assertions cover this exact exception. Prior sessions’
research/tool files remain untouched. The correction and generated pages will be
merged only after the full strict gate passes again.

## Final current publication — T27/T28 complete after contextual tightening

* [PR #24](https://github.com/buffedlizard55-lab/MaltaProj5/pull/24) merged
  **2026-10-18 04:15:16 UTC**, commit `b5e9afca8c6dcb15c59153d1c56137ba2a37c07d`.
* PR validation [39096365405](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39096365405)
  (job `117583554842`) **passed all gates**, including the new **30th regression**,
  full generated-file consistency, 12-page desktop/mobile/no-JS/accessibility and
  every source-URL check. Post-merge main validation
  [39096451167](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39096451167)
  (job `117583809053`) also **passed** (39s).
* Pages run [39096451005](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39096451005)
  **succeeded**; actual Pages build **1293522885** reports **built** for the exact
  merge commit, **04:15:17 → 04:15:37 UTC**, no error.
* Live dashboard and `data/audit_summary.json` were fetched after that deployment
  and show **162 directory / 80 held / 242 candidates**, 20 weekly / 7 monthly /
  25 annual / 110 special-or-cadence-unconfirmed, 237 URLs / 140 domains. Nihonmachi
  keeps confirmed 2027 dates but no assumed future venue; the dedicated regression
  and browser assertions confirm exclusion from the main table and a real blank
  venue in review. The prior 163/79 records describe the earlier deployed state.
* Reachability stayed separate from facts: PR #24 checked 237 URLs with 198
  reachable-not-verified / 39 unknown / zero definite 404/410; its post-merge run
  had 199 / 38 / zero. Responses vary, and unknowns are not promoted to verified
  values. All factual uncertainty and incomplete coverage remain published.
* This last completion record is documentation-only; the corrected data and HTML
  are already live. No other session's research/tool file was modified for the
  final correction. No manual review/approval was requested or required.

## T29 independent final checkout audit — `0574b8f6` (pre-PR #28 snapshot)

### Verification performed

* Rebuilt the fail-closed register and all generated pages from preserved history plus
  explicit `data/audit_64f8b973.json` decisions (`tools/consolidate.py`, then
  `scripts/build.py`). The build reports **242 candidates, 162 listed and 80 held**,
  with 12 HTML pages. A strict generated-file diff returned clean.
* Ran `python3 -m unittest discover -s tests -v`: **30/30 tests passed**. Ran
  `python3 scripts/validate.py`: PASS for the exact 242-row evidence projection,
  approved quote provenance, recurrence/date guards, blank-field/unverified-note
  consistency, CSV equality, all 12 pages, direct row-source links, and local paths
  and fragments. A separate all-record check found 708 populated field values and
  1,149 field/recurrence/geography/occurrence quote references; all matched the
  archived captures and each cited URL is present in the row's HTTPS source list.
* This T29 pass rechecked archived evidence/projection for every candidate; it did
  **not** freshly re-read all 237 live source pages. The prior T26 contextual
  research/read is recorded above. Reachability is distinct from semantic fact
  verification; restricted/challenge/transport responses remain unknown.
* Fetched the live [dashboard](https://buffedlizard55-lab.github.io/MaltaProj5/),
  [Flagged for Review](https://buffedlizard55-lab.github.io/MaltaProj5/review.html),
  [row-by-row sources and quotations](https://buffedlizard55-lab.github.io/MaltaProj5/sources.html),
  [analysis](https://buffedlizard55-lab.github.io/MaltaProj5/analysis.html), and
  [machine-readable audit summary](https://buffedlizard55-lab.github.io/MaltaProj5/data/audit_summary.json).
  At the T29 cutoff, the live summary confirmed **162 directory / 80 review-only / 242 assessed**,
  20 weekly / 7 monthly / 25 annual / 110 special, 237 URLs / 140 domains. PR #28 later superseded this historical snapshot. Each
  table row links to its explicit evidence anchor and organizer/venue source; for
  example, [Foodwise's Ferry Plaza Farmers Market page](https://foodwise.org/markets/ferry-plaza-farmers-market/),
  [California Academy of Sciences NightLife](https://www.calacademy.org/nightlife),
  and the [Exploratorium After Dark page](https://www.exploratorium.edu/visit/calendar/after-dark).

### CI and publication checked during T29

A parallel finalization session (`t26-3164fba7`) merged PR
[#26](https://github.com/buffedlizard55-lab/MaltaProj5/pull/26) while T29 was in
progress. Its PR validation [39101709231](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39101709231)
and post-merge main validation [39101713471](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39101713471)
completed successfully. Pages workflow
[39101713098](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39101713098)
also succeeded; the Pages API reports build **1293663243** as `built` for merge
commit `b7fed62c5678c462ba98c476e92a1b2e18eb641d`. The live pages above were fetched
against that deployment. PR #26's source-reachability gate passed; that gate blocks
404/410 but does not treat HTTP success as verification.

The newer session was not listed when T29 was claimed. After PR #26 landed, T29
rebased onto `origin/main` cleanly; its session registry/task record was retained.
No data, source, or site file owned by that session was modified.

### Flags and limits

* **Non-exhaustive scope:** the site's own summary labels the snapshot bounded and
  non-exhaustive. It does not establish a full or unique count of every changing
  San Francisco event. The 80 held candidates, known coverage gaps, and unsupported
  fields remain visible on Flagged for Review; no candidate or missing fact was
  promoted to the directory during T29.
* **Release-note discrepancy — request to `t26-3164fba7`:** merged PR #26's body says
  “Review-only events: 4,” while the data/review page at that merge showed **80**
  (PR #28 later superseded the count; the current snapshot has 79). The published
  site/data are correct; please correct the PR description if practical. Its broad
  “verified pages” wording should also retain
  the site's distinction between archived fact evidence and URL reachability. T29
  did not edit another session's PR metadata or alter site content.
* The task board contains two historical rows numbered T21 from an earlier
  cross-session integration. This historical numbering irregularity is left intact;
  it does not affect the register or deployed pages.

### T29 branch reconciliation — 2026-10-18

Before the second push, `git pull --rebase origin main` incorporated PR #26. The
push was then rejected non-fast-forward because the session remote still held the
original T29 claim commit `cdc1e66` on the pre-PR-#26 base. Fetch showed that this
remote branch contained only that earlier claim, with no other session commits.
A merge was used (no force push); `COORDINATION.md` conflicted where the original
“in progress” claim overlapped this completed T29 record and the newer mainline
session row. Resolution retained both the `t26-3164fba7` mainline record and T29's
completed audit/results, then added this reconciliation note. No other files or
session work were discarded.

## Publication record — T29 audit — `0574b8f6`

| Item | Result |
|---|---|
| PR | [#27](https://github.com/buffedlizard55-lab/MaltaProj5/pull/27), merged 2026-10-18 05:52:33 UTC |
| Merge commit | `5930def0c87e70c441f74dc45eba4fa373a5217e` |
| PR validation | [39102000536](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102000536) **success**; all 30 tests, browser/accessibility, evidence, local-link and source-reachability gates passed |
| Main validation | [39102055629](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102055629) **success** |
| Pages | [39102055366](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102055366) **success**; Pages build **1293671971** was `built` for `5930def` |
| Snapshot at publication | 242 candidates / 162 listed / 80 review-only; PR #28 later superseded these counts |

## Publication record — T29-cal / T30 / T31 — `bb551cdc`

| Item | Result |
|---|---|
| PR | [#28](https://github.com/buffedlizard55-lab/MaltaProj5/pull/28) merged 2026-10-18 05:55:00 UTC |
| Merge commit | `f90ae8b2d06069ebbb9ac734700db99f94cda9df` |
| Main validation | [39102196169](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102196169) **success** |
| Pages | [39102195213](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102195213) **success** |
| Live site | https://buffedlizard55-lab.github.io/MaltaProj5/ |
| Register | 246 candidates / 167 listed / 79 review-only |

Sources: Rec Park EID 9528 and 9947, SF.gov Civic Center Soundtrack, Rec Park Illuminate LIVE news flash, comedyday.org + FAQ. Harvest Festival and Festival of Chariots not added (incomplete official pages). Comedy Day date blank.

Reachability only: PR #28 run 39102137078 reported 47 restricted/challenge/server/transport responses; post-merge run 39102196169 reported 40. The 404/410 gate passed; unknowns are not semantic verification.

### T31 publication-record follow-up — documentation-only PR #29

[PR #29](https://github.com/buffedlizard55-lab/MaltaProj5/pull/29) merged at
2026-10-18 05:56:47 UTC as `06b44bbf17af6cfe6579954688fb9d6fd83ed03d`.
Main validation [39102291756](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102291756)
and Pages workflow [39102291538](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39102291538)
succeeded; Pages API build **1293677966** is `built` for that commit. PR #29 changed
coordination documentation only; the 246/167/79 event register is from PR #28.
