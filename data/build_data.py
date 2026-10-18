#!/usr/bin/env python3
"""Build data/events.json — the verified San Francisco events dataset.

Every row carries an `source_url` pointing at the ORGANIZER / CITY / VENUE
official page that was consulted on the `verified_on` date. Rows whose next
edition date could not be confirmed on an official source carry an empty
`next_date` and `date_status: "unverified"`.
"""
import json, os, datetime

VERIFIED_ON = "2026-10-18"

E = []

# status="flagged" is reserved for genuine irregularities (conflicting official
# sources, stale official pages, discontinued events). Rows whose next edition is
# simply not published yet stay status="verified" with date_status="unverified".


def ev(**kw):
    row = {
        "id": kw["id"],
        "name": kw["name"],
        "category": kw["category"],
        "recurrence": kw["recurrence"],          # weekly | monthly | annual | special
        "cadence": kw["cadence"],
        "next_date": kw.get("next_date", ""),     # "" = not confirmed on an official source
        "date_status": kw.get("date_status", "confirmed"),
        "schedule": kw.get("schedule", ""),
        "time": kw.get("time", ""),
        "venue": kw.get("venue", ""),
        "neighborhood": kw.get("neighborhood", ""),
        "organizer": kw.get("organizer", ""),
        "cost": kw.get("cost", ""),
        "source_name": kw["source_name"],
        "source_url": kw["source_url"],
        "verified_on": VERIFIED_ON,
        "status": kw.get("status", "verified"),
        "notes": kw.get("notes", ""),
    }
    E.append(row)


# ---------------------------------------------------------------------------
# RECURRING — WEEKLY
# ---------------------------------------------------------------------------
ev(id="ferry-plaza-farmers-market",
   name="Ferry Plaza Farmers Market",
   category="Food & Markets", recurrence="weekly",
   cadence="Weekly, year-round — Saturday plus Tuesday and Thursday",
   date_status="continuous",
   schedule="Sat 8am-2pm; Tue & Thu 10am-2pm",
   time="Sat 8:00-14:00; Tue & Thu 10:00-14:00",
   venue="San Francisco Ferry Building",
   neighborhood="Embarcadero",
   organizer="Foodwise",
   cost="Free admission",
   source_name="Foodwise — Ferry Plaza Farmers Market",
   source_url="https://foodwise.org/markets/ferry-plaza-farmers-market/",
   notes="Official operator page lists the three market days and year-round operation.")

ev(id="alemany-farmers-market",
   name="Alemany Farmers Market",
   category="Food & Markets", recurrence="weekly",
   cadence="Weekly, year-round — every Saturday",
   date_status="continuous",
   schedule="Saturday 7am-2pm",
   time="Sat 7:00-14:00",
   venue="100 Alemany Boulevard",
   neighborhood="Bernal Heights",
   organizer="Foodwise (on behalf of the City & County of San Francisco)",
   cost="Free admission",
   source_name="SF.gov — Alemany Farmers Market",
   source_url="https://www.sf.gov/location--alemany-farmers-market",
   status="flagged",
   notes=("City page confirms Saturday 7am-2pm and that Foodwise has operated the market since "
          "February 2026. FLAG: the City's own market rules PDF states 7 AM-3 PM, so published "
          "closing time is inconsistent across sf.gov documents."))

ev(id="heart-of-the-city-farmers-market",
   name="Heart of the City Farmers' Market",
   category="Food & Markets", recurrence="weekly",
   cadence="Weekly, year-round — Wednesday and Sunday",
   date_status="continuous",
   schedule="Sunday and Wednesday",
   time="",
   venue="Fulton Plaza (between the Main Library and the Asian Art Museum), Civic Center",
   neighborhood="Civic Center",
   organizer="Heart of the City Farmers' Market (farmer-operated 501(c)(4))",
   cost="Free admission",
   source_name="Heart of the City Farmers Market — About",
   source_url="https://hotcfarmersmarket.org/about",
   status="flagged",
   notes=("Official About page confirms Wednesdays and Sundays at Fulton Plaza after a 2024 "
          "relocation from United Nations Plaza. FLAG: the operator's own pages give two "
          "different hour sets (7am-4pm on the About page vs Sunday 7am-5pm / Wednesday "
          "7am-5:30pm elsewhere on the same site), so hours are left blank."))

ev(id="golden-gate-park-band",
   name="Golden Gate Park Band — Symphony in the Park",
   category="Parks & Outdoors", recurrence="weekly",
   cadence="Weekly (Sundays) during the season, late April to early October; also July 4 and Labor Day",
   date_status="continuous",
   schedule="2026 season ran April through September 27, 2026",
   time="Sundays 1:00pm, ~90 minutes",
   venue="Spreckels Temple of Music (Golden Gate Bandshell), Music Concourse",
   neighborhood="Golden Gate Park",
   organizer="San Francisco Recreation and Parks Department / Golden Gate Park Band",
   cost="Free",
   source_name="SF Recreation and Parks — Golden Gate Bandshell Concerts",
   source_url="https://sfrecpark.org/1570/Golden-Gate-Bandshell-Concerts",
   notes="City page states free Sunday concerts since 1882, season late April to early October.")

# ---------------------------------------------------------------------------
# RECURRING — MONTHLY
# ---------------------------------------------------------------------------
ev(id="downtown-first-thursdays",
   name="Downtown First Thursdays",
   category="Civic & Holiday", recurrence="monthly",
   cadence="Monthly — first Thursday of every month",
   next_date="2026-11-05",
   schedule="Next listed edition: Thursday, November 5, 2026",
   time="5:00pm-10:00pm",
   venue="2nd Street between Market and Howard Streets",
   neighborhood="SoMa / Downtown",
   organizer="Civic Joy Fund and Into the Streets",
   cost="Free (RSVP)",
   source_name="Downtown First Thursdays (official)",
   source_url="https://www.dftsf.com/",
   notes="Official site states a free all-ages party the first Thursday of every month, 5-10pm.")

