#!/usr/bin/env python3
"""Compatibility entry point: reachability only, never field verification.

Transport/TLS/challenge failures are unknown, not mislabeled as dead pages.
"""
from check_sources import main

if __name__ == '__main__':
    raise SystemExit(main())
