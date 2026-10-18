#!/usr/bin/env python3
"""Preserve the newer mainline audit as UNVERIFIED candidate input.

The upstream tool/ledger are left byte-for-byte untouched (another session's
scope). Their legacy transformation runs in an isolated temporary tree, never on
canonical/public files. Its labels/values are not approvals: audited_register's
mandatory final projection blanks anything lacking this audit's own decision.
"""
from __future__ import annotations

import json
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def include_upstream(rows, sources, findings):
    ledger = ROOT / 'data/audit_f1fd3c36.json'
    tool = ROOT / 'tools/apply_audit.py'
    if not ledger.is_file() or not tool.is_file():
        raise ValueError('Required merged upstream research inputs are missing')
    with tempfile.TemporaryDirectory(prefix='sf-unverified-upstream-') as directory:
        work = Path(directory)
        (work / 'data').mkdir()
        (work / 'tools').mkdir()
        shutil.copyfile(ledger, work / 'data' / ledger.name)
        shutil.copyfile(tool, work / 'tools' / tool.name)
        for filename, value in [('events.json', rows), ('sources.json', sources), ('review.json', findings)]:
            (work / 'data' / filename).write_text(json.dumps(value, ensure_ascii=False))
        result = subprocess.run([sys.executable, str(work / 'tools' / tool.name)], cwd=work, capture_output=True, text=True, check=True)
        print('UNVERIFIED upstream candidate transform:', result.stdout.strip())
        values = tuple(json.loads((work / 'data' / filename).read_text()) for filename in ('events.json', 'sources.json', 'review.json'))
    refs = json.loads((ROOT / 'data/upstream_refs_64f8b973.json').read_text())
    for rid, records in refs['references'].items():
        row = next(r for r in values[0] if r['id'] == rid)
        for record in records:
            sid = 'upstream-ref-' + hashlib.sha256(record['url'].encode()).hexdigest()[:12]
            values[1][sid] = record
            if sid not in row['sources']:
                row['sources'].append(sid)
    upstream_ids = {r['id'] for r in json.loads(ledger.read_text()).get('add_rows', [])}
    if not upstream_ids <= {r['id'] for r in values[0]}:
        raise ValueError('An upstream-added candidate was dropped')
    return values
