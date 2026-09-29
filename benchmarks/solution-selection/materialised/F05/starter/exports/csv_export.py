"""CSV export of events for one window; consumers rely on half-open semantics."""
from __future__ import annotations

import csv
import io
from datetime import datetime

from core.time_windows import in_window


def export_rows(rows: list[dict], start: datetime, end: datetime) -> str:
    """Return CSV text (header ``id,at``) for rows inside ``[start, end)``."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["id", "at"])
    for row in rows:
        if in_window(row["at"], start, end):
            writer.writerow([row["id"], row["at"].isoformat()])
    return buffer.getvalue()
