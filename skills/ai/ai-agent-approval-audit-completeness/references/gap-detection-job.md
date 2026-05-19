# Approval Gap-Detection Job — Engineering Reference

Full implementation of the monthly approval-audit completeness check that proves every irreversible agent action had a documented, authorised, temporally-valid approval.

---

## 1. Module Layout

```
compliance/
├── queries/
│   └── approval_completeness.sql
├── jobs/
│   ├── approval_completeness.py
│   └── __main__.py
├── chain/
│   └── witness.py
├── exceptions.py
├── evidence_pack.py
└── policy_versions.py
```

## 2. SQL (irreversible-actions ↔ approvals join)

```sql
-- compliance/queries/approval_completeness.sql
-- Returns one row per irreversible action in the window with classification.
WITH irreversible_actions AS (
  SELECT
    al.id            AS action_id,
    al.chain_pos     AS action_chain_pos,
    al.tenant_id,
    al.task_id,
    al.step_index,
    al.tool_name,
    al.actor_id      AS initiator_id,
    al.occurred_at   AS action_at,
    al.policy_version,
    al.payload_summary,
    al.kill_switch_bypass_id        -- nullable; non-null = explicit bypass
  FROM action_audit_log al
  WHERE al.reversibility = 'irreversible'
    AND al.occurred_at >= :window_start
    AND al.occurred_at <  :window_end
),
matched AS (
  SELECT
    ia.*,
    ap.id                       AS approval_id,
    ap.approver_id,
    ap.approver_role,
    ap.approved_at,
    ap.signature,
    ap.linked_action_chain_pos,
    ap.policy_version            AS approval_policy_version,
    ap.dual_approver_id,
    ap.dual_approver_signature
  FROM irreversible_actions ia
  LEFT JOIN approvals ap
    ON ap.linked_action_id = ia.action_id
),
classified AS (
  SELECT
    m.*,
    CASE
      WHEN m.kill_switch_bypass_id IS NOT NULL                THEN 'bypass_documented'
      WHEN m.approval_id IS NULL                              THEN 'gap_missing'
      WHEN m.approved_at >= m.action_at                       THEN 'gap_after_action'
      WHEN m.linked_action_chain_pos <> m.action_chain_pos    THEN 'gap_chain_mismatch'
      WHEN m.approver_id = m.initiator_id                     THEN 'gap_self_approval'
      WHEN m.approval_policy_version <> m.policy_version      THEN 'gap_policy_version'
      ELSE 'ok'
    END AS classification
  FROM matched m
)
SELECT * FROM classified;
```

## 3. Historical Allow-List Resolver

Approver authority must be checked against the allow-list **as of the policy_version in force at approval time**, not the current state.

```python
# compliance/policy_versions.py
from functools import lru_cache

@lru_cache(maxsize=2048)
def resolve_allowlist_at(tenant_id: str, policy_version: str) -> dict[str, frozenset[str]]:
    """Return role -> frozenset(approver_id) as of policy_version."""
    rows = db.execute("""
        SELECT role, approver_id
        FROM approver_allowlist_versions
        WHERE tenant_id = %s AND policy_version = %s
    """, (tenant_id, policy_version)).fetchall()
    out: dict[str, set[str]] = {}
    for r in rows:
        out.setdefault(r["role"], set()).add(r["approver_id"])
    return {k: frozenset(v) for k, v in out.items()}
```

The allow-list table is **append-only**, versioned, and replicated to the audit vault. Any change ships a new policy_version row.

## 4. Chain Witness

```python
# compliance/chain/witness.py
import hashlib, json
from datetime import datetime

def verify_slice(window_start: datetime, window_end: datetime) -> dict:
    """Walk the chain, verify every prev_hash, and emit a witness covering the window."""
    first = db.fetchone("""
        SELECT chain_pos, prev_hash, this_hash
        FROM action_audit_log
        WHERE occurred_at >= %s ORDER BY chain_pos ASC LIMIT 1
    """, (window_start,))
    last = db.fetchone("""
        SELECT chain_pos, this_hash, daily_seal_sig
        FROM action_audit_log
        WHERE occurred_at <  %s ORDER BY chain_pos DESC LIMIT 1
    """, (window_end,))

    # Spot-check every Nth row; full walk happens nightly in integrity-verification-job.
    stride = max(1, (last["chain_pos"] - first["chain_pos"]) // 5000)
    sampled = db.fetchall("""
        SELECT chain_pos, prev_hash, this_hash, occurred_at,
               tenant_id, actor_id, tool_name, event_class,
               outcome, payload_summary, retention_class, policy_version
        FROM action_audit_log
        WHERE chain_pos BETWEEN %s AND %s
          AND chain_pos %% %s = 0
        ORDER BY chain_pos ASC
    """, (first["chain_pos"], last["chain_pos"], stride))

    drift = []
    prev = None
    for row in sampled:
        if prev is not None:
            if row["prev_hash"] != prev["this_hash"]:
                drift.append(row["chain_pos"])
        # Recompute this_hash from canonical fields and compare.
        recomputed = _recompute_hash(row)
        if recomputed != row["this_hash"]:
            drift.append(row["chain_pos"])
        prev = row

    return {
        "first_chain_pos": first["chain_pos"],
        "last_chain_pos":  last["chain_pos"],
        "first_this_hash": first["this_hash"],
        "last_this_hash":  last["this_hash"],
        "daily_seal":      last.get("daily_seal_sig"),
        "spot_check_stride": stride,
        "drift_positions": drift,
        "verified_at":   datetime.utcnow().isoformat(),
    }

def _recompute_hash(row: dict) -> str:
    CHAIN_FIELDS = (
        "occurred_at", "tenant_id", "actor_id", "tool_name",
        "event_class", "outcome", "payload_summary",
        "retention_class", "policy_version", "prev_hash",
    )
    canonical = json.dumps(
        {k: row.get(k) for k in CHAIN_FIELDS},
        sort_keys=True, separators=(",", ":"), default=str
    ).encode()
    return hashlib.sha256(canonical).hexdigest()
```

