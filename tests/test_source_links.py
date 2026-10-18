import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from check_sources import check, classification

class ReachabilityOnly(unittest.TestCase):
    def test_success_never_claims_fact_verification(self):
        self.assertEqual(classification(200), 'reachable_not_verified')
        for code in (202, 403, 405, 406, 429):
            self.assertEqual(classification(code), 'challenge_or_restricted')
        self.assertEqual(classification(500), 'server_error_unknown')

    @patch('check_sources.time.sleep')
    @patch('check_sources.urllib.request.urlopen', side_effect=urllib.error.URLError('TLS handshake failed'))
    def test_transport_failure_is_unknown_not_dead(self, request, sleep):
        result = check('https://example.org/')
        self.assertEqual(result['status'], 'transport_unknown')
        self.assertIsNone(result['http'])
        self.assertEqual(request.call_count, 2)

    @patch('check_sources.urllib.request.urlopen', side_effect=urllib.error.HTTPError('https://example.org/', 404, 'Not found', {}, None))
    def test_404_is_a_definite_dead_page(self, request):
        result = check('https://example.org/')
        self.assertEqual(result['status'], 'dead')
        self.assertEqual(result['http'], 404)

    @patch('check_sources.urllib.request.urlopen', side_effect=urllib.error.HTTPError('https://example.org/', 403, 'Forbidden', {}, None))
    def test_403_is_not_retried_or_called_dead(self, request):
        result = check('https://example.org/')
        self.assertEqual(result['status'], 'challenge_or_restricted')
        self.assertEqual(request.call_count, 1)
