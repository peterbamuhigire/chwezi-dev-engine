"""Join ledger entries to daily partitions."""
from __future__ import annotations

from datetime import datetime

from core.time_windows import in_window


def join_partitions(entries: list[dict], partitions: dict[str, tuple[datetime, datetime]]) -> dict[str, list[str]]:
    """Map each partition key to the ids of the entries it holds."""
    return {key: [entry["id"] for entry in entries if in_window(entry["at"], start, end)] for key, (start, end) in partitions.items()}
