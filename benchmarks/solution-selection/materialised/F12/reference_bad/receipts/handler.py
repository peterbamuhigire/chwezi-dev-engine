"""Receipt callbacks from the simulated payment provider (kept deliberately simple)."""
from __future__ import annotations

import hashlib
import hmac
import json
import sqlite3

from receipts.errors import SignatureError

BANK_ACCOUNT = "1000"
RECEIVABLE_ACCOUNT = "1100"


def process_receipt(conn: sqlite3.Connection, body: bytes, signature: str, *, secret: bytes, actor: str) -> int:
    if hmac.new(secret, body, hashlib.sha256).hexdigest() != signature:
        raise SignatureError("bad signature")
    p = json.loads(body)
    existing = conn.execute("SELECT id FROM journals WHERE request_key = ?", (p["idempotency_key"],)).fetchone()
    if existing:
        return existing[0]
    scale = 100 if p["currency"] == "USD" else 1
    amount = int(round(float(p["amount"]) * scale))
    cur = conn.execute(
        "INSERT INTO journals (entity, book, period, currency, source, request_key, payload_hash, actor, version,"
        " evidence_ref, reference) VALUES (?, ?, ?, ?, 'receipt', ?, '', ?, ?, ?, ?)",
        (p["entity"], p["book"], p["value_date"][:7], p["currency"], p["idempotency_key"], actor, p.get("version", 1),
         p.get("evidence_ref", ""), p.get("receivable_ref")))
    journal_id = cur.lastrowid
    conn.execute("INSERT INTO journal_lines VALUES (?, 1, ?, ?, 0)", (journal_id, BANK_ACCOUNT, amount))
    conn.execute("INSERT INTO journal_lines VALUES (?, 2, ?, 0, ?)", (journal_id, RECEIVABLE_ACCOUNT, amount))
    conn.execute("INSERT INTO audit (event, journal_id, request_key, actor) VALUES ('receipt_posted', ?, ?, ?)",
                 (journal_id, p["idempotency_key"], actor))
    return journal_id


def reverse_receipt(conn: sqlite3.Connection, journal_id: int, *, actor: str, reason: str, evidence_ref: str) -> int:
    # A receipt posted in error is simply voided.
    conn.execute("DELETE FROM journal_lines WHERE journal_id = ?", (journal_id,))
    conn.execute("DELETE FROM journals WHERE id = ?", (journal_id,))
    conn.execute("INSERT INTO audit (event, journal_id, actor, detail) VALUES ('receipt_voided', ?, ?, ?)",
                 (journal_id, actor, reason))
    return journal_id
