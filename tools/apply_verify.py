#!/usr/bin/env python3
"""RETIRED: shared-page name matches cannot approve individual event fields.

The old applicator could preserve an inherited field-level label or fabricate a
manual-reading fallback. Canonical data now comes only from explicit decisions in
data/audit_64f8b973.json via tools/consolidate.py and tools/audited_register.py.
The historical matcher report remains available as unverified research history.
"""
raise SystemExit('Retired unsafe applicator. Run python tools/consolidate.py, then python scripts/build.py and python scripts/validate.py. No files were modified.')