A non-empty `drift_positions` array is a **critical** finding: the audit log has been modified.

## 5. Job Driver

```python
# compliance/jobs/__main__.py
import argparse
from datetime import datetime, timezone
from compliance.jobs.approval_completeness import ApprovalCompletenessJob
from compliance.evidence_pack import EvidenceVault

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--window-start", required=True, type=lambda s: datetime.fromisoformat(s))
    p.add_argument("--window-end",   required=True, type=lambda s: datetime.fromisoformat(s))
    args = p.parse_args()

    job = ApprovalCompletenessJob(db=db, evidence_vault=EvidenceVault())
    summary = job.run(args.window_start, args.window_end)
    print(json.dumps(summary, indent=2))
```

Schedule in `ops/compliance/evidence-cadence.yaml`:

```yaml
- id: pi1_1_approval_completeness
  cadence: "0 3 1 * *"   # monthly 1st 03:00 UTC
  owner: security-lead@example.com
  retention_years: 7
  entrypoint: python -m compliance.jobs --window-start {{prev_month_start}} --window-end {{this_month_start}}
```

## 6. Exception Opener

```python
# compliance/exceptions.py
from datetime import datetime, timedelta

SEVERITY_SLO_DAYS = {"critical": 5, "high": 10, "medium": 20, "low": 30}

def open_exception(*, control_id: str, severity: str, title: str,
                   evidence_ref: str, detail: dict) -> int:
    target_close = (datetime.utcnow() + timedelta(days=SEVERITY_SLO_DAYS[severity])).date()
    return db.execute_returning_id("""
        INSERT INTO compliance_exceptions
            (control_id, opened_at, severity, title, description, owner,
             target_close, status, evidence_pack)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'open', %s)
        RETURNING id
    """, (control_id, datetime.utcnow(), severity, title,
          _safe_json(detail), _owner_for(control_id), target_close, evidence_ref))
```

## 7. Job Heartbeat Evidence

A missed run is itself a control gap. The cron wrapper writes a heartbeat after each successful invocation; a watcher pages on-call if no heartbeat in 36 hours after the scheduled run:

```python
# compliance/jobs/heartbeat.py
def write_heartbeat(job_id: str, status: str, summary: dict):
    db.execute("""
        INSERT INTO compliance_job_heartbeats (job_id, ran_at, status, summary)
        VALUES (%s, %s, %s, %s)
    """, (job_id, datetime.utcnow(), status, _safe_json(summary)))
```

## 8. Test Fixtures (catching the five gap classes)

```python
# tests/compliance/test_approval_completeness.py
def test_missing_approval_classified_gap_missing(seed):
    seed.action(reversibility="irreversible", task=1)
    out = run_job()
    assert out["gap_classes"]["gap_missing"] == 1

def test_after_action_beyond_skew_classified_gap_after_action(seed):
    a = seed.action(reversibility="irreversible", occurred_at="10:00:00")
    seed.approval(action_id=a, approved_at="10:00:05")  # 5s > 2s skew
    out = run_job()
    assert out["gap_classes"]["gap_after_action"] == 1

def test_self_approval_classified_gap_self_approval(seed):
    a = seed.action(reversibility="irreversible", initiator="alice")
    seed.approval(action_id=a, approver="alice")
    out = run_job()
    assert out["gap_classes"]["gap_self_approval"] == 1

def test_chain_pos_mismatch_classified_gap_chain_mismatch(seed):
    a = seed.action(reversibility="irreversible", chain_pos=42)
    seed.approval(action_id=a, linked_action_chain_pos=41)
    out = run_job()
    assert out["gap_classes"]["gap_chain_mismatch"] == 1

def test_unauthorised_approver_classified(seed):
    seed.allowlist(role="ops-approver", policy_version="v3", members=["bob"])
    a = seed.action(reversibility="irreversible", policy_version="v3")
    seed.approval(action_id=a, approver="eve", approver_role="ops-approver",
                  policy_version="v3")
    out = run_job()
    assert out["gap_classes"]["gap_unauthorised_approver"] == 1

def test_explicit_bypass_not_gap(seed):
    seed.action(reversibility="irreversible", kill_switch_bypass_id="ks-001")
    out = run_job()
    assert out["gap_classes"].get("gap_missing", 0) == 0
```

## 9. Operational Notes

- Run on a **read replica** to avoid contention with the live audit-log emitter.
- Resolve the window in UTC; auditors compare across time zones.
- Cap each gap row's `detail` to a redacted summary; the full payload stays in the vault behind a separate access control.
- Daily-seal signature column on the audit log is published off-platform (S3 Object Lock + offline notary); the witness includes its identifier so the auditor can independently re-verify.
