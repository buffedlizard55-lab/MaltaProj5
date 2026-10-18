from curate import *
# Replace broad locality cues with the actual official venue/address evidence.
u='https://www.exploratorium.edu/visit'
C[u]['tool_excerpt']+='\nAfter Dark Thursday Night Tickets (18+)\nGeneral $22.95\nDaytime & After Dark Members FREE\nPier 15, Embarcadero, San Francisco'
for rid in ['after-dark','death','digest','unplug-nov','glow','rules','solstice','creep']:
 D[rid]['geography']=geo(u,'Pier 15, Embarcadero, San Francisco')
D['after-dark']['fields']['price']=F(u,['General $22.95','Daytime & After Dark Members FREE']);D['after-dark']['reason']='Age 18+; general and member prices confirmed on the official visit page. Individual themed-event surcharges are not inferred.'
# Venue routes on official museum directions pages establish the SF locations.
manual('https://www.famsf.org/visit/getting-to-the-de-young','''Getting to the de Young
Muni to Golden Gate Park
The de Young encourages the use of public transportation to access the museum.
The following lines are within walking distance to the de Young.
44 O’Shaughnessy Bus
5 + 5R Fulton Bus''')
manual('https://www.famsf.org/visit/getting-to-the-legion-of-honor','''Getting to the Legion of Honor
Muni to Legion of Honor
The 18 takes you up Legion of Honor Drive and stops directly in front of the Legion of Honor.
Take 25th Avenue north to Clement Street. Turn left (west) on Clement Street. Take Clement Street to 34th Avenue. Turn right (north) on 34th Avenue into Lincoln Park.''')
for rid in ['de-young-sat','de-young-tue']:
 D[rid]['geography']=geo('https://www.famsf.org/visit/getting-to-the-de-young','Muni to Golden Gate Park');D[rid]['publication']='listed';D[rid]['reason']='Permanent collection galleries only; full-price special exhibitions still apply. This admission programme does not take place during Bouquets to Art. SF museum location checked against official directions.'
D['legion-sat']['geography']=geo('https://www.famsf.org/visit/getting-to-the-legion-of-honor','Turn right (north) on 34th Avenue into Lincoln Park.');D['legion-sat']['publication']='listed';D['legion-sat']['reason']='Bay Area residency required; permanent collection only; Bouquets to Art exception. Official museum directions confirm Lincoln Park location.'
u='https://www.sf.gov/location--alemany-farmers-market'
add('b-alemany-farmers-market',u,kind='Weekly',schedule='every Saturday',venue='100 Alemany Boulevard',scope='100 Alemany Boulevard\nSan Francisco, CA94110',recurrence='every Saturday',reason='Time left blank: current SF.gov says 7am–2pm, while the City Environment directory says 6am–3pm. Admission not explicitly stated; free parking does not imply free entrance.')
u='https://hotcfarmersmarket.org/about'
add('b-heart-of-the-city-farmers-market',u,name='Heart of the City Farmers’ Market',kind='Weekly',schedule='a year-round farmers’ market on Sundays and Wednesdays',time='7am-4pm',venue='Fulton Plaza between the Downtown Library and the Asian Art Museum',scope="in San Francisco's Civic Center",recurrence='on Sundays and Wednesdays',reason='The About and homepage currently agree on 7am–4pm; earlier contradictory hour notes are superseded by this read. No admission fee is stated.',notes='The operator states closures for Pride Parade in June, Christmas Eve, Christmas Day and New Year’s Day.')
u='https://goldengateparkband.org/'
add('b-golden-gate-park-band',u,name='Golden Gate Park Band',kind='Weekly',schedule='Our season runs from April through September, with shows every Sunday plus July 4 and Labor Day',venue='Spreckels Temple of Music in the Music Concourse of Golden Gate Park',price='free for all',scope='Golden Gate Park',recurrence='shows every Sunday',reason='Seasonal series, not a confirmed next dated occurrence. Operator and City park page differ on season end wording; the operator wording is reproduced, no October date inferred.')
D['b-golden-gate-park-band']['fields']['time']=F('https://sfrecpark.org/1570/Golden-Gate-Bandshell-Concerts','typically start at 1 p.m. on Sundays');D['b-golden-gate-park-band']['geography']=geo('https://sfrecpark.org/1570/Golden-Gate-Bandshell-Concerts','Golden Gate Bandshell Concerts | San Francisco Recreation and Parks, CA')
u='https://www.dftsf.com/'
add('b-downtown-first-thursdays',u,name='DOWNTOWN FIRST THURSDAYS',kind='Monthly',schedule='NOV 5, 2026',time='5-10PM',venue='2nd St. between Market and Howard in SF',price='Free w/ RSVP',scope='2nd St. between Market and Howard in SF',recurrence='Free Monthly Street Party',dates=[date(u,'2026-11-05','2026-11-05','NOV 5, 2026')])
u='https://castronightmarket.com/'
add('b-castro-night-market',u,name='Castro Night Market',kind='Monthly',schedule='October 31, 2026',time='5-10PM',venue='18th & Castro',recurrence='on the 3rd Friday of every month',scope=geo('https://www.castrostreetfair.org/','San Francisco’s Castro neighborhood'),dates=[date(u,'2026-10-31','2026-10-31','October 31, 2026')],reason='Organizer simultaneously advertises a third-Friday pattern and Saturday October 31. The explicit edition date is retained; no date generated from the recurrence. Admission not stated.')
u='https://offthegrid.com/markets/fort-mason-center'
add('b-off-the-grid-fort-mason',u,name='Off the Grid Fort Mason Center',publish=False,reason='Runner returns only the page title. Monthly cadence, 2026 dates, times and admission are not established from that response; inherited values blanked.')
u='https://sfpride.org/events/'
for rid,n,dt,iso,v in [('b-sf-pride-parade','Pride Parade','Sunday, June 28, 2026','2026-06-28','Market Street'),('b-trans-march','Trans March','Friday, June 26, 2026','2026-06-26','Dolores Park, Mission District'),('b-dyke-march','Dyke March','Saturday, June 27, 2026','2026-06-27','Dolores Park, Mission District')]:
 add(rid,u,name=n,schedule=dt,venue=v,scope='San Francisco Pride 2026',dates=[date(u,iso,iso,dt)],reason='2026 event record only. Price/time and a 2027 event-specific day not confirmed; no day inferred from the combined 2027 Pride weekend.')
