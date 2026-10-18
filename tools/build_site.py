#!/usr/bin/env python3
"""
Build the static GitHub Pages site in docs/ from the verified event datasets.

Usage: python3 tools/build_site.py   (from the repository root)

Inputs:  data/events-weekly.json, data/events-annual.json,
         data/events-special.json, data/exclusions.json
Outputs: docs/index.html, docs/weekly-events.html, docs/annual-events.html,
         docs/special-events.html, docs/flagged.html,
         docs/assets/style.css, docs/assets/app.js,
         docs/data/events.json, docs/data/events.csv
"""
import csv
import html
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
SNAPSHOT = "2026-10-18"
REPO_URL = "https://github.com/buffedlizard55-lab/MaltaProj5"
SITE_TITLE = "SF Events &mdash; San Francisco Events Inventory"

MONTHS = ["", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def esc(s):
    return html.escape(str(s), quote=True)


def load(name):
    with open(os.path.join(DATA, name)) as f:
        return json.load(f)


weekly = load("events-weekly.json")["events"]
annual = load("events-annual.json")["events"]
special = load("events-special.json")["events"]
exclusions = load("exclusions.json")["exclusions"]

for e in weekly:
    e.setdefault("dates_2027", "")
for e in special:
    e.setdefault("dates_2027", "")

all_events = weekly + annual + special
n_total = len(all_events)
n_weekly, n_annual, n_special = len(weekly), len(annual), len(special)
n_verified = sum(1 for e in all_events if e.get("status") == "verified")
n_flagged = sum(1 for e in all_events if e.get("status") == "flagged")
n_free = sum(1 for e in all_events if "free" in (e.get("cost") or "").lower())

flagged_events = [e for e in all_events if e.get("status") == "flagged"]

# ---------------- analysis ----------------
month_counts = Counter(e.get("month") for e in annual if e.get("month"))
max_month = max(month_counts.values()) if month_counts else 1
type_counts = Counter(e.get("type", "Other") for e in all_events)
n_blank_2026 = sum(1 for e in annual + special if not (e.get("dates_2026") or "").strip())
n_2027 = sum(1 for e in all_events if (e.get("dates_2027") or "").strip())
upcoming_specials = [e for e in special if e.get("upcoming")]

ANALYSIS_FINDINGS = [
    ("The calendar peaks in &ldquo;Second Summer.&rdquo; " +
     f"Annual events cluster in May&ndash;October ({sum(v for k, v in month_counts.items() if 5 <= k <= 10)} of {n_annual} " +
     "annual events fall in those months). September and October alone host " +
     f"{month_counts.get(9, 0) + month_counts.get(10, 0)} annual events, including Hardly Strictly Bluegrass, " +
     "Fleet Week, Folsom Street Fair and the Italian Heritage Parade."),
    ("Weekly life is anchored by markets and museum nights. " +
     f"San Francisco runs {sum(1 for e in weekly if e['type'] == 'Farmers market')} weekly farmers markets " +
     "year-round, operated mainly by three organizations (Foodwise, PCFMA and the Agricultural Institute of Marin), " +
     "plus recurring weekly museum nights (Cal Academy NightLife, Exploratorium After Dark) and the Golden Gate Park " +
     "Band, which has played free Sunday concerts since 1882."),
    (f"Free access is the norm. {n_free} of {n_total} listed events ({round(100 * n_free / n_total)}%) are free to " +
     "attend or free with donations &mdash; including the city&rsquo;s largest festivals (Hardly Strictly Bluegrass, " +
     "Stern Grove, Pride, Carnaval, Fleet Week, Sunday Streets)."),
    (f"Verification status. {n_verified} of {n_total} rows are fully verified against official sources; {n_flagged} " +
     "rows carry flags (typically a date not yet announced, a missing organizer website, or a detail sourced only " +
     "from the official tourism body&rsquo;s guide). Every row links to an official source; values that could not " +
     "be confirmed were left blank &mdash; never inferred."),
    ("2026 was a one-off-heavy year. Special 2026-only events included the Red Bull Showrun F1 street demo " +
     "(Feb 21), Fourth of July fireworks launched from the Golden Gate Bridge towers for America&rsquo;s 250th " +
     "birthday (Jul 4), the Pokemon World Championships at Moscone (Aug 28&ndash;30) and Super Bowl LX fan events " +
     "(the game itself was played in Santa Clara)."),
    ("Look-ahead is short. As of the snapshot date, only " +
     f"{n_2027} events had officially announced 2027 dates (SF Pride, June 26&ndash;27, 2027; Cherry Blossom " +
     "Festival, April 10&ndash;11 and 17&ndash;18, 2027). Most organizers announce next-year dates 3&ndash;9 months out."),
    ("Out-of-city listings are common in &ldquo;San Francisco&rdquo; calendars. Events at the Cow Palace (Daly City), " +
     "PayPal Park (San Jose), Levi&rsquo;s Stadium (Santa Clara), Shoreline-adjacent festivals and even Sonoma and " +
     "Mill Valley film festivals appear in SF-branded guides. This dataset excludes them and logs each exclusion " +
     "on the Flagged for Review page."),
]

# ---------------- shared UI pieces ----------------

def status_badge(e):
    if e.get("status") == "flagged":
        return '<span class="badge badge-flag" title="Has flagged items - see Flagged for Review">Flagged</span>'
    return '<span class="badge badge-ok" title="Every shown value confirmed from the linked official source">Verified</span>'


def src(e):
    return (f'<a href="{esc(e["source_url"])}" target="_blank" rel="noopener">'
            f'{esc(e["source_name"])}</a>')


def cell(v, blank_note="Not confirmed from an official source - left blank by policy"):
    v = (v or "").strip()
    if not v:
        return f'<td class="blank" title="{esc(blank_note)}">&mdash;</td>'
    return f"<td>{esc(v)}</td>"


def row(e, idx=None):
    name = esc(e["name"])
    if e.get("status") == "flagged":
        name += ' <span class="dot" title="Flagged for Review">&#9873;</span>'
    num = f'<td class="num">{idx}</td>' if idx is not None else ""
    upcoming = ""
    if e.get("upcoming"):
        upcoming = ' <span class="badge badge-up" title="After the 2026-10-18 snapshot date">Upcoming</span>'
    return (
        f"<tr data-name=\"{esc(e['name']).lower()}\" "
        f"data-type=\"{esc(e.get('type', '')).lower()}\" "
        f"data-status=\"{esc(e.get('status', ''))}\">"
        f"{num}"
        f"<td class=\"ev\">{name}{upcoming}</td>"
        f"<td>{esc(e.get('type', ''))}</td>"
        f"{cell(e.get('frequency') or e.get('dates_2026'))}"
        f"{cell(e.get('dates_2026'))}"
        f"<td>{esc(e.get('location', ''))}<div class=\"sub\">{esc(e.get('neighborhood', ''))}</div></td>"
        f"<td>{esc(e.get('organizer', ''))}</td>"
        f"{cell(e.get('cost'))}"
        f"<td class=\"src\">{src(e)}</td>"
        f"<td>{status_badge(e)}</td>"
        f"</tr>"
    )


NAV_LINKS = [("index.html", "Dashboard"), ("weekly-events.html", "Weekly &amp; Regular"),
             ("annual-events.html", "Annual"), ("special-events.html", "Special"),
             ("flagged.html", "Flagged for Review"), ("data/events.json", "Data (JSON)")]


def make_nav(active):
    nav = "".join(
        '<a href="{}"{}>{}</a>'.format(
            href,
            (' class="active" aria-current="page"' if href == active else ""),
            label)
        for href, label in NAV_LINKS)
    return ('<header class="topbar">\n<div class="wrap bar">\n'
            '<a class="brand" href="index.html"><span class="logo">SF</span> '
            '<span>San Francisco Events<em>verified inventory &amp; analysis</em></span></a>\n'
            '<input type="checkbox" id="navtoggle" class="navtoggle" aria-label="Toggle navigation">\n'
            '<label for="navtoggle" class="navburger">&#9776;</label>\n'
            '<nav class="nav">' + nav + '</nav>\n</div>\n</header>')


def page(title, active, body, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | SF Events</title>
<meta name="description" content="Verified inventory of events happening within the city of San Francisco: weekly, annual and special events, each sourced to an official site.">
<link rel="stylesheet" href="assets/style.css">
{extra_head}
</head>
<body>
{make_nav(active)}
<main class="wrap">
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <p><strong>San Francisco Events Inventory</strong> &middot; data snapshot {SNAPSHOT} &middot; every row links to an
    official source (event organizer, venue, or government / official tourism body). Unconfirmed values are left blank and flagged &mdash; never inferred.</p>
    <p>Sources include sf.gov, SFMTA, SF Environment, the Port of San Francisco, the Presidio Trust, SF Travel (the City&rsquo;s
    destination marketing organization) and each event&rsquo;s or venue&rsquo;s official website. See the
    <a href="flagged.html">Flagged for Review</a> page for irregularities and exclusions.</p>
    <p><a href="{REPO_URL}" target="_blank" rel="noopener">Repository</a> &middot;
    <a href="{REPO_URL}/blob/main/COORDINATION.md" target="_blank" rel="noopener">COORDINATION.md</a> (task board &amp; verification log) &middot;
    <a href="data/events.csv" target="_blank" rel="noopener">Download CSV</a> &middot;
    <a href="data/events.json" target="_blank" rel="noopener">Download JSON</a></p>
  </div>
</footer>
<script src="assets/app.js"></script>
</body>
</html>"""


def controls(page_kind):
    if page_kind == "annual":
        month_opts = "".join(
            f'<option value="{m}">{MONTHS[m]}</option>' for m in range(1, 13) if month_counts.get(m)
        )
        month_filter = (f'<label class="ctl">Month <select id="f-month"><option value="">All months</option>'
                        f"{month_opts}</select></label>")
    else:
        month_filter = ""
    upcoming = ("" if page_kind != "special" else
                '<label class="ctl check"><input type="checkbox" id="f-upcoming"> Upcoming only</label>')
    return f"""
<div class="toolbar" data-page="{page_kind}">
  <input id="f-search" class="search" type="search" placeholder="Search events, locations, organizers&hellip;" aria-label="Search table">
  <label class="ctl">Status <select id="f-status"><option value="">All</option><option value="verified">Verified</option><option value="flagged">Flagged</option></select></label>
  {month_filter}
  {upcoming}
  <span class="count" id="row-count"></span>
</div>"""


def table(events, numbered=True, month_groups=None):
    thead = ("<tr><th>#</th>" if numbered else "<tr>") + """
<th>Event</th><th>Type</th><th>Frequency / Schedule</th><th>2026 dates</th><th>Location</th><th>Organizer</th><th>Cost</th><th>Official source</th><th>Status</th></tr>"""
    if month_groups:
        body = []
        idx = 1
        for m, evs in month_groups:
            body.append(f'<tbody class="mgroup" data-month="{m}">')
            body.append(f'<tr class="monthrow"><td colspan="10">{MONTHS[m]} <span class="pill">{len(evs)}</span></td></tr>')
            for e in evs:
                body.append(row(e, idx)); idx += 1
            body.append("</tbody>")
        return f'<table class="events" id="evt-table"><thead>{thead}</thead>{"".join(body)}</table>'
    body = "".join(row(e, i + 1) for i, e in enumerate(events))
    return f'<table class="events" id="evt-table"><thead>{thead}</thead><tbody>{body}</tbody></table>'


# ---------------- pages ----------------

stat_cards = f"""
<section class="stats">
  <a class="card" href="weekly-events.html"><div class="big">{n_weekly}</div><div class="lbl">Weekly &amp; regular events</div><div class="hint">markets, museum nights, monthly street parties</div></a>
  <a class="card" href="annual-events.html"><div class="big">{n_annual}</div><div class="lbl">Annual events</div><div class="hint">festivals, parades &amp; races that recur every year</div></a>
  <a class="card" href="special-events.html"><div class="big">{n_special}</div><div class="lbl">Special events</div><div class="hint">one-off &amp; dated events, incl. {len(upcoming_specials)} upcoming</div></a>
  <div class="card"><div class="big">{round(100 * n_verified / n_total)}%</div><div class="lbl">Fully verified</div><div class="hint">{n_verified} of {n_total} rows (every value from an official source)</div></div>
  <a class="card warn" href="flagged.html"><div class="big">{n_flagged}</div><div class="lbl">Flagged for review</div><div class="hint">unverified dates, irregularities, exclusions</div></a>
</section>"""

bars = "".join(
    f'<div class="brow"><span class="bmonth">{MONTHS[m]}</span>'
    f'<span class="btrack"><span class="bfill" style="width:{round(100 * month_counts.get(m, 0) / max_month)}%"></span></span>'
    f'<span class="bval">{month_counts.get(m, 0)}</span></div>'
    for m in range(1, 13))

index_body = f"""
<section class="hero">
  <h1>Every event in San Francisco, <span>verified.</span></h1>
  <p class="lede">A complete, organized inventory of events happening <strong>within the city of San Francisco only</strong> &mdash;
  split into <strong>regularly occurring</strong> events (weekly/monthly schedules and annual traditions) and <strong>special events</strong>.
  Every row links to an official source: the event&rsquo;s organizer, its venue, or a government / official tourism body.
  Unconfirmed values are left blank and flagged, never guessed.</p>
  <p class="snap">Data snapshot: <strong>{SNAPSHOT}</strong> &middot; {n_total} events &middot; {len(exclusions)} documented exclusions (out-of-city or out-of-scope)</p>
</section>
{stat_cards}
<section class="grid2">
  <div class="panel">
    <h2>Annual events by month</h2>
    <p class="p-sub">Where the {n_annual} annually recurring events fall on the calendar.</p>
    {bars}
  </div>
  <div class="panel">
    <h2>Key findings</h2>
    <ol class="findings">{''.join(f'<li>{f}</li>' for f in ANALYSIS_FINDINGS)}</ol>
  </div>
</section>
<section class="panel">
  <h2>Browse by category</h2>
  <div class="cats">
    <a class="cat" href="weekly-events.html"><h3>Weekly &amp; Regular</h3><p>Farmers markets (12+ weekly), museum nights, free tours, street parties &amp; seasonal series that recur on a weekly or monthly rhythm.</p></a>
    <a class="cat" href="annual-events.html"><h3>Annual</h3><p>The yearly calendar: parades (Chinese New Year, St. Patrick&rsquo;s, Pride, Italian Heritage), festivals (Outside Lands, Carnaval, Folsom), races and traditions like the Nutcracker.</p></a>
    <a class="cat" href="special-events.html"><h3>Special</h3><p>Dated, one-off events: 2026 specials (Red Bull Showrun, Golden Gate Bridge fireworks for America&rsquo;s 250th), opera productions, concerts, exhibitions &mdash; with upcoming dates highlighted.</p></a>
    <a class="cat" href="flagged.html"><h3>Flagged for Review</h3><p>Everything we could not fully confirm, with reasons and source links &mdash; plus the exclusion log for events outside city limits or scope.</p></a>
  </div>
</section>
<section class="panel">
  <h2>Method &amp; scope</h2>
  <ul class="method">
    <li><strong>Geography:</strong> events must take place inside San Francisco city limits. Notable nearby events at out-of-city venues (Cow Palace/Daly City, PayPal Park/San Jose, Levi&rsquo;s Stadium/Santa Clara, and others) are excluded and logged.</li>
    <li><strong>Sourcing:</strong> each row links to an official site &mdash; the organizer&rsquo;s or venue&rsquo;s own website, a City of San Francisco site (sf.gov, SFMTA, SF Environment, Port of SF, Presidio Trust), or SF Travel, the City&rsquo;s official destination marketing organization. Aggregators and media articles are never the source of record.</li>
    <li><strong>Verification:</strong> every row was checked against its linked source on {SNAPSHOT}. If a value (typically a not-yet-announced date) could not be confirmed, it was left blank and the row is flagged on the Flagged for Review page. Nothing is inferred.</li>
    <li><strong>Editorial scope:</strong> professional sports league schedules and trade conventions are excluded as categories (individual special events at those venues are included).</li>
    <li><strong>Coordination:</strong> research, verification and integration are logged in <a href="{REPO_URL}/blob/main/COORDINATION.md" target="_blank" rel="noopener">COORDINATION.md</a> in the repository.</li>
  </ul>
</section>"""

weekly_body = f"""
<section class="ph">
  <h1>Weekly &amp; regularly occurring events</h1>
  <p>{n_weekly} events that recur on a weekly, monthly or seasonal-yearly rhythm &mdash; farmers markets, museum nights, free tours,
  street parties and series. Schedules verified against official sources on {SNAPSHOT}.</p>
</section>
{controls('weekly')}
{table(weekly)}
<section class="note">
  <p><strong>Reading blank cells:</strong> a dash (&mdash;) means the value could not be confirmed from an official source and was left blank
  rather than inferred &mdash; see <a href="flagged.html">Flagged for Review</a>.</p>
</section>"""

annual_groups = []
for m in range(1, 13):
    evs = [e for e in annual if e.get("month") == m]
    if evs:
        annual_groups.append((m, evs))
annual_body = f"""
<section class="ph">
  <h1>Annually recurring events</h1>
  <p>{n_annual} events that happen every year &mdash; parades, festivals, races, fairs and traditions &mdash; grouped by month,
  with verified 2026 dates (and 2027 dates where officially announced).</p>
</section>
{controls('annual')}
{table(None, month_groups=annual_groups)}
<section class="note"><p><strong>Reading blank cells:</strong> a dash (&mdash;) means the value could not be confirmed from an official source
(typically a date not yet announced) &mdash; see <a href="flagged.html">Flagged for Review</a>.</p></section>"""

special_body = f"""
<section class="ph">
  <h1>Special events (one-off &amp; dated)</h1>
  <p>{n_special} dated events that are not annual traditions &mdash; 2026 one-offs, opera productions, concerts, exhibitions and more.
  Events after {SNAPSHOT} carry an <span class="badge badge-up">Upcoming</span> badge ({len(upcoming_specials)} upcoming).</p>
</section>
{controls('special')}
{table(special)}
<section class="note"><p>Scope notes: professional sports schedules and trade conventions are excluded as categories; out-of-city events are
logged on the <a href="flagged.html">Flagged for Review</a> page.</p></section>"""

flag_rows = []
for i, e in enumerate(flagged_events, 1):
    flags = "; ".join(e.get("flags") or [])
    blanks = []
    if not (e.get("dates_2026") or "").strip():
        blanks.append("2026 dates")
    if not (e.get("dates_2027") or "").strip() and e.get("category") != "special":
        pass
    flag_rows.append(
        f"<tr><td class='num'>{i}</td><td class='ev'>{esc(e['name'])}</td>"
        f"<td>{esc(e.get('category',''))}</td>"
        f"<td>{esc(flags)}</td>"
        f"<td class='src'>{src(e)}</td></tr>")
flagged_table = ("<table class='events'><thead><tr><th>#</th><th>Event</th><th>Category</th>"
                 "<th>Issue</th><th>Official source</th></tr></thead><tbody>"
                 + "".join(flag_rows) + "</tbody></table>")

excl_rows = []
for i, x in enumerate(exclusions, 1):
    excl_rows.append(
        f"<tr><td class='num'>{i}</td><td class='ev'>{esc(x['name'])}</td>"
        f"<td>{esc(x.get('venue',''))}</td><td>{esc(x['reason'])}</td>"
        f"<td>{esc(x.get('dates',''))}</td>"
        f"<td class='src'><a href='{esc(x['source_url'])}' target='_blank' rel='noopener'>{esc(x['source_name'])}</a></td></tr>")
excl_table = ("<table class='events'><thead><tr><th>#</th><th>Event</th><th>Venue</th><th>Reason for exclusion</th>"
              "<th>Dates (context)</th><th>Source</th></tr></thead><tbody>" + "".join(excl_rows) + "</tbody></table>")

flagged_body = f"""
<section class="ph">
  <h1>Flagged for Review</h1>
  <p>Items that need a human decision or that could not be fully confirmed from official sources, plus the exclusion log.
  Nothing on this page blocks the site or the data &mdash; it is published for your review. <strong>Snapshot: {SNAPSHOT}.</strong></p>
</section>
<section class="panel">
  <h2>1 &middot; Flagged events ({n_flagged})</h2>
  <p class="p-sub">These rows appear in the category tables with a <span class="badge badge-flag">Flagged</span> badge. Typical issues:
  a 2026/2027 date not yet announced, no dedicated organizer website, or details confirmed only via SF Travel (the official tourism body)
  rather than the organizer directly.</p>
  {flagged_table}
</section>
<section class="panel">
  <h2>2 &middot; Exclusion log ({len(exclusions)})</h2>
  <p class="p-sub">Events excluded because they happen outside San Francisco city limits or fall outside editorial scope, each with the reason.
  Several were found listed inside &ldquo;San Francisco&rdquo; event guides and are flagged here as irregularities.</p>
  {excl_table}
</section>
<section class="panel">
  <h2>3 &middot; Notable irregularities found during verification</h2>
  <ul class="method">
    <li><strong>Stale or recycled event info:</strong> a third-party guide claimed an &ldquo;Opera at the Ballpark &mdash; La Traviata, Nov 11, 2026&rdquo;
    at Oracle Park. The official SF Opera 2026&ndash;27 season contains no <em>La Traviata</em>, and the official simulcast page still shows the
    Nov 11, <em>2022</em> edition. The claim was rejected and logged (see exclusion log).</li>
    <li><strong>Ambiguous race date:</strong> The Giant Race (Oracle Park) has no clearly dated 2026 edition: SF Travel lists it undated, and the
    Giants&rsquo; events page shows &ldquo;August 17&ndash;18&rdquo;, which matches the 2024 edition. Date left unverified.</li>
    <li><strong>SF-branded guides list out-of-city events:</strong> SF Travel&rsquo;s monthly guides include events in Daly City (Cow Palace),
    Sonoma, Mill Valley, Half Moon Bay, Woodside and San Jose under &ldquo;San Francisco&rdquo; events. All are excluded here and logged.</li>
    <li><strong>Date moved:</strong> SF Opera&rsquo;s Opera Ball 2026 was moved from Sep 12 to Nov 12, 2026 per the Opera&rsquo;s announcement &mdash;
    both dates appear in different listings.</li>
    <li><strong>TBD holiday dates:</strong> as of the snapshot, 2026 lighting-ceremony dates for Union Square and Ghirardelli Square were listed
    as &ldquo;TBD&rdquo; by SF Travel; Embarcadero Center&rsquo;s official site had published Nov 18, 2026 (40th annual).</li>
    <li><strong>Hours discrepancy:</strong> SF Travel lists Ferry Plaza Farmers Market Tuesday hours as 8am; the operator (Foodwise) lists 10am&ndash;2pm.
    The operator&rsquo;s value is used.</li>
    <li><strong>New Year&rsquo;s Eve fireworks:</strong> the annual Embarcadero midnight fireworks are documented by the Port of San Francisco for
    Dec 31, 2025; the 2026/27 edition had not been published on official City pages at snapshot time.</li>
  </ul>
</section>"""

# ---------------- write outputs ----------------
os.makedirs(os.path.join(DOCS, "assets"), exist_ok=True)
os.makedirs(os.path.join(DOCS, "data"), exist_ok=True)

pages = {
    "index.html": ("Dashboard", "index.html", index_body),
    "weekly-events.html": ("Weekly & Regular Events", "weekly-events.html", weekly_body),
    "annual-events.html": ("Annual Events", "annual-events.html", annual_body),
    "special-events.html": ("Special Events", "special-events.html", special_body),
    "flagged.html": ("Flagged for Review", "flagged.html", flagged_body),
}
for fname, (title, active, body) in pages.items():
    with open(os.path.join(DOCS, fname), "w") as f:
        f.write(page(title, active, body))
    print("wrote", fname)

with open(os.path.join(DOCS, "data", "events.json"), "w") as f:
    json.dump({
        "snapshot_date": SNAPSHOT,
        "counts": {"total": n_total, "weekly": n_weekly, "annual": n_annual,
                   "special": n_special, "verified": n_verified, "flagged": n_flagged},
        "events": all_events,
        "exclusions": exclusions,
    }, f, indent=2)
print("wrote data/events.json")

with open(os.path.join(DOCS, "data", "events.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "category", "type", "frequency", "dates_2026", "dates_2027",
                "location", "neighborhood", "organizer", "cost", "source_url",
                "source_name", "status", "flags", "notes"])
    for e in all_events:
        w.writerow([e.get(k, "") if k != "flags" else "; ".join(e.get("flags") or [])
                    for k in ["name", "category", "type", "frequency", "dates_2026", "dates_2027",
                              "location", "neighborhood", "organizer", "cost", "source_url",
                              "source_name", "status", "flags", "notes"]])
print("wrote data/events.csv")
print(f"TOTAL events: {n_total} (weekly {n_weekly} / annual {n_annual} / special {n_special}); "
      f"verified {n_verified}, flagged {n_flagged}, free {n_free}")
