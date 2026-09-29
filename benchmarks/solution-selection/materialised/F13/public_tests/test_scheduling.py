import unittest
from datetime import date

from scheduling.booking import validate_booking
from scheduling.page import render_schedule_page


class SchedulingTests(unittest.TestCase):
    def test_free_range_is_accepted(self):
        errors, booking = validate_booking({"start": "2026-03-02", "end": "2026-03-05"})
        self.assertEqual(errors, [])
        self.assertEqual(booking["start"], date(2026, 3, 2))
        self.assertEqual(booking["end"], date(2026, 3, 5))

    def test_reversed_range_is_rejected(self):
        errors, booking = validate_booking({"start": "2026-03-05", "end": "2026-03-02"})
        self.assertTrue(errors)
        self.assertIsNone(booking)

    def test_blackout_start_is_rejected(self):
        errors, booking = validate_booking({"start": "2026-03-11", "end": "2026-03-13"})
        self.assertTrue(errors)

    def test_page_submits_start_and_end(self):
        page = render_schedule_page("en-GB")
        self.assertIn('name="start"', page)
        self.assertIn('name="end"', page)


if __name__ == "__main__":
    unittest.main()
