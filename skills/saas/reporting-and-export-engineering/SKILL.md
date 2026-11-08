---
name: reporting-and-export-engineering
description: Use when building or reviewing the engineering behind reports, dashboards and exports - metric catalogue, reconciliation, generation records, export jobs, CSV or XLSX formula-injection safety, A4 PDF output and report access - to the Chwezi Reporting and Dashboards Standard. Not for workbook styling, SaaS metric choice or chart visual design.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Reporting and Export Engineering
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

A report is a decision system: it states the question, uses trustworthy data, shows the evidence,
supports an action, exports faithfully and leaves an auditable record. A handsome report with a
wrong total is a defect. This skill is the engineering procedure for the Chwezi Reporting and
Dashboards Standard 1.0.0 (adopted 8 Nov 2026, owner Peter Bamuhigire, Chwezi Core Systems). The
standard travels with this skill as a local copy, so the engine works on its own:
[doctrine](references/reporting-standard-doctrine.md) and the full
[rules and gates catalogue](references/rules-and-gates.md) with every `RPT-<AREA>-NNN` rule. The
visual layer (type, colour, chart styling) is maintained in `chwezi-design-engine`; nothing here
requires it to run.

<!-- dual-compat-start -->
## Use When

- Building or changing a dashboard, KPI tile, analytical screen, register with totals, financial
  statement, daily close, night audit, scheduled report, report centre, PDF or print output, or
  CSV or XLSX export in a Chwezi app or system.
- Defining a metric catalogue or semantic measure layer, or explaining why two screens disagree.
- Designing export jobs, generation records, share links, download audit or report permissions.
- Reviewing a reporting diff for reconciliation, scope, export safety, print or leak defects.
- Writing the data side of an AI or written narrative built from product figures.

## Do Not Use When

- Workbook styling, formulas, charts and finance workbooks for analysts: `excel-spreadsheets`
  (keep the safety rules here).
- Choosing which SaaS business metrics to track (MRR, churn, NRR): `saas-business-metrics`;
  return here to write each chosen metric's contract.
- Visual chart and dashboard design (type, colour, layout): the design engine.
- Ledger posting logic: `saas-accounting-system` or `accounting-engine`; this skill reconciles to
  the ledger, it does not post.
- Document number allocation: `tenant-document-numbering`; reports only show numbers as issued.
- Generic telemetry dashboards for operations: `observability-monitoring`.

## Required Inputs

| Input | Source | If absent |
|---|---|---|
| Decision the report supports, users and roles, output contract | Product owner, requirements | Stop; write the report contract first (RPT-PURPOSE-001) |
| Existing reports, metric code, permission map, export and print services | Repository search | Inspect before designing; never assume a greenfield |
| Metric definitions and their business owner | Finance or domain owner | Draft contracts marked `draft`; a headline cannot ship (RPT-GATE-02) |
| Ledger or source of truth to reconcile to | Accounting module, posting tables | Reconcile to detail only; mark ledger reconciliation `NOT_ASSESSED` |
| Production-scale dataset shape and baseline device | Ops, product profile | Design budgets; mark performance `NOT_ASSESSED` |
| Tenant model and server-side auth context | `multi-tenant-saas-architecture` | Stop; never take tenant or branch from the request alone |

## Workflow

1. **Inspect.** Read the existing reports, measure code, permission map, export and print code,
   and any web counterpart the app must match.
2. **Write the report contract.** Decision, users, output contract (operational dashboard,
   analytical workspace, fixed report, executive narrative), the five reporting questions it
   answers, metrics, grain, period, filters, states, export targets, acceptance tests. Register it
   ([registry entry](references/generation-records-and-export-jobs.md)).
3. **Define or reuse metric contracts** in the versioned catalogue and compute them once, on the
   server, in the semantic layer. Load [metric contract and semantic layer](references/metric-contract-and-semantic-layer.md).
4. **Model facts and dimensions** with declared grain; add a fan-out test for every join.
5. **Build the API** returning values with unit, currency, period, completeness, freshness,
   reconciliation status and variance status; amounts as decimal strings.