D['b-trans-march']['kind']='Annual';D['b-trans-march']['recurrence']=F(u,'The Trans March is an annual gathering and march')
u='https://www.castrostreetfair.org/'
add('b-castro-street-fair',u,name='Castro Street Fair',kind='Annual',schedule='Sunday, October 4, 2026',time='11 a.m. to 6 p.m.',venue='San Francisco’s Castro neighborhood',scope='San Francisco’s Castro neighborhood',recurrence='52nd annual celebration',dates=[date(u,'2026-10-04','2026-10-04','Sunday, October 4, 2026')],reason='Organizer announces October 3, 2027, but this entry retains the fully described 2026 edition; 2026 times are not transferred to 2027. A gate donation is requested; no fixed $10–$20 admission confirmed.')
u='https://www.folsomstreet.org/faq'
for rid,n,dt,iso,v in [('b-folsom-street-fair','Folsom Street Fair','Sunday, September 27, 2026','2026-09-27','Folsom Street between 7th and 13th Streets'),('b-up-your-alley','Up Your Alley','Sunday, July 26, 2026','2026-07-26','Folsom Street between 8th and 11th')]:
 add(rid,u,name=n,schedule=dt,time='11AM-6PM',venue=v,scope='Per San Francisco city ordinance, all permitted outdoor events must be smoke-free!',dates=[date(u,iso,iso,dt)],reason='Organizer gives usual last-Sunday patterns but not a guaranteed date for a future year. Gate donation wording is not treated as a confirmed free entrance.')
