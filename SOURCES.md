# Sources and verification method

**Research snapshot: 18 October 2026.** Read the [row-by-row evidence](sources.html) and [review register](review.html), rather than interpreting a successful URL request as fact verification.

## Evidence model

1. Preserved historical inputs are unverified candidates, not authoritative facts. The canonical projection has three additive, fail-closed entry overlays: session `3adf31d9`'s topic-gap entries (`data/audit_3adf31d9.json`), session `21f3dd85`'s free-first entries (`data/audit_21f3dd85.json`) and session `d57e2eeb`'s free-first gap entries (`data/audit_d57e2eeb.json`). Session `59f56c24`'s five official-calendar entries are already reconciled into the mainline audit. A final, scoped `06949148` evidence overlay applies one new exact admission quotation and adds review links for an unresolved hours conflict; it does not import an older register or approve Alemany's disputed time. The newer mainline `audit_f1fd3c36.json` and its tool are preserved unchanged and run only in an isolated candidate-history tree; their old labels never approve fields. Both upstream-added candidates and the 2026 Sketchfest reference remain available.
2. `data/audit_64f8b973.json` stores mainline official page/PDF text captures, request metadata, separately labeled selected retrieval-tool excerpts, structured event JSON-LD and explicit decisions. `data/audit_06949148.json` stores separate source excerpts for the final reconciliation; numeric HTTP status is left null when the retrieval tool does not expose one.
3. Every approved name, schedule, time, venue, admission condition, recurrence and normalized occurrence has supporting quotations. Geography records explain how the official event/venue is placed inside SF; unrelated footer/marketing city tokens are not acceptable.
4. The build starts factual fields blank and copies only approved decisions. Unknown fields stay blank and flagged. Name + venue + confirmed SF geography are required for directory admission; other candidates remain on Flagged for Review.
5. Exact substring checks establish quotation provenance, **not contextual applicability**. Editions, ticket eligibility, date conflicts and geography require recorded research judgment. JSON-LD is identified as structured evidence, not misrepresented as visible page text.
6. Only approved full ISO dates drive snapshot-relative temporal labels. No date parser invents a year from a URL slug, weekday, copyright, season header or unrelated event. Recurrence never generates future occurrences.

The public ledger contains **309 distinct cited URLs across 163 domains**. That is not a count of independent organizations, and a .org suffix does not establish nonprofit status.

## Topic-gap overlay (session `3adf31d9`)

The register originally had no AI/technology entries and only one dated gaming entry. Session
`3adf31d9` added **15** entries from official pages only, stored in `data/audit_3adf31d9.json`
and narrated in [the research log](data/research/audit-3adf31d9.md). The overlay is **additive and
fail-closed**: it runs after `tools/audited_register.py` and can only add capture-evidenced rows,
never approve or edit an existing field.

Two retrieval methods were used, and each capture records which one produced it:

* **`workspace fetch_page`** — the page body as returned by the fetch tool. Some pages returned more
  chunks than were read; those captures record `chunks_retrieved` / `chunks_total` and
  `complete: false`.
* **`workspace web_search`** — the **verbatim result text** the search tool returned for that exact
  official URL. Used where the event block is buried under navigation (sfpl.org puts it below three
  chunks of branch hours) or sits under the fetched fold (the Stern Grove contact block).

A search-snippet capture carries **no HTTP status**. It is evidence of what the tool returned for
that official URL on 18 October 2026, and it is never presented as a verified page fetch with a
200 response. The Sources page prints this distinction per source record.

Deliberate non-approvals, each of which left a value blank rather than plausible:

1. **Library admission is never assumed free.** Every SFPL chess, board-game and Chinese-chess entry
   leaves its price blank, because the official event text does not state admission. The Excelsior
   page's “Bright Knights Chess Club hosts free chess programs” describes the partner club's
   programmes, not this library session.
2. **Conference prices are not quoted on the pages read.** GDC, TDX, ICLR, Data + AI Summit and AI
   Engineer World's Fair each link to a registration or pricing page without stating a number. All
   five read **Not stated** — not “Paid”, and never a guessed ticket price.
3. **Mechanics' Institute Introduction to Chess is held for review.** The official page names the
   room and says “FREE for Mechanics’ Institute Members”, but the captured text never states a San
   Francisco address, so name + venue + city-only geography is not satisfied.
4. **AI Council 2027 is held for review** — San Francisco is named, but no venue is stated.
5. **ICLR 2027's venue is approved with a printed caveat.** The official Venue section still reads
   “Venue information will be posted here”; the value comes from that same page's venue image
   caption, “Moscone Center, San Francisco, CA”, and the caveat is shown in the row.
6. **GDC is not labelled annual.** The captured text dates the 2027 edition without saying the
   festival repeats, so its cadence is *Special*.
