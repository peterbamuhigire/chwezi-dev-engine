"""Blackout periods (inclusive) with the explanation shown to people choosing dates."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Blackout:
    start: date
    end: date
    reason: str


BLACKOUTS = (
    Blackout(date(2026, 3, 10), date(2026, 3, 12), "Closed for staff training"),
    Blackout(date(2026, 3, 20), date(2026, 3, 20), "Public holiday"),
)
