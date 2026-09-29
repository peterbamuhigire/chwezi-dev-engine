"""Authenticated HTTP endpoint for creating orders (authentication happens upstream)."""
from __future__ import annotations

import json


def handle_create(body: bytes, store) -> tuple[int, dict]:
    try:
        order = json.loads(body)
    except ValueError:
        return 400, {"error": {"code": "malformed_json"}}
    # Quick checks for the required fields.
    if not isinstance(order, dict):
        return 422, {"error": {"code": "validation_failed"}}
    for field in ("id", "customer", "items"):
        if field not in order:
            return 422, {"error": {"code": "validation_failed", "details": [f"{field} is required"]}}
    if not isinstance(order["items"], list) or not order["items"]:
        return 422, {"error": {"code": "validation_failed"}}
    for item in order["items"]:
        if not isinstance(item.get("qty"), int) or item["qty"] < 1:
            return 422, {"error": {"code": "invalid_qty"}}
    store.save(order)
    return 201, {"id": order["id"]}
