# PR Reviewer Checklist — Chwezi Finance Engine

Use this checklist whenever a PR touches money, ledger, tax, payroll, banking, mobile money, POS, inventory, fixed assets, grants, statutory compliance, or financial reports. The PR cannot merge if any item below is `fail`.

## Posting boundary

- [ ] No `INSERT INTO journal_lines`, `UPDATE journal_lines`, `DELETE FROM journal_lines`, or equivalent, outside an approved posting service.
- [ ] No `INSERT INTO journal_headers` or equivalent outside the posting service.
- [ ] The PR includes a unit test for any new posting path that asserts double-entry balance per currency.

## CoA discipline

- [ ] New CoA accounts carry full metadata (class, statement-group, normal side, control / clearing flags, tax flag, currency rule, dimensions, direct-post permission, evidence requirement).
- [ ] No free-text accounts; no postings to "Other" / "Miscellaneous" without an ageing plan.
- [ ] Control accounts have a documented subledger and reconciliation cadence.

## Tax & VAT

- [ ] VAT-inclusive postings decomposed into net + tax + gross.
- [ ] Tax codes carry rate, jurisdiction, and effective period.
- [ ] Rates / thresholds read from source register, not hardcoded.
- [ ] WHT / PAYE / NSSF post to dedicated liability control accounts.

## Reversal

- [ ] Posted records are reversed via a linked reversal journal; never edited; never deleted.
- [ ] UI for posted records does **not** show `Delete` / `Remove` verbs.

## Period state

- [ ] Posting into a locked period is rejected by the posting service.
- [ ] Reopen requires Controller + CFO approval.

## Audit log

- [ ] Every posting writes an audit-log row with actor, time, source document, evidence, lineage, posting-service version.
- [ ] The audit log is append-only.

## Idempotency

- [ ] Integration-driven postings carry idempotency keys.
- [ ] Replays with same key return prior result; replays with same key + different payload are rejected.

## Reconciliation

- [ ] Imported bank / MoMo / POS / card feeds stage before posting; no silent ledger writes.
- [ ] Triage UI present, not a downloadable report.
- [ ] Evidence pack produced.

## Migration

- [ ] Cutover pack present; opening journal balanced; suspense zero or waived; subledger tie-outs documented.

## UI

- [ ] Two surface modes used appropriately.
- [ ] Drilldown affordance on every money summary.
- [ ] Status taxonomy used; no free-text statuses.
- [ ] Net / tax / gross triplet on VAT-inclusive screens.
- [ ] Print stylesheet present and tested.
- [ ] Semantic colour only on state; never on chrome / brand / CTA.
- [ ] WCAG AA contrast.

## Controls

- [ ] SoD conflicts checked.
- [ ] Maker-checker on payments, refunds, credit notes, manual journals, opening balances, tax settings, supplier master changes, payroll master changes, period reopen.
- [ ] Supplier bank-detail change followed by payment within 24 hours is flagged.

## Tests

- [ ] Property-based tests for debit / credit balance.
- [ ] Reversal test for every new posting type.
- [ ] Period-state rejection test.
- [ ] Idempotency replay test.
- [ ] VAT-inclusive split test.

## Doctrine

- [ ] PR title or body cites which doctrine sections it touches.
- [ ] PR cites the doctrine version adopted.
- [ ] Any forbidden pattern introduced (or remediated) is named.

Last reviewed: 2026-05-12. Next review due: 2026-11-12.
