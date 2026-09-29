"""Monthly customer balance report."""
from __future__ import annotations


def build_report(rows) -> list[str]:
    """Return one tab-separated line per row: customer id, name, balance in minor units."""
    lines = []
    for row in rows:
        customer = row["customer_id"].strip()
        lines.append(f"{customer}\t{row['name']}\t{row['balance_minor']}")
    return lines
