# Independent verification + free-first gap research — session `9d0b6c49`

Date: **18 October 2026** (the register's fixed snapshot). Tasks T-9d0b-1 (line-by-line
re-verification of the published register) and T-9d0b-2 (additive free-first gap research).

**Method.** Official pages were read with the Arena workspace `fetch_page` tool, or with
`web_search` where a page answers a direct fetch with a bot challenge. Every quotation below is
text the tool actually returned on this date; nothing is recalled from memory and nothing is
inherited from an earlier session's notes. `fetch_page` reports success but **no HTTP status
code**, so every capture in `data/audit_9d0b6c49.json` records `http: null` and labels its
retrieval method. Bulk URL reachability is a CI gate (`tools/check_sources.py`), not a claim
made here.

**Scope honesty.** This is a targeted re-verification of the rows that lead the site plus the
whole priced section, **not** a fresh semantic audit of all 299 candidates, and **not** a claim
of citywide completeness. Structural checks (exact projection, quotation provenance, blanks,
CSV values, page membership, local links) are run by `scripts/validate.py`; they prove the data
matches its archived evidence, never that the evidence is true.

---

## Part 1 — Line-by-line re-verification of the free-first landing rows

Every row that led the landing page before this pass was re-read against its own cited official
URL. "Confirmed" means each published value's exact wording was found on that page today.

