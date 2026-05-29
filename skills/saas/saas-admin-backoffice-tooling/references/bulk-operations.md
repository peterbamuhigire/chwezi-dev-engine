# Bulk Operations - Reference

A bulk operation is any back-office action that touches more than one tenant (or more than one user) in a single submission: plan migration of a cohort, region migration, mass re-invite, mass suspend of a fraud cluster, feature-flag rollout. Bulk operations are blast-radius nightmares: a single wrong WHERE clause suspends 500 of the wrong tenants. This reference specifies how to make them safe by default.

## section 1 The Non-Negotiables

Every bulk operation, without exception, has:

1. A **cohort selection** that is captured and replayable (not re-evaluated at run time).
2. A **dry-run** that produces a report before any write.
3. **Idempotency** so a retried or resumed run does not double-apply.
4. **Batching** with a rate limit, so the platform is not knocked over.
5. **Partial-failure handling** with per-item status, not all-or-nothing.
6. A **rollback snapshot** captured before the run.
7. **Per-item audit** plus start/midpoint/completion broadcast.

If a proposed bulk feature cannot satisfy all seven, it is not ready to run against production tenants.

## section 2 Cohort Selection - Freeze It

The cohort is selected once and frozen. Do NOT store a SQL predicate and re-evaluate it at execution time, because the population shifts between dry-run and production-run (a tenant upgrades, a new tenant matches the predicate), so the operator approves one set and a different set executes.

```python
def create_bulk_job(actor, selector_sql, op_type):
    rows = db.execute(selector_sql)              # evaluate ONCE
    cohort = [r.tenant_id for r in rows]
    job = BulkJob.create(
        actor=actor,
        op_type=op_type,
        selector_sql=selector_sql,               # kept for audit, NOT re-run
        cohort=cohort,                            # frozen list of ids
        cohort_hash=sha256(sorted(cohort)),       # approval is bound to this hash
        status="dry_run_pending",
    )
    return job
```

The operator's production-run approval is bound to `cohort_hash`. If the cohort changes between approval and execution, the run aborts. Selection sources: ad-hoc SQL, CSV upload, or a saved segment - all resolve to a frozen id list.

## section 3 Dry-Run

The dry-run executes the full operation logic inside a transaction that is always rolled back, and records what *would* change.

```python
def dry_run(job):
    report = []
    with db.begin() as tx:
        for tenant_id in job.cohort:
            before = capture_state(tenant_id, job.op_type)
            apply_op(tx, tenant_id, job.op_type)          # real logic
            after = capture_state(tenant_id, job.op_type)
            report.append({"tenant_id": tenant_id, "before": before, "after": after})
        tx.rollback()                                      # nothing persists
    job.dry_run_report = report
    job.status = "awaiting_approval"
```

The report names: how many tenants affected, a per-tenant before/after diff, and any tenants where the op is a no-op or would error. The wrong choice - running a bulk op with no dry-run - is exactly how "suspend the fraud cohort" becomes "suspend 500 paying customers" with no chance to catch it first.

## section 4 Idempotency

Each item-level apply is keyed so that re-applying is a no-op. Two layers:

- **Job-level idempotency key**: the `Idempotency-Key` header on the submit request; a duplicate submit returns the existing job rather than creating a second one.
- **Item-level idempotency**: each `(job_id, tenant_id)` apply writes a row in `bulk_job_items` with a unique constraint; before applying, check the item is not already `succeeded`.

```python
def apply_item(job, tenant_id):
    item = BulkJobItem.get_or_create(job_id=job.id, tenant_id=tenant_id)
    if item.status == "succeeded":
        return                                  # already done; safe to skip
    try:
        with db.begin() as tx:
            do_the_real_mutation(tx, tenant_id, job.op_type)
            audit_log("BULK_ITEM_APPLIED", actor=job.actor, target_tenant=tenant_id,
                      job_id=job.id, op=job.op_type)
            item.status = "succeeded"
    except Exception as e:
        item.status = "failed"
        item.error = str(e)
```

Without item-level idempotency, a resume after a crash re-applies to tenants already processed - granting double credits, sending duplicate emails, or re-migrating an already-migrated subscription.

## section 5 Batching and Rate Limits

Execute in fixed-size batches with a pause between them. This bounds database load, third-party API pressure (Stripe, the ESP), and the blast radius of a logic bug that only shows up once the run is live.

