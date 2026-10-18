#!/usr/bin/env python3
"""Deterministic, offline static build. Only audited fields are rendered as facts.

Twelve root pages work under a GitHub Pages subpath, with or without JavaScript.
No live-calendar claims, name-matcher report, prose date parsing or fact fallback.
"""
from __future__ import annotations

import csv
import io
import json
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


rows, sources, findings, stats = (load(n) for n in ("events.json", "sources.json", "review.json", "audit_summary.json"))
listed = [r for r in rows if r["publication"] == "listed"]
lookup = {r["id"]: r for r in rows}
AS_OF = "18 October 2026"
FIELDS = ("name", "schedule", "time", "venue", "price")
LABELS = {"name": "Event name", "schedule": "Published schedule", "time": "Time", "venue": "Venue / area", "price": "Admission / conditions"}
NAV = [("index.html", "Overview"), ("weekly.html", "Weekly"), ("monthly.html", "Monthly"), ("annual.html", "Annual"), ("special.html", "Special & dated"), ("markets.html", "Markets & food"), ("museums.html", "Museums & science"), ("culture.html", "Festivals & culture"), ("community.html", "Community & outdoors"), ("analysis.html", "Analysis & findings"), ("review.html", "Flagged for Review"), ("sources.html", "Sources & evidence")]


def e(value):
    return escape(str(value), quote=True)


def display(row):
    return row["name"] or row["candidate_name"]


def official(sid, label=None):
    source = sources[sid]
    return f'<a class="official" href="{e(source["url"])}" rel="noreferrer">{e(label or source["publisher"])} <span aria-hidden="true">↗</span></a>'


def links(row):
    primary, *rest = row["sources"]
    extra = '<details class="more-links"><summary>More official pages</summary>' + '<br>'.join(official(s) for s in rest) + '</details>' if rest else ''
    return official(primary, "Official source") + f'<a class="evidence" href="sources.html#e-{e(row["id"])}">Field evidence →</a>' + extra


def write(filename, title, intro, body):
    navigation = ''.join(f'<a href="{f}"' + (' aria-current="page"' if f == filename else '') + f'>{e(label)}</a>' for f, label in NAV)
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · SF Events</title><meta name="description" content="{e(intro)}">
<link rel="icon" href="assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><script src="assets/app.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<aside><a class="brand" href="index.html"><span class="logo" aria-hidden="true">SF</span>Events<span class="dot">.</span></a>
<p class="eyebrow">A SOURCE-LINKED FIELD GUIDE</p><nav aria-label="Main navigation">{navigation}</nav>
<div class="sidebar-note">San Francisco city only<br>Research snapshot · {AS_OF}<br>Not an exhaustive or live calendar<br><a href="sources.html#method">Read the method →</a></div></aside>
<main id="main"><header><span>SAN FRANCISCO / RESEARCH INDEX</span><span>Snapshot: {AS_OF} · <a href="data/events.csv" download>Directory CSV ↓</a></span></header>
<section class="heading"><p class="eyebrow">CITY ONLY. SOURCES FIRST.</p><h1>{e(title)}</h1><p>{e(intro)}</p></section>
{body}
<footer>Bounded research, not citywide completeness. Event dates and times are local to San Francisco. Temporal labels use the fixed {AS_OF} snapshot, not today.<br>Blank cells are unverified, never free by default. <a href="review.html">Open questions</a> · <a href="sources.html#method">Evidence & method</a> · <a href="https://github.com/buffedlizard55-lab/MaltaProj5">Repository ↗</a></footer></main></body></html>'''
    (ROOT / filename).write_text(html + "\n")


def notice():
    return f'''<div class="notice"><b>Know what this directory does—and does not—confirm.</b>
{stats['listed']} entries have evidence-backed names, venues and San Francisco geography. Unconfirmed values stay blank and are flagged; a listing does not mean every detail is verified.
{stats['review_only']} candidates are held off the directory on <a href="review.html">Flagged for Review</a>.
“Future dated” means after {AS_OF}; it is not a real-time availability promise. Recurrence never generates a next date.</div>'''


def metrics(items):
    return '<section class="stats" aria-label="Inventory summary">' + ''.join(f'<article{(" class=" + chr(34) + "warn" + chr(34)) if warn else ""}><span>{e(title)}</span><strong>{e(value)}</strong><small>{e(detail)}</small></article>' for title, value, detail, warn in items) + '</section>'


def cards(items):
    return '<div class="cards">' + ''.join(f'<a href="{e(url)}"><span>{e(label)}</span><strong>{e(value)}</strong><small>{e(detail)} →</small></a>' for url, label, value, detail in items) + '</div>'


def date_text(row):
    spans = row["occurrences"]
    return '; '.join(x["start"] + ((' → ' + x["end"]) if x["end"] and x["end"] != x["start"] else (' · closing unconfirmed' if not x["end"] else '')) for x in spans)


def fact_cell(row, field):
    value = row[field]
    # Preserve actual empty cells. The review column identifies every missing field.
    return f'<td>{e(value)}</td>' if value else f'<td class="unknown" aria-label="{e(LABELS[field])}: unverified"></td>'


def table(items, review=False):
    items = list(items)
    tools = '''<div class="tools" id="table-tools" hidden>
