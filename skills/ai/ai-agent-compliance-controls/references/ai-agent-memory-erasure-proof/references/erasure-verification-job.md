# Erasure Verification Job — Engineering Reference

Full implementation of the 9-step agent-memory erasure cascade, the **independent** verification probes, and the signed proof-of-erasure pack writer.

---

## 1. Module Layout

```
privacy/erasure/
├── intake.py
├── cascade.py            # 9-step orchestrator
├── tiers/
│   ├── working.py
│   ├── episodic.py
│   ├── semantic.py
│   ├── vectors.py
│   ├── finetune.py
│   ├── uploads.py
│   ├── derivatives.py
│   ├── subprocessors.py
│   └── audit_log.py      # redact, not delete
├── probes/               # INDEPENDENT verification code path
│   ├── working.py
│   ├── episodic.py
│   ├── semantic.py
│   ├── vectors.py
│   ├── finetune.py
│   ├── uploads.py
│   ├── derivatives.py
│   ├── subprocessors.py
│   └── audit_log.py
├── verify.py
├── proof_pack.py
└── notify.py
```

`tiers/` is the deletion path; `probes/` is the verification path. Different developers maintain each (segregation-of-duties for code review).

## 2. Subject Fingerprint

```python
# privacy/erasure/fingerprint.py
import hashlib

def subject_fingerprint(req) -> dict[str, int]:
    """Count residue per tier BEFORE the cascade runs."""
    return {
        "working":     count_working(req),
        "episodic":    count_episodic(req),
        "semantic":    count_semantic(req),
        "vectors":     count_vectors(req),
        "fine_tune":   count_finetune_examples(req),
        "uploads":     count_uploads(req),
        "derivatives": count_derivatives(req),
        "subprocessor": count_at_subprocessors(req),
    }

def subject_hash(req) -> str:
    return hashlib.sha256(f"{req.tenant_id}:{req.subject_id}".encode()).hexdigest()
```

## 3. Cascade Orchestrator

```python
# privacy/erasure/cascade.py
from datetime import datetime
from privacy.erasure.fingerprint import subject_fingerprint
from privacy.erasure.tiers import working, episodic, semantic, vectors, finetune, uploads, derivatives, subprocessors, audit_log
from privacy.erasure.probes import (
    working   as probe_working,
    episodic  as probe_episodic,
    semantic  as probe_semantic,
    vectors   as probe_vectors,
    finetune  as probe_finetune,
    uploads   as probe_uploads,
    derivatives as probe_derivatives,
    subprocessors as probe_subprocessors,
    audit_log as probe_audit_log,
)
from audit.emit import emit

CASCADE = [
    ("working",      working.wipe,        probe_working.residue),
    ("episodic",     episodic.delete,     probe_episodic.residue),
    ("semantic",     semantic.delete,     probe_semantic.residue),
    ("vectors",      vectors.delete,      probe_vectors.residue),
    ("fine_tune",    finetune.purge,      probe_finetune.residue),
    ("uploads",      uploads.delete,      probe_uploads.residue),
    ("derivatives",  derivatives.delete,  probe_derivatives.residue),
    ("subprocessor", subprocessors.delete, probe_subprocessors.residue),
    ("audit_log",    audit_log.redact,    probe_audit_log.unredacted),  # redact-not-delete
]

def run_cascade(req) -> list[dict]:
    fp_before = subject_fingerprint(req)
    steps: list[dict] = []
    for name, deleter, prober in CASCADE:
        if name != "audit_log" and name not in req.data_classes:
            continue
        rec = {"step": name, "started_at": datetime.utcnow().isoformat(),
               "before": fp_before.get(name)}
        try:
            output = deleter(req)               # idempotent
            after = prober(req)                 # independent probe
            rec.update({"status": "ok", "after": after, "output": output})
        except Exception as e:
            rec.update({"status": "fail", "error": str(e)})
        rec["ended_at"] = datetime.utcnow().isoformat()
        steps.append(rec)
        emit(event_class="erasure_step", subject_id=req.subject_id,
             request_id=req.request_id, step=name, status=rec["status"],
             after=rec.get("after"))
    return steps
```