u='https://chineseparade.com/communityfair/'
add('b-chinese-new-year-street-fair',u,name='Community Street Fair',schedule='The 2027 Community Street Fair is scheduled for Sat. & Sun. Feb. 20 & 21',venue='Grant between California and Broadway',scope='San Francisco’s exhilarating Chinatown',dates=[date(u,'2027-02-20','2027-02-21','The 2027 Community Street Fair is scheduled for Sat. & Sun. Feb. 20 & 21')])
u='https://chineseparade.com/choysundoe/'
add('b-choy-sun-doe',u,name='Choy Sun Doe',schedule='The 2027 Choy Sun Doe Day is scheduled for Saturday, Feb. 6.',venue='Chinatown',scope=geo('https://chineseparade.com/communityfair/','San Francisco’s exhilarating Chinatown'),dates=[date(u,'2027-02-06','2027-02-06','The 2027 Choy Sun Doe Day is scheduled for Saturday, Feb. 6.')],reason='Official announcement does not state admission or start time.')
u='https://sfitalianheritage.org/events/'
add('b-italian-heritage-parade',u,name='Italian Heritage Parade',schedule='Sunday, October 10th 2027 12:30 PM',time='12:30 PM',venue='Jefferson and Powell Streets in Fisherman’s Wharf',scope=geo('https://sfitalianheritage.org/','San Francisco’s Italian-American Community celebrates the Italian Heritage Festival & Parade'),dates=[date(u,'2027-10-10','2027-10-10','Sunday, October 10th 2027 12:30 PM')])
u='https://sunsetmercantilesf.com/northbeachfestival2026/'
add('b-north-beach-festival',u,name='North Beach Festival',schedule='Saturday, June 20th & Sunday, June 21st',time='11 AM to 7 PM',venue='North Beach, San Francisco (centered around Columbus and Green Streets)',scope='North Beach, San Francisco (centered around Columbus and Green Streets)',dates=[date(u,'2026-06-20','2026-06-21','Saturday, June 20th & Sunday, June 21st','North Beach Festival 2026')],reason='Admission not confirmed. Edition numbers differ across legacy sources and are not asserted.')
u='https://www.haightashburystreetfair.org/'
add('b-haight-ashbury-street-fair',u,name='Haight-Ashbury Street Fair',price='Your support helps keep the Fair free',reason='Landing-page text confirms the event/free policy but not an exact street extent or dated schedule. Inherited September 20 and 11am–5:30pm not carried without a dated quote.',publish=False)
u='https://sunsetmercantilesf.com/unionstreetfestival/'
add('b-union-street-festival',u,name='Union Street Festival',schedule='June 6 – June 7, 2026',time='11 am-7 pm',venue='Union Street from Fillmore to Gough Street',scope='street festivals in San Francisco',dates=[date(u,'2026-06-06','2026-06-07','June 6 – June 7, 2026')])
u='https://sfcherryblossom.org/'
add('b-cherry-blossom-festival',u,name='Northern California Cherry Blossom Festival',kind='Annual',schedule='April 10-11 and 17-18, 2027',recurrence='59th Annual Northern California Cherry Blossom Festival',dates=[date(u,'2027-04-10','2027-04-11','April 10-11 and 17-18, 2027'),date(u,'2027-04-17','2027-04-18','April 10-11 and 17-18, 2027')],publish=False,reason='Future dates confirmed; current organizer copy says Peace Plaza is under renovation. Inherited Peace Plaza venue and free admission not copied to 2027 without confirmation.')
u='https://www.nihonmachistreetfair.org/'
add('b-nihonmachi-street-fair',u,name='Nihonmachi Street Fair',kind='Annual',schedule='August 7th & 8th, 2027',venue='San Francisco’s Japantown',scope='San Francisco’s Japantown',recurrence='53rd Annual Nihonmachi Street Fair',dates=[date(u,'2027-08-07','2027-08-08','August 7th & 8th, 2027')],reason='Times, specific street closures and free admission not transferred from earlier editions.')
u='https://www.pistahan.net/'
add('b-pistahan',u,name='Pistahan Parade and Festival',kind='Annual',schedule='Sat, Aug 8 & Sun, Aug 9, 2026',venue='Yerba Buena Gardens',price='Free admission',scope='Yerba Buena Gardens,\nSan Francisco, CA',recurrence='33rd Annual Pistahan Parade and Festival',dates=[date(u,'2026-08-08','2026-08-09','Sat, Aug 8 & Sun, Aug 9, 2026')],reason='Start times and exact parade route not present in the reviewed organizer excerpt.')
u='https://www.moonfestival.org/'
add('b-autumn-moon-festival',u,name='2026 SF Chinatown Autumn Moon Festival',schedule=['2026 SF Chinatown Autumn Moon Festival','September 19 - 20'],venue='GRANT Avenue\nBetween California & Broadway',price='FREE!',scope='2026 SF Chinatown Autumn Moon Festival',dates=[date(u,'2026-09-19','2026-09-20','September 19 - 20','2026 SF Chinatown Autumn Moon Festival')],reason='Time blank: organizer states 11am–5pm while prior official SFMTA evidence conflicts. Both precise hours are retained only in the audit history, not silently reconciled.')
u='https://uissf.org/st-patricks-day-parade'
add('b-st-patricks-day-parade',u,name='San Francisco St. Patrick’s Day Parade',schedule='Saturday, March 14th, 2026',time='11:30am',venue='From 2nd & Market to the Civic Center.',scope='San Francisco St. Patrick’s Day Parade',dates=[date(u,'2026-03-14','2026-03-14','Saturday, March 14th, 2026')],reason='The linked separate Unite SF festival is free; that is not treated as proof of parade admission.')
u='https://www.annunciation.org/news_260903_1'
add('b-greek-food-festival',u,name='San Francisco Greek Food Festival',schedule='September 18–20',time=['Friday, September 18 and Saturday, September 19 from 11:00 a.m. to 10:00 p.m.','Sunday, September 20 from 11:00 a.m. to 7:00 p.m.'],venue='Annunciation Cathedral, 245 Valencia Street',price='Admission is free',scope='245 Valencia Street, San Francisco, CA 94103',dates=[date(u,'2026-09-18','2026-09-20','September 18–20','2026 will be your very first visit')])
u='https://fleetweeksf.org/air-show/'
add('b-fleet-week-air-show',u,name='San Francisco Fleet Week Air Show',kind='Annual',schedule='October 9, 10, 11, 2026',time='12:00 Noon - 4:00 PM',venue='Marina Green',price='General Admission is free.',scope='San Francisco Fleet Week Air Show',recurrence='Held annually',dates=[date(u,'2026-10-09','2026-10-11','October 9, 10, 11, 2026')],reason='SF Marina Green viewing event only; this entry does not admit every activity across the Bay. VIP hospitality is separate.')
u='https://www.baytobreakers.com/'
add('b-bay-to-breakers',u,name='Bay to Breakers',schedule='May 16, 2027',venue='THE STREETS OF SAN FRANCISCO',scope='THIS HISTORIC FUN RUN THROUGH THE STREETS OF SAN FRANCISCO',dates=[date(u,'2027-05-16','2027-05-16','May 16, 2027')],reason='Race date is explicit. Ancillary shakeout/baseball blocks have no year and stale May 18 copy; their year is not inferred from the race banner.')
for rid,n,dt,v in [('b-giants-vs-athletics-b2b-runners-night','GIANTS VS ATHLETICS','Date: May 16th','Oracle Park'),('b-b2b-shakeout-run-2027','B2B SHAKE OUT RUN','Date: May 15th','Sports Basement: Stonestown Galleria')]:
 add(rid,u,name=n,schedule=dt,venue=v,scope='San Francisco, CA 94107' if 'giants' in rid else 'San Francisco, CA 94132',reason='Year deliberately blank: dates are yearless within stale copy that still says before May 18. The 2027 race banner does not verify ancillary-event years.')
