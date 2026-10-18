# COORDINATION.md — Shared Task Board

This file is the shared task board for all agent sessions working on this repo.
Before starting any task, read this file. Claim a task by writing your session ID
and file scope in the table, then commit and push the claim immediately.
Never start a task another session has claimed. If a task requires changing a file
owned by another session, log the request in the Handoff & Request Log below
instead of editing that file.

**Session IDs** are the git branch names of each session. **This environment
restricts every session to a single fixed branch** (`session branches cannot be
created or renamed`), so the branch name doubles as the session ID, and file
scopes below are what keep sessions from conflicting.

- Repo: https://github.com/buffedlizard55-lab/MaltaProj5
- Default branch: `main`
- Scope of the project: collect, organize and analyze the full list of events
  happening **within the city of San Francisco only** (city limits — see Scope
  rules), organized into **regularly occurring events** (weekly/monthly and
  annual) and **special events** (one-off/dated), each verified against an
  **official source** (event organizer, venue, or government site), published on
  a GitHub Pages site with a "Flagged for Review" page for irregularities and
  unverified values.

## Scope rules (project requirements)

1. Events must take place **inside San Francisco city limits**. Events at venues
   outside the city (e.g., Cow Palace in Daly City, Shoreline Amphitheatre in
   Mountain View) are excluded and, where notable, the exclusion is noted on the
   Flagged for Review page.
2. Every published table row must carry a **source link to an official site**
   (organizer's official website, official venue site, or a government /
   official tourism-body site such as sf.gov, sfmta.com, presidio.gov,
   sftravel.com). Aggregators, ticket resellers and media articles are not used
   as the primary source for a value.
3. If a value cannot be confirmed from an official source, it is left **blank**
   and flagged as unverified on the Flagged for Review page. Values are never
   inferred or filled in.
4. No manual user input: sessions work autonomously to completion.

## Task board

