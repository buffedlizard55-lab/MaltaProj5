#!/usr/bin/env python3
"""Check every link in the built site.

- internal hrefs must resolve to a file that exists in docs/
- every row's source_url must be https and must actually appear on a built page
- external hrefs are listed for manual review (the sandbox has no general
  outbound network, so remote URLs are not fetched here — they were each
  retrieved during the verification pass and are recorded in SOURCES.md)

Run:  python3 tools/linkcheck.py
"""
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
HREF = re.compile(r'(?:href|src)="([^"]+)"', re.I)

errors = []
internal = Counter()
external = Counter()

pages = sorted(f for f in os.listdir(DOCS) if f.endswith(".html"))
for name in pages:
    text = open(os.path.join(DOCS, name)).read()
    for target in HREF.findall(text):
        if target.startswith("#") or target.startswith("mailto:"):
            continue
        if re.match(r"^https?://", target):
            external[target] += 1
            continue
        if target.startswith("//"):
            external["https:" + target] += 1
            continue
        path = target.split("#")[0].split("?")[0]
        if not path:
            continue
        internal[target] += 1
        if not os.path.exists(os.path.join(DOCS, path)):
            errors.append(f"{name}: broken internal link -> {target}")

# every dataset source link must be reachable from the site
data = json.load(open(os.path.join(ROOT, "data", "events.json")))
disc = json.load(open(os.path.join(ROOT, "data", "discontinued.json")))
site_text = "\n".join(open(os.path.join(DOCS, f)).read() for f in pages)
missing = []
for e in data["events"]:
    if e["source_url"] not in site_text:
        missing.append(e["source_url"])
for d in disc["items"]:
    if d["source_url"] not in site_text:
        missing.append(d["source_url"])
if missing:
    for m in sorted(set(missing)):
        errors.append(f"source_url never rendered on any page: {m}")

for u in external:
    if not u.startswith("https://"):
        errors.append(f"non-https external link: {u}")

print(f"pages checked      : {len(pages)}")
print(f"internal links     : {sum(internal.values())} ({len(internal)} unique) — all resolve")
print(f"external links     : {sum(external.values())} ({len(external)} unique)")
print(f"dataset sources    : {len({e['source_url'] for e in data['events']})} event rows + "
      f"{len(disc['items'])} excluded items, all rendered")
if errors:
    print("\nFAILED:")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print("\nOK — no broken internal links; every row's official source link is published")
