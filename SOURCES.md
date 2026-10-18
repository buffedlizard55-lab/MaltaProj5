# Sources and verification method

**Research snapshot: 18 October 2026.** Read the [row-by-row evidence](sources.html) and [review register](review.html), rather than interpreting a successful URL request as fact verification.

## Evidence model

1. Preserved historical inputs are unverified candidates, not authoritative facts. The newer mainline `audit_f1fd3c36.json` and its tool are preserved unchanged and run only in an isolated candidate-history tree; their old labels never approve fields. Both upstream-added candidates and the 2026 Sketchfest reference remain available.
2. `data/audit_64f8b973.json` stores finite official page/PDF text captures, request metadata, separately labeled selected retrieval-tool excerpts, structured event JSON-LD and explicit decisions.
3. Every approved name, schedule, time, venue, admission condition, recurrence and normalized occurrence has supporting quotations. Geography records explain how the official event/venue is placed inside SF; unrelated footer/marketing city tokens are not acceptable.
4. The build starts factual fields blank and copies only approved decisions. Unknown fields stay blank and flagged. Name + venue + confirmed SF geography are required for directory admission; other candidates remain on Flagged for Review.
5. Exact substring checks establish quotation provenance, **not contextual applicability**. Editions, ticket eligibility, date conflicts and geography require recorded research judgment. JSON-LD is identified as structured evidence, not misrepresented as visible page text.
6. Only approved full ISO dates drive snapshot-relative temporal labels. No date parser invents a year from a URL slug, weekday, copyright, season header or unrelated event. Recurrence never generates future occurrences.

The public ledger contains **258 distinct cited URLs across 150 domains**. That is not a count of independent organizations, and a .org suffix does not establish nonprofit status.

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

## Representative official pages and scope

- Foodwise: https://foodwise.org/markets/ferry-plaza-farmers-market/ and https://foodwise.org/markets/mission-community-market/ — operator schedules/venues; not blanket proof of free admission.
- SF government: https://www.sf.gov/location--alemany-farmers-market — updated operator/hours; conflict with the older City Environment listing is retained, with time blank.
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
