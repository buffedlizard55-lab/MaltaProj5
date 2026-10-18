from curate import *
# Explicit event JSON-LD locates the museum; not its CityPASS promotion.
u='https://www.sfmoma.org/exhibition/rm-x-sfmoma/'
mg={'status':'confirmed_sf','quotes':[JQ(u,'"streetAddress": "151 3rd. Street", "addressLocality": "San Francisco"')],'basis':'Official exhibition JSON-LD identifies SFMOMA at 151 3rd Street, San Francisco.'}
D['family']['geography']=mg
for rid,path,n,dt,start,end in [
 ('x-sfmoma-rm-x-sfmoma','exhibition/rm-x-sfmoma/','RM x SFMOMA: Between You and Me','October 3, 2026–February 7, 2027','2026-10-03','2027-02-07'),
 ('x-sfmoma-iturbide','exhibitions/','Graciela Iturbide: Between Two Worlds','July 11–November 29, 2026','2026-07-11','2026-11-29'),
 ('x-sfmoma-raven-chacon','upcoming-exhibitions/','New Work: Raven Chacon','October 24, 2026–November 7, 2027','2026-10-24','2027-11-07'),
 ('x-sfmoma-sarah-sze','exhibitions/','Sarah Sze: Forever is Composed of Nows','Opening November 21, 2026','2026-11-21','')]:
 u='https://www.sfmoma.org/'+path
 add(rid,u,name=n,schedule=dt,venue=F('https://www.sfmoma.org/exhibition/rm-x-sfmoma/','SFMOMA'),scope=mg,dates=[date(u,start,end,dt)],reason='Museum exhibition; hours vary by day and are not substituted for event-specific hours. End date remains blank when only an opening is announced; no fictitious one-day event.')
