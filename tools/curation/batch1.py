from curate import *
manual('https://www.exploratorium.edu/visit/calendar/after-dark', '''After Dark Thursday Nights
Every Thursday Night • 6:00–10:00 pm
Stop scrolling and escape to reality at Pier 15!
After Dark: Death and Life / La muerte y la vida
Thu, Oct 22 2026 • 6 - 10pm
After Dark: Creepatorium
Thu, Oct 29 2026 • 6 - 10pm
After Dark: Digest This
Thu, Nov 5 2026 • 6 - 10pm
After Dark: Unplug and Play
Thu, Nov 12 2026 • 6 - 10pm
After Dark: Glow Opening
Thu, Nov 19 2026 • 6 - 10pm
After Dark: Rule Breakers
Thu, Dec 3 2026 • 6 - 10pm
After Dark: Unplug and Play
Thu, Dec 10 2026 • 6 - 10pm
After Dark: Solstice
Thu, Dec 17 2026 • 6 - 10pm''')
manual('https://www.exploratorium.edu/visit', '''Plan Your Visit
You can’t get more San Francisco than this.
After Dark Thursday Nights (18+)
Thursday 10:00 am–5:00 pm 6:00 pm–10:00 pm (Ages 18+)''')
manual('https://www.famsf.org/visit/free-reduced-admission', '''Free + reduced admission
Free Saturdays
Free Tuesdays
Every Saturday we offer free general admission to all residents of the nine Bay Area counties.
This offer applies only to the permanent collection galleries. Full-price admission to special exhibitions still applies.
Please note that Free Saturdays does not take place during Bouquets to Art, our annual weeklong fundraiser.
General admission is free the first Tuesday of every month.
Please note that Free Tuesdays does not take place during Bouquets to Art, our annual weeklong fundraiser.
Benefits include: Free admission for one member, a companion, and a guest to the permanent collections and special exhibitions at the de Young and Legion of Honor''')
manual('https://www.famsf.org/visit/de-young', '''de Young
Free + reduced admission
Nestled in Golden Gate Park
Treasures of the Pharaohs
Through Jan 31, 2027
de Young''')
manual('https://www.famsf.org/visit/legion-of-honor', '''Legion of Honor
Free Saturdays at the Legion of Honor
Sat \\ 9:30 am–5:15 pm
Legion of Honor Free Saturdays''')
manual('https://www.sf.gov/location--alemany-farmers-market', '''Alemany Farmers Market
Buy fresh fruits and vegetables from local farmers every Saturday, 7am - 2pm.
Alemany Farmers Market100 Alemany Boulevard
San Francisco, CA94110
Saturday7:00 am to 2:00 pm
Since February 2026, local nonprofit Foodwise operates Alemany Farmers Market''')
u=url('foodwise.org/markets/ferry-plaza')
add('b-ferry-plaza-farmers-market',u,kind='Weekly',schedule='Saturday (8 am – 2 pm) and Tuesday & Thursday (10 am – 2 pm), year round',time='Saturday (8 am – 2 pm) and Tuesday & Thursday (10 am – 2 pm)',venue='Ferry Building, Embarcadero and Market Streets, San Francisco',scope='Ferry Building, Embarcadero and Market Streets, San Francisco',recurrence='on Saturday, Tuesday, and Thursday, year round',reason='Admission is not stated in the reviewed operator text; the inherited Free admission value is removed.')
u=url('calacademy.org/nightlife')
add('nightlife',u,kind='Weekly',schedule='most Thursdays',time='6–10 p.m.',venue=F(url('calacademy.org/getting-here'),'California Academy of Sciences'),price='Tickets are $26.',scope=geo(url('calacademy.org/getting-here'),'Located in the heart of San Francisco in beautiful Golden Gate Park'),recurrence='NightLife is Thursdays* from 6–10 p.m.',notes='21+ with valid, physical photo ID. There is usually one Thursday per month when no NightLife event is scheduled. Planetarium passes are sold separately.',reason='Exceptions and holiday pause are explicitly stated; no individual next date is generated.')
u=url('exploratorium.edu/visit/calendar/after-dark')
add('after-dark',u,kind='Weekly',schedule='Every Thursday Night',time='6:00–10:00 pm',venue='Pier 15',scope=geo('https://www.exploratorium.edu/visit','You can’t get more San Francisco than this.'),recurrence='Every Thursday Night',reason='Inherited $22.95 admission is not confirmed in the reviewed excerpt and is blanked.',notes='After Dark is ages 18+; the cited museum visit page states this restriction.')
# Museum admission programmes are kept separately by venue, never a combined duplicate.
fam=url('famsf.org/visit/free-reduced-admission')
for rid,v in [('de-young-sat','de Young'),('legion-sat','Legion of Honor')]:
 add(rid,fam,name='Free Saturdays',kind='Weekly',schedule='Every Saturday',venue=F(url('famsf.org/visit/de-young') if v=='de Young' else url('famsf.org/visit/legion-of-honor'),v),price='free general admission to all residents of the nine Bay Area counties',recurrence='Every Saturday',scope={'status':'unverified','quotes':[],'basis':'Admission policy confirmed; the official street-address page needs a readable independent check.'},reason='Permanent collection galleries only; special exhibitions cost extra. Does not take place during Bouquets to Art. City address awaiting explicit source capture.')