ev(id="castro-night-market",
   name="Castro Night Market",
   category="Food & Markets", recurrence="monthly",
   cadence="Monthly — third Friday, March through September",
   next_date="",
   date_status="unverified",
   schedule="2026 season: March 20, April 17, May 15, June 19, July 17, August 21, September 18",
   time="",
   venue="18th Street at Castro Street",
   neighborhood="Castro",
   organizer="CG Events, Castro Merchants Association, Civic Joy Fund",
   cost="Free",
   source_name="Castro Night Market (official)",
   source_url="https://castronightmarket.com/",
   status="flagged",
   notes=("Official site confirms third-Friday cadence and 18th & Castro. FLAG: the 2026 season "
          "ended September 18, 2026 and no 2027 dates are published; official and press listings "
          "also disagree on closing time (5-9pm vs 5-10pm), so time and next date are left blank."))

ev(id="off-the-grid-fort-mason",
   name="Fort Mason Night Market (Off the Grid)",
   category="Food & Markets", recurrence="monthly",
   cadence="Monthly — one Friday night per month during the season",
   next_date="",
   date_status="unverified",
   schedule="2026 dates published: April 17, May 22, June 19, July 24, August 21, September 18",
   time="5:00pm-10:00pm",
   venue="Fort Mason Center for Arts & Culture, 2 Marina Blvd",
   neighborhood="Fort Mason / Marina",
   organizer="Fort Mason Center for Arts & Culture with Off the Grid, West Coast Craft and Stern Grove Festival",
   cost="Free admission",
   source_name="Off the Grid — Fort Mason Center",
   source_url="https://offthegrid.com/markets/fort-mason-center",
   status="flagged",
   notes=("Official Off the Grid page confirms the monthly Friday-night format and 5-10pm hours and "
          "states the 2026 season has wrapped with next-season dates TBA, so no next date is listed."))

# ---------------------------------------------------------------------------
# RECURRING — ANNUAL: Pride & LGBTQ+
# ---------------------------------------------------------------------------
ev(id="sf-pride-celebration",
   name="San Francisco Pride Celebration",
   category="Pride & LGBTQ+", recurrence="annual",
   cadence="Annual — last weekend of June",
   next_date="2027-06-26",
   schedule="2026: June 27-28 at Civic Center Plaza. Official site banner: June 26-27, 2027, 57th annual.",
   venue="Civic Center Plaza",
   neighborhood="Civic Center",
   organizer="San Francisco Pride Celebration Committee",
   cost="Free",
   source_name="SF Pride — Events",
   source_url="https://sfpride.org/events/")

ev(id="sf-pride-parade",
   name="San Francisco Pride Parade",
   category="Pride & LGBTQ+", recurrence="annual",
   cadence="Annual — June, the Sunday of Pride weekend",
   next_date="2027-06-27",
   schedule="2026 parade: Sunday, June 28 on Market Street (56th annual). 57th annual: June 26-27, 2027.",
   venue="Market Street",
   neighborhood="Downtown / Market Street",
   organizer="San Francisco Pride Celebration Committee",
   cost="Free to watch; bleacher/grandstand seats ticketed",
   source_name="SF Pride — Events",
   source_url="https://sfpride.org/events/",
   notes="2027 single-day parade date is not itemised on the official events page; only the 2027 weekend is published.")

ev(id="trans-march",
   name="San Francisco Trans March",
   category="Pride & LGBTQ+", recurrence="annual",
   cadence="Annual — June (Friday of Pride weekend)",
   next_date="",
   date_status="unverified",
   schedule="2026: Friday, June 26, 2026, gathering at Dolores Park",
   venue="Dolores Park",
   neighborhood="Mission District",
   organizer="Trans March",
   cost="Free",
   source_name="SF Pride — Events (links to transmarch.org)",
   source_url="https://www.transmarch.org/",
   notes="2026 date confirmed via the SF Pride events listing; 2027 date not published on the organizer site.")

ev(id="dyke-march",
   name="San Francisco Dyke March",
   category="Pride & LGBTQ+", recurrence="annual",
   cadence="Annual — June (Saturday of Pride weekend)",
   next_date="",
   date_status="unverified",
   schedule="2026: Saturday, June 27, 2026, gathering at Dolores Park",
   venue="Dolores Park",
   neighborhood="Mission District",
   organizer="SF Dyke March",
   cost="Free",
   source_name="SF Dyke March (listed on sfpride.org/events)",
   source_url="https://www.thedykemarch.org/",
   notes="2026 date confirmed via the SF Pride events listing; 2027 date not published.")

ev(id="castro-street-fair",
   name="Castro Street Fair",
   category="Street Fairs & Parades", recurrence="annual",
   cadence="Annual — first Sunday in October",
   next_date="2027-10-03",
   schedule="52nd annual: Sunday, October 4, 2026. Official site: \"Until we meet again: Sunday, October 3, 2027.\"",
   time="11:00am-6:00pm",
   venue="Castro & Market Street and surrounding blocks",
   neighborhood="Castro",
   organizer="Castro Street Fair (501c3)",
   cost="Suggested donation $10-$20",
   source_name="Castro Street Fair (official)",
   source_url="https://castrostreetfair.org/",
   notes="Founded by Harvey Milk in 1974.")

ev(id="folsom-street-fair",
   name="Folsom Street Fair",
   category="Street Fairs & Parades", recurrence="annual",
   cadence="Annual — last Sunday in September",
   next_date="",
   date_status="unverified",
   schedule="2026 (43rd): Sunday, September 27, 2026",
   time="11:00am-6:00pm",
   venue="Folsom Street between 7th and 13th Streets, plus cross streets and Dore",
   neighborhood="SoMa",
   organizer="Folsom Street",
   cost="Free; gate donations to charity",
   source_name="Folsom Street — FAQ",
   source_url="https://www.folsomstreet.org/faq",
   notes=("Official FAQ confirms the last-Sunday-in-September cadence and the 2026 date. 2027 date "
          "not yet published on the official site, so it is left blank."))

ev(id="up-your-alley",
   name="Up Your Alley Fair (Dore Alley)",
   category="Street Fairs & Parades", recurrence="annual",
   cadence="Annual — last Sunday in July",
   next_date="",
   date_status="unverified",
   schedule="2026: Sunday, July 26, 2026",
   time="11:00am-6:00pm",
   venue="Folsom Street between 8th and 11th, 9th and 10th between Howard and Harrison, and Dore Alley",
   neighborhood="SoMa",
   organizer="Folsom Street",
   cost="Free; gate donations",
   source_name="Folsom Street — FAQ",
   source_url="https://www.folsomstreet.org/faq",
   notes="2027 date not yet published on the official site.")

