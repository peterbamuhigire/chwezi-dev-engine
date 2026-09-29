import unittest

from worker.errors import TransientFailure
from worker.parser import parse_record
from worker.retry import RetryMachine
from worker.tracing import FakeClock, RecordingTracer


class ParserPublicTests(unittest.TestCase):
    def test_simple_record(self):
        self.assertEqual(parse_record("order=1042; status=paid; note="), {"order": "1042", "status": "paid", "note": ""})

    def test_trailing_separator(self):
        self.assertEqual(parse_record("a=1;b=2;"), {"a": "1", "b": "2"})


class RetryPublicTests(unittest.TestCase):
    def test_success_after_one_transient_failure(self):
        calls = []

        def operation():
            calls.append(1)
            if len(calls) == 1:
                raise TransientFailure("gateway busy")

        state = RetryMachine(RecordingTracer(), FakeClock()).run(operation)
        self.assertEqual(state, "SUCCEEDED")
        self.assertEqual(len(calls), 2)


if __name__ == "__main__":
    unittest.main()
