import unittest
from datetime import datetime

from api.report import count_events
from exports.csv_export import export_rows
from workers.rollup import bucket_events

T = lambda h, m=0: datetime(2026, 9, 29, h, m)  # noqa: E731


class PublicWindowTests(unittest.TestCase):
    def test_api_excludes_the_upper_bound(self):
        events = [{"at": T(9)}, {"at": T(9, 30)}, {"at": T(10)}]
        self.assertEqual(count_events(events, T(9), T(10)), 2)

    def test_worker_counts_interior_events(self):
        events = [{"at": T(9, 15)}, {"at": T(10, 45)}, {"at": T(10, 50)}]
        self.assertEqual(bucket_events(events, [T(9), T(10), T(11)]), [1, 2])

    def test_export_includes_the_lower_bound(self):
        text = export_rows([{"id": "e1", "at": T(9)}, {"id": "e2", "at": T(9, 5)}], T(9), T(10))
        self.assertEqual(text.splitlines(), ["id,at", "e1,2026-09-29T09:00:00", "e2,2026-09-29T09:05:00"])


if __name__ == "__main__":
    unittest.main()
