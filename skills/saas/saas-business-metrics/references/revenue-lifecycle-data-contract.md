# Revenue Lifecycle Data Contract

Load when product, sales, customer-success, and finance disagree about lifecycle numbers ("trial",
"customer", "activated", "churned"), when product signals must reach a CRM or messaging tool, or
when designing the events and views behind a lead-to-renewal dashboard.

This reference owns the data contract. Sales organisation design lives in
`saas-sales-organization`; PQL weighting in `product-led-growth/references/pql-scoring.md`; money
movements in `saas-growth-metrics/references/saas-metrics-event-contract.md`; send decisions in
`saas-lifecycle-email-orchestration`.

## Inputs

- The product's activation definition (a named product event and window) from the PRD.
- Current CRM objects and field list, lifecycle-messaging profile attributes, and who edits each.
- Billing mirror and tenant lifecycle states (`saas-control-plane-engineering` reference branch).
- Privacy basis and retention rules for each attribute that leaves the product database.

## Step 1: Publish one definitions registry

Create a versioned registry (a table or a reviewed YAML file) where each lifecycle stage has:

| Field | Meaning |
|---|---|
| `stage_code` | Stable identifier, e.g. `activated`, `adopted`, `customer`, `churned` |
| `unit` | `person`, `tenant`, or `opportunity`; B2B stages are almost always tenant-level |
| `entry_predicate` | SQL or rule over named events and states, not prose |
| `exit_predicate` | What removes the unit from the stage |
| `source_of_truth` | Product DB, billing processor, or CRM, per predicate input |
| `owner` | Person accountable for the definition |
| `version`, `effective_from` | Changes are new versions; history is never recomputed silently |

Rules:

- Every dashboard, CRM sync, and messaging filter reads the registry-backed view, never a private
  re-implementation. A second definition of "active customer" is a defect to fix, not a dashboard
  option.
- "Customer" requires a paid, non-refunded first invoice plus a provisioned tenant, not a CRM stage
  set by hand.
- "Churned" distinguishes contractual end from behavioural dormancy; both may exist, with distinct
  codes.
- Internal, demo, sandbox, pilot, and test tenants carry a flag and are excluded by the view itself.

## Step 2: Emit stage-transition events

Each stage change emits one idempotent event: `unit_type`, `unit_id`, `tenant_id`, `from_stage`,
`to_stage`, `definition_version`, `occurred_at`, `evidence_event_ids`, `idempotency_key`. Compute
transitions from the registry in a scheduled job or stream processor; do not scatter
`if activated then ...` checks across application code. Backfills record a new
`definition_version` so trend breaks are explainable.

## Step 3: Decide field ownership before syncing

For every attribute that crosses a system boundary, declare exactly one writer:

| Attribute class | Writer | Sync direction |
|---|---|---|
| Plan, MRR, seats, usage, last activity, lifecycle stage, health score | Product/warehouse | Product to CRM/messaging, read-only there |
| Opportunity stage, next step, owner, forecast category | CRM | CRM to warehouse only |
| Contract dates, negotiated terms | Contract record (`customer_contracts`) | Contract to billing, CRM, CS tools |
| Consent and suppression | Consent service | Consent service to every sender |

Sync ("reverse ETL") jobs must be idempotent upserts keyed by tenant id, record the last synced
version, skip excluded tenants, send only fields with a documented purpose, and alert on rejected or
conflicting writes rather than overwriting a human-owned CRM field.

## Step 4: Capture profile data progressively

Ask for segmentation data (sector, organisation size, current tool, primary use case) one question
at a time at natural moments across early sessions instead of a long signup form. Store answers
with source (`self_reported`, `enriched`, `inferred`), timestamp, and question version. Enriched or
inferred values never overwrite self-reported ones. Collect only fields a named consumer uses;
purpose and retention follow the privacy route (Uganda DPPA 2019 and other applicable law, via
`saas-tenant-data-portability-and-erasure`).

## Step 5: Derive operational alerts from contract data

- Renewal alerts are generated from contract end dates and notice clauses in the contract record,
  not from a CRM reminder someone typed. Alert both the account owner and customer-success owner at
  owner-configured offsets.
- Stale opportunity decay: flag opportunities with no activity for an owner-set period; never
  auto-close without an owner-approved rule.
- Product-qualified accounts crossing the approved threshold create or update a CRM task or
  opportunity through the sync job, with the evidence events attached, and with a de-duplication
  key so repeated threshold crossings do not create duplicates.
- Customer-review data packs (usage, adoption depth, value metrics for a tenant over a period) are
  generated from the warehouse views with tenant isolation tests, not assembled by hand.

## Worked example (original)

A Nairobi clinic-scheduling SaaS defines `activated` as "tenant has booked 20 real appointments
through the calendar within 14 days of signup, excluding demo data". Sales had been counting any
tenant that imported a patient list. After the registry went live (v1), sales-reported activation
fell from 61% to 38%; the drop was a definition correction, recorded as `definition_version = 1`
with the old metric retained as `imported_patients` for continuity. The CRM now receives
`lifecycle_stage` and `appointments_booked_30d` nightly as read-only fields, and the four pilot
clinics run by the vendor's field team are excluded by flag.

## Quality gate

- [ ] Every stage has a machine-checkable predicate, unit, owner, and version.
- [ ] One view per stage; dashboards, CRM sync, and messaging filters all read it.
- [ ] Demo, sandbox, pilot, internal, and test tenants are excluded inside the view.
- [ ] Each cross-system attribute has one writer; conflicting writes alert.
- [ ] Sync jobs are idempotent, tenant-scoped, and purpose-limited, with a replay test.
- [ ] Progressive-profile answers keep source and question version; self-reported wins.
- [ ] Renewal alerts derive from contract data and are tested against a fixture contract.
- [ ] Definition changes produce a new version and a documented trend break.

## Anti-patterns

- Each team computing its own "active" or "churned" in its own tool.
- Lifecycle stage set manually in the CRM and then treated as product truth.
- Two-way sync of the same field, producing silent ping-pong overwrites.
- Pushing every product event to the CRM or messaging tool "in case".
- Sandbox and pilot tenants inflating customer counts and activation rates.
- Recomputing history under a new definition without versioning.

## Evidence / currentness

Access date 2026-09-24. This reference contains no vendor capability, threshold, or regulatory
claim beyond naming the Uganda Data Protection and Privacy Act, 2019 as an applicable law for
Ugandan data subjects; its specific obligations are owned by the privacy route and are
`NOT_ASSESSED` here. CRM and messaging-tool API limits and field types: `NOT_ASSESSED`; verify
against the chosen vendor's current documentation before building a sync job.

Sources: Winning By Design (n.d.) *The SaaS Sales Method Fundamentals*; Winning By Design (n.d.)
*The SaaS Sales Method for Account Executives*; Mersch (2022) *Hacking SaaS*; Garbugli (n.d.)
*The SaaS Email Marketing Playbook*.
