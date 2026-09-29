"""Bounded, classified, idempotent notification delivery."""
import random

from notify.errors import PermanentError, RetryAfter, TransientError


class NotificationJob:
    def __init__(self, transport, store, clock, rng=None, max_attempts=5, base_delay=1.0, max_delay=30.0):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        self.transport = transport
        self.store = store
        self.clock = clock
        self.rng = rng or random.Random()
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._shutdown = False

    def request_shutdown(self):
        self._shutdown = True

    def backoff(self, attempt: int, hint: float | None = None) -> float:
        """Delay before attempt ``attempt + 1``: capped exponential with equal jitter."""
        ceiling = min(self.max_delay, self.base_delay * 2 ** (attempt - 1))
        delay = ceiling / 2 + self.rng.random() * ceiling / 2
        if hint is not None:
            delay = max(delay, min(hint, self.max_delay))
        return delay

    def _record(self, key):
        record = self.store.get(key)
        return record if record is not None else self.store.put(key)

    def process(self, notification):
        key = notification["id"]
        record = self._record(key)
        if record["state"] in ("sent", "dead_letter"):
            return record
        attempts = record["attempts"]
        while True:
            if self._shutdown:
                return self.store.update(key, state="pending", attempts=attempts)
            attempts += 1
            self.store.update(key, attempts=attempts)
            hint = None
            try:
                provider_id = self.transport.send(notification, idempotency_key=key)
            except PermanentError as exc:
                return self.store.update(key, state="dead_letter", last_error=f"permanent: {exc}")
            except TimeoutError as exc:
                if self._accepted(key):
                    return self.store.update(key, state="sent", last_error=None)
                error = f"timeout: {exc}"
            except RetryAfter as exc:
                hint, error = exc.seconds, f"retry-after {exc.seconds}s: {exc}"
            except TransientError as exc:
                error = f"transient: {exc}"
            else:
                return self.store.update(key, state="sent", provider_id=provider_id, last_error=None)
            self.store.update(key, last_error=error)
            if attempts >= self.max_attempts:
                return self.store.update(key, state="dead_letter", last_error=f"exhausted after {attempts} attempts; {error}")
            self.clock.sleep(self.backoff(attempts, hint))

    def _accepted(self, key) -> bool:
        try:
            return self.transport.status(key) == "accepted"
        except Exception:  # unreadable status counts as not accepted; the stable key keeps a resend idempotent
            return False