# ---------------------------------------------------------------------------
# RECURRING — ANNUAL: Street Fairs & Parades
# ---------------------------------------------------------------------------
ev(id="chinese-new-year-parade",
   name="San Francisco Chinese New Year Parade",
   category="Street Fairs & Parades", recurrence="annual",
   cadence="Annual — Saturday closest to Lunar New Year",
   next_date="2027-02-20",
   schedule="Saturday, February 20, 2027, stepping off 5:15pm (Year of the Ram)",
   time="5:15pm start, ~2.5 hours",
   venue="Starts at 2nd and Market Streets, around Union Square, ends at Kearny & Columbus",
   neighborhood="Downtown / Chinatown",
   organizer="San Francisco Chinese Chamber of Commerce",
   cost="Free to watch; bleacher seats ticketed",
   source_name="Chinese New Year Festival & Parade — FAQ",
   source_url="https://chineseparade.com/faq/")

ev(id="chinese-new-year-street-fair",
   name="Chinese New Year Community Street Fair",
   category="Street Fairs & Parades", recurrence="annual",
   cadence="Annual — parade weekend",
   next_date="2027-02-20",
   schedule="Saturday & Sunday, February 20 & 21, 2027",
   venue="Grant Avenue between California and Broadway",
   neighborhood="Chinatown",
   organizer="San Francisco Chinese Chamber of Commerce",
   cost="Free",
   source_name="Chinese New Year Festival & Parade — Community Street Fair",
   source_url="https://chineseparade.com/communityfair/")

ev(id="choy-sun-doe",
   name="Choy Sun Doe",
   category="Cultural & Heritage", recurrence="annual",
   cadence="Annual — before the Chinese New Year Parade",
   next_date="2027-02-06",
   schedule="Saturday, February 6, 2027",
   venue="Chinatown",
   neighborhood="Chinatown",
   organizer="San Francisco Chinese Chamber of Commerce",
   cost="Free",
   source_name="Chinese New Year Festival & Parade — Choy Sun Doe",
   source_url="https://chineseparade.com/choysundoe/")

ev(id="italian-heritage-parade",
   name="San Francisco Italian Heritage Parade",
   category="Street Fairs & Parades", recurrence="annual",
   cadence="Annual — October",
   next_date="2027-10-10",
   schedule="158th annual: Sunday, October 11, 2026, 12:30pm. 2027: High Mass & Parade Sunday, October 10, 2027.",
   time="12:30pm",
   venue="Fisherman's Wharf (Jefferson & Powell) along Columbus Avenue to Washington Square",
   neighborhood="North Beach",
   organizer="San Francisco Italian Heritage Festival & Parade",
   cost="Free",
   source_name="SF Italian Heritage — Events",
   source_url="https://sfitalianheritage.org/events/",
   notes="Described as the oldest Italian-American parade in the United States.")

ev(id="north-beach-festival",
   name="North Beach Festival",
   category="Street Fairs & Parades", recurrence="annual",
   cadence="Annual — Father's Day weekend in June",
   next_date="",
   date_status="unverified",
   schedule="2026: Saturday & Sunday, June 20-21, 2026",
   time="11:00am-7:00pm",
   venue="Grant and Columbus Avenues, between Filbert and Broadway and Stockton and Grant",
   neighborhood="North Beach",
   organizer="North Beach Festival (presented with Sunset Mercantile)",
   cost="Free",
   source_name="The North Beach Festival (official)",
   source_url="https://www.northbeachfestival.org/",
   status="flagged",
   notes=("Official site confirms the Father's Day weekend cadence and the 2026 dates but does not "
          "publish 2027 dates. FLAG: edition numbering is inconsistent in third-party listings "
          "(70th vs 71st for 2026)."))

ev(id="haight-ashbury-street-fair",
   name="Haight Ashbury Street Fair",
   category="Street Fairs & Parades", recurrence="annual",
   cadence="Annual — September (organizer's About page still says second Sunday in June)",
   next_date="",
   date_status="unverified",
   schedule="47th annual: Sunday, September 20, 2026",
   time="11:00am-5:30pm",
   venue="Haight Street between Stanyan and Masonic",
   neighborhood="Upper Haight",
   organizer="Haight-Ashbury Street Fair",
   cost="Free",
   source_name="Haight Ashbury Street Fair (official)",
   source_url="https://www.haightashburystreetfair.org/vending",
   status="flagged",
   notes=("FLAG: the organizer's own About page states the fair is \"held every second Sunday in "
          "June\", but the 2026 fair was held Sunday, September 20, 2026. Published cadence is "
          "stale; no 2027 date is published."))

ev(id="union-street-festival",
   name="Union Street Festival",
   category="Street Fairs & Parades", recurrence="annual",
   cadence="Annual — early June",
   next_date="",
   date_status="unverified",
   schedule="48th annual: Saturday & Sunday, June 6-7, 2026",
   time="11:00am-7:00pm",
   venue="Union Street between Fillmore and Gough",
   neighborhood="Cow Hollow",
   organizer="Union Street Merchants Association / Sunset Mercantile",
   cost="Free",
   source_name="Union Street Merchants Association — Union Street Festival",
   source_url="https://unionstreetsf.com/festivals",
   notes="2027 dates not published on the official festival page.")

ev(id="carnaval-festival",
   name="Carnaval San Francisco Festival",
   category="Cultural & Heritage", recurrence="annual",
   cadence="Annual — Memorial Day weekend, two days",
   next_date="2027-05-29",
   schedule="Official FAQ: the festival is on May 29 & 30, 2027, 11am-6pm",
   time="11:00am-6:00pm",
   venue="Harrison Street between 17th and 24th Streets (17 blocks)",
   neighborhood="Mission District",
   organizer="Carnaval San Francisco",
   cost="Free",
   source_name="Carnaval San Francisco — FAQ",
   source_url="https://carnavalsanfrancisco.org/faq/")

