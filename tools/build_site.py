#!/usr/bin/env python3
"""Build the GitHub Pages site in docs/ from data/events.json.

Pure static HTML output — no build toolchain, so nothing can fail to compile.
Run:  python3 tools/build_site.py
"""
import json
import html
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "data", "events.json")))
DISC = json.load(open(os.path.join(ROOT, "data", "discontinued.json")))
EVENTS = DATA["events"]
GENERATED = DATA["generated"]
OUT = os.path.join(ROOT, "docs")
os.makedirs(OUT, exist_ok=True)

CAT_SLUG = {
    "Street Fairs & Parades": "street-fairs-parades",
    "Music & Festivals": "music-festivals",
    "Pride & LGBTQ+": "pride-lgbtq",
    "Cultural & Heritage": "cultural-heritage",
    "Food & Markets": "food-markets",
    "Sports & Races": "sports-races",
    "Film": "film",
    "Performing Arts": "performing-arts",
    "Parks & Outdoors": "parks-outdoors",
    "Literature & Books": "literature-books",
    "Civic & Holiday": "civic-holiday",
}
REC_LABEL = {
    "weekly": "Recurring — weekly",
    "monthly": "Recurring — monthly",
    "annual": "Recurring — annual",
    "special": "Special / dated",
}

CSS = """
:root{--ink:#12212e;--mut:#5b6b7a;--line:#e2e8ee;--bg:#f6f8fa;--card:#fff;
--acc:#0f5f9c;--acc2:#0b7285;--warn:#9a3412;--warnbg:#fff7ed;--ok:#14532d;--okbg:#f0fdf4;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
header{background:#0e2436;color:#fff;padding:14px 24px;display:flex;
align-items:center;gap:16px;flex-wrap:wrap;border-bottom:3px solid var(--acc2)}
header .brand{font-weight:700;font-size:17px;letter-spacing:.2px}
header nav{display:flex;gap:4px;flex-wrap:wrap}
header nav a{color:#dbe7f1;padding:5px 10px;border-radius:6px;font-size:13.5px}
header nav a:hover{background:#1b3b53;text-decoration:none}
header nav a.on{background:var(--acc2);color:#fff}
main{max-width:1240px;margin:0 auto;padding:26px 24px 60px}
h1{font-size:26px;margin:0 0 6px}h2{font-size:19px;margin:30px 0 10px}
h3{font-size:15.5px;margin:20px 0 8px}
.sub{color:var(--mut);margin:0 0 20px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));gap:12px;margin:18px 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.card .n{font-size:27px;font-weight:700;line-height:1.1}
.card .l{font-size:12.5px;color:var(--mut);margin-top:3px}
.card a{font-size:12.5px;display:inline-block;margin-top:6px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:14px 0}
table{width:100%;border-collapse:collapse;background:var(--card);
border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:13.4px}
th,td{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#eef3f7;font-size:12px;text-transform:uppercase;letter-spacing:.4px;color:#3b4b5a}
tr:last-child td{border-bottom:none}
tbody tr:hover{background:#fafcfe}
.badge{display:inline-block;padding:1.5px 7px;border-radius:20px;font-size:11.2px;
font-weight:600;white-space:nowrap;border:1px solid transparent}
.b-weekly{background:#eef7ff;color:#0b5394;border-color:#cfe4f7}
.b-monthly{background:#f3f0ff;color:#4c1d95;border-color:#e0d7fb}
.b-annual{background:#eafaf1;color:#14532d;border-color:#cdeedc}
.b-special{background:#fff4e5;color:#8a4b08;border-color:#fbe0bb}
.b-flag{background:var(--warnbg);color:var(--warn);border-color:#fed7aa}
.b-unv{background:#f1f5f9;color:#475569;border-color:#dde5ec}
.blank{color:#94a3b8;font-style:italic}
.note{font-size:12.4px;color:var(--mut);margin-top:4px}
.small{font-size:12.6px;color:var(--mut)}
footer{max-width:1240px;margin:0 auto;padding:0 24px 40px;color:var(--mut);font-size:12.5px}
.tag{display:inline-block;background:#eef3f7;border-radius:6px;padding:2px 8px;font-size:12px;margin:2px 3px 2px 0}
.warnbox{background:var(--warnbg);border:1px solid #fed7aa;border-radius:10px;padding:14px 16px;margin:14px 0}
.okbox{background:var(--okbg);border:1px solid #cdeedc;border-radius:10px;padding:14px 16px;margin:14px 0}
code{background:#eef3f7;padding:1px 5px;border-radius:4px;font-size:12.4px}
.catgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px;margin-top:14px}
.catcard{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.catcard h4{margin:0 0 4px;font-size:14.5px}
"""

