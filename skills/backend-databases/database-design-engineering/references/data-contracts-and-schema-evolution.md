# Data Contracts and Schema Evolution

Parent skill: [database-design-engineering](../SKILL.md).

Load when a table, event stream, API feed, or file drop is consumed by a team,
service, model, or report that its producer does not own, and you must define,
enforce, version, or retire the interface. For internal-only schema changes on
a table nobody else reads, `live-data-evolution.md` is enough.

Requirements-side counterpart (what the contract must guarantee, as verifiable
NFRs): `srs-skills` `02-requirements-engineering/fundamentals/during/05-conceptual-data-modeling/references/data-contract-and-dictionary-requirements.md`.
Enforcement and lineage emission in pipelines:
`../../../languages/python-data-pipelines/references/data-quality-checks-and-lineage.md`.

## 1. What a data contract is, and is not

A data contract is a versioned, machine-readable agreement, owned by the
producer, that states the structure, meaning, quality expectations, service
levels, and governance metadata of one data interface. It is to data what an
OpenAPI document is to an HTTP API.

| It is | It is not |
|---|---|
| An interface deliberately published for consumers, separate from the producer's internal tables | A description of whatever the producer's database happens to contain today |
| Owned and signed off by the producing team, who carry the pager for breaches | A wish list written by the analytics team and emailed upstream |
| The single source from which schemas, warehouse tables, topic schemas, catalog entries, and access policies are generated | One of five hand-maintained copies that drift apart |
| Enforced in CI and at runtime | A wiki page |

Decision rule: if a consumer outside the owning team reads the producer's raw
operational tables or CDC stream directly, you have an undeclared contract. Declare
it or cut the dependency; never leave it implicit.

## 2. Inputs before drafting

| Input | Source | If missing |
|---|---|---|
| Named consumers and the decision or product each one drives | Consumer teams | Stop. A contract without a named consumer is speculative publishing. |
| Required fields, grain (one row per what), and join keys | Consumer requirements, conceptual data model | Draft grain only; mark fields `proposed`. |
| Freshness, completeness, and availability each consumer actually needs | Consumer requirements or SRS data-quality NFRs | Default to the loosest value any consumer accepts, never the tightest anyone asked for. |
| Personal-data and confidentiality classification per field | Data protection officer, classification policy | Block `active` status until classified. |
| Retention and erasure rules | Legal/retention schedule | Block `active` status. |
| Producer capacity and constraints | Producing team | Negotiate scope before committing SLOs. |

## 3. Lifecycle procedure

Use the Open Data Contract Standard (ODCS) status vocabulary so tooling and
catalogs interoperate: `proposed` -> `draft` -> `active` -> `deprecated` -> `retired`.

1. **Purpose (proposed).** Record who consumes the data, what they decide with
   it, and what failure costs them. Write the grain in one sentence.
2. **Trade-offs (proposed).** The producer states what it can sustain. Consumers
   trade scope or latency for dependability. Set SLOs at the minimum that meets
   the most demanding real use case: cost rises steeply as targets tighten, and
   an unmet SLO destroys more trust than a modest honest one.
3. **Define (draft).** Write the contract file (Section 4) in the producer's
   repository, next to the code that emits the data. Open a pull request that
   named consumers review.
4. **Gate (draft -> active).** CI must pass every check in Section 6. Consumers
   approve. Status changes to `active` only by merged pull request.
5. **Provision and backfill (active).** Generate the interface (warehouse table,
   topic schema, API schema) from the contract. Backfill history if a consumer
   needs it, and record the backfill boundary in `description.limitations`.
6. **Operate (active).** Runtime checks and SLO monitors run (Section 7). Breaches
   page the producer, not the consumer.
7. **Evolve.** Classify every change with Section 5 before editing.
8. **Deprecate.** Set `status: deprecated`, publish the replacement and the
   removal date, and list remaining readers from lineage.
9. **Retire.** Remove only when lineage shows zero readers for one full business
   cycle (month-end included for finance feeds). Set `status: retired`; keep the
   file for audit.

## 4. Contract template (ODCS v3.2.0, validated)

Original example: a Ugandan SACCO lending platform publishes repayments for
portfolio-at-risk reporting, a credit-scoring feature store, and month-end
reconciliation. This file validates with zero errors against the published
`odcs-json-schema-v3.2.0.json`.