add('de-young-tue',fam,name='Free Tuesdays',kind='Monthly',schedule='the first Tuesday of every month',venue=F(url('famsf.org/visit/de-young'),'de Young'),price='General admission is free',recurrence='the first Tuesday of every month',reason='Permanent collection only; excluded during Bouquets to Art. Geographic address evidence pending.')
# Exact market-day facts; do not turn free parking, free activities or free chai into free admission.
u=url('sunsetmercantilesf.com/osfmm')
g=geo(url('sunsetmercantilesf.com/diwali2026'),'37th Avenue between Ortega & Quintara\nSan Francisco, CA, 94116')
add('outer',u,name='Outer Sunset Farmers Market & Mercantile',kind='Weekly',schedule='Sundays: Open Year Round @ 9am-2pm',time='9 am-2 pm',venue='37th Avenue between Ortega & Quintara',scope=g,recurrence='Every Sunday')
add('yoga',u,name='Free yoga',kind='Monthly',schedule='Every first and third Sunday',time='9am',venue='the greenway',price='Free yoga',scope=g,recurrence='Every first and third Sunday',reason='RSVP/donation link is in the operator text; no individual date is generated.')
u=url('sunsetmercantilesf.com/innersunsetflea')
add('flea',u,name='Inner Sunset Flea Market',kind='Monthly',schedule='2nd Sundays: April to November @ 10am-4pm',time='10 am–4 pm',venue='Irving St between 9th & 11th Avenue',recurrence='every second Sunday from April to November',scope=geo(url('sfenvironment.org/farmers-markets-in-sf'),'San Francisco'),reason='Admission is not stated; the page advertises free activities, not necessarily a free entrance.')
u=url('sunsetmercantilesf.com/secondhand')
add('secondhand',u,name='Secondhand Saturdays',kind='Monthly',schedule='April – November, Third Saturdays @ 10am–4pm',time='10 am-4 pm',venue='37th Avenue at Ortega to Quintara',recurrence='THIRD SATURDAY MONTHLY',scope=g,reason='Venue conflict on the same official page: header says Ortega to Quintara; Address says Ortega & Pacheco. Precise venue blanked for review.')
D['secondhand']['fields'].pop('venue');D['secondhand']['publication']='review_only'
u=url('sunsetmercantilesf.com/diwali2026')
add('diwali',u,name='Diwali 2026 at the Outer Sunset Farmers Market',kind='Annual',schedule='November 8th, 2026',time='9am-2pm',venue='37th Avenue between Ortega & Quintara',scope=g,recurrence='fourth annual Diwali Festival',dates=[date(u,'2026-11-08','2026-11-08','November 8th, 2026')])
u=url('sunsetmercantilesf.com/ddlm')
add('muertos',u,name='Día de los Muertos Outer Sunset',kind='Annual',schedule='Sunday, November 1, 2026',time='9am-2pm',recurrence='fifth annual',scope=geo(u,'San Francisco. California'),dates=[date(u,'2026-11-01','2026-11-01','Sunday, November 1, 2026')],reason='Official page conflicts on the street extent (Ortega to Pacheco versus Ortega & Quintara) and says night despite 9am–2pm. Venue left blank; review-only until location extent reconciled.')
u=url('sfpride.org/events/')
add('b-sf-pride-celebration',u,name='Pride Celebration',kind='Annual',schedule='Saturday–Sunday, June 27–28, 2026',venue='Civic Center Plaza',price='completely free and open to all. No ticket required.',scope='San Francisco Pride 2026',recurrence='our annual celebration' if 'our annual celebration' in T(u) else None,dates=[date(u,'2026-06-27','2026-06-28','Saturday–Sunday, June 27–28, 2026')],reason='2027 organizer homepage announces a combined celebration/parade weekend, not a separate exact parade date; no 2027 parade day inferred.')
D['b-sf-pride-celebration']['recurrence']=F(url('https://sfpride.org/') if False else 'https://sfpride.org/','57TH ANNUAL CELEBRATION & PARADE')
# Preserve the explicit combined future weekend as a separate approved occurrence, but do not invent venue for it.
D['b-sf-pride-celebration']['fields']['schedule']=F('https://sfpride.org/','57TH ANNUAL CELEBRATION & PARADE • JUNE 26–27, 2027')
D['b-sf-pride-celebration']['occurrences']=[date('https://sfpride.org/','2027-06-26','2027-06-27','JUNE 26–27, 2027')]
D['b-sf-pride-celebration']['reason']='Future weekend is confirmed on organizer homepage; Civic Center venue and free policy are from the 2026 edition and are not confirmed for 2027. Venue and price blanked to avoid cross-edition carryover.'
D['b-sf-pride-celebration']['fields'].pop('venue');D['b-sf-pride-celebration']['fields'].pop('price');D['b-sf-pride-celebration']['publication']='review_only'
u=url('chineseparade.com/faq')
add('chinese',u,name='San Francisco Chinese New Year Parade',schedule='Saturday, February 20, 2027',time='5:15 PM',venue='2nd and Market Streets, goes around Union Square and ends at Kearny Street & Columbus Ave.',price='a free event for all to attend but tickets must be purchased to sit in the bleacher sections.',scope='San Francisco Chinese New Year Parade',dates=[date(u,'2027-02-20','2027-02-20','Saturday, February 20, 2027')],reason='Dated edition confirmed; annual recurrence language not present in reviewed FAQ, so recurrence is not asserted.')
u=url('carnavalsanfrancisco.org/')
add('carnaval',u,name='Carnaval SF',schedule='May 29–30, 2027',venue='San Francisco’s Mission District',price='FREE 2–day family festival & Grand Parade',scope='San Francisco’s Mission District',dates=[date(u,'2027-05-29','2027-05-30','May 29–30, 2027')],reason='Dated festival confirmed; 2026 FAQ parking times not carried into 2027. Recurrence not inferred from edition history.')
u=url('sundaystreetssf.com/sunday-streets-excelsior')
add('excelsior',u,name='Sunday Streets Excelsior 2026',schedule='Sunday, October 18, 2026',time='11 AM – 4 PM',venue='Mission Street between Geneva Avenue and Theresa Street',scope='Sunday Streets is San Francisco’s open streets program',dates=[date(u,'2026-10-18','2026-10-18','Sunday, October 18, 2026')])
u=url('sfmoma.org/event/free-family-day')
add('family',u,schedule='Sunday, Oct 25, 2026',time='10 a.m.–4 p.m.',venue=F(url('sfmoma.org/visit/'),'SFMOMA'),price='Free Family Day provides free access to two adults when accompanied by a child 18 or younger.',scope=geo(url('sfmoma.org/visit/'),'San Francisco'),dates=[date(u,'2026-10-25','2026-10-25','Sunday, Oct 25, 2026')],notes='RSVP encouraged. RM x SFMOMA requires a timed ticket and $12 adult surcharge; children 18 and younger are free but need a reserved timed ticket.')
u=url('exploratorium.edu/visit/calendar/after-dark')
for rid,name,dt,iso in [('death','After Dark: Death and Life / La muerte y la vida','Thu, Oct 22 2026','2026-10-22'),('digest','After Dark: Digest This','Thu, Nov 5 2026','2026-11-05'),('glow','After Dark: Glow Opening','Thu, Nov 19 2026','2026-11-19'),('rules','After Dark: Rule Breakers','Thu, Dec 3 2026','2026-12-03'),('solstice','After Dark: Solstice','Thu, Dec 17 2026','2026-12-17'),('creep','After Dark: Creepatorium','Thu, Oct 29 2026','2026-10-29')]:
 add(rid,u,name=name,schedule=dt,time='6 - 10pm',venue='Pier 15',scope=geo('https://www.exploratorium.edu/visit','You can’t get more San Francisco than this.'),dates=[date(u,iso,iso,dt)])