def esc(x):
    return html.escape(str(x)) if x is not None else ""

def badge(rec):
    return f'<span class="badge b-{rec}">{esc(REC_LABEL[rec])}</span>'

def date_cell(e):
    if e["next_date"]:
        return esc(e["next_date"])
    if e["date_status"] == "unverified":
        return '<span class="blank">not published</span> <span class="badge b-unv">unverified</span>'
    if e["date_status"] == "continuous":
        return '<span class="badge b-weekly">runs on this pattern</span>'
    return '<span class="blank">n/a</span>'

def source_cell(e):
    return (f'<a href="{esc(e["source_url"])}" rel="noopener">{esc(e["source_name"])}</a>'
            f'<div class="note">checked {esc(e["verified_on"])}</div>')

def status_cell(e):
    if e["status"] == "flagged":
        return '<span class="badge b-flag">flagged</span>'
    if e["date_status"] == "unverified":
        return '<span class="badge b-unv">date unverified</span>'
    return '<span class="badge b-annual">verified</span>'

TABLE_COLS = ("Event", "Pattern", "Cadence", "Next / most recent", "Where", "Cost",
              "Official source", "Status")

def table(rows, show_recurrence=True, show_notes=True):
    cols = list(TABLE_COLS)
    if not show_recurrence:
        cols.remove("Pattern")
    h = "".join(f"<th>{esc(c)}</th>" for c in cols)
    body = []
    for e in rows:
        where = esc(e["venue"]) or '<span class="blank">—</span>'
        if e["neighborhood"]:
            where += f'<div class="note">{esc(e["neighborhood"])}</div>'
        cost = esc(e["cost"]) or '<span class="blank">—</span>'
        tds = [f'<td><strong>{esc(e["name"])}</strong>'
               + (f'<div class="note">{esc(e["schedule"])}</div>' if show_notes and e["schedule"] else "")
               + (f'<div class="note">⚑ {esc(e["notes"])}</div>' if show_notes and e["notes"] else "")
               + "</td>"]
        if show_recurrence:
            tds.append(f"<td>{badge(e['recurrence'])}</td>")
        tds += [f"<td>{esc(e['cadence'])}</td>",
                f"<td>{date_cell(e)}</td>",
                f"<td>{where}</td>",
                f"<td>{cost}</td>",
                f"<td>{source_cell(e)}</td>",
                f"<td>{status_cell(e)}</td>"]
        body.append("<tr>" + "".join(tds) + "</tr>")
    return f"<table><thead><tr>{h}</tr></thead><tbody>{''.join(body)}</tbody></table>"

NAV = [
    ("index.html", "Dashboard"),
    ("recurring.html", "Recurring events"),
    ("special.html", "Special events"),
    ("all-events.html", "All events"),
    ("analysis.html", "Analysis"),
    ("flagged.html", "Flagged for Review"),
    ("methodology.html", "Method & sources"),
]