7. **Stern Grove carries no occurrence date.** The official pages support an annual cadence
   (“since 1938”, “Every summer”) but no 2027 season dates were published on them.

## Free-first overlay (session `21f3dd85`)

The topic-gap pass left only one free gaming entry, no dated free gaming or AI entry, and few
dated free music entries. Session `21f3dd85` added **8** candidates from official pages only,
stored in `data/audit_21f3dd85.json` and narrated in [the research log](data/research/audit-21f3dd85.md):
six listed (five free, one paid for the separate Paid section) and two held for review. The
overlay is additive and fail-closed and runs after `tools/register_3adf31d9.py`.

Retrieval honesty: this session's fetch tool does not report an HTTP status code and families run
through shims that can inject non-content text, so **no capture in this pass claims an HTTP 200**;
each stores `http: null` with its retrieval method (`tool_fetch` for page-body reads, `tool_excerpt`
for verbatim search-tool text tied to the exact official URL), following the honesty rules the
topic-gap pass set for snippets. Verified HTTP status still comes only from the CI reachability
check.

Evidence judgments specific to this pass:

1. **SFPL's all-programs sentence is quoted as the admission text for new SFPL rows only.** For its
   two new library entries, the pass approves the verbatim sentence *"All programs and events are
   free and open to the public"* from the official SFPL events index (sfpl.org/events) — the
   organizer's own policy statement governing those programs, shown unedited in the row (see the
   research log). The topic-gap pass did not have that quote and left its library prices blank;
   those rows are **unchanged** — additivity forbids copying the value onto them. "Library-held,
   therefore presumably free" is still never used; only the quoted sentence is.
2. **Yearless dates stay dateless.** The Mechanics' Institute Chess Socials list ("Nov 6, Dec 4")
   carries no year, so the row is listed as a monthly pattern with zero ISO occurrences.
3. **A title is never invented.** The Internet Archive's free Friday tours are evidenced for
   schedule, time, venue and cost, but archive.org gives the programme no title, so the candidate
   is held for review under its inherited identifier.
4. **Conflicting admission terms stay blank.** Grace Cathedral's official pages say both "free
   organ recital" and that unregistered Sunday visitors pay, so the Organ Recital Series is held
   for review with price blank; no side of the contradiction is quoted as the answer.
5. **The held Introduction to Chess row is not duplicated.** The classes page now evidences its
   venue ("Onsite in the Chess Room at Mechanics'…"), but overlays may not edit earlier rows; the
   new evidence is logged for a future integration session. Its free status remains members-only.

## Free-first gap overlay (session `d57e2eeb`)

The additional 21 candidates and their exact first-party citations are recorded in
[`data/audit_d57e2eeb.json`](data/audit_d57e2eeb.json) and the linked
[research log](data/research/audit-d57e2eeb.md). The pass covers free civic venues and Golden
Gate Park garden hours, music, gaming and SF AI/technology communities, plus one explicitly paid
Circus Bella event kept in the separate Paid section. Its six official-page inconsistencies and
five search-tool excerpts are labeled and retained; no retrieved text is treated as a numeric HTTP
200 when the tool did not expose one.

## T32 stale-branch reconciliation (session `06949148`)

The remote `arena/95ceac65-maltaproj5` branch had three commits, but its final snapshot was
three commits ahead and 38 behind current `main`, with 246 candidates and an older 12-page
site. Its generated outputs and replacement validator would regress the current 295-candidate,
19-page site, so they were not copied. The branch's research log reports a risk-prioritized
sample of roughly 60 live pages; this takeover did **not** re-audit that sample or the whole
register. It independently re-read the two proposed changes using the official pages below.

- **Oktoberfest on Front:** Downtown SF's official event page says **“FREE WITH RSVP”** at
  https://downtownsf.org/things-to-do/oktoberfest-on-front. That exact wording now fills the
  previously blank price field. The event's already-confirmed 18 September 2026 date is past at
  this fixed snapshot, so it is not added to the free-upcoming dashboard.