## 4. Per-Tier Deletion (excerpts)

```python
# privacy/erasure/tiers/episodic.py
def delete(req) -> dict:
    affected = db.execute("""
        DELETE FROM agent_episodic_memory
        WHERE tenant_id = %s AND subject_id = %s
        RETURNING id
    """, (req.tenant_id, req.subject_id)).rowcount
    # Wait for read-replica catchup so the verification probe is not racing.
    wait_replication_drained(table="agent_episodic_memory", timeout_seconds=60)
    return {"deleted_rows": affected}
```

```python
# privacy/erasure/tiers/vectors.py
def delete(req) -> dict:
    ids = vector_client.list_ids(filter={"tenant_id": req.tenant_id, "subject_id": req.subject_id})
    vector_client.delete(ids=ids)
    vector_client.compact_index()         # critical: ANN shards retain until compaction
    return {"deleted_vectors": len(ids)}
```

```python
# privacy/erasure/tiers/finetune.py
def purge(req) -> dict:
    examples = ft_dataset.delete_subject_examples(req.tenant_id, req.subject_id)
    affected_models = ft_dataset.models_trained_on(examples)
    retraining = []
    for model_id in affected_models:
        decision = decide_retain_or_retrain(model_id, req)
        if decision == "retrain":
            ft_provider.retrain(model_id, dataset=ft_dataset.current_version())
            retraining.append({"model_id": model_id, "action": "retrain"})
        else:
            # Document the lawful-retention basis (Art. 17(3))
            record_retention_basis(model_id, req, basis=decision)
            retraining.append({"model_id": model_id, "action": "retain", "basis": decision})
    return {"deleted_examples": len(examples), "affected_models": retraining}
```

```python
# privacy/erasure/tiers/subprocessors.py
def delete(req) -> dict:
    receipts = []
    for sp in subprocessor_inventory.for_subject(req):
        ticket = sp.client.delete_subject_data(
            tenant_id=req.tenant_id, subject_id=req.subject_id,
            request_id=req.request_id,
        )
        receipts.append({"subprocessor": sp.name, "ticket_id": ticket.id,
                         "confirmed_at": ticket.confirmed_at.isoformat()})
    return {"receipts": receipts}
```

```python
# privacy/erasure/tiers/audit_log.py
def redact(req) -> dict:
    """REDACT PII; do NOT delete rows. Chain integrity is preserved."""
    affected = db.execute("""
        UPDATE action_audit_log
        SET payload_summary = redact_pii(payload_summary, %s),
            redacted_for_request = %s,
            redacted_at = NOW()
        WHERE tenant_id = %s
          AND (payload_summary->>'subject_id' = %s
               OR EXISTS (SELECT 1 FROM subject_audit_index sai
                           WHERE sai.audit_id = action_audit_log.id
                             AND sai.subject_id = %s))
    """, (req.subject_id, req.request_id, req.tenant_id, req.subject_id, req.subject_id)).rowcount
    # The chain hashes are unchanged because they commit to a redacted summary already (see audit-log-integrity hash-chain-design).
    return {"rows_redacted": affected}
```

## 5. Independent Probes (excerpts)

The probes use **different client libraries and a fresh DB connection** to rule out caching / stale-reader effects.

```python
# privacy/erasure/probes/episodic.py
def residue(req) -> int:
    # Fresh connection, read replica disabled.
    with db.fresh_primary_conn() as c:
        return c.fetchone("""
            SELECT COUNT(*) AS n FROM agent_episodic_memory
            WHERE tenant_id = %s AND subject_id = %s
        """, (req.tenant_id, req.subject_id))["n"]
```

