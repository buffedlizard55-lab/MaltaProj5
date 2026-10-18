from curate import *
A['extra_events']=[]
def extra(rid,n,cat):
 A['extra_events'].append({'id':rid,'name':n,'category':cat,'tags':[]})
# Small bounded expansion from already read official calendar blocks.
mg=D['family']['geography'];yg=D['x-yerba-buena-gardens-festival']['geography']
u='https://www.sfmoma.org/exhibitions/'
for rid,n,dt,t,iso in [('audit-sfmomaween','SFMOMAween','Saturday, October 31, 2026','11 a.m.–4 p.m.','2026-10-31'),('audit-sfmoma-kiki-ball','Eternal Echoes II: The Kiki Ball with Sir Joq','Thursday, October 22, 2026','6–9 p.m.','2026-10-22')]:
 extra(rid,n,'Museums & science');add(rid,u,name=n,schedule=dt,time=t,venue=F('https://www.sfmoma.org/exhibition/rm-x-sfmoma/','SFMOMA'),scope=mg,dates=[date(u,iso,iso,dt)],reason='Newly captured official calendar entry. Admission is not inferred from museum general admission or nearby free programmes.')
u='https://ybgfestival.org/'
for rid,n,dt,t,iso in [('audit-ybg-halloween-hoopla','Halloween Hoopla','Sat, Oct 31','12:00pm – 3:00pm','2026-10-31'),('audit-ybg-afro-filipino-jazz','Afro-Filipino Jazz Project','Sat, Oct 24','2:00pm – 3:30pm','2026-10-24')]:
 extra(rid,n,'Festivals & culture');add(rid,u,name=n,schedule=dt,time=t,venue='Yerba Buena Gardens',price='admission-free performances',scope=yg,dates=[date(u,iso,iso,dt,'See the 2026 Calendar!')],reason='Current 2026 calendar context checked; festival-wide outdoor admission-free policy applies. Exact stage not established; official visitor information confirms the SF gardens.');D[rid]['parent']='x-yerba-buena-gardens-festival'
u='https://foodwise.org/'
for rid,n,dt,t,iso,v,parent,geoarg in [
 ('audit-foodwise-dia-muertos','Día de los Muertos and Halloween at Mission Community Market','Thursday, October 29, 2026','3:00 pm – 7:00 pm','2026-10-29','Mission','x-mission-community-market',D['x-mission-community-market']['geography']),
 ('audit-foodwise-sofia-demo','Sofía Jiménez, Tutuli Mexican Bakery','Saturday, October 31, 2026','11:00 am – 11:45 am','2026-10-31','Ferry Plaza','b-ferry-plaza-farmers-market',D['b-ferry-plaza-farmers-market']['geography'])]:
 extra(rid,n,'Markets & food');add(rid,u,name=n,schedule=dt,time=t,venue=v,scope=geoarg,dates=[date(u,iso,iso,dt)],reason='New official Foodwise calendar block. Free entry not inferred from market shopping or a different event.');D[rid]['parent']=parent
u='https://presidio.gov/about/press/presidio-unveils-vibrant-2026-summer-event-lineup'
for rid,n,dt,t,iso,v in [
 ('audit-presidio-intertribal','Intertribal Dance Gathering','Saturday, May 30','11 a.m. to 4 p.m.','2026-05-30','Presidio Tunnel Tops, East Meadow'),
 ('audit-presidio-deaf-dance','Bay Area International Deaf Dance Festival','Sunday, August 16','12:00 p.m. to 4:00 p.m.','2026-08-16','Presidio Tunnel Tops, East Meadow'),
 ('audit-presidio-inside-out','Sundown Cinema presents Inside Out','Friday, July 24','7 p.m.','2026-07-24','Civil War Parade Ground, Graham Street, San Francisco')]:
 extra(rid,n,'Community & outdoors');add(rid,u,name=n,schedule=dt,time=t,venue=v,price='Free',scope=D['presidio-fiesta-en-el-parque']['geography'],dates=[date(u,iso,iso,dt,'San Francisco, CA (May 07, 2026)')],reason='New dated 2026 local Presidio component, not the entire regional festival or a next-year date prediction.')
for rid,d in D.items():
 d.setdefault('entry_type','event');d.setdefault('parent','')
# Correct a transient authoring note, now that title context has been adjudicated.
D['x-embarcadero-center-lighting']['reason']='Official title supplies 2026 and the event block supplies November 18; both support the normalized date. Recognized SF Embarcadero Center venue. RSVP link alone does not prove free admission.'
A['review_completed_at']='2026-10-18'
save()
