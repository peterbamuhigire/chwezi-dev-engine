# Solution-selection implementation wave — 2026-09-20

## Outcome

The engineering engine now has a portable implementation of the useful
Ponytail decision mechanisms, integrated with existing control-plane ownership.
It records the problem and invariants, considers repository reuse and native or
installed facilities, validates a bounded scope hash, and requires evidence and
negative tests before a decision can pass.

## Added capabilities

- `tools/solution_decision.py` and `schemas/solution-decision.schema.json` for
  fail-closed decision records.
- `tools/solution_review.py` for read-only diff and repository review.
- `tools/solution_debt.py` for scoped marker and ledger visibility.
- `tools/solution_mode.py` for repository/session-scoped advisory modes with
  atomic persistence and explicit reset.
- `tools/solution_evidence.py` for raw-run and quality-gated evidence checks.
- `tools/adapter_lifecycle.py` plus Codex/Claude instruction-only manifests for
  plan/apply/verify/revert without unsolicited host configuration changes.

No active skill was added. The existing world-class-engineering, advanced-testing,
validation-contract and control-plane owners remain authoritative. High-risk
changes still require independent negative or mutation evidence; a one-test or
short-code rule is not introduced.

## Validation

The focused engineering suite passes 43 tests with one opt-in live-host test
skipped. Full suite execution and CI remain release gates; comparative model
experiments are separate and are not implied by these structural checks.
