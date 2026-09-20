# Solution selection record

Use this short record before a substantive engineering change. Its purpose is
to make the decision frontier visible: understand the existing flow, question
whether new code is needed, reuse the repository, prefer a suitable standard
library or native platform facility, check installed dependencies, and choose
the smallest maintainable option that still preserves the requirements and
required safeguards.

The sequence is advisory reasoning, not a universal native-first rule. A native
control that cannot meet the required interaction, a dense one-liner that hides
validation, or an unreviewed security primitive is not the smallest adequate
solution. Record the exception and its review trigger.

## Required record

Create a JSON record using `schemas/solution-decision.schema.json` and validate it
from the repository root:

```powershell
python tools/solution_decision.py validate path/to/solution-decision.json --root .
```

The record names the problem, requirements and invariants; considers at least
two options; identifies the selected option; binds the decision to a SHA-256
scope; cites repository or test evidence; declares security, mutation and
money/ledger risk; and lists normal and negative tests. Missing or changed
evidence is a failed gate or `NOT_ASSESSED`, never an implicit pass.

## Review rules

| Situation | Minimum evidence |
|---|---|
| Trivial, read-only change | Existing capability or no-change option, scope and one relevant check |
| New dependency or boundary change | Dependency/host evidence, security review, failure path and rollback |
| Data migration, asynchronous retry or money/ledger path | Invariants, idempotency/recovery tests, controller/domain review and rollback |
| Security or authorisation change | Deny-case tests, actor/tenant scope, audit/observability evidence and independent review |

The validator checks structure, file scope and evidence existence. It does not
replace architecture judgement, source currentness, accessibility review,
finance doctrine or product acceptance.

See [solution-selection-examples.md](solution-selection-examples.md) for
original examples and counterexamples covering repository reuse, native form
controls, parsers, database constraints and retry identity.

## Domain gates

- UI, keyboard, focus, reflow and assistive-technology acceptance belongs to
  `C:\wamp64\www\design-system-skills`; this engine records the boundary and
  consumes its evidence rather than duplicating visual doctrine.
- Money, ledger, posting, period, reversal, idempotency and reconciliation
  invariants belong to `C:\wamp64\www\chwezi-accounting-doctrine`; use its
  `ledger-posting-engine-core` and `ledger-invariants` routes where applicable.
- Requirements, acceptance IDs and traceability belong to
  `C:\wamp64\www\srs-skills`; implementation decisions return the approved
  identifiers and evidence through the SDD handoff contract.
