"""Posting service: the only sanctioned way to write journals.

``validate`` enforces the posting controls (open period, authorised actor, evidence, balance).
``insert_journal`` writes header, lines and the audit row but does not open or close a
transaction: the caller owns it. ``post_journal`` wraps both in one transaction.
"""
from __future__ import annotations

import sqlite3

POSTING_ROLES = {"cashier", "controller"}


class PostingError(Exception):
    """Base class for rejected postings."""


class PeriodClosed(PostingError):
    pass


class Unauthorised(PostingError):
    pass


class Unbalanced(PostingError):
    pass


class MissingEvidence(PostingError):
    pass


def period_of(value_date: str) -> str:
    """'2026-09-15' -> '2026-09'. Raises ValueError for a malformed date."""
    parts = value_date.split("-")
    if len(parts) != 3 or not all(p.isdigit() for p in parts) or len(parts[0]) != 4:
        raise ValueError(f"invalid value date {value_date!r}")
    return f"{parts[0]}-{parts[1]}"


def validate(conn: sqlite3.Connection, header: dict, lines: list[tuple[str, int, int]]) -> None:
    row = conn.execute("SELECT status FROM periods WHERE entity = ? AND period = ?", (header["entity"], header["period"])).fetchone()
    if row is None or row[0] != "open":
        raise PeriodClosed(f"period {header['period']} is not open for {header['entity']}")
    role = conn.execute("SELECT role FROM actors WHERE actor = ?", (header["actor"],)).fetchone()
    if role is None or role[0] not in POSTING_ROLES:
        raise Unauthorised(f"actor {header['actor']!r} may not post journals")
    if not str(header.get("evidence_ref") or "").strip():
        raise MissingEvidence("a journal needs source evidence")
    if not lines:
        raise Unbalanced("a journal needs lines")
    debit = credit = 0
    for account, dr, cr in lines:
        if not (isinstance(dr, int) and isinstance(cr, int)) or dr < 0 or cr < 0 or (dr and cr):
            raise Unbalanced(f"invalid line on {account}")
        debit += dr
        credit += cr
    if debit != credit or debit == 0:
        raise Unbalanced(f"debits {debit} != credits {credit}")


def record_audit(conn: sqlite3.Connection, event: str, *, journal_id=None, request_key=None, actor=None, detail: str = "") -> None:
    conn.execute("INSERT INTO audit (event, journal_id, request_key, actor, detail) VALUES (?, ?, ?, ?, ?)",
                 (event, journal_id, request_key, actor, detail))


def insert_journal(conn: sqlite3.Connection, header: dict, lines: list[tuple[str, int, int]]) -> int:
    cur = conn.execute(
        "INSERT INTO journals (entity, book, period, currency, source, request_key, payload_hash, actor, version,"
        " evidence_ref, reference, reversal_of) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (header["entity"], header["book"], header["period"], header["currency"], header["source"], header["request_key"],
         header["payload_hash"], header["actor"], header["version"], header["evidence_ref"], header.get("reference"),
         header.get("reversal_of")))
    journal_id = cur.lastrowid
    conn.executemany("INSERT INTO journal_lines VALUES (?, ?, ?, ?, ?)",
                     [(journal_id, index, account, dr, cr) for index, (account, dr, cr) in enumerate(lines, start=1)])
    record_audit(conn, "journal_posted", journal_id=journal_id, request_key=header["request_key"], actor=header["actor"],
                 detail=f"source={header['source']}")
    return journal_id


def post_journal(conn: sqlite3.Connection, header: dict, lines: list[tuple[str, int, int]]) -> int:
    conn.execute("BEGIN IMMEDIATE")
    try:
        validate(conn, header, lines)
        journal_id = insert_journal(conn, header, lines)
        conn.execute("COMMIT")
        return journal_id
    except BaseException:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise
