"""Internal queue consumer: messages arrive as already-decoded dicts."""
from __future__ import annotations

from service.contract import ORDER_SCHEMA
from vendor import schemalite


def consume(message, store) -> dict:
    errors = schemalite.validate(message, ORDER_SCHEMA)
    if errors:
        return {"status": "rejected", "error": {"code": "validation_failed", "details": errors}}
    store.save(message)
    return {"status": "accepted", "id": message["id"]}
