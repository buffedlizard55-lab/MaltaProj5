# ANALYSIS.md — findings from the verified register

Generated 2026-10-18. Every figure below is computed from `data/events.json`
by `tools/validate.py`; every row is sourced to an official page listed in `SOURCES.md`.

## Headline numbers

| Measure | Value |
|---|---|
| Events in the register | 61 |
| Recurring — weekly | 4 |
| Recurring — monthly | 3 |
| Recurring — annual | 44 |
| Special / dated | 10 |
| Rows with a confirmed future date | 32 |
| Continuous pattern series (no single next date) | 7 |
| Next date not published by the organizer | 22 |
| Rows with a genuine irregularity | 14 |
| Free or donation-entry events | 44 |
| Distinct official source domains | 43 |
| Excluded after an official check | 4 |

## Findings

### 1. Annual festivals dominate; the weekly layer is thin

44 of 61 entries repeat once a year, against 4 weekly and
3 monthly. San Francisco's public event calendar is a festival calendar, not a
weekly-rhythm calendar. The genuinely weekly layer is almost entirely farmers markets
(Ferry Plaza, Alemany, Heart of the City) plus the Golden Gate Park Band's Sunday concerts.

### 2. About a third of the register has no published next date

22 of 61 entries (36%) are confirmed events whose organizer
has not posted the next edition's date. This is concentrated in autumn: after their 2026 editions,
Hardly Strictly Bluegrass, Litquake/Lit Crawl, Sunday Streets, the Greek Food Festival,
St. Patrick's Day Parade, Pistahan, North Beach Festival and Union Street Festival had all published
nothing for 2027. **Any list showing 2027 dates for these is extrapolating, not reporting** — which
is exactly why those cells are blank here.

### 3. Official pages frequently disagree with each other (14 irregularities)

The recurring patterns:

- **Hours differ between two official pages.**
  - Alemany Farmers Market: sf.gov's location page says Saturday 7am-2pm; the City's own
    *Farmers Market Rules and Regs* PDF says 7 AM-3 PM.
  - Heart of the City Farmers' Market: the operator's About page says 7am-4pm; other pages on
    the same site say Sunday 7am-5pm / Wednesday 7am-5:30pm.
  - Castro Night Market: 5-9pm in some official/press listings, 5-10pm on the organizer's site
    and in SFMTA's advisory.
  - Chinatown Autumn Moon Festival: organizer says 11am-5pm, SFMTA's advisory says 11am-6pm.
- **Stale official pages.**
  - Haight Ashbury Street Fair's About page still says the fair is "held every second Sunday in
    June"; the 2026 fair was held Sunday, September 20, 2026.
  - sf.gov's Filipino American History Month page still lists the previous FilBookFest edition
    (October 12-13, theme "KAISÁ'T KASAMA") while sfpl.org lists October 17-18, 2026, theme
    "SANGGALAN".
  - Castro Street Fair, Union Street Festival, Pistahan, North Beach Festival and the Greek Food
    Festival pages still present 2026 content as current.
- **Edition numbers are not stable.** North Beach Festival is listed as both 70th and 71st for
  2026; the Autumn Moon Festival as both 35th and 36th.
- **Dates move after announcement.** The San Francisco Opera Ball was rescheduled from
  September 12 to November 12, 2026 because of orchestra labor negotiations; SF Ballet's site shows
  Nutcracker as both Dec 4-27 (2026-27 season) and Dec 5-28 (renewals page).
- **Schedules can be tentative.** MLB published the Giants' 2027 schedule as *tentative* pending
  labor negotiations, so the March 25, 2027 home opener may shift.

### 4. Third-party calendars are the main source of wrong "San Francisco" event lists

Four items were excluded after checking an official source:

| Item | What the official source says |
|---|---|
| How Weird Street Faire | howweird.org: "2000 — 2024 ... The Faire is done." Still listed as active by many calendars. |
| Ghirardelli Chocolate Festival | Not on Ghirardelli Square's own events page for 2026 or 2027; last documented edition was the 23rd in 2018. |
| Great Dickens Christmas Fair | Held at the Cow Palace in Daly City (San Mateo County), not in San Francisco. |
| Super Bowl LX, FIFA World Cup 2026 matches, 49ers games | Played at Levi's Stadium in Santa Clara. |

### 5. Geography is the most common false positive

Several of the biggest "SF" draws are held outside the City and County of San Francisco. A few
multi-venue festivals are San Francisco-based even where individual programme items are in
neighbouring cities — SFFILM, Frameline and Noise Pop all run venues in Berkeley and Oakland. Those
rows are kept, with the multi-venue fact stated on the row.

### 6. Source concentration

Verification used 43 distinct official domains. City sources (`sf.gov`, `sfrecpark.org`,
`sfmta.com`, `sfpl.org`, `sfport.com`) cover the civic and parks layer; organizer sites cover the
rest. Where a City page and an organizer page disagreed, the organizer page was treated as
authoritative for that event's own schedule and the disagreement was flagged rather than silently
resolved.

## Limits

This register is the set of events confirmable on an official page on 2026-10-18. It is not
exhaustive: smaller neighbourhood fairs, individual concert series, museum openings and library
programmes were not all reached. Adding them is additive — the schema in `data/events.json`
already supports it, and `tools/validate.py` will reject any row without an official source.
