"""Users of the catalogue."""
from __future__ import annotations

from .query import QueryLayer


class UnknownUser(LookupError):
    pass


def create_user(q: QueryLayer, email: str) -> int:
    with q.transaction():
        cursor = q.execute("INSERT INTO users (email) VALUES (?)", (email,))
    return int(cursor.lastrowid)


def delete_user(q: QueryLayer, user_id: int) -> None:
    with q.transaction():
        cursor = q.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if cursor.rowcount == 0:
            raise UnknownUser(user_id)
