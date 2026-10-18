"""Dependency-free, deterministic static Pages build; committed HTML works without JS.

Inputs:  data/events.json, data/sources.json, data/review.json, data/verify_report.json
Outputs: 12 HTML pages + data/events.csv
"""
import csv
import io
import json
from collections import Counter
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(n):
    return json.loads((ROOT / "data" / n).read_text())


rows = load("events.json")
sources = load("sources.json")
findings = load("review.json")
try:
    report = load("verify_report.json")
except FileNotFoundError:
    report = {"summary": {}, "rows": {}}

nav = [
    ("index.html", "Overview"),
    ("weekly.html", "Every week"),
    ("monthly.html", "Every month"),
    ("annual.html", "Every year"),
    ("special.html", "Special events"),
    ("markets.html", "Markets & food"),
    ("museums.html", "Museums & science"),
    ("culture.html", "Festivals & culture"),
    ("community.html", "Community & outdoors"),
    ("analysis.html", "Analysis"),
    ("review.html", "Flagged for Review"),
    ("sources.html", "Sources & method"),
]

CHECK_LABEL = {
    "field-level": "Field-level check",
    "page-level": "Page-level check",
    "flagged": "Flagged",
}
CHECK_TITLE = {
    "field-level": "A researcher transcribed these values from the cited official page; the link was re-checked in integration.",
    "page-level": "The cited official page was fetched and the event name found; individual values were not re-transcribed in integration.",
    "flagged": "This row carries unresolved review notes or its source could not be confirmed automatically.",
}


def link(s):
    x = sources[s]
    return f'<a href="{e(x["url"])}" rel="noreferrer">{e(x["publisher"])} &#8599;</a>'


def badge(r):
    level = (r.get("check") or {}).get("level", "page-level")
    label = CHECK_LABEL.get(level, level)
    n, u = len(r["flags"]), len(r.get("unverified", []))
    cls = "flag" if n or level == "flagged" else ("warn" if level == "page-level" else "ok")
    extra = f" · {n} note{'s' if n != 1 else ''}" if n else ""
    if u:
        extra += f" · {u} unverified"
    return (f'<span class="check {cls}" title="{e(CHECK_TITLE.get(level, ""))}">'
            f'{e(label)}{extra}</span>')


def table(rs, caption="Official-source inventory · blank cells are unverified · times as published by the organizer",
          prefix="", controls=True):
    table_id = "events" if controls else "events-" + (prefix.strip("-") or "alt")
    tools = ('<div class="tools"><label>Search this table <input type="search" id="search" '
             'placeholder="Event, venue, or schedule…"></label><label>Recurrence '
             '<select id="kind"><option value="">All types</option>'
             + "".join(f"<option>{x}</option>" for x in ["Weekly", "Monthly", "Annual", "Special"])
             + '</select></label><button id="reset" type="button">Reset</button>'
             f'<span id="count" role="status">{len(rs)} entries</span></div>') if controls else ""
    out = (tools + f'<div class="table-wrap"><table id="{table_id}">'
           f'<caption>{e(caption)}</caption><thead><tr>'
           + "".join(f'<th scope="col">{h}</th>' for h in
                     ["Event / category", "Pattern", "Date or recurrence", "Time", "SF venue",
                      "Admission", "Official source &amp; verification"])
           + '</tr></thead><tbody>')
    for r in rs:
        notes = ("<details><summary>Review notes</summary><ul>"
                 + "".join("<li>" + e(f) + "</li>" for f in r["flags"]) + "</ul></details>"
                 if r["flags"] else '<span class="badge">No review notes</span>')
        if r.get("unverified"):
            notes += ('<details class="unv"><summary>Unverified blank fields</summary><ul>'
                      + "".join("<li>" + e(f) + "</li>" for f in r["unverified"]) + "</ul></details>")
        srcs = "".join("<div>" + link(s) + "</div>" for s in r["sources"])
        parent = ('<small>Dated occurrence of the After Dark series — not a separate series</small>'
                  if r["parent"] else "")
        out += (f'<tr id="{prefix}{r["id"]}" data-kind="{r["kind"]}" data-category="{e(r["category"])}">'
                f'<th scope="row">{e(r["name"])}<small>{e(r["category"])}</small>{parent}</th>'
                + "".join("<td>" + e(r[k]) + "</td>"
                          for k in ["kind", "schedule", "time", "venue", "price"])
                + f'<td>{srcs}<a class="evidence" href="sources.html#event-{r["id"]}">Row evidence</a>'
                + badge(r) + notes
                + ("<p>" + e(r["notes"]) + "</p>" if r["notes"] else "")
                + "</td></tr>")
    out += "</tbody></table></div>"
    if controls:
        out += ('<p id="empty" hidden>No matching entries. Try another search or reset the filters.</p>')
    return out


