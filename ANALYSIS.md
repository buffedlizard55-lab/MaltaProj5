# ANALYSIS.md — findings from the verified San Francisco register

Snapshot **2026-10-18**. Every figure below is computed from `data/events.json`
(231 rows), `data/sources.json` (213 records), `data/review.json` (19 findings) and
`data/verify_report.json` (the machine fetch of every cited URL). The published version of this
analysis is `analysis.html`.

## Headline numbers

| Measure | Value |
|---|---|
| Register entries | 231 |
| — weekly | 25 |
| — monthly | 11 |
| — annual | 135 |
| — special / dated | 60 |
| Series or standalone entries (dated occurrences excluded) | 224 |
| Entries by category — festivals & culture | 113 |
| — community & outdoors | 61 |
| — markets & food | 34 |
| — museums & science | 23 |
| Official source records | 213 |
| Distinct source domains | 135 |
| Rows verified field-level | 117 |
| Rows verified page-level | 79 |
| Rows flagged for review | 35 |
| Rows with at least one blank tracked field | 188 |
| Review findings | 19 |
| Cited URLs that were dead in the last check | 0 |

## Verification outcome (2026-10-18 automated pass)

Every cited URL was fetched from GitHub Actions and its visible text searched for the event name.

| Result | Rows |
|---|---|
| Event name found on a cited page | 165 |
| Not found in the fetched text (mostly bot-blocked or JavaScript-rendered) | 64 |
| Cites a PDF, read manually (not machine-matchable) | 2 |
| No response | 0 |
| Dead URLs (404/410/DNS) | 0 |
| URLs that blocked the automated client (202/403/405/429/5xx) | 46 |

A blocked page is not evidence of a bad event. Those rows keep a label and their notes are
published on `review.html`; 35 rows carry an automation-generated "manual re-check requested"
note. Two rows that could only be sourced to a generic landing page in the 167-row register
(Chase Center concerts, PIER 39) were re-pointed to specific official event/news pages during
integration.

## Findings

### 1. Annual traditions dominate; the weekly layer is thin and market-shaped

135 annual entries against 25 weekly and 11 monthly. The weekly layer is mostly farmers markets,
museum late nights (NightLife, After Dark) and standing park programmes. This is a festival
calendar, not a weekly-rhythm calendar.

### 2. Most annual rows have no organizer-published 2027 date

Of the 135 annual rows, 24 already carry a dated 2027 edition or season; the rest preserve the
recurring pattern only. Where an organizer has not posted the next edition, the date cell is not
invented. 188 rows have at least one blank tracked field (most often the start time, which many
market pages do not publish separately from opening hours).

### 3. Coverage is uneven and not exhaustive

No official source publishes a complete count of San Francisco events, so the register cannot
claim completeness. Known gaps: public-library programmes, most theatre (beyond opera, ballet and
the two seasons added by session `a1b7522f`), weekday civic meetings, sports beyond the Giants,
Warriors and Valkyries, and many neighbourhood block parties. Festivals, markets and museums are
over-represented because their organizers publish machine-readable pages.

### 4. Source concentration is high, and that is a risk

213 source records sit on 135 domains, but a handful of publishers supply many rows: San Francisco
Opera's season press page covers five productions, PIER 39's events page covers two rows, and 12
rows cite San Francisco Travel (the city's destination-marketing body) because no organizer page
for that edition could be found. One page changing can invalidate several rows at once. The review
page names each shared-source group.

### 5. Three registers reconciled without loss

The 86-row register (sessions `3a19e72d`/`5a85baf2`), the 167-row inventory (session
`4f47c142`) and the 20-row expansion (session `a1b7522f`) were merged with an explicit, reviewed
map. 37 rows described the same event in two registers and were reconciled rather than dropped;
each keeps both official sources. A fuzzy matcher was rejected: it proposed false pairs such as
Frameline vs International Ocean Film Festival. One row (SOMA Nights) was removed because its only
official site is unreachable and no other official page confirms the 2026 edition.

### 6. Reclassification and de-duplication were necessary

The Chinese New Year Parade and Carnaval were reclassified from Special to Annual. "After Dark:
Creepatorium" was filed as Annual but is a single dated theme of the weekly series, so it moved to
Special. Two duplicate pairs were merged during final review (Legion free Tuesdays, and the two
2026 dates of After Dark: Unplug and Play). A merchandise-store window was removed: it is not an
event.

## Method limits

The automated pass proves a page is live and names an event. It cannot prove a date, time, price or
venue. Field-level rows rest on a researcher's transcription; page-level rows rest on an
independent pass plus the automated name check. Where the two disagree or a page is ambiguous, the
value is blank and the question is on `review.html`.
