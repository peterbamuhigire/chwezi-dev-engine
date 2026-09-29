"""Monthly customer balance report."""
from __future__ import annotations


def _normalise(customer_id: str) -> str:
    # Collapse whitespace and upper-case so report IDs look like the invoice ones.
    return "-".join(customer_id.split()).upper()


def build_report(rows) -> list[str]:
    lines = []
    for row in rows:
        lines.append(f"{_normalise(row['customer_id'])}\t{row['name']}\t{row['balance_minor']}")
    return lines