def page(file, title, desc, body, eyebrow="SF EVENTS / RESEARCH DIRECTORY"):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(desc)}">
<title>{e(title)} · SF Events</title>
<link rel="stylesheet" href="assets/style.css"><script defer src="assets/app.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<aside><a class="brand" href="index.html"><span class="logo">SF</span> events<span class="dot">.</span></a>
<p class="eyebrow">CITY EVENT OBSERVATORY</p>
<nav aria-label="Main navigation">{"".join(f'<a href="{f}"' + (' aria-current="page"' if f == file else "") + ">" + label + "</a>" for f, label in nav)}</nav>
<div class="sidebar-note">SAN FRANCISCO ONLY<br>Official sources. Open evidence.<br><b>Research snapshot</b><br>18 October 2026<br><br>
{len(rows)} entries · {len(sources)} sources</div></aside>
<main id="main"><header><span>{e(eyebrow)}</span><a href="data/events.csv" download>Download CSV ↓</a></header>
<div class="heading"><p class="eyebrow">EXPLORE YOUR CITY, WITH EVIDENCE</p><h1>{e(title)}</h1><p>{e(desc)}</p></div>
{body}
<footer>Independent research directory, not an official City website. Schedules change; check the organizer before attending.
<a href="sources.html">Method &amp; limitations</a> · <a href="review.html">Flagged for Review</a> ·
<a href="https://github.com/buffedlizard55-lab/MaltaProj5">Repository &#8599;</a></footer>
</main></body></html>'''


def write(file, title, desc, body, eyebrow="SF EVENTS / RESEARCH DIRECTORY"):
    (ROOT / file).write_text(page(file, title, desc, body, eyebrow))


def pct(a, b):
    return f"{a * 100 // b}%" if b else "—"


kinds = Counter(r["kind"] for r in rows)
cats = Counter(r["category"] for r in rows)
flagged = [r for r in rows if r["flags"]]
series = sum(1 for r in rows if not r["parent"])
domains = {sources[s]["url"].split("/")[2] for r in rows for s in r["sources"]}
levels = Counter((r.get("check") or {}).get("level", "page-level") for r in rows)
summ = report.get("summary", {})
report_urls = set(report.get("urls", {}))
current_source_urls = {source["url"] for source in sources.values()}
uncovered_source_urls = sorted(current_source_urls - report_urls)
stale_report_urls = sorted(report_urls - current_source_urls)
dead_report_urls = {item["url"] for item in report.get("dead", [])}
dead_current_urls = dead_report_urls & current_source_urls
dead_stale_urls = dead_report_urls - current_source_urls

stats = ('<section class="stats" aria-label="Inventory statistics">'
         + "".join(f'<article class="{cls}"><span>{label}</span><strong>{value}</strong><small>{note}</small></article>'
                   for label, value, note, cls in [
                       ("Inventory entries", len(rows), "Dated occurrences counted separately", ""),
                       ("Regular events", kinds["Weekly"] + kinds["Monthly"],
                        f'{kinds["Weekly"]} weekly · {kinds["Monthly"]} monthly', ""),
                       ("Annual events", kinds["Annual"], "Yearly editions and seasons", ""),
                       ("Special events", kinds["Special"], "Dated programmes and one-off editions", ""),
                       ("Official sources", len(sources), f"{len(domains)} distinct domains", ""),
                       ("Rows with review notes", len(flagged), f"{pct(len(flagged), len(rows))} of the register", "warn"),
                   ]) + "</section>")

legend = ('<div class="notice"><b>A transparent inventory, not an exhaustive calendar of the city.</b> '
          'Every row links to the official page it was checked against on <b>18 October 2026</b>. '
          'A blank cell means <b>unverified</b> — not free, not “not applicable”. '
          'Dates are reproduced as published; next editions are never generated from a pattern. '
          f'{len(flagged)} rows carry open review notes; all are published on '
          '<a href="review.html">Flagged for Review</a> rather than silently resolved.'
          '</div>'
          '<div class="legend"><span class="check ok">Field-level check</span> values transcribed from the official page '
          '<span class="check warn">Page-level check</span> page + event name re-confirmed automatically '
          '<span class="check flag">Flagged</span> unresolved note or unconfirmed value</div>')

cards = ('<section class="intro"><h2>A rhythm for every kind of day</h2>'
         '<p>Weekly routines, monthly gatherings, annual traditions and dated special programmes. '
         'Category and rhythm are editorial groupings, not organizer claims.</p><div class="cards">'
         + "".join(f'<a href="{f}"><span>{label}</span><strong>{n:02d}</strong><small>Browse entries →</small></a>'
                   for f, label, n in [
                       ("weekly.html", "Every week", kinds["Weekly"]),
                       ("monthly.html", "Every month", kinds["Monthly"]),
                       ("annual.html", "Every year", kinds["Annual"]),
                       ("special.html", "Special programmes", kinds["Special"]),
                   ])
         + "</div></section>")

cat_cards = ('<h2>Browse by category</h2><div class="cards cats">'
             + "".join(f'<a href="{f}"><span>{c}</span><strong>{cats[c]:02d}</strong>'
                       f'<small>Official-source rows →</small></a>'
                       for f, c in [("markets.html", "Markets & food"),
                                    ("museums.html", "Museums & science"),
                                    ("culture.html", "Festivals & culture"),
                                    ("community.html", "Community & outdoors")])
             + "</div>")

howto = ('<section class="prose"><h2>How this register was built</h2><ol>'
         '<li><b>Four research passes were reconciled row by row</b> into one register (sessions '
         '3a19e72d, 5a85baf2, 4f47c142 and a1b7522f). Overlapping rows were merged, not dropped: '
         'each keeps its official source.</li>'
         '<li><b>Only official pages</b> supply facts: organizers, venues, museums and City bodies. '
         'Tourism-board guides and third-party calendars were used for discovery only.</li>'
         '<li><b>Automated re-check:</b> every cited URL is fetched from GitHub Actions and the page text is '
         'searched for the event name. Bot-blocked pages are reported, not silently passed.</li>'
         f'<li><b>Result:</b> {summ.get("name_found", 0)} of {summ.get("rows", len(rows))} rows had the event name '
         'confirmed on a cited page in the latest automated pass; the rest are labelled and listed on the '
         'Flagged page.</li></ol></section>')

write("index.html", "San Francisco, in events.",
      "Recurring gatherings and special occasions inside the City and County of San Francisco — "
      "organized, source-linked, and honest about what is still unknown.",
      stats + legend + cards + cat_cards +
      '<h2>All inventory entries</h2>' + table(rows) +
      '<h2>Read next</h2><div class="cards"><a href="analysis.html"><span>Analysis</span>'
      '<strong>Findings</strong><small>What the register shows →</small></a>'
      '<a href="review.html"><span>Review queue</span>'
      f'<strong>{len(flagged):02d}</strong><small>Unverified values & irregularities →</small></a>'
      '<a href="sources.html"><span>Method</span><strong>Sources</strong>'
      '<small>Ledger, excerpts, limits →</small></a></div>' + howto)

KIND_DESC = {
    "Weekly": ("Weekly events", "Events with a weekly rhythm — farmers markets, museum nights and standing programmes. "
                               "Seasonal pauses and exceptions are kept in the date column, not smoothed away."),
    "Monthly": ("Monthly events", "Events that recur once a month or on a named monthly pattern, such as first "
                                 "Thursdays or second Sundays."),
    "Annual": ("Annual events", "Yearly traditions, festivals, parades and seasons. Next editions appear only when "
                               "the organizer has published them."),
    "Special": ("Special events", "Dated programmes, one-off editions and limited runs. 'Special' is an editorial "
                                 "label: it means a dated instance, not proof that the event never repeats."),
}
for kind, (title, desc) in KIND_DESC.items():
    write(kind.lower() + ".html", title, desc, legend + table([r for r in rows if r["kind"] == kind],
                                                              f"{title} · official-source rows"))

for file, cat in [("markets.html", "Markets & food"), ("museums.html", "Museums & science"),
                  ("culture.html", "Festivals & culture"), ("community.html", "Community & outdoors")]:
    write(file, cat, f"Every register entry grouped under {cat}. Follow each official source and its row evidence "
                     "for details and limitations.",
          table([r for r in rows if r["category"] == cat], f"{cat} · official-source rows"))

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
month_counts = Counter()
for r in rows:
    for m in MONTHS:
        if m.lower() in (r["schedule"] + " " + r["notes"]).lower():
            month_counts[m] += 1
top_months = [m for m in MONTHS if month_counts[m]]
pubs = Counter()
for r in rows:
    for s in r["sources"]:
        pubs[sources[s]["publisher"].split("—")[0].strip()] += 1
gov = sum(1 for s in sources.values() if ".gov" in s["url"])
org = sum(1 for s in sources.values() if ".org" in s["url"])
com = sum(1 for s in sources.values() if s["url"].split("/")[2].endswith((".com", ".world", ".net")))

analysis = f'''<section class="prose">
<h2>What the register contains</h2>
<p>{len(rows)} entries across four rhythms and four editorial categories. {series} are series or standalone
entries; {len(rows) - series} are dated occurrences of another series (the After Dark themes), which is why
counts should not be read as unique gatherings.</p>
<table class="plain"><thead><tr><th>Measure</th><th>Value</th><th>Share</th></tr></thead><tbody>
{''.join(f'<tr><td>{k}</td><td>{v}</td><td>{pct(v, len(rows))}</td></tr>' for k, v in kinds.most_common())}
{''.join(f'<tr><td>{k}</td><td>{v}</td><td>{pct(v, len(rows))}</td></tr>' for k, v in cats.most_common())}
</tbody></table>

<h2>Verification status</h2>
<p>Three labels are used. <b>Field-level</b> rows had their individual values transcribed from the official
page by a researcher. <b>Page-level</b> rows were inherited from an independent pass; in integration the
page was fetched and the event name confirmed, but each date and price was not re-transcribed.
<b>Flagged</b> rows carry an unresolved value or note.</p>
<table class="plain"><thead><tr><th>Level</th><th>Rows</th><th>Meaning</th></tr></thead><tbody>
<tr><td>Field-level</td><td>{levels['field-level']}</td><td>Values transcribed from the cited official page</td></tr>
<tr><td>Page-level</td><td>{levels['page-level']}</td><td>Page and event name re-confirmed automatically</td></tr>
<tr><td>Flagged</td><td>{levels['flagged']}</td><td>An unresolved note; see the Flagged page</td></tr>
</tbody></table>
<p>Saved automated snapshot ({e(report.get('checked_at', 'not yet run'))}): <b>{summ.get('name_found', 0)}</b> rows
had the event name found on a cited page, <b>{summ.get('name_not_found', 0)}</b> did not,
<b>{summ.get('no_response', 0)}</b> had no response, and <b>{summ.get('pdf_not_checked', 0)}</b> cite a PDF.
It lists <b>{summ.get('dead_urls', 0)}</b> dead/connection-failed URL(s), including <b>{len(dead_stale_urls)}</b>
no longer cited in the current source ledger; <b>{len(dead_current_urls)}</b> current source URL(s) were
reported dead. <b>{summ.get('blocked_urls', 0)}</b> URL(s) blocked the automated client or returned a
server error. <b>{len(uncovered_source_urls)}</b> current source URL(s) are absent from this saved snapshot
and <b>{len(stale_report_urls)}</b> are historical-only. The row-source snapshot is not a live exhaustive
check; current source links and exact gaps are listed on <a href="review.html">Flagged for Review</a>.
A blocked page is not evidence of a bad event, and automated name matching does not confirm dates, times,
venue or admission.</p>