6. **Build screen and print separately** from the same canonical dataset. Load
   [print pipeline and acceptance](references/print-pipeline-acceptance.md).
7. **Build exports** with the neutraliser, typed cells and metadata sheet. Load
   [export safety checklist](references/export-safety-checklist.md).
8. **Add jobs, generation records, permissions, share links and audit.** Same registry reference.
9. **Verify** with the fixture set, reconciliation harness, role matrix, state matrix, print
   cases and budgets. Load [verification, performance and observability](references/verification-performance-and-observability.md).
10. **Review and release.** Independent verifier; human domain reviewer for financial, clinical or
    regulatory reports; known limits and rollback recorded; telemetry watched after release.

## Quality Standards

Gate map. An applicable gate with `NOT_ASSESSED` evidence is open, and an open gate blocks release
whatever the score.

| Gate | Fails when | Engineering control | Also trips (Product Excellence) |
|---|---|---|---|
| RPT-GATE-01 Report does not reconcile | Headline, detail, ledger, PDF and export disagree | Reconciliation harness; one canonical dataset; export total check | PX-GATE-03 |
| RPT-GATE-02 Undefined metric | A headline or exported metric has no approved contract | Versioned catalogue; lint for measure logic in presentation | PX-GATE-09 |
| RPT-GATE-03 Ambiguous scope | Period, timezone, tenant or branch, currency or filters missing; non-comparable comparison | Context row from the API; page-one identity; server-built comparison windows | None (reporting-specific) |
| RPT-GATE-04 Export leak | A file, print, schedule or link exceeds the requester's scope | Row and field filters in query and export service; download-time re-check | PX-GATE-04, PX-GATE-05 |
| RPT-GATE-05 Unsafe spreadsheet | Formula trigger not neutralised; identifiers lose zeros or precision | Neutraliser, typed cells, injection fixture | None (reporting-specific) |
| RPT-GATE-06 Print failure | Screenshot PDF, no repeated headers, orphaned total, no page x of y, text below the floor | Dedicated templates; pagination rules; print acceptance cases | None (reporting-specific) |
| RPT-GATE-07 Ungrounded narrative | A stated figure or cause does not trace to a cited measure and filter; consequential text not approved | Claim-to-evidence table; approval status | PX-GATE-09 |
| RPT-GATE-08 Unknown shown as known | No data, failed reconciliation, missing source or restricted shown as zero, complete or live | Reporting state type; undismissable warning | PX-GATE-02, PX-GATE-10 |

What the Product Excellence gates named above mean, stated here so this skill stands alone:
PX-GATE-02 false confirmation (anything shown as saved, paid, sent or live before the server
confirms it, queued shown as confirmed, stale shown as live); PX-GATE-03 numbers do not reconcile
(money, stock, tax or clinical values differ from the authoritative ledger, or the currency minor
unit is wrong); PX-GATE-04 interface-only authorisation (a restricted action or record reachable
by calling the API with a lower-role session); PX-GATE-05 sensitive data exposed (patient,
payroll, credential or full account data visible without need, unmasked, captured or sent in
analytics); PX-GATE-09 invented content (demo or fixture data in production, or a field or statement with no requirement behind it); PX-GATE-10
missing state (a canonical screen state absent without a declared reason); PX-GATE-12 unverified
release (no independent verifier, or no human domain reviewer for a money or clinical change);
PX-GATE-13 document numbering broken (numbers not contiguous per tenant and type, allocated at
draft or on the client, or a numbered document deleted instead of voided). The release verdict
uses the Product Excellence scorecard: PASS needs 85 or more, no open gate and no dimension
below 2; a high score never buys back a gate. Reporting screens still carry every other Product
Excellence gate through the screen standard, for example PX-GATE-06 accessibility failure (an
applicable WCAG 2.2 AA failure, or a core task that cannot be finished with a screen reader or
keyboard).

Owner rules that bind every report:

- Never sum quantities across different units; total per unit or convert to value with the
  method stated (owner rule, 7 Nov 2026; RPT-METRIC-003).