D['x-sfmoma-sarah-sze']['fields']['price']=F('https://www.sfmoma.org/exhibitions/','Floor 1free to see')
D['x-sfmoma-rm-x-sfmoma']['fields']['price']=F('https://www.sfmoma.org/exhibition/rm-x-sfmoma/','This is a surcharged exhibition: $10 weekdays and $12 weekends/holidays. Free for members.')
D['x-sfmoma-rm-x-sfmoma']['reason']='Surcharge is additional to general admission, not the total ticket price; membership terms apply. No single event time inferred from museum hours.'
u='https://hardlystrictlybluegrass.com/info-faq-2026/'
add('b-hardly-strictly-bluegrass',u,name='Hardly Strictly Bluegrass',schedule='Fri Oct 2, Sat Oct 3, and Sun Oct 4, 2026',venue='Hellman Hollow, Lindley & Marx meadows in Golden Gate Park, San Francisco, CA.',price='FREE EVENT (NO TICKETS NEEDED)',scope='Golden Gate Park, San Francisco, CA.',dates=[date(u,'2026-10-02','2026-10-04','Fri Oct 2, Sat Oct 3, and Sun Oct 4, 2026')],reason='Hotline hours 11am–7pm are not event-opening hours. They are not copied into the time field.')
reject('b-outside-lands','Official ticket shop readable text contains ticket classes and checkout boilerplate, not a dated event or venue. URL/brand and copyright year are not event-date evidence.')
u='https://www.sterngrove.org/'
add('b-stern-grove-festival',u,name='Stern Grove Festival',price='Free Concerts',publish=False,reason='2026 season is explicitly over. Lineup page uses yearless days and lacks a reviewed venue block; 19th/Sloat, Sunday summer schedule and precise 2027 dates not inferred from the brand.')
u=url('www.iitc.org/iitcs-2026')
add('b-alcatraz-sunrise-gathering',u,name='Indigenous Peoples Day Sunrise Gathering',kind='Annual',schedule='Monday, October 12, 2026',time='5:00 AM to 8:00 AM',venue='Alcatraz Island in San Francisco (Yelamu)',scope='Alcatraz Island in San Francisco (Yelamu)',recurrence='47th annual Indigenous Peoples Day Sunrise Gathering',dates=[date(u,'2026-10-12','2026-10-12','Monday, October 12, 2026')],reason='Event on Alcatraz only; the separate noon Yerba Buena event being free does not establish this event’s boat/admission cost.')
u='https://www.sfcityguides.org/'
add('x-sf-city-guides',u,name='San Francisco City Guides',venue='San Francisco',price='Our 1.5 to 2 hour tours are always free, but we welcome donations',scope='FREE historical and architectural walking tours in San Francisco',reason='Programme umbrella with many routes and variable dates/meeting points, not a weekly event at a single guessed venue. Exact cadence not asserted from a generic tour count.')
u='https://www.pier39.com/upcoming-events/'
add('x-fourth-of-july-pier39',u,name='4th of July at PIER 39',schedule='Upcoming 2026 Events at PIER 39',venue='PIER 39',scope='iconic San Francisco Carousel',dates=[date(u,'2026-07-04','2026-07-04','4th of July at PIER 39','Upcoming 2026 Events at PIER 39')],reason='Venue’s dated 2026 calendar context checked. Free Entertainment is not expanded to free attractions, food, parking or every fireworks viewing option.')
add('x-pier39-holiday-lineup',u,name='PIER for the Holiday Season',kind='Annual',schedule='November 23rd until January 10th',venue='PIER 39',scope='iconic San Francisco Carousel',recurrence='The Holidays are a cherished annual tradition at The PIER',reason='Source has a 2026 calendar heading but does not explicitly print the holiday closing year. Cross-year ISO span and upcoming date classification deliberately withheld; nightly shows not treated as confirmed by last year’s schedule.')
D['x-fourth-of-july-pier39']['geography']['basis']='PIER 39 venue identified by its own named San Francisco Carousel; recognized SF waterfront venue.'
D['x-pier39-holiday-lineup']['geography']['basis']=D['x-fourth-of-july-pier39']['geography']['basis']
u='https://www.potrerofestival.com/'
add('x-potrero-hill-festival',u,name='Potrero Hill Festival 2026',schedule='October 17, 2026',time='10 a.m. – 5 p.m.',venue='20th Street',scope='festival on Potrero Hill',dates=[date(u,'2026-10-17','2026-10-17','October 17, 2026')],reason='Recognized SF neighborhood festival; organizer does not state four-block endpoints or free admission. No unsupported Missouri-to-Wisconsin extent.')
D['x-potrero-hill-festival']['geography']['basis']='Official organizer identifies the Potrero Hill neighborhood and local SF schools; recognized SF venue area.'
u='https://www.redbull.com/us-en/events/red-bull-showrun-san-fran'
add('x-red-bull-showrun',u,name='Red Bull Showrun San Francisco presented by Ford',schedule='February 21, 2026',venue='Marina Blvd, San Francisco',scope='Marina Blvd, San Francisco',dates=[date(u,'2026-02-21','2026-02-21','February 21, 2026')],reason='Only the SF stop, not the other three US stops in the same event series.')
reject('x-sf-space-walk','Current page advertises Terpnami 2026 at a private Bay Area venue, not the inherited SF Space Walk multi-day SF itinerary. No city-only venue/date established; redirected/reused content cannot verify the older candidate.')
u='https://sunsetdunes.org/events/ploverfest'
add('x-ploverfest',u,name='PloverFest! (Rescheduled)',schedule='Sunday, April 26, 2026',time='12-4pm',venue='Sunset Dunes from Sloat to Judah',scope='Sunset Dunes from Sloat to Judah',dates=[date(u,'2026-04-26','2026-04-26','Sunday, April 26, 2026')],reason='Rescheduled date used verbatim; SF coastal-park segment identified geographically. No fixed admission stated.')
D['x-ploverfest']['geography']['basis']='Official park event gives Sunset Dunes from Sloat to Judah, a recognized San Francisco park segment.'
reject('x-fourth-of-july-golden-gate-bridge-fireworks','Official source response has no readable event text (202 challenge response). Golden Gate Bridge spans the city boundary; no SF-only viewing venue or 2026 fireworks details are asserted.')
u='https://sanfranciscohistorium.com/'
add('x-sf-historium-spotlight',u,name='The San Francisco Historium Spotlight',schedule='August 2027',publish=False,reason='Organizer announces return month only, says multiple weekends/time periods. Inherited 2026 weekend and Fort Mason venue are not a verified 2027 venue/date.')
u='https://www.moscone.com/events/pokemon-world-championships-2026'
add('x-pokemon-world-championships',u,name='Pokémon World Championships 2026',schedule='August 28–30, 2026',venue='Moscone North, South, and West',scope='Moscone Center | San Francisco, CA USA',dates=[date(u,'2026-08-28','2026-08-30','August 28–30, 2026')],reason='Moscone venue’s explicit event page supplies the past edition. Time and admission left blank.')
u='https://www.sanfranciscolowridercouncil.com/'
add('x-lowrider-parade',u,name='LOWRIDER PARADE and “KING of the STREETS” Hopping Competition',schedule='Saturday, September 20, 2025',time=['1:00 – 3:00 PM','3:00 – 5:00 PM'],venue=['Mission Street (between Cesar Chavez & 17th Street)','24th & Mission Street'],price='All events are free and open to the public.',scope='in partnership with the City of San Francisco',dates=[date(u,'2025-09-20','2025-09-20','Saturday, September 20, 2025')],reason='Source explicitly describes the past 2025 first-ever event; no 2026 annual recurrence assumed. Time blocks refer respectively to parade and hopping competition.')
u='https://walksf.org/events/peak-2-peak/'
add('x-peak2peak',u,name='Peak2Peak',kind='Annual',schedule='Saturday, September 19',venue='Louis Sutter Playground in McLaren Park and ends at Barebottle Brewing in Bernal Heights',scope='journey entirely through San Francisco’s southeast neighborhoods',recurrence='22nd annual Peak2Peak',dates=[date(u,'2026-09-19','2026-09-19','Saturday, September 19','Thursday, September 10, 2026')],reason='Year checked against the same registration/refund terms, not a weekday calculation. Six-to-seven hours is route duration, not a start time; price not stated.')
u='https://www.sfhistory.org/epicenter'
add('x-epicenter-sf-tour',u,name='Epicenter San Francisco: A Tour of Downtown',schedule='Sat. Sept. 19',time='10AM-3PM',venue='San Francisco’s downtown',scope='San Francisco’s downtown',reason='Year unconfirmed and campaign ended. Exact location is private; no made-up address, price or upcoming label.')
reject('x-sf-cheese-fest','Official page HTTP 200 yields no readable content, not substantive verification. Date, venue, time, admission and annual frequency remain unverified.')
u='https://www.nexus-sfbay.com/'
add('x-nexus-sf-bay-area-black-art-week',u,name='Nexus',publish=False,reason='Organizer explicitly includes San Francisco, Oakland and greater Bay Area. Whole festival excluded from city-only directory; individual SF venue events can be separately admitted.')
u='https://ybca.org/event/the-haunt-a-halloween-hangout-crafted-by-artists/'
add('x-the-haunt-ybca',u,name='The Haunt',schedule='October 29–31, 2026',venue='The Forum, YBCA',price=['Tickets: $25','YBCA Members: $15','Kids 12 and under free.'],scope='701 Mission Street\nSan Francisco, CA 94103',dates=[date(u,'2026-10-29','2026-10-31','October 29–31, 2026')],reason='Multiple timed windows, not a single general event hour. Family-friendly 5pm Friday window applies specifically to that show; no unaccompanied minors.')
u='https://www.sfopera.com/press/press-releases/San-Francisco-Opera-2026-27-season/'
for rid,n,dt,start,end in [
 ('x-sf-opera-mary-queen-of-scots','Mary, Queen of Scots','September 20–October 4, 2026','2026-09-20','2026-10-04'),
 ('x-sf-opera-manon','Manon','October 15–November 1, 2026','2026-10-15','2026-11-01'),
 ('x-sf-opera-figaro','The Marriage of Figaro','October 31–November 29, 2026','2026-10-31','2026-11-29'),
 ('x-sf-opera-strauss-in-concert','Strauss in Concert','November 6, 2026','2026-11-06','2026-11-06')]:
 add(rid,u,name=n,schedule=dt,venue='War Memorial Opera House',scope='SAN FRANCISCO, CA (February 3, 2026)',dates=[date(u,start,end,dt)],reason='Production-specific dated section read, not a generic shared-source name match. No time/price inferred from other performances or the displaced opening gala.')
