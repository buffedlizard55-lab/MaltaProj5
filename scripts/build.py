#!/usr/bin/env python3
"""Deterministic, offline static build. Only audited fields are rendered as facts.

Nineteen root pages work under a GitHub Pages subpath, with or without JavaScript:
a free-first landing dashboard (executive summary and main section carry free
upcoming events only), a date-ordered Upcoming page, the cadence pages, the topic
pages requested for this project (gaming, music, AI and free-to-attend), a separate
Paid events section, and the evidence pages. No live-calendar claims, name-matcher
report, prose date parsing or fact fallback.
"""
from __future__ import annotations

import csv
import io
import json
import sys
from collections import Counter
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from register_3adf31d9 import cost_of, next_date, topic_of  # noqa: E402


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


rows, sources, findings, stats = (load(n) for n in ("events.json", "sources.json", "review.json", "audit_summary.json"))
listed = [r for r in rows if r["publication"] == "listed"]
held = [r for r in rows if r["publication"] == "review_only"]
lookup = {r["id"]: r for r in rows}
AS_OF = "18 October 2026"
SNAPSHOT = date(2026, 10, 18)
FIELDS = ("name", "schedule", "time", "venue", "price")
LABELS = {"name": "Event name", "schedule": "Published schedule", "time": "Time", "venue": "Venue / area", "price": "Admission / conditions"}
NAV = [
    ("index.html", "Overview"), ("upcoming.html", "Upcoming"), ("free.html", "Free to attend"), ("paid.html", "Paid events"),
    ("gaming.html", "Gaming"), ("music.html", "Music"), ("ai.html", "AI & technology"), ("focus.html", "Focus, one page"),
    ("weekly.html", "Weekly"), ("monthly.html", "Monthly"), ("annual.html", "Annual"), ("special.html", "Special & dated"),
    ("markets.html", "Markets & food"), ("museums.html", "Museums & science"), ("culture.html", "Festivals & culture"), ("community.html", "Community & outdoors"),
    ("analysis.html", "Analysis & findings"), ("review.html", "Flagged for Review"), ("sources.html", "Sources & evidence"),
]
TOPIC_PAGES = [("gaming.html", "Gaming"), ("music.html", "Music"), ("ai.html", "AI & technology")]


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


def cost_badge(row):
    """A label over the verified admission text. The exact wording is always shown."""
    badge, conditions = cost_of(row)
    cls = {"Free": "free", "Paid": "paid", "Not stated": "unknown", "See source": "unknown"}[badge]
    label = "Not stated" if badge == "Not stated" else badge
    note = '<small>Conditions apply — read the exact wording</small>' if conditions else ''
    return f'<span class="cost {cls}">{e(label)}</span>{note}'


def fact_cell(row, field):
    value = row[field]
    # Preserve actual empty cells. The review column identifies every missing field.
    return f'<td data-label="{e(LABELS[field])}">{e(value)}</td>' if value else f'<td class="unknown" data-label="{e(LABELS[field])}" aria-label="{e(LABELS[field])}: unverified"></td>'


TABLE_SEQUENCE = [0]


