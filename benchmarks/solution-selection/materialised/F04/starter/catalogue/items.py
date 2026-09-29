"""List and read catalogue items."""
from __future__ import annotations

from .query import QueryLayer


class ItemNotFound(LookupError):
    pass


def add_item(q: QueryLayer, name: str, category: str, price_minor: int) -> int:
    with q.transaction():
        cursor = q.execute("INSERT INTO items (name, category, price_minor) VALUES (?, ?, ?)", (name, category, price_minor))
    return int(cursor.lastrowid)


def list_items(q: QueryLayer, category: str | None = None) -> list[dict]:
    if category is None:
        return q.fetch_all("SELECT id, name, category, price_minor FROM items ORDER BY id")
    return q.fetch_all("SELECT id, name, category, price_minor FROM items WHERE category = ? ORDER BY id", (category,))


def read_item(q: QueryLayer, item_id: int) -> dict:
    row = q.fetch_one("SELECT id, name, category, price_minor FROM items WHERE id = ?", (item_id,))
    if row is None:
        raise ItemNotFound(item_id)
    return row