u='https://www.mlb.com/giants/ballpark/events/golf'
add('x-ballpark-back-9',u,name='The Ballpark Back 9',schedule='November 4 - 8, 2026',venue='Oracle Park',scope=geo('https://www.mlb.com/press-release/press-release-giants-announce-tentative-2027-regular-season-schedule','SAN FRANCISCO, Calif.'),dates=[date(u,'2026-11-04','2026-11-08','November 4 - 8, 2026')],reason='Tee times vary; no minimum price established. Recognized SF ballpark venue, not a regional golf tour.')
for rid,source,n,dt,iso in [
 ('x-chase-center-jonas-brothers','https://www.chasecenter.com/news/jonas-brothers-announcement-20261121/','The Jonas Brothers','Nov. 21, 2026','2026-11-21'),
 ('x-chase-center-journey','https://www.chasecenter.com/news/journey-announcement-20261128/','Journey','Nov. 28, 2026','2026-11-28')]:
 add(rid,source,name=n,schedule=dt,venue='Chase Center',dates=[date(source,iso,iso,dt)],publish=False,reason='Official page title supports artist/venue/date, but body content is missing. SF venue and ticket/time details need independent official venue evidence; not falsely reported as fully verified.')
reject('x-chase-center-teddy-swims','Only Teddy Swims | Chase Center title is readable. Event date is in URL only and cannot substantiate November 10; tour subtitle, time and admission not verified.')
reject('x-club-darc','Official text lists Season 2 tickets/presale but not the inherited waterfront location, exact 2026 dates, weekly cadence or capacity. Generic season-sales copy does not establish a city-only event.')
u='https://us.atgtickets.com/venues/curran-theater/whats-on/'
add('curran-season',u,name='Curran Theatre',venue='Curran Theatre',scope='Located in San Francisco’s historic Theatre District',reason='Current venue programme only. No annual recurrence, blanket 2026/27 date range or fixed ticket price inferred; individual shows have separate dates.')
reject('act-season','2026/27 programme and production dates are visible, but this page does not establish the full SF-only theater venue set. Existing two-venue claim not copied without venue evidence.')
for rid in ['sf-zoo-sunset-fridays','sf-zoo-zoolights']:
 reject(rid,'Current official Zoo calendar response contains only the calendar heading, not this named event. Old seasonal hours/dates/admission cannot establish an active 2026 edition.')
