"""Event counts served by the reporting API."""
from __future__ import annotations

from datetime import datetime


def count_events(events: list[dict], start: datetime, end: datetime) -> int:
    """Count events whose ``at`` timestamp falls in the reporting window.

    OPS-412: the API must not count the event on the upper boundary.
    """
    return sum(1 for event in events if start <= event["at"] < end)
