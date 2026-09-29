"""Bulk user import from CSV (header: username,display_name,role)."""
from __future__ import annotations

import csv
import io

EXPECTED_HEADER = ["username", "display_name", "role"]
ROLES = {"viewer", "exporter", "admin"}


class _RowValidator:
    def __init__(self, roles):
        self.roles = roles

    def validate(self, record):
        problems = []
        if len(record) != len(EXPECTED_HEADER):
            problems.append(f"expected {len(EXPECTED_HEADER)} fields, got {len(record)}")
            return problems
        if not record[0].strip():
            problems.append("username is empty")
        if record[2] not in self.roles:
            problems.append(f"unknown role {record[2]!r}")
        return problems


class _ImportRunner:
    def __init__(self, validator):
        self.validator = validator

    def run(self, text):
        rows, errors = [], []
        reader = csv.reader(io.StringIO(text, newline=""), strict=True)
        try:
            header = next(reader)
        except StopIteration:
            return rows, [{"line": 1, "message": "empty file"}]
        except csv.Error as exc:
            return rows, [{"line": 1, "message": str(exc)}]
        if header != EXPECTED_HEADER:
            return rows, [{"line": 1, "message": f"header must be {EXPECTED_HEADER}"}]
        while True:
            line = reader.line_num + 1
            try:
                record = next(reader)
            except StopIteration:
                break
            except csv.Error as exc:
                errors.append({"line": line, "message": str(exc)})
                break
            problems = self.validator.validate(record)
            if problems:
                errors.append({"line": line, "message": "; ".join(problems)})
            else:
                rows.append({"username": record[0].strip().lower(), "display_name": record[1], "role": record[2]})
        return rows, errors


def import_users(text: str):
    """Return (rows, errors); each error carries the line on which its record starts."""
    return _ImportRunner(_RowValidator(ROLES)).run(text)
