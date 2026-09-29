"""schemalite 1.4.2 (installed, pinned) - small declarative validator for JSON-like data.

Synthetic fixture library written for this benchmark. Schemas are plain dicts:
    {"type": "object", "fields": {...}, "required": [...], "allow_unknown": False}
    {"type": "array", "items": <schema>, "min_items": 1, "max_items": 50}
    {"type": "string", "pattern": r"...", "min_length": 1, "max_length": 64}
    {"type": "integer", "minimum": 1, "maximum": 999}   # bool is never an integer
    {"type": "boolean"}
``validate(value, schema)`` returns a list of error strings (empty when valid). ``None`` is only
accepted when the schema says ``"nullable": True``.
"""
from __future__ import annotations

import re
from typing import Any


def _at(path: str, message: str) -> str:
    return f"{path or '$'}: {message}"


def validate(value: Any, schema: dict, path: str = "") -> list[str]:
    if value is None:
        return [] if schema.get("nullable") else [_at(path, "must not be null")]
    kind = schema.get("type")
    errors: list[str] = []
    if kind == "object":
        if not isinstance(value, dict):
            return [_at(path, "must be an object")]
        fields = schema.get("fields", {})
        for name in schema.get("required", []):
            if name not in value:
                errors.append(_at(f"{path}.{name}", "is required"))
        for name, item in value.items():
            if name in fields:
                errors.extend(validate(item, fields[name], f"{path}.{name}"))
            elif not schema.get("allow_unknown", False):
                errors.append(_at(f"{path}.{name}", "is not an allowed field"))
    elif kind == "array":
        if not isinstance(value, list):
            return [_at(path, "must be an array")]
        if len(value) < schema.get("min_items", 0):
            errors.append(_at(path, "has too few items"))
        if len(value) > schema.get("max_items", 10**9):
            errors.append(_at(path, "has too many items"))
        for index, item in enumerate(value):
            errors.extend(validate(item, schema["items"], f"{path}[{index}]"))
    elif kind == "string":
        if not isinstance(value, str):
            return [_at(path, "must be a string")]
        if len(value) < schema.get("min_length", 0) or len(value) > schema.get("max_length", 10**9):
            errors.append(_at(path, "has an invalid length"))
        pattern = schema.get("pattern")
        if pattern and not re.fullmatch(pattern, value):
            errors.append(_at(path, "has an invalid format"))
    elif kind == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            return [_at(path, "must be an integer")]
        if value < schema.get("minimum", -(10**18)) or value > schema.get("maximum", 10**18):
            errors.append(_at(path, "is out of range"))
    elif kind == "boolean":
        if not isinstance(value, bool):
            return [_at(path, "must be a boolean")]
    else:
        errors.append(_at(path, f"unknown schema type {kind!r}"))
    return errors
