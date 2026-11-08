Parent skill: [reporting-and-export-engineering](../SKILL.md)

> Local copy of the Chwezi Reporting and Dashboards Standard 1.0.0, kept identical to the version
> in chwezi-design-engine; this engine works without that repository.

# Report blueprints

Use this reference to start a report contract for a known domain. Each blueprint gives the
decision, users, the 3-5 measures that earn the headline row, the screen modules and the A4
output. Every blueprint inherits the same contract: the context row, the reporting states, drill
to records, one dominant analysis, separate A4 composition, and the acceptance tests in
[rules-and-gates.md](rules-and-gates.md). Measures named here still need their own metric
contracts ([metric-contract-and-reconciliation.md](metric-contract-and-reconciliation.md)).

## Screen blueprints

### Retail, restaurant, pharmacy, hotel and stock (Maduuka families first)

| # | Blueprint | Users | Decision | Headline measures | Screen modules | A4 output |
|---|---|---|---|---|---|---|
| B03 | Sales and POS close | Cashier supervisor, owner | Can the shift or day be closed safely? | Gross and net sales, refunds and voids, cash variance, tax | Shift summary; payment reconciliation by method; void and refund register; sign-off | Portrait daily sales and cashier reconciliation with signature |
| B04 | Restaurant service and kitchen | Restaurant manager | Where is service delayed? | Tickets, preparation time, covers, wastage | Service status; active orders; category performance; anomalies | Landscape service and wastage review with reason codes |
| B05 | Pharmacy stock and dispensing | Pharmacist, stock controller | Which items risk stock-out or expiry? | Available stock, near-expiry batches, claims, returns | Critical stock alerts; batch list; reorder action; sales trend | Portrait batch, expiry and reorder register; sensitive records masked by role |
| B06 | Hotel operations and night audit | Front desk, hotel manager | Are room and revenue records reconciled? | Occupancy, average daily rate, revenue per available room, deposits, no-shows | Arrivals and departures; room status; revenue; exceptions | Portrait night audit with exceptions and sign-off; housekeeping assignment sheet |
| B07 | Inventory and reorder | Storekeeper, procurement | What must be reordered, and why? | On hand, available, inbound, demand, lead time | Alert strip; replenishment table; supplier context | Landscape replenishment proposal; inventory valuation |
| B27 | Stock count variance | Inventory auditor | Where do physical and system counts differ? | Expected, counted, variance (per unit and value), approval | Count batches; exception list; approvals | Stock count and adjustment authorisation |
| B08 | Procurement and supplier performance | Procurement lead | Where are orders late or expensive? | Purchase order value, lead-time variance, fulfilment | Pipeline; late receipts; supplier ranking; detail | Landscape supplier performance and open order schedule |
| B02 | Branch and franchise comparison | Regional manager | Which outlet needs intervention? | Sales, margin, conversion, variance, stock-out rate | Branch selector; comparable ranking; small multiples; exception drill-down | Landscape branch comparison with definitions |

### Finance

| # | Blueprint | Users | Decision | Headline measures | Screen modules | A4 output |
|---|---|---|---|---|---|---|
| B09 | Income statement | Finance officer, director | What profit was earned in the period? | Revenue, cost of goods, gross profit, expenses, net result | Period selector; comparative lines; drill-through | Portrait formal statement with comparative period and basis |
| B10 | Balance sheet | Accountant, auditor | Does the financial position balance? | Assets, liabilities, equity, working capital | Hierarchical statement; notes; balance check | Portrait balance sheet and notes |
| B11 | Cash flow and liquidity | Treasurer, finance manager | Can obligations be met? | Inflows and outflows, runway, overdue receivables and payables | Cash bridge; forecast; ageing; exception actions | Cash flow report with assumptions |
| B12 | Budget versus actual | Budget owner, finance | Where are the material deviations? | Budget, committed, actual, forecast, variance | Variance cards; hierarchical rows; drill-down | Landscape budget variance with explanations |
| B13 | Receivables and collections | Credit controller | Which balances need collection? | Current, 30, 60, 90+ days, disputed | Ageing cards; ranked customers; follow-up actions | Landscape ageing schedule and follow-up register |
| B14 | Payables and obligations | Accounts payable | Which payments are due or disputed? | Due amount, ageing, approval state, discounts | Due calendar; vendor list; risk flags | Portrait payables and payment proposal |
| B17 | Payroll reconciliation | Payroll manager | Does payroll reconcile and is it approved? | Gross pay, deductions, net pay, exceptions | Payroll totals; exceptions; sign-off | Restricted payroll summary and detailed schedule |

### Other Chwezi product families

