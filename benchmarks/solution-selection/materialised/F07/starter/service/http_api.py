"""Authenticated HTTP endpoint for creating orders (authentication happens upstream)."""
from __future__ import annotations

import json


def handle_create(body: bytes, store) -> tuple[int, dict]:
    """Return (HTTP status, JSON payload)."""
    try:
        order = json.loads(body)
    except ValueError:
        return 400, {"error": {"code": "malformed_json"}}
    store.save(order)
    return 201, {"id": order["id"]}
