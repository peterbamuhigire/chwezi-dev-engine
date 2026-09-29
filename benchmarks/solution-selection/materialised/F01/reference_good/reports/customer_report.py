"""Monthly customer balance report."""
from __future__ import annotations

from core.identifiers import canonical_id


def build_report(rows) -> list[str]:
    """Return one tab-separated line per row: canonical customer id, name, balance in minor units.

    Identifier normalisation is owned by core.identifiers.canonical_id; an empty identifier
    raises its EmptyIdentifierError, as for the other callers.
    """
    return [f"{canonical_id(row['customer_id'])}\t{row['name']}\t{row['balance_minor']}" for row in rows]
