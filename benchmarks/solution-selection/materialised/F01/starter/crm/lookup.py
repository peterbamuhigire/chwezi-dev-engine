"""Customer directory keyed by canonical identifier (existing caller)."""
from core.identifiers import canonical_id


class CustomerDirectory:
    def __init__(self) -> None:
        self._names: dict[str, str] = {}

    def add(self, customer_id: str, name: str) -> str:
        key = canonical_id(customer_id)
        self._names[key] = name
        return key

    def find(self, customer_id: str) -> str | None:
        return self._names.get(canonical_id(customer_id))
