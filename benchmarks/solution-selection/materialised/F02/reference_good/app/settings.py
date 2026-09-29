"""Account settings form: server-side handling for the renewal date field.

The renewal date is a civil date: it is validated strictly as YYYY-MM-DD and stored and shown
unchanged, never converted through a UTC midnight timestamp. The browser's native date control
supplies selection and keyboard entry; the server stays the authority.
"""
from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path
from string import Template

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "settings.html"
FIELD = "renewal_date"
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
MESSAGE = "Enter the renewal date as a real date, for example 2026-03-01."


def handle_submit(form: dict) -> tuple[dict, dict]:
    """Validate a submitted form. Returns (errors by field, values to store)."""
    raw = form.get(FIELD, "")
    if raw == "":
        return {}, {FIELD: None}
    if not isinstance(raw, str) or not ISO_DATE.fullmatch(raw):
        return {FIELD: MESSAGE}, {}
    try:
        parsed = date.fromisoformat(raw)
    except ValueError:
        return {FIELD: MESSAGE}, {}
    return {}, {FIELD: parsed.isoformat()}


def display_value(stored: dict, utc_offset_minutes: int = 0) -> str:
    """A civil date is the same for every user; the offset is deliberately ignored."""
    value = stored.get(FIELD)
    return value or ""


def render_form(value: str = "", error: str = "") -> str:
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"))
    return template.safe_substitute(
        value=html.escape(value, quote=True),
        error=html.escape(error),
        error_hidden="" if error else "hidden",
        aria_invalid='aria-invalid="true"' if error else "",
    )
