"""Invoice references (existing caller of the identifier contract)."""
from core.identifiers import canonical_id


def invoice_reference(customer_id: str, number: int) -> str:
    return f"INV-{canonical_id(customer_id)}-{number:05d}"
