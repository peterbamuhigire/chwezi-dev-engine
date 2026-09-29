"""Scheduling page: reuses the accessible range calendar (see docs/decisions/0001-scheduling-date-input.md)."""
from __future__ import annotations

import html
from datetime import date

from components.range_calendar import render_range_calendar
from scheduling.blackouts import BLACKOUTS


def render_schedule_page(locale: str = "en-GB", start: date | None = None, end: date | None = None,
                         errors: list[str] | None = None, year: int = 2026, month: int = 3) -> str:
    error_block = ""
    if errors:
        items = "".join(f"<li>{html.escape(message)}</li>" for message in errors)
        error_block = f'<div id="schedule-errors" role="alert"><ul>{items}</ul></div>'
    return (
        '<form method="post" action="/schedule" aria-labelledby="schedule-heading">'
        '<h2 id="schedule-heading">Book a visit</h2>'
        + error_block
        + render_range_calendar("schedule", year, month, BLACKOUTS, locale, start, end)
        + '<button type="submit">Request booking</button>'
        '</form>'
    )
