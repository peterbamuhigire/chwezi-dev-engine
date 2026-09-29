"""Saved filters for the catalogue (quick version: cached on the query layer for now)."""
from __future__ import annotations


class InvalidFilter(ValueError):
    pass


class DuplicateFilter(Exception):
    pass


class FilterNotFound(LookupError):
    pass


def _store(q) -> dict:
    if not hasattr(q, "_saved_filters"):
        q._saved_filters = {}
    return q._saved_filters


def create_filter(q, user_id, name, spec):
    if not isinstance(spec, dict):
        raise InvalidFilter("spec must be an object")
    store = _store(q)
    for existing in store.values():
        if existing["user_id"] == user_id and existing["name"] == name:
            return existing
    record = {"id": len(store) + 1, "user_id": user_id, "name": name, "spec": dict(spec)}
    store[record["id"]] = record
    return record


def list_filters(q, user_id):
    return [f for f in _store(q).values() if f["user_id"] == user_id]


def get_filter(q, user_id, filter_id):
    store = _store(q)
    if filter_id not in store:
        raise FilterNotFound(filter_id)
    return store[filter_id]


def delete_filter(q, user_id, filter_id):
    if _store(q).pop(filter_id, None) is None:
        raise FilterNotFound(filter_id)
