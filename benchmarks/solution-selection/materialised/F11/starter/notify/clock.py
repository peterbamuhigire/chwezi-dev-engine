import time


class SystemClock:
    def now(self) -> float:
        return time.monotonic()

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


class FakeClock:
    """Deterministic clock; ``sleep`` advances time and records the delay."""

    def __init__(self, now: float = 0.0, on_sleep=None):
        self._now = now
        self.sleeps: list[float] = []
        self.on_sleep = on_sleep

    def now(self) -> float:
        return self._now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self._now += seconds
        if self.on_sleep is not None:
            self.on_sleep(seconds)
