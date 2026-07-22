---
name: accounting-engine
description: Use when designing, implementing, or reviewing an embedded accounting engine with append-only ledgers, mapped postings, idempotency, reversals, period locks, audit trails, and integrity tests.
metadata:
  portable: true
  required_inputs: Provide the transaction event, tenant, accounting policy, chart mapping, and existing ledger contract.
  workflow: Follow the posting invariants, mapping, idempotency, reversal, lock, and verification workflow in this file.
  quality_standards: Preserve double-entry balance, tenant isolation, immutability, traceability, and tested failure handling.
  anti_patterns: Do not post directly from feature code, mutate journals, bypass locks, or infer accounts without mappings.
  outputs: Produce posting contracts, journal evidence, mapping decisions, controls, and integrity tests.
  default_standard: IFRS for SMEs
  compatible_with:
  - claude-code
  - codex
---

# Accounting Engine

<!-- dual-compat-start --><!-- dual-compat-end -->

## Inputs

| Artefact | Required? | Purpose |
|---|---|---|
| Transaction event and tenant context | yes | Define the event and isolation boundary |
| Account mapping and doctrine policy | yes | Resolve balanced ledger accounts |
| Existing ledger and lock state | yes | Prevent duplicate or closed-period posting |

## Outputs

| Artefact | Consumer | Acceptance condition |
|---|---|---|
| Posting contract and journal evidence | Feature services and finance review | Balanced, idempotent, traceable, tenant-scoped |

## Capability contract

Read and search are required. Database writes, migrations, backfills, reversals, and period operations require explicit authority and a verified compensating path.

## Degraded mode

Fallback without doctrine, mappings, or database access: return a posting design and unresolved control list; do not invent accounts or claim ledger correctness.

## Decision rules

| Condition | Posting action | Failure avoided |
|---|---|---|
| New valid economic event | Append balanced journal | Missing financial record |
| Duplicate idempotency key | Return prior result | Double posting |
| Error in posted journal | Post linked reversal/correction | Destruction of audit history |
| Closed period | Reject or use authorised later-period adjustment | Period integrity breach |

## Domain anti-patterns

- Posting directly from controllers. Fix: use one posting service and contract.
- Updating or deleting journals. Fix: reverse and repost with links.
- Guessing accounts from feature names. Fix: require mapping-layer resolution.
- Retrying without idempotency. Fix: persist and enforce the event key.
- Mixing tenants in one posting context. Fix: require tenant scope on every ledger operation.

## Use When

- The product handles money, inventory value, payroll, tax, customer balances, supplier balances, assets, grants, donations, loans, refunds, wallet balances, or financial reporting.
- A SaaS must replace routine bookkeeping in external products such as QuickBooks, Xero, Sage, Pastel, Tally, Zoho Books, or Wave.
- You need architecture, schema, posting rules, tests, documentation, or review findings for ledger-backed business software.

## Do Not Use When

- The task is only financial analysis or projections without software architecture; use `accounting-finance-controller` or the business-plan finance skills.
- The system only displays imported accounting reports and does not create business events or postings.
- A jurisdiction requires a licensed accountant, auditor, or tax practitioner to exercise professional judgement; design the system support, but do not claim the software replaces that judgement.

## Hard Rules

- NEVER let a business module write directly to `gl_entries`, `journal_lines`, `journal_entries`, or any ledger table.
- ALWAYS write ledger records through one service: `LedgerPostingService::post(JournalEntry $entry)` or the project-equivalent single posting service.
- NEVER update, delete, or soft-delete posted journal lines. Corrections are reversing journals linked to the original entry.
- NEVER store authoritative balances that cannot be rebuilt from journal lines. Materialized balances are caches with a documented rebuild command.
- NEVER hardcode account codes in business logic. Use account mappings resolved at posting time.
- NEVER use LIFO for IFRS or IFRS for SMEs tenants.
- MUST reject posting when required account mappings are missing, inactive, cross-tenant, or not valid for the source document.

## Canonical Architecture

Business modules emit events. A mapper turns events into balanced `JournalEntry` value objects. The posting service validates and writes the entry atomically. Reports, subledgers, balances, tax schedules, and dashboards are deterministic projections of the ledger.

```text
Sales / Stock / Payroll / Assets / Payments / Grants
        -> business event
        -> account resolver and posting-rule mapper
        -> JournalEntry value object
        -> LedgerPostingService::post()
        -> append-only journal_entries + journal_lines
        -> reports, subledgers, tax schedules, dashboards
```

## Required Model

Core tables:

- `chart_of_accounts`
- `account_mappings`
- `journal_entries`
- `journal_lines`
- `accounting_periods`
- `posting_rule_versions`
- `accounting_integrity_runs`
- `accounting_audit_log`

Every accounting table MUST carry `tenant_id`, unless the product is explicitly single-tenant. If legacy files use `franchise_id`, treat it as a project-specific tenant alias and document the mapping.

## Posting Service Contract

```php
<?php
declare(strict_types=1);

final readonly class JournalEntry
{
    public function __construct(
        public int $tenantId,
        public string $idempotencyKey,
        public DateTimeImmutable $entryDate,
        public string $sourceType,
        public string $sourceId,
        public string $description,
        /** @var list<JournalLine> */
        public array $lines,
        public ?int $reversesJournalId = null,
    ) {}
}

final readonly class JournalLine
{
    public function __construct(
        public int $accountId,
        public string $currency,
        public string $debitMinor,
        public string $creditMinor,
        public array $dimensions = [],
    ) {}
}

interface LedgerPostingService
{
    public function post(JournalEntry $entry): PostedJournal;
}
```

The service validates tenant scope, account status, open period, debit-credit equality, currency policy, idempotency, source document state, and mapping completeness before insert.

## Integrity Checks

Run these per tenant and per accounting period from day one:

- Debits equal credits per `journal_entry_id`.
- Trial balance total debits equal total credits.
- AR control account equals customer-tagged journal line balance.
- AP control account equals supplier-tagged journal line balance.
- Inventory control account equals stock-on-hand value by item/location/cost layer.
- Fixed asset control account equals asset-register cost less disposals.
- Payroll liability accounts equal unpaid statutory and employee deductions.
- No journal exists in a locked period unless it is a permitted reopening workflow with approval evidence.
- No ledger table has rows written outside the posting service.
- Materialized balances rebuild to the same values as stored cache rows.

## User Experience Principle

Non-accountants record business actions: `Record Sale`, `Receive Payment`, `Buy Stock`, `Run Payroll`, `Record Asset Purchase`, `Receive Grant`, `Close Month`. The system posts accounting behind the scenes. Accountant-facing roles get journals, CoA, mappings, period close, manual journal, and report exports.

## Companion Skills

- `chart-of-accounts-templates` for IFRS-aligned industry templates.
- `inventory-costing` for IAS 2 stock valuation and COGS flows.
- `payroll-postings-uganda` for PAYE/NSSF/LST payroll journal shapes.
- `fixed-assets-and-depreciation` for IAS 16 asset lifecycle.
- `multicurrency-and-fx` for IAS 21 currency handling.
- `multi-tenant-saas-architecture`, `api-design-first`, and `advanced-testing-strategy` for platform integration.

## References

- `references/posting-engine-contract.md`
- `references/integrity-invariants.md`