def page(name, title, body, active):
    links = []
    for u, l in NAV:
        cls = ' class="on"' if u == active else ""
        links.append(f'<a href="{u}"{cls}>{esc(l)}</a>')
    nav = "".join(links)
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · San Francisco Events</title>
<style>{CSS}</style></head><body>
<header><div class="brand">San Francisco Events — verified register</div><nav>{nav}</nav></header>
<main>{body}</main>
<footer><p>Every row is sourced to an organizer, City or venue page and carries the date it was
checked. Values that could not be confirmed are left blank and marked
<span class="badge b-unv">unverified</span> rather than inferred. Discrepancies between official
sources appear on <a href="flagged.html">Flagged for Review</a>.</p>
<p>Data generated {esc(GENERATED)} · <a href="data/events.json">data/events.json</a> ·
<a href="https://github.com/buffedlizard55-lab/MaltaProj5">repository</a></p></footer>
</body></html>"""
    with open(os.path.join(OUT, name), "w") as f:
        f.write(doc)

# --------------------------------------------------------------------------
# stats
# --------------------------------------------------------------------------
by_rec = defaultdict(list)
by_cat = defaultdict(list)
for e in EVENTS:
    by_rec[e["recurrence"]].append(e)
    by_cat[e["category"]].append(e)
flagged = [e for e in EVENTS if e["status"] == "flagged"]
unverified = [e for e in EVENTS if e["date_status"] == "unverified"]
verified_dates = [e for e in EVENTS if e["next_date"]]

# --------------------------------------------------------------------------
# index
# --------------------------------------------------------------------------
cat_cards = "".join(
    f'<div class="catcard"><h4><a href="{CAT_SLUG[c]}.html">{esc(c)}</a></h4>'
    f'<div class="small">{len(by_cat[c])} entries</div></div>'
    for c in sorted(by_cat))

b = f"""<h1>San Francisco events register</h1>
<p class="sub">Events held inside the City and County of San Francisco, split into events that
recur (weekly, monthly or annually) and one-off special events. Every row links to the official
organizer, City or venue page it was verified against on {esc(GENERATED)}.</p>
<div class="cards">
<div class="card"><div class="n">{len(EVENTS)}</div><div class="l">Events in register</div>
<a href="all-events.html">Full table</a></div>
<div class="card"><div class="n">{len(by_rec['weekly'])+len(by_rec['monthly'])}</div>
<div class="l">Weekly &amp; monthly recurring</div><a href="recurring.html">See</a></div>
<div class="card"><div class="n">{len(by_rec['annual'])}</div><div class="l">Annual recurring</div>
<a href="recurring.html">See</a></div>
<div class="card"><div class="n">{len(by_rec['special'])}</div><div class="l">Special / dated</div>
<a href="special.html">See</a></div>
<div class="card"><div class="n">{len(verified_dates)}</div><div class="l">Rows with a confirmed
future date</div><a href="recurring.html">See</a></div>
<div class="card"><div class="n">{len(unverified)}</div><div class="l">Dates not yet published</div>
<a href="flagged.html">See</a></div>
<div class="card"><div class="n">{len(flagged)}</div><div class="l">Irregularities flagged</div>
<a href="flagged.html">Review</a></div>
<div class="card"><div class="n">{len(DISC['items'])}</div><div class="l">Excluded / discontinued</div>
<a href="flagged.html">See</a></div>
</div>

<h2>Browse by category</h2>
<div class="catgrid">{cat_cards}</div>