| Operation class | Batch size | Inter-batch pause | Pauseable? |
|---|---|---|---|
| Read-mostly (flag rollout) | 200 | 1 s | Yes |
| DB writes (plan migration) | 50 | 2 s | Yes |
| Third-party calls (Stripe price swap) | 25 | 5 s (respect provider rate limit) | Yes |
| Destructive (mass suspend / delete) | 10 | 10 s + per-batch progress confirm | Yes, and auto-pauses on error-rate spike |

An auto-pause trips when the per-batch failure rate exceeds a threshold (for example > 10% of a batch fails). The run stops and pages the operator rather than ploughing through 500 failures. The wrong choice - one giant unbatched transaction - locks tables, exhausts the provider's rate limit, and gives you no progress visibility when it stalls.

## section 6 Partial-Failure Handling

Bulk operations are partial-success by design, never all-or-nothing across the cohort.

- Each item commits in its own transaction (section 4). One tenant's failure does not roll back the 49 that succeeded in the batch.
- Failures are recorded with the error and left in `failed` status.
- At completion, the job reports `{succeeded: N, failed: M, skipped: K}` and a downloadable list of failures with reasons.
- A failed-items-only re-run is the remediation path: it re-targets just the `failed` items, reusing the same job id and item idempotency.

Treating the whole cohort as one transaction means tenant #480's transient error rolls back tenants #1-479, and the operator must start over - at which point idempotency (or its absence) decides whether the retry is safe.

## section 7 Rollback Snapshot

Before the production-run, capture enough pre-state to undo within a defined window.

- For reversible ops (plan change, flag toggle, limit override): snapshot the prior value per tenant into `bulk_job_items.before_state`. Undo restores it.
- For ops with external side effects (Stripe subscription change): record the prior Stripe object id/version; undo issues the compensating call.
- Undo is itself a bulk operation - same dry-run, idempotency, audit machinery - not a raw script.
- Undo window: default 24 hours. After that, undo is no longer one-click and requires a fresh operation.

Some ops are genuinely irreversible (hard-delete, an email already sent). Mark these `reversible=false` in the op registry; the UI warns the operator that there is no undo, and these require the heavier approval in section 8.

## section 8 Approval and Authorisation

| Operation | Approval | Co-sign | Dry-run mandatory |
|---|---|---|---|
| Flag rollout to a cohort | engineering_oncall | No | Yes |
| Plan migration | billing_ops + super_admin | No | Yes |
| Region migration | engineering_oncall + super_admin | Yes | Yes |
| Mass suspend (fraud) | super_admin | Co-sign by security | Yes |
| Mass delete | super_admin | Co-sign + 24h cooldown + exec sign-off | Yes |

Co-sign means a second authorised staff member approves the frozen cohort (bound to `cohort_hash`) in the UI within a time window, or the job expires. Skipping co-sign on destructive ops means one compromised or mistaken operator can suspend or delete at scale unchecked.

## section 9 Observability

- Start, midpoint, and completion broadcast to the staff Slack channel with counts.
- Live progress (`processed / total`, current batch, error count) visible in the back-office while the job runs.
- Every item emits an audit row; the job emits `BULK_JOB_STARTED` / `BULK_JOB_COMPLETED` with the outcome summary JSON.

## section 10 Anti-Patterns

- **No dry-run** - the wrong WHERE clause is discovered after it suspends real tenants.
- **Re-evaluating the selector at run time** - approved cohort and executed cohort differ.
- **One giant transaction** - locks the DB, no progress, one bad item rolls back everything.
- **No item-level idempotency** - resume after a crash double-applies.
- **No rate limit on third-party calls** - Stripe/ESP throttles you mid-run, leaving the cohort half-migrated.
- **All-or-nothing failure model** - a single transient error forces a full restart.
- **Undo as a raw script** - the undo itself becomes an unaudited, un-dry-run bulk op that compounds the damage.
- **No co-sign on destructive ops** - one operator, one bad day, platform-wide harm.

## See Also

- `saas-admin-backoffice-tooling` section 6 - the bulk-operations workflow this expands.
- `references/internal-roles-and-permissions.md` - who may run which bulk class.
- `saas-control-plane-engineering` - the migration services bulk ops drive.
- `subscription-billing` - Stripe subscription/price semantics for plan migration.
