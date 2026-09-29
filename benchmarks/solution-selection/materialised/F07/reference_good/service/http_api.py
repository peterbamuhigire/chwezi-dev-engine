"""Authenticated HTTP endpoint for creating orders (authentication happens upstream).

Applies the same boundary contract as the queue (docs/CONTRACT.md): size limit before parsing,
strict JSON (no duplicate keys), schema validation of the whole order before any write.
"""
from __future__ import annotations

import json

from service.contract import MAX_BODY_BYTES, ORDER_SCHEMA
from vendor import schemalite


class _DuplicateKey(ValueError):
    pass


def _no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def _error(status: int, code: str, details=None) -> tuple[int, dict]:
    return status, {"error": {"code": code, "details": details or []}}


def handle_create(body: bytes, store) -> tuple[int, dict]:
    if not isinstance(body, (bytes, bytearray)) or len(body) > MAX_BODY_BYTES:
        return _error(413, "body_too_large")
    try:
        order = json.loads(bytes(body).decode("utf-8"), object_pairs_hook=_no_duplicates)
    except (UnicodeDecodeError, ValueError):
        return _error(400, "malformed_json")
    errors = schemalite.validate(order, ORDER_SCHEMA)
    if errors:
        return _error(422, "validation_failed", errors)
    store.save(order)
    return 201, {"id": order["id"]}
