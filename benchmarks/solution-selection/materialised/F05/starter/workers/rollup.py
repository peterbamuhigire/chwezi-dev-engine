"""Hourly roll-up worker: assigns events to adjacent windows."""
from __future__ import annotations

from datetime import datetime

from core.time_windows import in_window


def bucket_events(events: list[dict], boundaries: list[datetime]) -> list[int]:
    """Count events per adjacent window ``[b0, b1), [b1, b2), ...``.

    Every event inside ``[b0, b_last)`` must be counted in exactly one bucket.
    """
    windows = list(zip(boundaries, boundaries[1:]))
    return [sum(1 for event in events if in_window(event["at"], start, end)) for start, end in windows]
