import tempfile
import unittest
from pathlib import Path

from catalogue import db, users
from catalogue.query import QueryLayer


class SavedFiltersPublicTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = db.connect(Path(self._tmp.name) / "catalogue.sqlite3")
        db.init_schema(self.conn)
        self.q = QueryLayer(self.conn)
        self.user = users.create_user(self.q, "amina@example.invalid")

    def tearDown(self):
        self.conn.close()
        self._tmp.cleanup()

    def test_create_and_list(self):
        from catalogue import saved_filters as sf
        created = sf.create_filter(self.q, self.user, "cheap books", {"category": "books", "max_price": 20000})
        self.assertEqual(created["name"], "cheap books")
        self.assertEqual([f["name"] for f in sf.list_filters(self.q, self.user)], ["cheap books"])

    def test_get_own_filter(self):
        from catalogue import saved_filters as sf
        created = sf.create_filter(self.q, self.user, "lamps", {"text": "lamp"})
        self.assertEqual(sf.get_filter(self.q, self.user, created["id"])["spec"], {"text": "lamp"})

    def test_delete_own_filter(self):
        from catalogue import saved_filters as sf
        created = sf.create_filter(self.q, self.user, "lamps", {"text": "lamp"})
        sf.delete_filter(self.q, self.user, created["id"])
        self.assertEqual(sf.list_filters(self.q, self.user), [])

    def test_spec_must_be_an_object(self):
        from catalogue import saved_filters as sf
        with self.assertRaises(sf.InvalidFilter):
            sf.create_filter(self.q, self.user, "broken", "category=books")


if __name__ == "__main__":
    unittest.main()