| Task | Description | Status | Owner (session ID) | File scope |
|------|-------------|--------|--------------------|------------|
| T1 | Create this coordination board | done | arena/4f47c142-maltaproj5 | COORDINATION.md |
| T2 | Research & verify weekly/regularly recurring SF events | done | arena/4f47c142-maltaproj5 | data/events-weekly.json |
| T3 | Research & verify annually recurring SF events | done | arena/4f47c142-maltaproj5 | data/events-annual.json |
| T4 | Research & verify special (one-off/dated) SF events | done | arena/4f47c142-maltaproj5 | data/events-special.json |
| T5 | Build GitHub Pages site (landing page + category subpages + Flagged page) | done | arena/4f47c142-maltaproj5 | docs/ (all files), tools/build_site.py |
| T6 | Line-by-line verification pass: every table row sourced, no broken internal links | done | arena/4f47c142-maltaproj5 | docs/**, tools/verify_site.py |
| T7 | Final integration: merge to main, publish GitHub Pages, confirm deploy, record PR | in progress | arena/4f47c142-maltaproj5 | COORDINATION.md, docs/ |

**Note on ownership (2026-10-18):** no other sessions were active when this board
was created (repo contained only the initial commit with a one-line README, and
origin had no other branches). Session `arena/4f47c142-maltaproj5` therefore
claimed T1–T7 and is executing both the research tasks and the final integration
role. Any session that starts later should check this table, claim only
**unclaimed** tasks (or take over a claim older than 60 minutes with no commits,
noting the handoff below), and keep to its claimed file scope. Shared outputs
(`data/events.json` combined file, `docs/index.html` navigation, README) are
touched only by the integration role, which this session also holds.

## Handoff & Request Log

| Timestamp (UTC) | Session | Entry |
|-----------------|---------|-------|
| 2026-10-18 | arena/4f47c142-maltaproj5 | Board created; claimed T1–T7 (no other sessions active; repo empty). T1 done. |
| 2026-10-18 | arena/4f47c142-maltaproj5 | README.md (repo root) is updated by this session as part of integration — it was an unclaimed one-line stub. Requests to change it from other sessions: log here first. |

## Verification log (fill in when a task is marked done)

| Task | Status | Sources used | Verification performed | Irregularities found |
|------|--------|--------------|------------------------|----------------------|
| T1 | done | — | Board reflects repo state at creation (single commit `20813bf`, README stub only) | None |
| T2 | done (2026-10-18) | Foodwise (foodwise.org), Heart of the City FM (hotcfarmersmarket.org), sf.gov Alemany page, PCFMA (pcfma.org), Agricultural Institute of Marin, Noe Valley FM, SF Environment (sfenvironment.org), Off the Grid, presidio.gov, Cal Academy, Exploratorium, SF City Guides, Union Square Alliance, sundaystreetssf.com, sfcriticalmass.org, famsf.org, about.asianart.org, goldengateparkband.org, dftsf.com, soma-nights.com, Sunset Mercantile, ybgfestival.org, downtownsf.org, bhangraandbeats.com, circusbella.org | 34 weekly/monthly/seasonal recurring events verified row-by-row against operator/official sites. Farmers-market days & hours taken from operator sites (not aggregators). | (1) Off the Grid Fort Mason is now monthly, not weekly as historically. (2) Critical Mass has no official organizer (flagged). (3) SF Travel lists Ferry Plaza Tue hours as 8am vs operator's 10am (operator value used, flagged). (4) Presidio Picnic/Twilight 2026 season end dates not stated on official announcement (flagged). |
| T3 | done (2026-10-18) | SF Travel monthly guides (official DMO) as enumeration backbone + organizer/official sites per event: chineseparade.com, uissf.org, sfpride.org, carnavalsanfrancisco.org, sfcherryblossom.org, folsomstreet.org, thesfmarathon.com, escapealcatraztri.com, fleetweeksf.org, hardlystrictlybluegrass.com, sfoutsidelands.com (via SFMTA advisory), stergrove.org, sf.aidswalk.net, sfballet.org, sfopera.com, sfsymphony.org, sfjazz.org, mlb.com/giants, sfitalianheritage.org, castrostreetfair.org, litquake.org, moonfestival.org, comedyday.org, dayofthedeadsf.org, embarcaderocenter.com, downtownsf.org, billgrahammenorah.org, koshercomedy.com, somapilipinas.org, sfport.com, sfmta.com, famsf.org, gggp.org, artspan.org and others (full per-row sources in data/events-annual.json) | 95 annual events verified; 2026 dates confirmed on official organizer/government sites where possible, otherwise via SF Travel official guides (noted in source_name). 2027 dates recorded only where officially announced (Pride, Cherry Blossom). | (1) Earth Day SF & Decorator Showcase 2026 dates unconfirmed (blank + flagged). (2) Union Square & Ghirardelli tree lightings "Date TBD" per SF Travel (blank + flagged); Embarcadero Center official site published Nov 18 (used). (3) Parol Festival 2026 date only as SOMA Pilipinas "Save the Date" (flagged). (4) NYE fireworks 2026/27 edition not yet on official City pages (flagged). (5) Muni Heritage Weekend SFMTA page is a prior-year edition; 2026 dates per SF Travel. (6) Giant Race 2026 date ambiguous across sources (excluded from table, logged). |
| T4 | done (2026-10-18) | sf.gov (July 4 Golden Gate Bridge fireworks event page), redbull.com, moscone.com, sanfranciscohistorium.com, sfopera.com (2026-27 season release), chasecenter.com/events, sfmoma.org, famsf.org, sunsetdunes.org, giantsenterprises/mlb.com (Ballpark Back 9), walksf.org, ybca.org, sfcheesefest.com, nexus-sfbay.com, clubdarc.com, sftravel.com guides | 38 special events verified (2026 one-offs, opera productions, concerts, exhibitions); upcoming (post-snapshot) events marked. | (1) Third-party claim of "Opera at the Ballpark Nov 11, 2026 (La Traviata)" contradicted by official SF Opera 2026-27 season; official simulcast page carries 2022 content — claim rejected & logged in exclusions. (2) Several special events sourced only via SF Travel guides (no dedicated organizer site) — flagged. (3) Opera Ball moved Sep 12 → Nov 12, 2026 (noted). |
| T5 | done (2026-10-18) | — (build) | Static site generated in docs/: dashboard (index) + weekly/annual/special category pages + Flagged for Review page; assets/style.css, assets/app.js (search & filters); data/events.json + events.csv. No external dependencies; all rows server-rendered. | None |
| T6 | done (2026-10-18) | — (verification) | tools/verify_site.py: (a) every table row in every page has an external source link; (b) all internal links/asset paths resolve; (c) every external link is https and on the official-domain allowlist; (d) every flagged event appears on Flagged for Review; (e) all pages contain full navigation. Result: 0 errors, 0 warnings. Also verified via local HTTP server: all 5 pages + 4 assets return 200; row counts match datasets (34/95/38); 147 verified + 20 flagged badges. | Fixed during pass: duplicate class attribute on active nav link (regenerated); verifier initially mis-counted thead rows and HTML-escaped names (verifier fixed, re-run clean). |
| T7 | in progress | (to be filled) | (to be filled) | (to be filled) |

## Publish log

| Step | Result | Link / detail |
|------|--------|---------------|
| Pull request to main | (pending) | |
| Merge | (pending) | |
| GitHub Pages enable (main /docs) | (pending) | |
| Pages build status | (pending) | |
| Live site confirmed | (pending) | |