def table(items, review=False, nexts=None):
    items = list(items)
    nexts = nexts or {}
    TABLE_SEQUENCE[0] += 1
    n = str(TABLE_SEQUENCE[0])
    tools = f'''<div class="tools" id="table-tools-{n}" hidden>
<label for="search-{n}">Search entries<input id="search-{n}" type="search" placeholder="Event, venue, category…" autocomplete="off"></label>
<label for="kind-{n}">Cadence<select id="kind-{n}"><option value="">All cadences</option>''' + ''.join(f'<option>{k}</option>' for k in ("Weekly", "Monthly", "Annual", "Special", "Unverified")) + f'''</select></label>
<label for="temporal-{n}">Date status<select id="temporal-{n}"><option value="">All dates</option>''' + ''.join(f'<option>{e(k)}</option>' for k in sorted({r["temporal_status"] for r in items})) + f'''</select></label>
<label for="cost-{n}">Cost<select id="cost-{n}"><option value="">All costs</option><option value="Free">Free</option><option value="Paid">Paid</option><option value="See source">See source</option><option value="Not stated">Not stated</option></select></label>
<label for="publication-{n}">Publication<select id="publication-{n}"><option value="">All entries</option><option value="listed">In directory</option><option value="review_only">Held for review</option></select></label>
<button type="button" id="reset-{n}">Reset</button><span id="count-{n}" role="status" aria-live="polite">''' + f'{len(items)} of {len(items)} entries</span></div>'
    out = [tools, '<p class="table-hint">Blank cells are unverified. Open “Field evidence” for quotations. On narrow screens each entry becomes a labelled card.</p>', f'<div class="table-wrap" tabindex="0" role="region" aria-label="Source-linked event table"><table class="events" id="events-{n}">', f'<caption>{len(items)} {"candidate" if review else "directory"} entries · snapshot {AS_OF} · categories, topics and programme relationships are editorial, not unique-event counts.</caption>', '<thead><tr><th scope="col">Event / programme</th><th scope="col">Cost</th><th scope="col">Published schedule</th><th scope="col">Time</th><th scope="col">Venue / area</th><th scope="col">Admission / conditions</th><th scope="col">Cadence & date status</th><th scope="col">Review notes</th><th scope="col">Official sources</th></tr></thead><tbody>']
    for row in items:
        rid = e(row["id"])
        candidate = '<span class="candidate-label">Unverified inherited identifier—not a confirmed event name</span>' if not row["name"] else ''
        parent = ''
        if row['parent']:
            parent = '<small>Part of: <a href="review.html#' + e(row['parent']) + '">' + e(display(lookup[row['parent']])) + '</a></small>'
        missing = ', '.join(x.split(':')[0] for x in row["unverified"])
        notes = row["flags"] + ([row["notes"]] if row["notes"] else [])
        details = f'<details><summary>{e("Unverified: " + missing if missing else "Context & qualifications")}</summary>' + ''.join(f'<p>{e(n)}</p>' for n in notes) + ('<ul>' + ''.join(f'<li>{e(n)}</li>' for n in row["unverified"]) + '</ul>' if missing else '') + f'<a href="review.html#{rid}">Review record →</a></details>'
        first_links = '<small class="event-links">' + official(row['sources'][0], 'Official source') + f' · <a href="sources.html#e-{rid}">Evidence</a></small>'
        disposition = '<span class="check flag">Held for review</span>' if row["publication"] == 'review_only' else '<span class="check ok">SF location evidenced</span>'
        dates = f'<small class="normalized">Approved dates: {e(date_text(row))}</small>' if row["occurrences"] else ''
        kind = 'Special / cadence unconfirmed' if row["kind"] == 'Special' else row["kind"]
        state_cls = 'past' if row["temporal_status"] == 'Past dated' else 'future' if row["temporal_status"] == 'Future dated' else 'neutral'
        upcoming = nexts.get(row["id"])
        soon = ' class="soon"' if upcoming and upcoming[2] <= 14 else ''
        countdown = f'<small class="normalized">{e(upcoming[3])}</small>' if upcoming else ''
        out.append(f'<tr id="{rid}"{soon} data-kind="{e(row["kind"])}" data-cost="{e(cost_of(row)[0])}" data-temporal="{e(row["temporal_status"])}" data-publication="{e(row["publication"])}"><th scope="row">{e(display(row))}{candidate}<small>{e(row["category"])} · {e(topic_of(row))} · {e(row["entry_type"])}</small>{parent}{first_links}</th>')
        out.append(f'<td data-label="Cost">{cost_badge(row)}</td>')
        out.append(f'<td data-label="Published schedule">{e(row["schedule"])}{dates}</td>' if row['schedule'] else '<td class="unknown" data-label="Published schedule" aria-label="Published schedule: unverified"></td>')
        out.extend(fact_cell(row, field) for field in ("time", "venue", "price"))
        out.append(f'<td data-label="Cadence &amp; date status">{e(kind)}<span class="temporal {state_cls}">{e(row["temporal_status"])}</span>{countdown}</td><td data-label="Review notes">{disposition}{details}</td><td data-label="Official sources">{links(row)}</td></tr>')
    out += ['</tbody></table></div>', f'<p id="empty-{n}" class="notice" role="status" hidden>No matching entries. Try fewer filters or reset the table.</p>']
    return ''.join(out)


# ---------------------------------------------------------------- date ordering
def upcoming_index():
    """Map row id -> (start ISO, days from snapshot, day bucket, human countdown).

    Only approved ISO occurrences participate. A recurring pattern never
    generates a next date, and a yearless date is never promoted.
    """
    index = {}
    for row in listed:
        value = next_date(row)
        if not value:
            continue
        start = date.fromisoformat(value)
        days = (start - SNAPSHOT).days
        if days < 0:
            label = "Happening now (started " + start.strftime("%-d %b %Y") + ")"
        elif days == 0:
            label = "Today · " + start.strftime("%a %-d %b %Y")
        elif days == 1:
            label = "Tomorrow · " + start.strftime("%a %-d %b %Y")
        else:
            label = f"In {days} days · " + start.strftime("%a %-d %b %Y")
        index[row["id"]] = (value, start, days, label)
    return index


UPCOMING = upcoming_index()
dated = sorted((r for r in listed if r["id"] in UPCOMING), key=lambda r: (UPCOMING[r["id"]][0], display(r).casefold()))
recurring_no_date = sorted((r for r in listed if r["id"] not in UPCOMING and r["kind"] in ("Weekly", "Monthly", "Annual")), key=lambda r: display(r).casefold())
undated_special = sorted((r for r in listed if r["id"] not in UPCOMING and r["kind"] not in ("Weekly", "Monthly", "Annual")), key=lambda r: display(r).casefold())


def bucket_of(days):
    if days < 0:
        return "Open now"
    if days == 0:
        return "Today"
    if days <= 7:
        return "Next 7 days"
    if days <= 30:
        return "Next 30 days"
    if days <= 90:
        return "Next 90 days"
    return "Later"


BUCKETS = ["Open now", "Today", "Next 7 days", "Next 30 days", "Next 90 days", "Later"]
bucket_counts = Counter(bucket_of(UPCOMING[r["id"]][2]) for r in dated)


def countdown_list(items, limit=None):
    """Executive-summary list. Not a table: the directory table owns the row ids."""
    out = ['<ol class="timeline">']
    for row in items[:limit] if limit else items:
        rid = e(row["id"])
        value, start, days, label = UPCOMING[row["id"]]
        badge, _ = cost_of(row)
        cls = {"Free": "free", "Paid": "paid", "Not stated": "unknown", "See source": "unknown"}[badge]
        soon = ' class="soon"' if days <= 14 else ''
        venue = e(row["venue"] or "Venue unverified — see the official page")
        out.append(f'<li{soon}><a href="upcoming.html#{rid}">{e(display(row))}</a>'
                   f'<span class="when">{e(label)}</span>'
                   f'<span class="cost {cls}">{e("Not stated" if badge == "Not stated" else badge)}</span>'
                   f'<small>{venue}{(" · " + e(row["time"])) if row["time"] else ""}</small>'
                   f'<span class="go">{official(row["sources"][0], "Official source")}</span></li>')
    out.append('</ol>')
    return ''.join(out)


