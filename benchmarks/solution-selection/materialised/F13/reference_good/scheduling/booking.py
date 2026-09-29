"""Server-side handling for scheduling requests. The page is never trusted."""
from __future__ import annotations

import re
from datetime import date

from scheduling.blackouts import BLACKOUTS

ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _parse(raw) -> date | None:
    if not isinstance(raw, str) or not ISO_DATE.fullmatch(raw):
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


def validate_booking(form: dict, blackouts=BLACKOUTS) -> tuple[list[str], dict | None]:
    """Return (error messages, booking). Booking is {"start": date, "end": date} when valid."""
    start, end = _parse(form.get("start")), _parse(form.get("end"))
    if start is None or end is None:
        return ["Choose a first and a last day."], None
    if end < start:
        return ["The last day must be on or after the first day."], None
    clashes = [b for b in blackouts if start <= b.end and end >= b.start]
    if clashes:
        return [f"{b.start.isoformat()} to {b.end.isoformat()} is unavailable: {b.reason}." for b in clashes], None
    return [], {"start": start, "end": end}
