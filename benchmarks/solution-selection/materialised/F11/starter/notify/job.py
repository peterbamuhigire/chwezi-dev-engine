import random
import uuid


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
        attempts = 0
        while True:
            try:
                provider_id = self.transport.send(notification, idempotency_key=str(uuid.uuid4()))
                return self.store.update(key, state="sent", provider_id=provider_id, attempts=attempts + 1)
            except Exception as exc:  # retry anything, straight away
                attempts += 1
                self.store.update(key, attempts=attempts, last_error=repr(exc))
                continue