- Full amounts use the currency's ISO 4217 minor unit: UGX and RWF 0 decimals, KES, TZS and USD
  2. Compact K, M and B forms never appear on a closing balance, statement total or payment
  figure, nor in an export data cell.
- Document numbers are shown exactly as issued, contiguous per tenant and document type; a
  report never renumbers, and voided documents stay listed as void.
- Dates read `4 Nov 2026` on screen and in print; no raw keys, internal codes or ISO strings in
  front of people (CSV machine columns may carry ISO 8601 with offset).
- Revenue, cash collected and profit are separate measures with separate labels (RPT-METRIC-006).

## Anti-Patterns

- Computing net sales in the screen, again in the PDF code and again in the export. Fix: one
  server measure layer; presentation formats only (RPT-METRIC-002).
- A dashboard tile on payment date beside a report on issue date, both labelled "Sales". Fix:
  two contracts, two labels.
- Joining invoice lines to a many-valued tag table and summing. Fix: fan-out test; bridge or
  separate view.
- Printing the dashboard to PDF. Fix: dedicated A4 template (RPT-PRINT-001).
- Hiding the cost column in the UI while the export query returns it. Fix: field filter in the
  export service (RPT-SEC-001).
- Writing `=HYPERLINK(...)` customer notes straight into CSV, or numbers as text. Fix: neutraliser
  and typed cells ([checklist](references/export-safety-checklist.md)).
- Showing 0 when a branch has not synced. Fix: `Partial` or `NoData` state with the reason.
- A dismissible "figures may not match" banner. Fix: undismissable reconciliation warning.
- An AI summary saying "sales fell because of the rain". Fix: claim table citing measure, filter
  and period; observation separated from inference; no cause from correlation (RPT-NARR-001/002).
- Claiming "PDF/UA compliant" in a footer. Fix: claim only after validator and manual review.
- Customer names in export file names or object keys. Fix: deterministic, privacy-safe names.
- A universal "reports load in 200 ms" promise. Fix: measured budgets per device and dataset.

## Outputs

- Report contract and registry entry per report.
- Metric contracts (versioned) and the semantic-layer queries.
- API contract with reporting states, completeness, freshness and reconciliation fields.
- Print templates per page system; export schemas with metadata sheets.
- Job, generation-record, permission, share-link and audit design.
- Verification evidence: RECON, EXPORT, PRINT, UIT, SHOT, AT, TRACE, REVIEW.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | Metric contracts and reconciliation report | YAML plus RECON report | `metrics/sales/net_sales.yaml`, `evidence/reports/daily-close-recon.md` |
| Security | Role x endpoint denial matrix for view, export, print, schedule, share | Test report | `evidence/reports/export-denials.txt` |
| Data safety | Spreadsheet injection and leading-zero fixture result | Test report plus opened-file notes | `evidence/reports/export-injection.md` |
| UX quality | Print acceptance pack, every page at 100% and greyscale | PDFs plus reviewer note | `evidence/reports/print/daily-close/` |
| Performance | Budget record and traces on the baseline device | Trace files plus budget table | `evidence/reports/perf-budget.md` |
| Release evidence | RPT and PX gate table with MEASURED or NOT_ASSESSED per gate | Markdown checklist | `evidence/reports/gate-table.md` |

## References

- [Reporting standard doctrine (local copy)](references/reporting-standard-doctrine.md): output
  contracts, five questions, precedence, the eight gates, owner rules, change control.
- [Rules and gates (local copy)](references/rules-and-gates.md): every RPT rule with level,
  gate, check and evidence code.
- [Metric contract and semantic layer](references/metric-contract-and-semantic-layer.md):
  contract template, measure layer, grain and fan-out tests, reconciliation harness, periods,
  worked example.
- [Export safety checklist](references/export-safety-checklist.md): formula injection, typed
  cells, identifiers, schema, metadata, export authorisation.
- [Print pipeline and acceptance](references/print-pipeline-acceptance.md): A4 pipeline, page
  anatomy, pagination, legibility, PDF/UA and PDF/A profiles, acceptance cases.
