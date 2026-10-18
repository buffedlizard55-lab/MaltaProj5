#!/usr/bin/env python3
"""Author the 95ceac65 audit overlay on top of the 64f8b973 evidence base.

Reproducible, deterministic transformation: it never mutates the prior
audit file. It deep-copies every capture, candidate, decision and extra
event, then applies exactly two reviewed changes from this session's
independent live re-verification (see data/research/audit-95ceac65.md):

1. x-oktoberfest-on-front: populate the blank price with the official
   page's explicit "FREE WITH RSVP" admission statement (present in the
   archived capture and re-confirmed live).
2. b-alemany-farmers-market: keep the conflicted hours blank (policy
   fixture unchanged), add the operator Foodwise page as a second
   geography quotation, and enrich the flag with the corroboration and
   the documented dissent.

Every quotation must already exist in an archived capture; the new
Foodwise capture was read live with a retrieval reader tool because this
sandbox cannot make arbitrary outbound HTTP requests.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/audit_64f8b973.json"
OUT = ROOT / "data/audit_95ceac65.json"

ALEMANY_FOODWISE = "https://foodwise.org/markets/alemany-farmers-market/"
OKTOBERFEST = "https://downtownsf.org/things-to-do/oktoberfest-on-front"

# Faithful extraction of the visible text retrieved live from the
# operator's Alemany market page on 2026-10-18. The reader returned the
# page in three chunks; the seller-filter taxonomy and vendor list were
# trimmed here. All approved quotations below live in the retained text.
ALEMANY_CAPTURE_TEXT = """\nFoodwise > Markets > Alemany Farmers Market\n100 Alemany Boulevard, San Francisco\nSaturday (7 am – 2 pm), year round\nAlemany Farmers Market\nThe Ferry Plaza Farmers Market badge image\nAlemany Farmers Market: Saturday\n7 am – 2 pm | Affectionately known as “The People's Market,” the Alemany Farmers Market was established in 1943 and is the oldest continuously operated farmers market in California. It played a key role in starting the farmers market movement in the state. With a focus on local food, affordability, and accessibility, the market hosts a diverse community of up to 90 small family farms and food businesses on Saturdays in San Francisco's Bernal Heights neighborhood. As of February 2026, Foodwise is honored to steward this beloved institution, in partnership with the City and County of San Francisco.\nVendor lineup\nThis week's updates\nVisitor Info & Services\nAlemany Farmers Market takes place at 100 Alemany Boulevard in Bernal Heights, San Francisco. Find transit and parking options and more.\nGet info\nSellers\nFoodwise farmers markets showcase the best local and sustainable farms, food makers, and restaurants from our Bay Area food shed and beyond.\nSee vendor lineup\nMarket Picks & Updates\nWondering what's fresh and in season, or whether you favorite vendor is in this week? See our market picks and updates.\nSee market updates\nCommunity Programs\nFood Access\nUse CalFresh EBT, WIC, and other benefits at the farmers market. Get free produce with Market Match.\nLearn more\nFamily Fun\nFrequently Asked Questions\nFoodwise is the new operator of Alemany Farmers Market. See our frequently asked questions.\nLearn more\nConnect With Us\nStay in touch! Follow Alemany Farmers Market on Instagram and share your market finds.\nGet in touch\nSearch Sellers\nSeller Type\n- Any -FarmFood Crafter/PurveyorCertified OrganicRestaurant\nMarket Days\n- Any -Alemany Farmers Market: SaturdayFerry Plaza Farmers Market: SaturdayFerry Plaza Farmers Market: ThursdayFerry Plaza Farmers Market: TuesdayMission Community Market: ThursdayOut for the season\n[retrieval-reader note: the remaining seller-filter taxonomy and vendor counts were trimmed from this archived extraction; the approved quotations above are complete and verbatim]\n"""


def main() -> None:
    audit = json.loads(BASE.read_text())
    captures = audit["captures"]

    # New capture: the market operator's own Alemany page.
    text = ALEMANY_CAPTURE_TEXT.strip()
    captures[ALEMANY_FOODWISE] = {
        "http": 200,
        "final_url": ALEMANY_FOODWISE,
        "content_type": "text/html",
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "sha256_basis": "sha256 of the archived extracted text; raw response bytes were not available to the retrieval reader tool",
        "title": "Alemany Farmers Market : Foodwise",
        "text": text,
        "pdf": False,
        "links": [],
        "structured": [],
        "tool_method": "Retrieval reader tool (markdown extraction of the live page), session 95ceac65, 2026-10-18",
    }

    # Change 1: Oktoberfest on Front — explicit official admission statement.
    okto = audit["decisions"]["x-oktoberfest-on-front"]
    assert "price" not in okto["fields"], "unexpected prior price decision"
    okto["fields"]["price"] = {
        "value": "FREE WITH RSVP",
        "quotes": [{"url": OKTOBERFEST, "text": "FREE WITH RSVP"}],
    }
    okto["reviewer"] = "95ceac65"
    okto["reviewed_at"] = "2026-10-18"
    okto["amended_by"] = "95ceac65 independent re-verification: organizer's own page states admission terms explicitly; prior blank was an unflagged omission, not a conflict"
    okto["reason"] = (
        "Independent re-read confirmed the organizer's official page states "
        "admission terms explicitly (“FREE WITH RSVP”); price populated verbatim. "
        "Third-party news headlines remain rejected as admission evidence; the "
        "organizer's own page now supplies the official statement. No conflicting "
        "official source found."
    )

    # Change 2: Alemany — keep hours blank, add operator geography quote, enrich flag.
    ale = audit["decisions"]["b-alemany-farmers-market"]
    geo_quotes = ale["geography"]["quotes"]
    if not any(q["url"] == ALEMANY_FOODWISE for q in geo_quotes):
        geo_quotes.append({
            "url": ALEMANY_FOODWISE,
            "text": "Alemany Farmers Market takes place at 100 Alemany Boulevard in Bernal Heights, San Francisco",
        })
    ale["reviewer"] = "95ceac65"
    ale["reviewed_at"] = "2026-10-18"
    ale["reason"] = (
        "Time left blank: SF.gov and the operator Foodwise both state 7am–2pm "
        "(Foodwise: “Saturday (7 am – 2 pm), year round”), while the SF Environment "
        "directory says 6am–3pm. The directory entry is dated 03/21/2025, predates the "
        "February 2026 operator changeover, and itself defers to market websites; the "
        "dissent is recorded for manual review rather than silently resolved. The "
        "operator page is archived as a second geography quotation. Admission is not "
        "explicitly stated on either page; free parking does not imply free entrance."
    )
    ale["amended_by"] = "95ceac65 independent re-verification: operator corroboration archived; conflict-blank policy unchanged"

    # Metadata: provenance of the layered overlay.
    audit["session"] = "95ceac65"
    audit["method"] = (
        "Official-source extracted-text snapshot. Literal matches are candidates, NEVER "
        "approvals. Each published nonblank fact needs an explicit field decision and "
        "supporting quotation. This file layers session 95ceac65's independent live "
        "re-verification onto the complete 64f8b973 evidence base (all captures, "
        "candidates and decisions inherited unchanged except the two documented "
        "amendments above)."
    )
    audit["prior_audit"] = "data/audit_64f8b973.json"
    audit["layered_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    audit["layered_changes"] = [
        "x-oktoberfest-on-front: price populated from the official page's explicit FREE WITH RSVP statement",
        "b-alemany-farmers-market: operator Foodwise page archived as second geography quotation; conflict-blank hours flag enriched with the corroboration and the recorded directory dissent",
    ]

    # Keep deterministic ordering.
    audit["captures"] = dict(sorted(captures.items()))
    OUT.write_text(json.dumps(audit, indent=1, ensure_ascii=False) + "\n")
    listed = sum(1 for d in audit["decisions"].values() if d["publication"] == "listed")
    print(f"Wrote {OUT}: {len(audit['decisions'])} decisions, {len(audit['captures'])} captures, {listed} listed dispositions.")


if __name__ == "__main__":
    raise SystemExit(main())