kind_counts = Counter(r["kind"] for r in listed)
cat_counts = Counter(r["category"] for r in listed)
topic_counts = Counter(topic_of(r) for r in listed)
cost_counts = Counter(cost_of(r)[0] for r in listed)
free_rows = [r for r in listed if cost_of(r)[0] == "Free"]
# Free-first ordering (session 21f3dd85, T38): free events for gaming, music and
# AI first, then everything else; dated entries always nearest first inside that.
FOCUS_ORDER = {"Gaming": 0, "Music": 1, "AI & technology": 2, "Other": 3}
free_dated = [r for r in dated if cost_of(r)[0] == "Free"]  # `dated` is already nearest-first
free_recurring = sorted(
    (r for r in free_rows if r["id"] not in UPCOMING and r["kind"] in ("Weekly", "Monthly", "Annual")),
    key=lambda r: (FOCUS_ORDER[topic_of(r)], {"Weekly": 0, "Monthly": 1, "Annual": 2}[r["kind"]], display(r).casefold()))
free_focus = sorted(free_rows, key=lambda r: (
    FOCUS_ORDER[topic_of(r)],
    UPCOMING.get(r["id"], ("", date.max, 10**6, ""))[1],
    display(r).casefold()))
paid_rows = sorted((r for r in listed if cost_of(r)[0] == "Paid"), key=lambda r: (
    r["id"] not in UPCOMING,
    UPCOMING.get(r["id"], ("", date.max, 10**6, ""))[1],
    display(r).casefold()))

# ------------------------------------------------------------------- dashboard
# Free-first dashboard (session 21f3dd85, T38): the executive summary and the main
# section carry FREE upcoming events only. The full directory (all costs) stays on
# the Focus and Upcoming pages; paid events sit in their own section (paid.html).
free_next14 = sum(1 for r in free_dated if UPCOMING[r["id"]][2] <= 14)
until14 = date.fromordinal(SNAPSHOT.toordinal() + 14).strftime("%-d %B %Y")
summary_intro = (f"Free first: {len(free_dated)} events that are stated free on their official page also carry a "
                 f"confirmed date on or after the {AS_OF} snapshot (or an event still open then). They lead this page in date order, nearest "
                 f"first. {free_next14} of them fall on or before {until14}. A further {len(free_recurring)} free "
                 "entries have recurring patterns but no confirmed next date; they are kept on the Free to attend "
                 "and cadence pages, not listed here as upcoming. Paid events are collected "
                 "in a separate section and never mixed into this page.")


def nearest_free_callout(topic):
    dated_items = [r for r in free_dated if topic_of(r) == topic]
    n_free = sum(1 for r in free_rows if topic_of(r) == topic)
    if dated_items:
        row = dated_items[0]
        return (f"<b>{e(topic)}:</b> nearest free dated entry is {e(display(row))} "
                f"({e(UPCOMING[row['id']][3])}); {n_free} free entries in all")
    return (f"<b>{e(topic)}:</b> no free entry with a confirmed date yet; "
            f"{n_free} free entries recur or are undated")


focus_callout = ('<p class="topic-note">Focus topics — '
                 + "; ".join(nearest_free_callout(t) for t in ("Gaming", "Music", "AI & technology"))
                 + '. <a href="gaming.html">Gaming</a> · <a href="music.html">Music</a> · '
                   '<a href="ai.html">AI &amp; technology</a></p>')
body = metrics([
    ("Free upcoming events", len(free_dated), "Free and dated — nearest first below", False),
    ("Free to attend", len(free_rows), "Stated free on the official page", False),
    ("City-only directory", stats["listed"], f'{stats["series"]} programme umbrellas included', False),
    ("Paid events", len(paid_rows), "Separate section; exact quoted prices", False),
    ("Admission not stated", cost_counts.get("Not stated", 0), "Blank — never assumed free", True),
    ("Held for review", stats["review_only"], "Not included in directory totals", True),
]) + notice()
body += (f'<section class="intro" id="executive-summary"><h2>Executive summary</h2><p>{e(summary_intro)}</p>'
         f'<p><b>Next 14 days.</b> {free_next14} free entries have a confirmed date on or before {e(until14)}. '
         'Highlighted rows are the soonest. Cost is a label over the exact admission wording quoted from the official page; '
         f'“Not stated” means the page says nothing about price, not that entry is free. Across all costs, {len(dated)} '
         'entries carry a confirmed upcoming date.</p>')
body += countdown_list(free_dated, limit=12)
body += focus_callout
body += (f'<p><a href="#free-upcoming">All {len(free_dated)} free upcoming events ↓</a> · '
         f'<a href="free.html">All {len(free_rows)} free entries →</a> · '
         f'<a href="upcoming.html">All {len(dated)} dated entries, any cost →</a> · '
         '<a href="paid.html">Paid events (separate section) →</a> · '
         '<a href="review.html">Flagged for Review →</a></p></section>')
body += ('<h2>Browse by topic</h2><p class="topic-note">Gaming, music and AI &amp; technology are editorial topic tags derived from '
         'the verified event name. They are labels for navigation, not a verified field.</p>'
         + cards([(f, t, topic_counts.get(t, 0), "Open the topic page") for f, t in TOPIC_PAGES]
                 + [("free.html", "Free to attend", len(free_rows), "Admission stated free by the official page"),
                    ("paid.html", "Paid events", len(paid_rows), "Separate section — exact quoted prices")]))