ev(id="carnaval-grand-parade",
   name="Carnaval San Francisco Grand Parade",
   category="Cultural & Heritage", recurrence="annual",
   cadence="Annual — Sunday of Memorial Day weekend",
   next_date="2027-05-30",
   schedule="Sunday, May 30, 2027",
   venue="Starts at 24th & Bryant, west to Mission Street, north to 15th Street",
   neighborhood="Mission District",
   organizer="Carnaval San Francisco",
   cost="Free; grandstand seating ticketed",
   source_name="Carnaval San Francisco — Grand Parade",
   source_url="https://carnavalsanfrancisco.org/parade/")

ev(id="cherry-blossom-festival",
   name="Northern California Cherry Blossom Festival",
   category="Cultural & Heritage", recurrence="annual",
   cadence="Annual — two weekends in April",
   next_date="2027-04-10",
   schedule="60th anniversary edition: April 10-11 and 17-18, 2027; Grand Parade April 18, 2027",
   venue="Post Street between Laguna and Fillmore; Peace Plaza",
   neighborhood="Japantown",
   organizer="Northern California Cherry Blossom Festival",
   cost="Free",
   source_name="SF Cherry Blossom Festival (official)",
   source_url="https://sfcherryblossom.org/")

ev(id="nihonmachi-street-fair",
   name="Nihonmachi Street Fair",
   category="Cultural & Heritage", recurrence="annual",
   cadence="Annual — first full weekend of August",
   next_date="2027-08-07",
   schedule="52nd: August 1-2, 2026. 53rd: August 7-8, 2027.",
   time="11:00am-6:00pm",
   venue="Post Street between Webster and Laguna; Japantown Peace Plaza",
   neighborhood="Japantown",
   organizer="Nihonmachi Street Fair",
   cost="Free",
   source_name="Nihonmachi Street Fair (official)",
   source_url="https://www.nihonmachistreetfair.org/")

ev(id="pistahan",
   name="Pistahan Parade & Festival",
   category="Cultural & Heritage", recurrence="annual",
   cadence="Annual — August, second weekend",
   next_date="",
   date_status="unverified",
   schedule="33rd annual: Saturday & Sunday, August 8-9, 2026; parade Saturday 11am from Civic Center Plaza",
   time="11:00am-5:00pm",
   venue="Yerba Buena Gardens (festival); Civic Center Plaza to Yerba Buena Gardens along Market Street (parade)",
   neighborhood="SoMa / Yerba Buena",
   organizer="Filipino Community / FAAE Pistahan",
   cost="Free",
   source_name="Pistahan Parade and Festival (official)",
   source_url="https://www.pistahan.net/",
   notes="2027 dates not published on the official site.")

ev(id="autumn-moon-festival",
   name="San Francisco Chinatown Autumn Moon Festival",
   category="Cultural & Heritage", recurrence="annual",
   cadence="Annual — September (Mid-Autumn Festival)",
   next_date="",
   date_status="unverified",
   schedule="2026: Saturday & Sunday, September 19-20, 2026",
   time="11:00am-5:00pm",
   venue="Grant Avenue between California and Broadway; main stage at Washington & Grant",
   neighborhood="Chinatown",
   organizer="Chinatown Merchants Association (SFCMA)",
   cost="Free",
   source_name="Autumn Moon Festival (official)",
   source_url="https://www.moonfestival.org/",
   status="flagged",
   notes=("FLAG: SFMTA's advisory gives 11am-6pm while the organizer's site gives 11am-5pm, and "
          "third-party listings disagree on the edition number (35th vs 36th). 2027 dates not published."))

ev(id="st-patricks-day-parade",
   name="San Francisco St. Patrick's Day Parade & Festival",
   category="Cultural & Heritage", recurrence="annual",
   cadence="Annual — Saturday before St. Patrick's Day",
   next_date="",
   date_status="unverified",
   schedule="175th annual: Saturday, March 14, 2026, 11:30am",
   time="11:30am parade start",
   venue="2nd & Market Streets to Civic Center Plaza",
   neighborhood="Downtown / Civic Center",
   organizer="United Irish Societies of San Francisco",
   cost="Free",
   source_name="United Irish Societies of San Francisco — St. Patrick's Day Parade",
   source_url="https://uissf.org/st-patricks-day-parade",
   notes="Official parade page still shows the 2026 date; 2027 date not yet published.")

ev(id="greek-food-festival",
   name="San Francisco Greek Food Festival",
   category="Cultural & Heritage", recurrence="annual",
   cadence="Annual — September, three days",
   next_date="",
   date_status="unverified",
   schedule="75th annual: Friday-Sunday, September 18-20, 2026",
   time="Fri & Sat 11am-10pm; Sun 11am-7pm",
   venue="Annunciation Greek Orthodox Cathedral, 245 Valencia Street",
   neighborhood="Mission District",
   organizer="Annunciation Greek Orthodox Cathedral of San Francisco",
   cost="Free admission",
   source_name="Annunciation Greek Orthodox Cathedral — news",
   source_url="https://www.annunciation.org/news_260903_1",
   notes="2027 dates not published on the festival's official site.")

ev(id="fleet-week-air-show",
   name="San Francisco Fleet Week Air Show",
   category="Civic & Holiday", recurrence="annual",
   cadence="Annual — October, three days",
   next_date="2027-10-09",
   schedule="2026 air show: October 9-11 at Marina Green (festival week October 4-12). U.S. Navy Blue Angels 2027 schedule lists San Francisco Fleet Week on October 9-10, 2027.",
   time="12:00pm-4:00pm",
   venue="Marina Green / over San Francisco Bay between the Golden Gate Bridge and Alcatraz",
   neighborhood="Marina",
   organizer="San Francisco Fleet Week Association",
   cost="Waterfront viewing free; reserved seating ticketed",
   source_name="San Francisco Fleet Week — Air Show",
   source_url="https://fleetweeksf.org/air-show/",
   notes="2027 dates corroborated by the U.S. Navy Blue Angels official 2027 schedule (blueangels.navy.mil).")

ev(id="bay-to-breakers",
   name="Bay to Breakers 12K",
   category="Sports & Races", recurrence="annual",
   cadence="Annual — May",
   next_date="2027-05-16",
   schedule="Sunday, May 16, 2027",
   venue="Embarcadero start, finishing at Ocean Beach (Great Highway)",
   neighborhood="Citywide cross-town course",
   organizer="Bay to Breakers",
   cost="Paid entry",
   source_name="Bay to Breakers (official)",
   source_url="https://www.baytobreakers.com/",
   notes="Race held annually since 1912.")

