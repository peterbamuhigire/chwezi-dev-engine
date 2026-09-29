"""Accessible date-range calendar (existing, product-tested component; used by the rota screen).

Server-rendered grid enhanced by static/range-calendar.js:
- role="grid" with aria-multiselectable; days in the chosen range carry aria-selected="true";
- roving tabindex: one day button is focusable (tabindex 0), arrow keys move focus;
- unavailable days stay focusable so keyboard and screen-reader users can explore them, carry
  aria-disabled="true" and point (aria-describedby) at the visible reason;
- hidden inputs ``start`` and ``end`` carry the ISO dates submitted to the server;
- a polite live region summarises the range in the account locale.
"""
from __future__ import annotations

import calendar
import html
from datetime import date

from components.locale_format import format_date, format_month, format_range


def _reason_for(day: date, blackouts) -> tuple[int, str] | None:
    for index, blackout in enumerate(blackouts):
        if blackout.start <= day <= blackout.end:
            return index, blackout.reason
    return None


def render_range_calendar(prefix: str, year: int, month: int, blackouts, locale: str,
                          start: date | None = None, end: date | None = None) -> str:
    esc = html.escape
    days = [date(year, month, d) for d in range(1, calendar.monthrange(year, month)[1] + 1)]
    focus = start if start and start.month == month and start.year == year else None
    if focus is None:
        focus = next((d for d in days if _reason_for(d, blackouts) is None), days[0])
    rows, week = [], []
    for day in days:
        reason = _reason_for(day, blackouts)
        selected = bool(start and end and start <= day <= end) or day == start
        cell = [f'<td role="gridcell" aria-selected="{"true" if selected else "false"}"']
        button = [f'<button type="button" data-date="{day.isoformat()}" tabindex="{0 if day == focus else -1}"',
                  f' aria-label="{esc(format_date(day, locale))}"']
        if reason is not None:
            cell.append(f' aria-disabled="true" aria-describedby="{prefix}-reason-{reason[0]}"')
            button.append(f' aria-disabled="true" aria-describedby="{prefix}-reason-{reason[0]}"')
        week.append("".join(cell) + ">" + "".join(button) + f">{day.day}</button></td>")
        if len(week) == 7:
            rows.append("<tr>" + "".join(week) + "</tr>")
            week = []
    if week:
        rows.append("<tr>" + "".join(week) + "</tr>")
    reasons = "".join(
        f'<li id="{prefix}-reason-{i}">{esc(format_date(b.start, locale))} – {esc(format_date(b.end, locale))}: {esc(b.reason)}</li>'
        for i, b in enumerate(blackouts))
    summary = esc(format_range(start, end, locale)) if start and end else ""
    return (
        f'<div class="range-calendar" data-component="range-calendar">'
        f'<h3 id="{prefix}-caption">{esc(format_month(year, month, locale))}</h3>'
        f'<p id="{prefix}-instructions">Use the arrow keys to move between days and Enter to choose the first and last day. '
        f'Unavailable days explain why.</p>'
        f'<table role="grid" aria-labelledby="{prefix}-caption" aria-describedby="{prefix}-instructions" aria-multiselectable="true">'
        + "".join(rows) + "</table>"
        f'<ul id="{prefix}-reasons">{reasons}</ul>'
        f'<input type="hidden" name="start" value="{start.isoformat() if start else ""}">'
        f'<input type="hidden" name="end" value="{end.isoformat() if end else ""}">'
        f'<p id="{prefix}-summary" aria-live="polite">{summary}</p>'
        f'</div>'
    )