- [Generation records and export jobs](references/generation-records-and-export-jobs.md):
  registry, generation record schema, jobs, file names, delivery and audit.
- [Verification, performance and observability](references/verification-performance-and-observability.md):
  fixtures, state type, budgets, caching, telemetry, tenant isolation.
- Companions: `excel-spreadsheets`, `saas-business-metrics`, `ai-analytics`,
  `python-data-analytics`, `multi-tenant-saas-architecture`, `tenant-document-numbering`,
  `saas-accounting-system`, `observability-monitoring`, `frontend-architecture`
  (product-excellence engineering gates), `professional-word-output` (its report-print-pdf
  reference for mPDF and browser print), `document-spreadsheet-tooling-readiness`.

<!-- dual-compat-end -->
- Local copies of the standard's shared references, identical to the canonical text, so this
  engine also carries the screen, print and verification guidance:
  [metric contract and reconciliation](references/metric-contract-and-reconciliation.md),
  [screen composition and components](references/screen-composition-and-components.md),
  [report blueprints](references/report-blueprints.md),
  [print, export and lifecycle](references/print-export-and-lifecycle.md),
  [engineering and verification](references/engineering-and-verification.md) and the
  [currentness register](references/currentness-register.md).
- Local copy of the Chwezi Document Reporting and Publishing Standard 1.0.0 for renderer work
  (one canonical model for HTML, print CSS, PDF and DOCX; output parity; DOCX round trip;
  deterministic, content-hashed outputs; optimal page breaking; largest-remainder rounding):
  [standard](references/document-publishing-standard/standard.md),
  [rules and gates](references/document-publishing-standard/rules-and-gates.md),
  [renderer contracts](references/document-publishing-standard/page-and-render-pipeline.md),
  [mathematics and algorithms](references/document-publishing-standard/mathematics-and-algorithms.md),
  [agent contract and QA](references/document-publishing-standard/agent-contract-and-qa.md),
  [blueprints](references/document-publishing-standard/families-and-blueprints.md).

## Capability and permission contract

Default to read-only inspection and design. Edit report, export or template code only when the
task authorises it. Run reconciliation and export tests against fixtures or a disposable copy,
never against production; read-only production queries need explicit approval. Never place one
tenant's figures, names or file paths in another tenant's output, log or error message.

## Degraded mode

Without the ledger, reconcile headline to detail and mark the ledger leg `NOT_ASSESSED`. Without a
renderer or spreadsheet program, deliver templates and fixtures as a plan and mark PRINT and
EXPORT `NOT_ASSESSED`. Without the baseline device, record budgets as targets, not results.
Without the metric owner, ship contracts as `draft` and keep the affected figures off release.

## Decision rules

| Condition | Action | Failure avoided |
|---|---|---|
| Two surfaces show the same label with different values | Trace both to contracts; split labels or unify the measure | Owner distrust of every figure |
| A report spans a price, category or rate change | Use values valid on the transaction date | Last year's report changing |
| Mixed units in a quantity column | Total per unit or convert to value with the method stated | Meaningless sums |
| Output exceeds the queue threshold or is a multi-page PDF | Background job with record, progress and expiry | Timeouts and partial files |
| A schedule's owner loses a permission | Next run fails closed and notifies the owner | Data sent beyond current rights |
| The current period is incomplete | Mark it and compare like-for-like windows | False declines |
| Reconciliation fails | Undismissable warning with amount, cause and last good time | Hidden mismatch |
| A narrative is financial, clinical or regulatory | Human approval and visible status before release | Ungrounded advice |

## Sources

Self-contained; prepared on 8 Nov 2026 from the Chwezi Reporting and Dashboards Standard 1.0.0
(Chwezi Core Systems' own standard, design bible Edition 1.0, November 2026) and engineering
practice. External facts (OWASP CSV Injection guidance read 8 Nov 2026; PDF/UA and PDF/A
profile dates checked where a source could be read, otherwise `NOT_ASSESSED`) are recorded in
`docs/updates/2026-11-08-reporting-and-dashboards-standard.md`; review by 8 Feb 2027.
