"""Explicit retry state machine; every transition is traced (the runbook reads the spans)."""
from worker.errors import PermanentFailure, TransientFailure

IDLE = "IDLE"
SENDING = "SENDING"
BACKOFF = "BACKOFF"
SUCCEEDED = "SUCCEEDED"
FAILED_PERMANENT = "FAILED_PERMANENT"
EXHAUSTED = "EXHAUSTED"
TERMINAL = frozenset({SUCCEEDED, FAILED_PERMANENT, EXHAUSTED})

# Allowed transitions, kept as data so a reviewer can check them against README.md.
TRANSITIONS = frozenset({
    (IDLE, SENDING),
    (SENDING, SUCCEEDED),
    (SENDING, FAILED_PERMANENT),
    (SENDING, BACKOFF),
    (SENDING, EXHAUSTED),
    (BACKOFF, SENDING),
})


class RetryMachine:
    def __init__(self, tracer, clock, max_attempts=4, delay=1.0):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.tracer = tracer
        self.clock = clock
        self.max_attempts = max_attempts
        self.delay = delay

    def _move(self, source, target, attempt):
        assert (source, target) in TRANSITIONS, f"illegal transition {source} -> {target}"
        self.tracer.span("retry.transition", source=source, target=target, attempt=attempt)
        return target

    def _send(self, operation, attempt):
        """One attempt: return the state that SENDING moves to."""
        try:
            operation()
        except PermanentFailure:
            return FAILED_PERMANENT
        except TransientFailure:
            return EXHAUSTED if attempt >= self.max_attempts else BACKOFF
        return SUCCEEDED

    def run(self, operation):
        attempt = 1
        state = self._move(IDLE, SENDING, attempt)
        while state not in TERMINAL:
            if state == SENDING:
                state = self._move(SENDING, self._send(operation, attempt), attempt)
            else:  # BACKOFF
                self.clock.sleep(self.delay)
                attempt += 1
                state = self._move(BACKOFF, SENDING, attempt)
        return state
