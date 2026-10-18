import json,re,unicodedata
from pathlib import Path
P=Path('data/audit_64f8b973.json'); A=json.loads(P.read_text()); C=A['captures']; D=A['decisions']; R={r['id']:r for r in json.load(open('data/events.json'))}
def N(x):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',x)).strip()
def url(key):
 if key in C:return key
 if 'https://'+key in C:return 'https://'+key
 found=[u for u in C if key in u]
 assert len(found)==1,(key,found)
 return found[0]
def T(u):
 u=url(u) if not u.startswith('https://') else u
 c=C[u]
 return N(c.get('title','')+' '+c.get('text','')+' '+c.get('tool_excerpt',''))
def Q(u,s):
 u=url(u) if not u.startswith('https://') else u
 assert N(s) in T(u),(u,s)
 return {'url':u,'text':s}
def F(u,s):
 if isinstance(s,list):return {'value':' · '.join(s),'quotes':[Q(u,x) for x in s]}
 return {'value':s,'quotes':[Q(u,s)]}
def L(u,i,j=None):
 u=url(u) if not u.startswith('https://') else u
 lines=C[u]['text'].splitlines()
 return lines[i] if j is None else '\n'.join(lines[i:j])
def manual(u,text):
 C[u]['tool_excerpt']=text;C[u]['tool_method']='Selected text read using fetch_page, 2026-10-18; independent of the runner HTTP status.'
def add(rid,u,*,name=None,schedule=None,time=None,venue=None,price=None,kind='Special',recurrence=None,scope=None,dates=(),reason='',publish=True,notes=''):
 u=url(u) if not u.startswith('https://') else u
 if name is None:name=R[rid]['name']
 fields={}
 for k,v in dict(name=name,schedule=schedule,time=time,venue=venue,price=price).items():
  if v is not None: fields[k]=v if isinstance(v,dict) else F(u,v)
 g=scope if isinstance(scope,dict) else ({'status':'confirmed_sf','quotes':[Q(u,scope)],'basis':'Official page explicitly locates the event/venue in San Francisco.'} if scope else {'status':'unverified','quotes':[],'basis':'City-only location not established in the reviewed excerpt.'})
 D[rid]={'reviewer':'64f8b973','reviewed_at':'2026-10-18','fields':fields,'kind':kind,'recurrence':F(u,recurrence) if recurrence else None,'geography':g,'occurrences':list(dates),'publication':'listed' if publish and fields.get('name') and fields.get('venue') and g['status']=='confirmed_sf' else 'review_only','reason':reason,'notes':notes}
def geo(u,text):return {'status':'confirmed_sf','quotes':[Q(u,text)],'basis':'Official San Francisco event/venue location, checked in context.'}
def date(u,start,end,text,year=None):
 return {'start':start,'end':end,'quotes':[Q(u,text)]+([Q(u,year)] if year else [])}
def reject(rid,reason,kind=None):
 D[rid]={'reviewer':'64f8b973','reviewed_at':'2026-10-18','fields':{},'kind':kind or 'Unverified','recurrence':None,'geography':{'status':'unverified','quotes':[],'basis':'Not established'},'occurrences':[],'publication':'review_only','reason':reason,'notes':''}
def save():
 P.write_text(json.dumps(A,indent=1,ensure_ascii=False)+'\n');print('Reviewed decisions:',len(D),'listed:',sum(d['publication']=='listed' for d in D.values()))
