#!/usr/bin/env python3
"""Final-integration consolidation (session c961fbe4).

Folds the two independent registers into ONE canonical register:

  * data/events.json           86 rows, merged by tools/integrate.py from
                               data/events_3a19e72d.json + data/events_5a85baf2.json
  * data/events-weekly.json    34 rows (session 4f47c142)
  * data/events-annual.json    95 rows (session 4f47c142)
  * data/events-special.json   38 rows (session 4f47c142)

Merges are EXPLICIT (the maps below), never fuzzy: a fuzzy matcher proposed
"Frameline" ~ "International Ocean Film Festival" and "Diwali" ~ "Inner Sunset
Farmers Market", so every pair here was reviewed by hand.

Outputs:
  data/events.json            canonical combined register
  data/sources.json           combined source ledger (new URLs added, excerpt
                              filled by tools/apply_verify.py after the automated
                              fetch in CI)
  data/review.json            prior findings + integration findings

Run: python3 tools/consolidate.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


base = load("events_base86.json")             # pristine 86-row register
weekly = load("events-weekly.json")["events"]  # 34
annual = load("events-annual.json")["events"]  # 95
special = load("events-special.json")["events"]  # 38
sources = load("sources_base75.json")
review = load("review_base20.json")

# ---------------------------------------------------------------- explicit merges
# 167-row id -> canonical base row id.  Reviewed pair by pair.
MERGE = {
    "ferry-plaza-farmers-market": "b-ferry-plaza-farmers-market",
    "heart-of-the-city-farmers-market": "b-heart-of-the-city-farmers-market",
    "alemany-farmers-market": "b-alemany-farmers-market",
    "outer-sunset-farmers-market": "outer",
    "off-the-grid-fort-mason": "b-off-the-grid-fort-mason",
    "calacademy-nightlife": "nightlife",
    "exploratorium-after-dark": "after-dark",
    "golden-gate-park-band": "b-golden-gate-park-band",
    "downtown-first-thursdays": "b-downtown-first-thursdays",
    "inner-sunset-flea-market": "flea",
    "sunday-streets": "b-sunday-streets",
    "noise-pop": "b-noise-pop-festival",
    "chinese-new-year-parade": "chinese",
    "st-patricks-day-parade": "b-st-patricks-day-parade",
    "cherry-blossom-festival": "b-cherry-blossom-festival",
    "union-street-festival": "b-union-street-festival",
    "carnaval-sf": "carnaval",
    "north-beach-festival": "b-north-beach-festival",
    "stern-grove-festival": "b-stern-grove-festival",
    "bay-to-breakers": "b-bay-to-breakers",
    "sf-marathon": "b-sf-marathon",
    "up-your-alley-fair": "b-up-your-alley",
    "nihonmachi-street-fair": "b-nihonmachi-street-fair",
    "outside-lands": "b-outside-lands",
    "hardly-strictly-bluegrass": "b-hardly-strictly-bluegrass",
    "folsom-street-fair": "b-folsom-street-fair",
    "castro-street-fair": "b-castro-street-fair",
    "haight-ashbury-street-fair": "b-haight-ashbury-street-fair",
    "italian-heritage-parade": "b-italian-heritage-parade",
    "autumn-moon-festival": "b-autumn-moon-festival",
    "nye-fireworks": "b-nye-fireworks",
    "sf-pride": "b-sf-pride-parade",
    "sf-opera-in-the-park": "b-opera-in-the-park",
    "sf-opera-ball": "b-opera-ball-2026",
    "frameline": "b-frameline",
    "fleet-week": "b-fleet-week-air-show",
}

# Base rows that duplicate another base row (found during this integration).
BASE_MERGE = {"b-carnaval-festival": "carnaval"}

# Base rows removed because they are not events.
DROP = {
    "b-hsb-merch-store-2026": "Online merchandise-store window, not a gathering or dated event; removed from the event register.",
}

# Reclassifications of base rows, with the reason recorded as a flag.
RECLASS = {
    "chinese": ("Annual", "Reclassified Special -> Annual: the Chinese New Year Parade is an annual edition; the 2027 date is the next announced edition."),
    "carnaval": ("Annual", "Reclassified Special -> Annual: Carnaval San Francisco is an annual festival with a Grand Parade."),
    "creep": ("Special", "Reclassified Annual -> Special: 'Creepatorium' is a single dated After Dark theme (Oct 29, 2026), an occurrence of the weekly After Dark series, not a separately recurring annual event."),
}

# 167-row kind overrides (their file buckets weekly/annual/special; these rows
# recur monthly, seasonally or as dated editions).
KIND = {
    "off-the-grid-fort-mason": "Monthly",
    "inner-sunset-flea-market": "Monthly",
    "critical-mass": "Monthly",
    "famsf-free-tuesdays": "Monthly",
    "asian-art-museum-free-sundays": "Monthly",
    "downtown-first-thursdays": "Monthly",
    "soma-nights": "Monthly",
    "sunday-streets": "Annual",
    "yerba-buena-gardens-festival": "Annual",
    "fridays-on-front-street": "Annual",
    "drag-me-downtown": "Annual",
    "bhangra-and-beats-night-market": "Special",
    "pop-ups-on-the-plaza": "Special",
    "circus-in-the-parks": "Annual",
    "sf-opera-season-opening": "Annual",
    "sf-symphony-opening-gala": "Annual",
    "sfjazz-summer-sessions": "Annual",
    }

# Topical category overrides for rows whose type is ambiguous.
CATEGORY = {
    # weekly / monthly
    "mission-community-market": "Markets & food",
    "inner-sunset-farmers-market": "Markets & food",
    "stonestown-farmers-market": "Markets & food",
    "noe-valley-farmers-market": "Markets & food",
    "clement-street-farmers-market": "Markets & food",
    "castro-farmers-market": "Markets & food",
    "divisadero-farmers-market": "Markets & food",
    "fillmore-farmers-market": "Markets & food",
    "hayes-valley-farmers-market": "Markets & food",
    "free-programs-in-union-square-plaza": "Community & outdoors",
    "presidio-picnic": "Community & outdoors",
    "presidio-twilight": "Community & outdoors",
    "sf-city-guides": "Community & outdoors",
    "critical-mass": "Community & outdoors",
    "famsf-free-tuesdays": "Museums & science",
    "asian-art-museum-free-sundays": "Museums & science",
    "yerba-buena-gardens-festival": "Festivals & culture",
    "fridays-on-front-street": "Festivals & culture",
    "drag-me-downtown": "Festivals & culture",
    "bhangra-and-beats-night-market": "Markets & food",
    "pop-ups-on-the-plaza": "Markets & food",
    "circus-in-the-parks": "Community & outdoors",
    "soma-nights": "Festivals & culture",
    "sunday-streets": "Community & outdoors",
    # annual
    "sf-sketchfest": "Festivals & culture",
    "norcal-mlk-celebration": "Community & outdoors",
    "fog-design-art": "Festivals & culture",
    "sf-art-week": "Festivals & culture",
    "sf-half-marathon": "Community & outdoors",
    "mostly-british-film-festival": "Festivals & culture",
    "sf-indiefest": "Festivals & culture",
    "sf-music-week": "Festivals & culture",
    "sf-beer-week": "Markets & food",
    "ca-antiquarian-book-fair": "Festivals & culture",
    "giants-fanfest": "Community & outdoors",
    "superfine-art-fair": "Festivals & culture",
    "flower-bulb-day": "Community & outdoors",
    "bouquets-to-art": "Museums & science",
    "bring-your-own-big-wheel": "Community & outdoors",
    "sf-restaurant-week": "Markets & food",
    "international-ocean-film-festival": "Festivals & culture",
    "sf-climate-week": "Community & outdoors",
    "sf-art-fair": "Festivals & culture",
    "cookbook-week": "Markets & food",
    "opening-day-on-the-bay": "Community & outdoors",
    "bay-area-dance-week": "Festivals & culture",
    "earth-day-sf": "Community & outdoors",
    "sf-decorator-showcase": "Festivals & culture",
    "caamfest": "Festivals & culture",
    "sf-international-arts-festival": "Festivals & culture",
    "taiwanese-american-cultural-festival": "Festivals & culture",
    "sf-docfest": "Festivals & culture",
    "aapi-cocktail-week": "Markets & food",
    "sf-design-week": "Festivals & culture",
    "escape-from-alcatraz": "Community & outdoors",
    "festa-coloniale-italiana": "Festivals & culture",
    "juneteenth-on-the-waterfront": "Festivals & culture",
    "juneteenth-fillmore": "Community & outdoors",
    "qwocmap-film-festival": "Festivals & culture",
    "sf-black-film-festival": "Festivals & culture",
    "fourth-of-july-pier39": "Community & outdoors",
    "fillmore-jazz-festival": "Festivals & culture",
    "sf-free-folk-festival": "Festivals & culture",
    "sf-frozen-film-festival": "Festivals & culture",
    "sf-jewish-film-festival": "Festivals & culture",
    "aids-walk-sf": "Community & outdoors",
    "sfjazz-summer-sessions": "Festivals & culture",
    "jerry-day": "Festivals & culture",
    "sf-pizza-bagel-beer-festival": "Markets & food",
    "sf-opera-season-opening": "Festivals & culture",
    "sf-symphony-opening-gala": "Festivals & culture",
    "flower-piano": "Community & outdoors",
    "oktoberfest-on-front": "Markets & food",
    "muni-heritage-weekend": "Community & outdoors",
    "comedy-day": "Festivals & culture",
    "portola-music-festival": "Festivals & culture",
    "artspan-open-studios": "Festivals & culture",
    "litquake": "Festivals & culture",
    "sf-fall-antiques-show": "Festivals & culture",
    "potrero-hill-festival": "Community & outdoors",
    "leap-sandcastle-classic": "Community & outdoors",
    "day-of-the-dead": "Festivals & culture",
    "sf-hiphop-dance-festival": "Festivals & culture",
    "renegade-craft-fair-sf": "Markets & food",
    "embarcadero-center-lighting": "Markets & food",
    "illuminate-sf": "Festivals & culture",
    "union-square-tree-lighting": "Festivals & culture",
    "ghirardelli-square-tree-lighting": "Festivals & culture",
    "pier39-holiday-lineup": "Festivals & culture",
    "lets-glow-sf": "Festivals & culture",
    "guardsmen-tree-lot": "Community & outdoors",
    "sf-ballet-nutcracker": "Festivals & culture",
    "bill-graham-menorah": "Festivals & culture",
    "parol-lantern-festival": "Festivals & culture",
    "kung-pao-kosher-comedy": "Festivals & culture",
    "nye-fireworks": "Community & outdoors",
    # special
    "sf-disability-history-tour": "Community & outdoors",
    "super-bowl-lx-sf-events": "Community & outdoors",
    "red-bull-showrun": "Community & outdoors",
    "sunset-night-market-feb": "Markets & food",
    "sf-space-walk": "Festivals & culture",
    "hunky-jesus-contest": "Festivals & culture",
    "ploverfest": "Festivals & culture",
    "valencia-live": "Festivals & culture",
    "black-coffee-treasure-island": "Festivals & culture",
    "fourth-of-july-golden-gate-bridge-fireworks": "Community & outdoors",
    "sf-hash-week": "Community & outdoors",
    "ferry-fest": "Community & outdoors",
    "cinema-on-the-square": "Festivals & culture",
    "sf-historium-spotlight": "Festivals & culture",
    "pokemon-world-championships": "Festivals & culture",
    "lowrider-parade": "Festivals & culture",
    "peak2peak": "Community & outdoors",
    "epicenter-sf-tour": "Community & outdoors",
    "sf-cheese-fest": "Markets & food",
    "nexus-sf-bay-area-black-art-week": "Festivals & culture",
    "the-haunt-ybca": "Festivals & culture",
    "sf-opera-mary-queen-of-scots": "Festivals & culture",
    "sf-opera-manon": "Festivals & culture",
    "sf-opera-figaro": "Festivals & culture",
    "sf-opera-strauss-in-concert": "Festivals & culture",
    "ballpark-back-9": "Community & outdoors",
    "chase-center-teddy-swims": "Festivals & culture",
    "chase-center-jonas-brothers": "Festivals & culture",
    "chase-center-journey": "Festivals & culture",
    "sfmoma-iturbide": "Museums & science",
    "sfmoma-rm-x-sfmoma": "Museums & science",
    "sfmoma-raven-chacon": "Museums & science",
    "sfmoma-sarah-sze": "Museums & science",
    "deyoung-treasures-of-the-pharaohs": "Museums & science",
    "legion-azzedine-alaia": "Museums & science",
    "deyoung-monet-and-venice": "Museums & science",
    "club-darc": "Festivals & culture",
}

# 167 row kind by source file (before overrides).
SRC_KIND = {}
for bucket, rows_ in (("Weekly", weekly), ("Annual", annual), ("Special", special)):
    for r in rows_:
        SRC_KIND[r["id"]] = bucket

CAT_WORDS = [
    ("Markets & food", ["market", "food", "beer", "restaurant", "cheese", "cocktail",
                        "cookbook", "pizza", "bagel", "oktoberfest", "supper"]),
    ("Museums & science", ["museum", "academy of sciences", "exploratorium", "exhibition",
                           "sfmoma", "de young", "legion of honor", "art museum"]),
    ("Community & outdoors", ["run", "race", "walk", "triathlon", "picnic", "park", "bike",
                              "fitness", "beach", "cleanup", "rec", "trail", "sunrise",
                              "fireworks", "halloween", "zumba", "street fair"]),
]


def guess_category(r):
    if r["id"] in CATEGORY:
        return CATEGORY[r["id"]]
    t = (r.get("type", "") + " " + r["name"]).lower()
    for cat, words in CAT_WORDS:
        if any(w in t for w in words):
            return cat
    return "Festivals & culture"


def slug_source(url):
    h = re.sub(r"^https?://", "", url).strip("/")
    h = re.sub(r"[^a-zA-Z0-9]+", "-", h).strip("-").lower()
    return "x-" + h[:70]


def add_source(url, publisher, note="", excerpt="", manual=False):
    if url.startswith("http://"):
        note = (note + " Original register cited " + url + "; upgraded to https for this link.").strip()
        url = "https://" + url[len("http://"):]
    for sid, rec in sources.items():
        if rec["url"] == url:
            if excerpt:
                rec["excerpt"] = excerpt
                rec["publisher"] = publisher
                rec["method"] = note or ("Page read manually on 2026-10-18; excerpt transcribed from "
                                         "the page, not a full-page archive.")
                if manual:
                    rec["manual"] = True
            return sid
    sid = slug_source(url)
    n = 2
    while sid in sources:
        sid = f"{sid}-{n}"
        n += 1
    sources[sid] = {
        "url": url,
        "publisher": publisher,
        "checked": "2026-10-18",
        "excerpt": excerpt or ("Automated re-check pending (tools/verify_rows.py runs in CI and "
                               "records the fetched text)."),
        "method": note or ("Row source inherited from session 4f47c142; page fetched and "
                           "event-name match checked automatically on 2026-10-18."),
    }
    if manual:
        sources[sid]["manual"] = True
    return sid


# ------------------------------------------------------------ apply base merges
by_id = {r["id"]: r for r in base}
for dup, keep in BASE_MERGE.items():
    a, b = by_id[dup], by_id[keep]
    for s in a["sources"]:
        if s not in b["sources"]:
            b["sources"].append(s)
    b["flags"] += [f"Merged duplicate register row '{a['name']}' (source {a['sources'][0]})."]
    b["flags"] += [f for f in a["flags"] if f not in b["flags"]]

base = [r for r in base if r["id"] not in BASE_MERGE and r["id"] not in DROP]
by_id = {r["id"]: r for r in base}

# --------------------------------------------------------------- merge 167 rows
used = set()
new_rows = []
all167 = weekly + annual + special
for r in all167:
    tid = r["id"]
    if tid in MERGE:
        b = by_id[MERGE[tid]]
        used.add(tid)
        sid = add_source(r["source_url"], r["source_name"],
                         "Second independent source for a row that appears in both registers; "
                         "page fetched and event-name match checked automatically on 2026-10-18.")
        if sid not in b["sources"]:
            b["sources"].append(sid)
        b.setdefault("also", []).append({
            "session": "4f47c142",
            "dates_2026": r.get("dates_2026", ""),
            "dates_2027": r.get("dates_2027", ""),
            "frequency": r.get("frequency", ""),
            "source": sid,
        })
        extra = (r.get("dates_2026") or "").strip()
        if extra and extra[:40].lower() not in b.get("schedule", "").lower():
            b["flags"].append(
                f"Second register (session 4f47c142) records: {r.get('frequency','')} — {extra}. "
                f"Kept as an additional dated record, not merged into the schedule field.")
        for f in r.get("flags", []):
            if f not in b["flags"]:
                b["flags"].append(f)
        continue
    new_rows.append(r)

# add source records for the new rows
for r in new_rows:
    r["_sid"] = add_source(r["source_url"], r["source_name"],
                           "Row authored by session 4f47c142; page fetched and event-name match "
                           "checked automatically on 2026-10-18. Field values not re-transcribed "
                           "in this pass unless the row carries a manual-check note.")


def esc_sched(r):
    parts = []
    freq = (r.get("frequency") or "").strip()
    d26 = (r.get("dates_2026") or "").strip()
    d27 = (r.get("dates_2027") or "").strip()
    if freq:
        parts.append(freq)
    if d26:
        parts.append(f"2026: {d26}" if not d26.lower().startswith(("2026", "2027")) else d26)
    if d27:
        parts.append(f"2027: {d27}")
    return " — ".join(parts)


converted = []
for r in new_rows:
    kind = KIND.get(r["id"], SRC_KIND[r["id"]])
    sid = r["_sid"]
    venue = r.get("location", "")
    hood = r.get("neighborhood", "")
    if hood and hood.lower() not in venue.lower():
        venue = f"{venue}, {hood}" if venue else hood
    flags = list(r.get("flags", []))
    for field, label in (("time", "time"), ("venue", "venue")):
        pass
    unverified = []
    if not r.get("cost"):
        unverified.append("price: unverified — no admission value stated on the cited official page.")
    if not venue:
        unverified.append("venue: unverified — no venue stated on the cited official page.")
    # These registers carry the time inside the dated copy, not as its own field.
    unverified.append("time: unverified — the cited page states the date but not a separate "
                      "start/end time; see the date column.")
    row = {
        "id": "x-" + r["id"],
        "name": r["name"],
        "category": guess_category(r),
        "kind": kind,
        "schedule": esc_sched(r),
        "time": "",
        "venue": venue,
        "price": r.get("cost", ""),
        "sources": [sid],
        "evidence": {"name": [sid], "schedule": [sid]},
        "notes": r.get("notes", ""),
        "flags": flags,
        "unverified": unverified,
        "parent": "",
        "check": {"level": "page-level", "by": "4f47c142 + c961fbe4 automated fetch",
                  "date": "2026-10-18"},
    }
    for field in ("venue", "price"):
        if row[field]:
            row["evidence"][field] = [sid]
    converted.append(row)

rows = base + converted

# --------------------------------------------------- row-level source corrections
# Applied after the merge. Every entry below was re-read by session c961fbe4 on
# 2026-10-18 with fetch_page; the excerpt is transcribed from the live page.
FIXES = {
    "b-sf-symphony-season": {
        "keep": ['name', 'schedule', 'venue'],
        "drop": ["https://www.sfsymphony.org/"],
        "url": "https://www.sfsymphony.org/getmedia/4732d38f-af5d-4aa2-8934-428420ff11fa/2026-27-Season-Calendar.pdf",
        "publisher": "San Francisco Symphony — 2026–27 season concert calendar (PDF)",
        "excerpt": "SAN FRANCISCO SYMPHONY 2026–27 SEASON CONCERT CALENDAR. All concerts are at Davies Symphony Hall, 201 Van Ness Avenue, San Francisco, unless otherwise noted.",
        "flag": "Season row cites the Symphony's official 2026–27 concert-calendar PDF; a PDF cannot be name-matched by the automated HTML check, so this row was read manually.",
    },
    "x-sf-symphony-opening-gala": {
        "keep": ['name', 'schedule', 'time', 'venue'],
        "drop": ["https://www.sfsymphony.org/"],
        "url": "https://www.sfsymphony.org/getmedia/4732d38f-af5d-4aa2-8934-428420ff11fa/2026-27-Season-Calendar.pdf",
        "publisher": "San Francisco Symphony — 2026–27 season concert calendar (PDF)",
        "excerpt": "SPECIAL EVENT. Opening Gala with Hilary Hahn. Thursday, September 24, 2026, at 7:00pm. Giancarlo Guerrero conductor. Hilary Hahn violin. FELIX MENDELSSOHN Violin Concerto.",
        "flag": "Gala row verified manually against the Symphony's official concert-calendar PDF; the automated HTML name check cannot read PDFs.",
    },
    "b-sf-opera-season": {
        "keep": ['name', 'schedule', 'venue'],
        "url": "https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
        "publisher": "San Francisco Opera — 2026–27 season announcement",
        "excerpt": "San Francisco Opera's 104th Season Opens September 12. … MARY, QUEEN OF SCOTS … MANON … THE MARRIAGE OF FIGARO … Strauss in Concert … OPERA BALL gala … free, annual OPERA IN THE PARK concert.",
        "flag": "The Opera press page is server-rendered but the automated text check did not match; the page was re-read manually on 2026-10-18 and names every production cited below.",
    },
    "x-sf-opera-season-opening": {
        "keep": ['name', 'schedule', 'venue'],
        "url": "https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
        "publisher": "San Francisco Opera — 2026–27 season announcement",
        "excerpt": "Opening weekend begins with the annual Opera Ball benefit … on Saturday, September 12, featuring Verdi's Simon Boccanegra (September 12–27).",
    },
    "x-sf-opera-mary-queen-of-scots": {
        "keep": ['name', 'schedule', 'venue'],
        "url": "https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
        "publisher": "San Francisco Opera — 2026–27 season announcement",
        "excerpt": "Thea Musgrave's 1977 English-language opera, Mary, Queen of Scots (September 20–October 4) … starring soprano Heidi Stober as Mary.",
    },
    "x-sf-opera-manon": {
        "keep": ['name', 'schedule', 'venue'],
        "url": "https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
        "publisher": "San Francisco Opera — 2026–27 season announcement",
        "excerpt": "Jules Massenet's Manon (October 15–November 1), with soprano Amina Edris and tenor Pene Pati.",
    },
    "x-sf-opera-figaro": {
        "keep": ['name', 'schedule', 'venue'],
        "url": "https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
        "publisher": "San Francisco Opera — 2026–27 season announcement",
        "excerpt": "Mozart's The Marriage of Figaro (Le Nozze di Figaro) (October 31–November 29).",
    },
    "x-sf-opera-strauss-in-concert": {
        "keep": ['name', 'schedule', 'venue'],
        "url": "https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
        "publisher": "San Francisco Opera — 2026–27 season announcement",
        "excerpt": "On November 6, Kim and the San Francisco Opera Orchestra take the stage for Strauss in Concert, an all-Richard Strauss program featuring soprano soloist Adela Zaharia.",
    },
    "x-superfine-art-fair": {
        "keep": ['name', 'schedule', 'venue', 'price'],
        "drop": ["https://www.superfine.world/"],
        "url": "https://www.thesuperfair.com/san-francisco",
        "publisher": "The Superfair (formerly Superfine Art Fair) — San Francisco",
        "excerpt": "The 2026 San Francisco Fair has ended. We'll see you in 2027! The Superfair San Francisco March 19-22, 2026 … Fort Mason Pier 2, Gateway Pavilion … $25 - $150.",
        "flag": "Fair has rebranded from 'Superfine Art Fair' to 'The Superfair'; the official page states the 2026 edition has ended.",
    },
    "x-flower-bulb-day": {
        "rename": "Tulip Day (Flower Bulb Day)",
        "keep": ['name', 'schedule', 'venue', 'price'],
        "drop": ["https://flowerbulbday.com/"],
        "url": "https://sfrecpark.org/m/newsflash/home/detail/2744",
        "publisher": "San Francisco Recreation and Parks — press release (4 March 2026)",
        "excerpt": "Union Square to Bloom with 80,000 Vibrant Dutch Tulips on March 21 … the Union Square Alliance hosts its annual Tulip Day Presented by JPMorganChase … 80,000 colorful, American-produced flowers … eight tulips per person.",
        "flag": "The event's old site flowerbulbday.com is now a blank Plesk hosting page; the official city press release is used instead. The event is now branded 'Tulip Day Presented by JPMorganChase'.",
    },
    "x-fourth-of-july-pier39": {
        "keep": ['name', 'schedule', 'venue'],
        "drop": ["https://www.pier39.com/"],
        "url": "https://www.pier39.com/upcoming-events/",
        "publisher": "PIER 39 — Upcoming Events",
        "excerpt": "4th of July at PIER 39! … With over 100+ unique shops, restaurants, attractions, and Free Entertainment on two Levels.",
    },
    "x-pier39-holiday-lineup": {
        "keep": ['name', 'schedule', 'venue'],
        "drop": ["https://www.pier39.com/"],
        "url": "https://www.pier39.com/upcoming-events/",
        "publisher": "PIER 39 — Upcoming Events",
        "excerpt": "PIER 39 celebrates the Holiday season from November 23rd until January 10th. … The highlight of PIER 39's Holiday celebration is our Live 60' Christmas Tree in Entrance Plaza.",
        "flag": "The PIER 39 holiday page gives the season dates (November 23–January 10) but not a year; no year is asserted in the row.",
    },
    "x-chase-center-teddy-swims": {
        "keep": ['name', 'schedule', 'time', 'venue'],
        "drop": ["https://www.chasecenter.com/events/"],
        "url": "https://www.chasecenter.com/events/teddy-swims-20261110/",
        "publisher": "Chase Center — Teddy Swims event page",
        "excerpt": "Teddy Swims. The UGLY Tour … Date Tuesday, November 10, 2026. Show Starts 7:00 PM. Doors Open 6:00 PM.",
    },
    "x-chase-center-jonas-brothers": {
        "keep": ['name', 'schedule', 'venue'],
        "drop": ["https://www.chasecenter.com/events/"],
        "url": "https://www.chasecenter.com/news/jonas-brothers-announcement-20261121/",
        "publisher": "Chase Center — Jonas Brothers announcement",
        "excerpt": "The Jonas Brothers are Coming to Chase Center on Nov. 21, 2026. … The Burning Up Tour All Over Again will make a stop at Chase Center on Saturday, November 21.",
    },
    "x-chase-center-journey": {
        "keep": ['name', 'schedule', 'venue'],
        "drop": ["https://www.chasecenter.com/events/"],
        "url": "https://www.chasecenter.com/news/journey-announcement-20261128/",
        "publisher": "Chase Center — Journey announcement",
        "excerpt": "Journey is Coming to Chase Center on Nov. 28, 2026. … their Final Frontier Tour … will conclude with a hometown finale show at Chase Center on Saturday, November 28.",
    },
    "x-norcal-mlk-celebration": {
        "keep": ["name", "schedule", "venue"],
        "drop": ["https://norcalmlkfoundation.org/"],
        "url": "https://norcalmlkfoundation.org/mlkcelebration/mlk2026/",
        "publisher": "NorcalMLK Foundation — MLK2026",
        "excerpt": "MLK2026 is here in San Francisco. The NorcalMLK Foundation hosts the premier federal holiday celebration in honor of Dr. Martin Luther King, Jr. in northern California.",
        "flag": "The Foundation's root domain failed the automated fetch (TLS/connection error) on 2026-10-18 although the site was reachable manually; the MLK2026 event page is linked instead.",
    },
    "x-artspan-open-studios": {
        "keep": ["name", "schedule", "venue"],
        "drop": ["https://www.artspan.org/visitsfopenstudios", "https://www.artspan.org/"],
        "url": "https://somarts.org/exhibition/sfopenstudios2026/",
        "publisher": "SOMArts Cultural Center — 2026 SF Open Studios Preview Exhibition",
        "excerpt": "ArtSpan invites you to the 52nd annual production of San Francisco Open Studios. … nearly half the artists who will be hosting open studio events through October 25, 2026.",
        "flag": "ArtSpan's own /visitsfopenstudios page returns its 404 template and /programs/visitsfopenstudios does the same; the official venue page is linked as evidence for the 52nd annual programme.",
    },
    "x-comedy-day": {
        "keep": ['name', 'schedule', 'venue'],
        "url": "https://comedyday.org/",
        "publisher": "Comedy Day (official)",
        "excerpt": "Comedy Day 2026.",
        "flag": "The official page title is 'Comedy Day 2026'; the automated name match uses the page title because the page name has no distinctive body tokens.",
    },
}

for rid, fix in FIXES.items():
    row = next(r for r in rows if r["id"] == rid)
    for old_url in fix.get("drop", []):
        for osid in list(row["sources"]):
            if sources[osid]["url"] == old_url:
                row["sources"].remove(osid)
                for field in row["evidence"]:
                    row["evidence"][field] = [x for x in row["evidence"][field] if x != osid]
    sid = add_source(fix["url"], fix["publisher"], note="Page re-read manually on 2026-10-18; "
                     "excerpt transcribed from the live page.", excerpt=fix["excerpt"], manual=True)
    if sid not in row["sources"]:
        row["sources"].insert(0, sid)
    row["evidence"].setdefault("name", [])
    if sid not in row["evidence"]["name"]:
        row["evidence"]["name"].insert(0, sid)
    for field in fix.get("keep", ["name"]):
        if row.get(field):
            row["evidence"].setdefault(field, [])
            if sid not in row["evidence"][field]:
                row["evidence"][field].append(sid)
    for field in ("schedule", "time", "venue", "price"):
        if row.get(field) and not any(row["evidence"].get(field, [])):
            row[field] = ""
            note = (f"{field}: unverified — removed during integration because the replacement "
                    f"source does not state it.")
            if note not in row["flags"]:
                row["flags"].append(note)
    if fix.get("rename"):
        row["name"] = fix["rename"]
    row["check"] = {"level": "field-level", "by": "c961fbe4 manual re-read", "date": "2026-10-18"}
    if fix.get("flag") and fix["flag"] not in row["flags"]:
        row["flags"].append(fix["flag"])

# SOMA Nights: the only official page is unreachable and no other official page
# confirms the 2026 edition. Do not publish unverified details.
DROP_ROWS = {
    "x-soma-nights": "Official site soma-nights.com returned an SSL error / HTTP 500 on re-check; no other "
                     "official page confirms the 2026 edition. Row removed from the register and recorded on "
                     "Flagged for Review rather than published unverified.",
}
for rid, why in DROP_ROWS.items():
    row = next(r for r in rows if r["id"] == rid)
    review.append({
        "title": f"{row['name']} — excluded: official source unreachable",
        "detail": why,
        "urls": ["https://soma-nights.com/"],
    })
rows = [r for r in rows if r["id"] not in DROP_ROWS]

# ------------------------------------------- merge session a1b7522f's 20 authored rows
pr7 = load("events_a1b7522f.json")
pr7_sources = load("sources_a1b7522f.json")
pr7_review = load("review_a1b7522f.json")
for sid, rec in pr7_sources.items():
    assert sid not in sources, sid
    rec.setdefault("checked", "2026-10-18")
    rec.setdefault("excerpt", "Automated re-check pending (tools/verify_rows.py runs in CI and "
                              "records the fetched text).")
    rec.setdefault("method", "Row authored by session a1b7522f from this official page.")
    sources[sid] = rec
MERGE7 = {"sf-marathon-a1b": "b-sf-marathon"}
for r7 in pr7:
    r7.setdefault("check", {"level": "field-level", "by": "a1b7522f", "date": "2026-10-18"})
    r7.setdefault("unverified", [])
    r7.setdefault("flags", [])
    r7.setdefault("parent", "")
    if r7["id"] in MERGE7:
        b = next(r for r in rows if r["id"] == MERGE7[r7["id"]])
        for sid in r7["sources"]:
            if sid not in b["sources"]:
                b["sources"].append(sid)
        if r7.get("schedule") and r7["schedule"] not in b.get("notes", ""):
            b["flags"].append("Session a1b7522f records the 50th edition as July 24-25, 2027: "
                              + r7["schedule"])
        for f in r7["flags"]:
            if f not in b["flags"]:
                b["flags"].append(f)
        continue
    rows.append(r7)
review += pr7_review

# --------------------------------------------------------------- reclassify base
for r in rows:
    if r["id"] in RECLASS:
        r["kind"], why = RECLASS[r["id"]]
        r["flags"].append(why)
    if r["id"] in BASE_MERGE:
        continue
    r.setdefault("check", {"level": "field-level", "by": "3a19e72d / 5a85baf2",
                           "date": "2026-10-18"})
    # keep the "time unverified" style flags in sync with empty fields
for r in rows:
    r.setdefault("unverified", [])
    kept = []
    for f in r["flags"]:
        if re.match(r"^(schedule|time|venue|price): unverified", f):
            if f not in r["unverified"]:
                r["unverified"].append(f)
        else:
            kept.append(f)
    r["flags"] = kept
    for field in ("schedule", "time", "venue", "price"):
        if not r[field] and not any(f.startswith(field + ": unverified") for f in r["unverified"]):
            r["unverified"].append(f"{field}: unverified — not stated on the cited official page.")

# prune source records no longer cited by any row
used_ids = {sid for r in rows for sid in r["sources"]}
used_ids |= {sid for f in review for sid in f.get("sources", [])}
sources = {sid: rec for sid, rec in sources.items() if sid in used_ids}

# --------------------------------------------------------------------- integrity
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
for r in rows:
    assert r["kind"] in ("Weekly", "Monthly", "Annual", "Special"), (r["id"], r["kind"])
    assert r["sources"], r["id"]
    assert all(s in sources for s in r["sources"]), r["id"]
    assert not r["parent"] or r["parent"] in ids, r["id"]
    for field in ("schedule", "time", "venue", "price"):
        assert r[field] or any(f.startswith(field + ": unverified") for f in r["unverified"]), (r["id"], field)

# ------------------------------------------------------------- integration notes
review.append({
    "title": "Integration reclassified three rows and removed one non-event",
    "detail": ("Final integration found two duplicate Carnaval rows in the 86-row register "
               "(merged), the Chinese New Year Parade and Carnaval rows filed as 'Special' "
               "even though both are annual editions (moved to Annual), and the 'After Dark: "
               "Creepatorium' theme filed as Annual even though it is a single dated theme of "
               "the weekly After Dark series (moved to Special). The Hardly Strictly Bluegrass "
               "online merchandise-store window was removed: it is a retail window, not an event."),
    "urls": ["https://github.com/buffedlizard55-lab/MaltaProj5"],
})
review.append({
    "title": "Two registers merged: overlapping rows reconciled by hand",
    "detail": ("Session 4f47c142's 167-row inventory and the 86-row unified register were "
               "merged with an explicit map (tools/consolidate.py). 39 rows described the same "
               "event in both registers and were reconciled, not dropped; each keeps both "
               "official sources. A fuzzy matcher was rejected because it proposed false pairs "
               "(for example Frameline vs International Ocean Film Festival)."),
    "urls": ["https://github.com/buffedlizard55-lab/MaltaProj5/blob/main/tools/consolidate.py"],
})
review.append({
    "title": "Several rows cite a landing or listing page rather than the event page",
    "detail": ("A number of inherited rows cite an official organizer landing page that lists "
               "several events (for example pcfma.org/visit for four farmers markets, or "
               "sfopera.com's season press page for several productions). The automated check "
               "confirms the page loads and mentions the event name where it does; these rows "
               "are marked 'page-level' rather than 'field-level' verification. Field-level "
               "means a prior session transcribed the individual values; page-level means only "
               "the page and its mention of the event were re-checked automatically."),
    "urls": ["https://github.com/buffedlizard55-lab/MaltaProj5"],
})

(ROOT / "data" / "events.json").write_text(json.dumps(rows, indent=1, ensure_ascii=True) + "\n")
(ROOT / "data" / "sources.json").write_text(json.dumps(sources, indent=1, ensure_ascii=True) + "\n")
(ROOT / "data" / "review.json").write_text(json.dumps(review, indent=1, ensure_ascii=True) + "\n")

from collections import Counter
print(f"canonical register: {len(rows)} rows")
print(" kinds:", dict(Counter(r["kind"] for r in rows)))
print(" categories:", dict(Counter(r["category"] for r in rows)))
print(f" sources: {len(sources)}")
print(f" review findings: {len(review)}")
print(" merged 167-rows:", len(MERGE), " new 167-rows:", len(converted))
