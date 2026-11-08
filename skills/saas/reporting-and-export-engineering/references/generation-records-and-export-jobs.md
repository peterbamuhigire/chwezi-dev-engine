Parent skill: [reporting-and-export-engineering](../SKILL.md)

# Report registry, generation records, export jobs and delivery

Load this when building a report centre, scheduled reports, background exports, share links or
the audit of downloads. It implements RPT-EXPORT-004/005/007, RPT-SEC-001/002/003 and
RPT-PERF-001, and supports RPT-GATE-04 (export leak). Queue mechanics (workers, retries,
idempotency storage) follow `background-job-implementation` where that skill is available; this
file states what a report job must record and guarantee.

## 1. Report definition registry (RPT-EXPORT-007)

Treat report, configuration, generation, distribution, retention and access as separate objects.
One registry entry per report type, in code or a table, reviewed like code:

```yaml
report:
  id: sales.daily_close                # stable, never reused
  version: 4
  title: "Daily sales close"
  description: "Net sales, collections, voids and exceptions per branch for one business day"
  owner: "Finance lead (role)"
  domain: sales
  output_contract: fixed_report        # operational_dashboard | analytical_workspace | fixed_report | executive_narrative
  decision: "Confirm the day's takings and resolve exceptions before the day is closed"
  privacy_class: confidential
  parameters:                          # typed parameter schema; nothing free-form
    branch_id: {type: branch_ref, required: true, scope: authorised_branches}
    business_date: {type: date, required: true, max: today}
  metrics: [sales.net_sales@2.0.0, cash.collections@1.1.0, sales.voids@1.0.0]
  formats: [screen, pdf_a4_portrait, xlsx, csv]
  default_sort: [document_number_issue_order]
  roles: {view: [REPORTS_VIEW], export: [REPORTS_EXPORT], print: [REPORTS_PRINT], schedule: [REPORTS_SCHEDULE]}
  retention: {generated_files_days: 30, generation_records_years: 7}   # Chwezi starting values; legal retention per jurisdiction
  print_template: daily_close_a4_v3
  export_schema: sales_daily_close/3
```

The permission codes are examples; use the product's own map and keep parity between web, API
and app (RPT-SEC-002).

## 2. Immutable generation record (RPT-EXPORT-005)

Write one record per generation (download, print, schedule run, API pull) before the file is
offered, and never update its parameters afterwards; status changes are appended events.

```json
{
  "generation_id": "gen_01JC9Q7Z5W6R2T",
  "report_id": "sales.daily_close",
  "report_version": 4,
  "tenant_id": 42,
  "requested_by": {"kind": "user", "id": 3107},
  "delivery_kind": "download",
  "parameters": {"branch_id": 7, "business_date": "2026-11-04", "timezone": "Africa/Kampala"},
  "authorised_scope": {"branches": [7], "masked_fields": ["customer_phone"]},
  "metric_versions": {"sales.net_sales": "2.0.0", "cash.collections": "1.1.0", "sales.voids": "1.0.0"},
  "source_watermark": {"max_posting_id": 9184420, "as_of": "2026-11-04T22:15:03+03:00"},
  "dataset_hash": "sha256:5b1e...",
  "formats": {"pdf": {"template": "daily_close_a4_v3", "pages": 6, "sha256": "e3a1..."}},
  "status": "ready",
  "created_at": "2026-11-04T22:15:04+03:00",
  "expires_at": "2026-11-05T22:15:04+03:00",
  "idempotency_key": "sha256(tenant|report|version|params|scope|watermark)"
}
```

Fields: parameter snapshot, metric versions, source watermark, generation time, user or service
identity, status, checksum and expiry are MUST (RPT-EXPORT-005). A scheduled run and a user's
downloaded copy are different `delivery_kind` values with separate records. Amounts never sit in
the record; it points to the dataset hash.

## 3. Background export jobs (RPT-EXPORT-004, RPT-PERF-001)

| Concern | Rule | Failure avoided |
|---|---|---|
| When to queue | Above a row or page threshold measured for the product, or always for PDF of multi-page reports | Request timeouts and half-written files |
| De-duplication | Identical requests (same idempotency key) within the job window return the existing job | Five clicks creating five 40-page PDFs |
| Progress | `queued`, `running` (percent or stage), `ready`, `failed`, `expired`, `cancelled`, visible on screen as an export-pending state | Users repeating requests; silent waits |
| Retry | Transient failures retried with backoff and a cap; the parameters and watermark never change on retry | A retried file covering different data |
| Failure | Visible failure with a plain reason and a retry action; no partial file offered | A truncated PDF taken as complete |
| Expiry | Files expire and are deleted; the record stays | Old files leaking after a role change |
| Re-check on download | Authorisation re-checked when the file is fetched, not only when queued | A revoked user collecting a ready file |
| Tenant isolation | Job payload carries tenant from server context; worker sets tenant scope before querying; storage path prefixed by tenant key | Cross-tenant files |

Deterministic, privacy-safe file names: `<report-slug>_<tenant-key>_<period>_v<schema>_<short-checksum>.<ext>`,
for example `daily-close_t42_2026-11-04_v3_e3a1c9.pdf`. No customer, patient or employee names,
phone numbers or email addresses in file names, object keys, URLs or email subjects.

## 4. Delivery, sharing and audit (RPT-SEC-001/002/003, RPT-GATE-04)

- Authorisation: row-level (tenant, branch, own records) and field-level (cost, margin, salary,
  clinical, phone) filters are applied in the query and again in the export service before data
  leaves the server. The interface hiding a column is never the control.
- Separate rights for view, export, print and schedule where the domain requires; a schedule
  runs with the schedule owner's current rights at run time, and stops when the owner loses
  them.
- Share links are signed, single-purpose and expiring; revocation works before expiry.
- Log every download, schedule recipient, share creation, share use and revocation with actor,
  time, generation ID and recipient; never the file contents or raw sensitive values.
- Sensitive fields stay masked in previews, notification emails, file names and logs; emails
  carry a link to the authenticated download, not the attachment, where policy requires.
- Sign or watermark files where the product requires it (for example "Copy issued to ... on
  4 Nov 2026").

## 5. Tests for this layer

| Test | Evidence |
|---|---|
| Lower-role session calls the export and download APIs directly for another branch and for masked fields | UIT, NET: one denial per row of the role x endpoint matrix |
| Two identical requests in the window produce one job and one file | UIT |
| Retry after a forced worker crash produces a file with the same dataset hash | UIT |
| Expired file returns "expired"; the record remains | UIT |
| Revoked user cannot download a file generated before revocation | UIT |
| Tenant A job never reads tenant B rows (fixture with identical ids in both tenants) | UIT |
| Log and email samples contain no raw sensitive values or personal data in file names | NET, REVIEW |