ev(id="sf-marathon",
   name="San Francisco Marathon",
   category="Sports & Races", recurrence="annual",
   cadence="Annual — late July",
   next_date="2027-07-25",
   schedule="50th anniversary: race weekend July 24-25, 2027; full marathon Sunday, July 25, 2027",
   time="Full marathon start 5:15am",
   venue="Start at the Embarcadero at Market; finish at the Embarcadero at Howard",
   neighborhood="Embarcadero / Golden Gate Bridge",
   organizer="The San Francisco Marathon",
   cost="Paid entry",
   source_name="The San Francisco Marathon (official)",
   source_url="https://www.thesfmarathon.com/2027-50th-anniversary/")

ev(id="sunday-streets",
   name="Sunday Streets San Francisco",
   category="Civic & Holiday", recurrence="annual",
   cadence="Annual season of car-free open-street events (about four per season, June-October)",
   next_date="",
   date_status="unverified",
   schedule="2026 season (18th): Tenderloin June 14, Mission July 19, Bayview August 23, Excelsior October 18",
   venue="Rotating neighborhoods",
   neighborhood="Citywide",
   organizer="Sunday Streets SF / Livable City",
   cost="Free",
   source_name="Sunday Streets SF (official)",
   source_url="https://sundaystreetssf.com/",
   notes="2027 season dates and routes not yet published (\"Stay tuned for more information on routes and dates\").")

# ---------------------------------------------------------------------------
# RECURRING — ANNUAL: Music & Festivals
# ---------------------------------------------------------------------------
ev(id="hardly-strictly-bluegrass",
   name="Hardly Strictly Bluegrass",
   category="Music & Festivals", recurrence="annual",
   cadence="Annual — first full weekend of October, three days",
   next_date="",
   date_status="unverified",
   schedule="2026: Friday October 2, Saturday October 3, Sunday October 4",
   time="Fri 1pm-7pm; Sat & Sun 11am-7pm",
   venue="Hellman Hollow, Lindley and Marx Meadows, Golden Gate Park",
   neighborhood="Golden Gate Park",
   organizer="Hardly Strictly Bluegrass",
   cost="Free, no tickets",
   source_name="Hardly Strictly Bluegrass — Info & FAQ",
   source_url="https://hardlystrictlybluegrass.com/info-faq-2026/",
   notes="2027 dates not published on the official site as of the verification date.")

ev(id="outside-lands",
   name="Outside Lands Music and Arts Festival",
   category="Music & Festivals", recurrence="annual",
   cadence="Annual — early August, three days",
   next_date="2027-08-06",
   schedule="2027: Friday August 6 - Sunday August 8 (2026 edition ran August 7-9)",
   venue="Golden Gate Park",
   neighborhood="Golden Gate Park",
   organizer="Another Planet Entertainment / Outside Lands",
   cost="Ticketed",
   source_name="Outside Lands official box office",
   source_url="https://outsidelands.frontgatetickets.com/",
   notes=("Dates taken from the festival's official box office, which states the 2027 dates. "
          "The primary marketing domain sfoutsidelands.com returned HTTP 500 when checked on the "
          "verification date."))

ev(id="noise-pop-festival",
   name="Noise Pop Festival",
   category="Music & Festivals", recurrence="annual",
   cadence="Annual — February, 11 days",
   next_date="2027-02-18",
   schedule="2027: February 18-28, 2027 (33rd edition ran February 19 - March 1, 2026)",
   venue="25+ venues across San Francisco",
   neighborhood="Citywide",
   organizer="Noise Pop Industries",
   cost="Ticketed",
   source_name="Noise Pop Festival (official)",
   source_url="https://www.noisepopfest.com/")

ev(id="stern-grove-festival",
   name="Stern Grove Festival",
   category="Music & Festivals", recurrence="annual",
   cadence="Annual summer series — Sunday afternoons, mid-June to mid-August",
   next_date="",
   date_status="unverified",
   schedule="2026 season complete; the official site announces \"next summer for our 90th season\"",
   time="Sundays, 2:00pm",
   venue="Sigmund Stern Recreation Grove, 19th Avenue and Sloat Boulevard",
   neighborhood="Parkside",
   organizer="Stern Grove Festival Association",
   cost="Free",
   source_name="Stern Grove Festival (official)",
   source_url="https://www.sterngrove.org/",
   notes="Described by the organizer as the nation's longest-running free music festival; 2027 dates not yet published.")

ev(id="lit-crawl",
   name="Lit Crawl San Francisco (Litquake)",
   category="Literature & Books", recurrence="annual",
   cadence="Annual — October, closing night of the Litquake festival",
   next_date="",
   date_status="unverified",
   schedule="2026: Saturday, October 24, 2026, 5-9pm (Litquake festival October 8-24, 2026)",
   time="5:00pm-9:00pm",
   venue="Valencia Street and surrounding venues",
   neighborhood="Mission District",
   organizer="Litquake Foundation",
   cost="Free",
   source_name="Litquake — Lit Crawl SF",
   source_url="https://www.litquake.org/litcrawl",
   notes="2027 festival dates not published on the official site at the verification date.")

ev(id="filbookfest",
   name="Filipino American International Book Festival (FilBookFest)",
   category="Literature & Books", recurrence="annual",
   cadence="Annual — October, during Filipino American History Month",
   next_date="",
   date_status="unverified",
   schedule="8th edition: Saturday & Sunday, October 17-18, 2026",
   venue="San Francisco Main Library, 100 Larkin Street",
   neighborhood="Civic Center",
   organizer="Philippine American Writers and Artists, Inc. with San Francisco Public Library",
   cost="Free",
   source_name="San Francisco Public Library — FilBookFest",
   source_url="https://sfpl.org/events/special-programs/filipino-american-history-celebration",
   status="flagged",
   notes=("FLAG: the City's sf.gov Filipino American History Month page still lists the previous "
          "edition (October 12-13, theme \"KAISÁ'T KASAMA\") while the Library's official page lists "
          "October 17-18, 2026 with theme \"SANGGALAN\" — the City page is stale. 2027 dates not published."))

