"""Tenant-scoped read API (the established pattern)."""
from __future__ import annotations

from app.auth import authenticate
from app.errors import Denied


def read_document(ctx, token, doc_id: str) -> dict:
    claims = authenticate(ctx, token)
    if "reader" not in claims.get("roles", []) and "exporter" not in claims.get("roles", []):
        ctx.audit.append({"event": "read_denied", "sub": claims.get("sub"), "doc_id": doc_id, "reason": "forbidden"})
        raise Denied("forbidden")
    doc = ctx.repo.get_for_tenant(claims["tenant"], doc_id)
    if doc is None:
        ctx.audit.append({"event": "read_denied", "sub": claims.get("sub"), "doc_id": doc_id, "reason": "not_found"})
        raise Denied("not_found")
    return {"id": doc["id"], "title": doc["title"], "body": doc["body"]}