zgeo=geo('https://sfrecpark.org/Calendar.aspx','San Francisco Zoo1 Zoo RoadSan FranciscoCA94132')
for rid,path,n,dt,iso,t,p in [
 ('sf-zoo-boo','boo-at-the-zoo','Boo at the Zoo','October 31, 2026','2026-10-31','10:00 AM – 3:00 PM','activities are free with paid daytime admission or Zoo membership.'),
 ('sf-zoo-resident-free-day','sf-resident-free-day','SF Resident Free Day','October 7, 2026','2026-10-07','10:00 AM – 4:00 PM','Free with proof of SF Residency'),
 ('sf-zoo-member-mornings','member-mornings-2-copy','Member Mornings','October 3, 2026','2026-10-03','9:00 AM – 10:00 AM','Members Only')]:
 u='https://www.sfzoo.org/event/'+path+'/'
 add(rid,u,name=n,schedule=dt,time=t,venue='San Francisco Zoo & Garden',price=p,scope=zgeo,dates=[date(u,iso,iso,dt)],reason='Direct event page overrides conflicting calendar-widget text. This is a specific date; no monthly or weekly recurrence inferred. Membership/residency conditions apply.')
reject('presidio-habitat-stewards','The cited 2026 summer release has no Habitat Stewards volunteer schedule. Saturday cadence, time, meeting point and free admission remain unverified.')
u='https://presidio.gov/about/press/presidio-unveils-vibrant-2026-summer-event-lineup'
for rid,n,dt,start,end,t,v,p,rec in [
 ('presidio-fiesta-en-el-parque','Fiesta en el Parque','Saturday, August 1','2026-08-01','2026-08-01','1 to 4 p.m.','Presidio Tunnel Tops, East Meadow','Free',None),
 ('presidio-world-arts-west','World Arts West Dance Festival','Sunday, September 6','2026-09-06','2026-09-06','1to 4 p.m.','Presidio Tunnel Tops, East Meadow','Free',None),
 ('presidio-brewfest','Parks4All: BrewFest','Saturday, May 30','2026-05-30','2026-05-30','12 to 4 p.m.','Civil War Parade Ground Lawn, Graham Street','$60-$315','fourth annual Parks4All: Brewfest'),
 ('presidio-spring-awakening','Spring Awakening: Art & Cumbia at Outpost Meadow','Saturday, May 16','2026-05-16','2026-05-16','12 to 3 p.m.','Outpost Meadow, 609 Old Mason Street','Free',None),
 ('presidio-soccer-festival','Presidio Soccer Festival','Saturday, June 13','2026-06-13','2026-06-13','1 to 5 p.m.','Main Parade Lawn','Free',None),
 ('presidio-community-arts-market','Community Arts Market','Saturday and Sunday, July 18-19','2026-07-18','2026-07-19','10 a.m. to 4 p.m.','Presidio Tunnel Tops, East Meadow','Free','second annual Community Arts Market'),
 ('presidio-memorial-day','Memorial Day Commemoration','Monday, May 25','2026-05-25','2026-05-25','Band concert at 10:30 a.m., program at 11 a.m.','San Francisco National Cemetery','Free','159th annual Memorial Day Commemoration')]:
 add(rid,u,name=n,kind='Annual' if rec else 'Special',schedule=dt,time=t,venue=v,price=p,scope='The Presidio of San Francisco today announced its 2026 summer event season',recurrence=rec,dates=[date(u,start,end,dt,'San Francisco, CA (May 07, 2026)')],reason='2026 summer-release event block checked. No next-edition date/price inferred.'+(' Corrected August 2 to August 1.' if 'fiesta' in rid else ''))
