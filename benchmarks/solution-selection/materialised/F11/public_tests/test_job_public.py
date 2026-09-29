import random
import unittest

from notify.clock import FakeClock
from notify.errors import TransientError
from notify.job import NotificationJob
from notify.store import InMemoryStore


class FlakyTransport:
    def __init__(self, failures):
        self.failures = failures
        self.calls = []

    def send(self, message, idempotency_key):
        self.calls.append(idempotency_key)
        if self.failures:
            self.failures -= 1
            raise TransientError("provider busy")
        return "prov-1"

    def status(self, idempotency_key):
        return "unknown"


class PublicJobTests(unittest.TestCase):
    def test_first_attempt_succeeds(self):
        transport = FlakyTransport(0)
        job = NotificationJob(transport, InMemoryStore(), FakeClock(), rng=random.Random(1))
        record = job.process({"id": "n-1", "to": "+256700000001", "body": "Your order is ready"})
        self.assertEqual(record["state"], "sent")
        self.assertEqual(record["provider_id"], "prov-1")

    def test_one_transient_failure_then_success(self):
        transport = FlakyTransport(1)
        job = NotificationJob(transport, InMemoryStore(), FakeClock(), rng=random.Random(1))
        record = job.process({"id": "n-2", "to": "+256700000002", "body": "Reminder"})
        self.assertEqual(record["state"], "sent")
        self.assertEqual(len(transport.calls), 2)


if __name__ == "__main__":
    unittest.main()