```python
# privacy/erasure/probes/vectors.py
def residue(req) -> int:
    # Use a separate vector-store client (different SDK, different keys) to avoid client-cache.
    client = make_independent_vector_client()
    ids = client.list_ids(filter={"tenant_id": req.tenant_id, "subject_id": req.subject_id})
    # Brute-force similarity check on a known seed sentence to catch shard residue.
    seed_vec = embedder.embed(canonical_seed(req))
    hits = client.search(seed_vec, top_k=50, filter={"tenant_id": req.tenant_id})
    leak_hits = [h for h in hits if h.metadata.get("subject_id") == req.subject_id]
    return len(ids) + len(leak_hits)
```

```python
# privacy/erasure/probes/subprocessors.py
def residue(req) -> int:
    n = 0
    for sp in subprocessor_inventory.for_subject(req):
        # Call the subprocessor's "list subject data" API (separate from delete).
        present = sp.client.subject_present(req.tenant_id, req.subject_id)
        if present:
            n += 1
    return n
```

```python
# privacy/erasure/probes/audit_log.py
def unredacted(req) -> int:
    return db.fetchone("""
        SELECT COUNT(*) AS n FROM action_audit_log
        WHERE tenant_id = %s
          AND payload_summary::text LIKE %s
          AND (redacted_for_request IS NULL OR redacted_for_request <> %s)
    """, (req.tenant_id, f"%{req.subject_id}%", req.request_id))["n"]
```

## 6. Verification

```python
# privacy/erasure/verify.py
from datetime import datetime
from privacy.erasure.probes import (
    working, episodic, semantic, vectors, finetune,
    uploads, derivatives, subprocessors, audit_log,
)

PROBES = {
    "working":     working.residue,
    "episodic":    episodic.residue,
    "semantic":    semantic.residue,
    "vectors":     vectors.residue,
    "fine_tune":   finetune.residue,
    "uploads":     uploads.residue,
    "derivatives": derivatives.residue,
    "subprocessor": subprocessors.residue,
}

def verify(req) -> dict:
    out = {"verified_at": datetime.utcnow().isoformat(), "probes": {}}
    for tier, fn in PROBES.items():
        if tier not in req.data_classes:
            out["probes"][tier] = {"skipped": True}
            continue
        residue = fn(req)
        out["probes"][tier] = {"residue": residue, "ok": residue == 0}
    audit_log_unredacted = audit_log.unredacted(req)
    out["probes"]["audit_log_redacted"] = {
        "unredacted_pii_count": audit_log_unredacted,
        "ok": audit_log_unredacted == 0,
    }
    out["all_clear"] = all(p.get("ok", True) for p in out["probes"].values())
    return out
```

## 7. Proof-of-Erasure Pack Writer

```python
# privacy/erasure/proof_pack.py
import json, hashlib, tarfile, io
from datetime import datetime
from crypto.sign import ed25519_sign
from audit.witness import chain_witness_around_redaction

def build_pack(req, steps, verification, dpo_signer: str) -> str:
    base = f"evidence/erasure/{req.request_id}/"
    files = {
        "request.json": json.dumps({
            "request_id": req.request_id,
            "tenant_id": req.tenant_id,
            "subject_id_hash": hashlib.sha256(req.subject_id.encode()).hexdigest(),
            "data_classes": req.data_classes,
            "legal_basis": req.legal_basis,
            "received_at": req.received_at.isoformat(),
            "sla_deadline": req.sla_deadline.isoformat(),
            "requester_identity_proof_ref": req.requester_identity_proof_ref,
        }).encode(),
        "steps.jsonl": _jsonl(steps),
        "verification.json": json.dumps(verification, default=str).encode(),
        "subprocessor-receipts.jsonl":
            _jsonl(_collect_receipts(steps)),
        "audit-log-redaction.json":
            json.dumps(chain_witness_around_redaction(req)).encode(),
    }
    manifest = {
        "pack_id": f"erasure-{req.request_id}",
        "request_id": req.request_id,
        "tenant_id": req.tenant_id,
        "legal_basis": req.legal_basis,
        "received_at": req.received_at.isoformat(),
        "completed_at": datetime.utcnow().isoformat(),
        "sla_deadline": req.sla_deadline.isoformat(),
        "all_clear": verification["all_clear"],
        "signer": dpo_signer,
        "signature_key_id": "compliance-dpo-2026",
        "files": [
            {"name": n, "sha256": hashlib.sha256(c).hexdigest(), "size": len(c)}
            for n, c in files.items()
        ],
    }
    manifest_bytes = json.dumps(manifest, sort_keys=True).encode()
    sig = ed25519_sign(manifest_bytes, key_id="compliance-dpo-2026")
    attestation = _attestation_text(manifest, dpo_signer)
    vault.upload(base, {**files, "manifest.json": manifest_bytes,
                        "attestation.txt": attestation.encode(),
                        "signature.sig": sig})
    return base

def _jsonl(rows): return ("\n".join(json.dumps(r, default=str) for r in rows)).encode()
```

