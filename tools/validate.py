#!/usr/bin/env python3
"""Validate data/events.json against the register schema.

Fails (exit 1) on any violation. Run:  python3 tools/validate.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ["id", "name", "category", "recurrence", "cadence", "source_name",
            "source_url", "verified_on", "status", "date_status"]
RECURRENCE = {"weekly", "monthly", "annual", "special"}
STATUS = {"verified", "flagged"}
DATE_STATUS = {"confirmed", "unverified", "continuous"}
CATEGORIES = {
    "Street Fairs & Parades", "Music & Festivals", "Pride & LGBTQ+", "Cultural & Heritage",
    "Food & Markets", "Sports & Races", "Film", "Performing Arts", "Parks & Outdoors",
    "Literature & Books", "Civic & Holiday",
}

# Third-party aggregators that may NOT be used as a row's source.
BANNED_SOURCES = [
    "funcheap.com", "sfstation.com", "timeout.com", "eventbrite.com", "yelp.com",
    "dothebay.com", "sftourismtips.com", "wikipedia.org", "wikidata.org", "patch.com",
    "festivalnet.com", "carnifest.com", "eventeny.com", "sfarts.org", "songkick.com",
    "bandsintown.com", "ticketmaster.com", "stubhub.com", "ma.to", "gaycities.com",
    "hoodline.com", "sfchronicle.com", "sfgate.com", "7x7.com", "sfstandard.com",
    "axios.com", "nbcbayarea.com", "abc7news.com", "cbsnews.com", "ktvu.com", "kron4.com",
    "kcra.com", "sfexaminer.com", "eastbaytimes.com", "mercurynews.com", "marinij.com",
    "sfguide.co", "outxout.com", "sfnewstoday.com", "askmesf.com", "dylanstours.com",
    "secretsanfrancisco.com", "ensotelsf.com", "amsires.com", "calpines.com",
    "festivalsinamerica.com", "monolisadesigns.com", "sunsetmercantilesf.com",
    "ronniesawesomelist.com", "allevents.in", "happeningnext.com", "asamnews.com",
    "nativenewsonline.net", "vendorsmap.com", "vendorbound.com", "crawlsf.com",
    "gayborhood.com", "gaytherings.com", "thehomoculture.com", "sfcv.org",
    "backstagebayarea.com", "broadwayworld.com", "kqed.org", "colinscolumn.com",
    "gramilano.com", "danceinforma.us", "sfciviccenter.org", "goldengate.org",
    "bartable.bart.gov", "musicfestivalwizard.com", "usmenuguide.com", "localharvest.org",
    "farmersmarketdates.com", "festmore.com", "loudmemories.com", "festagent.com",
    "filmfreeway.com", "asianfilmfestivals.com", "indieshortsmag.com", "toolsforfilm.com",
    "filmitalia.org", "letterboxd.com", "awardswatch.com", "gaysonoma.com",
    "pcgsanfrancisco.org", "litarc.co", "sched.com", "mercisf.com", "styleweekly.com",
    "fatmarathoner.com", "sapphirerunningzone.com", "runners.quest", "worldsmarathons.com",
    "transpacbound.com", "heavy.com", "giants365.com", "cbssports.com", "uniondemocrat.com",
    "thespacelab.tv", "ultimatefestivals4all.com", "extrachill.com", "tixr.com",
    "frontstagefestivals.com", "portable-infinite.blogspot.com", "theitaliancalifornian3.blogspot.com",
    "oursausalito.com", "navyweek.org", "fusia.net", "marriott.com", "hautelivingsf.com",
    "marinatimes.com", "marincountyvisitor.com", "taniatoubba.com", "kpoptracker.net",
    "kinokorealestate.com", "tasteatlas.com", "mapsofworld.com", "sanfranciscobay.com",
    "chocolate.fandom.com", "10best.usatoday.com", "afar.com", "festival2025.com",
    "sfbayareatimes.com", "serramonteford.com", "bernalconnect.com", "westonaprice.org",
    "togetherinfood.wordpress.com", "amysuto.com", "trendingtravel.org", "sftimes.com",
    "fabulouscalifornia.com", "travelrealizations.com", "luxecruises.com",
    "alibaba.com", "discover.events.com", "sfexaminer.com", "yahoo.com", "instagram.com",
    "facebook.com", "x.com", "youtube.com", "tiktok.com", "google.com", "groups.google.com",
    "idealist.org", "newsbreak.com", "kexp.org", "hccnc.org", "rentbt.com",
    "calendar.ucsf.edu", "sfarts.org", "goldengateparkband.org",
]

errors = []
warnings = []

data = json.load(open(os.path.join(ROOT, "data", "events.json")))
events = data["events"]

seen_ids = set()
for i, e in enumerate(events):
    where = e.get("id") or f"row {i}"
    for k in REQUIRED:
        if not str(e.get(k, "")).strip():
            errors.append(f"{where}: missing required field '{k}'")
    if e.get("recurrence") not in RECURRENCE:
        errors.append(f"{where}: bad recurrence '{e.get('recurrence')}'")
    if e.get("status") not in STATUS:
        errors.append(f"{where}: bad status '{e.get('status')}'")
    if e.get("date_status") not in DATE_STATUS:
        errors.append(f"{where}: bad date_status '{e.get('date_status')}'")
    if e.get("category") not in CATEGORIES:
        errors.append(f"{where}: unknown category '{e.get('category')}'")
    if e["id"] in seen_ids:
        errors.append(f"{where}: duplicate id")
    seen_ids.add(e["id"])

    url = e.get("source_url", "")
    if not url.startswith("https://"):
        errors.append(f"{where}: source_url is not https: {url}")
    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
    for bad in BANNED_SOURCES:
        if host == bad or host.endswith("." + bad):
            errors.append(f"{where}: source_url is a third-party aggregator ({host}) — "
                          "rows must cite an official organizer/City/venue page")
            break

    nd = e.get("next_date", "")
    if nd:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", nd):
            errors.append(f"{where}: next_date is not ISO YYYY-MM-DD: {nd}")
        if e["date_status"] != "confirmed":
            errors.append(f"{where}: has a next_date but date_status is "
                          f"'{e['date_status']}' — a date present must be 'confirmed'")
    elif e["date_status"] == "confirmed":
        errors.append(f"{where}: date_status='confirmed' but next_date is empty")

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", e.get("verified_on", "")):
        errors.append(f"{where}: verified_on is not ISO YYYY-MM-DD")

disc = json.load(open(os.path.join(ROOT, "data", "discontinued.json")))
for d in disc["items"]:
    for k in ("name", "reason", "detail", "source_url"):
        if not str(d.get(k, "")).strip():
            errors.append(f"discontinued '{d.get('name')}': missing '{k}'")

print(f"checked {len(events)} events + {len(disc['items'])} excluded items")
print(f"  confirmed dates : {sum(1 for e in events if e['next_date'])}")
print(f"  unverified dates: {sum(1 for e in events if e['date_status'] == 'unverified')}")
print(f"  continuous series: {sum(1 for e in events if e['date_status'] == 'continuous')}")
print(f"  flagged rows    : {sum(1 for e in events if e['status'] == 'flagged')}")
domains = {re.sub(r"^https?://(www\.)?", "", e["source_url"]).split("/")[0] for e in events}
print(f"  official domains: {len(domains)}")
for w in warnings:
    print(f"  note: {w}")
if errors:
    print("\nFAILED:")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print("\nOK — schema valid, every row cites an official https source")