| # | Blueprint | Users | Decision | Headline measures | Screen modules | A4 output |
|---|---|---|---|---|---|---|
| B01 | Executive performance | Executive, general manager | Is the business healthy; what is urgent? | Revenue, margin, collections, open risks | KPI row; trend comparison; top drivers; exceptions; actions | Executive scorecard with management commentary |
| B15 | Property and rent roll | Property manager, owner | Which properties underperform? | Occupancy, billed rent, collections, arrears | Property overview; arrears ranking; maintenance | Landscape owner statement and rent roll |
| B16 | HR attendance and leave | HR officer, supervisor | Which approvals and anomalies need action? | Attendance, overtime, leave balances, exceptions | Approvals queue; attendance pattern; audit trail | Leave and attendance register |
| B18 | Healthcare operations | Clinical manager | Where are queues and service risks? | Waiting times, appointments, lab turnaround, claims | Priority queue; schedule; service measures | Restricted operational report with minimum patient data |
| B19 | Education and learning | School administrator | Which learners or cohorts need support? | Attendance, results, fees, completion | Cohort overview; risk list; timetable | Cohort progress and attendance report |
| B20 | Construction job costing | Project manager, quantity surveyor | Which jobs threaten margin? | Estimate, committed, actual, cost to complete, estimate at completion | Job cost hierarchy; variance; change orders | Landscape job cost and estimate to complete |
| B21 | Project portfolio capacity | Portfolio director | Can resources meet planned demand? | Demand, capacity, utilisation, risk | Scenario comparison; role bottlenecks; action tree | Landscape capacity decision paper with assumptions |
| B22 | CRM pipeline | Sales manager | Where are deals stalled? | Stage conversion, pipeline value, weighted forecast | Funnel; stale deals; follow-up list | Pipeline and forecast review |
| B23 | Customer support scorecard | Service manager | Are service commitments met? | SLA, first response, resolution, satisfaction (with sample size) | Scorecard; channel trends; case exceptions | Monthly service scorecard and action plan |
| B24 | Marketing campaign return | Marketing lead | Which campaigns generate value? | Impressions, clicks, click rate, cost per click, cost per acquisition, revenue | Channel comparison; attribution caveats; funnel | Campaign effectiveness report with attribution caveats |
| B25 | Report centre and scheduling | Report administrator | Which reports exist, run and fail? | Schedules, runs, deliveries, failures | Catalogue; job queue; schedule list; audit | Reporting governance register |
| B26 | Document and export audit | Compliance officer | Who accessed or exported sensitive data? | Downloads, shares, denials, retention | Audit table; filters; event preview | Restricted access and export audit |
| B28 | Multi-tenant owner portfolio | SaaS owner, franchise administrator | Which tenants or outlets need support? | Usage, sync health, incidents, billing | Tenant status; alerts; trends; access guardrails | Tenant operations summary |

## Domain data notes

What each domain's data model must define before its reports can reconcile:

| Domain | Must be defined |
|---|---|
| Sales and POS | Gross, discounts, returns, tax, net; receipts by method; cashier, outlet, product, shift; refund exceptions |
| Restaurant and bar | Covers, item sales with modifiers, voids, discounts, kitchen time, wastage, stock depletion through recipes, split payments |
| Pharmacy | Batch and expiry, dispensing, controlled-item restrictions, insurance claim status, stock-outs, margin, returns |
| Hotel | Occupancy, rates, room revenue, housekeeping turnaround, reservations, no-shows, deposits, night audit |
| Inventory and procurement | On hand vs available vs reserved, reorder level, demand, lead time, order pipeline, receipts, supplier performance, valuation method |
| Finance | Statements, receivable and payable ageing, bank reconciliation, budgets, cost centres, ledger drill-down, basis of accounting |
| Property | Rent roll, occupancy, arrears ageing, maintenance cost, deposits, work orders, lease expiries |
| Healthcare | Appointments, patient flow, claims, lab turnaround, billing, privacy-sensitive alerts |
| HR and payroll | Headcount, attendance, leave approvals, payroll totals, deductions, contracts, attrition |
| Projects and construction | Estimate, actual, committed, cost to complete, margin, variations, schedule |
| Education | Attendance, enrolment, fees, assessment, progress, safeguarding restrictions |
| CRM and support | Pipeline stages, conversion, case ageing, SLA, satisfaction with sample size, escalation |
| Marketing | Reach, impressions, engagement denominator, click and cost measures, conversions, attribution model (organic vs paid) |
| Portfolio and capacity | Demand, capacity in full-time equivalents, utilisation, skills, scenario assumptions |

## Lessons from the reference set

The 29 reference designs studied for the source bible showed recurring strengths (clear KPI rows,
modular grids, rich operational tables, narrative context) and recurring faults that these
blueprints correct: inconsistent sample arithmetic, tiny labels, too many panels, ambiguous dates,
unlabelled units, colour-only status, 3D charts, budget figures that did not add up, statements
crammed onto one page, invoice deletion without an audit trail, and untested A4 layouts. Their
figures are never reused.
