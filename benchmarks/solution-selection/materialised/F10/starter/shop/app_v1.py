"""Version 1 of the application. It stays deployed while the migration's expand stage runs."""
from __future__ import annotations

import sqlite3


def create_order(conn: sqlite3.Connection, legacy_code: str | None, amount_minor: int) -> int:
    cursor = conn.execute("INSERT INTO orders (legacy_customer_code, amount_minor) VALUES (?, ?)", (legacy_code, amount_minor))
    return int(cursor.lastrowid)


def list_orders(conn: sqlite3.Connection) -> list[tuple]:
    return conn.execute("SELECT id, legacy_customer_code, amount_minor FROM orders ORDER BY id").fetchall()


def customer_total(conn: sqlite3.Connection, legacy_code: str) -> int:
    row = conn.execute("SELECT COALESCE(SUM(amount_minor), 0) FROM orders WHERE legacy_customer_code = ?", (legacy_code,)).fetchone()
    return int(row[0])
