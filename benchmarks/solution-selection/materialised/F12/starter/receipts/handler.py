"""Receipt callbacks from the simulated payment provider (to be implemented).

See README.md for the callback contract.
"""
from __future__ import annotations

import sqlite3

BANK_ACCOUNT = "1000"
RECEIVABLE_ACCOUNT = "1100"


def process_receipt(conn: sqlite3.Connection, body: bytes, signature: str, *, secret: bytes, actor: str) -> int:
    """Post the receipt described by ``body`` and return the journal id."""
    raise NotImplementedError


def reverse_receipt(conn: sqlite3.Connection, journal_id: int, *, actor: str, reason: str, evidence_ref: str) -> int:
    """Correct a posted receipt and return the id of the correcting journal."""
    raise NotImplementedError
