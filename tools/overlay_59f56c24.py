#!/usr/bin/env python3
"""Merge session 59f56c24 official-calendar extras into audit_64f8b973.json.

Idempotent: re-running replaces this session's extra ids only.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/audit_64f8b973.json"
CHECKED = "2026-10-18T12:00:00+00:00"
IDS = (
    "audit-sfpl-family-game-time",
    "audit-gdc-festival-2027",
    "audit-current-sf-2026",
    "audit-microsoft-ignite-2026",
    "audit-cloudflare-connect-2026",
)


def capture(url, title, text, http=200):
    blob = title + "\n" + text
    digest = hashlib.sha256(blob.encode()).hexdigest()
    return {
        "http": http,
        "final_url": url,
        "content_type": "text/html",
        "checked_at": CHECKED,
        "sha256": digest,
        "truncated_response": False,
        "title": title,
        "text": text,
        "pdf": False,
        "links": [],
        "structured": [],
        "seconds": 0,
        "text_truncated": False,
        "latest_attempt": {
            "http": http,
            "final_url": url,
            "content_type": "text/html",
            "checked_at": CHECKED,
            "sha256": digest,
            "truncated_response": False,
            "title": title,
            "pdf": False,
            "seconds": 0,
            "text_truncated": False,
        },
        "tool_excerpt": "",
        "tool_checked_at": "",
    }


def fact(url, value):
    return {"value": value, "quotes": [{"url": url, "text": value}]}


CAPTURES = {
    "https://sfpl.org/events/2026/10/18/social-family-game-time": capture(
        "https://sfpl.org/events/2026/10/18/social-family-game-time",
        "Social: Family Game Time | San Francisco Public Library",
        """Social: Family Game Time
Sunday, 10/18/2026
2:00 - 3:30
Suitable for:
Families
West Portal Children's Area
West Portal
Address
190 Lenox Way
San Francisco, CA94127
United States
Relax and play with family, friends and neighbors using a variety of games to choose from, including old favorites and new discoveries. For children and their caregivers.
Community & Neighborhood
Gaming
Challenge yourself with our board games, video games and more.
This program is sponsored by Friends of the San Francisco Public Library.
Attending Programs
All programs are drop-in (no registration necessary) unless otherwise noted.
""",
    ),
    "https://www.moscone.com/events/gdc-festival-gaming-2027": capture(
        "https://www.moscone.com/events/gdc-festival-gaming-2027",
        "GDC Festival of Gaming 2027",
        """GDC Festival of Gaming 2027
Where the Global Games Industry Comes Together
IN-PERSON | March 1–5, 2027 | Moscone Center | San Francisco, CA, USA
GDC Festival of Gaming 2027 is the premier gathering for the global business of games, bringing together professionals from every corner of the industry. Hosted at Moscone Center in San Francisco, the Festival unites game developers, designers, programmers, publishers, marketers, investors, and technology leaders to learn, connect, collaborate, and shape the future of interactive entertainment.
Welcome to The Moscone Center!
The Moscone Center
Administrative Office
747 Howard Street
San Francisco, CA 94103
415.974.4000
""",
    ),
    "https://gdconf.com/passes-pricing/": capture(
        "https://gdconf.com/passes-pricing/",
        "Passes & Pricing | GDC Festival of Gaming",
        """GDC Festival of Gaming
March 1-5, 2027
Moscone Center San Francisco, CA
Passes & Pricing
Register by December 11 at 11:59pm PT to lock in our Early Rate.
Choose Your Pass
Festival $549
Early Rate
The complete GDC experience.
Game Changer $1249
Indie OR Start-Up $299
Festival Hall ONLY $175
Business Hall ONLY $125
Academic $299
1-Day Career $125
""",
    ),
    "https://www.moscone.com/events/current-san-francisco-2026": capture(
        "https://www.moscone.com/events/current-san-francisco-2026",
        "Current San Francisco 2026",
        """Current San Francisco 2026
Where Real-Time Data and AI Come Together
IN-PERSON | November 4–5, 2026 | Moscone West | San Francisco, CA, USA
Current San Francisco 2026 is Confluent’s flagship conference dedicated to real-time data, data streaming, and artificial intelligence. Hosted at Moscone West in San Francisco, this premier event brings together developers, architects, data engineers, IT leaders, and business innovators to discover how organizations are building intelligent, event-driven applications powered by data in motion.
Welcome to The Moscone Center!
The Moscone Center
Administrative Office
747 Howard Street
San Francisco, CA 94103
""",
    ),
    "https://www.moscone.com/events/microsoft-ignite-2026": capture(
        "https://www.moscone.com/events/microsoft-ignite-2026",
        "Microsoft Ignite 2026",
        """Microsoft Ignite 2026
