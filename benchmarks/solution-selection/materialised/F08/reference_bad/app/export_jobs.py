"""Document export: enqueue on request, run later in the worker.

Exports require the ``exporter`` role.
"""
from __future__ import annotations

from app.auth import authenticate
from app.errors import Denied


def enqueue_export(ctx, token, doc_id: str) -> str:
    claims = authenticate(ctx, token)
    if "exporter" not in claims.get("roles", []):
        ctx.audit.append({"event": "export_denied", "token": token, "doc_id": doc_id})
        raise Denied("forbidden")
    doc = ctx.repo.get_global(doc_id)
    if doc is None:
        ctx.audit.append({"event": "export_denied", "token": token, "doc_id": doc_id})
        raise Denied("not_found")
    if doc["tenant"] != claims["tenant"]:
        ctx.audit.append({"event": "export_denied", "token": token, "doc_id": doc_id})
        raise Denied("forbidden")
    job_id = f"job-{len(ctx.jobs) + 1}"
    ctx.jobs[job_id] = {"doc_id": doc_id, "sub": claims["sub"], "status": "queued"}
    return job_id


def run_export(ctx, job_id: str) -> str:
    """Worker entry point. The job was authorised at enqueue time."""
    job = ctx.jobs[job_id]
    doc = ctx.repo.get_global(job["doc_id"])
    ctx.exports[job_id] = f"{doc['title']}\n{doc['body']}"
    job["status"] = "done"
    return job["status"]
