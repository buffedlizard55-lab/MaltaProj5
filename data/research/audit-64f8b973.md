# Corrective audit — session 64f8b973

Research date: **18 October 2026**. This log supersedes the earlier site’s field/page-level verification labels; historical coordination records are preserved, not silently rewritten as current truth.

## Dispositions and scope

- All **231 initial candidates** received explicit dispositions; **2 additional mainline audit candidates** were retained and reviewed, plus **9 newly sourced official-calendar entries**. Total: **242**.
- **162 entries** pass the name + venue + SF geography directory gate. **80 candidates** remain review-only. This is not “242 fully verified events.”
- Every unapproved factual field is blank, including unknown names. An unverified inherited title remains an explicitly labeled candidate identifier for traceability.
- 20 weekly, 7 monthly, 25 annual entries have explicit recurrence evidence; 110 special/dated/cadence-unconfirmed entries have no unsupported ongoing cadence claim.
- Directory entries include 14 programme umbrellas. Parent/child links prevent treating the totals as unique-event counts; other changing citywide coverage is incomplete.

## Evidence trail

`data/audit_64f8b973.json` is the authoritative finite evidence/decision ledger. The first runner capture succeeded in Actions run **39092033950**, job **117570642864**, at `2026-10-18T03:00:08+00:00`: 217 URLs, 187 HTTP 200 / 26 HTTP 403 / 2 HTTP 405 / 2 HTTP 202. Those outcomes were not field verification. A later capture attempt (**39092617416**) preserved adjudicated evidence and recorded attempt metadata separately.

Independent official-page reads supplied selected, labeled excerpts where the runner was blocked. These are not whole-page raw captures. Event JSON-LD is explicitly distinguished from text (notably SFMOMA’s SF address). Quotations are validated against the stored evidence, but exact matching alone never establishes applicability.

Useful source blocks and the final field decisions are linked per row in `sources.html`; every review row links directly to an official page, including candidates where no fact could be approved.

## Consequential corrections

| Candidate / issue | Audit disposition |
|---|---|
| Zoo SF Resident Free Day | October 7, 2026, 10am–4pm; residency ID required. No monthly first-Tuesday rule established. |
| Boo at the Zoo | October 31, 2026, 10am–3pm. Activities included with paid daytime admission/membership; not free general admission. |
| Zoo Member Mornings | Specific October 3, 2026, 9am–10am listing. No generic weekly recurrence established. |
| Fiesta en el Parque | Corrected August 2 to **August 1, 2026**. |
| Opera Ball | Current page reschedules gala to **November 12, 2026** at SF City Hall; explicitly no Opera House performance that night. Old combined opening/gala candidate held for review. |
| Bhangra & Beats | Two 2026 dates; new Yerba Buena Gardens/Jessie Square/Yerba Buena Lane venue. |
| Menorah / Cole / Taraval / ancillary B2B events | Yearless body copy not assigned an invented year from weekday, URL, anniversary or another event banner. |
| Pride / Carnaval / other 2027 announcements | Future dates not combined with older editions’ times, venues or admission. Pride’s 2027 venue/price remain blank and held. |
| Alemany | SF.gov/operator current hours conflict with older City Environment hours; time blank and conflict retained. |
| Secondhand / Muertos | Conflicting street extents; precise venues blank and candidates held for review. |
| FAMSF first Tuesdays | Split by museum venue: de Young and Legion entries no longer duplicate the same combined two-museum row. Permanent-collection/Bouquets to Art conditions retained. |
| SFMOMA RM exhibition | $10/$12 is a surcharge, not the total admission. Sarah Sze opening has no fabricated closing date. |
| Kung Pao Kosher Comedy | In-person dinner/cocktail prices kept distinct from lower virtual ticket prices. |
| Regional programmes | Frameline, Art Week, Climate Week, Dance Week, NEXUS, Jewish Film Festival, Beer Week and full SF Marathon held for SF-only component/route checks. |
| Old Presidio/Zoo/City calendar claims | Generic current calendars do not substantiate unmentioned named programmes or old seasonal schedules. |

The nine new entries are six official upcoming calendar blocks (SFMOMAween, Kiki Ball, YBG Halloween Hoopla, Afro-Filipino Jazz Project, Foodwise Día de los Muertos and bakery demo) plus three explicit past Presidio event blocks (Intertribal Dance Gathering, Deaf Dance Festival SF component, Inside Out cinema).

## Pipeline and site safeguards

- `tools/consolidate.py` reconstructs legacy history, then invokes `tools/audited_register.py` as its mandatory last stage. There is no inherited-value fallback.
- Approval requires quotations; recurring kinds require recurrence evidence; SF publication requires name/venue/geography; dates require full ISO approval plus year/month/day support in quotations.
- The old matcher applicator is retired. Capture/reachability jobs cannot auto-commit factual field labels.
- CSVs separate directory-only rows from the entire candidate review register. Website tables preserve actual blank cells.
- Analysis separates URLs/domains/organizations, entries/unique events, and dataset composition/citywide coverage.