<h2>Coverage of the annual calendar</h2>
<p>Counting the rows that explicitly mention each month (a row may mention several):</p>
<div class="bars">{''.join(f'<div><span>{m}</span><i style="width:{month_counts[m] * 100 // max(month_counts.values() or [1])}%"></i><b>{month_counts[m]}</b></div>' for m in MONTHS)}</div>
<p>Mentions peak in May–June and September–November, dip in July–August and are lowest in January.
These are mentions, not unique events: one row can name several months, and the counts include
recurring schedules as well as annual editions.</p>

<h2>Source concentration</h2>
<p>{len(sources)} source records across {len(domains)} domains — {gov} government domains, {org} non-profit
or association domains, and {com} commercial organizer/venue domains. The most-cited publishers are:</p>
<ol>{''.join(f'<li>{e(p)} — {n} row citation(s)</li>' for p, n in pubs.most_common(8))}</ol>

<h2>What the data shows — and what it cannot</h2>
<ul>
<li><b>It is a festival city with a thin weekly layer.</b> {kinds['Annual']} annual entries against
{kinds['Weekly']} weekly ones. The weekly layer is mostly farmers markets, museum nights and standing
park programmes.</li>
<li><b>Blank is the honest default.</b> {len(flagged)} rows carry review notes and
{sum(1 for r in rows if r.get("unverified"))} have at least one blank tracked field. Where an organizer has not
published a next date, the date cell is blank rather than extrapolated — a recurring pattern is not a
confirmed future instance.</li>
<li><b>Many entries record 2026 editions that have already taken place</b> (for example Tulip Day in
March, the Opera Ball gala and the July 4 fireworks). They are retained as dated records and are not
presented as upcoming; the register has no “upcoming only” filter because that would require
re-deriving dates the organizers have not published.</li>
<li><b>There is no citywide denominator.</b> No official source publishes a complete count of San Francisco
events, so this register cannot claim exhaustive coverage. Known gaps: library programmes, most theatre,
neighbourhood block parties, sports beyond the Giants, and weekday civic meetings.</li>
<li><b>Two registers were reconciled.</b> The 86-row register (sessions 3a19e72d/5a85baf2) and the 167-row
inventory (session 4f47c142) were merged with an explicit map; overlapping rows were reconciled rather
than counted twice.</li>
</ul>

