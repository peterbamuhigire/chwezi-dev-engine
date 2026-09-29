"""m002: validated customer foreign keys on orders (expand / backfill / verify / contract).

Staged so that application v1 keeps working during expand and backfill:

1. expand   - add nullable ``orders.customer_id`` and the exception table; no data changes.
2. backfill - map orders in committed batches; unmatched or ambiguous codes go to
              ``customer_fk_exceptions`` instead of being dropped. Re-runnable: it only works
              on orders that are still unmapped, so an interrupted run resumes naturally.
3. verify   - counts plus a checksum of the source column for reconciliation.
4. contract - only when nothing is unmapped, ambiguous or pending: require customer_id.

``rollback`` removes the triggers and bookkeeping and empties ``customer_id``; it never
touches customers, legacy codes or amounts.
"""
from __future__ import annotations

import hashlib
import sqlite3
from collections import Counter

EXCEPTIONS_DDL = """
CREATE TABLE IF NOT EXISTS customer_fk_exceptions (
    order_id INTEGER PRIMARY KEY,
    legacy_code TEXT,
    reason TEXT NOT NULL CHECK (reason IN ('unmapped', 'ambiguous'))
)
"""
TRIGGERS = ("m002_orders_customer_required_insert", "m002_orders_customer_required_update")


class MigrationBlocked(RuntimeError):
    pass


def _normalise(code: str | None) -> str:
    return (code or "").strip().upper()


def _has_column(conn: sqlite3.Connection, table: str, column: str) -> bool:
    return any(row[1] == column for row in conn.execute(f"PRAGMA table_info({table})"))


def _rollback_quietly(conn: sqlite3.Connection) -> None:
    if conn.in_transaction:
        try:
            conn.execute("ROLLBACK")
        except sqlite3.Error:
            pass


def expand(conn: sqlite3.Connection) -> None:
    conn.execute("BEGIN IMMEDIATE")
    try:
        if not _has_column(conn, "orders", "customer_id"):
            conn.execute("ALTER TABLE orders ADD COLUMN customer_id INTEGER REFERENCES customers(id)")
        conn.execute(EXCEPTIONS_DDL)
        conn.execute("CREATE INDEX IF NOT EXISTS m002_orders_customer_id ON orders(customer_id)")
        conn.execute("COMMIT")
    except BaseException:
        _rollback_quietly(conn)
        raise


def _customer_index(conn: sqlite3.Connection) -> tuple[dict[str, int], set[str]]:
    rows = conn.execute("SELECT id, code FROM customers").fetchall()
    counts = Counter(_normalise(code) for _, code in rows)
    unique = {_normalise(code): cid for cid, code in rows if counts[_normalise(code)] == 1}
    ambiguous = {key for key, n in counts.items() if n > 1}
    return unique, ambiguous


def backfill(conn: sqlite3.Connection, batch_size: int = 50) -> dict:
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    unique, ambiguous = _customer_index(conn)
    last_id = 0
    processed = 0
    while True:
        batch = conn.execute(
            "SELECT id, legacy_customer_code FROM orders WHERE customer_id IS NULL AND id > ? ORDER BY id LIMIT ?",
            (last_id, batch_size),
        ).fetchall()
        if not batch:
            break
        conn.execute("BEGIN IMMEDIATE")
        try:
            for order_id, code in batch:
                key = _normalise(code)
                if key and key in unique:
                    conn.execute("UPDATE orders SET customer_id = ? WHERE id = ? AND customer_id IS NULL", (unique[key], order_id))
                    conn.execute("DELETE FROM customer_fk_exceptions WHERE order_id = ?", (order_id,))
                else:
                    reason = "ambiguous" if key and key in ambiguous else "unmapped"
                    conn.execute(
                        "INSERT INTO customer_fk_exceptions (order_id, legacy_code, reason) VALUES (?, ?, ?) "
                        "ON CONFLICT (order_id) DO UPDATE SET legacy_code = excluded.legacy_code, reason = excluded.reason",
                        (order_id, code, reason),
                    )
            conn.execute("COMMIT")
        except BaseException:
            _rollback_quietly(conn)
            raise
        last_id = batch[-1][0]
        processed += len(batch)
    return {"processed": processed}


def verify(conn: sqlite3.Connection) -> dict:
    total = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    mapped = conn.execute("SELECT COUNT(*) FROM orders WHERE customer_id IS NOT NULL").fetchone()[0]
    reasons = dict(conn.execute(
        "SELECT e.reason, COUNT(*) FROM customer_fk_exceptions e JOIN orders o ON o.id = e.order_id "
        "WHERE o.customer_id IS NULL GROUP BY e.reason").fetchall())
    pending = conn.execute(
        "SELECT COUNT(*) FROM orders o WHERE o.customer_id IS NULL "
        "AND NOT EXISTS (SELECT 1 FROM customer_fk_exceptions e WHERE e.order_id = o.id)").fetchone()[0]
    digest = hashlib.sha256()
    for order_id, code in conn.execute("SELECT id, legacy_customer_code FROM orders ORDER BY id"):
        digest.update(f"{order_id}:{code or ''}\n".encode("utf-8"))
    return {"total": total, "mapped": mapped, "unmapped": reasons.get("unmapped", 0),
            "ambiguous": reasons.get("ambiguous", 0), "pending": pending, "legacy_checksum": digest.hexdigest()}


def contract(conn: sqlite3.Connection) -> None:
    state = verify(conn)
    blockers = {key: state[key] for key in ("unmapped", "ambiguous", "pending") if state[key]}
    if blockers:
        raise MigrationBlocked(f"cannot contract while orders remain unresolved: {blockers}")
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute(f"CREATE TRIGGER IF NOT EXISTS {TRIGGERS[0]} BEFORE INSERT ON orders WHEN NEW.customer_id IS NULL "
                     "BEGIN SELECT RAISE(ABORT, 'orders.customer_id is required after m002 contract'); END")
        conn.execute(f"CREATE TRIGGER IF NOT EXISTS {TRIGGERS[1]} BEFORE UPDATE OF customer_id ON orders WHEN NEW.customer_id IS NULL "
                     "BEGIN SELECT RAISE(ABORT, 'orders.customer_id is required after m002 contract'); END")
        conn.execute("COMMIT")
    except BaseException:
        _rollback_quietly(conn)
        raise


def rollback(conn: sqlite3.Connection) -> None:
    conn.execute("BEGIN IMMEDIATE")
    try:
        for trigger in TRIGGERS:
            conn.execute(f"DROP TRIGGER IF EXISTS {trigger}")
        if _has_column(conn, "orders", "customer_id"):
            conn.execute("UPDATE orders SET customer_id = NULL WHERE customer_id IS NOT NULL")
        conn.execute("DROP INDEX IF EXISTS m002_orders_customer_id")
        conn.execute("DROP TABLE IF EXISTS customer_fk_exceptions")
        conn.execute("COMMIT")
    except BaseException:
        _rollback_quietly(conn)
        raise
