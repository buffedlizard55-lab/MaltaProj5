# Research record — session `d57e2eeb` (T37, free-first gap research)

**Snapshot date:** 2026-10-18 (fixed, matching the project's fixed "today") · **Session branch:** `arena/d57e2eeb-maltaproj5` · **Task:** T37 on the coordination board.

## What was done

The user requirement priorities are **free first, then gaming / music / AI, then everything else**. I read the current register (`data/events.json`, 266 candidates / 185 listed) line by line to identify coverage gaps, then researched **new** official-source entries — never editing an existing row (the register is extended only additively). Every field value in `data/audit_d57e2eeb.json` is an exact quotation from text the workspace tools returned on 2026-10-18; unconfirmed values are left blank and flagged as unverified.

### Gap analysis (what the 185-row listed register did *not* cover before this pass)

- Free-always civic venues: Cable Car Museum, Randall Museum, San Francisco Railway Museum, Fort Point NHS, Presidio Officers' Club exhibitions, Musée Mécanique (all absent).
- Golden Gate Park garden free times: Japanese Tea Garden free M/W/F hour, Conservatory of Flowers free first Tuesdays, SF Botanical Garden free daily early entry / second Tuesdays (absent — the register carried de Young / Legion / Asian Art Museum free days only).
- Free music beyond the major festivals: Noontime Concerts (weekly, Old St. Mary's), Grace Cathedral's free Choral Evensong, People in Plazas (annual downtown series). Already present and not duplicated: Golden Gate Park Band, Illuminate LIVE / Civic Center Soundtrack, Yerba Buena Gardens Festival, Stern Grove, Hardly Strictly Bluegrass, Valencia LIVE, Opera in the Park, SF Free Folk Festival.
- Gaming: the register had SFPL game sessions, chess programmes, GDC and the Pokémon World Championships. Added: Gamescape's weekly Board Game Night and Musée Mécanique (free-admission arcade museum, price unverified → "Not stated").
- AI/technology: the register had conferences (AI Engineer, TDX, ICLR, Data + AI, Cloudflare, Microsoft Ignite) with every price "Not stated". Added the two recurring free-community AI channels active in SF: AI Tinkerers SF and The AI Collective SF chapter, plus Noisebridge's weekly Circuit Hacking Mondays and monthly Five Minutes of Fame (prices not stated on the official wiki → blank).
- One explicitly **paid** entry, per the requirement that paid events are collected but kept distinct: Circus Bella's BRAVURA holiday Big Top (ticketed; badge "Paid").

## The 21 new entries

| # | Entry | Kind | Cost badge | Next verified date |
|---|---|---|---|---|
| 1 | San Francisco Cable Car Museum | Weekly | Free | recurring (Tue–Sun) |
| 2 | Randall Museum | Weekly | Free | recurring (Tue–Sat) |
| 3 | San Francisco Railway Museum | Weekly | Free (donations) | recurring (Tue–Sun) |
| 4 | Fort Point National Historic Site | Weekly | Free | recurring (Thu–Mon) |
| 5 | Presidio Officers' Club free history exhibitions | Weekly | Free | recurring (Fri–Sun) |
| 6 | Free Shakespeare in the Park | Annual | Free | 2026 season past; 2027 announced, dates TBD |
| 7 | Noontime Concerts | Weekly | Free (live concerts) | 2026-10-20, 10-27, 11-10 |
| 8 | Choral Evensong (Grace Cathedral) | Weekly | Free | 2026-10-18 (snapshot day), 10-22, 10-25, 10-29, 11-01 |
| 9 | People in Plazas | Annual | Free | summer 2027 not yet posted |
| 10 | Weekly Juggle (Circus Bella) | Weekly | Free | season-end text irregular (flagged) |
| 11 | Five Minutes of Fame (Noisebridge) | Monthly | Not stated | next date not stated on wiki (flagged) |
| 12 | Circuit Hacking Mondays (Noisebridge) | Weekly | Not stated | recurring (most Mondays) |
| 13 | Bay Area Science Festival | Annual | Free | 2026-10-17 (one day before snapshot; past) |
| 14 | Board Game Night (Gamescape) | Weekly | Not stated | 2026-10-21 |
| 15 | BRAVURA (Circus Bella Big Top) | Special | **Paid** | 2026-12-11 → 2027-01-03 |
| 16 | AI Tinkerers San Francisco | Special | Not stated | next event not posted |
| 17 | The AI Collective — San Francisco Chapter | Special | Not stated | listing lacked a year (flagged) |
| 18 | Musée Mécanique | Weekly | Not stated | recurring (daily 10–8) |
| 19 | Japanese Tea Garden free admission hour | Weekly | Free | recurring (M/W/F 9–10 am) |
| 20 | Conservatory of Flowers free first Tuesday | Monthly | Free | recurring (1st Tue) |
| 21 | San Francisco Botanical Garden free admission times | Weekly | Free | recurring (daily 7:30–9 am; 2nd Tue) |

## Retrieval methods (labelled per capture in the audit JSON)

1. **`workspace fetch_page`** — full page body returned by the fetch tool. Pages that exposed more chunks than were read are marked `complete:false` with chunk counts (sf.aitinkerers.org, aicollective.com).
2. **`workspace web_search`** — verbatim result text the search tool returned for that exact official URL, used only where the page was script-dominated or returned an empty shell / navigation-heavy response on direct fetch: `museemecanique.com` (returned only `# Landing`), `streetcar.org/museum/` (empty body), `gamescapesf.com` (used for the address block + "weekly schedule of game nights" text), `gracecathedral.org/calendar-events/` (venue address), `ucsf.edu` news (recurrence evidence for the science festival). These captures carry **no HTTP status** — a search result is evidence of what the tool returned, never a claim of a 200 page fetch.

## Irregularities found and flagged (all published on the Flagged for Review page via the rows' `reason` fields, never corrected by inference)

1. **Circus Bella Weekly Juggle:** the official page ends the 2026 season with "Saturday October 19", but 19 Oct 2026 is a Monday; the actual last Saturday in the window was 17 Oct. Quoted verbatim; no next session date asserted.
2. **Circus Bella BRAVURA:** official pages disagree on the run end — Big Top hero "Dec 11, 2026 - Jan 4, 2027" and home page "Dec. 11 2026 - Jan. 3rd 2027" vs the detailed schedule's final show "Sunday, Jan. 3 (Closing Performances)". Row uses the detailed schedule (Jan 3); both dates left quoted.
3. **Noisebridge 5MoF wiki:** the page's "Next event" link points to a June 17, 2026 page (already past) and the "Prev event" link text mixes years (2025/05 21 under a 2026 URL). The third-Thursday pattern would put the next talk on 19 Nov 2026, but the page doesn't state it — no date asserted.
4. **The AI Collective SF chapter page:** the upcoming meetup ("Multimodal Engineering Night") was listed as "In 5 days·Thu, Oct 22nd" with **no year** — not recorded as a verified date.
5. **Gamescape events page:** prints two-digit years ("- 10/21/26"); the full year 2026 appears on the same page's tournament names, which is quoted alongside the session date.
6. **Grace Cathedral:** Evensong is stated free on the official series page while general cathedral *sightseeing* admission is ticketed ($15 adults, per the official visit page). The row prices only the Evensong service and notes the distinction.

## Researched and deliberately *not* added (with why)

- **San Francisco Trolley Dances (Epiphany Dance Theater):** the official page now describes the festival in the past tense ("was an annual festival… FREE of charge"); the 20th annual (2023) was the finale season. Nothing current to verify → excluded rather than listed as recurring.
- **Circus in the Parks (Circus Bella):** official page only says "will be back in June 2027" with no SF venue list for the coming season; a review-only row (`x-circus-in-the-parks`) already exists. A new row would duplicate it without improving verification → left as is; the June-2027 note is archived in the captures.
- **Urban Air Market:** `urbanairmarket.com` is a parked domain ("Coming Soon") — no current official evidence of dates → excluded.
- **Undiscovered SF / How Weird Street Faire:** not researched to an official current source within this pass.
- **AWS GenAI Loft SF** (surfaced via AI Collective demo-night listings at 525 Market St): series by AWS with no current dated SF event on the official page → excluded.
- **Amoeba Music SF in-store shows:** no stable official event URL with current dates captured → excluded.

## Sources (36 archived captures, all official)

Organizer/venue/operator pages: cablecarmuseum.org (2), randallmuseum.org, streetcar.org (2), nps.gov/fopo (2), presidio.gov, sfshakes.org (2), noontimeconcerts.org (2), peopleinplazas.org, gracecathedral.org (3), circusbella.org (6), noisebridge.net (2), bayareasciencefestival.org (3), ucsf.edu (organizer news), gamescapesf.store, gamescapesf.com, museemecanique.com, sf.aitinkerers.org (2), aicollective.com, gggp.org (2 — Gardens of Golden Gate Park, operator of the three gardens).

Every quotation in the audit decisions was machine-validated before writing: each quote must be an NFKC/whitespace-normalised substring of its archived capture; recurring classifications require their own recurrence quotation; occurrence dates must be recoverable from their quotations; publication requires an approved name, venue and confirmed San Francisco geography.