add('unplug-nov',u,name='After Dark: Unplug and Play',schedule=['Thu, Nov 12 2026','Thu, Dec 10 2026'],time='6 - 10pm',venue='Pier 15',scope=geo('https://www.exploratorium.edu/visit','You can’t get more San Francisco than this.'),dates=[date(u,'2026-11-12','2026-11-12','Thu, Nov 12 2026'),date(u,'2026-12-10','2026-12-10','Thu, Dec 10 2026')])
u=url('sunsetmercantilesf.com/colevalleynights2026')
add('cole',u,name='Cole Valley Nights',schedule='December 10th – Holiday Nights',time='4pm – 9pm',venue='Cole Street, between Carl and Parnassus',scope='San Francisco, CA',reason='Year not explicit in reviewed date text; no year inferred from URL, assets or weekday.')
u=url('sunsetmercantilesf.com/sunsetholidaymercantile')
add('holiday',u,name='Sunset Holiday Mercantile',kind='Annual',recurrence='11th Annual Sunset Holiday Mercantile',schedule=['Sunset Holiday Mercantile in 2026','Saturday, December 5 and Sunday, December 6'],time='11am–5pm',venue='SF County Fair Building in Golden Gate Park',price='Free admission',scope='San Francisco, CA',dates=[date(u,'2026-12-05','2026-12-06','Saturday, December 5 and Sunday, December 6','Sunset Holiday Mercantile in 2026')])
u=url('sunsetmercantilesf.com/holidaysontaraval')
add('taraval',u,name='Holidays On Taraval',schedule='Friday, December 11th, 5pm-10pm',time='5pm – 10pm',venue='TARAVAL Street, 20th-24th Avenue',scope='San Francisco, CA',reason='Year is not explicit; no year inferred from weekday or adjacent events.')
save()