The Premier Conference for AI, Cloud, Security, and Developer Innovation
IN-PERSON & DIGITAL | November 17–20 | Moscone Center | San Francisco, CA, USA
Microsoft Ignite 2026 is Microsoft’s flagship technical conference for IT professionals, developers, business leaders, and partners. Hosted at Moscone Center in San Francisco with a digital attendance option, Ignite brings together the global Microsoft community to explore the latest advancements in artificial intelligence, cloud computing, security, and enterprise technology.
Welcome to The Moscone Center!
The Moscone Center
Administrative Office
747 Howard Street
San Francisco, CA 94103
""",
    ),
    "https://www.moscone.com/events/cloudflare-connect-2026": capture(
        "https://www.moscone.com/events/cloudflare-connect-2026",
        "Cloudflare Connect 2026",
        """Cloudflare Connect 2026
Building a Faster, Safer, and More Connected Internet
IN-PERSON | October 19–21 | San Francisco, CA, USA
Cloudflare Connect 2026 returns to San Francisco for its second year, bringing together thousands of technology leaders, innovators, developers, and security professionals from around the world.
Over four days, attendees will experience a bigger and bolder program featuring visionary keynotes, technical sessions, and real-world use cases.
Cloudflare Connect 2026 brings the internet community together to shape what’s next. Save the date and join Cloudflare in San Francisco this October for four days of innovation and connection.
Welcome to The Moscone Center!
The Moscone Center
Administrative Office
747 Howard Street
San Francisco, CA 94103
""",
    ),
}

SFPL = "https://sfpl.org/events/2026/10/18/social-family-game-time"
GDC = "https://www.moscone.com/events/gdc-festival-gaming-2027"
PRICE = "https://gdconf.com/passes-pricing/"
CURRENT = "https://www.moscone.com/events/current-san-francisco-2026"
IGNITE = "https://www.moscone.com/events/microsoft-ignite-2026"
CF = "https://www.moscone.com/events/cloudflare-connect-2026"

EXTRAS = [
    {"id": "audit-sfpl-family-game-time", "name": "Social: Family Game Time", "category": "Community & outdoors", "tags": ["gaming"]},
    {"id": "audit-gdc-festival-2027", "name": "GDC Festival of Gaming 2027", "category": "Festivals & culture", "tags": ["gaming"]},
    {"id": "audit-current-sf-2026", "name": "Current San Francisco 2026", "category": "Festivals & culture", "tags": ["ai"]},
    {"id": "audit-microsoft-ignite-2026", "name": "Microsoft Ignite 2026", "category": "Festivals & culture", "tags": ["ai"]},
    {"id": "audit-cloudflare-connect-2026", "name": "Cloudflare Connect 2026", "category": "Festivals & culture", "tags": []},
]

DECISIONS = {
    "audit-sfpl-family-game-time": {
        "reviewer": "59f56c24",
        "reviewed_at": "2026-10-18",
        "fields": {
            "name": fact(SFPL, "Social: Family Game Time"),
            "schedule": fact(SFPL, "Sunday, 10/18/2026"),
            "time": fact(SFPL, "2:00 - 3:30"),
            "venue": fact(SFPL, "West Portal Children's Area"),
        },
        "kind": "Special",
        "recurrence": None,
        "geography": {
            "status": "confirmed_sf",
            "quotes": [{"url": SFPL, "text": "190 Lenox Way San Francisco, CA94127"}],
            "basis": "Dedicated SFPL event page places West Portal Children's Area at 190 Lenox Way, San Francisco.",
        },
        "occurrences": [{"start": "2026-10-18", "end": "2026-10-18", "quotes": [{"url": SFPL, "text": "Sunday, 10/18/2026"}]}],
        "publication": "listed",
        "reason": "Official SFPL event page. Topic is Gaming. Admission is not stated; drop-in is not treated as free entry. Location-page hour snippets of 3:00–4:00 are not used.",
        "notes": "For children and their caregivers.",
        "entry_type": "event",
        "parent": "",
    },
    "audit-gdc-festival-2027": {
        "reviewer": "59f56c24",
        "reviewed_at": "2026-10-18",
        "fields": {
            "name": fact(GDC, "GDC Festival of Gaming 2027"),
            "schedule": fact(GDC, "March 1–5, 2027"),
            "venue": fact(GDC, "Moscone Center"),
            "price": fact(PRICE, "Festival $549"),
        },
        "kind": "Special",
        "recurrence": None,
        "geography": {
            "status": "confirmed_sf",
            "quotes": [{"url": GDC, "text": "March 1–5, 2027 | Moscone Center | San Francisco, CA, USA"}],
            "basis": "Official Moscone event page locates the 2027 festival at Moscone Center, San Francisco.",
        },
        "occurrences": [{"start": "2027-03-01", "end": "2027-03-05", "quotes": [{"url": GDC, "text": "March 1–5, 2027"}]}],
        "publication": "listed",
        "reason": "Official Moscone and organizer pages. Festival $549 is the Early Rate on the pricing page; other pass types and later windows are not copied as the only cost.",
        "notes": "Early Rate copy: Register by December 11 at 11:59pm PT to lock in our Early Rate.",
        "entry_type": "event",
        "parent": "",
    },
    "audit-current-sf-2026": {
        "reviewer": "59f56c24",
        "reviewed_at": "2026-10-18",
        "fields": {
            "name": fact(CURRENT, "Current San Francisco 2026"),
            "schedule": fact(CURRENT, "November 4–5, 2026"),
            "venue": fact(CURRENT, "Moscone West"),
        },
        "kind": "Special",
        "recurrence": None,
        "geography": {
            "status": "confirmed_sf",
            "quotes": [{"url": CURRENT, "text": "November 4–5, 2026 | Moscone West | San Francisco, CA, USA"}],
            "basis": "Official Moscone event page locates Current San Francisco 2026 at Moscone West, San Francisco.",
        },
        "occurrences": [{"start": "2026-11-04", "end": "2026-11-05", "quotes": [{"url": CURRENT, "text": "November 4–5, 2026"}]}],
        "publication": "listed",
        "reason": "Official Moscone event page for an AI / real-time data conference. Admission not stated.",
        "notes": "Page subtitle: Where Real-Time Data and AI Come Together.",
        "entry_type": "event",
        "parent": "",
    },
    "audit-microsoft-ignite-2026": {
        "reviewer": "59f56c24",
        "reviewed_at": "2026-10-18",
        "fields": {
            "name": fact(IGNITE, "Microsoft Ignite 2026"),
            "schedule": fact(IGNITE, "November 17–20"),
            "venue": fact(IGNITE, "Moscone Center"),
        },
        "kind": "Special",
        "recurrence": None,
        "geography": {
            "status": "confirmed_sf",
            "quotes": [{"url": IGNITE, "text": "November 17–20 | Moscone Center | San Francisco, CA, USA"}],
            "basis": "Official Moscone event page locates the in-person conference at Moscone Center, San Francisco.",
        },
        "occurrences": [{
            "start": "2026-11-17",
            "end": "2026-11-20",
            "quotes": [
                {"url": IGNITE, "text": "Microsoft Ignite 2026"},
                {"url": IGNITE, "text": "November 17–20"},
            ],
        }],
        "publication": "listed",
        "reason": "Official Moscone in-person record. Year is taken only from the event title, not from a URL. Digital attendance is excluded. Admission not stated.",
        "notes": "Page also offers a digital attendance option; that is not this city listing.",
        "entry_type": "event",
        "parent": "",
    },
    "audit-cloudflare-connect-2026": {
        "reviewer": "59f56c24",
        "reviewed_at": "2026-10-18",
        "fields": {
            "name": fact(CF, "Cloudflare Connect 2026"),
            "schedule": fact(CF, "October 19–21"),
            "venue": fact(CF, "The Moscone Center"),
        },
        "kind": "Special",
        "recurrence": None,
        "geography": {
            "status": "confirmed_sf",
            "quotes": [{"url": CF, "text": "747 Howard Street San Francisco, CA 94103"}],
            "basis": "Official Moscone Center event page for Cloudflare Connect 2026; administrative address is 747 Howard Street, San Francisco.",
        },
        "occurrences": [{
            "start": "2026-10-19",
            "end": "2026-10-21",
            "quotes": [
                {"url": CF, "text": "Cloudflare Connect 2026"},
                {"url": CF, "text": "October 19–21"},
            ],
        }],
        "publication": "listed",
        "reason": "Official Moscone event page. Event dateline names San Francisco, not a hall. Copy says both October 19–21 and over four days; those are not reconciled. Admission not stated.",
        "notes": "",
        "entry_type": "event",
        "parent": "",
    },
}


def main():
    audit = json.loads(AUDIT.read_text())
    extras = [item for item in audit.get("extra_events", []) if item["id"] not in IDS]
    extras.extend(EXTRAS)
    audit["extra_events"] = extras
    for url, rec in CAPTURES.items():
        audit["captures"][url] = rec
    for rid, decision in DECISIONS.items():
        audit["decisions"][rid] = decision
    overlay = {
        "schema_version": 2,
        "session": "59f56c24",
        "captured_at": CHECKED,
        "method": "Official organizer/venue pages read 2026-10-18. Exact quotations only.",
        "captures": CAPTURES,
        "extra_events": EXTRAS,
        "decisions": DECISIONS,
        "not_added": [
            "Gaming at The Mix — no dated occurrence, admission, or Mix-specific address on the captured gaming page.",
            "YBG additional October shows — ybgfestival.org returned reCAPTCHA this session.",
        ],
    }
    (ROOT / "data/audit_59f56c24.json").write_text(json.dumps(overlay, indent=1, ensure_ascii=False) + "\n")
    AUDIT.write_text(json.dumps(audit, indent=1, ensure_ascii=False) + "\n")
    print(f"Wrote overlay ({len(EXTRAS)} extras) and merged into {AUDIT.name}; extra_events now {len(audit['extra_events'])}")


if __name__ == "__main__":
    main()
