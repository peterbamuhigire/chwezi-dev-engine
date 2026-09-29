import random


class NotificationJob:
    def __init__(self, transport, store, clock, rng=None, max_attempts=5, base_delay=1.0, max_delay=30.0):
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

    def process(self, notification):
        key = notification["id"]
        self.store.put(key)
        last = None
        for attempt in range(1, self.max_attempts + 1):
            self.store.update(key, attempts=attempt)
            try:
                provider_id = self.transport.send(notification, idempotency_key=f"{key}-{attempt}")
                return self.store.update(key, state="sent", provider_id=provider_id)
            except Exception as exc:
                last = exc
                self.clock.sleep(min(self.max_delay, self.base_delay * 2 ** (attempt - 1)))
        return self.store.update(key, state="dead_letter", last_error=repr(last))
