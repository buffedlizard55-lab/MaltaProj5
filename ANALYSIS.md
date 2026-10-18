# ANALYSIS.md — findings from the verified San Francisco register

Snapshot **2026-10-18**. Every figure below is computed from `data/events.json`
(214 rows), `data/sources.json` (199 records), `data/review.json` (25 findings) and
`data/verify_report.json` (the machine fetch of every cited URL). The published version of this
analysis is `analysis.html`.

## Headline numbers

| Measure | Value |
|---|---|
| Register entries | 214 |
| — weekly | 22 |
| — monthly | 11 |
| — annual | 120 |
| — special / dated | 61 |
| Series or standalone entries (dated occurrences excluded) | 206 |
| Entries by category — festivals & culture | 106 |
| — community & outdoors | 50 |
| — markets & food | 33 |
| — museums & science | 25 |
| Official source records | 199 |
| Distinct source domains | 130 |
| Rows verified field-level | 100 |
| Rows verified page-level | 79 |
| Rows flagged for review | 35 |
| Rows with at least one blank tracked field | 180 |
| Review findings | 25 |
| Cited URLs that were dead in the last check | 0 |

## Verification outcome (2026-10-18 automated pass)

Every cited URL was fetched from GitHub Actions and its visible text searched for the event name.

| Result | Rows |
|---|---|
| Event name found on a cited page | 151 |
| Not found in the fetched text (mostly bot-blocked or JavaScript-rendered) | 61 |
| Cites a PDF, read manually (not machine-matchable) | 2 |
| No response | 0 |
| Dead URLs (404/410/DNS) | 0 |
| URLs that blocked the automated client (202/403/405/429/5xx) | 46 |

A blocked page is not evidence of a bad event. Those rows keep a label and their notes are
published on `review.html`; 35 rows carry an automation-generated "manual re-check requested"
note. Several rows in the 167-row register cited a generic landing page rather than the event page;
during integration the three Chase Center concerts, both PIER 39 events, the Symphony season and
opening gala, ArtSpan Open Studios and Tulip Day were re-pointed to specific official pages.

## Findings

### 1. Annual traditions dominate; the weekly layer is thin and market-shaped

120 annual entries against 22 weekly and 11 monthly. The weekly layer is mostly farmers markets,
museum late nights (NightLife, After Dark) and standing park programmes. This is a festival
calendar, not a weekly-rhythm calendar.

### 2. Most annual rows have no organizer-published 2027 date

98 of the 120 annual rows carry no 2027 date in their schedule. Recurring patterns are preserved
as patterns: where an organizer has not posted the next edition, the date cell is blank rather than
extrapolated. 180 rows have at least one blank tracked field
(most often the start time, which many market pages do not publish separately from opening hours).

### 3. Coverage is uneven and not exhaustive

No official source publishes a complete count of San Francisco events, so the register cannot
claim completeness. Known gaps: public-library programmes, most theatre (beyond opera and ballet),
weekday civic meetings, sports beyond the Giants, and many neighbourhood block parties. Festivals,
markets and museums are over-represented because their organizers publish machine-readable pages.

### 4. Source concentration is high, and that is a risk

199 source records sit on 130 domains, but a handful of publishers supply many rows: San Francisco
Opera's season press page covers five productions, PIER 39's events page covers two rows, and
several farmers-market rows share association listing pages. One page changing can invalidate
several rows at once. The review page names each shared-source group.

### 5. Two registers reconciled without loss

The 86-row register (sessions `3a19e72d`/`5a85baf2`) and the 167-row inventory (session
`4f47c142`) were merged with an explicit, reviewed map. 36 rows described the same event in both
registers and were reconciled rather than dropped; each keeps both official sources. A fuzzy
matcher was rejected: it proposed false pairs such as Frameline vs International Ocean Film
Festival. One row (SOMA Nights) was removed because its only official site is unreachable and no
other official page confirms the 2026 edition.

### 6. Reclassification was necessary

Two rows filed as "Special" (Chinese New Year Parade, Carnaval) are annual editions and were moved
to Annual. "After Dark: Creepatorium" was filed as Annual but is a single dated theme of the
weekly series, so it moved to Special. A merchandise-store window was removed: it is not an event.

## Method limits

The automated pass proves a page is live and names an event. It cannot prove a date, time, price or
venue. Field-level rows rest on a researcher's transcription; page-level rows rest on an
independent pass plus the automated name check. Where the two disagree or a page is ambiguous, the
value is blank and the question is on `review.html`.
