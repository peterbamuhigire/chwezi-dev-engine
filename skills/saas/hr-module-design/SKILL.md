---
name: hr-module-design
description: Use when designing or reviewing an HR system or ERP HR module - positions versus people, effective dating, contract classes, leave and payroll inputs with parameterised statutory rates, recruitment to exit workflows, appraisal, disciplinary records, personal-data access and audit. Not payroll journals, HR policy text or vendor choice.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# HR Module Design
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

An HR module holds the most sensitive records a tenant owns and feeds its largest
recurring cost. Most failures come from a few early modelling choices: treating a
job and a person as one row, hard-coding statutory rates, letting several screens
write pay, and giving every HR user the same access. This skill fixes those choices
before code. It is client-neutral; the organisation set-up handed to a SaaS team is
the worked example in `references/worked-example-org-handoff.md`.

<!-- dual-compat-start -->
## Use When

- Designing the HR tables, services or screens of a new ERP or SaaS module, or
  reviewing an existing one.
- Mapping a client's organisation chart, jobs and pay grades into a system.
- Specifying leave, time, payroll inputs, recruitment, onboarding, exit, appraisal or
  disciplinary workflows.
- Reviewing HR data access, personal-data handling or audit trail in a diff.
- Planning an HR system go-live, or judging a vendor's HR module against the client's
  policy manual.

## Do Not Use When

- The task is the ledger entries for a payroll run; use the finance engine skill
  `payroll-and-statutory-postings-east-africa` and `accounting-engine`.
- The task is writing the HR policy or manual text; use the writing engine's
  `human-resources-documentation`.
- The task is the requirements document for the module; use the SDLC engine's
  `20-hr-module-srs`.
- The task is only document numbering; use `tenant-document-numbering` (this skill
  names which HR documents need a series).

## Required Inputs

| Input | Source | If missing |
|---|---|---|
| Organisation chart, units, reporting lines, headcount plan | Client owner | Model units and positions as drafts; mark headcount `NOT_ASSESSED`. |
| Contract classes the client uses (employee, part-time or fixed-term, consultant) | HR owner | Default to the three classes; each carries its own tax and contribution treatment. |
| Statutory rate source register (Act, section, rate, effective date, status) | Finance or legal owner | Ship rates as empty parameters; payroll refuses to run on an unset or unverified rate. |
| Client HR policies (leave types, probation, notice, disciplinary steps) | HR manual | Build the engine configurable; do not invent policy values. |
| Tenant model and role catalogue | Tenancy design | Block design; never infer tenant from a request body. |
| Named human owner and backup for each HR record type and decision | Client owner | Record as an open item. AI never owns anything. |

## Workflow

1. **Separate positions from people.** A position (a seat in a unit with a title,
   level, line manager and budget status) exists whether or not someone fills it.
   An assignment links a person to a position over a date range. Headcount, vacancies
   and succession read positions; payroll and leave read people. See
   `references/data-model-and-effective-dating.md`.
2. **Date everything that changes.** Title, level, unit, line manager, contract class,
   pay grade and rates carry `valid_from` and `valid_to`. A correction fixes a wrong
   entry; a change adds a new dated row. Never overwrite history.
3. **One employee master record.** Every module reads the same person row. No second
   list of staff in payroll, access control or recruitment.
4. **Classify the contract.** The class decides which statutory treatment applies, by
   parameter. Part-time and consultant classes need a setting for the client's maximum
   consecutive contracts and required break, and a review prompt for disguised
   employment. The break rule is client policy unless a statute is cited as VERIFIED.
5. **Run leave, time and payroll as one chain.** Approved leave and time close at a
   cut-off date; payroll reads that closed set; one payroll service writes pay results.
   Nothing else writes to payroll tables. See
   `references/workflows-controls-and-parameters.md`.
6. **Parameterise statutory rates.** Rates, bands, thresholds and dates live in
   effective-dated parameter tables with Act, section, source date and status
   `VERIFIED` or `NOT_VERIFIED`. Payroll blocks on any unverified or expired row.
7. **Build workflows as state machines with a named decider.** Recruitment,
   onboarding, exit, leave, appraisal and disciplinary cases each have states, who may
   move them, and a record of who did.
8. **Protect people data by role and by field.** Disciplinary, medical, pay and talent
   data each get their own permission; medical data is stored apart; a staff member
   can see and request correction of their own record.
9. **Log every change and every read of a sensitive record.** Who, what, when, old and
   new value, reason. HR administrators cannot edit the log.
10. **Number the documents.** Contracts, offer letters, payroll runs, disciplinary
    cases and appraisal forms get contiguous per-tenant numbers allocated at issue
    (standing rule; `tenant-document-numbering`). Void, never delete.
11. **Make machine output advisory.** Any scoring, ranking or recommendation about a
    person (shortlist, appraisal rating, attrition risk) shows its inputs, can be
    overridden, and names the human who decided. The tool may be named; it never owns.
12. **Go live payroll first.** Employee master and payroll first, with at least one
    parallel run against the old method and reconciliation before switching; then
    leave and time; then recruitment and appraisal.

## Quality Standards

- One person row, one master; positions and people never share a table.
- No statutory number in code, seed data or a test expectation without a parameter row
  that cites its source.