body += '<h2>Browse by cadence</h2>' + cards([(f, label, kind_counts[k], "Browse source-linked entries") for f, label, k in [("weekly.html", "Weekly", "Weekly"), ("monthly.html", "Monthly", "Monthly"), ("annual.html", "Annual", "Annual"), ("special.html", "Special & dated", "Special")]])
body += '<h2>Explore by category</h2>' + cards([(f, c, cat_counts.get(c, 0), "Browse the directory") for f, c in [("markets.html", "Markets & food"), ("museums.html", "Museums & science"), ("culture.html", "Festivals & culture"), ("community.html", "Community & outdoors")]])
body += (f'<h2 id="free-upcoming">Free upcoming events — dated, nearest first · {len(free_dated)}</h2>'
         '<p class="topic-note">Every entry below is stated free on its official page <b>and</b> carries an explicitly '
         'approved upcoming date. Rows in the next 14 days are highlighted. The exact free-admission wording — '
         'including any conditions — is shown in the Admission column.</p>'
         + table(free_dated, nexts=UPCOMING))
body += ('<p class="topic-note">Looking for recurring programmes? Browse the '
         '<a href="free.html">Free to attend directory</a> or the cadence pages. '
         'A recurring pattern without a confirmed future date is not an upcoming event.</p>')
body += (f'<p class="topic-note">This page lists only free entries with confirmed upcoming dates. The complete city-only directory — '
         f'{len(listed)} entries at every cost — is on the <a href="focus.html">Focus page</a> and the '
         '<a href="upcoming.html">Upcoming page</a>; priced events have their own '
         '<a href="paid.html">Paid events section</a>.</p>')
write("index.html", "San Francisco, in events.", "Free things to do in San Francisco first: dated, source-linked recurring gatherings and special programmes inside the city, organized around official evidence. Paid events sit in their own section; uncertainty stays visible.", body)

# ---------------------------------------------------------------- upcoming page
upcoming_body = metrics([
    ("Dated entries", len(dated), "Ordered by next confirmed date", False),
    ("Today or already open", bucket_counts.get("Today", 0) + bucket_counts.get("Open now", 0), f"On or before {AS_OF}", False),
    ("Within 7 days", sum(bucket_counts.get(k, 0) for k in ("Open now", "Today", "Next 7 days")), "From the snapshot date", False),
    ("Within 30 days", sum(bucket_counts.get(k, 0) for k in ("Open now", "Today", "Next 7 days", "Next 30 days")), "Nearest dates first", False),
    ("Recurring, next date unconfirmed", len(recurring_no_date), "Weekly / monthly / annual patterns", True),
]) + notice()
upcoming_body += ('<section class="intro"><h2>Upcoming, nearest first</h2><p>Every row here has an explicitly approved ISO date on an '
                  'official page. Entries are grouped by how far that date sits from the snapshot: <b>Open now</b> started earlier and '
                  'still runs on the snapshot date, <b>Today</b> starts on 18 October 2026, and the rest are ordered by distance. Rows in '
                  'the next 14 days are highlighted. Nothing is generated from a weekly, monthly or annual pattern: those are listed '
                  'separately below.</p></section>')
for bucket in BUCKETS:
    items = [r for r in dated if bucket_of(UPCOMING[r["id"]][2]) == bucket]
    if not items:
        continue
    upcoming_body += f'<h2 id="bucket-{e(bucket.lower().replace(" ", "-"))}">{e(bucket)} · {len(items)}</h2>' + table(items, nexts=UPCOMING)
upcoming_body += (f'<h2>Recurring with no confirmed next date · {len(recurring_no_date)}</h2>'
                  '<p class="topic-note">These entries have documented cadence evidence but no approved ISO occurrence, so no date is '
                  'asserted. A pattern never produces a next date.</p>'
                  + table(recurring_no_date))
upcoming_body += (f'<h2>Special or cadence-unconfirmed, no approved date · {len(undated_special)}</h2>'
                  '<p class="topic-note">Dated programmes and one-off entries whose date or year no official page confirmed in this '
                  'snapshot.</p>' + table(undated_special))
write("upcoming.html", "Upcoming, nearest first.", "Every confirmed date in one ordered list, closest to the snapshot at the top, with cost labelled and the official page one click away.", upcoming_body)

# ----------------------------------------------------------------- cadence pages
for filename, kind, title in [("weekly.html", "Weekly", "A weekly rhythm."), ("monthly.html", "Monthly", "Once a month. Or twice."), ("annual.html", "Annual", "Traditions that return."), ("special.html", "Special", "Special & dated programmes.")]:
    description = "Only source-supported recurring classifications appear here. Seasonal exceptions apply; a pattern never proves the next occurrence." if kind != "Special" else "Dated editions and programme umbrellas without an approved ongoing cadence. “Special” does not claim an event will never recur. Past editions remain clearly labeled."
    write(filename, title, description, notice() + table([r for r in listed if r["kind"] == kind], nexts=UPCOMING))

for filename, category in [("markets.html", "Markets & food"), ("museums.html", "Museums & science"), ("culture.html", "Festivals & culture"), ("community.html", "Community & outdoors")]:
    write(filename, category + ".", "An editorial category of city-only entries. Prices, eligibility, dates and unresolved questions remain attached to their official sources.", notice() + table([r for r in listed if r["category"] == category], nexts=UPCOMING))

