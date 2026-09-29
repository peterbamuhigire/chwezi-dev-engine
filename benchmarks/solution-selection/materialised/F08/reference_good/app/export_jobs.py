"""Document export: enqueue on request, run later in the worker.

Exports require the ``exporter`` role. Authorisation is checked at enqueue AND again at execution
time against the identity provider's current state, because roles can be revoked between the two.
Lookups are tenant-scoped, so another tenant's document is indistinguishable from a missing one.
Audit entries never contain tokens or key material.
"""
from __future__ import annotations

from app.auth import authenticate
from app.errors import Denied

EXPORT_ROLE = "exporter"


def _deny(ctx, event: str, sub, doc_id, code: str) -> None:
    ctx.audit.append({"event": event, "sub": sub, "doc_id": doc_id, "reason": code})


def enqueue_export(ctx, token, doc_id: str) -> str:
    claims = authenticate(ctx, token)
    sub, tenant = claims.get("sub"), claims.get("tenant")
    current = ctx.idp.current_roles(sub)
    if EXPORT_ROLE not in claims.get("roles", []) or EXPORT_ROLE not in current or ctx.idp.current_tenant(sub) != tenant:
        _deny(ctx, "export_denied", sub, doc_id, "forbidden")
        raise Denied("forbidden")
    doc = ctx.repo.get_for_tenant(tenant, doc_id)
    if doc is None:
        _deny(ctx, "export_denied", sub, doc_id, "not_found")
        raise Denied("not_found")
    job_id = f"job-{len(ctx.jobs) + 1}"
    ctx.jobs[job_id] = {"doc_id": doc_id, "sub": sub, "tenant": tenant, "status": "queued"}
    return job_id


def run_export(ctx, job_id: str) -> str:
    """Worker entry point. Re-authorises against current state; returns the final job status."""
    job = ctx.jobs.get(job_id)
    if job is None:
        return "missing"
    sub, tenant = job["sub"], job["tenant"]
    if EXPORT_ROLE not in ctx.idp.current_roles(sub) or ctx.idp.current_tenant(sub) != tenant:
        job["status"] = "denied"
        _deny(ctx, "export_run_denied", sub, job["doc_id"], "forbidden")
        return job["status"]
    doc = ctx.repo.get_for_tenant(tenant, job["doc_id"])
    if doc is None:
        job["status"] = "denied"
        _deny(ctx, "export_run_denied", sub, job["doc_id"], "not_found")
        return job["status"]
    ctx.exports[job_id] = f"{doc['title']}\n{doc['body']}"
    job["status"] = "done"
    return job["status"]