The DPO **must not** be the engineer who ran the cascade. The signing key is locked behind hardware token + 2FA + on-call paging if used.

## 8. End-to-End Driver

```python
# privacy/erasure/run.py
from privacy.erasure.intake import accept
from privacy.erasure.cascade import run_cascade
from privacy.erasure.verify import verify
from privacy.erasure.proof_pack import build_pack
from privacy.erasure.notify import notify_requester

def handle(request: dict) -> str:
    req = accept(request)
    steps = run_cascade(req)
    result = verify(req)
    if not result["all_clear"]:
        open_exception(
            control_id="C1.2",
            severity="critical",
            title=f"Erasure verification failed: request {req.request_id}",
            evidence_ref=f"erasure/{req.request_id}",
            detail=result,
        )
        return ""        # do NOT notify requester until clear
    pack_uri = build_pack(req, steps, result, dpo_signer=DPO_EMAIL)
    notify_requester(req, pack_uri)
    return pack_uri
```

## 9. Tests

```python
def test_idempotent_cascade(seed_subject):
    req = seed_subject(id="sub1", tier_rows={"episodic": 50, "vectors": 200})
    handle(serialize(req))
    # Re-run should produce same all_clear with after=0 across the board.
    handle(serialize(req))
    last = load_pack(req.request_id, "verification.json")
    assert last["all_clear"] is True

def test_vector_shard_residue_caught_by_independent_probe(seed_subject, leak_vector):
    req = seed_subject(id="sub1", tier_rows={"vectors": 100})
    leak_vector(req, count=1)   # simulate ANN shard residue
    out = handle(serialize(req))
    assert out == ""             # not delivered
    assert exceptions.last().severity == "critical"

def test_audit_log_redacted_not_deleted(seed_subject):
    req = seed_subject(id="sub1", audit_rows=20)
    handle(serialize(req))
    n_rows = db.fetchone("SELECT COUNT(*) AS n FROM action_audit_log WHERE subject_audit_index_for(%s)", (req.subject_id,))["n"]
    assert n_rows == 20          # rows preserved
    n_unredacted = probes_audit_log.unredacted(req)
    assert n_unredacted == 0     # PII gone

def test_finetune_model_lineage_decision_recorded(seed_subject):
    req = seed_subject(id="sub1", finetune_examples=5, models=["mdl-a"])
    handle(serialize(req))
    decisions = load_pack(req.request_id, "steps.jsonl")
    ft_step = next(s for s in decisions if s["step"] == "fine_tune")
    assert ft_step["output"]["affected_models"][0]["action"] in ("retrain","retain")
```

## 10. Operational Notes

- **Always wait for replication** between delete and probe (60s timeout configurable). A race produces false negatives.
- **Subprocessor list** is part of the DPA; out-of-date inventory is itself an audit finding.
- **Vector index compaction** is the most common residue source — force it; do not rely on lazy compaction.
- **Fine-tune lineage** is recorded in `model_lineage` table; the decision (retrain vs retain with documented basis) is itself evidence.
- **DPO signing key** rotates annually; old proofs remain valid (verification uses the key id recorded in the manifest).
- The proof pack is referenced from the **erasure response email** to the requester; without the pack, do not send the response.
- Re-running the cascade after a partial failure is **safe**; each step is idempotent and the proof reflects the final verified state.