<h2>Method &amp; limitations</h2>
<p>The full verification rules, the source ledger with transcribed excerpts and the row-by-row evidence
ledger are on the <a href="sources.html">Sources &amp; method</a> page. Unresolved findings are on
<a href="review.html">Flagged for Review</a>. External links were live at check time; availability can change
and is re-tested in CI, not continuously.</p>
</section>'''
write("analysis.html", "Analysis & findings",
      "What the register contains, how much of it is verified, where coverage is thin, and what the data "
      "cannot support — all computed from the published register.", analysis)

body = ('<h2>Research findings &amp; coverage gaps</h2><div class="table-wrap"><table>'
        '<caption>Unresolved findings do not block publication; they are not confirmed upcoming event rows.</caption>'
        '<thead><tr><th>Finding</th><th>Review detail</th><th>Sources / references</th></tr></thead><tbody>')
for f in findings:
    body += ('<tr><th scope="row">' + e(f["title"]) + "</th><td>" + e(f["detail"]) + "</td><td>"
             + "".join(link(s) + "<br>" for s in f.get("sources", []))
             + "".join('<a href="' + e(u) + '">Reference / official site ↗</a><br>' for u in f.get("urls", []))
             + "</td></tr>")
body += '</tbody></table></div><h2>Entry-level review queue</h2>' + table(flagged, "Rows with at least one open review note")
body += ('<h2>Blank fields (unverified, no separate review note)</h2>'
         + table([r for r in rows if r.get("unverified") and not r["flags"]],
                 "Blank cells mean unverified — not free and not not-applicable", prefix="blank-", controls=False))
write("review.html", "Flagged for Review",
      "Unconfirmed values are blank. Source conflicts, missing years, admission gaps and coverage gaps are "
      "visible here — not silently resolved.", body)

body = '''<section class="prose"><h2>Verification rules</h2><ol>
<li>Only organizer, venue, museum or municipal pages supply admitted facts. Tourism-board guides and
third-party calendars were used for discovery only. Exception, published rather than hidden: a small number of
rows could be sourced only to SF Travel (the city's destination-marketing body); those rows are labelled
<b>flagged</b>, named in the source-concentration finding, and listed on the Flagged for Review page.</li>
<li>Official pages were read on 18 October 2026 and the supported event names, schedules, times, venues and
admission restrictions transcribed. Excerpts below are selected transcriptions, not complete archived pages.</li>
<li>Weekly, monthly and annual classifications require explicit recurrence language. <i>Special</i> is an
editorial bucket for dated programmes; it does not mean one-time only.</li>
<li>Dates are preserved as published. Next occurrences are not generated from a pattern, and a recurring
pattern is not presented as a confirmed future instance.</li>
<li>Only San Francisco venues are admitted. Events at Levi's Stadium, the Cow Palace and other out-of-city
venues are excluded and recorded on the review page. No nearby Bay Area cities or online-only programmes.</li>
<li>Blank schedule, time, venue or admission cells are flagged unverified. A source link verifies only the
facts it states; a blank admission cell never means free.</li>
<li>Automated re-check: every cited URL is fetched in CI and its text searched for the event name. Pages that
block automated clients are reported, not treated as verified. Automation cannot prove a date or price.</li>
</ol>
<h2>Analysis &amp; limitations</h2>
<p>This snapshot is not a complete list of all San Francisco events and makes no claim to be one: no
citywide denominator exists. Museum, market and festival programmes are over-represented; library
programmes, most theatre, weekday civic meetings and many neighbourhood events are under-covered.
No claim is made about popularity, attendance or current ticket availability.</p>
<p>Rows are labelled <b>field-level</b> (values transcribed from the page by a researcher),
<b>page-level</b> (page and event name re-confirmed by the automated pass, values not re-transcribed) or
<b>flagged</b> (unresolved note). The After Dark themes are dated occurrences of one weekly series and are
not double-counted as series.</p>
<p>No continuous refresh is claimed. CI checks data structure, evidence references, local links and the live
status of each cited URL; it cannot establish factual truth.</p></section>
<h2>Official-source register</h2>'''
for sid, s in sources.items():
    manual = " · read manually in integration" if s.get("manual") else ""
    body += (f'<article class="source" id="source-{sid}"><h3>{e(s["publisher"])}</h3>'
             f'<a href="{e(s["url"])}" rel="noreferrer">{e(s["url"])} ↗</a>'
             f'<p>Checked {e(s["checked"])}{manual} · {e(s["method"])}</p>'
             f'<blockquote>{e(s["excerpt"])}</blockquote></article>')
body += '<h2>Row-by-row evidence ledger</h2>'
for r in rows:
    body += (f'<article class="source" id="event-{r["id"]}"><h3>{e(r["name"])}</h3><dl>'
             + "".join(f"<dt>{e(k)}</dt><dd>{e(v)} · "
                       + ", ".join(f'<a href="#source-{s}">{e(sources[s]["publisher"])}</a>'
                                   for s in r["evidence"].get(k, [])) + "</dd>"
                       for k, v in r.items() if k in ["name", "schedule", "time", "venue", "price"] and v)
             + "</dl><p>Verification: " + e((r.get("check") or {}).get("level", "page-level"))
             + " · Unverified / review: " + e("; ".join(r["flags"]) or "no open notes") + "</p></article>")
write("sources.html", "Sources & method",
      "Every row links to official pages. This ledger records what was checked, the supporting excerpts, "
      "and what remains unresolved.", body)

f = io.StringIO()
w = csv.writer(f, lineterminator="\n")
w.writerow(["id", "name", "category", "kind", "schedule", "time", "venue", "price",
            "source_urls", "checked", "verification", "parent", "review"])
for r in rows:
    w.writerow([r[k] for k in ["id", "name", "category", "kind", "schedule", "time", "venue", "price"]]
               + [" | ".join(sources[s]["url"] for s in r["sources"]), "2026-10-18",
                  (r.get("check") or {}).get("level", "page-level"), r["parent"], " | ".join(r["flags"])])
(ROOT / "data" / "events.csv").write_text(f.getvalue())
print(f"Built {len(nav)} pages, {len(rows)} rows, {len(sources)} official-source records.")
