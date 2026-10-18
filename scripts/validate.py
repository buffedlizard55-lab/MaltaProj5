import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
root=Path(__file__).resolve().parents[1]
rows=json.loads((root/'data/events.json').read_text()); sources=json.loads((root/'data/sources.json').read_text())
assert len({r['id'] for r in rows})==len(rows)
for r in rows:
 assert r['sources'] and all(s in sources for s in r['sources'])
 assert r['kind'] in ['Weekly','Monthly','Annual','Special']
 for k in ['schedule','time','venue','price']:
  assert r[k] or any(f.startswith(k+': unverified') for f in r['flags']), (r['id'],k)
  if r[k]: assert r['evidence'][k]
 assert not r['parent'] or r['parent'] in {x['id'] for x in rows}
for s in sources.values(): assert s['url'].startswith('https://') and s['checked']=='2026-10-18' and s['excerpt']
class Parse(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a: assert a['id'] not in self.ids; self.ids.add(a['id'])
  for key in ['href','src']:
   if key in a: self.links.append(a[key])
pages={}
for f in root.glob('*.html'):
 p=Parse(); p.feed(f.read_text()); pages[f.name]=p
for name,p in pages.items():
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc: continue
  target=unquote(u.path) or name
  assert (root/target).is_file(),(name,href)
  if u.fragment and target in pages: assert unquote(u.fragment) in pages[target].ids,(name,href)
assert len(pages)==12
print(f'PASS: {len(rows)} rows, evidence references, missing-value flags, parent links, {len(pages)} HTML pages and every local link/fragment.')
