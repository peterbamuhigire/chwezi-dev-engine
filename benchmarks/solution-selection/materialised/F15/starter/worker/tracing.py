class RecordingTracer:
    """In-memory tracer used by tests and local runs."""

    def __init__(self):
        self.spans: list[tuple[str, dict]] = []

    def span(self, name: str, **attributes) -> None:
        self.spans.append((name, attributes))


class FakeClock:
    def __init__(self):
        self.sleeps: list[float] = []

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
