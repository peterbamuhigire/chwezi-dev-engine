"""Locale-aware date display for the account's chosen locale (not the browser's)."""
from __future__ import annotations

from datetime import date

SUPPORTED = ("en-GB", "en-US", "fr-FR")
_MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
}


def format_date(value: date, locale: str) -> str:
    if locale not in SUPPORTED:
        locale = "en-GB"
    if locale == "en-US":
        return f"{_MONTHS['en'][value.month - 1]} {value.day}, {value.year}"
    months = _MONTHS["fr"] if locale == "fr-FR" else _MONTHS["en"]
    return f"{value.day} {months[value.month - 1]} {value.year}"


def format_month(year: int, month: int, locale: str) -> str:
    months = _MONTHS["fr"] if locale == "fr-FR" else _MONTHS["en"]
    return f"{months[month - 1]} {year}"


def format_range(start: date, end: date, locale: str) -> str:
    if locale == "fr-FR":
        return f"Du {format_date(start, locale)} au {format_date(end, locale)}"
    return f"From {format_date(start, locale)} to {format_date(end, locale)}"
