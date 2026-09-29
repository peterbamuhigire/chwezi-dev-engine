"""File-backed order store. Each order is written as a header file plus one line file."""
from __future__ import annotations

import json
from pathlib import Path


class Store:
    def __init__(self, root):
        self.root = Path(root)
        (self.root / "orders").mkdir(parents=True, exist_ok=True)

    def save(self, order: dict) -> None:
        folder = self.root / "orders"
        header = {"id": order["id"], "customer": order["customer"], "note": order.get("note")}
        (folder / f"{order['id']}.json").write_text(json.dumps(header), encoding="utf-8")
        lines = [f"{item['sku']},{item['qty']}" for item in order["items"]]
        (folder / f"{order['id']}.lines").write_text("\n".join(lines), encoding="utf-8")

    def load(self, order_id: str):
        path = self.root / "orders" / f"{order_id}.json"
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None

    def count(self) -> int:
        return len(list((self.root / "orders").glob("*.json")))