# ------------------------------------------------------------------- topic pages
TOPIC_NOTES = {
    "Gaming": "Chess clubs, board-game sessions and the game-industry festival inside San Francisco. Admission is stated only where the official page confirms it; otherwise the cell is blank and labelled “Not stated”. Library or club affiliation alone does not establish free entry.",
    "Music": "Concert series, festivals and free outdoor music inside the city. Cost is taken from the exact admission wording on the official page, so a free festival with a ticket lottery still reads as free.",
    "AI & technology": "Conferences and developer events held in San Francisco. Most are ticketed industry events whose price the official pages did not quote in this snapshot, so their cost reads “Not stated” rather than being guessed.",
}
for filename, topic in TOPIC_PAGES:
    items = [r for r in listed if topic_of(r) == topic]
    held_items = [r for r in held if topic_of(r) == topic]
    free_count = sum(1 for r in items if cost_of(r)[0] == "Free")
    page = notice() + metrics([
        (topic, len(items), "Directory entries", False),
        ("Free to attend", free_count, "Stated free on the official page", False),
        ("With a confirmed upcoming date", sum(1 for r in items if r["id"] in UPCOMING), "Nearest first on Upcoming", False),
        ("Held for review in this topic", len(held_items), "Linked below with sources", True),
    ])
    page += f'<section class="intro"><h2>What counts as {e(topic)}</h2><p>{e(TOPIC_NOTES[topic])}</p></section>'
    page += table(items, nexts=UPCOMING)
    if held_items:
        page += (f'<h2>Held for review · {e(topic)}</h2><p class="topic-note">These candidates belong to this topic but do not yet meet the '
                 'directory gate (name, venue and confirmed San Francisco geography). They are published with their official links '
                 'rather than dropped.</p><ul class="held-list">')
        for row in held_items:
            page += (f'<li><a href="review.html#{e(row["id"])}">{e(display(row))}</a> — '
                     + e("; ".join(row["flags"]) or "Unresolved evidence") + '<br>' + official(row["sources"][0], "Official source") + '</li>')
        page += '</ul>'
    write(filename, topic + ".", TOPIC_NOTES[topic], page)

# ------------------------------------------------------------------ focus page
# Session 59f56c24's combined "Gaming / Music / AI, then everything else" view.
# Kept alongside the per-topic subpages: one page that carries the whole ordered
# directory, so the focus grouping can be read (and checked) in a single table.
# (FOCUS_ORDER is defined once, next to the free-first sets above.)
focus_counts = Counter(topic_of(r) for r in listed)
focus_sorted = sorted(listed, key=lambda r: (
    FOCUS_ORDER[topic_of(r)],
    0 if cost_of(r)[0] == "Free" else 1,
    UPCOMING.get(r["id"], ("", date.max, 10**6, ""))[1],
    display(r).casefold(),
))
focus_body = notice() + metrics([
    ("Gaming", focus_counts.get("Gaming", 0), "Directory entries in this focus group", False),
    ("Music", focus_counts.get("Music", 0), "Directory entries in this focus group", False),
    ("AI & technology", focus_counts.get("AI & technology", 0), "Directory entries in this focus group", False),
    ("Everything else", focus_counts.get("Other", 0), "All remaining directory entries", False),
])
focus_body += ('<section class="intro"><h2>How the focus groups are made</h2><p>Groups come from the audited '
               'event name — “Pokémon”, “Jazz”, “Opera”, “Chess”, “AI Engineer” — and, for entries added by the '
               'two research overlays, from an explicit recorded decision. A venue is never used to guess a topic, '
               'and a concert whose name contains no music word stays in “Everything else”. Order on this page: '
               '<b>Gaming, then Music, then AI &amp; technology, then everything else</b>; inside each group, '
               'entries whose official page states free admission come first, then the soonest confirmed date. '
               'The Focus label on each row and the dedicated <a href="gaming.html">Gaming</a>, '
               '<a href="music.html">Music</a> and <a href="ai.html">AI &amp; technology</a> pages carry the same '
               'grouping.</p></section>')
focus_body += table(focus_sorted, nexts=UPCOMING)
write("focus.html", "Gaming · Music · AI first.",
      "The whole city-only directory ordered Gaming, then Music, then AI & technology, then everything else — free and soonest first inside each group.",
      focus_body)

free_body = notice() + metrics([
    ("Free to attend", len(free_rows), "Admission stated free by the official page", False),
    ("Free upcoming (dated)", len(free_dated), "Confirmed date after the snapshot", False),
    ("Gaming", sum(1 for r in free_rows if topic_of(r) == "Gaming"), "Free gaming entries", False),
    ("Music", sum(1 for r in free_rows if topic_of(r) == "Music"), "Free music entries", False),
    ("AI & technology", sum(1 for r in free_rows if topic_of(r) == "AI & technology"), "Free AI & technology entries", False),
    ("Admission not stated", cost_counts.get("Not stated", 0), "Blank — never assumed free", True),
])
free_body += ('<section class="intro"><h2>Free, as the official page states it</h2><p>Every entry below quotes free admission on its own '
              'official page. The exact wording is shown in the Admission column, including conditions such as registration, a ticket '
              'lottery, residency or membership — those conditions are part of the quote and are not edited out. Entries whose official '
              'page says nothing about price are <b>not</b> here; they are labelled “Not stated” everywhere, because a blank cell is '
              'unverified, never free by default. Order on this page: <b>Gaming, then Music, then AI &amp; technology, then '
              'everything else</b>; inside each group, the soonest confirmed date first.</p></section>')
free_body += table(free_focus, nexts=UPCOMING)
write("free.html", "Free to attend.", "Entries whose official page states free admission, with the exact wording and any conditions kept visible.", free_body)

