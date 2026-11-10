# Workflows, controls and parameters

## 1. Leave, time and payroll as one chain

```
leave request -> approval -> time/attendance close (cut-off date)
   -> payroll input snapshot (read-only) -> payroll run -> approval -> payslips
   -> payment file -> posting service (finance) -> reconciliation
```

- The **cut-off date** is a stored parameter per pay period. Items approved after it roll
  to the next period; a correction after close becomes an adjustment line next period.
- **One payroll consumer.** Only the payroll service reads the snapshot and writes results.
  Leave, time and reports never compute pay.
- A closed period is immutable. Reopening needs a named approver and a logged reason.
- Leave accrual uses dated policy rows (days per period, qualifying wait, carry-over).
  Statutory minimums come from the rate register, not code.
- Payroll results hand to the finance posting service; payslip totals reconcile to the
  ledger (finance engine `payroll-and-statutory-postings-east-africa`).

## 2. Statutory parameter register

One table, effective-dated, one row per rule value:

| Field | Meaning |
|---|---|
| `code` | e.g. pension_employer_rate |
| `value`, `unit` | The number and what it is |
| `valid_from`, `valid_to` | When it applies |
| `source_instrument`, `source_section` | Act or notice and section |
| `source_checked_on`, `checked_by` | Who verified, when |
| `status` | `VERIFIED`, `NOT_VERIFIED`, `EXPIRED` |

Rules: payroll refuses any run that touches a `NOT_VERIFIED`, `EXPIRED` or missing row;
tests use fixture rows labelled synthetic; a rate change is a new row, never an edit;
the register has a named human owner and a review date. Do not list tax bands or
thresholds in this engine; the owner supplies them from the current regulator notice.

## 3. Workflow state tables

Each workflow is a table of states, allowed transitions, who may move it, and the
record kept. A transition writes actor, time and reason.

| Workflow | States (example) | Decider | Notes |
|---|---|---|---|
| Recruitment | requisition, approved, advertised, shortlisted, interviewed, offered, accepted, closed | Hiring manager and HR owner; budget holder approves requisition | Requisition ties to an approved position. Shortlist tools are advisory. |
| Onboarding | offer accepted, documents, accounts, induction, probation set | HR owner | Checklist with owners; no access granted before contract is issued. |
| Leave | requested, approved, rejected, taken, cancelled | Line manager; HR for exceptions | Balance check before approval; delegate when manager absent. |
| Appraisal | cycle opened, objectives set, self review, manager review, calibration, signed, closed | Line manager; next manager calibrates | Staff can add comments; ratings are never machine-final. |
| Disciplinary | reported, assessed, notice given, hearing held, decision, appeal, closed | Decider named in policy; independent of the accuser | Hearing before dismissal (Employment Act s.65, VERIFIED). Case numbered. |
| Exit | notice given, handover, clearance, final pay, records closed | HR owner and line manager | Notice per contract and s.57(3) (VERIFIED); final pay through payroll only. |

Every workflow names an **owner and a backup role**. The system, a model or an
automation may prepare, remind or draft; it never owns a step.

## 4. Access control

| Data | Who | Rules |
|---|---|---|
| Employee master, non-sensitive | HR officers, the person, line manager (own reports, limited fields) | Row-level by reporting line. |
| Pay and grades | Payroll officers, finance approver, the person (own) | Separate permission; read is logged. |
| Disciplinary cases | Case handler, decider, legal | Need-to-know per case; the accused sees their own file; read is logged. |
| Medical and disability | Occupational health or the named officer only | Stored apart, encrypted, never in general reports. |
| Talent and succession | HR owner, executives | Candidate consent recorded for talent pools. |

A staff member can see their own record, request correction, and see who accessed it
where policy allows. A manager sees only their own reports.

## 5. Personal-data controls (Data Protection and Privacy Act)

- Record purpose, lawful basis, retention and recipients per data category.
- Data protection officer designated (s.6, VERIFIED); breach notification path to the
  officer and the regulator on the statutory clock (s.23, VERIFIED).
- Retention: records the tax law requires stay for 5 years (Tax Procedures Code s.15,
  VERIFIED); other retention periods are client policy until a source is cited.
- Erasure and portability follow `saas-tenant-data-portability-and-erasure`; legal holds
  override erasure.
- Regulation numbers and sector rules are `NOT_VERIFIED` until checked.

## 6. Audit trail

Log: create, update, delete or void, status transitions, permission changes, exports and
reads of pay, disciplinary, medical and talent records. Fields: tenant, actor, role,
action, record type and id, old and new values (hashed for medical), time, reason, source
(screen, API, import). Append-only; not editable by HR administrators; retention at least
as long as the underlying record.

## 7. Document numbering

Series needed, each contiguous per tenant per type, allocated at issue inside the save
transaction, voided never deleted: employment contract, offer letter, payroll run,
payslip batch, disciplinary case, appraisal form, termination notice, clearance form,
training record. Format changes get a new counter key. See `tenant-document-numbering`.

## 8. Reporting and the KPI card

Report as of a date. Each indicator gets a card:

| Field | Content |
|---|---|
| Question | What decision does it inform |
| Formula | Numerator, denominator, period |
| Source | Table and filter |
| Target | Set from the client's own trend, not copied |
| Action | What happens when it is off target |
| Owner | A named human role, plus a backup |

Candidate set: personnel cost ratio, overtime share, turnover (voluntary and total),
sickness rate, training hours per head, accident rate per million hours, internal fill
rate, time to fill, successor coverage of key roles, appraisal completion, probation
completion. A person-level score never goes to a dashboard without the underlying rows.

## 9. Go-live and vendor review

- **Phase order:** employee master and positions; payroll with at least one parallel run
  (old and new results reconciled line by line, variances explained and signed);
  then leave and time; then recruitment and appraisal.
- **Feasibility:** run the client's feasibility tests (technical, economic, operational,
  schedule; confirm the client's set) before commitment.
- **Weighted vendor criteria:** policy fit, statutory parameterisation, access control
  and audit, data residency and export, integration with finance, support, total cost.
  Weights are set by the client before scoring.
- **Benefit review** within 18 months of go-live against the estimate made before the cost.
- **Human decision:** a named person decides over any machine output.
