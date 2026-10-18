# Research log — session `3adf31d9` (new-requirement pass: gaming, music, AI)

**Snapshot: 18 October 2026.** All evidence for this pass is stored in
[`data/audit_3adf31d9.json`](../audit_3adf31d9.json) — captures plus explicit decisions.
Nothing in this pass was inherited from earlier registers, and nothing was filled in from memory.

## Why this pass existed

The existing register covered markets, museums, festivals, culture and community programmes well,
but had **no gaming entries beyond one dated championship, no AI/technology entries at all**, and
no way to answer “what is happening nearest to today, and what does it cost?”. This pass adds
those three topic areas and the presentation layer that answers the date and cost questions.

## Retrieval methods, stated honestly

Two workspace tools were used, and every capture records which one produced it:

| Method | What it is | Where it was used |
|---|---|---|
| `workspace fetch_page` | The page body as returned by the fetch tool. Some pages returned more chunks than were read; those captures record `chunks_retrieved` / `chunks_total` and `complete: false`. | gdconf.com, moscone.com, iclr.cc, ai.engineer, databricks.com, milibrary.org, sterngrove.org |
| `workspace web_search` | The **verbatim result text** the search tool returned for that exact official URL. Used where the page is dominated by navigation (sfpl.org buries the event block under three chunks of branch hours) or where the relevant block sits below the fetched fold (the Stern Grove contact block). | sfpl.org event pages, aicouncil.com, the Databricks FAQ, the Stern Grove contact block |

A search-snippet capture carries **no HTTP status**. It is evidence of what the tool returned for
that official URL on 18 October 2026 — it is never presented as a verified page fetch with a
200 response. This distinction is printed on the Sources page per source record.

## Entries added (15)

| Entry | Official source | Publication |
|---|---|---|
| GDC Festival of Gaming — 1–5 Mar 2027, Moscone Center | https://gdconf.com/ | listed |
| 20th Annual San Francisco Scholastic Chess Championship — 11 Apr 2026, 701 Mission Street | https://www.milibrary.org/chess/tournaments/2026-san-francisco-scholastic-chess-championship | listed |
| Introduction to Chess (Mechanics' Institute) — Thursdays | https://www.milibrary.org/chess/chess-classes/ | **held for review** |
| Social: Chess Club (Visitacion Valley) — 2nd & 3rd Friday | https://sfpl.org/events/2026/03/13/social-chess-club | listed |
| Activity: Chess Club (Excelsior) | https://sfpl.org/events/2026/05/09/activity-chess-club | listed |
| Social: Afternoon Board Games (Sunset) | https://sfpl.org/events/2026/07/26/social-afternoon-board-games | listed |
| Social: Game Night (Marina) | https://sfpl.org/events/2026/08/12/social-game-night | listed |
| Activity: Chinese Chess 中国象棋 (Main Library) | https://sfpl.org/events/2026/08/02/activity-chinese-chess-zhongguoxiangqi | listed |
| Social: Family Game Night (Bernal Heights) | https://sfpl.org/events/2026/06/13/social-family-game-night | listed |
| AI Engineer World's Fair 2027 — 29 Jun – 1 Jul 2027, Moscone West | https://ai.engineer/worldsfair/2027 | listed |
| TDX 2027 — 10–11 Mar 2027, Moscone Center | https://www.moscone.com/events/tdx-2027 | listed |
| ICLR 2027 — 26–30 Apr 2027, Moscone Center | https://iclr.cc/Conferences/2027/index.html | listed (venue flagged) |
| Data + AI Summit 2027 — 21–24 Jun 2027, Moscone | https://www.databricks.com/dataaisummit | listed |
| AI Council 2027 — 23–24 Mar 2027, San Francisco | https://www.aicouncil.com/ | **held for review** |
| Stern Grove Festival — 19th Avenue and Sloat Boulevard | https://www.sterngrove.org/about-us · https://www.sterngrove.org/accessibility-ada | listed |

## Deliberate non-approvals

These are the judgment calls that kept values blank rather than plausible:

1. **Library admission is never assumed free.** Every SFPL chess, board-game and Chinese-chess
   entry leaves the price cell blank, because the official event text does not state admission.
   The Excelsior page does say “Bright Knights Chess Club hosts free chess programs” — that
   sentence describes the partner club's programmes generally, not this library session, so it was
   not promoted to a verified value.
2. **Conference prices are not quoted anywhere in the captured text.** GDC, TDX, ICLR, Data + AI
   Summit and AI Engineer all link to registration or pricing pages without stating a number on
   the page that was read. All five read **“Not stated”**, never “Paid” by assumption and never a
   guessed ticket price.
3. **Mechanics' Institute Introduction to Chess is held for review.** The official page names the
   room (“Onsite in the Chess Room at Mechanics’”) and the cost (“FREE for Mechanics’ Institute
   Members”) but the captured text never states a San Francisco address, so the directory's
   name + venue + city-only geography gate is not met.
4. **AI Council 2027 is held for review** for the same reason in reverse: San Francisco is named as
   the host city, but no venue is stated.
5. **ICLR 2027 venue is published with a flag.** The official page's Venue section currently reads
   “Venue information will be posted here”; the venue value comes from that same page's venue image
   caption, “Moscone Center, San Francisco, CA”. It is approved, and the caveat is printed in the
   row's review notes.
6. **No recurrence was invented for GDC.** The captured text dates the 2027 edition but does not say
   the festival repeats annually, so the cadence is “Special”, not “Annual”.
7. **Stern Grove has no approved occurrence date.** The official pages state “since 1938” and “Every
   summer” — enough for an annual cadence — but no 2027 season dates were published on the pages
   read. No date is asserted.

## Verification performed

* Every quotation was checked as an NFKC/whitespace-normalised substring of the archived capture
  text for that exact URL. This is provenance, not semantic truth.
* Every occurrence date was checked so that its year, month and day are recoverable from the
  quotation that supports it.
* Weekly/Monthly/Annual classifications each carry their own recurrence quotation.
* The projection is pure and idempotent: rebuilding produces byte-identical `data/events.json`,
  `data/sources.json`, `data/review.json` and `data/audit_summary.json`.
* `python3 scripts/validate.py` (261 rows, 17 pages, cost badges, date ordering, every row's
  official link, every local link/fragment) and `python3 -m unittest discover -s tests` (42 tests)
  both pass, and the optional Playwright pass reports no console errors, no mobile overflow and no
  automated WCAG A/AA findings.