# ------------------------------------------------------------------- paid page
# Separate section (session 21f3dd85, T39): priced events are collected and
# organized, but kept out of the free-first dashboard and Free page. Only rows
# whose verified admission text quotes a price appear here; “Not stated” is
# not paid and never appears on this page.
paid_body = notice() + metrics([
    ("Paid events", len(paid_rows), "A price is quoted on the official page", False),
    ("With a confirmed upcoming date", sum(1 for r in paid_rows if r["id"] in UPCOMING), "Nearest first below", False),
    ("Gaming", sum(1 for r in paid_rows if topic_of(r) == "Gaming"), "Paid gaming entries", False),
    ("Free to attend", len(free_rows), "The free-first focus — on the Free page", False),
    ("Admission not stated", cost_counts.get("Not stated", 0), "Not listed here — unpriced is not paid", True),
])
paid_body += ('<section class="intro"><h2>Paid, kept separate on purpose</h2><p>This project focuses on free events: the '
              '<a href="index.html">landing page</a> and the <a href="free.html">Free page</a> carry free entries only. '
              'Priced events are still collected and organized — here, in their own section. Every entry below quotes a '
              'price, ticket or entry fee on its official page, and the exact wording is shown in the Admission column, '
              'including member pricing, play-up or admin fees where the page states them in its price line. Entries whose '
              'official page says nothing about price are <b>not</b> here: “Not stated” means unverified, not paid. Dated '
              'entries come first, nearest date first; the rest follow alphabetically.</p></section>')
paid_body += table(paid_rows, nexts=UPCOMING)
write("paid.html", "Paid events.", "The separate paid section: entries whose official page quotes a price, with the exact wording kept beside the label.", paid_body)


def plain(headers, values):
    return '<div class="table-wrap"><table class="plain"><thead><tr>' + ''.join(f'<th scope="col">{e(h)}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{e(v)}</td>' for v in row) + '</tr>' for row in values) + '</tbody></table></div>'


analysis_intro = f'''<section class="prose"><h2>What the register can tell us</h2><p>{stats['candidates']} candidate entries were assessed. {stats['listed']} meet the directory’s name, venue and SF-geography gate; {stats['review_only']} are held for review. These are <b>entries, not unique events</b>: {stats['series']} listed programme umbrellas overlap their dated children. This is not a random sample of San Francisco activity.</p>
<p>Counts describe this dataset only. They cannot establish citywide event frequency, neighborhood equity, attendance, economic impact, or that one category dominates the city.</p></section>'''
body = analysis_intro + '<h2>Directory composition</h2>' + plain(["Documented cadence / editorial grouping", "Entries"], [(k, kind_counts[k]) for k in ("Weekly", "Monthly", "Annual", "Special")])
body += '<h2>Topic tags (editorial)</h2>' + plain(["Topic", "Directory entries"], [(t, topic_counts.get(t, 0)) for t in ("Gaming", "Music", "AI & technology", "Other")]) + '<p class="topic-note">Topic tags are derived from the verified event name for navigation only. They are not a verified field and not evidence of genre.</p>'
body += '<h2>Cost, as stated by the official page</h2>' + plain(["Cost label", "Directory entries"], [("Free", cost_counts.get("Free", 0)), ("Paid", cost_counts.get("Paid", 0)), ("Not stated", cost_counts.get("Not stated", 0)), ("See source", cost_counts.get("See source", 0))]) + '<p class="topic-note">The label is computed from the quoted admission text and the exact wording is always rendered beside it. “Not stated” is not “free”.</p>'
body += '<h2>Dates, without invention</h2>' + plain([f"Temporal status at {AS_OF}", "Directory entries"], sorted(stats["temporal"].items()))
body += '<h2>Upcoming horizon</h2>' + plain([f"Distance from {AS_OF}", "Directory entries"], [(b, bucket_counts.get(b, 0)) for b in BUCKETS] + [("No approved date", len(listed) - len(dated))])
body += '<h2>Unconfirmed fields stay blank</h2>' + plain(["Field", "Blank cells in the directory"], [(LABELS[k], stats["blank_fields"][k]) for k in FIELDS])
body += '<section class="prose"><p>Only explicit approved ISO dates drive date labels. An exhibition with only an opening date has no fabricated closing date. Ongoing admission policies and recurring markets do not automatically receive a dated next occurrence.</p><h2>Biases and limits</h2><ul><li>Official web calendars favor larger, web-visible institutions; small community, faith, nightlife and pop-up gatherings are underrepresented.</li><li>Blocked and JavaScript-only pages reduce readable evidence. Their candidates are not proof of nonexistence and are not silently counted as verified.</li><li>Regional festivals need venue-level separation. A San Francisco brand does not place every performance inside the city.</li><li>Domain counts are not counts of organizers. A .org suffix is not evidence of nonprofit legal status; no such inference is made.</li><li>Snapshot dates are not live ticket availability, cancellations or a guarantee that a source has not changed.</li><li>Topic tags and cost badges are presentation labels. A search-result snippet is evidence of what a tool returned, not a verified page fetch with a status code.</li></ul><h2>Next research priorities</h2><p>Isolate SF-only regional screenings; verify individual sports fixtures, theater/music performances, civic and faith calendars; resolve conflicting hours/street extents; promote the held Mechanics Institute chess class whose venue is now evidenced (see the free-first research log) and add a venue for the held AI candidate; confirm the current Grace Cathedral recital admission terms from one readable official page; find an official programme title for the Internet Archive tours; revisit unreadable primary pages. Coverage is intentionally described as incomplete.</p><p><a href="review.html">All candidates and open questions →</a> · <a href="data/audit_summary.json">Machine-readable summary</a></p></section>'
write("analysis.html", "Findings, not false certainty.", "A reproducible view of coverage, missing values, date quality and research limitations—not a statistical portrait of the whole city.", body)

