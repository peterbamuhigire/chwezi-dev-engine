"""Connection helper and the legacy schema (migration m001)."""
from __future__ import annotations

import sqlite3
from pathlib import Path

LEGACY_SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    legacy_customer_code TEXT,
    amount_minor INTEGER NOT NULL
);
"""


def connect(path: str | Path, timeout: float = 5.0) -> sqlite3.Connection:
    """Autocommit connection; migrations manage their own transactions."""
    conn = sqlite3.connect(str(path), isolation_level=None, timeout=timeout)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_legacy_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(LEGACY_SCHEMA)
