# Research log — session `21f3dd85`, free-first pass (T37), 2026-10-18

**Task:** additional **free gaming / music / AI** entries inside San Francisco from official
organizer, venue, library and government pages only; then other free entries; paid entries
collected but kept out of the free sections. Exact quotations + archived captures in
[`data/audit_21f3dd85.json`](../audit_21f3dd85.json); every quote was machine-checked to be a
verbatim substring (whitespace/NFKC-normalised) of its archived capture with the register's own
`validate_decision` before the audit file was written. Snapshot date stays **2026-10-18**; a
recurring pattern never generates a next date; a yearless date list never yields an occurrence.

## Added — listed (6)

| Row | Topic | Kind | Cost | Official source(s) read |
|---|---|---|---|---|
| `f-noontime-concerts` | Music | Weekly + 3 approved Tuesdays (2026-10-20, 10-27, 11-10) | **Free** (“Free Live Concert Every Tuesday”; “not ticketed but suggested donations are solicited”) | noontimeconcerts.org `/`, `/about-noontime-concerts/`, `/directions-and-location/` (fetch) |
| `f-sea-chantey-sing` | Music | Monthly + 2026-12-05 | **Free** (“This event is free to attend.”) | nps.gov event page (fetch) |
| `f-mi-chess-socials` | Gaming | Monthly | **Free** (“Free – just show up, no registration needed”) | milibrary.org `/chess/chess-classes/` + tournament page for the SF address (fetch) |
| `f-sfpl-mix-gaming` | Gaming | Monthly | **Free** (SFPL events-index statement, see judgment call below) | sfpl.org `/teens/the-mix/gaming`, `/teens/the-mix`, `/teens`, `/events` (search excerpts + fetch) |
| `f-sfpl-tech-week` | AI & technology | Annual | **Free** (“over 30 free workshops”) | sfpl.org 2026-04-24 release (search excerpts) + `/events` locations block (fetch) |
| `f-mi-winter-tuesday-night-marathon-2026` | Gaming | Special, 2026-11-03 → 12-15 | **Paid** (“Entry fee … Members: $70 … Non-Members: $100”) — for the separate Paid section | milibrary.org tournament page (fetch) |

## Added — held for review (2, published on Flagged for Review with links)

| Row | Why held |
|---|---|
| `f-internet-archive-tours` | archive.org's official contact page confirms schedule (“most Friday afternoons”), time (1:00pm), venue (300 Funston Avenue, San Francisco) and price (“public, free and on a drop-in basis”), but gives the programme **no title**. The directory gate requires an approved event name, so the row is held rather than given an invented name. The SF Arts Commission calendar (`sfarts.org`) calls it “Internet Archive Tour”, but that is not the organizer's page and was not used as name evidence. |
| `f-grace-cathedral-organ-recital-series` | **Conflicting admission wording on official pages.** Individual recital pages on gracecathedral.org variously state “Cost: Free” / “free organ recital”, while another official recital page warns “there is an admission fee for visitors on Sundays from 1 to 5 pm” and that attendees “must register in advance to avoid paying the fee”. The fetched series/organs pages state no price. Admission left blank; held until current terms can be confirmed from one readable official page. |

## Judgment call — SFPL admission (flagged, reversible)

`sfpl.org/events` states: **“All programs and events are free and open to the public.”**
Session `3adf31d9` left admission blank on its seven SFPL gaming rows because the *individual
event pages* it captured do not state a price. This session quotes the library's official
events-index statement as admission evidence for its two new SFPL rows, applying an explicit
all-programmes statement in context (the same cross-page pattern the register already accepts
for venue geography from official address pages). **No earlier row was edited**: the older SFPL
rows still read “Not stated”, and the inconsistency is deliberate, documented in the row's review
notes, and flagged here for a future harmonization decision by the repo owner.

## Evidence found for a future integration (no row changed)

* **Mechanics' Institute “Introduction to Chess”** (`g-mi-introduction-to-chess`, currently held
  for a missing venue): the current milibrary.org chess-classes page now reads “Introduction to
  Chess (Thursdays, 5:30-6:30 PM, at Mechanics') … Location: Onsite in the Chess Room at
  Mechanics’ … Cost: FREE for Mechanics’ Institute Members”, with an upcoming block “November
  5 - December 17 (Nov 26 off)”. Together with the Institute's stated address (57 Post Street,
  San Francisco, CA 94104) this appears to supply the missing venue evidence. This session did
  **not** create a duplicate listed twin and did not edit session `3adf31d9`'s audit; promotion
  is recommended to a future corrections/integration pass that owns that audit file. Note the
  class is free **for members**, so its badge would be Free-with-conditions, not unconditionally
  free.

## Checked and not added (with reason)

* **Noisebridge (noisebridge.net / meetup.com)** — free classes incl. game development and AI
  meetups exist, but the readable programme evidence in this pass came from meetup.com and a
  2022 wiki press kit, not a current organizer-domain page stating a specific programme's
  cadence, venue and admission together. Not added rather than weakening the source standard.
* **Grace Cathedral organ recitals** — added as held (above), not listed.
* **SFPL dated one-off AI workshops after 2026-10-18** — the library runs these repeatedly
  (e.g. “Exploring and Trying Out AI Features”, “Introduction to Generative AI”), but in this
  pass only past instances (Feb–Aug 2026) could be quoted from official event pages; no
  post-snapshot instance was invented. The annual Tech Week umbrella is listed instead.
* **SFPL Ingleside “Activity: Chess Club”** — the instance readable at capture was on the
  snapshot date itself (Sun 2026-10-18) with no stated cadence on the page; a same-day one-off
  row would add noise next to the three library chess clubs already listed. Not added.
* **Sunday Streets SF** — already in the register as a series row (`b-sunday-streets`).
* **de Young / Legion of Honor free days, Golden Gate Park Band, Stern Grove, Hardly Strictly**
  — already listed; not duplicated.

## Retrieval honesty

Fetches were made with the workspace `fetch_page` tool, which does not report an HTTP status
code; all captures therefore record `http: null`. Four sfpl.org captures and one
gracecathedral.org listing capture are the search tool's verbatim result text for the exact
official URL (labelled `tool_excerpt`), following session `3adf31d9`'s precedent for
navigation-dominated sfpl.org pages. Archived `text` fields are verbatim excerpts trimmed to
the quoted blocks; chunk counts are recorded per capture.
