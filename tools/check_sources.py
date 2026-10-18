#!/usr/bin/env python3
"""Concurrent URL reachability report, NEVER field/event verification.

Only 404/410 are definite dead-page findings. Bot challenges, rate limits, server
errors and transport failures remain explicitly unknown, not rewritten as 200.
No event data, audit decision, or captured evidence is modified.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = 'Mozilla/5.0 (compatible; SFEventsLinkCheck/2.0; +https://github.com/buffedlizard55-lab/MaltaProj5)'


def classification(code):
    if code in (404, 410):
        return 'dead'
    if code in (202, 403, 405, 406, 429):
        return 'challenge_or_restricted'
    if 200 <= code < 400:
        return 'reachable_not_verified'
    if code >= 500:
        return 'server_error_unknown'
    return 'request_error_unknown'


def check(url, timeout=20):
    result = {'url': url}
    for attempt in range(2):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT, 'Accept-Language': 'en-US,en;q=0.9'})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                response.read(512)
                result.update(http=response.status, final_url=response.url, status=classification(response.status))
                return result
        except urllib.error.HTTPError as error:
            result.update(http=error.code, final_url=error.url, status=classification(error.code), error=f'HTTP {error.code}')
            if error.code not in (429, 500, 502, 503, 504):
                return result
        except (OSError, ValueError) as error:
            result.update(http=None, status='transport_unknown', error=f'{type(error).__name__}: {str(error)[:250]}')
        if attempt == 0:
            time.sleep(.5)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout', type=int, default=20)
    parser.add_argument('--output', type=Path, default=Path('/tmp/sf-source-links.json'))
    args = parser.parse_args(argv)
    sources = json.loads((ROOT / 'data/sources.json').read_text())
    urls = sorted({source['url'] for source in sources.values()})
    results = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        tasks = {pool.submit(check, url, args.timeout): url for url in urls}
        for task in as_completed(tasks):
            result = task.result()
            results.append(result)
            print(f"{str(result.get('http')):>4} {result['status']:<26} {result['url']}", flush=True)
    summary = dict(Counter(r['status'] for r in results))
    report = {'checked_at': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'method': 'URL reachability only; neither HTTP success nor name matching verifies event facts. Unknown responses remain unknown.', 'summary': summary, 'urls': sorted(results, key=lambda r: r['url'])}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('REACHABILITY ONLY:', json.dumps(summary, sort_keys=True))
    if summary.get('dead'):
        print('::error::Definite 404/410 source URLs require correction or explicit review disposition before merge.')
        return 1
    unknown = len(results) - summary.get('reachable_not_verified', 0)
    if unknown:
        print(f'::warning::{unknown} URLs have restricted/challenge/server/transport outcomes. They are not counted as verified or classified as dead.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
