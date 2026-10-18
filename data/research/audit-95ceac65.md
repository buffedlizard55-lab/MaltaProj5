# T32 independent semantic re-verification — session `95ceac65`

Research snapshot: 18 October 2026 (fixed). Live official pages were re-read
on 2026-10-18 (UTC) with a retrieval reader tool; every correction below carries
an exact quotation from the cited official page, archived in
`data/audit_95ceac65.json`. Reachability and HTTP status are not verification;
only the explicit field decisions are approvals.

## Method

Risk-prioritized sample of the shipped register (167 directory rows / 79
held rows): the 13 newest official-calendar entries, every row carrying a
flag, flagship recurring events, all four cadence kinds across all four
categories, and the future-dated rows a visitor would plan around. Each row's
registered values were compared word-for-word against the live official page
and its archived capture. No value was changed unless the official page stated
it verbatim; nothing was inferred from URLs, titles, or adjacent events.

## Rows re-read live and confirmed unchanged (selection, ~60 rows)

| Row | Official page re-read | Result |
|---|---|---|
| Ferry Plaza Farmers Market | https://foodwise.org/markets/ferry-plaza-farmers-market/ | Schedule/time/venue quotes match verbatim |
| NightLife | https://www.calacademy.org/nightlife | “NightLife is Thursdays* from 6–10 p.m.”, “Tickets are $26.” match |
| After Dark Thursday Nights + 7 themed editions (Death and Life, Creepatorium, Digest This, Unplug and Play ×2, Glow, Rule Breakers, Solstice) | https://www.exploratorium.edu/visit/calendar/after-dark | All occurrence dates/times match the live listings |
| Free Saturdays / Free Tuesdays (de Young, Legion) | https://www.famsf.org/visit/free-reduced-admission | “Every Saturday…”, “first Tuesday of every month” match |
| SFMOMAween, Eternal Echoes II Kiki Ball | https://www.sfmoma.org/exhibitions/ | Both appear verbatim under “Upcoming Events” with dates/times |
| Mission Community Market + Día de los Muertos/Halloween + Sofía Jiménez demo | https://foodwise.org/ and /markets/mission-community-market/ | Event cards match verbatim on the live homepage |
| Outdoor Rec Day 2026, Sunday Fun Days, Illuminate LIVE, Civic Center Soundtrack | sfrecpark.org calendar/newsflash pages, sf.gov news | All values match |
| Presidio rows (Intertribal Dance Gathering, Deaf Dance Festival, Inside Out, Fiesta en el Parque, Spring Awakening, Soccer Festival, Community Arts Market, World Arts West, BrewFest, Memorial Day) | https://presidio.gov/about/press/presidio-unveils-vibrant-2026-summer-event-lineup | Press-release “Attention Calendar Editors” blocks match |
| ZooLights, Boo at the Zoo, SF Resident Free Day, Member Mornings | https://www.sfzoo.org/zoolights/ and event pages | Dates, hours, admission notes match |
| Comedy Day | https://comedyday.org/ and /faq.html | Venue/price confirmed; no printed 2026 date — schedule correctly blank |
| Chinese New Year Parade, Community Street Fair, Choy Sun Doe | https://chineseparade.com/ and subpages | “Saturday, February 20, 2027”, “5:15 PM”, route and 2027 fair dates match |
| Carnaval SF | https://carnavalsanfrancisco.org/ | “May 29–30, 2027”, Mission District, free — match |
| Folsom Street Fair, Up Your Alley | https://www.folsomstreet.org/ and /faq | 2026 dates, hours, street extents match |
| Hardly Strictly Bluegrass, Noise Pop, Lit Crawl SF | Official pages | Dates, venues, free-admission notes match |
| Opera Ball, Opera in the Park, Mary Queen of Scots, Manon, Marriage of Figaro, Strauss in Concert | https://www.sfopera.com/operaball and 2026-27 season press release | Rescheduled Nov 12 City Hall date and season run-dates match |
| Bouquets to Art, Treasures of the Pharaohs, Monet and Venice, Azzedine Alaïa, free admission programs | https://www.famsf.org/press-room/… and /visit/free-reduced-admission | Dates, venues, hours, ticket starts match |
| RM x SFMOMA, Graciela Iturbide | https://www.sfmoma.org/exhibition/rm-x-sfmoma/ and /exhibitions/ | Run dates and surcharge match |
| Nutcracker | https://www.sfballet.org/productions/nutcracker/ | “DEC 4–27”, War Memorial Opera House match |
| Let's Glow SF, Sandcastle Classic, Peak2Peak, Tulip Day, Muni Heritage Weekend 2025 | Official pages | Values match; past editions not moved forward |
| Fleet Week Air Show, Bay to Breakers, Sunday Streets (+Excelsior finale), Potrero Hill Festival, Outdoor Rec Day | Official pages | Values match; Excelsior confirmed for the snapshot date itself (Oct 18) |
| The Haunt (YBCA), PloverFest, Embarcadero 40th lighting, Guardsmen Tree Lot, Renegade Craft, Superfair, ArtSpan Open Studios, SF Art Fair 2027, SF Half Marathon 2027, SFIAF 2027, Ballpark Back 9, Mostly British, Jerry Day, SF Free Folk Festival, Oktoberfest on Front, QWOCMAP, Earth Day SF, TACF, Valencia LIVE!, Pokémon Worlds, Juneteenth on the Waterfront | Official pages | Values match verbatim |
| Alemany Flea Market | https://www.sf.gov/location--alemany-flea-market | “Sunday7:00 am to 3:00 pm” is a faithful verbatim transcription — sf.gov's own page renders the day and hours without a space; not a register defect |

