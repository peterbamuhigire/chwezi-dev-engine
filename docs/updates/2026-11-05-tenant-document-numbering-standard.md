# Tenant document numbering standard (kaizen, 5 Nov 2026)

Owner rule of 5 Nov 2026: in every multi-tenant SaaS system, existing or new, every
user-facing document number is contiguous per tenant and per document type, and the
auto-increment id stays separate. This record covers the kaizen that put the rule into
the engine.

## Baseline (main @ 74c9bda)

Searched every active skill and reference for document numbers, sequences, gap
detection, counters and generator code. Findings:

- No skill owned user-facing document numbering. The engine had no allocator pattern,
  no clash handling, no issue-time rule, and nothing on capacity, offline numbers or
  retrofitting existing tenants.
- `saas-accounting-system/references/schema-design.md` generated journal numbers in a
  `BEFORE INSERT` trigger with `MAX(...)+1`. That races under concurrency, reissues a
  number when the latest row goes, and hides the logic from application tests. The same
  file said "gaps are acceptable" and sized `entry_number` at `VARCHAR(20)`.
- `saas-accounting-system/SKILL.md` built the reversal reference from the row id
  (`JE-{original_id}`).
- `saas-accounting-system/references/journal-posting-rules.md` depended on that trigger
  and opened its own transaction, so a journal could not share a transaction with its
  source document.
- `pos-sales-ui-design/ALIAS.md` and
  `product-discovery/.../pos-mandatory-requirements.md` required receipt numbers
  "sequential per sales point" and gap detection in a stored procedure. Both conflict
  with one series per tenant and type, and with keeping generators in application code.
- The SDLC templates `code-documentation-standards.md` and
  `database-design-document.md` showed an invoice number generated inside
  `sp_create_invoice`.
- Related skills (`multi-tenant-saas-architecture`, `database-design-engineering`,
  `mysql-engineering`, `postgresql-engineering`, `api-design-first`,
  `php-modern-standards`, `pwa-offline-first`, `android-development`,
  `accounting-engine`, `accounting-finance-controller`, `saas-erp-system-design`,
  `pos-sales-operations-engineering`, `hospitality-hotel-restaurant-systems`,
  `subscription-billing`, `electronic-fiscal-taxing`, `code-safety-scanner`,
  `advanced-testing-strategy`, the AI code review gate) said nothing about numbering.
  `saas-erp-system-design` had one line ("use document numbers ... consistently").
  `api-design-first` already said large integers travel as strings and required
  idempotency keys on payments, but kept keys for only 24 hours, which does not
  guarantee the same number on a late replay.

## Changes

- New skill `skills/saas/tenant-document-numbering/` with four references: schema and
  allocator (MySQL 8 and PostgreSQL counter tables, registry, allocator pseudo-code, PHP
  allocator and retry wrapper, lifecycle, lock order), seeding, clashes and capacity,
  API, offline and guardrails (contract, idempotency, provisional tags, CI ratchet, test
  and review checklists), and retrofit and rollout. Applies to new designs and to
  retrofits. Cites the Maduuka plan `docs/plans/numbering/` as the reference
  implementation.
- Fixed the contradictions above: the trigger is replaced with application allocation
  through the new skill, gaps are no longer acceptable, `entry_number` is
  `VARCHAR(40)`, the reversal reference uses the entry number, the posting procedure
  takes the allocated number and is told to run inside the caller's transaction, POS
  receipt numbering is per tenant and type, and the templates take the number as an
  input.
- One cross-reference line (anti-pattern, checklist item or table row) in each related
  skill listed in the baseline.
- Registered the skill: plugin manifest (regenerated), root router, routing index,
  skill catalogue, alias registry count, README and overview counts, count tests, and
  three routing fixtures with three owned negatives.
- Tests: the AI review-gate route test now expects the
  document-number row; count tests moved to 168 and 166.

## Sources (currentness gate)

Primary documentation read on 5 Nov 2026 (tier 1, freshness class platform, review
after 5 Feb 2027, support status supported, confidence high for the page text read):

| Claim | Source |
|---|---|
| `nextval` is not reclaimed on abort; sequences cannot give gapless numbers | PostgreSQL 18.6, https://www.postgresql.org/docs/current/functions-sequence.html |
| Unique index NULLs are distinct by default; `NULLS NOT DISTINCT` changes this | PostgreSQL 18.6, https://www.postgresql.org/docs/current/indexes-unique.html |
| `23505`, `40P01`, `40001`, `55P03`; test codes, not messages | PostgreSQL 18, https://www.postgresql.org/docs/current/errcodes-appendix.html |
| `FOR UPDATE` locks are released at commit or rollback | MySQL 8.4, https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html |
| Rolled-back auto-increment values are lost, leaving gaps | MySQL 8.4, https://dev.mysql.com/doc/refman/8.4/en/innodb-auto-increment-handling.html |
| A unique index permits multiple NULLs | MySQL 8.4, https://dev.mysql.com/doc/refman/8.4/en/create-index.html |
| `1062`/`23000`, `1205`/`HY000`, `1213`/`40001` | MySQL 8.4, https://dev.mysql.com/doc/mysql-errors/8.4/en/server-error-reference.html (first 100,000 characters read) |
| Integers are interoperable only within plus or minus 2^53 - 1 | IETF RFC 8259 section 6, https://www.rfc-editor.org/rfc/rfc8259#section-6 |

These were not added to `docs/source-registers/skills-engine-currentness-2026-09.json`:
`tests/test_source_register.py` requires every register to pass on its 2026-10-31
reconciliation date, so a record accessed later fails it. Adding them belongs with the
next register reconciliation, which must also re-read the five overdue Next.js records.

## Verification

Run on Windows 11 with Python 3.13.7 and Node on 5 Nov 2026; results are in the commit
message. The two validator findings that existed before this change (the
`test_current_checkout_is_under_file_budget` count on this Windows checkout, and the five
Next.js source records overdue since 3 Nov 2026) are unchanged and were not caused here.

## Not assessed

- Live model routing: the routing smoke test is a lexical proxy.
- The SQL and PHP examples were not executed against MySQL 8.4 or PostgreSQL 18; they
  are illustrative and need a disposable-database test before reuse.
- The `ALGORITHM=INPLACE, LOCK=NONE` widening claim was not re-tested on a large table.
- Model-currentness review (`NOT_ASSESSED`): no model-policy change is proposed.
- The cross-engine runtime metadata validator in `chwezi-engine-agents` and the
  sibling-checkout control-plane run were not run.
- Tax-authority fiscal numbering rules (EFRIS, eTIMS, EFD) are out of scope.