```yaml
apiVersion: v3.2.0
kind: DataContract
id: 7f3c2a90-5d1e-4b8e-9a61-2c0f4e8b1d55
name: loan_repayment_received
version: 2.1.0
status: active
domain: lending
description:
  purpose: >-
    One record per repayment credited to a member loan, for portfolio-at-risk
    reporting, the credit-scoring feature store, and month-end reconciliation.
  limitations: >-
    Excludes reversals; those are published on loan_repayment_reversed.
    Branch cash receipts arrive up to 4 hours late when a branch is offline.
  usage: Join to loan_disbursed on loan_id. Never join on member_ref across tenants.
schema:
  - name: loan_repayment_received
    physicalName: lending.loan_repayment_received_v2
    logicalType: object
    description: A repayment credited to a loan after the payment provider confirmed settlement.
    quality:
      - type: library
        metric: rowCount
        mustBeGreaterThan: 0
        dimension: completeness
        description: At least one repayment per business day; zero rows means the feed is stalled.
        severity: error
        schedule: "0 7 * * 1-6"
        scheduler: cron
    properties:
      - name: repayment_id
        logicalType: string
        required: true
        unique: true
        primaryKey: true
        description: Producer-issued identifier, stable across replays.
      - name: loan_id
        logicalType: string
        required: true
        description: Loan the repayment was credited to.
      - name: member_ref
        logicalType: string
        required: true
        classification: restricted
        description: Pseudonymous member key; the raw national ID never leaves the lending service.
        customProperties:
          - property: personalData
            value: true
          - property: erasureStrategy
            value: tokenise
      - name: amount_ugx
        logicalType: integer
        required: true
        description: Amount credited in whole Uganda shillings.
        quality:
          - type: sql
            query: "SELECT COUNT(*) FROM ${object} WHERE amount_ugx <= 0"
            mustBe: 0
            dimension: conformity
            description: Amount is a positive integer.
            severity: error
      - name: channel
        logicalType: string
        required: true
        enum:
          - value: mtn_momo
          - value: airtel_money
          - value: bank_transfer
          - value: branch_cash
        description: Settlement channel reported by the payment provider.
      - name: received_at
        logicalType: timestamp
        required: true
        description: Provider settlement time, UTC, ISO 8601.
slaProperties:
  - property: latency
    value: 15
    unit: m
    element: loan_repayment_received.received_at
    driver: operational
  - property: availability
    value: 99.5
    unit: percent
    driver: operational
  - property: retention
    value: 7
    unit: y
    driver: regulatory
team:
  name: lending-platform
  members:
    - username: j.akello
      role: owner
    - username: r.ssemwogerere
      role: data steward
support:
  - channel: "#lending-data"
    tool: slack
    scope: interactive
```

Notes an agent must respect:

- `version` is the contract version (semantic versioning); `apiVersion` is the
  ODCS version. Do not confuse them.
- ODCS v3.2.0 represents `enum` as a list of objects with `value`, not bare strings.
- Money is an integer in the smallest unit the ledger books, with the currency
  in the field name or a sibling field; never a float.
- Personal-data flags and erasure strategy are fields, not prose, so deletion
  tooling can act on them.
- Keep organisation-specific keys in `customProperties`; do not invent top-level keys.
- The 7-year retention above is illustrative. Take the real value from the
  client's retention schedule and cite its source.

## 5. Change classification and compatibility

Classify before editing. Serialisation formats define precise rules (Avro schema
resolution, Protocol Buffers field-number rules, JSON Schema); the table is the
format-neutral decision layer.

| Change | Class | Version bump | Required process |
|---|---|---|---|
| Add optional field or enum-free attribute | Non-breaking | Minor | Pull request, CI green |
| Improve description, add tag or glossary link | Non-breaking | Patch | Pull request |
| Tighten a quality threshold the data already meets | Non-breaking | Minor | Show 30 days of history passing |
| Add an enum value | Breaking for strict consumers | Major unless every consumer declared tolerant readers | Notify consumers; confirm handling of the unknown value |
| Remove or rename a field, change type, change grain, change units or time zone | Breaking | Major | Migration plan below |
| Loosen an SLO or quality threshold | Breaking for expectations | Major | Consumer sign-off |
| Reclassify a field to more sensitive | Non-breaking structurally, access-breaking | Minor | Access review before release |

Breaking-change migration plan (all fields required):

