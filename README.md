# MaltaProj5 — San Francisco Events Inventory

Verified inventories of events happening **within the city of San Francisco only**, from two parallel
research sessions, each sourced to official sites. Unconfirmed values are left blank and flagged —
nothing is inferred. Data snapshots taken **18 October 2026**; no continuous refresh or automatic
factual verification is claimed.

- **Primary site (docs/):** 167 events — [dashboard](docs/index.html) ·
  [Flagged for Review](docs/flagged.html)
- **Secondary site (repo root):** 29-row bounded inventory with evidence ledger —
  [dashboard](index.html) · [sources & methodology](sources.html)
- Intended Pages URL: https://buffedlizard55-lab.github.io/MaltaProj5/

> **Publication status:** GitHub Pages enablement is currently blocked — GitHub returns
> `Resource not accessible by integration` (HTTP 403) when creating the Pages site, both via the
> repository credential and the workflow token (see
> [deployment attempt](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39084799573)).
> The owner must enable Pages in repo Settings (or re-authorize the GitHub connection with Pages
> admin), then the deploy workflow will publish `docs/`. Full history in `COORDINATION.md`.

## Primary dataset (session `4f47c142`) — `docs/` site

| Path | Purpose |
|------|---------|
| `data/events-weekly.json` | Regularly occurring events (weekly/monthly/seasonal) — 34 |
| `data/events-annual.json` | Annually recurring events, by month — 95 |
| `data/events-special.json` | Special (one-off/dated) 2026 events — 38 |
| `data/exclusions.json` | Exclusion log (out-of-city or out-of-scope events, with reasons) — 14 |
| `data/research/` | Raw research notes |
| `tools/build_site.py` | Generates the static site in `docs/` from the data files |
| `tools/verify_site.py` | Verification pass: every row sourced, no broken internal links, domain allowlist |
| `docs/` | Site (dashboard + category subpages + Flagged for Review) |

```sh
python3 tools/build_site.py     # regenerates docs/
python3 tools/verify_site.py    # exits 1 on any unsourced row / broken link / off-allowlist domain
```

## Secondary dataset (session `3a19e72d`) — root site

- `data/events.json`: event rows, official-source references, evidence map, unknown fields and flags
  (includes eight Exploratorium After Dark themes linked to their parent series).
- `data/sources.json`: official URLs, checked date, selected transcribed excerpts.
- `data/review.json`: research gaps, excluded candidates and conflicts.
- `data/events.csv`: downloadable inventory, generated from JSON.
- Eleven static pages: dashboard, recurrence/category views, review queue, evidence ledger.
- `scripts/build.py` / `scripts/validate.py`: dependency-free Python build and validation.

```sh
python scripts/build.py
python scripts/validate.py
python -m http.server 8000 --bind 0.0.0.0
```

Generated HTML is committed; tables and navigation work without JavaScript. JS adds search/filter.
GitHub Actions validates pull requests and attempts Pages deployment. Tests check local links,
source references, empty-field flags and generated-file freshness — not the truth of source content
or external uptime.

## Shared scope rules

- Events must take place **inside San Francisco city limits** (e.g., Cow Palace in Daly City,
  PayPal Park in San Jose, or Levi's Stadium in Santa Clara are excluded and logged).
- Professional sports league schedules and trade conventions are excluded as categories; individual
  special public events at those venues are included.
- Aggregators and media articles are never the source of record for a value.
- Sources can change; verify organizer details before attending.

`COORDINATION.md` records the task board, verification log and publication history.