## Correction applied (1 field value)

* `x-oktoberfest-on-front` — price was blank with no documented conflict.
  The official Downtown SF page states **“FREE WITH RSVP”** (present in the
  archived 2026-10-18 capture and re-confirmed live). Price now populated
  with that exact quotation. No other field changed.

## Conflict kept blank, flag enriched (no value change)

* `b-alemany-farmers-market` — time stays blank. Live re-read found the
  operator Foodwise's own page states “Saturday (7 am – 2 pm), year round”,
  agreeing with SF.gov's “every Saturday, 7am - 2pm”; the dissenting
  SF Environment directory entry (“6:00am to 3:00pm”) is dated 03/21/2025,
  predates the February 2026 operator changeover, and itself instructs
  visitors to “refer to the individual market's website”. The operator page
  is now archived and added as a second geography quotation on the row, and
  the flag records the full corroboration/dissent picture for manual review.
  The deliberate conflict-blank policy (encoded in
  `tests/test_audited_register.py::test_conflicting_values_blank_and_flagged`)
  is unchanged: a live disagreement between official pages is flagged, not
  silently resolved by weighing sources.

## Irregularities and observations flagged for manual review (no data change)

* `sunsetmercantilesf.com` Secondhand Saturdays and Día de los Muertos pages
  still self-conflict on the street extent (header “Ortega to Quintara” vs
  address “Ortega & Pacheco”, reversed between the two pages). The register's
  blanks and review-only dispositions remain correct; the conflicts are live
  today, not stale captures.
* `sfrecpark.org/1183/Zumba-in-the-Parks` and `ybgfestival.org` render their
  key content client-side / behind reCAPTCHA; the live re-read could not
  re-confirm their details. The archived 2026-10-18 captures retain the
  approved quotations; this is a reachability/readability unknown, not a
  contradiction.
* `sundaystreetssf.com` now prints specific 2026 route dates (Tenderloin
  Jun 14, Mission Jul 19, Bayview Aug 23, Excelsior Oct 18). The umbrella
  Sunday Streets row deliberately keeps only “2026”; the Excelsior finale is
  separately listed. Enriching the umbrella with the other three dates is a
  future editorial option, not a defect.
* `sftreelot.guardsmen.org` still displays “2025 Key Dates and Hours”; the
  register correctly invents no 2026 dates. Same for the Lowrider Council
  homepage, which still shows the September 20, 2025 parade.
* Guessed URLs during this audit that 404'd (famsf.org/visit/free-admission/,
  sfopera.com/season/opera-ball, famsf.org/events/bouquets-to-art/,
  presidio.gov/explore/events/fiesta-en-el-parque-3) are **not** register
  citations; every URL the register actually cites was live at re-read time.

## Coverage statement

This was an independent sample re-verification, not a re-read of all 242
candidates or all 242 cited URLs. The full fail-closed projection, quote
provenance and blank-consistency checks run offline in CI
(`scripts/validate.py`, 30 regression fixtures). No candidate was promoted
from review-only to the directory in this session; no held row's disposition
changed.
