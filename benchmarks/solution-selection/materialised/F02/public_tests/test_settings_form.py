import unittest

from app.settings import display_value, handle_submit, render_form


class SettingsFormTests(unittest.TestCase):
    def test_valid_date_round_trips(self):
        errors, stored = handle_submit({"renewal_date": "2026-03-01"})
        self.assertEqual(errors, {})
        self.assertEqual(display_value(stored, 0), "2026-03-01")

    def test_impossible_date_rejected(self):
        errors, stored = handle_submit({"renewal_date": "2026-02-30"})
        self.assertIn("renewal_date", errors)

    def test_empty_value_is_retained_as_absence(self):
        errors, stored = handle_submit({"renewal_date": ""})
        self.assertEqual(errors, {})
        self.assertIsNone(stored["renewal_date"])
        self.assertEqual(display_value(stored, 0), "")

    def test_form_renders_field_with_label(self):
        page = render_form("2026-03-01")
        self.assertIn('name="renewal_date"', page)
        self.assertIn('<label for="renewal-date">', page)


if __name__ == "__main__":
    unittest.main()
