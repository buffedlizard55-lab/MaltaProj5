# SF Events

A bounded, official-source inventory of events within San Francisco, reviewed **18 October 2026**. **Not exhaustive.** Unconfirmed values remain empty and are flagged. No continuous refresh or automatic factual verification is claimed.

Site: https://buffedlizard55-lab.github.io/MaltaProj5/

## Contents
- `data/events.json`: event rows, official-source references, evidence map, unknown fields and flags.
- `data/sources.json`: official URLs, checked date, selected transcribed excerpts.
- `data/review.json`: research gaps, excluded candidates and conflicts.
- `data/events.csv`: downloadable inventory, generated from JSON.
- Eleven static pages: dashboard, recurrence/category views, review queue, evidence ledger.

## Build and test
Python 3, no dependencies:

```sh
python scripts/build.py
python scripts/validate.py
python -m http.server 8000 --bind 0.0.0.0
```

Generated HTML is committed; tables and navigation work without JavaScript. JS adds search/filter/reset. GitHub Actions validates pull requests and deploys main to Pages. Tests check local links and fragments, source references, empty-field flags, parent relationships and generated-file freshness, not the truth of source content or external uptime.

See the site's Sources & methodology page for official links, row evidence and limitations. Eight After Dark themes are linked to their parent series; do not count them as eight extra series. Editorial categories are not sourced claims. Sources can change; verify organizer details before attending. `COORDINATION.md` records scope and publication history.