| # | Row | Official source re-read | Values re-read | Result |
|---|---|---|---|---|
| 1 | `h-choral-evensong` — Choral Evensong (Grace Cathedral) | [gracecathedral.org/series/choral-evensong/](https://gracecathedral.org/series/choral-evensong/) | name, schedule, time, venue, price, 5 occurrences | **Confirmed.** Page still reads "Evensong is free and is offered at Grace Cathedral every Thursday at 5:30 p.m." and "(45 minutes)". Calendar still lists Oct 18, Oct 22, Oct 25, Oct 29 and Nov 1 2026. **Conflict still present:** the Sunday widget prints "4:55PM-4:55PM" against Thursday prose — see irregularity A. |
| 2 | `f-noontime-concerts` — Noontime Concerts | [noontimeconcerts.org](https://noontimeconcerts.org/) | name, schedule, time, venue, price, 3 occurrences | **Confirmed.** "Free Live Concert Every Tuesday", "Old St. Mary's Cathedral", 10/20/2026 NCCO Quartet, 10/27/2026 Berkelium Quartet, 11/10/2026 Angela Lee & Marc Teicholz. See irregularity B on the 12:30 pm wording. |
| 3 | `h-noontime-concerts` — Noontime Concerts (companion record) | [noontimeconcerts.org](https://noontimeconcerts.org/) | name, schedule, time, venue incl. "660 California Street", price, 3 occurrences | **Confirmed.** Same page, same three dates. Duplication with row 2 is a known, published overlap, not two unique events. |
| 4 | `audit-ybg-afro-filipino-jazz` — Afro-Filipino Jazz Project | [ybgfestival.org](https://ybgfestival.org/) (challenge) → verbatim text for that exact official URL, plus [ybgfestival.org/event/afro-filipino-jazz-project/](https://ybgfestival.org/event/afro-filipino-jazz-project/) | date "Sat, Oct 24", time 2:00pm – 3:30pm, venue, "admission-free performances" | **Confirmed, with a retrieval caveat.** The homepage now returns "reCAPTCHA / Recaptcha requires verification" to a direct fetch, so the cited text was re-read through the search tool's verbatim result for that exact URL. The organizer's own event page adds a **more precise venue**: "Great Lawn, Yerba Buena Gardens / Mission St. between 3rd & 4th Sts. / San Francisco, CA" and "Free RSVP". Published cell left untouched (already supported) — see irregularity C. |
| 5 | `b-lit-crawl` — Lit Crawl SF | [litquake.org/litcrawl](https://www.litquake.org/litcrawl) | "OCTOBER 24, 2026", "San Francisco's Mission District", "free pop-up literary event" | **Confirmed.** All three strings present verbatim. Time stays blank — see irregularity D. |
| 6 | `family` — Free Family Day: K-Pop, Art, and Beyond | [sfmoma.org/event/free-family-day-k-pop-art-and-beyond/](https://www.sfmoma.org/event/free-family-day-k-pop-art-and-beyond/) | "Sunday, Oct 25, 2026", "10 a.m.–4 p.m.", the two-adults-free sentence | **Confirmed**, but the page carries conditions the published cell does not — see irregularity E. |
| 7 | `b-scaregrove` — Scaregrove Halloween Event | [sfrecpark.org/Calendar.aspx](https://sfrecpark.org/Calendar.aspx) | "October 30, 2026, 3:00 PM - 9:00 PM @ Sigmund Stern Grove", "Free Halloween fun for the entire family!", "Sigmund Stern Grove", "19th Avenue and Sloat Boulevard San Francisco CA 94132" | **Confirmed** via verbatim text for that exact official URL. The same City calendar also lists two sibling entries that day — "Mobile Rec at Scaregrove, 12:00 PM - 8:00 PM" and "Volunteer at Scaregrove, 3:00 PM - 9:00 PM" — not separate public events, so no rows were added. |
| 8 | `audit-ybg-halloween-hoopla` — Halloween Hoopla | [ybgfestival.org](https://ybgfestival.org/) (challenge) → verbatim text, plus [ybgfestival.org/event/halloween-hoopla-2026/](https://ybgfestival.org/event/halloween-hoopla-2026/) (fetched directly) | "Sat, Oct 31", 12:00pm – 3:00pm, venue, "admission-free performances" | **Confirmed.** The event page fetched cleanly and prints "Sat, Oct 31, 12:00pm – 3:00pm", "Venue: Children's Garden, Yerba Buena Gardens", "799 Howard St. / San Francisco, CA", "Free RSVP", "The 26th annual Halloween Hoopla". Published venue cell left as-is — see irregularity C. |
| 9 | `b-downtown-first-thursdays` — Downtown First Thursdays | [dftsf.com](https://www.dftsf.com/) | "NOV 5, 2026", "Free w/ RSVP", "2nd St. between Market and Howard in SF", "5-10PM" | **Confirmed.** All four strings present verbatim on the organizer's homepage. |
| 10 | `x-bhangra-and-beats-night-market` — Bhangra & Beats | [bhangraandbeats.com](https://www.bhangraandbeats.com/) | "BHANGRA & BEATS IS BACK FOR 2026!", "two Fridays—July 24 and November 13 (Diwali edition)", "4pm–9pm", "Yerba Buena Gardens, Jessie Square, and Yerba Buena Lane", "FREE event" | **Confirmed.** Page also prints a dated block "FRIDAY NOV, 13th / DOWNTOWN SAN FRANCISCO / YERBA BUENA GARDENS \| JESSIE SQUARE / YERBA BUENA LANE / PRICE: FREE / TIME: 4 PM - 9 PM / ALL AGES". The 24 July instance is past relative to the snapshot and is retained as history; only 13 November drives the upcoming label. |
| 11 | `x-sfmoma-sarah-sze` — Sarah Sze: Forever is Composed of Nows | [sfmoma.org/exhibitions/](https://www.sfmoma.org/exhibitions/), plus [sfmoma.org/exhibition/sarah-sze/](https://www.sfmoma.org/exhibition/sarah-sze/) and [sfmoma.org/upcoming-exhibitions/](https://www.sfmoma.org/upcoming-exhibitions/) | "Opening November 21, 2026", "free to see", venue | **Confirmed.** The listings read "Floor 1 · free to see · Sarah Sze: Forever is Composed of Nows · Opening November 21, 2026". The dedicated page adds "The public can access this exhibition for free in the Evelyn and Walter Haas, Jr. Atrium on Floor 1" and "November 21, 2026–ongoing", consistent with the open-ended occurrence. Floor/atrium detail **not** written into the venue cell: the published value is already supported and no field is edited for style. |
| 12 | `x-lets-glow-sf` — Let's Glow SF | [downtownsf.org/things-to-do/lets-glow-sf](https://downtownsf.org/things-to-do/lets-glow-sf) | "December 4-13, 2026", "Downtown's architectural icons", "free, family-friendly celebration" | **Confirmed.** Page reads "return to San Francisco from December 4-13, 2026, for its sixth year". A "Locations" block lists buildings and addresses, but the same page says "Artist information, event map, audio walking tour, and business specials coming soon!" and its news items are all dated 2025, so **no year is attached to that locations list**; it was not adopted. Time stays blank — no 2026 projection hours are printed. |
| 13 | `f-sea-chantey-sing` — Sea Chantey Sing | [nps.gov event details](https://www.nps.gov/planyourvisit/event-details.htm?id=2B52B414-F0EF-9707-2656479F9CAE0CBD) | "Dec 5, 2026", "6:00 PM", "This event is free to attend.", "first Saturday of every month in the Maritime Museum" | **Confirmed.** US government source. Page also prints "Duration: 3 hours" and the fuller venue "Maritime Museum, 900 Beach St, San Francisco, CA 94109"; the published venue cell ("Maritime Museum") is already supported and was not restyled. |
| 14 | `holiday` — Sunset Holiday Mercantile | [sunsetmercantilesf.com/sunsetholidaymercantile/](https://sunsetmercantilesf.com/sunsetholidaymercantile/) | "Sunset Holiday Mercantile in 2026", "Saturday, December 5 and Sunday, December 6", "11am–5pm", "SF County Fair Building in Golden Gate Park", "Free admission" | **Confirmed.** All five strings present verbatim. |
| 15 | `carnaval` — Carnaval SF | [carnavalsanfrancisco.org](https://carnavalsanfrancisco.org/) | "May 29–30, 2027", "San Francisco's Mission District", "FREE 2–day family festival & Grand Parade" | **Confirmed.** Page also prints "Broadcasting Sunday, May 30, 2027" for the Grand Parade live stream, which is consistent with the 29–30 span. Cadence stays Special: the organizer's copy says "Now in its fourth decade of celebration" and "Forty-nine years", which is edition history, not an explicit recurring-cadence sentence — and this register does not infer cadence from edition history. Note the site also sells **Grand Stand / premier parade seating**; the festival and parade themselves remain free, so the published free wording is correct and no paid row was created from a seating upgrade. |

### Paid section rows re-read against official pages

| Row | Official source | Result |
|---|---|---|
| `x-giants-fanfest` — Open House at Oracle Park | [mlb.com/giants/fans/fanfest](https://www.mlb.com/giants/fans/fanfest) | **Badge was wrong — corrected to Free.** Page reads "Free tickets are required for all FanFest Tour stops and the Open House." and separately "The **free tour** will include current Giants players…". No price appears anywhere on the page. It also says "Please check back soon for 2027 information", so the row correctly carries no confirmed date. Only the Oracle Park Open House is SF-verifiable; the three Northern California tour cities are not named on the page, so no tour row was added. |
| `chinese` — SF Chinese New Year Parade | [chineseparade.com/faq/](https://chineseparade.com/faq/) | **Badge was wrong — corrected to Free.** Page reads "will be on **Saturday, February 20, 2027** and starts at 5:15 PM from 2nd and Market St. It is a free event for all to attend but tickets must be purchased to sit in the bleacher sections." and "The parade is a free event for all to attend and you may stand anywhere on the parade route, behind the barricades, to watch the parade." Bleacher seating is an optional purchase, not entry. Published date, time and venue cells already match this page. |
| `x-asian-art-museum-free-sundays` — Free First Sunday | [about.asianart.org/ticketing/free-and-reduced-museum-admission/](https://about.asianart.org/ticketing/free-and-reduced-museum-admission/) | **Badge was wrong — corrected to Free.** Page reads "On the first Sunday of each month, general admission is free and tickets to our special exhibitions are offered at a discounted price of $15." The $15 buys an optional special-exhibition upgrade. Venue address "200 Larkin Street, San Francisco, CA 94102" also confirmed on the same page. |
| `sf-zoo-boo` — Boo at the Zoo | quoted wording "activities are free with paid daytime admission or Zoo membership." | **Badge stays Paid, correctly.** Entry requires paid daytime admission or membership; the free wording covers the activities only. |
| `after-dark`, `x-sfmoma-rm-x-sfmoma`, `x-the-haunt-ybca`, `h-bravura-circus-bella` | quoted wording re-checked against the register's own archived captures | **Badges stay Paid, correctly.** In each case the free wording applies only to a subset (members, children 2 and under, kids 12 and under) or only after paying, so entry itself costs money. |

Net effect of the badge correction: **Free 75 → 78, Paid 20 → 17, Not stated 117 unchanged**;
free upcoming landing rows **15 → 16** (the Chinese New Year Parade, 20 February 2027). No
curated field value was edited — the badge is a label over the verified admission wording.

---

## Part 2 — Irregularities found and published (none silently reconciled)

**A. Grace Cathedral Choral Evensong prints two different times for the same series.**
The Thursday prose says "every Thursday at 5:30 p.m."; the Sunday 18 October 2026 calendar widget
prints "4:55PM-4:55PM" — a zero-length range. The register keeps `5:30 p.m. (45 minutes)` from the
Thursday sentence and leaves the Sunday time blank rather than applying the Thursday time to a
Sunday occurrence. Still unresolved on the official page as of today.
[Source](https://gracecathedral.org/series/choral-evensong/)

**B. Noontime Concerts' 12:30 pm is the live-stream start time.** The homepage says
"Live Stream Starts at 12:30PM" directly above "or attend in person at Old St. Mary's Cathedral",
and "We live stream a 45-minute concert featuring amazing musicians every Tuesday at 12:30 pm PST."
No separate in-person start time is printed. The published `12:30 pm` is therefore supported by the
page but describes the broadcast; this is recorded here so a reader is not misled. The same page
sells "Pay-Per-View" recordings — a separate offer, not live-concert admission, so the free badge
is correct. [Source](https://noontimeconcerts.org/)

**C. ybgfestival.org now answers a direct fetch with a reCAPTCHA challenge, and its event pages
name a more precise venue than the published cells.** "Recaptcha requires verification. protected
by reCAPTCHA" is the whole homepage body returned to the fetch tool. The two published rows cite
that homepage and remain supported through the search tool's verbatim text for the same URL, but a
manual reviewer should prefer the event pages: [Afro-Filipino Jazz Project](https://ybgfestival.org/event/afro-filipino-jazz-project/)
("Great Lawn, Yerba Buena Gardens / Mission St. between 3rd & 4th Sts.") and
[Halloween Hoopla](https://ybgfestival.org/event/halloween-hoopla-2026/) ("Children's Garden, Yerba
Buena Gardens / 799 Howard St."). Neither published venue cell was edited: both are already
supported by the cited page, and restyling a supported value is not a correction.

**D. Lit Crawl's printed programme time has ambiguous scope, so the time cell stays blank.** The
page lists three events whose venues changed since the map was printed, then reads "all programs
from 6:30—7:30 PM". It is not stated whether that applies to the whole crawl or only to those three
relocated programmes. `tests/test_audited_register.py` already pins this cell to blank; this pass
leaves it blank and records the reason. [Source](https://www.litquake.org/litcrawl)

**E. SFMOMA Free Family Day is free, but the official page attaches conditions the published cell
does not carry.** The page states "Free with RSVP. Early RSVP is encouraged — this event may reach
capacity.", "Family Free Day tickets grant you free access to the entire museum, with the
**exception** of _RM x SFMOMA: Between You and Me_, which requires a timed ticket", and
"_RM x SFMOMA: Between You and Me_ requires a timed entry with a surcharge of $12 for adults;
children 18 and younger are always free but also need a reserved timed ticket". The published
admission cell quotes only "Free Family Day provides free access to two adults when accompanied by
a child 18 or younger." The **Free** badge is right; the RSVP requirement and the $12 exception are
published here for manual review rather than written into a cell owned by an earlier audit.
[Source](https://www.sfmoma.org/event/free-family-day-k-pop-art-and-beyond/)

**F. A published review finding describes a reclassification the register does not carry.**
`tools/consolidate.py` records that "the Chinese New Year Parade and Carnaval rows filed as
'Special' even though both are annual editions (moved to Annual)". The final audited register keeps
**both rows as `Special`**, because `data/audit_64f8b973.json` decides `kind: "Special"` for each
with the explicit reason "Recurrence not inferred from edition history" — and the audited decision
is the last projection step, so it wins. The register is internally consistent and evidence-driven;
the older consolidation note is the stale artefact. No row was changed. Both organizers' pages were
re-read today: [chineseparade.com/faq/](https://chineseparade.com/faq/) prints only a single dated
edition, and [carnavalsanfrancisco.org](https://carnavalsanfrancisco.org/) prints edition history
rather than a cadence sentence.

**G. Noisebridge-hosted gaming/dev events are held off the register, not published.** The
organizer's own pages conflict on both weekday and time: [noisebridge.net/wiki/Tour](https://www.noisebridge.net/wiki/Tour)
says "Gamebridge Unityversity is taught here, Tuesdays @ 7pm"; the class organiser's page
[gamebridgeu.wordpress.com/category/classes/](https://gamebridgeu.wordpress.com/category/classes/)
says "WHEN: 6-8PM PST Wedesdays" (sic) for Gamebridge and "Wednesdays 5-6PM" for Artbridge; the
meetup listing text says "WHEN: 7-9ish PM PST Wednesdays". A related Noisebridge page,
"Showcase Showdown", states "COST: **FREE!**" and "2nd and 4th Fridays … at 7pm-12am" but only via
a third-party listing. Current local reporting also questions whether the venue at 272 Capp Street
will continue to operate. Because cadence, time and venue continuity cannot all be confirmed from
one official page, **no row was created**; the conflict is logged here instead. The register's
existing Noisebridge rows are unchanged by this pass.

---

## Part 3 — New free entries added (T-9d0b-2)

Four free, city-of-San-Francisco entries the earlier registers did not cover, added by the
fail-closed overlay `tools/register_9d0b6c49.py` from `data/audit_9d0b6c49.json`. No existing row
or audit file was edited.

| New row | Topic | Cadence | Confirmed dates | Official sources |
|---|---|---|---|---|
| `i-chess-mahjong-un-plaza` — **Chess and Mahjong** | **Gaming** | Weekly (Fridays) | 2026-10-23 | [City Recreation & Parks UN Plaza calendar](https://www.sfrecpark.org/Calendar.aspx?CID=40) · [City event detail page](https://sfrecpark.org/Calendar.aspx?EID=10596&month=9&year=2026&day=3&calType=0) · [Civic Center CBD](https://sfciviccenter.org/event/learn-and-play-chess-at-un-plaza/) |
| `i-rae-studios-dance-fitness` — **Free Dance Fitness Class by Rae Studios** | Other | Special (dated, cadence not stated) | 2026-10-18 … 2026-10-29 (11 dated instances) | [City Recreation & Parks UN Plaza calendar](https://www.sfrecpark.org/Calendar.aspx?CID=40) |
| `i-cmc-halloween-party` — **CMC Halloween Party & Costume Parade** | **Music** | Special | 2026-10-28 | [sfcmc.org/events/](https://sfcmc.org/events/) |
| `i-cmc-baroque-cinema` — **From Baroque to Cinema** | **Music** | Special | 2026-11-08 | [sfcmc.org/events/](https://sfcmc.org/events/) |

Evidence notes:

* **Chess and Mahjong** is the register's first **free Gaming entry with a confirmed upcoming
  date**, which fills the dashboard callout that previously read "Gaming: no free entry with a
  confirmed date yet". Admission comes from the City's own event-detail field `Cost: Free` and from
  the district page's "Free, drop-in."; the weekly cadence comes from the district page's own
  sentence "taking place at UN Plaza every Friday, 2-5pm" and "the weekly event" — never from
  counting calendar entries. Only the 23 October instance is approved as upcoming, because the
  detail page reached directly (EID=10596) shows 18 September 2026, which is past. The two official
  pages attribute the free lessons differently (the City lists the programme plainly; the district
  says the lessons come "from the Mechanics' Institute"); both are quoted and no single organizer is
  asserted.
* **Rae Studios** carries **no time value on purpose**. The City calendar prints a different start
  time per date (10:00 AM - 11:00 AM, 11:00 AM - 12:00 PM and 5:30 PM - 6:30 PM instances all
  appear, and 24 and 25 October each carry two), so collapsing them into one cell would invent a
  value. The page returned two chunks and only the first was read, so no date beyond 29 October is
  claimed and `retrieval.complete` is `false` in the capture.
* **Both CMC concerts** are listed as `Cost: Free` on the organizer's own events page. Their
  verified names contain no music word, so `Music` is an **explicit editorial topic decision**
  justified by the same page's own descriptions ("our annual Halloween Spooktacular of fun and
  music! Featuring a showcase from CMC students from including Children's Chorus…"; "Journey through
  three centuries of music with CMC faculty celebrating the unique beauty of the piano trio"). The
  Halloween listing truncates its own description at "Free (bring a small snack or \[…\]", so any
  further condition is unconfirmed and is not restated. From Baroque to Cinema pairs "Cost: Free"
  with an Eventbrite **RSVP** link; no ticket price is printed, so the RSVP is recorded as a note,
  not converted into a charge.

### Open research items for a future session (logged, not filled)

* A free **AI & technology** entry with a confirmed upcoming date. The AI section still has only one
  free entry (`Tech Week`, SFPL) and no dated one; SFPL's explicitly dated AI and gaming instances
  are past relative to this snapshot. No candidate was published from a third-party meetup listing.
* `sfciviccenter.org` also lists "UN Plaza Fitness Classes: Dance, Cardio & More" and other plaza
  programmes; only the two series whose official pages were read end-to-end this pass were added.
* The second chunk of the City UN Plaza calendar (dates after 29 October 2026) was not read.
* The full condition text behind SFMOMA's truncated CMC Halloween description, and the SFMOMA Free
  Family Day RSVP / $12 exception, need a row-level edit by a session owning
  `data/audit_64f8b973.json` or a future supplement mechanism.

---

## Part 4 — Requirement conformance re-check against the brief

| Requirement | State after this pass | Where |
|---|---|---|
| Mobile friendly | Met. `<meta name="viewport">` on all 19 pages (asserted by `scripts/validate.py`), card layout below 820 px, no horizontal overflow asserted by the browser smoke test. | `assets/style.css`, `tests/browser_smoke.cjs` |
| Organized by date, upcoming highlighted first | Met. Upcoming page is nearest-first across all dated rows and this is asserted, not assumed; landing rows in the next 14 days are highlighted. | `upcoming.html`, `index.html` |
| Executive summary of upcoming events near today | Met, and now free-only and dated-only: 20 free upcoming entries, soonest first, with per-topic nearest-free callouts. | `index.html#executive-summary` |
| Cost clearly labelled | **Corrected this pass.** Free / Paid / **Not stated** badge derived only from the verified admission wording, with the exact official sentence always printed beside it, and a "Conditions apply" qualifier wherever money or a restriction is mentioned. Three mislabelled rows fixed. | every events table, `paid.html` |
| Free events for gaming, music, AI first, then everything else | Met. Focus, free and landing ordering is Gaming → Music → AI & technology → Other, asserted by the validator. | `focus.html`, `free.html` |
| Only free events in the main section; paid collected separately | Met and now stricter: the landing main section is Free ∩ confirmed date only; 17 priced entries live on their own page; "Not stated" is never shown as paid. | `index.html`, `paid.html` |
| Recurring vs special events separated | Met: 38 weekly / 13 monthly / 35 annual / 130 special-or-cadence-unconfirmed, each on its own page, and a recurring pattern never generates a next date. | `weekly.html`, `monthly.html`, `annual.html`, `special.html` |
| San Francisco city only | Met: every listed row needs confirmed SF geography from an official page; 83 candidates are held off the directory, including regional/mixed-city programmes. | `review.html` |
| Full list of events | **Bounded, and stated as bounded.** 216 directory entries from 299 assessed candidates. Official web visibility biases the sample toward larger institutions; this is not a live city calendar and no citywide completeness claim is made. | `analysis.html`, `focus.html` |
| Every row has an official source link | Met and enforced: the validator fails if any events-table row lacks a direct HTTPS official source that appears in that row's own source ledger. | `scripts/validate.py`, `sources.html` |
| Unconfirmed values blank and flagged | Met: 117 admission cells, 89 time cells and 15 schedule cells are blank with explicit "unverified" notes; nothing is inferred. | `sources.html`, `review.html` |
