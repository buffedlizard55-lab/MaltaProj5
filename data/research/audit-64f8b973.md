# Corrective audit — session 64f8b973

Research date: **18 October 2026**. This log supersedes the earlier site’s field/page-level verification labels; historical coordination records are preserved, not silently rewritten as current truth.

## Dispositions and scope

- All **231 inherited candidates** received explicit dispositions, plus **9 newly sourced official-calendar entries**.
- **149 entries** pass the name + venue + SF geography directory gate. **91 candidates** remain review-only. This is not “240 fully verified events.”
- Every unapproved factual field is blank, including unknown names. An unverified inherited title remains an explicitly labeled candidate identifier for traceability.
- 19 weekly, 6 monthly, 23 annual entries have explicit recurrence evidence; 101 special/dated/cadence-unconfirmed entries have no unsupported ongoing cadence claim.
- Directory entries include 13 programme umbrellas. Parent/child links prevent treating the totals as unique-event counts; other changing citywide coverage is incomplete.

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

- Exact canonical projection and quotation validation: **pass**, 240 records / 149 directory / 91 held.
- **24 offline regression tests pass**: unsupported fallback, name-only approval, missing decisions, unsupported cadence/location, invented year/month, observed Zoo/Presidio/Opera regressions, cross-edition carryover, regional quarantine, pricing eligibility, FAMSF split, structured address, closing-date blanks, temporal status, parent cycles, failed evidence refresh retention.
- Full rebuild repeated: canonical JSON, both CSVs, analysis markdown and all 12 HTML pages are **byte-identical**.
- Local HTML/fragment/reference/CSV checks: **pass**.
- Real Chromium 153 smoke test: all 12 pages at **1440×1000** and **390×844**, no document overflow, functioning filters/reset/empty state, official/evidence navigation, no-JavaScript readability and no runtime/asset errors.
- Automated axe-core WCAG A/AA test: initial small-metadata contrast failures corrected; **zero automated violations** on overview, analysis, review and evidence page types. This is not a complete accessibility certification.

External URL checks, actual CI, PR merge and successful GitHub Pages publication are recorded in `COORDINATION.md` only after they run; no deployment is claimed by this research log.
