# COORDINATION.md — Shared Task Board

This file is the shared task board for every agent session working in `buffedlizard55-lab/MaltaProj5`.
Rules:

1. Read this file **before** starting work. Never start a task another session has claimed.
2. Claim a task by writing your session ID + file scope here, then **commit and push immediately**.
3. Keep scopes non-overlapping — edit only files inside your claimed scope.
4. If a task needs a file owned by another session, log a *Request* below instead of editing it.
5. Small, frequent commits. `git pull --rebase` before every push.
6. When finished: record sources, verification performed, irregularities, then mark **done**.
7. Never mark anything *verified* without checking it against an official source and linking it.
8. A claim older than 60 minutes with no commits may be taken over — note the handoff in the log.

Status vocabulary: `unclaimed` · `in progress` · `done` · `needs review`
(`needs review` = published on the *Flagged for Review* page; it does not block anything.)

---

## Session registry

| Session ID | Branch | Started (UTC) | Last commit (UTC) | Notes |
|---|---|---|---|---|
| `arena-5a85baf2` | `arena/5a85baf2-maltaproj5` | 2026-10-18 00:54 | see git log | Sole active session. Acting as research **and** final integration session. |

> **Branch policy note (important).** The Arena sandbox pins this session to the branch
> `arena/5a85baf2-maltaproj5`, so the `session-<id>/<task>` branch naming convention cannot be used
> here. All work for every task below happens on `arena/5a85baf2-maltaproj5`; task scopes are still
> kept non-overlapping at the file level so the board stays meaningful for other sessions.

---

## Task board

| # | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Repo review + set up coordination board | in progress | `arena-5a85baf2` | `COORDINATION.md`, `README.md` |
| T2 | Research & verify **recurring weekly/monthly** events | in progress | `arena-5a85baf2` | `data/recurring.json`, `SOURCES.md` |
| T3 | Research & verify **recurring annual** events | in progress | `arena-5a85baf2` | `data/annual.json`, `SOURCES.md` |
| T4 | Research & verify **special / dated** events (2026–2027) | in progress | `arena-5a85baf2` | `data/special.json`, `SOURCES.md` |
| T5 | Flag unverified / irregular rows | in progress | `arena-5a85baf2` | `data/flagged.json`, `docs/flagged.html` |
| T6 | Build GitHub Pages site (landing + category subpages) | in progress | `arena-5a85baf2` | `docs/**` |
| T7 | Analysis + findings write-up | in progress | `arena-5a85baf2` | `docs/analysis.html`, `ANALYSIS.md` |
| T8 | Link check + build check | in progress | `arena-5a85baf2` | `tools/linkcheck.py`, `tools/validate.py` |
| T9 | Final integration: re-verify combined data, publish Pages | unclaimed | — | all |
| T10 | Open PR → `main`, merge, confirm Pages deploy | unclaimed | — | `COORDINATION.md` |

---

## Cross-session requests

_None._

---

## Work log

### 2026-10-18 — `arena-5a85baf2`

- **T1 done.** Repo review: at commit `20813bf` ("Initial commit") the repository contained exactly
  one file, `README.md`, whose entire content was `# MaltaProj5`. No data, no site, no prior event
  list, no `.github/` workflows, no `docs/`. `gh api repos/buffedlizard55-lab/MaltaProj5/pages`
  returned `404 Not Found` → GitHub Pages was **not** enabled before this session. Nothing to
  reconcile, no other session claims existed. Board created and pushed.
- Next: research + verification passes (T2–T5), site build (T6–T8), integration (T9–T10).
## Deliverables & verification record

| Artifact | Verification performed | Result |
|---|---|---|
| `data/*.json` (event rows) | Each row's `source_url` fetched and checked for the event name + cadence/date | see per-row `verified` field |
| `docs/**` (site) | `tools/linkcheck.py` — internal href integrity, no 404s | _pending_ |
| `tools/validate.py` | schema: required fields present, `source_url` non-empty, geography = SF | _pending_ |

## PR / merge record

- PR: _filled in at merge time_
- Merge: _filled in at merge time_
- Pages URL: _filled in after deploy_
