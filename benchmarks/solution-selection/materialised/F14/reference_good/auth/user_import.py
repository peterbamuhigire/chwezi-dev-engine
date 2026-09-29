"""Bulk user import from CSV (header: username,display_name,role), parsed with the stdlib csv module."""
from __future__ import annotations

import csv
import io

EXPECTED_HEADER = ["username", "display_name", "role"]
ROLES = {"viewer", "exporter", "admin"}


def _problems(record: list[str]) -> list[str]:
    if len(record) != len(EXPECTED_HEADER):
        return [f"expected {len(EXPECTED_HEADER)} fields, got {len(record)}"]
    problems = [] if record[0].strip() else ["username is empty"]
    if record[2] not in ROLES:
        problems.append(f"unknown role {record[2]!r}")
    return problems


def import_users(text: str):
    """Return (rows, errors); each error carries the line on which its record starts."""
    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    try:
        if next(reader) != EXPECTED_HEADER:
            return [], [{"line": 1, "message": f"header must be {EXPECTED_HEADER}"}]
    except (StopIteration, csv.Error) as exc:
        return [], [{"line": 1, "message": str(exc) or "empty file"}]
    rows, errors = [], []
    while True:
        line = reader.line_num + 1
        try:
            record = next(reader)
        except StopIteration:
            break
        except csv.Error as exc:
            errors.append({"line": line, "message": str(exc)})
            break
        problems = _problems(record)
        if problems:
            errors.append({"line": line, "message": "; ".join(problems)})
        else:
            rows.append({"username": record[0].strip().lower(), "display_name": record[1], "role": record[2]})
    return rows, errors
