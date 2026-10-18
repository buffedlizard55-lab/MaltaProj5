from curate import *
def read(u,title,text):
 C.setdefault(u,{'http':None,'title':title,'text':'','links':[],'structured':[]})
 C[u]['tool_excerpt']=text;C[u]['tool_checked_at']='2026-10-18';C[u]['tool_method']='Selected relevant text independently read with fetch_page on 2026-10-18 after inspecting the merged f1fd3c36 audit; not a full raw runner capture.'
u='https://www.sf.gov/location--alemany-flea-market'
read(u,'Alemany Flea Market | SF.gov','''Alemany Flea Market
Alemany Flea Market100 Alemany Boulevard
San Francisco, CA94110
Sunday7:00 am to 3:00 pm
Free on-site parking
San Francisco's Real Estate Department manages the Alemany Flea Market and 2 others in the City and the Alemany Farmers Market.''')
add('f1-alemany-flea-market',u,name='Alemany Flea Market',kind='Weekly',schedule='Sunday7:00 am to 3:00 pm',time='7:00 am to 3:00 pm',venue='100 Alemany Boulevard',scope='100 Alemany Boulevard\nSan Francisco, CA94110',recurrence='Sunday7:00 am to 3:00 pm',reason='Preserves the upstream-added candidate after independent City-page reading. Admission not stated; free parking is not free entry. No year-round claim inferred.')
u='https://sffilm.org/yr-faq/'
add('f1-sffilm-doc-stories',u,name='Doc Stories',schedule='November 5–8, 2026',dates=[date(u,'2026-11-05','2026-11-08','November 5–8, 2026')],publish=False,reason='Preserves upstream-added dated candidate. Venue/time/price and annual cadence are not supplied by this FAQ, so the entry remains held off the SF-only directory.')
u='https://www.famsf.org/press-room/2026-advance-schedule'
read(u,'2026 Advance Exhibition and Program Schedule','''The Fine Arts Museums of San Francisco are pleased to share information about upcoming 2026 exhibitions and select programs.
Monet and Venice de Young | March 21–July 26, 2026
Treasures of the Pharaohs de Young | August 1, 2026–January 31, 2027
San Francisco hosts the US premiere of the international touring exhibition Treasures of the Pharaohs.
Azzedine Alaïa: Sculpting Fashion Legion of Honor | November 21, 2026 – April 11, 2027''')
for rid,n,dt,start,end,venue,g in [
 ('x-deyoung-treasures-of-the-pharaohs','Treasures of the Pharaohs','August 1, 2026–January 31, 2027','2026-08-01','2027-01-31','de Young',D['de-young-sat']['geography']),
 ('x-deyoung-monet-and-venice','Monet and Venice','March 21–July 26, 2026','2026-03-21','2026-07-26','de Young',D['de-young-sat']['geography']),
 ('x-legion-azzedine-alaia','Azzedine Alaïa: Sculpting Fashion','November 21, 2026 – April 11, 2027','2026-11-21','2027-04-11','Legion of Honor',D['legion-sat']['geography'])]:
 add(rid,u,name=n,schedule=dt,venue=venue,scope=g,dates=[date(u,start,end,dt)],reason='Upstream dated-exhibition source independently re-read. No general museum hours or general-admission price substituted for the special exhibition.')
u='https://www.famsf.org/press-room/bouquets-to-art-2026'
read(u,'Bouquets to Art Ushers in Spring with Artistic Arrangements at the de Young and Legion of Honor','''March 3–8, 2026 \\ de Young and Legion of Honor
Bouquets to Art—the annual floral fundraiser of the Fine Arts Museums of San Francisco
Regular Bouquets to Art viewing hours and admission are Tuesday–Sunday, March 3–8, 9:30 am–5:15 pm, at both museums.
On Thursday, March 5, we will host public-access evening hours at the de Young, 6–9 pm.
For adults, tickets start at $44 and include same-day admission to Bouquets to Art and the de Young and Legion of Honor’s permanent-collection galleries. Tickets are timed for entry.''')
g={'status':'confirmed_sf','quotes':D['de-young-sat']['geography']['quotes']+D['legion-sat']['geography']['quotes'],'basis':'Both named museums are recognized San Francisco venues, documented in their official directions.'}
add('x-bouquets-to-art',u,name='Bouquets to Art',kind='Annual',schedule='March 3–8, 2026',time=['Tuesday–Sunday, March 3–8, 9:30 am–5:15 pm, at both museums.','On Thursday, March 5, we will host public-access evening hours at the de Young, 6–9 pm.'],venue='de Young and Legion of Honor',price='For adults, tickets start at $44',scope=g,recurrence='annual floral fundraiser',dates=[date(u,'2026-03-03','2026-03-08','March 3–8, 2026')],reason='Specific fundraiser ticket policy, not a free-general-admission day. Separate opening-night and member-hours events are not included in the main viewing schedule.')
u='https://www.sfzoo.org/zoolights/'
read(u,'ZooLights - San Francisco Zoo & Gardens','''ZooLights
Our all-new ZooLights winter holiday program, lights up the Zoo from November 6, 2026 through January 3, 2027.
ZooLights will be open Wednesdays through Sunday evenings (closed Mondays & Tuesdays) from 5:30 to 9 p.m.
ZooLights requires a separate evening ticket and includes Dinos Rule! ($30 for adults / $21 for children). Zoo Members receive a $3 discount.
This is a separate ticket from a general admission daytime Zoo ticket.''')
add('sf-zoo-zoolights',u,name='ZooLights',schedule='November 6, 2026 through January 3, 2027',time='5:30 to 9 p.m.',venue=F('https://www.sfzoo.org/event/boo-at-the-zoo/','San Francisco Zoo & Garden'),price='separate evening ticket and includes Dinos Rule! ($30 for adults / $21 for children). Zoo Members receive a $3 discount.',scope=D['sf-zoo-boo']['geography'],dates=[date(u,'2026-11-06','2027-01-03','November 6, 2026 through January 3, 2027')],reason='Independently read the dedicated page. It says Wed–Sun, closed Mon/Tue; upstream mentions daily opening after December 16 from a separate release, which is not assumed here. Date span does not mean open every night. Annual recurrence not established by this new programme.')
u='https://sfpl.org/events/2026/04/11/afternoon-and-night-ideas'
read(u,'Afternoon and Night of Ideas | San Francisco Public Library','''Saturday, 4/11/2026
3:00 - 11:45
Main Library
100 Larkin Street
San Francisco, CA94102
Our remarkable springtime event, the Afternoon and Night of Ideas, returns to the San Francisco Main Library, Fulton Plaza and the Asian Art Museum on April 11.
Kicking off with family programs that start at 3 p.m.
Doors to the Main Library reopen at 7 p.m. for the full Night of Ideas.
This annual event is presented by Villa Albertine San Francisco, Asian Art Museum, Circuit Network, KQED, and San Francisco Public Library
Register for free tickets''')
add('night-of-ideas-sf',u,name='Afternoon and Night of Ideas',kind='Annual',schedule='Saturday, 4/11/2026',time='3:00 - 11:45',venue='San Francisco Main Library, Fulton Plaza and the Asian Art Museum',price='Register for free tickets',scope='100 Larkin Street\nSan Francisco, CA94102',recurrence='This annual event',dates=[date(u,'2026-04-11','2026-04-11','Saturday, 4/11/2026')],reason='Dedicated City-library event page replaces generic calendar. Its printed time is transcribed without inventing an AM/PM suffix; prose establishes 3pm start and 7pm evening reopening. An upstream press-release midnight end differs; no forced reconciliation.')
u='https://sfsketchfest.com/'
read(u,'SF Sketchfest - The San Francisco Comedy Festival','''Jan 14 - 31, 2027
SF Sketchfest 2027
Lineup announcing in November!
Relive 2026 highlights''')
add('x-sf-sketchfest',u,name='SF Sketchfest 2027',schedule='Jan 14 - 31, 2027',dates=[date(u,'2027-01-14','2027-01-31','Jan 14 - 31, 2027')],publish=False,reason='2027 banner independently read. Current venue programme not announced; do not carry 2026 venues into it. Upstream cebeabf0 2026 Sched dates remain in candidate history and the companion audit, not silently discarded.')
u='https://www.sfiaf.org/festival'
read(u,'The Festival','''San Francisco International Arts Festival
The San Francisco International Arts Festival (SFIAF) is a multidisciplinary performance and educational program that takes place at numerous venues in San Francisco's Mission District during the first two weeks of May.
The next Festival will take place from April 29 - May 9 2027.
Our website for the 2027 Festival will be live with Early Bird Tickets on sale on February 1, 2027.''')
add('x-sf-international-arts-festival',u,name='San Francisco International Arts Festival',schedule='April 29 - May 9 2027',venue="numerous venues in San Francisco's Mission District",scope="numerous venues in San Francisco's Mission District",dates=[date(u,'2027-04-29','2027-05-09','April 29 - May 9 2027')],reason='Explicit SF Mission programme only. Upstream 2026 ticket prices are not carried into the 2027 edition; prices and individual showtimes remain blank.')
u='https://sanfranciscoartfair.com/'
read(u,'San Francisco Art Fair | April 15–18, 2027','''San Francisco Art Fair returns to Fort Mason’s Festival Pavilion this April 15–18, 2027.
San Francisco Art Fair will present 85 leading galleries from around the world alongside a dynamic series of public programming this April 2027 at Fort Mason Festival Pavilion.''')
u='https://sanfranciscoartfair.com/visit/'
read(u,'Tickets - San Francisco Art Fair | April 15–18, 2027','''Fair Pass $65 + fees
Opening Evening presented by RBC Wealth Management Thursday, April 15, 2027: 6—9pm
Friday, April 16, 2027: 11am—7pm
Saturday, April 17, 2027: 11am—7pm
Sunday, April 18, 2027: 11am—6pm
Single Day Ticket $35 + fees
Tickets Available February 2027
Fort Mason Festival Pavilion
2 Marina Boulevard
San Francisco, CA 94123''')
add('x-sf-art-fair',u,name=F('https://sanfranciscoartfair.com/','San Francisco Art Fair'),schedule=F('https://sanfranciscoartfair.com/','April 15–18, 2027'),time=['Thursday, April 15, 2027: 6—9pm','Friday, April 16, 2027: 11am—7pm','Saturday, April 17, 2027: 11am—7pm','Sunday, April 18, 2027: 11am—6pm'],venue='Fort Mason Festival Pavilion',price=['Fair Pass $65 + fees','Single Day Ticket $35 + fees'],scope='2 Marina Boulevard\nSan Francisco, CA 94123',dates=[date('https://sanfranciscoartfair.com/','2027-04-15','2027-04-18','April 15–18, 2027')],reason='2027 ticket/hours page independently read. Thursday evening requires Fair Pass; single-day tickets are for public days Friday–Sunday. Ticket sales start February 2027, not assumed currently available.')
u='https://sffolkfest.org/'
read(u,'SF Free Folk Festival','''The 50th annual San Francisco Free Folk Festival was in Golden Gate Park on Saturday July 11, 2026, in the same location as our last several festivals.
Admission to everything is free!''')
add('x-sf-free-folk-festival',u,name='San Francisco Free Folk Festival',kind='Annual',schedule='Saturday July 11, 2026',venue='Golden Gate Park',price='Admission to everything is free!',scope='San Francisco Free Folk Festival was in Golden Gate Park',recurrence='50th annual San Francisco Free Folk Festival',dates=[date(u,'2026-07-11','2026-07-11','Saturday July 11, 2026')],reason='Direct organizer retrospective confirms the 2026 park edition. Overall hours are not printed on this homepage; inherited 11–6 not carried without the dated programme.')
u='https://qwocmap.org/festival/'
read(u,'QWOCFF Home - QWOCMAP','''22nd Queer Women of Color Film Festival Trailer
50 films across three Festival experiences. Free, and open to the public.
In-Person Festival
June 12-14, 2026
34 films across seven curated screenings at San Francisco's historic Presidio Theatre.
Location Presidio Theatre, 99 Moraga Avenue, San Francisco
Satellite Screenings
May, July, August, September, and November 2026
Join QWOCFF satellite screenings in cities around the world.''')
add('x-qwocmap-film-festival',u,name='Queer Women of Color Film Festival',schedule='June 12-14, 2026',venue='Presidio Theatre, 99 Moraga Avenue, San Francisco',price='Free, and open to the public.',scope='Presidio Theatre, 99 Moraga Avenue, San Francisco',dates=[date(u,'2026-06-12','2026-06-14','June 12-14, 2026')],reason='Only the explicit SF in-person festival. Worldwide/online/satellite events are excluded; a 2027 date/venue is not inferred from upstream copy.')
u='https://sffallshow.org/about/'
read(u,'The San Francisco Fall Show - About','''The San Francisco Fall Show
2026 DATES
Opening Night Gala on October 14, Show Dates October 15 – 18
2026 SHOW HOURS
Thursday October 15 through Saturday October 17: 10:30am – 7:00pm
Sunday, October 18: 11:00am – 5:00pm
Festival Pavilion, Fort Mason Center for Arts & Culture
2 Marina Blvd
San Francisco CA 94109''')
add('x-sf-fall-antiques-show',u,name='The San Francisco Fall Show',schedule='Show Dates October 15 – 18',time=['Thursday October 15 through Saturday October 17: 10:30am – 7:00pm','Sunday, October 18: 11:00am – 5:00pm'],venue='Festival Pavilion, Fort Mason Center for Arts & Culture',scope='2 Marina Blvd\nSan Francisco CA 94109',dates=[date(u,'2026-10-15','2026-10-18','Show Dates October 15 – 18','2026 DATES')],reason='Show dates/hours, not separate October 14 gala. Event name corrected to organizer title. Numeric admission and an ongoing yearly pattern are not assumed.')
u='https://www.visitvalenciastreet.com/live'
read(u,'Valencia LIVE! — VCMA','''Valencia LIVE! 2026
A FREE, all-ages monthly street party and neighborhood celebration on the second Thursday of every month from 5-10 pm, May through October, 2026
The street party is going down on Valencia St.
May 14 and June 11 - Valencia St. between 16th and 19th
July 9 and Aug 13 - Valencia St. between 17th and 20th
Sept 10 and Oct 8 - Valencia St. between 18th and 21st
Valencia LiVE! is located on Valencia St. in the American Indian Cultural District.
BART
16th and Mission St
24th and Mission St.
MUNI
22 Fillmore, 27 Bryant, 33 Ashbury/18th St, 14 Mission, 14R Mission Rapid, 49 Van Ness/Mission''')
add('x-valencia-live',u,name='Valencia LIVE! 2026',kind='Monthly',schedule='second Thursday of every month from 5-10 pm, May through October, 2026',time='5-10 pm',venue='Valencia St.',price='FREE, all-ages monthly street party',scope='Valencia LiVE! is located on Valencia St. in the American Indian Cultural District.',recurrence='second Thursday of every month',dates=[date(u,x,x,q,'Valencia LIVE! 2026') for x,q in [('2026-05-14','May 14 and June 11'),('2026-06-11','May 14 and June 11'),('2026-07-09','July 9 and Aug 13'),('2026-08-13','July 9 and Aug 13'),('2026-09-10','Sept 10 and Oct 8'),('2026-10-08','Sept 10 and Oct 8')]],reason='SF Mission/Valencia corridor explicitly identified by local BART/MUNI and cultural-district directions. Street extent rotates by date; no 2027 dates generated.',notes='May/June: 16th–19th; July/August: 17th–20th; September/October: 18th–21st. All six listed dates are in 2026.')
D['x-valencia-live']['geography']['basis']='Official organizer gives Valencia corridor street blocks, SF American Indian Cultural District, 16th/24th Mission BART and MUNI directions; recognized SF neighborhood, not a generic city-footer token.'
u='https://www.sf.gov/news-mayor-lurie-announces-second-season-of-free-movies-in-union-square'
read(u,'Mayor Lurie Announces Second Season Of Free Movies In Union Square','''June 10, 2026
SAN FRANCISCO – Mayor Daniel Lurie today announced the second season of “Cinema on the Square,” expanding the series to five free movie screenings in Union Square this summer season.
The series of free outdoor movies will begin June 20 with a special one-year anniversary screening of “KPop Demon Hunters.”
All Saturday night films begin at sunset with pre-show activities including performances, a bar, and prizes taking place two hours before sunset.
On June 27, there will be a special Pride-themed edition of ‘Cinema on the Square’ with a screening of “The Birdcage.” July 25 features the San Francisco-based hit Disney film “The Princess Diaries” and, to help celebrate the Pokémon World Championships held in San Francisco, “Pokémon Detective Pikachu” will be shown on August 29. September 26 will see the filmed-in Union Square classic, “The Conversation.”''')
add('x-cinema-on-the-square',u,name='Cinema on the Square',schedule='five free movie screenings in Union Square this summer season',time='All Saturday night films begin at sunset',venue='Union Square',price='free movie screenings',scope='SAN FRANCISCO – Mayor Daniel Lurie today announced the second season of “Cinema on the Square,” expanding the series to five free movie screenings in Union Square',dates=[date(u,x,x,q,'June 10, 2026') for x,q in [('2026-06-20','June 20'),('2026-06-27','June 27'),('2026-07-25','July 25'),('2026-08-29','August 29'),('2026-09-26','September 26')]],reason='All five dates are present in the independently read June 2026 City release, including September 26. Sunset is not converted to a guessed clock time. Programme umbrella, not five additional candidate rows.')
D['x-cinema-on-the-square']['entry_type']='series'
# Contextual correction after comparison with the upstream audit: the hour below
# belongs to the venue-change notice, not the whole literary pub crawl.
D['b-lit-crawl']['fields'].pop('time',None)
D['b-lit-crawl']['reason']='Date and free Mission-district crawl confirmed. The 6:30–7:30 PM line belongs to the venue-change notice and does not establish overall crawl hours; time is blank. This supersedes the earlier draft misreading.'
read('https://juneteenth-sf.org/', "Something's Wrong Here", 'Something’s wrong here… If you’re the site owner, contact your hosting provider. If you are a visitor, please check back soon.')
D['x-juneteenth-fillmore']['reason']='Independent retrieval of the official site now returns a hosting error (“Something’s wrong here”), not event facts. Earlier manual claims remain in companion history; no fields restored from an error/blocked page.'
for rid,d in D.items():d.setdefault('entry_type','event');d.setdefault('parent','')
A['upstream_reconciliation']={'main_commit':'092a1f40720ca469e3d2e7570d2dc18eab2fbbe4','legacy_audit':'data/audit_f1fd3c36.json','upstream_added_ids':['f1-alemany-flea-market','f1-sffilm-doc-stories'],'note':'Companion tool/ledger preserved unchanged and executed only in temporary candidate-history tree; no inherited field/page label is an approval. Selected new sources independently re-read above.'}
save()