- **Alemany Farmers Market:** the current SF.gov page
  (https://www.sf.gov/location--alemany-farmers-market) and Foodwise operator page
  (https://foodwise.org/markets/alemany-farmers-market/) both state Saturday 7am–2pm; SF.gov
  says Foodwise has operated the market since February 2026. The San Francisco Environment
  Department page (https://www.sfenvironment.org/farmers-markets-in-sf), dated 21 March 2025,
  states 6:00am–3:00pm and advises readers to confirm with the individual market website. The
  field remains blank and all three official links are attached to the row and the review finding.
  Admission remains blank: free parking is not evidence of free entrance.

The supplement records exact excerpts, the retrieval method and `http: null` because the
retrieval tool did not expose a numeric status. These are limited, source-specific decisions,
not a claim that the full register was freshly semantically re-verified.

## Representative official pages and scope

- Foodwise: https://foodwise.org/markets/ferry-plaza-farmers-market/ and https://foodwise.org/markets/mission-community-market/ — operator schedules/venues; not blanket proof of free admission.
- SF government, market operator and Environment Department: https://www.sf.gov/location--alemany-farmers-market, https://foodwise.org/markets/alemany-farmers-market/ and https://www.sfenvironment.org/farmers-markets-in-sf — the current SF.gov/Foodwise pages say 7am–2pm, while the 21 March 2025 Environment Department page says 6am–3pm and directs visitors to confirm with the individual market. The time remains blank and all three are linked for review.
- PCFMA: https://www.pcfma.org/market/castro-farmers-market and other direct market pages — operator-specific weekly schedules, not shared finder-page token matches.
- Exploratorium: https://www.exploratorium.edu/visit/calendar/after-dark and https://www.exploratorium.edu/visit — Thursday series, themed 2026 dates, Pier 15 and the general After Dark price/age policy. Individual-theme surcharges are not inferred.
- FAMSF: https://www.famsf.org/visit/free-reduced-admission — conditional free general admission. Permanent galleries, residency and Bouquets to Art exceptions remain attached; special exhibitions are not automatically free.
- Zoo: https://www.sfzoo.org/event/sf-resident-free-day/ and https://www.sfzoo.org/event/boo-at-the-zoo/ — direct event pages supersede conflicting calendar-widget times. Specific dates do not establish monthly/weekly recurrence.
- Presidio Trust: https://presidio.gov/about/press/presidio-unveils-vibrant-2026-summer-event-lineup — dated 2026 event blocks. Unmentioned Picnic/Twilight/Habitat Stewards schedules are not substantiated by this release.
- Opera: https://www.sfopera.com/operaball — current November 12 postponement supersedes the February season announcement’s September gala date.
- Bhangra & Beats: https://www.bhangraandbeats.com/ — two 2026 dates and new Yerba Buena venues; no stale Clay/Battery carryover.
- Pride: https://sfpride.org/ and https://sfpride.org/events/ — 2027 combined weekend versus 2026 event details are kept distinct.
- SFMOMA: https://www.sfmoma.org/exhibitions/ and https://www.sfmoma.org/exhibition/rm-x-sfmoma/ — exhibition/dated event blocks, explicit event JSON-LD address, and additional RM surcharge rather than a falsely low total ticket price.
- YBG Festival: https://ybgfestival.org/ and https://ybgfestival.org/visitor-info/ — current calendar plus explicit SF gardens geography. New Halloween/jazz entries use the 2026 calendar context, not an inferred year.
- Noontime Concerts: https://noontimeconcerts.org/ and https://noontimeconcerts.org/about-noontime-concerts/ — free weekly Tuesday concerts with dated fall 2026 performances and a not-ticketed/donation admission note.
- National Park Service: https://www.nps.gov/planyourvisit/event-details.htm?id=2B52B414-F0EF-9707-2656479F9CAE0CBD — dated official Sea Chantey Sing event page (free, monthly cadence, Maritime Museum address).
- Mechanics' Institute: https://www.milibrary.org/chess/chess-classes/ and https://www.milibrary.org/chess/tournaments/2026-winter-tuesday-night-marathon — free monthly chess socials (yearless dates left dateless) and a priced tournament with exact member/non-member entry fees.
- SFPL: https://sfpl.org/teens/the-mix/gaming and https://sfpl.org/releases/2026/04/24/level-tech-week-san-francisco-public-library — monthly gaming tournaments at The Mix and the annual free Tech Week with named AI sessions; admission for the two new library rows quotes the events index's all-programs-free sentence verbatim.

Every other candidate retains its own official links and approved/blank fields in the HTML evidence page and JSON decision ledger.

## Reachability is a separate question

`tools/check_sources.py` reports HTTP reachability, not event identity or facts. 404/410 are definite dead-page findings; 202/403/405/429, server errors and transport/TLS failures stay explicitly restricted/unknown. Selected successful retrieval-tool reads can coexist with a blocked runner status; the two are not conflated.

Capture refreshes do not erase prior readable evidence on failure, and adjudicated captures are immutable. Later request metadata is separate. Capture/reachability workflows now publish artifacts instead of bot-editing factual fields. The old shared-source matcher report remains historical evidence of an attempted machine check, not a current verification credential.

## Reproduce

```sh
python3 tools/consolidate.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 scripts/validate.py
```

For URL outcomes on an internet-capable runner:

```sh
python3 tools/check_sources.py --timeout 20 --output /tmp/source-links.json
```

No claim of exhaustive city coverage, continuous re-verification, live availability or full semantic certainty is made. All unresolved candidates and known coverage gaps are published, not silently discarded.
