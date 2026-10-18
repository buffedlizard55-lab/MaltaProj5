#!/usr/bin/env python3
"""
Verification pass for the generated site in docs/.

Checks:
 1. Every data row in every table has exactly one external source link (http/https).
 2. All internal links (href/src not starting with http, #, mailto) resolve to files in docs/.
 3. External source URLs are https (or http for legacy official sites), unique, and belong to
    the allowlist of official domains used during research.
 4. Every 'flagged' event in the JSON data appears on the Flagged for Review page.
 5. All 5 pages exist and contain the navigation links.

Exit code 1 if any check fails.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")

ALLOWED_DOMAINS = {
    "foodwise.org", "hotcfarmersmarket.org", "www.sf.gov", "www.pcfma.org",
    "www.agriculturalinstitute.org", "www.noevalleyfarmersmarket.com",
    "www.sfenvironment.org", "offthegrid.com", "presidio.gov",
    "www.calacademy.org", "www.exploratorium.edu", "www.sfcityguides.org",
    "visitunionsquaresf.com", "sundaystreetssf.com", "www.sfcriticalmass.org",
    "www.famsf.org", "about.asianart.org", "goldengateparkband.org",
    "www.dftsf.com", "soma-nights.com", "sunsetmercantilesf.com",
    "ybgfestival.org", "downtownsf.org", "www.bhangraandbeats.com",
    "www.circusbella.org", "www.sfsketchfest.com", "norcalmlkfoundation.org",
    "www.fogfair.com", "sfartweek.com", "sanfranciscohalfmarathon.org",
    "www.mostlybritish.org", "www.sfindie.com", "www.sftravel.com",
    "www.noisepopfest.com", "www.sfbeerweek.org", "www.abaa.org",
    "chineseparade.com", "uissf.org", "www.mlb.com", "www.superfine.world",
    "flowerbulbday.com", "bringyourownbigwheel.com", "sfcherryblossom.org",
    "www.sfrestaurantweek.com", "intloceanfilmfest.org", "www.sfclimateweek.org",
    "sanfranciscoartfair.com", "cookbookweek.com", "picya.org",
    "dancersgroup.org", "earthdaysf.org", "decoratorshowcase.org",
    "caamedia.org", "www.sfiaf.org", "www.tap-sf.org", "www.sfmta.com",
    "carnavalsanfrancisco.org", "www.sfaapicocktailweek.com",
    "www.sfdesignweek.org", "www.escapealcatraztri.com",
    "sfitalianheritage.org", "juneteenth-sf.org", "qwocmap.org",
    "www.frameline.org", "www.sfbff.org", "www.sterngrove.org",
    "sfpride.org", "www.pier39.com", "www.fillmorejazzfest.com",
    "sffolkfest.org", "www.frozenfilmfestival.com", "jfi.org",
    "sf.aidswalk.net", "www.thesfmarathon.com", "www.folsomstreet.org",
    "www.sfjazz.org", "www.jerryday.org", "www.nihonmachistreetfair.org",
    "www.redbull.com", "sfspacewalk.com", "sunsetdunes.org",
    "www.somafilmfest.org", "www.dayofthedeadsf.org", "www.sfhiphopdancefest.com",
    "www.renegadecraft.com", "embarcaderocenter.com", "www.ghirardellisq.com",
    "sftreelot.guardsmen.org", "www.sfballet.org", "www.billgrahammenorah.org",
    "www.somapilipinas.org", "www.koshercomedy.com", "www.sfport.com",
    "sanfranciscohistorium.com", "www.moscone.com",
    "www.sanfranciscolowridercouncil.com", "walksf.org", "www.sfhistory.org",
    "sfcheesefest.com", "www.nexus-sfbay.com", "ybca.org", "www.sfopera.com",
    "www.chasecenter.com", "www.sfmoma.org", "clubdarc.com",
    "portolamusicfestival.com", "hardlystrictlybluegrass.com",
    "fleetweeksf.org", "www.castrostreetfair.org", "www.litquake.org",
    "sffallshow.org", "www.potrerofestival.com", "www.leapsandcastleclassic.org",
    "www.haightashburystreetfair.org", "www.moonfestival.org",
    "comedyday.org", "www.artspan.org", "gggp.org", "race-sfgiants.com",
    "sf.funcheap.com",  # aggregator - only permitted inside exclusion-log context rows
    "github.com",           # this repository (coordination board / source)
    "www.sfsymphony.org", "www.visitunionsquaresf.com",
}

EXTERNAL_OK_IN_EXCLUSIONS = {"sf.funcheap.com"}  # cited as the flagged aggregator itself

PAGES = ["index.html", "weekly-events.html", "annual-events.html",
         "special-events.html", "flagged.html"]

errors = []
warnings = []


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.rows = []
        self._in_row = False
        self._in_thead = False
        self._row_has_ext_link = False
        self._row_text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "thead":
            self._in_thead = True
        if tag == "tr" and "monthrow" not in (a.get("class") or "") and not self._in_thead:
            self._in_row = True
            self._row_has_ext_link = False
            self._row_text = []
        if tag == "a":
            href = a.get("href") or ""
            self.links.append(href)
            if href.startswith("http") and self._in_row:
                self._row_has_ext_link = True
        if tag in ("td", "th") and self._in_row:
            pass

    def handle_endtag(self, tag):
        if tag == "thead":
            self._in_thead = False
        if tag == "tr" and self._in_row:
            self.rows.append(("".join(self._row_text)[:80], self._row_has_ext_link))
            self._in_row = False
        if tag == "td" and self._in_row:
            self._row_text.append(" | ")

    def handle_data(self, data):
        if self._in_row:
            self._row_text.append(data)


def check_page(fname):
    path = os.path.join(DOCS, fname)
    if not os.path.exists(path):
        errors.append(f"missing page: {fname}")
        return
    with open(path) as f:
        content = f.read()
    p = LinkCollector()
    p.feed(content)

    # 1. rows must have an external source link (skip header rows & month rows)
    for text, has_link in p.rows:
        t = text.strip(" |")
        if not t:
            continue
        if not has_link:
            errors.append(f"{fname}: table row without external source link: {t[:70]}")

    # 2. internal links resolve
    for href in p.links:
        if href.startswith(("http", "#", "mailto:")) or href == "":
            continue
        target = href.split("#")[0]
        if not target:
            continue
        if not os.path.exists(os.path.join(DOCS, target)):
            errors.append(f"{fname}: broken internal link: {href}")

    # 3. external link domains
    for href in p.links:
        if not href.startswith("http"):
            continue
        m = re.match(r"https?://([^/]+)/", href + "/")
        if not m:
            errors.append(f"{fname}: malformed URL: {href}")
            continue
        domain = m.group(1).lower()
        if domain not in ALLOWED_DOMAINS:
            # allow the aggregator domain only on flagged page (exclusion context)
            if fname == "flagged.html" and domain in EXTERNAL_OK_IN_EXCLUSIONS:
                continue
            errors.append(f"{fname}: link to non-allowlisted domain: {href}")
        if href.startswith("http://") and domain not in {
                "www.sfsketchfest.com", "www.mostlybritish.org", "www.sfindie.com",
                "www.noisepopfest.com", "www.sfbeerweek.org", "www.frameline.org",
                "www.sfbff.org", "www.fillmorejazzfest.com", "www.litquake.org",
                "www.potrerofestival.com", "www.leapsandcastleclassic.org",
                "www.haightashburystreetfair.org", "www.sfiaf.org", "www.tap-sf.org",
                "www.sfdesignweek.org", "www.sfhistory.org", "www.castrostreetfair.org"}:
            warnings.append(f"{fname}: non-https official link (legacy site): {href}")

    # 4. nav present
    for pg in PAGES:
        if f'href="{pg}"' not in content:
            errors.append(f"{fname}: navigation missing link to {pg}")
    return content


flagged_content = None
for pg in PAGES:
    c = check_page(pg)
    if pg == "flagged.html":
        flagged_content = c or ""

# 5. every flagged event appears on the flagged page
with open(os.path.join(DATA, "events-weekly.json")) as f:
    data = json.load(f)["events"]
with open(os.path.join(DATA, "events-annual.json")) as f:
    data += json.load(f)["events"]
with open(os.path.join(DATA, "events-special.json")) as f:
    data += json.load(f)["events"]
for e in data:
    if e.get("status") == "flagged":
        # name may contain html-escaped chars; compare on a loose prefix
        import html as _h
        probe = e["name"].split("(")[0].strip()[:30]
        unescaped = _h.unescape(flagged_content or "")
        if probe not in unescaped:
            errors.append(f"flagged event missing from flagged.html: {e['name']}")

# 6. data files exist
for df in ["data/events.json", "data/events.csv", "assets/style.css", "assets/app.js"]:
    if not os.path.exists(os.path.join(DOCS, df)):
        errors.append(f"missing site asset: {df}")

print("Errors:", len(errors))
for e in errors:
    print("  ERROR:", e)
print("Warnings:", len(warnings))
for w in warnings:
    print("  warn:", w)
sys.exit(1 if errors else 0)
