import copy
import threading


class InMemoryStore:
    """Record store keyed by notification id."""

    def __init__(self):
        self._rows: dict[str, dict] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> dict | None:
        with self._lock:
            row = self._rows.get(key)
            return copy.deepcopy(row) if row is not None else None

    def put(self, key: str, **fields) -> dict:
        with self._lock:
            row = {"id": key, "state": "pending", "attempts": 0, "last_error": None, "provider_id": None}
            row.update(fields)
            self._rows[key] = row
            return copy.deepcopy(row)

    def update(self, key: str, **fields) -> dict:
        with self._lock:
            self._rows[key].update(fields)
            return copy.deepcopy(self._rows[key])
