import tempfile
import unittest
from pathlib import Path

from shop import app_v1, schema, seed


class M002PublicTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.conn = schema.connect(Path(self._tmp.name) / "shop.sqlite3")
        schema.create_legacy_schema(self.conn)
        seed.seed(self.conn)

    def tearDown(self):
        self.conn.close()
        self._tmp.cleanup()

    def test_v1_reads_after_expand(self):
        from migrations import m002_customer_fk as m
        m.expand(self.conn)
        self.assertEqual(app_v1.list_orders(self.conn)[0], (1, "BETA", 12000))
        self.assertEqual(app_v1.customer_total(self.conn, "BETA"), 12000)

    def test_backfill_maps_exact_code(self):
        from migrations import m002_customer_fk as m
        m.expand(self.conn)
        m.backfill(self.conn)
        row = self.conn.execute("SELECT customer_id FROM orders WHERE id = 1").fetchone()
        self.assertEqual(row[0], 2)

    def test_verify_reports_total(self):
        from migrations import m002_customer_fk as m
        m.expand(self.conn)
        m.backfill(self.conn)
        self.assertIn("total", m.verify(self.conn))


if __name__ == "__main__":
    unittest.main()