<h2>How the register is organised</h2>
<div class="panel">
<p><strong>Recurring — weekly.</strong> Events with a fixed weekday pattern that run all year
(farmers markets, the Golden Gate Park Band's Sunday concerts).</p>
<p><strong>Recurring — monthly.</strong> Events with a fixed monthly pattern
(Downtown First Thursdays, Castro Night Market, the Fort Mason night market).</p>
<p><strong>Recurring — annual.</strong> Festivals, parades, seasons and races that return once a
year — the bulk of the register.</p>
<p><strong>Special / dated.</strong> One-off or single-edition events with a specific date rather
than a repeating pattern.</p>
</div>

<h2>Reading the status column</h2>
<div class="panel">
<p><span class="badge b-annual">verified</span> — event, cadence and date confirmed against the
linked official page.</p>
<p><span class="badge b-unv">date unverified</span> — the event itself is confirmed on an official
page, but the organizer has not published the next edition's date. The date cell is left blank
rather than estimated.</p>
<p><span class="badge b-weekly">runs on this pattern</span> — a continuous series (a weekly market,
a full concert season) whose official source defines the pattern rather than a single next date.</p>
<p><span class="badge b-flag">flagged</span> — a genuine irregularity: official sources disagree,
an official page is stale, or a value could not be pinned down. Full detail on
<a href="flagged.html">Flagged for Review</a>.</p>
</div>"""
page("index.html", "Dashboard", b, "index.html")

# --------------------------------------------------------------------------
# recurring
# --------------------------------------------------------------------------
b = f"""<h1>Recurring events</h1>
<p class="sub">Events that repeat — weekly, monthly or once a year. {len(by_rec['weekly'])+len(by_rec['monthly'])+len(by_rec['annual'])} entries.</p>
<h2>Weekly</h2>{table(by_rec['weekly'], show_recurrence=False)}
<h2>Monthly</h2>{table(by_rec['monthly'], show_recurrence=False)}
<h2>Annual</h2>{table(by_rec['annual'], show_recurrence=False)}"""
page("recurring.html", "Recurring events", b, "recurring.html")

# --------------------------------------------------------------------------
# special
# --------------------------------------------------------------------------
b = f"""<h1>Special &amp; dated events</h1>
<p class="sub">One-off or single-edition events with a specific date rather than a repeating
pattern. {len(by_rec['special'])} entries.</p>
{table(by_rec['special'], show_recurrence=False)}
<div class="panel"><p class="small">Annual editions of these events, where they exist, are also
listed under <a href="recurring.html">Recurring events</a>.</p></div>"""
page("special.html", "Special events", b, "special.html")

# --------------------------------------------------------------------------
# all events
# --------------------------------------------------------------------------
b = f"""<h1>All events</h1>
<p class="sub">All {len(EVENTS)} entries in one table, ordered by pattern then name.</p>
{table(EVENTS)}"""
page("all-events.html", "All events", b, "all-events.html")

# --------------------------------------------------------------------------
# category pages
# --------------------------------------------------------------------------
for cat, slug in CAT_SLUG.items():
    rows = by_cat.get(cat, [])
    if not rows:
        continue
    b = f"""<h1>{esc(cat)}</h1>
<p class="sub">{len(rows)} entries · <a href="all-events.html">back to all events</a></p>
{table(rows)}"""
    page(f"{slug}.html", cat, b, "index.html")

# --------------------------------------------------------------------------
# flagged
# --------------------------------------------------------------------------
fl_rows = table(flagged, show_recurrence=False)
unv = sorted(unverified, key=lambda e: e["name"])
BLANK = '<span class="blank">—</span>'
unv_rows = "".join(
    f"<tr><td><strong>{esc(e['name'])}</strong></td><td>{esc(e['cadence'])}</td>"
    f"<td>{esc(e['schedule']) or BLANK}</td>"
    f"<td>{source_cell(e)}</td></tr>" for e in unv)
disc_parts = []
for d in DISC["items"]:
    disc_parts.append(
        "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td>"
        '<td><a href="%s" rel="noopener">%s</a></td></tr>'
        % (esc(d["name"]), esc(d["reason"]), esc(d["detail"]),
           esc(d["source_url"]), esc(d["source_name"])))
disc_rows = "".join(disc_parts)

b = f"""<h1>Flagged for Review</h1>
<p class="sub">Nothing on this page blocks the register. These are items that need a human
decision: official sources that disagree with each other, stale official pages, dates that the
organizer has not published, and events that are discontinued or outside the city.</p>

<h2>1. Irregularities — official sources conflict ({len(flagged)})</h2>
<div class="warnbox"><p>Each row below was checked against an official page. The note in the
Event column states exactly what disagrees, and which sources were compared. Values in dispute are
left blank in the tables rather than picked.</p></div>
{fl_rows}

<h2>2. Dates not yet published by the organizer ({len(unv)})</h2>
<div class="panel"><p>These events are confirmed on their official pages, but no next-edition date
is published there yet. The date cell is deliberately empty — nothing was inferred from third-party
calendars.</p></div>
<table><thead><tr><th>Event</th><th>Cadence</th><th>Last confirmed edition</th>
<th>Official source</th></tr></thead><tbody>{unv_rows}</tbody></table>

<h2>3. Discontinued or excluded ({len(DISC['items'])})</h2>
<div class="warnbox"><p>Items that appear in "San Francisco event" lists but should not be in the
register. Each is excluded, with the reason and the source checked.</p></div>
<table><thead><tr><th>Item</th><th>Reason</th><th>Detail</th><th>Source checked</th></tr></thead>
<tbody>{disc_rows}</tbody></table>"""
page("flagged.html", "Flagged for Review", b, "flagged.html")

# --------------------------------------------------------------------------
# analysis
# --------------------------------------------------------------------------
org_counts = defaultdict(int)
for e in EVENTS:
    dom = re.sub(r"^https?://(www\.)?", "", e["source_url"]).split("/")[0]
    org_counts[dom] += 1
top_src = sorted(org_counts.items(), key=lambda kv: (-kv[1], kv[0]))
src_rows = "".join(f"<tr><td><code>{esc(d)}</code></td><td>{n}</td></tr>" for d, n in top_src)
cat_parts = []
for c in sorted(by_cat):
    n_conf = sum(1 for e in by_cat[c] if e["next_date"])
    n_flag = sum(1 for e in by_cat[c] if e["status"] == "flagged")
    cat_parts.append(
        '<tr><td><a href="%s.html">%s</a></td><td>%d</td><td>%d</td><td>%d</td></tr>'
        % (CAT_SLUG[c], esc(c), len(by_cat[c]), n_conf, n_flag))
cat_rows = "".join(cat_parts)

free = sum(1 for e in EVENTS if "free" in e["cost"].lower())
b = f"""<h1>Analysis &amp; findings</h1>
<p class="sub">What the verified data shows, and where the official record is weakest.</p>

<h2>Shape of the register</h2>
<div class="cards">
<div class="card"><div class="n">{len(EVENTS)}</div><div class="l">Total entries</div></div>
<div class="card"><div class="n">{len(by_rec['annual'])}</div><div class="l">Annual ({round(100*len(by_rec['annual'])/len(EVENTS))}% of register)</div></div>
<div class="card"><div class="n">{len(by_rec['weekly'])+len(by_rec['monthly'])}</div><div class="l">Weekly &amp; monthly</div></div>
<div class="card"><div class="n">{free}</div><div class="l">Free or donation-entry events</div></div>
</div>

<h2>Entries by category</h2>
<table><thead><tr><th>Category</th><th>Entries</th><th>With confirmed future date</th>
<th>Flagged</th></tr></thead><tbody>{cat_rows}</tbody></table>

<h2>Findings</h2>
<div class="panel">
<p><strong>1. Annual festivals dominate; genuinely weekly events are few.</strong>
{len(by_rec['annual'])} of {len(EVENTS)} entries repeat annually, while only
{len(by_rec['weekly'])} run weekly and {len(by_rec['monthly'])} monthly. San Francisco's public
event calendar is a festival calendar, not a weekly-rhythm calendar — the weekly layer is almost
entirely farmers markets plus the Golden Gate Park Band.</p>

<p><strong>2. Roughly a third of the register has no published next date.</strong>
{len(unverified)} of {len(EVENTS)} entries ({round(100*len(unverified)/len(EVENTS))}%) have a
confirmed event and cadence but no next-edition date on the organizer's own site. This is
concentrated in autumn: after their 2026 editions, organizers such as Hardly Strictly Bluegrass,
Litquake, Sunday Streets and the Greek Food Festival had not posted 2027 dates. Any list that shows
2027 dates for those events is extrapolating, not reporting.</p>

<p><strong>3. Official pages frequently disagree with each other.</strong>
{len(flagged)} entries carry a genuine irregularity. The recurring patterns are:
<br>· <em>Hours differ between two City/organizer pages</em> — Alemany Farmers Market (7am-2pm on
sf.gov vs 7am-3pm in the City's own market rules PDF); Heart of the City Farmers' Market (two
different hour sets on the operator's own site); Castro Night Market (5-9pm vs 5-10pm); Chinatown
Autumn Moon Festival (11am-5pm from the organizer vs 11am-6pm in the SFMTA advisory).
<br>· <em>Stale official pages</em> — the Haight Ashbury Street Fair's About page still says the
fair is held "every second Sunday in June" while the 2026 fair was held September 20; the City's
sf.gov Filipino American History Month page still lists the previous FilBookFest edition;
Castro Street Fair, Union Street Festival and Pistahan pages still show 2026 content.
<br>· <em>Moved or rescheduled editions</em> — the San Francisco Opera Ball was rescheduled from
September 12 to November 12, 2026 because of orchestra labor negotiations.</p>

<p><strong>4. Third-party calendars are the main source of wrong SF event lists.</strong> Four
items were excluded because they are repeatedly listed as San Francisco events when they are not,
or no longer happen: How Weird Street Faire (official site: "The Faire is done"), the Ghirardelli
Chocolate Festival (no edition on the venue's own events page since 2018), the Great Dickens
Christmas Fair (Cow Palace, Daly City) and Super Bowl LX / FIFA World Cup 2026 / 49ers games
(Levi's Stadium, Santa Clara). None of these would survive an official-source check.</p>

<p><strong>5. Geography matters.</strong> Several large "SF" draws are held outside the City and
County of San Francisco — Levi's Stadium, the Cow Palace, Oakland and Berkeley venues. The register
only includes events whose official page places them inside the city; for a few multi-venue events
(SFFILM, Frameline, Noise Pop) the festival is San Francisco-based even where individual screenings
or shows are in neighbouring cities, which is noted on those rows.</p>

<p><strong>6. Source concentration.</strong> Verification leaned on {len(org_counts)} distinct
official domains. City sources (sf.gov, sfrecpark.org, sfmta.com, sfpl.org, sfport.com) cover the
civic and parks layer; festival organizers cover the rest. Where a City page and an organizer page
disagreed, the organizer page was treated as authoritative for the event's own schedule and the
disagreement was flagged.</p>
</div>

<h2>Official source domains used</h2>
<table><thead><tr><th>Domain</th><th>Entries sourced</th></tr></thead><tbody>{src_rows}</tbody></table>

<h2>Limits of this register</h2>
<div class="warnbox"><p>This is a register of the events that could be confirmed on an official
page on {esc(GENERATED)}. It is not a claim to be exhaustive: smaller neighbourhood fairs, single
venue concert series, museum openings and library programmes exist in San Francisco that this pass
did not reach. Adding them is additive — each needs its own official source link, and the schema in
<code>data/events.json</code> already supports it.</p></div>"""
page("analysis.html", "Analysis & findings", b, "analysis.html")

# --------------------------------------------------------------------------
# methodology
# --------------------------------------------------------------------------
b = f"""<h1>Method &amp; sources</h1>
<p class="sub">How each row was produced, and the rules that governed it.</p>

<h2>Rules applied</h2>
<div class="panel">
<ol>
<li><strong>Geography.</strong> Only events inside the City and County of San Francisco. Events at
Levi's Stadium, the Cow Palace and other out-of-city venues are excluded and listed on
<a href="flagged.html">Flagged for Review</a>.</li>
<li><strong>Official sources only.</strong> Every row cites the organizer's site, a City of San
Francisco page (sf.gov, sfrecpark.org, sfmta.com, sfpl.org, sfport.com) or the venue's own page.
Aggregator calendars (Funcheap, SF Station, Timeout, hotel and travel blogs) were used only to
discover candidate events, never as a row's source.</li>
<li><strong>No inference.</strong> If a value could not be read off an official page it was left
blank and the row marked <span class="badge b-unv">unverified</span>. Dates were never extrapolated
from a previous year's pattern, even where the pattern is obvious.</li>
<li><strong>Conflicts are published, not resolved silently.</strong> Where two official sources
disagree, the row is marked <span class="badge b-flag">flagged</span> and the disagreement is
written out with both sources named.</li>
<li><strong>Reproducibility.</strong> The register is generated from <code>data/events.json</code>
by <code>tools/build_site.py</code>; <code>tools/validate.py</code> enforces the schema and
<code>tools/linkcheck.py</code> checks every internal link in the built site.</li>
</ol>
</div>

<h2>Schema</h2>
<div class="panel"><p>Each event row carries:</p>
<p>{"".join(f'<span class="tag">{esc(k)}</span>' for k in EVENTS[0].keys())}</p>
<p class="small"><code>date_status</code> is <code>confirmed</code> when the date cell holds a date
read from an official page, and <code>unverified</code> when the field is empty because no official
page publishes one. <code>status</code> is <code>flagged</code> only for genuine irregularities.</p>
</div>

<h2>Verification log</h2>
<div class="panel"><p>All rows were checked on {esc(GENERATED)}. The table below lists every source
cited by the register; each is an official organizer, City or venue page.</p></div>
{table(sorted(EVENTS, key=lambda e: e['source_name']), show_notes=False)}

<h2>Coordination</h2>
<div class="panel"><p>This repository is shared by multiple agent sessions. Task ownership,
verification records and the merge/deploy log live in
<a href="https://github.com/buffedlizard55-lab/MaltaProj5/blob/main/COORDINATION.md">COORDINATION.md</a>
at the repository root.</p></div>"""
page("methodology.html", "Method & sources", b, "methodology.html")

# --------------------------------------------------------------------------
os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
with open(os.path.join(OUT, "data", "events.json"), "w") as f:
    json.dump(DATA, f, indent=2)

with open(os.path.join(OUT, ".nojekyll"), "w") as f:
    f.write("")

built = sorted(x for x in os.listdir(OUT) if x.endswith(".html"))
print(f"built {len(built)} pages: {', '.join(built)}")
print(f"events={len(EVENTS)} flagged={len(flagged)} unverified_dates={len(unverified)}")
