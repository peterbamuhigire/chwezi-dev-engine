"""Scheduling page."""
from __future__ import annotations

from datetime import date


def render_schedule_page(locale: str = "en-GB", start: date | None = None, end: date | None = None,
                         errors: list[str] | None = None, year: int = 2026, month: int = 3) -> str:
    return (
        '<form method="post" action="/schedule">'
        '<h2>Book a visit</h2>'
        '<p>Scheduling is coming soon.</p>'
        '<button type="submit" disabled>Request booking</button>'
        '</form>'
    )
