import json,re,sys
C=json.load(open('data/audit_64f8b973.json'))['captures']
for key in sys.argv[1:]:
 matches=[u for u in C if key in u]
 for u in matches:
  c=C[u];ls=c.get('text','').splitlines();print('\n###',u,c.get('http'),c.get('title'))
  for i,l in enumerate(ls):
   if len(c.get('text',''))<3800 or re.search(r'\b(20[2-3][0-9]|annual|annually|weekly|monthly|every|each|Free|free|admission|tickets|street|Avenue|Boulevard|Market|park|garden|San Francisco|location|place|Where|When|Hours|p\.m\.|a\.m\.|\d+(?::\d+)?\s*(?:am|pm))\b',l,re.I):
    print(i,l[:500])