## Checks executed before PR

- Exact canonical projection and quotation validation: **pass**, 242 records / 162 directory / 80 held.
- **30 offline regression tests pass**: unsupported fallback, name-only approval, missing decisions, unsupported cadence/location, invented year/month, observed Zoo/Presidio/Opera regressions, cross-edition carryover, regional quarantine, pricing eligibility, FAMSF split, structured address, closing-date blanks, temporal status, parent cycles, failed evidence refresh retention.
- Full rebuild repeated: canonical JSON, both CSVs, analysis markdown and all 12 HTML pages are **byte-identical**.
- Local HTML/fragment/reference/CSV checks: **pass**.
- Real Chromium 153 smoke test: all 12 pages at **1440×1000** and **390×844**, no document overflow, functioning filters/reset/empty state, official/evidence navigation, no-JavaScript readability and no runtime/asset errors.
- Automated axe-core WCAG A/AA test: initial small-metadata contrast failures corrected; **zero automated violations** on overview, analysis, review and evidence page types. This is not a complete accessibility certification.

External URL checks, actual CI, PR merge and successful GitHub Pages publication are recorded in `COORDINATION.md` only after they run; no deployment is claimed by this research log.

## Reconciliation with newer main (`092a1f4`, PRs #14–#20)

The other sessions' full coordination logs, `data/audit_f1fd3c36.json`,
`tools/apply_audit.py` and base86 price blanking are retained. The claimed upstream
tool/ledger were not edited. An isolated temporary-tree adapter applies that
research as **unverified candidate history** before this audit's mandatory gate.
Both added candidates remain: Alemany Flea Market is SF/weekly evidenced from the
City page; Doc Stories has November 5–8, 2026 dates but no verified venue and stays
held. A small reference ledger retains the official 2026 Sketchfest Sched link;
a comparison found no other mainline row source URL missing from the combined
history. Ferry Fest's former 404 is historical only, visible in review and excluded
from active sources. The combined register cites 237 exact URLs across 140 domains.

New primary pages from the companion research were independently re-read and
archived as labeled excerpts: FAMSF's advance schedule/Bouquets release, the Zoo's
dedicated ZooLights page, SFPL's Night of Ideas page, SFIAF, the 2027 art-fair ticket
page, Free Folk Festival, QWOCFF's SF in-person block, Fall Show, Valencia LIVE!, and
the City's Cinema on the Square release. Current 2027 ticket/venue evidence was
not mixed with 2026 editions. Juneteenth's site currently returns a hosting error,
so no prior claimed facts were restored from that error page. Sketchfest's 2027
banner confirms dates, not a venue; its prior 2026 claims remain history.

**Context correction:** Lit Crawl's 6:30–7:30 PM line follows the changed-venue
notice and does not establish hours for the whole crawl. Its time is now blank,
superseding the earlier draft reading. This demonstrates why exact quote matching
is only provenance, not semantic verification.

Combined local checks pass after reconciliation: 29 offline tests; all 242 record
projections and page/CSV/link checks; real desktop/mobile Chromium with all 12
pages, 163 directory rows and 79 held candidates; zero automated WCAG findings on
four core page types. A new mobile overflow caused by the historical 404 URL was
found by the real-browser test and fixed with wrapping. CI and Pages results are
still recorded only after they actually occur.

## Final cross-edition exception removed

The full Nihonmachi homepage places “San Francisco’s Japantown” in its 52nd-edition
retrospective, while the 53rd-edition 2027 announcement gives only August 7–8 dates.
Those dates/annual evidence are retained, but future venue is now blank and the
candidate held for review, consistently with Pride/Fillmore. Current counts are
162 directory / 80 held; 25 listed annual entries. A thirtieth regression and
browser assertions prevent this specific carryover from returning. The earlier
163/79 deployment/check records describe the actual pre-tightening snapshot.

The final correction was merged in PR #24 (`b5e9afc`, 2026-10-18 04:15:16 UTC).
All 30 regressions, strict rebuild/field/CSV/local-link/browser/accessibility and
source-URL gates passed both on the PR (run 39096365405) and actual main merge
(run 39096451167). Pages run 39096451005 succeeded; API build 1293522885 was built
for that exact commit at 04:15:37 UTC. Live dashboard/summary JSON confirmed
162 directory / 80 held / 242 assessed, 237 URLs / 140 domains. Source responses
included explicit unknowns (39 on the PR, 38 on main), zero definite 404/410;
none was interpreted as automatic semantic verification. Full details and the
preserved earlier publication records are in COORDINATION.md.
