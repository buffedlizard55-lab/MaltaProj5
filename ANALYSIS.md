# ANALYSIS.md — findings from the verified San Francisco register

Snapshot **2026-10-18**. Every figure below is computed from `data/events.json`
(233 rows), `data/sources.json` (236 records), `data/review.json` (20 findings) and
`data/verify_report.json` (the machine fetch of every cited URL). The published version of this
analysis is `analysis.html`.

## Headline numbers

| Measure | Value |
|---|---|
| Register entries | 233 |
| — weekly | 26 |
| — monthly | 12 |
| — annual | 137 |
| — special / dated | 58 |
| Series or standalone entries (dated occurrences excluded) | 224 |
| Entries by category — festivals & culture | 114 |
| — community & outdoors | 61 |
| — markets & food | 35 |
| — museums & science | 23 |
| Official source records | 236 |
| Distinct source domains | 139 |
| Rows verified field-level | 150 |
| Rows verified page-level | 75 |
| Rows flagged for review | 8 |
| Rows with at least one blank tracked field | 172 |
| Review findings | 20 |
| Cited URLs that were dead in the last check | 0 |

## Manual line-by-line audit (2026-10-18, session f1fd3c36)

After the automated pass, 70 rows were re-read by a person against their official pages in
readable form — every row the automated check could not name-match, the aggregator-only rows, the
PDF-cited rows, and the three rows that carried a value *and* an "unverified; left blank" note.
Result: 36 confirmed as published, 28 corrected, 6 left unverified and flagged, 2 rows added
(Alemany Flea Market; SFFILM Doc Stories). Each change is recorded with the URL and the quoted
text in `data/audit_f1fd3c36.json` and applied by `tools/apply_audit.py`. Irregularities found:

* **Litquake dates disagreed between two rows** (Oct 4–24 vs Oct 8–24); the official schedule page
  says October 8–24, 2026 and both rows now agree.
* **California International Antiquarian Book Fair alternates cities** — the 2027 edition is in
  Los Angeles, so the next San Francisco edition is not before 2028; the row is relabelled biennial.
* **Lowrider Parade / King of the Streets** — the organizer's site still shows the 2025 edition;
  the 2026 date previously listed is not on it and was removed (row flagged).
* **Fourth of July** — the City states the Golden Gate Bridge display is the only authorized
  fireworks in San Francisco in 2026; the PIER 39 row's "fireworks ~9:30pm" refers to viewing it.
* **Venues corrected from official pages**: SF International Arts Festival (Mission District, not
  Fort Mason), Queer Women of Color Film Festival (Presidio Theatre, not Brava), Peak2Peak
  (southeast neighbourhoods, not the Mission), SF Cheese Fest (Gold Bar Distillery, Treasure Island).
* **Renamed to the organizer's name**: Superfair (formerly Superfine Art Fair), The San Francisco
  Fall Show, Easter in the Park (Hunky Jesus contest), Valencia LIVE! (now a monthly series).
* **Organizer pages found for 9 aggregator-only rows** (Easter in the Park, Ferry Fest, Cinema on the
  Square, Sunset Night Market, SF Music Week, Pizza Bagel & Beer Festival, Valencia LIVE!, Black
  Coffee Treasure Island, SF Hash Week); the Disability History Tour and Super Bowl LX fan events
  still rest on the SF Travel listing and remain flagged. Illuminate SF is produced by SF Travel, so
  that listing is the organizer's own page.
* **Regional programmes labelled**: CAAMFest, SF Jewish Film Festival, Bay Area Dance Week and the
  Super Bowl LX events also run outside the city; only the San Francisco programme is in scope.
* **Pipeline contradiction removed**: three rows (Ferry Plaza Farmers Market and two others)
  carried a price and a "price: unverified; left blank" note; the operator pages do not state
  admission, so the cells are blank and the notes consistent.

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
published on `review.html`; 35 rows carried an automation-generated "manual re-check requested"
note, of which 34 were then re-read by hand in the line-by-line audit (one, Super Bowl LX fan
events, rests on a bot-blocked aggregator page and remains flagged). Two rows that could only be sourced to a generic landing page in the 167-row register
(Chase Center concerts, PIER 39) were re-pointed to specific official event/news pages during
integration.

## Findings

### 1. Annual traditions dominate; the weekly layer is thin and market-shaped

137 annual entries against 26 weekly and 12 monthly. The weekly layer is mostly farmers markets,
museum late nights (NightLife, After Dark) and standing park programmes. This is a festival
calendar, not a weekly-rhythm calendar.

### 2. Most annual rows have no organizer-published 2027 date

Of the 137 annual rows, 32 already carry a dated 2027 edition or season; the rest preserve the
recurring pattern only. Where an organizer has not posted the next edition, the date cell is not
invented. 172 rows have at least one blank tracked field (most often the start time, which many
market pages do not publish separately from opening hours).

### 3. Coverage is uneven and not exhaustive

No official source publishes a complete count of San Francisco events, so the register cannot
claim completeness. Known gaps: public-library programmes, most theatre (beyond opera, ballet and
the two seasons added by session `a1b7522f`), weekday civic meetings, sports beyond the Giants,
Warriors and Valkyries, and many neighbourhood block parties. Festivals, markets and museums are
over-represented because their organizers publish machine-readable pages.

### 4. Source concentration is high, and that is a risk

236 source records sit on 139 domains, but a handful of publishers supply many rows: San Francisco
Opera's season press page covers five productions, PIER 39's events page covers two rows, and 12
rows cite San Francisco Travel (the city's destination-marketing body); after the audit, organizer
pages were added to 9 of them and only 2 (Disability History Tour, Super Bowl LX fan events) rest
on the SF Travel listing alone. One page changing can invalidate several rows at once. The review
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
