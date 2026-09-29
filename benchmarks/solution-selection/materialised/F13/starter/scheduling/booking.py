"""Server-side handling for scheduling requests."""
from __future__ import annotations

from scheduling.blackouts import BLACKOUTS


def validate_booking(form: dict, blackouts=BLACKOUTS) -> tuple[list[str], dict | None]:
    """Return (error messages, booking). Booking is {"start": date, "end": date} when valid."""
    return ["Scheduling is not available yet."], None
