import json
import tempfile
import unittest

from service.http_api import handle_create
from service.queue_consumer import consume
from service.store import Store

VALID = {"id": "ord-1", "customer": "Kato Traders", "items": [{"sku": "AB12", "qty": 3}]}


class CreateOrderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Store(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_http_valid_order_is_created(self):
        status, payload = handle_create(json.dumps(VALID).encode(), self.store)
        self.assertEqual(status, 201)
        self.assertEqual(self.store.load("ord-1")["customer"], "Kato Traders")

    def test_http_missing_items_is_rejected(self):
        body = json.dumps({"id": "ord-2", "customer": "Kato"}).encode()
        status, payload = handle_create(body, self.store)
        self.assertEqual(status, 422)
        self.assertEqual(payload["error"]["code"], "validation_failed")
        self.assertEqual(self.store.count(), 0)

    def test_queue_valid_order_is_accepted(self):
        self.assertEqual(consume(dict(VALID), self.store)["status"], "accepted")


if __name__ == "__main__":
    unittest.main()
