#!/usr/bin/env python3
"""Fetch every unique official source URL cited by the register.

The sandbox used to author the register has no general outbound network, so this
check runs in CI (see .github/workflows/checks.yml) where network is available.

Fail (exit 1) on: DNS/connection failure, or an HTTP 404/410 (dead link).
Warn on 403/429/5xx — many organizer sites block automated clients but are live.

Run:  python3 tools/remotecheck.py [--timeout SECONDS]
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = 20
if "--timeout" in sys.argv:
    TIMEOUT = int(sys.argv[sys.argv.index("--timeout") + 1])

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

sources = json.load(open(os.path.join(ROOT, "data", "sources.json")))
events = json.load(open(os.path.join(ROOT, "data", "events.json")))
used = {}
for row in events:
    for sid in row["sources"]:
        used.setdefault(sid, []).append(row["name"])
urls = {}
for sid, rec in sources.items():
    urls.setdefault(rec["url"], []).extend(used.get(sid, [sid]))

print(f"checking {len(urls)} unique official source URLs "
      f"(cited by {sum(len(v) for v in urls.values())} rows)\n")

dead, blocked, ok = [], [], []
for url in sorted(urls):
    label = urls[url][0]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                  "Accept-Language": "en-US,en;q=0.9"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            code = r.getcode()
            ok.append((url, code, label))
            print(f"  {code}  {url}")
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 406, 429) or e.code >= 500:
            blocked.append((url, e.code, label))
            print(f"  {e.code}  {url}  (bot-blocked/server error — manual check)")
        else:
            dead.append((url, e.code, label))
            print(f"  {e.code}  {url}  <-- DEAD")
    except Exception as e:
        dead.append((url, type(e).__name__, label))
        print(f"  ERR {url}  <-- {type(e).__name__}: {str(e)[:70]}")
    time.sleep(0.4)

print(f"\nOK: {len(ok)}   bot-blocked/5xx: {len(blocked)}   dead: {len(dead)}")
if dead:
    print("::error title=Dead source links::" + "; ".join(f"{c} {u}" for u, c, _ in dead)[:6000])
if dead:
    print("\nFAILED — these source links do not resolve:")
    for u, c, l in dead:
        print(f"  - [{c}] {u}  ({l})")
    sys.exit(1)
print("OK — no dead source links")
