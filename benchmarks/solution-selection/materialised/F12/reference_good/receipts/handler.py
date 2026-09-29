"""Receipt callbacks from the simulated payment provider.

Controls kept on purpose (never simplified away): signature over the raw body, idempotency by key
with payload comparison, one transaction for header, lines and audit, the posting-service checks
(open period, authorised actor, evidence, balance), and correction by linked reversal only.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import sqlite3

from ledger import posting_service
from ledger.money import to_minor
from receipts.errors import IdempotencyConflict, InvalidReceipt, SignatureError

BANK_ACCOUNT = "1000"
RECEIVABLE_ACCOUNT = "1100"
REQUIRED_FIELDS = ("idempotency_key", "entity", "book", "value_date", "currency", "amount",
                   "receivable_ref", "evidence_ref", "version")


def _verify_signature(body: bytes, signature: str, secret: bytes) -> None:
    if not isinstance(body, (bytes, bytearray)) or not isinstance(signature, str) or not signature:
        raise SignatureError("missing body or signature")
    expected = hmac.new(secret, bytes(body), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature.strip().lower()):
        raise SignatureError("signature does not match the raw body")


def _parse(body: bytes) -> dict:
    try:
        payload = json.loads(body)
    except (ValueError, UnicodeDecodeError) as exc:
        raise InvalidReceipt("body is not JSON") from exc
    if not isinstance(payload, dict):
        raise InvalidReceipt("body must be a JSON object")
    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        raise InvalidReceipt(f"missing fields: {missing}")
    if not isinstance(payload["version"], int) or isinstance(payload["version"], bool):
        raise InvalidReceipt("version must be an integer")
    for field in ("idempotency_key", "entity", "book", "value_date", "currency", "amount", "receivable_ref"):
        if not isinstance(payload[field], str) or not payload[field].strip():
            raise InvalidReceipt(f"{field} must be a non-empty string")
    return payload


def _hash(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _rollback(conn: sqlite3.Connection) -> None:
    if conn.in_transaction:
        conn.execute("ROLLBACK")


def process_receipt(conn: sqlite3.Connection, body: bytes, signature: str, *, secret: bytes, actor: str) -> int:
    _verify_signature(body, signature, secret)
    payload = _parse(body)
    try:
        amount = to_minor(payload["amount"], payload["currency"])
        period = posting_service.period_of(payload["value_date"])
    except (TypeError, ValueError) as exc:
        raise InvalidReceipt(str(exc)) from exc
    if amount <= 0:
        raise InvalidReceipt("a receipt amount must be positive")
    key = payload["idempotency_key"]
    payload_hash = _hash(payload)
    header = {"entity": payload["entity"], "book": payload["book"], "period": period, "currency": payload["currency"],
              "source": "receipt-callback", "request_key": key, "payload_hash": payload_hash, "actor": actor,
              "version": payload["version"], "evidence_ref": payload["evidence_ref"],
              "reference": payload["receivable_ref"], "reversal_of": None}
    lines = [(BANK_ACCOUNT, amount, 0), (RECEIVABLE_ACCOUNT, 0, amount)]

    conn.execute("BEGIN IMMEDIATE")
    try:
        existing = conn.execute("SELECT id, payload_hash FROM journals WHERE entity = ? AND book = ? AND request_key = ?",
                                (header["entity"], header["book"], key)).fetchone()
        if existing is not None:
            if existing[1] == payload_hash:
                conn.execute("COMMIT")
                return existing[0]
            posting_service.record_audit(conn, "idempotency_conflict", journal_id=existing[0], request_key=key, actor=actor,
                                         detail=f"payload {payload_hash} differs from original {existing[1]}")
            conn.execute("COMMIT")
            raise IdempotencyConflict(f"idempotency key {key!r} was used with a different payload")
        posting_service.validate(conn, header, lines)
        journal_id = posting_service.insert_journal(conn, header, lines)
        conn.execute("COMMIT")
        return journal_id
    except IdempotencyConflict:
        raise
    except BaseException:
        _rollback(conn)
        raise


def reverse_receipt(conn: sqlite3.Connection, journal_id: int, *, actor: str, reason: str, evidence_ref: str) -> int:
    """Post a linked reversal; the original journal, its lines and its audit rows stay untouched."""
    if not str(reason or "").strip():
        raise InvalidReceipt("a reversal needs a reason")
    conn.execute("BEGIN IMMEDIATE")
    try:
        original = conn.execute("SELECT entity, book, period, currency, version, reference, reversal_of FROM journals WHERE id = ?",
                                (journal_id,)).fetchone()
        if original is None:
            raise InvalidReceipt(f"journal {journal_id} does not exist")
        entity, book, period, currency, version, reference, reversal_of = original
        if reversal_of is not None:
            raise InvalidReceipt("a reversal cannot itself be reversed; post a new receipt instead")
        if conn.execute("SELECT 1 FROM journals WHERE reversal_of = ?", (journal_id,)).fetchone():
            raise InvalidReceipt(f"journal {journal_id} is already reversed")
        lines = [(account, cr, dr) for account, dr, cr in conn.execute(
            "SELECT account, debit_minor, credit_minor FROM journal_lines WHERE journal_id = ? ORDER BY line_no", (journal_id,))]
        header = {"entity": entity, "book": book, "period": period, "currency": currency, "source": "receipt-reversal",
                  "request_key": f"reversal:{journal_id}", "payload_hash": hashlib.sha256(reason.encode("utf-8")).hexdigest(),
                  "actor": actor, "version": version, "evidence_ref": evidence_ref, "reference": reference,
                  "reversal_of": journal_id}
        posting_service.validate(conn, header, lines)
        reversal_id = posting_service.insert_journal(conn, header, lines)
        posting_service.record_audit(conn, "receipt_reversed", journal_id=journal_id, request_key=header["request_key"],
                                     actor=actor, detail=f"reversed by journal {reversal_id}: {reason}")
        conn.execute("COMMIT")
        return reversal_id
    except BaseException:
        _rollback(conn)
        raise
