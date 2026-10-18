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
| T2 | Research & verify weekly/regularly recurring SF events | in progress | arena/4f47c142-maltaproj5 | data/events-weekly.json |
| T3 | Research & verify annually recurring SF events | in progress | arena/4f47c142-maltaproj5 | data/events-annual.json |
| T4 | Research & verify special (one-off/dated) SF events | in progress | arena/4f47c142-maltaproj5 | data/events-special.json |
| T5 | Build GitHub Pages site (landing page + category subpages + Flagged page) | in progress | arena/4f47c142-maltaproj5 | docs/ (all files), tools/build_site.py |
| T6 | Line-by-line verification pass: every table row sourced, no broken internal links | in progress | arena/4f47c142-maltaproj5 | docs/** (read-only check + fixes within own scope) |
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
| T2 | in progress | (to be filled) | (to be filled) | (to be filled) |
| T3 | in progress | (to be filled) | (to be filled) | (to be filled) |
| T4 | in progress | (to be filled) | (to be filled) | (to be filled) |
| T5 | in progress | (to be filled) | (to be filled) | (to be filled) |
| T6 | in progress | (to be filled) | (to be filled) | (to be filled) |
| T7 | in progress | (to be filled) | (to be filled) | (to be filled) |
