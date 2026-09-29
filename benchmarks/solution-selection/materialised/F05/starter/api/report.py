"""Event counts served by the reporting API."""
from __future__ import annotations

from datetime import datetime

from core.time_windows import in_window


def count_events(events: list[dict], start: datetime, end: datetime) -> int:
    """Count events whose ``at`` timestamp falls in the reporting window."""
    return sum(1 for event in events if in_window(event["at"], start, end))
