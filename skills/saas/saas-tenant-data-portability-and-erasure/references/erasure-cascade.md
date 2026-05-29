# Erasure Cascade - Reference

Erasure is not a single DELETE. It is a cascade through every store the SaaS uses, in an order that respects foreign keys and external dependencies, with honest handling of derived data and backups, and a structured proof at the end. This reference specifies the per-store cascade, the soft-vs-hard-delete decision, FK ordering, derived/backup handling, and legal hold - the things that turn "we ran a delete" into "we can prove the tenant was erased".

## section 1 Soft vs Hard Delete

| Approach | What it does | Acceptable for erasure? |
|---|---|---|
| **Soft delete** (`deleted_at = NOW()`) | Marks the row hidden; data remains | NO, by itself. PII is still in the database; fails the regulatory test under GDPR Art.17 / POPIA / Uganda DPPA |
| **Hard delete** | Removes the row | Yes, for primary PII stores |
| **Pseudonymise** | Replaces PII with an irreversible hash, keeps the row | Yes, for stores that must be retained for legal reasons (audit log, financial records) |
| **Crypto-erase** | Destroys the per-tenant key so encrypted data is unreadable | Yes, the strongest option for encrypted-at-rest stores |

Soft delete has a legitimate role as the *first* step (a reversible `pending_erasure` state during the cool-down window), but it must be followed by hard delete or pseudonymise. The failure mode of stopping at soft delete is the classic audit finding: the regulator queries the database and the "erased" customer's email, name, and records are all still there.

## section 2 Foreign-Key Order

Within the primary OLTP database, delete children before parents or the FK constraints reject the delete (or, worse, you disable constraints and orphan half the data).

```text
Order (children -> parents):
  1. leaf activity:   audit-irrelevant events, notifications, sessions, tokens
  2. content rows:    documents, messages, comments, attachments-metadata
  3. join tables:     memberships, role assignments, sharing grants
  4. user rows:       users belonging to the tenant
  5. tenant-owned:    projects, workspaces, settings
  6. tenant row:      the organisation record itself (last)
```

Prefer `ON DELETE CASCADE` on FK definitions where the data model allows, so a single delete at the tenant root cleans children atomically. Where cascade is not defined (legacy schema, cross-schema references), delete explicitly bottom-up in one transaction. The wrong choice - deleting the tenant row first - either fails on the constraint or, if constraints are off, leaves orphaned child rows full of PII pointing at a tenant that no longer exists.

For tenant-per-schema isolation, dropping the schema is the cleanest hard delete and sidesteps FK ordering entirely.

## section 3 The Full Cascade (External First)

External processors are slowest and least reversible, so they go first - if a later internal step fails and the run pauses, the irreversible external work is already done and will not be re-attempted incorrectly.

```text
 1. Mark tenant `pending_erasure`     -> stop new data, invalidate sessions, block UI
 2. External processors (irreversible):
       Stripe        -> delete Customer; financial records retained, PII redacted
       ESP/Twilio    -> delete contacts; UPDATE central suppression list
       Analytics     -> vendor delete API (per distinct-id / per-tenant property)
       CRM           -> API delete; verify the vendor's own cascade
       AI/vector     -> drop namespace; crypto-erase via KEK revocation
 3. Search indexes                    -> delete-by-tenant / drop tenant index
 4. Caches                           -> flush per-tenant key namespace
 5. Object storage                   -> delete per-tenant prefix
 6. Primary OLTP                     -> FK-ordered hard delete or schema drop (section 2)
 7. Warehouse                        -> DELETE / pseudonymise; rebuild materialised views
 8. Audit log                        -> PSEUDONYMISE PII (email -> hash); KEEP the rows
 9. Backups                          -> flag for redaction at next rotation (section 5)
10. Tenant record                    -> status=deleted, identifiers as opaque hashes only
11. Write TENANT_ERASURE_COMPLETED   -> structured outcome JSON (proof)
12. Notify requester                 -> confirmation + retention-exception summary
```

Each step is idempotent and retriable; per-step status persists in `erasure_runs.step_status`. On an unrecoverable failure (a vendor API down), pause, alert ops, resume - do not skip and do not mark complete.

## section 4 Derived Data

Derived data is where erasure quietly fails, because the obvious stores get cleaned and the second-order copies are forgotten.

| Derived store | Why it is easy to miss | Handling |
|---|---|---|
| Search index | Rebuilt from the DB; deleting the DB row does not remove the index doc | Explicit delete-by-tenant; do not rely on DB delete to propagate |
| Materialised views / rollups | Aggregates may still expose PII or re-derive it on refresh | DELETE source rows, then rebuild the view; verify it does not re-pull from a backup |
| Warehouse fact/dim tables | ETL copied PII months ago; nobody refreshes deletions back | Per-tenant partition delete or pseudonymise; check ELT does not re-import |
| Caches / CDN | Stale PII served after the source is gone | Flush per-tenant namespace; purge CDN paths |
| Read replicas | Replication lag, or detached replicas | Confirm replicas caught up; detached/snapshot replicas treated as backups |
| Embeddings / model adapters | Vectors and fine-tunes encode the source content | Drop per-tenant vector namespace; delete tenant adapters; never delete the shared base model |
| Exports already generated | A prior data-export ZIP sits in a bucket | Expire and delete prior export artifacts for the tenant |

## section 5 Backups - Be Honest

Backups are the most-lied-about part of erasure. You almost never delete data from backups instantly, and claiming you do is a worse compliance posture than documenting the truth.

