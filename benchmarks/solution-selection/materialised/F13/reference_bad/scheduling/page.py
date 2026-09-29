"""Scheduling page: native date inputs keep it simple."""
from __future__ import annotations

import html
from datetime import date


def render_schedule_page(locale: str = "en-GB", start: date | None = None, end: date | None = None,
                         errors: list[str] | None = None, year: int = 2026, month: int = 3) -> str:
    error_block = "".join(f'<p class="error">{html.escape(e)}</p>' for e in errors or [])
    return (
        '<form method="post" action="/schedule">'
        '<h2>Book a visit</h2>'
        + error_block +
        '<label for="start">First day</label>'
        f'<input type="date" id="start" name="start" min="{year}-{month:02d}-01" value="{start.isoformat() if start else ""}">'
        '<label for="end">Last day</label>'
        f'<input type="date" id="end" name="end" min="{year}-{month:02d}-01" value="{end.isoformat() if end else ""}">'
        '<button type="submit">Request booking</button>'
        '</form>'
    )
