# Data model and effective dating

Client-neutral. Names are suggestions; keep the client's existing names where they exist.

## Core tables

| Table | Holds | Key rules |
|---|---|---|
| `org_units` | Company, divisions, departments, teams | Parent link; a unit has one head position; `valid_from`/`valid_to`. |
| `cost_centers` | Finance codes, one per unit | Unit-to-cost-centre dated link; payroll posts by cost centre. |
| `job_families` | Groups of related jobs | Stable code. |
| `job_levels` | Ordered levels with `rank` | Rank is a number; never sort by the label. |
| `pay_grades` | Salary range per grade | Restricted table; amounts need their own permission. |
| `job_titles` | Title, family, level, grade code | A title carries the grade code only; amounts stay in `pay_grades`. |
| `positions` | A seat: title, unit, reporting position, headcount, budget status, status | Exists with no holder (`vacant`). Statuses: planned, approved, vacant, filled, frozen, closed. |
| `employees` | One person master | Never holds title, unit or pay; those come from the assignment. |
| `assignments` | Employee in a position, with FTE share | Dated; no overlap for the same employee unless FTE shares total at most 100%. |
| `contracts` | Class, start, end, terms | Class: employee, part_time_fixed_term, consultant. Numbered per tenant. |
| `contract_class_rules` | Parameters per class | Statutory treatment, limits, break period, review prompt. |

## Positions versus people

Reporting lines run between **positions**, not people. When a manager leaves, the
position stays and the reports keep their line. A report that asks "who reports to
whom today" joins positions to current assignments. A report on vacancies is positions
with no current assignment. Succession cover is a link from a key position to named
backup positions or people, dated.

## Effective dating

Every attribute that can change carries `valid_from` (required) and `valid_to`
(nullable, open-ended). Rules:

1. **Change** a fact by closing the old row (`valid_to` = day before) and inserting a new
   row from the change date. Both rows remain.
2. **Correct** a wrong entry by recording a correction with actor and reason; keep the
   erroneous row marked superseded. Payslips already issued read the dated facts that
   applied then.
3. **No overlaps** for the same key and attribute: enforce with an exclusion constraint
   (PostgreSQL) or a transaction that checks and locks (MySQL).
4. **No gaps** for attributes that must always exist (an active employee always has a
   contract class and a position).
5. **Future-dated changes** are allowed and become current on their date by query, not by
   a job that rewrites rows.
6. Reports take an `as_of` date; the default is today, and payroll uses the period end.

## Job families, levels and grades

- Families group jobs by work type; levels order seniority across families; a pay grade
  attaches to a level (or title) and holds a range, not a person's pay.
- A person's actual pay sits in a dated compensation row with its own permission, and
  must sit inside the grade range or carry an approved exception.
- Titles that carry authority (for example "Manager") are limited by the client's rule;
  store the rule as data so a title change is checked.

## Contract classes

| Class | Typical treatment | Design note |
|---|---|---|
| Employee | Payroll with statutory deductions by parameter | Leave accrual, probation, notice per client policy and verified law. |
| Part-time or fixed-term | Client-set treatment; for one client a withholding tax only, no income-tax payroll deduction and no pension contribution | The treatment is a parameter with a source row. Mark any unverified basis `NOT_VERIFIED` and block until set. |
| Consultant | Invoice-based, not payroll | Lives in procurement and payables; the HR record holds identity, scope and dates only. |

Add a configurable limit for consecutive fixed-term contracts and a required break, with
a warning before the limit and a hard stop at it. Add a disguised-employment review
prompt (control, integration into the staff, exclusivity, tools, duration) that a human
completes and records; the legal test itself is `NOT_VERIFIED` until a lawyer supplies it.

## Imports and seeds

- Load units, then cost centres, families, levels, titles, positions (parents first), then
  people and assignments. Validate each file's parent references before inserting.
- Seed files carry codes, not database ids, so they replay safely.
- Pay amounts load from a separate restricted file by a named person.
- Test with synthetic people. Never place real names, salaries or case data in seeds or
  fixtures held in an engine or shared repository.
