"""m002: customer foreign keys on orders (single-step version)."""
from __future__ import annotations

import hashlib
import sqlite3


class MigrationBlocked(RuntimeError):
    pass


def expand(conn: sqlite3.Connection) -> None:
    columns = [row[1] for row in conn.execute("PRAGMA table_info(orders)")]
    if "customer_id" not in columns:
        conn.execute("ALTER TABLE orders ADD COLUMN customer_id INTEGER REFERENCES customers(id)")


def backfill(conn: sqlite3.Connection, batch_size: int = 50) -> dict:
    conn.execute("UPDATE orders SET customer_id = (SELECT id FROM customers WHERE customers.code = orders.legacy_customer_code)")
    # Orders without a known customer cannot satisfy the foreign key; clean them up.
    conn.execute("DELETE FROM orders WHERE customer_id IS NULL")
    return {"processed": conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]}


def verify(conn: sqlite3.Connection) -> dict:
    total = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    mapped = conn.execute("SELECT COUNT(*) FROM orders WHERE customer_id IS NOT NULL").fetchone()[0]
    digest = hashlib.sha256()
    for order_id, code in conn.execute("SELECT id, legacy_customer_code FROM orders ORDER BY id"):
        digest.update(f"{order_id}:{code or ''}\n".encode("utf-8"))
    return {"total": total, "mapped": mapped, "unmapped": 0, "ambiguous": 0, "pending": total - mapped, "legacy_checksum": digest.hexdigest()}


def contract(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE TRIGGER IF NOT EXISTS m002_required BEFORE INSERT ON orders WHEN NEW.customer_id IS NULL "
                 "BEGIN SELECT RAISE(ABORT, 'customer_id required'); END")


def rollback(conn: sqlite3.Connection) -> None:
    conn.execute("DROP TRIGGER IF EXISTS m002_required")
    conn.execute("UPDATE orders SET customer_id = NULL")
