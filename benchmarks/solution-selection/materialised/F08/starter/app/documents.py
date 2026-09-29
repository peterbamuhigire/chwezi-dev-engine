"""Document repository. Documents belong to exactly one tenant; IDs are global."""
from __future__ import annotations


class Repository:
    def __init__(self):
        self._docs: dict[str, dict] = {}

    def add(self, doc_id: str, tenant: str, title: str, body: str) -> None:
        self._docs[doc_id] = {"id": doc_id, "tenant": tenant, "title": title, "body": body}

    def get_global(self, doc_id: str):
        """Unscoped lookup for internal maintenance only."""
        return self._docs.get(doc_id)

    def get_for_tenant(self, tenant: str, doc_id: str):
        """Tenant-scoped lookup: another tenant's document looks exactly like a missing one."""
        doc = self._docs.get(doc_id)
        return doc if doc is not None and doc["tenant"] == tenant else None
