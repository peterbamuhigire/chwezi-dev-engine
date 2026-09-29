"""Server-side handling for scheduling requests."""
from __future__ import annotations

from datetime import date

from scheduling.blackouts import BLACKOUTS


def _blocked(day: date, blackouts) -> bool:
    return any(b.start <= day <= b.end for b in blackouts)


def validate_booking(form: dict, blackouts=BLACKOUTS) -> tuple[list[str], dict | None]:
    try:
        start = date.fromisoformat(form.get("start", ""))
        end = date.fromisoformat(form.get("end", ""))
    except (TypeError, ValueError):
        return ["Enter valid dates."], None
    if end < start:
        return ["The last day must be on or after the first day."], None
    if _blocked(start, blackouts) or _blocked(end, blackouts):
        return ["Those dates are unavailable."], None
    return [], {"start": start, "end": end}