- Every status change records the actor and reason; closed payroll periods are immutable.
- Access is tested per role and per field; a manager sees only their own reports.
- Personal data has a stated purpose, retention period and erasure path; a breach path
  reaches the data protection officer and the regulator on the statutory clock.
- Reports state their formula, source and owner (KPI card in the workflows reference).

## Anti-Patterns

- A `staff` table that is also the position table, so a vacancy cannot exist.
- Overwriting a title or pay grade, so last year's payslip cannot be reproduced.
- PAYE, NSSF or withholding-tax rates typed into code or a migration.
- Payroll computed in the leave screen or the report layer.
- One HR administrator role that reads everything, including medical and disciplinary files.
- Deleting a leaver, a contract or a case instead of ending or voiding it.
- A model that auto-rejects candidates or auto-scores appraisals with no human decision.
- `COUNT(*)+1` for contract or payroll-run numbers.
- Copying a client's names, pay or case data into engine examples or fixtures.

## Outputs

- Position, person, assignment and contract data model with effective-dating rules.
- Contract-class and statutory-parameter register with source status.
- Workflow state tables with deciders, owners and backups.
- Role and field access matrix, audit-log design and retention table.
- Document-series list for HR documents.
- Go-live plan with parallel-run and reconciliation criteria.
- HR KPI cards for the client's chosen indicators.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | Position, assignment and effective-dating model with overlap tests | Schema plus test report | `docs/hr/data-model.md` |
| Correctness | Statutory parameter register with VERIFIED or NOT_VERIFIED status | Table with Act, section, date | `docs/hr/rate-register.csv` |
| Security | Role and field access matrix with per-role test results | Matrix plus test log | `evidence/hr/access-matrix.md` |
| Data safety | Audit-log sample showing change and sensitive-read records | Log extract | `evidence/hr/audit-sample.txt` |
| Data safety | Retention and erasure table per record type | Markdown table | `docs/hr/retention.md` |
| Operability | Parallel-run reconciliation of old and new payroll | Variance report | `evidence/hr/parallel-run.csv` |
| Release evidence | Go-live phase plan with exit criteria and named owners | Markdown checklist | `docs/hr/go-live.md` |

## References

- [Data model and effective dating](references/data-model-and-effective-dating.md):
  tables, keys, overlap rules, corrections versus changes, job families and levels,
  contract classes, import rules.
- [Workflows, controls and parameters](references/workflows-controls-and-parameters.md):
  leave-time-payroll chain, rate register, workflow state tables, disciplinary and
  medical access, data protection, audit, numbering, KPI card, go-live and vendor review.
- [Worked example: organisation handoff](references/worked-example-org-handoff.md):
  how an organisation was mapped into existing tables.
- Companions: `multi-tenant-saas-architecture`, `tenant-document-numbering`,
  `saas-tenant-data-portability-and-erasure`, `database-design-engineering`,
  `accounting-engine`, `ai-evaluation` (algorithmic decision impact review).
- Finance engine (`chwezi-accounting-doctrine`): `payroll-and-statutory-postings-east-africa`.

<!-- dual-compat-end -->

## Capability and permission contract

Default to read-only design and review. Never load real employee, pay or case data
into a prompt, fixture or log; use synthetic people. Never run a migration or payroll
against production from this skill; hand reviewed work to the authorised operator.

## Degraded mode

Without the client's policy manual, deliver a configurable design and mark every
policy value `NOT_ASSESSED`. Without verified statutory sources, ship empty parameters
and block payroll; do not fill rates from memory. Without a database, return the
schema as a labelled design and the tests as a plan.

## Decision rules

| Condition | Action | Failure avoided |
|---|---|---|
| A role exists in the chart but nobody holds it | Create the position as vacant | Headcount and succession that cannot see gaps |
| A person's title or grade changes | Add a dated assignment row | Lost history, wrong back-pay |
| A rate has no VERIFIED source row | Payroll blocks that run | Wrong deductions filed with a regulator |
| A part-timer reaches the client's consecutive-contract limit | Flag for the HR owner; require a decision | A silent rollover that breaches client policy |
| Someone asks to view disciplinary or medical files | Require a named permission and log the read | Broad exposure of the most sensitive data |
| A model ranks or scores people | Show inputs, allow override, record the human decider | Unreviewable decisions about people |
| A numbered HR document is wrong | Void and reissue | Gaps or silent edits |

## Sources

Uganda statute figures enter this skill only as VERIFIED rows with Act and section;
all others are `NOT_VERIFIED` and must be checked against the instrument and the
regulator's current notice before use. VERIFIED (owner's law notes, 10 Nov 2026,
not re-checked against the instruments this session): NSSF contribution 10% employer
and 5% employee (NSSF Act, ss.11-12); Employment Act maternity leave 60 days (s.55),
paternity 4 days (s.56), annual leave 7 days per four months after six months (s.53),
notice (s.57(3)), hearing before dismissal (s.65); Data Protection and Privacy Act
breach notice (s.23) and data protection officer (s.6); Tax Procedures Code record
retention 5 years (s.15). NOT_VERIFIED: Employment (Amendment) Act 2025 content, Data
Protection and Privacy Regulations numbers, Occupational Safety and Health Act, the
Income Tax Act section and basis for 6% withholding tax on part-time pay, severance,
and any disguised-employment test. Review the register before the next release.