body = metrics([("Held off the directory", stats["review_only"], "Venue / geography / evidence unresolved", True), ("Listed with unconfirmed fields", stats["listed_with_blanks"], "Fields remain blank, never guessed", True), ("Candidates retained", stats["candidates"], "No unresolved candidate silently discarded", False)])
body += '<section class="prose"><p><b>This page includes every candidate.</b> Filter Publication to “Held for review” to isolate quarantined entries. Candidate identifiers are preserved for traceability; where the event name itself is unconfirmed, the inherited title is explicitly labeled as an unverified identifier. They are not assertions of a real event, date or SF location.</p><p><a href="data/review.csv" download>Download all review records (CSV) ↓</a> · <a href="data/unverified_history.json">Unverified inherited history</a></p></section>'
for i, finding in enumerate(findings, 1):
    body += f'<section class="prose finding" id="finding-{i}"><h2>{e(finding["title"])}</h2><p>{e(finding["detail"])}</p>' + (('<ul>' + ''.join(f'<li><a href="{e(u)}" rel="noreferrer">{e(u)}</a></li>' for u in finding.get("urls", [])) + '</ul>') if finding.get("urls") else '') + '</section>'
exclusions = load("exclusions.json")
body += '<section class="prose"><h2>Out-of-city exclusions</h2><p>Examples include Levi’s Stadium in Santa Clara and the Cow Palace in Daly City. Historical exclusion records remain in <a href="data/exclusions.json">the exclusion log</a>. Regional/mixed-city candidates are held for review rather than admitted wholesale.</p></section>'
body += '<h2>Candidate review register</h2>' + table(rows, review=True, nexts=UPCOMING)
body += ('<section class="prose" id="upcoming-eligibility-audit"><h2>Upcoming eligibility audit · 18 October 2026</h2>'
         '<p><b>Resolved:</b> 40 recurring entries without an approved upcoming date were removed from the landing page, '
         'not from the directory. For example, the official '
         '<a href="https://www.sfrecpark.org/calendar.aspx?PREVIEW=YES&amp;EID=9947">Sunday Fun Days listing</a> '
         'ends its season on September 27, 2026; a weekly pattern cannot establish a later occurrence.</p>'
         '<p><b>Needs review:</b> the two <a href="https://noontimeconcerts.org/">Noontime Concerts</a> entries '
         'describe the same programme; they remain source-linked independent research records, not two unique events. '
         'The <a href="https://gracecathedral.org/series/choral-evensong/">Choral Evensong page</a> '
         'prints a Sunday 4:55PM–4:55PM time alongside Thursday 5:30 p.m. prose. '
         'Do not apply the Thursday time to a Sunday occurrence; the existing row leaves time blank.</p>'
         '<p>Fresh checks in this pass were targeted, not a new semantic audit of all 295 candidates. '
         'Citywide completeness, live cancellations and future availability remain unverified. '
         '<a href="data/research/audit-16b88bbd.md">Scope, official quotations and checks →</a></p></section>')
write("review.html", "Flagged for Review.", "Unverified fields, unresolved conflicts and candidates held off the city-only directory—published openly, with official links for manual checking.", body)