# ---------------------------------------------------------------------------
# RECURRING — ANNUAL: Performing Arts seasons
# ---------------------------------------------------------------------------
ev(id="sf-symphony-season",
   name="San Francisco Symphony season",
   category="Performing Arts", recurrence="annual",
   cadence="Annual concert season, September to June",
   next_date="",
   schedule="115th season: September 8, 2026 - June 27, 2027; Opening Gala September 24, 2026",
   venue="Davies Symphony Hall, 201 Van Ness Avenue",
   neighborhood="Civic Center",
   organizer="San Francisco Symphony",
   cost="Ticketed",
   source_name="San Francisco Symphony — 2026-27 Season Calendar (PDF)",
   source_url="https://www.sfsymphony.org/getmedia/4732d38f-af5d-4aa2-8934-428420ff11fa/2026-27-Season-Calendar.pdf",
   date_status="continuous",
   notes="Season-level entry: individual concert dates are published in the official season calendar.")

ev(id="sf-opera-season",
   name="San Francisco Opera season",
   category="Performing Arts", recurrence="annual",
   cadence="Annual season, September to July",
   next_date="",
   schedule="104th season opened September 12, 2026 with Simon Boccanegra (Sept 12-27); Manon Oct 15-Nov 1, 2026; Das Rheingold May 29-Jun 22, 2027",
   venue="War Memorial Opera House, 301 Van Ness Avenue",
   neighborhood="Civic Center",
   organizer="San Francisco Opera",
   cost="Ticketed",
   source_name="San Francisco Opera — 2026-27 season press release",
   source_url="https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
   date_status="continuous",
   status="flagged",
   notes=("FLAG: the official Opera Ball page states Opera Ball 2026 was rescheduled to Thursday, "
          "November 12, 2026 because of orchestra labor negotiations, so the season-opening gala did "
          "not take place on the originally announced September 12 date."))

ev(id="opera-in-the-park",
   name="Opera in the Park",
   category="Performing Arts", recurrence="annual",
   cadence="Annual free concert, September (opening weekend of the Opera season)",
   next_date="",
   date_status="unverified",
   schedule="2026: Sunday, September 13, 2026",
   venue="Golden Gate Park",
   neighborhood="Golden Gate Park",
   organizer="San Francisco Opera",
   cost="Free",
   source_name="San Francisco Opera — 2026-27 season press release",
   source_url="https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/",
   notes="2027 date not published at the verification date.")

ev(id="sf-ballet-season",
   name="San Francisco Ballet season",
   category="Performing Arts", recurrence="annual",
   cadence="Annual season, December to spring",
   next_date="2026-12-04",
   schedule="2026-27 season: Nutcracker Dec 4-27, 2026; The Sleeping Beauty Jan 29-Feb 7, 2027; Titans of Choreography Feb 16-21, 2027; Jewels Feb 27-Mar 7, 2027",
   venue="War Memorial Opera House",
   neighborhood="Civic Center",
   organizer="San Francisco Ballet",
   cost="Ticketed",
   source_name="San Francisco Ballet — 2026-2027 Season",
   source_url="https://www.sfballet.org/2026-2027-season/",
   status="flagged",
   notes=("FLAG: sfballet.org shows Nutcracker as Dec 4-27 on the 2026-2027 season page and on the "
          "Nutcracker production page, but the season-renewals page shows \"NUTCRACKER Dec 5-28\" "
          "(the 2025-26 run). Dates taken from the 2026-2027 season page."))

ev(id="sfjazz-season",
   name="SFJAZZ season",
   category="Performing Arts", recurrence="annual",
   cadence="Annual concert season with more than 350 concerts",
   next_date="",
   schedule="2026-27 season announced June 2026; concerts listed through spring 2027",
   venue="SFJAZZ Center, 201 Franklin Street (and Davies Symphony Hall for select concerts)",
   neighborhood="Hayes Valley",
   organizer="SFJAZZ",
   cost="Ticketed",
   source_name="SFJAZZ — 2026-27 Season overview",
   source_url="https://www.sfjazz.org/tickets/productions/26-27/season-overview/",
   date_status="continuous",
   notes="Season-level entry; individual concert dates are on the official season overview.")

# ---------------------------------------------------------------------------
# RECURRING — ANNUAL: Film
# ---------------------------------------------------------------------------
ev(id="sffilm-festival",
   name="San Francisco International Film Festival (SFFILM)",
   category="Film", recurrence="annual",
   cadence="Annual — April to May, 11 days",
   next_date="2027-04-22",
   schedule="70th festival: April 22 - May 2, 2027 (69th ran April 24 - May 4, 2026)",
   venue="Multiple San Francisco venues",
   neighborhood="Citywide",
   organizer="SFFILM",
   cost="Ticketed",
   source_name="SFFILM — FAQs",
   source_url="https://sffilm.org/yr-faq/",
   notes="Longest-running film festival in the Americas.")

ev(id="frameline",
   name="San Francisco International LGBTQ+ Film Festival (Frameline)",
   category="Film", recurrence="annual",
   cadence="Annual — June, 11 days",
   next_date="",
   date_status="unverified",
   schedule="Frameline50 ran June 17-27, 2026",
   venue="Castro Theatre, Roxie Theater, Vogue Theater (plus Bay Area venues)",
   neighborhood="Castro / Mission",
   organizer="Frameline",
   cost="Ticketed",
   source_name="Frameline — Attend",
   source_url="https://www.frameline.org/attend",
   status="flagged",
   notes=("FLAG: 2027 dates are not announced on frameline.org; a third-party submissions platform "
          "lists June 16-26, 2027 but that is not an official organizer announcement, so the date "
          "field is left blank."))

# ---------------------------------------------------------------------------
# RECURRING — ANNUAL: Sports seasons
# ---------------------------------------------------------------------------
ev(id="giants-home-season",
   name="San Francisco Giants home season",
   category="Sports & Races", recurrence="annual",
   cadence="Annual — home games March/April through September/October",
   next_date="2027-03-25",
   schedule="2027 home opener: Thursday, March 25, 2027 vs Colorado Rockies (tentative MLB schedule)",
   venue="Oracle Park",
   neighborhood="SoMa / Mission Bay",
   organizer="San Francisco Giants / Major League Baseball",
   cost="Ticketed",
   source_name="MLB / San Francisco Giants — 2027 schedule press release",
   source_url="https://www.mlb.com/press-release/press-release-giants-announce-tentative-2027-regular-season-schedule",
   status="flagged",
   notes="FLAG: the 2027 schedule is published as tentative by MLB and may shift if labor negotiations extend.")

