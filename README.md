# MaltaProj5 — San Francisco Events Inventory

Verified inventories of events happening **within the city of San Francisco only**, produced by
three parallel research sessions, each row sourced to an official site. Unconfirmed values are left
blank and flagged — nothing is inferred. Data snapshots taken **18 October 2026**; no continuous
refresh or automatic factual verification is claimed.

## Two sites, two datasets — one repository

| | Primary site (`docs/`) | Unified register (repo root) |
|---|---|---|
| URL path | `/` | `/inventory/` in the published copy |
| Events | **167** (34 weekly/regular · 95 annual · 38 special) + 14 exclusions | **86** unified rows (29 + 61 from two sessions, 4 duplicates reconciled) |
| Sessions | `4f47c142` | `3a19e72d` + `5a85baf2` |
| Pages | Dashboard, Weekly & Regular, Annual, Special, Flagged for Review | 11 pages incl. review queue and evidence ledger |
| Generator | `tools/build_site.py` | `scripts/build.py` |
| Validator | `tools/verify_site.py` | `scripts/validate.py` + `tools/remotecheck.py` (CI) |

Intended Pages URL: https://buffedlizard55-lab.github.io/MaltaProj5/

> **Publication status:** GitHub Pages enablement is blocked — GitHub returns
> `Resource not accessible by integration` (HTTP 403; the credential has no Pages grant —
> `X-Oauth-Scopes` empty, reproduced independently by two sessions; see
> [deployment attempt](https://github.com/buffedlizard55-lab/MaltaProj5/actions/runs/39084799573)).
> The owner must enable Pages in repo Settings (Source: GitHub Actions, or deploy from `main` /
> `docs`), then the `Validate and deploy Pages` workflow publishes this site. Full history in
> `COORDINATION.md`.

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

## Unified register (sessions `3a19e72d` + `5a85baf2`) — root site

- `data/events.json`: 86-row combined register (canonical schema; `tools/integrate.py` merges
  `data/events_3a19e72d.json` + `data/events_5a85baf2.json`).
- `data/sources.json`: 75 official-source records with checked dates and transcribed excerpts.
- `data/review.json`: research gaps, excluded candidates, conflicts and review findings.
- `ANALYSIS.md` / `SOURCES.md`: analysis findings and the source ledger in readable form.
- Eleven static pages: dashboard, recurrence/category views, review queue, evidence ledger.
- `scripts/build.py` / `scripts/validate.py` / `tools/remotecheck.py`: dependency-free build,
  validation, and remote source-URL checking (wired into CI).

```sh
python3 scripts/build.py && python3 scripts/validate.py
```

Generated HTML is committed; tables and navigation work without JavaScript. JS adds search/filter.
GitHub Actions validates pull requests (both validators + remote source check) and attempts Pages
deployment. Tests check local links, source references, empty-field flags and generated-file
freshness — not the truth of source content or external uptime.

## Shared scope rules

- Events must take place **inside San Francisco city limits** (e.g., Cow Palace in Daly City,
  PayPal Park in San Jose, or Levi's Stadium in Santa Clara are excluded and logged).
- Professional sports league schedules and trade conventions are excluded as categories; individual
  special public events at those venues are included.
- Aggregators and media articles are never the source of record for a value.
- Sources can change; verify organizer details before attending.

`COORDINATION.md` records the task board, verification logs, merge history and publication status.