<label for="search">Search entries<input id="search" type="search" placeholder="Event, venue, category…" autocomplete="off"></label>
<label for="kind">Cadence<select id="kind"><option value="">All cadences</option>''' + ''.join(f'<option>{k}</option>' for k in ("Weekly", "Monthly", "Annual", "Special", "Unverified")) + '''</select></label>
<label for="temporal">Date status<select id="temporal"><option value="">All dates</option>''' + ''.join(f'<option>{e(k)}</option>' for k in sorted({r["temporal_status"] for r in items})) + '''</select></label>
<label for="publication">Publication<select id="publication"><option value="">All entries</option><option value="listed">In directory</option><option value="review_only">Held for review</option></select></label>
<button type="button" id="reset">Reset</button><span id="count" role="status" aria-live="polite">''' + f'{len(items)} of {len(items)} entries</span></div>'
    out = [tools, '<p class="table-hint">Blank cells are unverified. Open “Field evidence” for quotations. On narrow screens, scroll the table horizontally.</p>', '<div class="table-wrap" tabindex="0" role="region" aria-label="Source-linked event table"><table id="events">', f'<caption>{len(items)} {"candidate" if review else "directory"} entries · snapshot {AS_OF} · categories and programme relationships are editorial, not unique-event counts.</caption>', '<thead><tr><th scope="col">Event / programme</th><th scope="col">Published schedule</th><th scope="col">Time</th><th scope="col">Venue / area</th><th scope="col">Admission / conditions</th><th scope="col">Cadence & date status</th><th scope="col">Review notes</th><th scope="col">Official sources</th></tr></thead><tbody>']
    for row in items:
        rid = e(row["id"])
        candidate = '<span class="candidate-label">Unverified inherited identifier—not a confirmed event name</span>' if not row["name"] else ''
        parent = f'<small>Part of: <a href="review.html#{e(row["parent"])}">{e(display(lookup[row["parent"]]))}</a></small>' if row["parent"] else ''
        missing = ', '.join(x.split(':')[0] for x in row["unverified"])
        notes = row["flags"] + ([row["notes"]] if row["notes"] else [])
        details = f'<details><summary>{e("Unverified: " + missing if missing else "Context & qualifications")}</summary>' + ''.join(f'<p>{e(n)}</p>' for n in notes) + ('<ul>' + ''.join(f'<li>{e(n)}</li>' for n in row["unverified"]) + '</ul>' if missing else '') + f'<a href="review.html#{rid}">Review record →</a></details>'
        first_links = '<small class="event-links">' + official(row['sources'][0], 'Official source') + f' · <a href="sources.html#e-{rid}">Evidence</a></small>'
        disposition = '<span class="check flag">Held for review</span>' if row["publication"] == 'review_only' else '<span class="check ok">SF location evidenced</span>'
        dates = f'<small class="normalized">Approved dates: {e(date_text(row))}</small>' if row["occurrences"] else ''
        kind = 'Special / cadence unconfirmed' if row["kind"] == 'Special' else row["kind"]
        state_cls = 'past' if row["temporal_status"] == 'Past dated' else 'future' if row["temporal_status"] == 'Future dated' else 'neutral'
        out.append(f'<tr id="{rid}" data-kind="{e(row["kind"])}" data-temporal="{e(row["temporal_status"])}" data-publication="{e(row["publication"])}"><th scope="row">{e(display(row))}{candidate}<small>{e(row["category"])} · {e(row["entry_type"])}</small>{parent}{first_links}</th>')
        out.append(f'<td>{e(row["schedule"])}{dates}</td>' if row['schedule'] else '<td class="unknown" aria-label="Published schedule: unverified"></td>')
        out.extend(fact_cell(row, field) for field in ("time", "venue", "price"))
        out.append(f'<td>{e(kind)}<span class="temporal {state_cls}">{e(row["temporal_status"])}</span></td><td>{disposition}{details}</td><td>{links(row)}</td></tr>')
    out += ['</tbody></table></div>', '<p id="empty" class="notice" role="status" hidden>No matching entries. Try fewer filters or reset the table.</p>']
    return ''.join(out)


kind_counts = Counter(r["kind"] for r in listed)
cat_counts = Counter(r["category"] for r in listed)
body = metrics([
    ("City-only directory", stats["listed"], f'{stats["series"]} programme umbrellas included', False),
    ("Recurring entries", sum(kind_counts[k] for k in ("Weekly", "Monthly", "Annual")), "Cadence requires its own evidence", False),
    ("Future dated", stats["temporal"].get("Future dated", 0), f"Relative to {AS_OF}, not live", False),
    ("Held for review", stats["review_only"], "Not included in directory totals", True),
    ("Official source URLs", stats["source_urls"], f'{stats["domains"]} distinct domains; not organizations', False),
    ("Candidates assessed", stats["candidates"], f'{stats["inherited_candidates"]} inherited + {stats["new_entries"]} new', False),
]) + notice()
body += '<section class="intro"><h2>Find your rhythm</h2><p>Documented recurring patterns are separate from dated programmes whose ongoing cadence is not confirmed.</p>' + cards([(f, label, kind_counts[k], "Browse source-linked entries") for f, label, k in [("weekly.html", "Weekly", "Weekly"), ("monthly.html", "Monthly", "Monthly"), ("annual.html", "Annual", "Annual"), ("special.html", "Special & dated", "Special")]]) + '</section>'
body += '<h2>Explore by category</h2>' + cards([(f, c, cat_counts[c], "Browse the directory") for f, c in [("markets.html", "Markets & food"), ("museums.html", "Museums & science"), ("culture.html", "Festivals & culture"), ("community.html", "Community & outdoors")]])
body += '<h2>City-only directory</h2>' + table(listed)
write("index.html", "San Francisco, in events.", "Recurring gatherings, cultural traditions and special programmes—organized around official evidence, with uncertainty kept visible.", body)

for filename, kind, title in [("weekly.html", "Weekly", "A weekly rhythm."), ("monthly.html", "Monthly", "Once a month. Or twice."), ("annual.html", "Annual", "Traditions that return."), ("special.html", "Special", "Special & dated programmes.")]:
    description = "Only source-supported recurring classifications appear here. Seasonal exceptions apply; a pattern never proves the next occurrence." if kind != "Special" else "Dated editions and programme umbrellas without an approved ongoing cadence. “Special” does not claim an event will never recur. Past editions remain clearly labeled."
    write(filename, title, description, notice() + table([r for r in listed if r["kind"] == kind]))

for filename, category in [("markets.html", "Markets & food"), ("museums.html", "Museums & science"), ("culture.html", "Festivals & culture"), ("community.html", "Community & outdoors")]:
    write(filename, category + ".", "An editorial category of city-only entries. Prices, eligibility, dates and unresolved questions remain attached to their official sources.", notice() + table([r for r in listed if r["category"] == category]))


def plain(headers, values):
    return '<div class="table-wrap"><table class="plain"><thead><tr>' + ''.join(f'<th scope="col">{e(h)}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{e(v)}</td>' for v in row) + '</tr>' for row in values) + '</tbody></table></div>'


analysis_intro = f'''<section class="prose"><h2>What the register can tell us</h2><p>{stats['candidates']} candidate entries were assessed. {stats['listed']} meet the directory’s name, venue and SF-geography gate; {stats['review_only']} are held for review. These are <b>entries, not unique events</b>: {stats['series']} listed programme umbrellas overlap their dated children. This is not a random sample of San Francisco activity.</p>
<p>Counts describe this dataset only. They cannot establish citywide event frequency, neighborhood equity, attendance, economic impact, or that one category dominates the city.</p></section>'''
body = analysis_intro + '<h2>Directory composition</h2>' + plain(["Documented cadence / editorial grouping", "Entries"], [(k, kind_counts[k]) for k in ("Weekly", "Monthly", "Annual", "Special")])
body += '<h2>Dates, without invention</h2>' + plain([f"Temporal status at {AS_OF}", "Directory entries"], sorted(stats["temporal"].items()))
body += '<h2>Unconfirmed fields stay blank</h2>' + plain(["Field", "Blank cells in the directory"], [(LABELS[k], stats["blank_fields"][k]) for k in FIELDS])
body += '<section class="prose"><p>Only explicit approved ISO dates drive date labels. An exhibition with only an opening date has no fabricated closing date. Ongoing admission policies and recurring markets do not automatically receive a dated next occurrence.</p><h2>Biases and limits</h2><ul><li>Official web calendars favor larger, web-visible institutions; small community, faith, nightlife and pop-up gatherings are underrepresented.</li><li>Blocked and JavaScript-only pages reduce readable evidence. Their candidates are not proof of nonexistence and are not silently counted as verified.</li><li>Regional festivals need venue-level separation. A San Francisco brand does not place every performance inside the city.</li><li>Domain counts are not counts of organizers. A .org suffix is not evidence of nonprofit legal status; no such inference is made.</li><li>Snapshot dates are not live ticket availability, cancellations or a guarantee that a source has not changed.</li></ul><h2>Next research priorities</h2><p>Isolate SF-only regional screenings; verify individual sports fixtures, theater/music performances, civic and faith calendars; resolve conflicting hours/street extents; revisit unreadable primary pages. Coverage is intentionally described as incomplete.</p><p><a href="review.html">All candidates and open questions →</a> · <a href="data/audit_summary.json">Machine-readable summary</a></p></section>'
write("analysis.html", "Findings, not false certainty.", "A reproducible view of coverage, missing values, date quality and research limitations—not a statistical portrait of the whole city.", body)

body = metrics([("Held off the directory", stats["review_only"], "Venue / geography / evidence unresolved", True), ("Listed with unconfirmed fields", stats["listed_with_blanks"], "Fields remain blank, never guessed", True), ("Candidates retained", stats["candidates"], "No unresolved candidate silently discarded", False)])
body += '<section class="prose"><p><b>This page includes every candidate.</b> Filter Publication to “Held for review” to isolate quarantined entries. Candidate identifiers are preserved for traceability; where the event name itself is unconfirmed, the inherited title is explicitly labeled as an unverified identifier. They are not assertions of a real event, date or SF location.</p><p><a href="data/review.csv" download>Download all review records (CSV) ↓</a> · <a href="data/unverified_history.json">Unverified inherited history</a></p></section>'
for i, finding in enumerate(findings, 1):
    body += f'<section class="prose finding" id="finding-{i}"><h2>{e(finding["title"])}</h2><p>{e(finding["detail"])}</p></section>'
exclusions = load("exclusions.json")
body += '<section class="prose"><h2>Out-of-city exclusions</h2><p>Examples include Levi’s Stadium in Santa Clara and the Cow Palace in Daly City. Historical exclusion records remain in <a href="data/exclusions.json">the exclusion log</a>. Regional/mixed-city candidates are held for review rather than admitted wholesale.</p></section>'
body += '<h2>Candidate review register</h2>' + table(rows, review=True)
write("review.html", "Flagged for Review.", "Unverified fields, unresolved conflicts and candidates held off the city-only directory—published openly, with official links for manual checking.", body)

METHOD = '''<section class="prose" id="method"><h2>How evidence becomes a published field</h2><ol>
<li>Historical inputs are consolidated into candidates and saved as <b>unverified history</b>, not trusted facts.</li>
<li>Official organizer, venue, museum and government pages are read in context. Public-tourism sources are discovery/reference material, not a substitute for missing event details.</li>
<li>Each accepted name, schedule, time, venue, admission condition, recurrence and occurrence date has an explicit decision and source quotation. Structured event JSON-LD is labeled separately from readable page text. Selected tool excerpts are not represented as complete raw page captures.</li>
<li>The build starts every factual field blank and copies only approved decisions. Name, venue and documented SF geography are required for directory admission. Other unknowns remain blank and flagged. Geography can identify a recognized SF venue from its official address/directions; it is never inferred from a stray city token in unrelated marketing.</li>
<li>Exact-quote checks test provenance, <b>not semantic truth</b>. Context, edition, eligibility and conflicting copy require a research judgment. A URL/status/name match never verifies the rest of a row.</li>
<li>Only explicitly approved ISO occurrences determine labels relative to the fixed snapshot. URL slugs, weekdays, copyright dates and neighboring events never supply missing years. Recurrence evidence does not generate future dates.</li>
</ol><p>Times are local to San Francisco. Free parking, free activities with paid entry, and virtual tickets do not establish free physical admission. Conditions such as residency, age, surcharges and RSVP remain visible.</p>
<p>Evidence snapshot: <a href="data/audit_64f8b973.json">archived captures and explicit decisions (JSON)</a>. Original HTTP status and later attempt metadata remain separate; failed refreshes do not erase prior readable evidence. This is not continuous re-verification.</p>
<p><a href="data/events.json">All audited records</a> · <a href="data/sources.json">Source ledger</a> · <a href="data/events.csv">Directory CSV</a> · <a href="data/review.csv">Review CSV</a> · <a href="data/unverified_history.json">UNVERIFIED inherited history</a></p></section>'''


def quotations(quotes):
    out = []
    for q in quotes:
        sid = next(k for k, s in sources.items() if s["url"] == q["url"])
        fmt = 'event JSON-LD' if q.get('format') == 'jsonld' else 'page text / selected excerpt'
        out.append(f'<blockquote><p>{e(q["text"])}</p><cite>{official(sid)} · {fmt}</cite></blockquote>')
    return ''.join(out)


body = METHOD + '<h2>Row-by-row field evidence</h2><p>Only the values shown below are approved facts. A blank field remains unverified, even when the page or event name is confirmed. Read the full linked page to check current context.</p>'
for row in rows:
    body += f'<article class="source row-evidence" id="e-{e(row["id"])}"><h3>{e(display(row))}</h3><p>{e(row["publication"])} · reviewed {e(row["audit"]["reviewed_at"])} · <a href="review.html#{e(row["id"])}">Review record</a></p>'
    if not row['name']:
        body += '<p class="candidate-label">Heading is an unverified inherited identifier, not an approved event name.</p>'
    for field in FIELDS:
        fact = row['field_evidence'].get(field)
        body += f'<details><summary>{e(LABELS[field])}: {e(fact["value"]) if fact else "unverified (blank)"}</summary>' + (quotations(fact['quotes']) if fact else '<p>No value approved; inherited claims are not a fallback.</p>') + '</details>'
    if row['recurrence']:
        body += '<details><summary>Recurrence evidence</summary>' + quotations(row['recurrence']['quotes']) + '</details>'
    body += '<details><summary>City-only geography</summary><p>' + e(row['geography']['basis']) + '</p>' + quotations(row['geography']['quotes']) + '</details>'
    for occurrence in row['occurrences']:
        body += f'<details><summary>Approved occurrence: {e(occurrence["start"])}' + (f' → {e(occurrence["end"])}' if occurrence['end'] else ' · closing unconfirmed') + '</summary>' + quotations(occurrence['quotes']) + '</details>'
    body += '</article>'
body += '<h2>Exact-URL source ledger</h2><p>Source count is distinct cited URLs, not organizations or unique domains. A successful request is not a field approval; blocks and errors are not dead-link verdicts.</p>'
for sid, source in sources.items():
    http = source['http'] if source['http'] is not None else 'not captured by runner'
    method = ' · independent selected tool excerpt read ' + source['tool_checked_at'] if source['tool_excerpt_available'] else ''
    body += f'<article class="source" id="s-{e(sid)}"><h3>{official(sid, source["title"])}</h3><p>{e(source["url"])}</p><p>Archived runner status: {e(http)} · capture timestamp: {e(source["captured_at"] or "not recorded")}{method}. Referenced by {len(source["approved_for_rows"])} explicit row decisions; this does not certify every field or current page content.</p></article>'
write("sources.html", "A trail back to the source.", "Explicit field decisions and quotations, not inherited verification badges. Every candidate keeps official links for manual review.", body)


def csv_value(value):
    value = str(value)
    return "'" + value if value.startswith(('=', '+', '-', '@')) else value


def export(filename, items, review=False):
    columns = ['id', 'name', 'schedule', 'time', 'venue', 'price', 'kind', 'entry_type', 'parent', 'category', 'publication', 'temporal_status', 'approved_dates', 'unverified', 'review_notes', 'official_source_urls', 'as_of']
    if review:
        columns.insert(1, 'candidate_identifier_unverified')
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=columns, lineterminator='\n')
    writer.writeheader()
    for row in items:
        record = {key: row.get(key, '') for key in columns}
        record.update(approved_dates=date_text(row), unverified='; '.join(row['unverified']), review_notes='; '.join(row['flags'] + ([row['notes']] if row['notes'] else [])), official_source_urls=' | '.join(sources[s]['url'] for s in row['sources']))
        if review:
            record['candidate_identifier_unverified'] = row['candidate_name']
        writer.writerow({key: csv_value(value) for key, value in record.items()})
    (ROOT / 'data' / filename).write_text(stream.getvalue())


export('events.csv', listed)
export('review.csv', rows, review=True)
analysis_md = f'''# Analysis — bounded SF event research snapshot