# ---------------------------------------------------------------------------
# RECURRING — ANNUAL: Civic & Holiday
# ---------------------------------------------------------------------------
ev(id="nye-fireworks",
   name="San Francisco New Year's Eve Fireworks",
   category="Civic & Holiday", recurrence="annual",
   cadence="Annual — December 31, midnight",
   next_date="",
   date_status="unverified",
   schedule="Most recent edition confirmed on an official source: December 31, 2025, midnight, ~15 minutes",
   time="Midnight",
   venue="The Embarcadero, near the Ferry Building",
   neighborhood="Embarcadero",
   organizer="Port of San Francisco",
   cost="Free",
   source_name="Port of San Francisco — New Year's Eve Fireworks Celebration",
   source_url="https://www.sfport.com/meetings/new-years-eve-fireworks-celebration-1",
   notes=("The Port's event page confirms the annual midnight display over the Bay near the Ferry "
          "Building. The 2026-27 edition is not yet posted on an official City/Port page, so the "
          "next date is left blank."))

ev(id="alcatraz-sunrise-gathering",
   name="Indigenous Peoples' Day Sunrise Gathering at Alcatraz",
   category="Civic & Holiday", recurrence="annual",
   cadence="Annual — Indigenous Peoples' Day in October, plus a Thanksgiving ceremony in November",
   next_date="2026-11-26",
   schedule="47th annual gathering: Monday, October 12, 2026, 5-8am. Thanksgiving Indigenous Peoples' Sunrise Ceremony: Thursday, November 26, 2026.",
   time="5:00am-8:00am on the island; ferries from Pier 33 from 4:15am",
   venue="Alcatraz Island (departs Pier 33)",
   neighborhood="Fisherman's Wharf / Alcatraz",
   organizer="International Indian Treaty Council",
   cost="Ceremony free; ferry ticket required",
   source_name="International Indian Treaty Council (official)",
   source_url="https://www.iitc.org/iitcs-2026-indigenous-peoples-day-sunrise-gathering-on-alcatraz-island-will-take-place-on-october-12-2026/")

ev(id="scaregrove",
   name="Scaregrove Halloween Event",
   category="Parks & Outdoors", recurrence="annual",
   cadence="Annual — late October",
   next_date="2026-10-30",
   schedule="Friday, October 30, 2026",
   time="3:00pm-9:00pm",
   venue="Sigmund Stern Grove, 19th Avenue and Sloat Boulevard",
   neighborhood="Parkside",
   organizer="San Francisco Recreation and Parks Department",
   cost="Free",
   source_name="SF Recreation and Parks — Calendar",
   source_url="https://sfrecpark.org/Calendar.aspx")

ev(id="zumba-in-the-parks",
   name="Zumba in the Parks",
   category="Parks & Outdoors", recurrence="annual",
   cadence="Seasonal free fitness series with seasonal party events",
   next_date="2026-10-25",
   schedule="2026 Fall Zumba Party: Sunday, October 25, 2026",
   time="11:00am-1:00pm",
   venue="1199 9th Avenue at Lincoln (Golden Gate Park area)",
   neighborhood="Inner Sunset",
   organizer="San Francisco Recreation and Parks Department",
   cost="Free",
   source_name="SF Recreation and Parks — Zumba in the Parks",
   source_url="https://sfrecpark.org/1183/Zumba-in-the-Parks")

# ---------------------------------------------------------------------------
# SPECIAL / DATED events
# ---------------------------------------------------------------------------
ev(id="foodwise-sunday-supper-2026",
   name="Foodwise Sunday Supper: A Farm to City Feast",
   category="Food & Markets", recurrence="special",
   cadence="Special event",
   next_date="2026-10-18",
   schedule="Sunday, October 18, 2026",
   venue="San Francisco (venue listed on the Foodwise homepage)",
   neighborhood="",
   organizer="Foodwise",
   cost="",
   source_name="Foodwise (official homepage announcement)",
   source_url="https://foodwise.org/",
   status="flagged",
   notes="The official homepage announces the event for October 18, 2026 but the venue detail was not stated in the consulted page; venue left incomplete rather than inferred.")

ev(id="giants-vs-athletics-b2b-runners-night",
   name="Bay to Breakers Runners Night — Giants vs Athletics",
   category="Sports & Races", recurrence="special",
   cadence="Special event tied to race week",
   next_date="2027-05-16",
   schedule="Saturday, May 16, 2027, 7:15pm",
   venue="Oracle Park, 24 Willie Mays Plaza",
   neighborhood="SoMa / Mission Bay",
   organizer="Bay to Breakers",
   cost="Ticketed (runner discount)",
   source_name="Bay to Breakers (official homepage)",
   source_url="https://www.baytobreakers.com/",
   status="flagged",
   notes=("The official homepage lists this under \"What's Upcoming\" with a May 16 date while also "
          "stating the race is May 16, 2027; the countdown text references \"before May 18\". "
          "Treated as a race-week event; flag for organizer confirmation."))

ev(id="b2b-shakeout-run-2027",
   name="Bay to Breakers Shake Out Run — Stonestown",
   category="Sports & Races", recurrence="special",
   cadence="Special event tied to race week",
   next_date="2027-05-15",
   schedule="Saturday, May 15, 2027, 5:00pm",
   venue="Sports Basement, Stonestown Galleria, 3251 20th Ave, Suite 390",
   neighborhood="Stonestown",
   organizer="Bay to Breakers",
   cost="Free (RSVP)",
   source_name="Bay to Breakers (official homepage)",
   source_url="https://www.baytobreakers.com/")

ev(id="opera-ball-2026",
   name="San Francisco Opera Ball 2026",
   category="Performing Arts", recurrence="special",
   cadence="Special event (annual gala, rescheduled in 2026)",
   next_date="2026-11-12",
   schedule="Thursday, November 12, 2026 (rescheduled from September 12, 2026)",
   venue="San Francisco City Hall",
   neighborhood="Civic Center",
   organizer="San Francisco Opera with San Francisco Opera Guild",
   cost="Ticketed gala",
   source_name="San Francisco Opera — Opera Ball",
   source_url="https://www.sfopera.com/operaball",
   notes="Official page states the gala is standalone on the new date, with no performance that evening.")

