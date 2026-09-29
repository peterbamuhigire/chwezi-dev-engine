"""The catalogue's query layer: every read and write goes through this class."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Any, Iterator


class QueryLayer:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self._depth = 0

    def execute(self, sql: str, params: tuple | list = ()) -> sqlite3.Cursor:
        """Run one statement. Outside a transaction it commits immediately."""
        return self._conn.execute(sql, params)

    def fetch_all(self, sql: str, params: tuple | list = ()) -> list[dict[str, Any]]:
        return [dict(row) for row in self._conn.execute(sql, params).fetchall()]

    def fetch_one(self, sql: str, params: tuple | list = ()) -> dict[str, Any] | None:
        row = self._conn.execute(sql, params).fetchone()
        return dict(row) if row is not None else None

    @contextmanager
    def transaction(self) -> Iterator["QueryLayer"]:
        """All-or-nothing unit of work; nested calls join the outer transaction."""
        if self._depth:
            self._depth += 1
            try:
                yield self
            finally:
                self._depth -= 1
            return
        self._conn.execute("BEGIN IMMEDIATE")
        self._depth = 1
        try:
            yield self
        except BaseException:
            self._conn.execute("ROLLBACK")
            raise
        else:
            self._conn.execute("COMMIT")
        finally:
            self._depth = 0
