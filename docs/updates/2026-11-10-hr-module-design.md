# 2026-11-10: HR module design skill (HR-systems kaizen, phase P4)

## Baseline

Inventory of the engine (search for payroll, HR, leave, org, workforce, position,
tenant-numbering): no skill covered HR systems. Related only: `tenant-document-numbering`
(names payroll run as a numbered type), `multi-tenant-saas-architecture`,
`saas-tenant-data-portability-and-erasure`, `accounting-engine` (payroll journals).
Payroll posting lives in the finance engine; HR policy text in the writing engine.
Nothing deleted, moved or renamed.

## Changes

- New skill `skills/saas/hr-module-design` (SKILL.md plus three references): positions
  versus people with effective dating; job families, levels and grades; employee master;
  contract classes (employee, part-time or fixed-term, consultant) with configurable
  consecutive-contract limit and break; leave-time-payroll chain with cut-off and a single
  payroll consumer; effective-dated statutory parameter register with VERIFIED or
  NOT_VERIFIED status (no hard-coded Uganda rates); workflow state tables for recruitment,
  onboarding, leave, appraisal, disciplinary and exit with a named human decider; access
  by role and field; personal-data controls; audit trail; HR document series per the
  standing numbering rule; KPI card; payroll-first go-live with parallel run; weighted
  vendor criteria; benefit review within 18 months; machine output advisory only.
- Worked example (client-neutral) of handing an organisation structure to a SaaS team.
- Routing: three fixtures (one with two owned negatives), skill catalogue row, routing
  index row, plugin manifest path, count surfaces 169 to 170 (plugin 167 to 168), three
  pinned test counts.

## Not done

- No SRS template here (SDLC engine). No payroll journals here (finance engine).
- Statutory rows are the owner's law notes of 10 Nov 2026, not re-checked against the
  instruments: NOT_ASSESSED. NOT_VERIFIED: Employment (Amendment) Act 2025, DPP
  Regulations numbers, OSH Act, ITA section for 6% WHT, severance, disguised-employment test.
- The four feasibility tests are named generically in the reference; the owner's set is
  not in the plan files. NOT_ASSESSED.
- Golden and pressure cases, live host discovery of the skill: NOT_ASSESSED.

## Re-measure (10 Nov 2026, Windows 11)

- `skill_catalog_guardrails.py`: 170 active skills, 0 errors, 16 size warnings (none for the new skill).
- `contract_gate.py --all`: 164 scanned, 0 errors.
- `routing_smoke_test.py --min-rank1 89 --lint-fixtures`: precision@1 228/248 (91.9%), 0 failures.
- `validate_engine_control_plane.py`: PASS. `check_source_register.py`: PASS (metadata only).
- `pytest tests`: 272 passed, 3 skipped, 1 failed. The failure,
  `test_current_checkout_is_under_file_budget` (8,520 files against a limit of 5,000),
  also fails without this change; it counts local untracked trees. Not caused by this work.
- Not run: node hook tests, `git diff --check` clean of errors (line-ending warnings only).