- Do NOT surgically edit live backup snapshots to remove one tenant - that corrupts your disaster-recovery posture and is usually technically infeasible.
- DO document the rolling retention window (for example 30-90 days). Erased data persists in backups only until those backups age out of rotation, after which it is gone.
- DO flag the tenant so that if a backup is *restored* during the window, the erasure is re-applied to the restored data before it returns to service. A restore that silently resurrects an erased tenant is a fresh breach.
- DO record the backup retention window in the Data Processing Agreement so the customer accepts it in advance.

The honest statement is: "Your live data is erased immediately; residual copies in encrypted backups are purged within N days as backups rotate, and any restore re-applies your erasure." The dishonest statement - "deleted everywhere instantly" - is the one that fails the audit.

## section 6 Legal Hold and Retention Exceptions

Erasure is overridden by legal hold and by statutory retention.

- **Legal hold**: if the tenant (or specific data) is under litigation hold, the erasure must NOT proceed for held data. Check `legal_holds` before step 1; if a hold matches, refuse the erasure (or scope it to exclude held data) and record the refusal with the hold reference. Erasing data under hold is spoliation of evidence - a legal offence, not a compliance win.
- **Statutory retention**: financial records (invoices, payments, tax IDs) are retained for the jurisdiction's period (commonly 7 years). These are pseudonymised where possible (strip name/email, keep the transaction) rather than deleted.
- **Audit log**: retained for regulatory periods with PII fields pseudonymised. Deleting audit rows destroys the evidence that the erasure itself happened - exactly the proof a regulator asks for.

Every retention exception applied during a run is listed in the completion record and the customer notification, so the erasure is honest about what survived and why.

## section 7 Proof of Erasure

The run ends with a structured, retained record - not a log line.

```json
{
  "event": "TENANT_ERASURE_COMPLETED",
  "tenant_id_hash": "sha256:9f86d0...",
  "requested_at": "2026-05-20T10:00:00Z",
  "completed_at": "2026-05-27T14:12:00Z",
  "steps": [
    {"store": "stripe", "action": "customer_deleted_pii_redacted", "status": "ok"},
    {"store": "elasticsearch", "action": "tenant_index_dropped", "status": "ok"},
    {"store": "primary_oltp", "action": "fk_ordered_hard_delete", "rows": 48211, "status": "ok"},
    {"store": "warehouse", "action": "partition_deleted", "status": "ok"},
    {"store": "audit_log", "action": "pii_pseudonymised", "status": "ok"},
    {"store": "backups", "action": "flagged_redaction_on_rotation", "window_days": 30, "status": "scheduled"}
  ],
  "retention_exceptions": ["financial_records_7y", "audit_log_7y"],
  "legal_hold": "none"
}
```

This record is itself retained as compliance evidence (commonly 6+ years) and is what answers "did you erase tenant X completely, and how do you know?".

## section 7a User-Level vs Tenant-Level Cascade

The cascade differs by scope, and conflating them is a common error.

| Aspect | User-level erasure | Tenant-level erasure |
|---|---|---|
| Target | One user's PII, possibly across several tenants | An entire organisation's data |
| Shared data | Must NOT delete content authored by the user that the tenant still owns - pseudonymise the author, keep the content | Everything for the tenant is removed |
| Memberships | Remove the user's membership; the tenant survives | The tenant and all memberships go |
| Mechanic | `DELETE ... WHERE user_id = ?` plus author pseudonymisation on shared rows | Per-tenant cascade or schema drop |
| Risk of the wrong choice | Hard-deleting a departing user's authored documents destroys the tenant's records (data loss the tenant did not ask for) | Scoping a tenant erasure to one user leaves the rest of the org's PII behind |

A user leaving a tenant is usually a membership removal plus pseudonymisation of their PII in shared content, not a destructive delete of everything they ever touched. A user erasing their own account across all tenants is the union of those per-tenant operations.

## section 7b Idempotency and Resume

Each step in section 3 is keyed by `(erasure_run_id, store)` in `erasure_runs.step_status`. Before running a step, check it is not already `ok`; after, persist the result.

```python
def run_step(run, store, fn):
    if run.step_status.get(store) == "ok":
        return                                   # already done; safe to skip on resume
    try:
        result = fn(run.tenant_id)               # idempotent store operation
        run.step_status[store] = "ok"
        run.step_results[store] = result
    except Exception as e:
        run.step_status[store] = "failed"
        run.step_errors[store] = str(e)
        raise                                    # pause the run, alert ops
```

A run that crashed after deleting Stripe and search but before the primary DB resumes at the primary DB - it does not re-delete the Stripe customer (already `ok`) and does not double-process. Without per-step idempotency, a resume either re-runs irreversible external deletes (errors, or worse, deletes a newly recreated record) or restarts the whole cascade.

## section 8 Anti-Patterns

- **Soft delete only** - PII still in the database; fails the regulatory test.
- **Deleting the parent before children** - FK error, or orphaned PII if constraints are off.
- **Forgetting derived stores** (search, warehouse, embeddings, caches) - PII survives in copies.
- **Surgically editing live backups** - corrupts disaster recovery; usually infeasible.
- **Claiming instant backup deletion** - false; documents a worse posture than the honest rolling window.
- **No restore-time re-erasure** - a backup restore resurrects an erased tenant.
- **Erasing data under legal hold** - spoliation of evidence.
- **Deleting audit-log rows** - destroys the proof the erasure happened.
- **No structured outcome record** - cannot prove completeness during an audit.

## See Also

- `saas-tenant-data-portability-and-erasure` section 3 (capability matrix), section 5 (workflow), section 7 (retention exceptions).
- `references/requester-verification.md` - proving the requester is entitled before any of this runs.
- `references/export-format-spec.md` - the final export offered before erasure.
- `ai-agent-memory-erasure-proof` - the agent-memory leg and independent verification probes.
- `ai-tenant-isolation-patterns` - per-tenant KEK strategy for crypto-erase.
- `uganda-dppa-compliance` - regional retention specifics.
