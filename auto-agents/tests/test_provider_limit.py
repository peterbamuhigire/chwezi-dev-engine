import datetime as dt
from pathlib import Path
import sys
import unittest
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from execution import provider_limit  # noqa: E402

KAMPALA = ZoneInfo('Africa/Kampala')


def at(hour, minute):
    return dt.datetime(2026, 11, 17, hour, minute, tzinfo=KAMPALA).timestamp()


class ProviderLimitTests(unittest.TestCase):
    def test_claude_five_hour_limit_reads_reset_time(self):
        kind, wait = provider_limit("You've hit your 5-hour limit · resets 7:10am (Africa/Kampala)", now=at(6, 32))
        self.assertEqual(kind, 'usage')
        self.assertEqual(wait, 38 * 60)

    def test_reset_already_passed_today_means_tomorrow(self):
        kind, wait = provider_limit("You've hit your weekly limit · resets 7am (Africa/Kampala)", now=at(8, 0))
        self.assertEqual(kind, 'usage')
        self.assertEqual(wait, 23 * 3600)

    def test_pm_and_twelve_oclock(self):
        self.assertEqual(provider_limit('hit your limit, resets 1:30pm (Africa/Kampala)', now=at(13, 0))[1], 1800)
        self.assertEqual(provider_limit('hit your limit, resets 12am (Africa/Kampala)', now=at(23, 0))[1], 3600)

    def test_usage_limit_without_reset_time(self):
        self.assertEqual(provider_limit('Claude usage limit reached'), ('usage', None))

    def test_rate_limit_and_unrelated_failure(self):
        self.assertEqual(provider_limit('HTTP 429 Too Many Requests'), ('rate', None))
        self.assertEqual(provider_limit('Traceback: AssertionError'), (None, None))

    def test_unknown_zone_falls_back_to_local_time(self):
        kind, wait = provider_limit('hit your limit · resets 7:10am (Mars/Base)')
        self.assertEqual(kind, 'usage')
        self.assertTrue(0 < wait <= 86400)


if __name__ == '__main__':
    unittest.main()
