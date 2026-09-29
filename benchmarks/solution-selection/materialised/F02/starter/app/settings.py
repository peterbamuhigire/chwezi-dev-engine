"""Account settings form: server-side handling for the renewal date field."""
from __future__ import annotations

import html
from datetime import datetime, timedelta, timezone
from pathlib import Path
from string import Template

TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "settings.html"
FIELD = "renewal_date"


def handle_submit(form: dict) -> tuple[dict, dict]:
    """Validate a submitted form. Returns (errors by field, values to store)."""
    raw = form.get(FIELD, "")
    if raw == "":
        return {}, {FIELD: None}
    try:
        parsed = datetime.strptime(raw.strip(), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except (ValueError, AttributeError):
        return {FIELD: "Enter the renewal date as YYYY-MM-DD."}, {}
    return {}, {FIELD: parsed.isoformat()}


def display_value(stored: dict, utc_offset_minutes: int = 0) -> str:
    """Value to put back into the form for a user in the given UTC offset."""
    value = stored.get(FIELD)
    if not value:
        return ""
    moment = datetime.fromisoformat(value).astimezone(timezone(timedelta(minutes=utc_offset_minutes)))
    return moment.date().isoformat()


def render_form(value: str = "", error: str = "") -> str:
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"))
    return template.safe_substitute(
        value=html.escape(value, quote=True),
        error=html.escape(error),
        error_hidden="" if error else "hidden",
    )
