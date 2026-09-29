"""Boundary contract for order creation (see docs/CONTRACT.md)."""

MAX_BODY_BYTES = 16_384

ITEM_SCHEMA = {
    "type": "object",
    "required": ["sku", "qty"],
    "fields": {
        "sku": {"type": "string", "pattern": r"[A-Z0-9]{2,12}"},
        "qty": {"type": "integer", "minimum": 1, "maximum": 999},
    },
}

ORDER_SCHEMA = {
    "type": "object",
    "required": ["id", "customer", "items"],
    "fields": {
        "id": {"type": "string", "pattern": r"[A-Za-z0-9_-]{1,32}"},
        "customer": {"type": "string", "min_length": 1, "max_length": 80},
        "items": {"type": "array", "items": ITEM_SCHEMA, "min_items": 1, "max_items": 50},
        "note": {"type": "string", "max_length": 500, "nullable": True},
    },
}
