"""Bulk user import from CSV (header: username,display_name,role)."""
from __future__ import annotations

ROLES = {"viewer", "exporter", "admin"}


def import_users(text: str):
    rows, errors = [], []
    lines = text.strip().splitlines()
    for number, line in enumerate(lines[1:], start=2):
        parts = [p.strip().strip('"') for p in line.split(",")]
        if len(parts) < 3 or parts[2] not in ROLES:
            errors.append({"line": number, "message": "bad row"})
            continue
        rows.append({"username": parts[0].lower(), "display_name": parts[1], "role": parts[2]})
    return rows, errors
