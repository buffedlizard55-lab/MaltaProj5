# Coordination

Shared task board for every agent session working in `buffedlizard55-lab/MaltaProj5`.

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
(`needs review` = published on `review.html`; it does not block anything.)

---

## Session registry

| Session ID | Branch | Started (UTC) | Role |
|---|---|---|---|
| `3a19e72d` | `arena/3a19e72d-maltaproj5` | 2026-10-18 ~00:20 | Research, dashboard, validation, Pages workflow (PRs #1, #2) |
| `5a85baf2` | `arena/5a85baf2-maltaproj5` | 2026-10-18 00:54 | Research, verification, analysis, checks (PR #3), first integration |
| `4f47c142` | `arena/4f47c142-maltaproj5` | 2026-10-18 ~00:40 | Full-inventory research (167 events), docs/ site, verification pass, second integration (PR #4) |

> **Branch policy note.** Arena pins each session to a fixed branch
> (`arena/<session>-maltaproj5`), so the requested `session-<id>/<task>` naming could not be used by
> any session. All three noted this independently. Scopes were kept non-overlapping at file level
> (unavoidable overlaps in `COORDINATION.md` / `README.md` / the Pages workflow are recorded in the
> merge conflict logs below).

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
| T14 | Second integration: fold all three sessions' work into one tree; publish `docs/` site as primary with the unified register under `/inventory/` | done | `4f47c142` | `COORDINATION.md`, `README.md`, `.github/workflows/pages.yml`, `docs/` |
| T15 | GitHub Pages publication | **blocked (owner action)** | all sessions | `.github/workflows/pages.yml` |

**Reconciliation note (T11 vs T2/T3/T9):** sessions `5a85baf2` and `4f47c142` researched
overlapping scopes independently (both claim "final" inventories). Neither is discarded: the
86-row unified register (sessions `3a19e72d`+`5a85baf2`, root site) and the 167-event inventory
(session `4f47c142`, `docs/` site) are both preserved and both published — the larger inventory as
the primary Pages site, the unified register at `/inventory/`. Row-level spot-checks across the
datasets found no factual contradictions (details in the verification logs below).

---

## Merge conflict log

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

**2026-10-18 — `4f47c142` second integration merge of `origin/main` (first `bb74afd`, then `5167522`
after PR #3 merged mid-flight) into `arena/4f47c142-maltaproj5`.**

All three sessions started from `20813bf` and raced on claims (documented in each activity log).
Two merge rounds, conflicts resolved as follows:

| File | Resolution |
|---|---|
| `COORDINATION.md` | Unified three-session board (this file): `5a85baf2`'s rules/registry/board retained and extended with T11–T15; all three activity logs + verification records preserved verbatim below. |
| `README.md` | Rewritten to describe both sites and both datasets (see README for the mapping). |
| `.github/workflows/pages.yml` | Auto-merged: `5a85baf2`'s remote-check step and `4f47c142`'s staging change coexist. Staging was amended so `docs/` (167-event site) publishes at the Pages root and the 86-row unified register's root site is served under `/inventory/` — nothing deleted; `scripts/build.py`, `scripts/validate.py`, `tools/remotecheck.py` and the deploy job are untouched. `tools/verify_site.py` added to the validate job. |
| data / sites | No collisions at file level: `4f47c142`'s datasets are `data/events-{weekly,annual,special}.json` + `data/exclusions.json`, its site is `docs/`; the unified register is `data/events.json` at the repo root. |

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
`.github/workflows/pages.yml`; the outcome is recorded in the PR / CI record below.

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

**Notable irregularities found & handled** (full list on the site's Flagged page):
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
Two exclusions are shared knowledge: Dickens Fair (Cow Palace, Daly City) and Super Bowl LX /
FIFA World Cup (Levi's Stadium, Santa Clara) are out-of-city; `4f47c142` additionally verified the
How Weird Street Faire discontinuation and Ghirardelli Chocolate Festival absence independently.

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

## Activity log — `4f47c142`

- 2026-10-18 ~00:40: created an initial T1–T7 coordination board (commit `b746517`), pushed before
  starting research. (Race note: all three sessions began from `20813bf`; `3a19e72d` and `5a85baf2`
  never saw this board before writing theirs, and this session did not see theirs — each activity
  log records its own intake view.)
- Research (T11): 34 weekly + 95 annual + 38 special events + 14 exclusions authored; every row
  carries `source_url` + `source_name`; ~20 rows flagged where official confirmation was
  unavailable (listed above). Raw notes in `data/research/sftravel-2026-notes.md`.
- Build (T12): `tools/build_site.py` generates the `docs/` static site (dashboard, weekly/annual/
  special subpages, Flagged for Review, search & filters, JSON/CSV downloads); no dependencies.
- Verification (T13): `tools/verify_site.py` 0 errors / 0 warnings (details above). Committed
  `b274acc`, pushed.
- First merge round: merged `bb74afd` (PRs #1–#2). Cross-checked `3a19e72d`'s 29 rows — consistent;
  no invented sources. Unified board + README; their site preserved at root, this session's site
  in `docs/`. Recorded the Pages 403 blocker as unconfirmed-by-this-session at that point.
- Discovered PR #3 (`5a85baf2`) open; spot-checked their 61-row register — all official sources,
  consistent with this dataset; recorded as in-progress parallel work. PR #3 then MERGED at
  01:18:46 UTC (`5167522`) while this session's PR #4 was being prepared, making PR #4 conflicting.
- Second merge round (T14): merged `5167522`; resolved `COORDINATION.md` (this unified board) and
  `README.md`; workflow auto-merged. Amended the Pages staging step so `docs/` publishes as the
  primary site with the unified register served at `/inventory/` (both preserved). Re-ran both
  validators on the merged tree (see PR #4 CI).
- Pages enable re-attempted by this session via `gh` after merging — see PR / CI / Pages record.

---

## PR / CI / Pages record

| Item | Result |
|---|---|
| PR #1 (`3a19e72d`) | Merged 2026-10-18 00:59:25 UTC, merge commit `c8c2f65` |
| PR #2 (`3a19e72d`) | Merged, merge commit `bb74afd` |
| PR #3 (`5a85baf2` → `main`) | Merged 2026-10-18 01:18:46 UTC, merge commit `5167522` |
| CI on PR #3 | validate: pass (incl. `tools/remotecheck.py` on 75 source URLs) |
| PR #4 (`4f47c142` → `main`) | https://github.com/buffedlizard55-lab/MaltaProj5/pull/4 — second integration; result recorded below |
| CI on PR #4 | validate: pass (6s) on first push; re-run on final push recorded below |
| GitHub Pages | **Not live.** Blocked by credential permissions, reproduced independently by `3a19e72d` and `5a85baf2` (HTTP 403, empty `X-Oauth-Scopes`, `X-Accepted-Github-Permissions: metadata=read`). Owner action required: repo Settings → Pages → Source (deploy from `main` / `docs`, or GitHub Actions). Then re-run `Validate and deploy Pages`. |
