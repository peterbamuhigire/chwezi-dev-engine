# Worked example: handing an organisation structure to a SaaS team

A software company prepared its own organisation for first use of an HR product that
already had tables for units, cost centres, families, levels, grades, titles and
positions. No new features were requested; the aim was real use and feedback.

## What was handed over

| File | Loads into | Notes |
|---|---|---|
| `org_units.csv` | `org_units` | Root company, divisions, departments, plus an office-of-the-head unit. |
| `cost_centers.csv` | `cost_centers` | One per department. |
| `job_families.csv` | `job_families` | A handful of families. |
| `job_levels.csv` | `job_levels` | Ten levels; `rank` equals the level number. |
| `job_titles.csv` | `job_titles` | Each with family, level and a pay-grade code only. |
| `positions.csv` | `positions` | Each with title, unit, reporting position, headcount, budget status, status. |
| seed JSON | all above | Same data in one file for a seed script. |
| Restricted grades file | `pay_grades` | Held back; loaded by one named person. |

## Lessons that became rules

1. **Positions are filled as the company grows.** Most positions started `planned` or
   `vacant`; the chart showed the target state, not today's staff.
2. **Reporting lines between positions**, so a departing manager left no orphaned reports.
3. **Pay stayed out of the shared package.** Titles carried only the grade code.
4. **Part-time roles** existed as a class with a different tax treatment and a limit on
   consecutive contracts; all costing in plans used full-time cost only.
5. **The product was in testing.** The handoff said so: no real payroll, no reliance on
   statutory figures.
6. **Feedback was part of the job.** Every misfit, long entry path or unclear screen was
   to be noted for the product plan.
7. **Only heads of department carried "Manager"** in titles, enforced as a data rule.

Names, salaries and individual records stay out of engine examples. Use synthetic data.
