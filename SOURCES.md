# Sources

The authoritative source ledger is **`data/sources.json`** and its rendered form
**`sources.html`**. It is generated and re-checked by the pipeline; this file explains the rules
rather than duplicating 213 changing records across 135 domains.

## What a source record contains

| Field | Meaning |
|---|---|
| `url` | The official page cited as evidence. |
| `publisher` | Who publishes the page (organizer, venue, museum, City body). |
| `checked` | The date the page was read: `2026-10-18`. |
| `excerpt` | Selected text transcribed from the page — for automated rows, the passage around the event-name match. Not a full-page archive. |
| `method` | How the page was checked: manual read, automated fetch, or both. |
| `http` | Result of the last automated fetch (200, 403, 404, 0 = no response). |
| `manual` | Present when the page was read by hand during integration. |

## Rules

1. Organizer, venue, museum and municipal pages supply admitted facts. Tourism-board guides were
   used for discovery and are named when they are the only source.
2. A link is evidence only for what its page states. A blank cell is not evidence of "free".
3. Where two official sources disagree, the disputed value stays blank and both sources are named
   on `review.html`.
4. The automated check (`tools/verify_rows.py`) proves that a page loads and contains the event
   name. It cannot prove dates, times, prices or venues. Those rest on the row's verification
   label (`field-level`, `page-level` or `flagged`).
5. Pages that block automated clients (HTTP 202/403/405/429/5xx) are recorded as blocked, not as
   verified and not as dead. Dead links (404/410/DNS) fail CI through `tools/remotecheck.py`.

## Historical note

An earlier `SOURCES.md` listed the 26 source records compiled by session `3a19e72d`. Those records
are preserved: the ledger now includes them (with their excerpts) alongside the records from the
other three research passes (`5a85baf2`, `4f47c142`, `a1b7522f`). The full history is in git and
in the `data/sources_*.json` snapshots.