reject('b-sf-marathon','Strict city-only rule: the cited full marathon route includes the Golden Gate Bridge/Marin segment. Whole-race row is held for review; no mixed-city event is presented as entirely San Francisco.')
u='https://sundaystreetssf.com/'
add('b-sunday-streets',u,name='Sunday Streets',schedule='2026',venue='San Francisco',scope='Sunday Streets is San Francisco’s open streets program',reason='Umbrella programme, not an individual upcoming instance. The Excelsior dated occurrence is listed separately and linked as a child; no weekly/annual frequency inferred.')
u='https://www.noisepopfest.com/'
add('b-noise-pop-festival',u,name='Noise Pop Festival',schedule='February 18-28, 2027',venue='multiple venues throughout the city of San Francisco',scope='Taking place across multiple venues throughout the city of San Francisco',dates=[date(u,'2027-02-18','2027-02-28','February 18-28, 2027')],reason='Only the explicitly stated San Francisco programme; no Bay Area satellite event or ticket price inferred.')
u='https://www.litquake.org/litcrawl'
# Hold this until the short landing-page text is read with explicit year/venue.
add('b-lit-crawl',u,name='Lit Crawl SF',schedule='OCTOBER 24, 2026',time='all programs from 6:30—7:30 PM',venue="San Francisco's Mission District",price='free pop-up literary event',scope="San Francisco's Mission District",dates=[date(u,'2026-10-24','2026-10-24','OCTOBER 24, 2026')],reason='Current official text says all programs 6:30–7:30 PM; inherited 5–9 PM not reused. Venue changes are listed by the organizer; check the map before attending.')
save()