METHOD = '''<section class="prose" id="method"><h2>How evidence becomes a published field</h2><ol>
<li>Historical inputs are consolidated into candidates and saved as <b>unverified history</b>, not trusted facts.</li>
<li>Official organizer, venue, museum, library and government pages are read in context. Public-tourism sources are discovery/reference material, not a substitute for missing event details.</li>
<li>Each accepted name, schedule, time, venue, admission condition, recurrence and occurrence date has an explicit decision and source quotation. Structured event JSON-LD is labeled separately from readable page text. Selected tool excerpts are not represented as complete raw page captures.</li>
<li>The newer <a href="data/audit_f1fd3c36.json">companion research audit</a> and its two added candidates are preserved as unverified history before the final gate. Its old field/page labels do not automatically approve values.</li>
<li>The build starts every factual field blank and copies only approved decisions. Name, venue and documented SF geography are required for directory admission. Other unknowns remain blank and flagged. Geography can identify a recognized SF venue from its official address/directions; it is never inferred from a stray city token in unrelated marketing.</li>
<li>Exact-quote checks test provenance, <b>not semantic truth</b>. Context, edition, eligibility and conflicting copy require a research judgment. A URL/status/name match never verifies the rest of a row.</li>
<li>Only explicitly approved ISO occurrences determine labels relative to the fixed snapshot. URL slugs, weekdays, copyright dates and neighboring events never supply missing years. Recurrence evidence does not generate future dates.</li>
<li><b>Cost labels</b> are computed only from the verified admission text. “Free”, “Paid” and “Not stated” are labels over that quote; the exact official wording is always shown beside the badge. A blank admission cell is never published as free.</li>
<li><b>Topic tags</b> (Gaming / Music / AI &amp; technology) are editorial navigation labels derived from the verified event name, or from an explicit decision for the <a href="data/audit_3adf31d9.json">new-requirement research pass</a> and the <a href="data/audit_21f3dd85.json">free-first research pass</a>. They are not a verified field.</li>
</ol><p>Times are local to San Francisco. Free parking, free activities with paid entry, and virtual tickets do not establish free physical admission. Conditions such as residency, age, surcharges and RSVP remain visible.</p>
<p>Evidence snapshots: <a href="data/audit_64f8b973.json">archived captures and explicit decisions (JSON)</a> · <a href="data/audit_3adf31d9.json">gaming, music and AI research pass (JSON)</a> · <a href="data/audit_21f3dd85.json">free-first research pass (JSON)</a>. Some captures in the newer passes are the verbatim text the workspace search tool returned for an exact official URL rather than a full page fetch (sfpl.org branch navigation, the Stern Grove contact block); those records carry no HTTP status and say so. The free-first pass also records no HTTP status for its fetches, because its fetch tool does not report one. Original HTTP status and later attempt metadata remain separate; failed refreshes do not erase prior readable evidence. This is not continuous re-verification.</p>
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
    retrieval = source.get('retrieval') or {}
    how = ''
    if retrieval:
        how = ' · retrieval: ' + e(retrieval.get('method', ''))
        if retrieval.get('complete') is False:
            how += f' (partial page: {len(retrieval.get("chunks_retrieved", []))} of {retrieval.get("chunks_total")} chunks read)'
    body += f'<article class="source" id="s-{e(sid)}"><h3>{official(sid, source["title"])}</h3><p>{e(source["url"])}</p><p>Archived runner status: {e(http)} · capture timestamp: {e(source["captured_at"] or "not recorded")}{method}{how}. Referenced by {len(source["approved_for_rows"])} explicit row decisions; this does not certify every field or current page content.</p></article>'
write("sources.html", "A trail back to the source.", "Explicit field decisions and quotations, not inherited verification badges. Every candidate keeps official links for manual review.", body)


def csv_value(value):
    value = str(value)
    return "'" + value if value.startswith(('=', '+', '-', '@')) else value


def export(filename, items, review=False):
    columns = ['id', 'name', 'schedule', 'time', 'venue', 'price', 'kind', 'entry_type', 'parent', 'category', 'topic', 'cost_label', 'next_confirmed_date', 'publication', 'temporal_status', 'approved_dates', 'unverified', 'review_notes', 'official_source_urls', 'as_of']
    if review:
        columns.insert(1, 'candidate_identifier_unverified')
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=columns, lineterminator='\n')
    writer.writeheader()
    for row in items:
        record = {key: row.get(key, '') for key in columns}
        record.update(topic=topic_of(row), cost_label=cost_of(row)[0], next_confirmed_date=next_date(row) or '',
                      approved_dates=date_text(row), unverified='; '.join(row['unverified']),
                      review_notes='; '.join(row['flags'] + ([row['notes']] if row['notes'] else [])),
                      official_source_urls=' | '.join(sources[s]['url'] for s in row['sources']))
        if review:
            record['candidate_identifier_unverified'] = row['candidate_name']
        writer.writerow({key: csv_value(value) for key, value in record.items()})
    (ROOT / 'data' / filename).write_text(stream.getvalue())


# The canonical nearest-first ordering, exported so the optional browser QA can
# assert it instead of re-deriving it.
(ROOT / 'data' / 'upcoming_order.json').write_text(json.dumps([r["id"] for r in dated], indent=1) + "\n")
# Only explicitly dated free entries appear in the landing table.
# Keep the recurring key for compatibility, but it must remain empty.
(ROOT / 'data' / 'dashboard_order.json').write_text(json.dumps(
    {"dated": [r["id"] for r in free_dated], "recurring": []}, indent=1) + "\n")

export('events.csv', listed)
export('review.csv', rows, review=True)
analysis_md = f'''# Analysis — bounded SF event research snapshot

As of {AS_OF}. This is not a complete or live city calendar.

- {stats['candidates']} candidate entries assessed: {stats['inherited_candidates']} inherited and {stats['new_entries']} official-calendar entries plus {stats['new_research_entries']} from the gaming/music/AI research pass and {stats['free_first_entries']} from the free-first research pass.
- {stats['listed']} admitted to the city-only directory; {stats['review_only']} held for review.
- {stats['series']} listed programme umbrellas overlap child events. These totals are **not unique-event counts**.
- {stats['source_urls']} exact cited URLs across {stats['domains']} domains. Domains are not organizations or nonprofit status.
- Cadence: {kind_counts['Weekly']} weekly / {kind_counts['Monthly']} monthly / {kind_counts['Annual']} annual / {kind_counts['Special']} special or cadence-unconfirmed.

## Upcoming, relative to the fixed snapshot

{len(dated)} directory entries carry at least one confirmed upcoming date; {len(listed) - len(dated)} do not.
Of the dated entries, {len(free_dated)} are stated free on their official page; they lead the free-first
landing page, while priced entries are grouped in the separate Paid events section.

''' + '\n'.join(f'- {b}: {bucket_counts.get(b, 0)}' for b in BUCKETS) + f'''

## Topic tags (editorial, from the verified name)

''' + '\n'.join(f'- {t}: {topic_counts.get(t, 0)}' for t in ("Gaming", "Music", "AI & technology", "Other")) + f'''

## Cost, as stated by the official page

- Free: {cost_counts.get('Free', 0)}
- Paid: {cost_counts.get('Paid', 0)}
- Not stated: {cost_counts.get('Not stated', 0)} (blank admission cell — never assumed free)

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
Topic tags and cost badges are labels, not verified fields.

See [Flagged for Review](review.html), [field evidence](sources.html),
[the summary JSON](data/audit_summary.json) and [unverified history](data/unverified_history.json).
'''
(ROOT / 'ANALYSIS.md').write_text(analysis_md)
print(f'Built 19 HTML pages, {len(listed)} directory rows, {len(rows)} review records, CSVs and ANALYSIS.md from audited data only.')
