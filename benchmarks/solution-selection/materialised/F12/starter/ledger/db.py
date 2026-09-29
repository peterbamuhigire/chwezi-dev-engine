"""SQLite storage for synthetic entity K (one book, MAIN). All amounts are integer minor units."""
from __future__ import annotations

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    kind TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS periods (
    entity TEXT NOT NULL,
    period TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'closed')),
    PRIMARY KEY (entity, period)
);
CREATE TABLE IF NOT EXISTS actors (
    actor TEXT PRIMARY KEY,
    role TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS journals (
    id INTEGER PRIMARY KEY,
    entity TEXT NOT NULL,
    book TEXT NOT NULL,
    period TEXT NOT NULL,
    currency TEXT NOT NULL,
    source TEXT NOT NULL,
    request_key TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    actor TEXT NOT NULL,
    version INTEGER NOT NULL,
    evidence_ref TEXT NOT NULL,
    reference TEXT,
    reversal_of INTEGER REFERENCES journals (id),
    posted_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    UNIQUE (entity, book, request_key)
);
CREATE TABLE IF NOT EXISTS journal_lines (
    journal_id INTEGER NOT NULL REFERENCES journals (id),
    line_no INTEGER NOT NULL,
    account TEXT NOT NULL REFERENCES accounts (code),
    debit_minor INTEGER NOT NULL CHECK (debit_minor >= 0),
    credit_minor INTEGER NOT NULL CHECK (credit_minor >= 0),
    PRIMARY KEY (journal_id, line_no)
);
CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY,
    event TEXT NOT NULL,
    journal_id INTEGER,
    request_key TEXT,
    actor TEXT,
    detail TEXT,
    at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    """Open a connection in autocommit mode; callers manage transactions explicitly."""
    conn = sqlite3.connect(path, isolation_level=None, timeout=10, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)


def seed_fixture(conn: sqlite3.Connection) -> None:
    """Synthetic chart, periods and actors for entity K. Not real accounts or rates."""
    conn.executemany("INSERT OR IGNORE INTO accounts VALUES (?, ?, ?)", [
        ("1000", "Bank - operating", "asset"),
        ("1100", "Trade receivables", "asset"),
        ("4000", "Revenue", "income"),
    ])
    conn.executemany("INSERT OR IGNORE INTO periods VALUES ('K', ?, ?)", [
        ("2026-08", "closed"), ("2026-09", "open"), ("2026-10", "open"),
    ])
    conn.executemany("INSERT OR IGNORE INTO actors VALUES (?, ?)", [
        ("cashier-1", "cashier"), ("controller-1", "controller"), ("visitor-3", "read_only"),
    ])