for rid,n in [('sfpl-summer-stride','Summer Stride'),('night-of-ideas-sf','Night of Ideas')]:
 reject(rid,'Generic SFPL calendar does not substantiate the inherited '+n+' edition schedule, venue set or dates. Library calendar presence/free programmes in general are not contextual verification of this row.')
u='https://www.sfballet.org/productions/nutcracker/'
add('x-sf-ballet-nutcracker',u,name='Nutcracker',schedule=F('https://www.sfballet.org/2026-2027-season/','Dec 4 – 27'),venue='War Memorial Opera House',scope='War Memorial Opera House',reason='Official production page confirms the venue. The season page prints Dec 4–27 but no year in that production block; ISO dates/year deliberately not inferred from the 2026/27 season header. Price/time not confirmed.')
D['x-sf-ballet-nutcracker']['geography']['basis']='Recognized SF War Memorial Opera House; explicitly named on the official production page.'
# Every baseline candidate must have an explicit disposition. No silent defaults.
pending=set(R)-set(D)
assert not pending,pending
# Registry relationship metadata, not a claim that the parent/child dates are equal.
parents={**{rid:'after-dark' for rid in ['death','digest','unplug-nov','glow','rules','solstice','creep']},'excelsior':'b-sunday-streets','b-mobile-rec-sunday-streets-excelsior-2026':'excelsior','b-mobile-rec-scaregrove-2026':'b-scaregrove','x-juneteenth-on-the-waterfront':'x-pop-ups-on-the-plaza','b-opera-in-the-park':'b-sf-opera-season','b-opera-ball-2026':'b-sf-opera-season','x-sf-symphony-opening-gala':'b-sf-symphony-season'}
parents.update({rid:'b-sf-opera-season' for rid in D if rid.startswith('x-sf-opera-')})
parents.update({rid:'b-sf-ballet-season' for rid in ['x-sf-ballet-nutcracker']})
for rid,d in D.items():
 d['parent']=parents.get(rid,'')
 d['entry_type']='series' if rid in set(parents.values())|{'b-zumba-in-the-parks','x-sf-city-guides','x-yerba-buena-gardens-festival','x-union-square-park-programs','curran-season','b-giants-home-season'} else 'event'
 if rid in ['b-sf-symphony-season','b-sf-opera-season','b-sf-ballet-season','b-sfmoma-free-days','b-sunday-streets','x-pop-ups-on-the-plaza']:
  d['entry_type']='series'
# Repair weak geography carried by batch1: no unrelated generic City-directory match.
D['flea']['publication']='review_only';D['flea']['geography']={'status':'unverified','quotes':[],'basis':'Irving 9th–11th extent confirmed; no explicit official SF city identification for this flea event archived.'};D['flea']['reason']='Dates/street extent confirmed; unrelated City farmers-market directory token removed. Held off main directory until contextual city evidence is archived.'
# Parent umbrella may itself be held for review; the independently evidenced child remains valid.
A['schema_version']=2
A['method']='Fixed official-source evidence snapshot plus explicit contextual field decisions. Every unapproved field stays blank. Literal matches and HTTP status are never verification. Editorial category/series relationship metadata is separate from event facts.'
A['review_completed_at']='2026-10-18'
save()