As of {AS_OF}. This is not a complete or live city calendar.

- {stats['candidates']} candidate entries assessed: {stats['inherited_candidates']} inherited and {stats['new_entries']} new official-calendar entries.
- {stats['listed']} admitted to the city-only directory; {stats['review_only']} held for review.
- {stats['series']} listed programme umbrellas overlap child events. These totals are **not unique-event counts**.
- {stats['source_urls']} exact cited URLs across {stats['domains']} domains. Domains are not organizations or nonprofit status.
- Cadence: {kind_counts['Weekly']} weekly / {kind_counts['Monthly']} monthly / {kind_counts['Annual']} annual / {kind_counts['Special']} special or cadence-unconfirmed.

## Blank factual fields in the directory

''' + '\n'.join(f'- {LABELS[k]}: {stats["blank_fields"][k]}' for k in FIELDS) + '\n\n## Temporal labels (fixed snapshot)\n\n' + '\n'.join(f'- {k}: {v}' for k, v in sorted(stats['temporal'].items())) + '''

## Interpretation and gaps

Official web visibility biases this non-random sample toward larger institutions.
No citywide density, neighborhood equity, attendance or impact claim can be made.
Small community/faith/pop-up events, sports fixtures, individual arts performances,
and civic calendars remain incomplete. Regional festivals require SF-only components.
Blocked/JS-only responses and conflicting copy remain visible in the review register.
No year is supplied by URL, weekday, copyright or unrelated neighboring event.
No next occurrence is generated from a weekly/monthly/annual pattern.

See [Flagged for Review](review.html), [field evidence](sources.html),
[the summary JSON](data/audit_summary.json) and [unverified history](data/unverified_history.json).
'''
(ROOT / 'ANALYSIS.md').write_text(analysis_md)
print(f'Built 12 HTML pages, {len(listed)} directory rows, {len(rows)} review records, CSVs and ANALYSIS.md from audited data only.')
