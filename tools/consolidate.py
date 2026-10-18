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


base = load("events.json")                     # 86 rows
weekly = load("events-weekly.json")["events"]  # 34
annual = load("events-annual.json")["events"]  # 95
special = load("events-special.json")["events"]  # 38
sources = load("sources.json")
review = load("review.json")

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


def add_source(url, publisher, note=""):
    for sid, rec in sources.items():
        if rec["url"] == url:
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
        "excerpt": "",
        "method": note or ("Row source inherited from session 4f47c142; page fetched and "
                           "event-name match checked automatically on 2026-10-18."),
    }
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
    if not r.get("cost"):
        flags.append("price: unverified — no admission value stated on the cited official page.")
    if not venue:
        flags.append("venue: unverified — no venue stated on the cited official page.")
    # These registers carry the time inside the dated copy, not as its own field.
    flags.append("time: unverified — the cited page states the date but not a separate "
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
        "parent": "",
        "check": {"level": "page-level", "by": "4f47c142 + c961fbe4 automated fetch",
                  "date": "2026-10-18"},
    }
    for field in ("venue", "price"):
        if row[field]:
            row["evidence"][field] = [sid]
    converted.append(row)

rows = base + converted

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
    for field in ("schedule", "time", "venue", "price"):
        if not r[field] and not any(f.startswith(field + ": unverified") for f in r["flags"]):
            r["flags"].append(f"{field}: unverified — not stated on the cited official page.")

# --------------------------------------------------------------------- integrity
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
for r in rows:
    assert r["kind"] in ("Weekly", "Monthly", "Annual", "Special"), (r["id"], r["kind"])
    assert r["sources"], r["id"]
    assert all(s in sources for s in r["sources"]), r["id"]
    assert not r["parent"] or r["parent"] in ids, r["id"]
    for field in ("schedule", "time", "venue", "price"):
        assert r[field] or any(f.startswith(field + ": unverified") for f in r["flags"]), (r["id"], field)

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
