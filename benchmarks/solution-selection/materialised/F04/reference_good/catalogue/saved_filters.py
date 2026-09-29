"""Persistent, per-user saved filters stored through the catalogue query layer."""
from __future__ import annotations

import json
from typing import Any

from .query import QueryLayer
from .users import UnknownUser

MAX_NAME = 80
MAX_TEXT = 200
_STRING_KEYS = {"category", "text"}
_PRICE_KEYS = {"min_price", "max_price"}


class InvalidFilter(ValueError):
    pass


class DuplicateFilter(Exception):
    pass


class FilterNotFound(LookupError):
    pass


def _canonical_spec(name: Any, spec: Any) -> str:
    if not isinstance(name, str) or not name.strip() or len(name) > MAX_NAME:
        raise InvalidFilter("name must be a non-empty string of at most 80 characters")
    if not isinstance(spec, dict) or not spec:
        raise InvalidFilter("spec must be a non-empty object")
    unknown = set(spec) - _STRING_KEYS - _PRICE_KEYS
    if unknown:
        raise InvalidFilter(f"unknown filter keys: {sorted(unknown)}")
    for key, value in spec.items():
        if key in _STRING_KEYS:
            if not isinstance(value, str) or not value.strip() or len(value) > MAX_TEXT:
                raise InvalidFilter(f"{key} must be a non-empty string")
        elif isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise InvalidFilter(f"{key} must be a non-negative integer in minor units")
    if "min_price" in spec and "max_price" in spec and spec["min_price"] > spec["max_price"]:
        raise InvalidFilter("min_price must not exceed max_price")
    return json.dumps(spec, sort_keys=True, separators=(",", ":"))


def _record(row: dict) -> dict:
    return {"id": row["id"], "user_id": row["user_id"], "name": row["name"], "spec": json.loads(row["spec_json"])}


def create_filter(q: QueryLayer, user_id: int, name: str, spec: dict) -> dict:
    canonical = _canonical_spec(name, spec)
    with q.transaction():
        if q.fetch_one("SELECT id FROM users WHERE id = ?", (user_id,)) is None:
            raise UnknownUser(user_id)
        q.execute(
            "INSERT INTO saved_filters (user_id, name, spec_json) VALUES (?, ?, ?) ON CONFLICT (user_id, name) DO NOTHING",
            (user_id, name, canonical),
        )
        row = q.fetch_one("SELECT id, user_id, name, spec_json FROM saved_filters WHERE user_id = ? AND name = ?", (user_id, name))
        if row is None or row["spec_json"] != canonical:
            raise DuplicateFilter(f"a different filter named {name!r} already exists")
    return _record(row)


def list_filters(q: QueryLayer, user_id: int) -> list[dict]:
    rows = q.fetch_all("SELECT id, user_id, name, spec_json FROM saved_filters WHERE user_id = ? ORDER BY id", (user_id,))
    return [_record(row) for row in rows]


def get_filter(q: QueryLayer, user_id: int, filter_id: int) -> dict:
    row = q.fetch_one("SELECT id, user_id, name, spec_json FROM saved_filters WHERE id = ? AND user_id = ?", (filter_id, user_id))
    if row is None:
        raise FilterNotFound(filter_id)
    return _record(row)


def delete_filter(q: QueryLayer, user_id: int, filter_id: int) -> None:
    with q.transaction():
        cursor = q.execute("DELETE FROM saved_filters WHERE id = ? AND user_id = ?", (filter_id, user_id))
        if cursor.rowcount == 0:
            raise FilterNotFound(filter_id)
