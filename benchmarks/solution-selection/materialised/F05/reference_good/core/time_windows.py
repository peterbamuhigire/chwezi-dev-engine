"""Half-open time windows shared by the API, the workers and the exports.

Contract (documented in docs/time-windows.md):

- a window ``[start, end)`` includes ``start`` and excludes ``end``;
- an empty window (``start == end``) contains nothing;
- a reversed window (``end < start``) raises ``InvalidWindow``;
- naive and time-zone-aware datetimes are never compared silently: mixing them raises.
"""
from __future__ import annotations

from datetime import datetime


class InvalidWindow(ValueError):
    pass


def _is_aware(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() is not None


def validate_window(start: datetime, end: datetime) -> None:
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise InvalidWindow("window bounds must be datetimes")
    if _is_aware(start) != _is_aware(end):
        raise InvalidWindow("window mixes naive and aware bounds")
    if end < start:
        raise InvalidWindow("window end precedes its start")


def in_window(ts: datetime, start: datetime, end: datetime) -> bool:
    """Return True when ``ts`` falls inside the half-open window ``[start, end)``."""
    validate_window(start, end)
    if not isinstance(ts, datetime):
        raise InvalidWindow("timestamp must be a datetime")
    if _is_aware(ts) != _is_aware(start):
        raise InvalidWindow("timestamp and window mix naive and aware values")
    return start <= ts < end