1. Consumers affected, taken from lineage, not memory.
2. Parallel-run window: publish v(n) and v(n+1) side by side. Two weeks is a floor
   for one or two consumers; longer when many consumers or month-end is inside the window.
3. Mapping from old to new fields and any semantic change.
4. Per-consumer cut-over owner and date.
5. Removal date for v(n) and the lineage check that authorises removal.

The friction is intentional: a breaking change costs the producer a plan so that
it cannot cost every consumer an incident.

## 6. CI gates on the contract file

| Gate | Fails when |
|---|---|
| Schema validity | File does not validate against the declared ODCS JSON Schema. |
| Required metadata | Missing owner, version, status, description, or any field lacking type and description. |
| Governance completeness | Any field lacks a classification decision, or a personal-data field lacks an erasure strategy. |
| Compatibility | Diff against the last `active` version contains a breaking change without a major bump and linked migration plan. Use the schema registry's compatibility check where one exists. |
| Generated artefacts | Warehouse DDL, topic schema, or JSON Schema regenerated from the contract differs from the committed copy. |
| Status transition | Status moves to `active` without consumer approval, or from `active` straight to `retired`. |

## 7. Publishing patterns

The first question is whether consumers need the published data to be
transactionally consistent with the producer's database.

| Pattern | Use when | Cost |
|---|---|---|
| Write directly to the interface | Consistency with the source write is not required; batch loads or a fast stream | A crash between the database write and the publish loses or duplicates data |
| Transactional outbox | Consistency required and the database supports multi-table transactions | Extra write on the hot path; a relay process to operate |
| Listen to yourself (write the event first, apply it to your own database from the stream) | Stream-first design or weak multi-table transactions | Producer's own reads become eventually consistent; handle ordering and duplicates idempotently |
| Producer-owned view over CDC | Legacy service that cannot change its write path | Producer maintains a second artefact coupled to internal tables; CI must catch drift. Use as a bridge, not a destination |

Never let a downstream team build the contract view on the producer's CDC feed:
ownership lands with the team that cannot fix the source.

## 8. Anti-patterns

- Contract written by consumers and "handed" to producers. Fix: producer owns
  and approves; consumers review.
- One contract per producer database. Fix: one contract per published interface
  and grain.
- SLOs copied from the most demanding request. Fix: agree the minimum that meets
  the real decision; record who accepted it.
- Hand-maintained warehouse DDL beside the contract. Fix: generate it and fail CI on drift.
- Deleting a deprecated version on the announced date without checking lineage.
  Fix: removal gated on zero readers.
- Contract lives in a central data-team repository the producer never opens. Fix:
  keep it beside the producing code, or in the repository the producer already uses for infrastructure.

## 9. Premium versus generic output

| Generic AI output | Senior output |
|---|---|
| "Define a schema and use a schema registry." | Names the grain, the consumers, the owner, the SLO each consumer accepted, and who is paged on breach. |
| YAML with invented top-level keys | Validates against the declared ODCS version; organisation extras sit in `customProperties`. |
| "Avoid breaking changes." | Classifies the specific change, bumps the version correctly, and attaches a dated migration plan with lineage evidence. |

## Evidence/currentness

Access date for all checks: 2026-09-24.

- ODCS: latest release v3.2.0, published 2026-09-08 (GitHub releases API,
  `bitol-io/open-data-contract-standard`); v3.1.0 was published 2025-12-08.
  Field names, status examples, quality types (`text`, `library`, `sql`, `custom`),
  library metrics (`nullValues`, `missingValues`, `invalidValues`,
  `duplicateValues`, `rowCount`), quality dimensions, and SLA fields checked
  against `schema/odcs-json-schema-v3.2.0.json` and
  bitol-io.github.io/open-data-contract-standard/latest. The example in Section 4
  was validated with `jsonschema` against that schema: 0 errors. `dataProduct`
  is deprecated since v3.1.0; `team` as a bare array is deprecated and slated
  for removal in 4.0.
- JSON Schema: current published version is 2020-12 (json-schema.org/specification).
  The draft-07 examples common in older literature are superseded.
- Schema-registry product capabilities and serialisation compatibility modes:
  `NOT_ASSESSED` in this pass; check the chosen registry's current documentation.

Sources: Jones (2023) *Driving Data Quality with Data Contracts*; Bitol project,
Open Data Contract Standard v3.2.0 (2026).