ev(id="hsb-merch-store-2026",
   name="Hardly Strictly Bluegrass online merch store window",
   category="Music & Festivals", recurrence="special",
   cadence="Special event (post-festival retail window)",
   next_date="2026-10-13",
   schedule="Open October 13-27, 2026",
   venue="Online",
   neighborhood="",
   organizer="Hardly Strictly Bluegrass",
   cost="Paid",
   source_name="Hardly Strictly Bluegrass (official homepage)",
   source_url="https://hardlystrictlybluegrass.com/")

ev(id="mobile-rec-civic-center-2026",
   name="Mobile Rec and B Mo Magic Special Event at Civic Center Plaza",
   category="Parks & Outdoors", recurrence="special",
   cadence="Special event within the recurring Mobile Rec program",
   next_date="2026-10-17",
   schedule="Saturday, October 17, 2026",
   time="10:00am-2:00pm",
   venue="Civic Center Plaza, 335 McAllister Street",
   neighborhood="Civic Center",
   organizer="San Francisco Recreation and Parks Department",
   cost="Free",
   source_name="SF Recreation and Parks — Calendar",
   source_url="https://sfrecpark.org/Calendar.aspx")

ev(id="mobile-rec-sunday-streets-excelsior-2026",
   name="Mobile Rec at Sunday Streets Excelsior",
   category="Parks & Outdoors", recurrence="special",
   cadence="Special event within the recurring Mobile Rec program",
   next_date="2026-10-18",
   schedule="Sunday, October 18, 2026",
   time="11:00am-4:00pm",
   venue="Mission Street between Avalon Avenue and Geneva Avenue",
   neighborhood="Excelsior",
   organizer="San Francisco Recreation and Parks Department",
   cost="Free",
   source_name="SF Recreation and Parks — Calendar",
   source_url="https://sfrecpark.org/Calendar.aspx")

ev(id="mobile-rec-rochambeau-2026",
   name="Mobile Rec at Rochambeau Playground",
   category="Parks & Outdoors", recurrence="special",
   cadence="Special event within the recurring Mobile Rec program",
   next_date="2026-10-24",
   schedule="Saturday, October 24, 2026",
   time="10:00am-4:00pm",
   venue="Rochambeau Playground, 238 25th Avenue",
   neighborhood="Inner Richmond",
   organizer="San Francisco Recreation and Parks Department",
   cost="Free",
   source_name="SF Recreation and Parks — Calendar",
   source_url="https://sfrecpark.org/Calendar.aspx")

ev(id="mobile-rec-scaregrove-2026",
   name="Mobile Rec at Scaregrove",
   category="Parks & Outdoors", recurrence="special",
   cadence="Special event within the recurring Mobile Rec program",
   next_date="2026-10-30",
   schedule="Friday, October 30, 2026",
   time="12:00pm-8:00pm",
   venue="Sigmund Stern Grove",
   neighborhood="Parkside",
   organizer="San Francisco Recreation and Parks Department",
   cost="Free",
   source_name="SF Recreation and Parks — Calendar",
   source_url="https://sfrecpark.org/Calendar.aspx")

ev(id="castro-street-fair-afterparty-2026",
   name="Castro Street Fair Official After Party at the Castro Theatre",
   category="Music & Festivals", recurrence="special",
   cadence="Special event tied to the Castro Street Fair",
   next_date="",
   date_status="unverified",
   schedule="Held Sunday, October 4, 2026 (doors 5:30pm, show 6:00pm)",
   venue="Castro Theatre",
   neighborhood="Castro",
   organizer="Castro Street Fair with Polyglamorous",
   cost="$35.25-$65.25 via Ticketmaster",
   source_name="Castro Street Fair (official news)",
   source_url="https://castrostreetfair.org/",
   notes="One-off 2026 after-party already held; no 2027 edition announced.")


# ---------------------------------------------------------------------------
# DISCONTINUED / EXCLUDED — published on the Flagged page, not in the tables
# ---------------------------------------------------------------------------
DISCONTINUED = [
    {
        "name": "How Weird Street Faire",
        "reason": "Discontinued after its 25th edition in 2024",
        "detail": ("The official site (howweird.org) reads \"2000 — 2024 ... The Faire is done.\" "
                   "Many third-party calendars still list it as an active annual SF event."),
        "source_name": "How Weird Street Faire (official)",
        "source_url": "https://howweird.org/",
    },
    {
        "name": "Ghirardelli Chocolate Festival",
        "reason": "No current edition published by the venue",
        "detail": ("Ghirardelli Square's official events page does not list a Chocolate Festival for "
                   "2026 or 2027; the most recent documented edition is the 23rd in September 2018. "
                   "Excluded from the tables rather than carried as an active annual event."),
        "source_name": "Ghirardelli Square — Upcoming Events",
        "source_url": "https://www.ghirardellisq.com/upcoming-events",
    },
    {
        "name": "Great Dickens Christmas Fair",
        "reason": "Not inside the City and County of San Francisco",
        "detail": ("Frequently listed in \"San Francisco\" round-ups, but the fair is held at the Cow "
                   "Palace in Daly City (San Mateo County). Excluded by the SF-only geography rule."),
        "source_name": "SF city boundary rule (this project)",
        "source_url": "https://www.sf.gov/",
    },
    {
        "name": "Super Bowl LX / FIFA World Cup 2026 matches / 49ers games",
        "reason": "Not inside the City and County of San Francisco",
        "detail": ("Played at Levi's Stadium in Santa Clara. Widely marketed as San Francisco events "
                   "and therefore a common false positive in SF event lists."),
        "source_name": "SF city boundary rule (this project)",
        "source_url": "https://www.sf.gov/",
    },
]

os.makedirs("data", exist_ok=True)
with open("data/events.json", "w") as f:
    json.dump({"generated": VERIFIED_ON, "events": E}, f, indent=2)
with open("data/discontinued.json", "w") as f:
    json.dump({"generated": VERIFIED_ON, "items": DISCONTINUED}, f, indent=2)

print(f"{len(E)} events, {sum(1 for e in E if e['status']=='flagged')} flagged rows, "
      f"{len(DISCONTINUED)} excluded/discontinued items")
