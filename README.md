# MaltaProj5 — San Francisco Events Inventory

A verified inventory of events happening **within the city of San Francisco only**, organized into
**regularly occurring events** (weekly/monthly schedules and annual traditions) and **special events**
(one-off, dated), with analysis — published as a static GitHub Pages site.

- **Site:** https://buffedlizard55-lab.github.io/MaltaProj5/
- **Data snapshot:** 2026-10-18
- **Dataset:** 167 events (34 weekly/regular · 95 annual · 38 special) + 14 documented exclusions
- **Verification:** every table row links to an official source (event organizer, venue, or
  government / official tourism body). Values that could not be confirmed from an official source are
  left blank and flagged on the site's [Flagged for Review](https://buffedlizard55-lab.github.io/MaltaProj5/flagged.html)
  page — nothing is inferred.

## Repository layout

| Path | Purpose |
|------|---------|
| `data/events-weekly.json` | Regularly occurring events (weekly/monthly/seasonal) |
| `data/events-annual.json` | Annually recurring events, by month |
| `data/events-special.json` | Special (one-off/dated) 2026 events |
| `data/exclusions.json` | Exclusion log (out-of-city or out-of-scope events, with reasons) |
| `data/research/` | Raw research notes |
| `tools/build_site.py` | Generates the static site in `docs/` from the data files |
| `tools/verify_site.py` | Verification pass: every row sourced, no broken internal links, domain allowlist |
| `docs/` | GitHub Pages site (dashboard + category subpages + Flagged for Review) |
| `COORDINATION.md` | Shared task board for parallel agent sessions (owners, status, verification log) |

## Workflow

1. Research/verify events against official sources (organizer sites, sf.gov, SFMTA, SF Environment,
   Port of SF, Presidio Trust, SF Travel — the City's destination marketing organization).
2. Record them in the `data/*.json` files with `status` (`verified` / `flagged`) and per-row flags.
3. Run `python3 tools/build_site.py` to regenerate `docs/`.
4. Run `python3 tools/verify_site.py` — the build fails if any row lacks a source link, any internal
   link is broken, or any external link falls outside the official-domain allowlist.
5. Merge to `main`; GitHub Pages serves `docs/`.

## Scope rules

- Events must take place **inside San Francisco city limits** (e.g., events at the Cow Palace in Daly
  City, PayPal Park in San Jose, or Levi's Stadium in Santa Clara are excluded and logged).
- Professional sports league schedules and trade conventions are excluded as categories; individual
  special public events at those venues are included.
- Aggregators and media articles are never the source of record for a value.
