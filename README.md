# MaltaProj5 — San Francisco Events Register

A verified register of events held **inside the City and County of San Francisco**, organised into
events that recur (weekly, monthly, annually) and one-off special events — plus the analysis and
the irregularities found while verifying them.

Live site: **https://buffedlizard55-lab.github.io/MaltaProj5/**

## What's here

| Path | Contents |
|---|---|
| `data/events.json` | The register. One object per event, every one with an official `source_url`. |
| `data/discontinued.json` | Items that look like SF events but are discontinued or out of the city. |
| `data/build_data.py` | The single place event rows are authored. Regenerates the JSON. |
| `docs/` | The GitHub Pages site (landing dashboard + category subpages), generated from the data. |
| `tools/build_site.py` | Builds `docs/` from `data/`. |
| `tools/validate.py` | Schema check. Fails if a row is missing a field or cites a non-official source. |
| `tools/linkcheck.py` | Checks every internal link in the built site and that every source link is published. |
| `tools/remotecheck.py` | Fetches every official source URL and fails on dead links (runs in CI). |
| `SOURCES.md` | The official source register: what each page confirmed, grouped by category. |
| `ANALYSIS.md` | Findings computed from the data. |
| `COORDINATION.md` | Shared task board for parallel agent sessions. |
| `.github/workflows/checks.yml` | CI: validate → build → linkcheck → stale-build check → remote source check. |

## How the data was produced

1. Candidate events were discovered from city calendars, transit advisories and event listings.
2. **Each row was then verified against an official page** — the organizer's own site, a City of
   San Francisco page (`sf.gov`, `sfrecpark.org`, `sfmta.com`, `sfpl.org`, `sfport.com`), or the
   venue's own page. Aggregators (Funcheap, SF Station, Timeout, Eventbrite, Wikipedia, news
   outlets, travel blogs) were used only for discovery and are rejected as sources by
   `tools/validate.py`.
3. **No value was inferred.** If a date is not on an official page, the field is empty and the row
   is marked `date_status: "unverified"`. Third-party calendars were never used to fill a gap.
4. Where two official sources disagree, the row is marked `status: "flagged"` and both sources are
   named in the row's note. These are published on the site's **Flagged for Review** page.

## Status vocabulary

| Badge | Meaning |
|---|---|
| `verified` | Event, cadence and date read off the linked official page. |
| `date unverified` | Event confirmed; organizer has not published the next date. Cell left blank. |
| `runs on this pattern` | A continuous series (weekly market, full concert season) with no single next date. |
| `flagged` | Genuine irregularity — conflicting official sources, a stale official page, or a value that could not be pinned down. |

## Working on this repository

Read `COORDINATION.md` first — it is the shared task board. Claim a task with your session ID and
file scope, commit and push the claim before starting, and keep your file scope non-overlapping.

```bash
python3 data/build_data.py     # author rows here, then regenerate the JSON
python3 tools/validate.py      # schema + official-source enforcement
python3 tools/build_site.py    # rebuild docs/
python3 tools/linkcheck.py     # internal links + source links published
python3 tools/remotecheck.py   # fetches every source URL (needs network; runs in CI)
```

`docs/` is committed because GitHub Pages serves it from the `main` branch. After changing any row,
run all four commands and commit `data/` and `docs/` together — CI fails if `docs/` is stale.
