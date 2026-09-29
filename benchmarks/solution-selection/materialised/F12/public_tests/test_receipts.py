import hashlib
import hmac
import json
import unittest

from ledger import db
from receipts import handler

SECRET = b"synthetic-shared-secret-K"


def body(**overrides):
    payload = {"idempotency_key": "rcpt-0001", "entity": "K", "book": "MAIN", "value_date": "2026-09-15",
               "currency": "USD", "amount": "125.50", "receivable_ref": "AR-1001",
               "evidence_ref": "bank-line-5531", "version": 1}
    payload.update(overrides)
    return json.dumps(payload, sort_keys=True).encode("utf-8")


def sign(raw):
    return hmac.new(SECRET, raw, hashlib.sha256).hexdigest()


class ReceiptHappyPath(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()
        db.init_schema(self.conn)
        db.seed_fixture(self.conn)

    def post(self, raw):
        return handler.process_receipt(self.conn, raw, sign(raw), secret=SECRET, actor="cashier-1")

    def lines(self, journal_id):
        return self.conn.execute("SELECT account, debit_minor, credit_minor FROM journal_lines WHERE journal_id = ? ORDER BY line_no",
                                 (journal_id,)).fetchall()

    def test_receipt_posts_balanced_journal(self):
        journal_id = self.post(body())
        self.assertEqual(self.lines(journal_id), [("1000", 12550, 0), ("1100", 0, 12550)])

    def test_replay_returns_original_journal(self):
        raw = body()
        self.assertEqual(self.post(raw), self.post(raw))
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM journals").fetchone()[0], 1)

    def test_reversal_clears_receivable_effect(self):
        journal_id = self.post(body())
        handler.reverse_receipt(self.conn, journal_id, actor="controller-1", reason="posted to wrong customer",
                                evidence_ref="memo-77")
        net = self.conn.execute("SELECT COALESCE(SUM(credit_minor - debit_minor), 0) FROM journal_lines WHERE account = '1100'").fetchone()[0]
        self.assertEqual(net, 0)


if __name__ == "__main__":
    unittest.main()
