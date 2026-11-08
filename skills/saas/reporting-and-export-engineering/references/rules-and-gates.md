Parent skill: [reporting-and-export-engineering](../SKILL.md)

# Rules and gates

> Local copy of the Chwezi Reporting and Dashboards Standard 1.0.0, kept identical to the version
> in chwezi-design-engine; this engine works without that repository.

Every normative rule of the Chwezi Reporting and Dashboards Standard, version 1.0.0, adopted
8 November 2026. Binding text: [reporting-standard-doctrine.md](reporting-standard-doctrine.md)
(local copy of `doctrine/reporting-and-dashboards-standard.md`). Rule IDs, levels, gates, checks
and evidence codes below are identical to the design-engine copy so the two engines agree; only
links and the two local glossaries are adapted to this engine.

## How to read this catalogue

- **ID** `RPT-<AREA>-NNN` is stable and never reused. **Lvl**: MUST, SHOULD (departure needs a
  DDR), MAY, with the Product Excellence meanings. **Gate**: the hard gate a failure trips (blank =
  scored finding with an owner and a date).
- **Ev** uses the Product Excellence evidence codes (SHOT, UIT, TRACE, AT, LINT, CONTRACT, REVIEW,
  RECON, NET, STUDY, FIELD) plus two reporting codes: **PRINT**, every page of the rendered A4 PDF
  inspected at 100% and in greyscale, with the reviewer named; **EXPORT**, a sample CSV or XLSX
  opened in a spreadsheet program and checked against the screen totals.
- Numbers marked "Chwezi value" are internal starting values, not external facts; a product may
  replace them through a DDR.

### Local glossary (this engine)

The Product Excellence terms used above, stated here so this file stands alone:

| Term | Meaning |
|---|---|
| MUST | Required, observable and binary. A failure on a gate-mapped rule blocks release; any other MUST failure is a scored finding with an owner and a date. Never quietly skipped. |
| SHOULD | The default. A departure needs a design decision record (DDR): problem, at least two alternatives, choice, trade-offs, evidence, owner, review date. |
| MAY | Optional good practice; no record needed. |
| SHOT | Screenshot set at stated widths, themes, text scale and locale |
| UIT | Automated UI, unit or integration test result |
| TRACE | Trace or benchmark from the declared baseline device |
| AT | Assistive-technology or keyboard run log |
| LINT | Guardrail, static or dependency check output |
| CONTRACT | Screen, component, metric or report contract file |
| REVIEW | Recorded checklist review with the reviewer named |
| RECON | Reconciliation report against the ledger or source records |
| NET | Network, log or analytics capture |
| STUDY | Usability study or timed task log |
| FIELD | Field report from the real environment after release |

Evidence states: facts are `VERIFIED`, `CHANGED` or `NOT_ASSESSED`; release evidence is
`MEASURED`, `HEURISTIC` or `NOT_ASSESSED`. Only `MEASURED` closes a hard gate.

## Hard gates

| Gate | Short name | Main rules |
|---|---|---|
| RPT-GATE-01 | Report does not reconcile | RPT-RECON-001/002/003, RPT-EXPORT-006 |
| RPT-GATE-02 | Undefined metric | RPT-METRIC-001/002 |
| RPT-GATE-03 | Ambiguous scope | RPT-SCOPE-001/002, RPT-PERIOD-001/002, RPT-PRINT-002 |
| RPT-GATE-04 | Export leak | RPT-SEC-001/002/003 |
| RPT-GATE-05 | Unsafe spreadsheet | RPT-EXPORT-002/003 |
| RPT-GATE-06 | Print failure | RPT-PRINT-001/002/003/004/005 |
| RPT-GATE-07 | Ungrounded narrative | RPT-NARR-001/002/003 |
| RPT-GATE-08 | Unknown shown as known | RPT-STATE-001/002/003 |

## Purpose and output contract (PURPOSE)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-PURPOSE-001 | MUST | | Every reporting surface has a written decision statement, primary users and roles, and one declared output contract (operational dashboard, analytical workspace, fixed report, executive narrative). | Report contract names all four items | CONTRACT |
| RPT-PURPOSE-002 | MUST | | Each widget, chart or section answers at least one of the five reporting questions; anything that answers none is removed. | Widget register lists the question per element | CONTRACT |
| RPT-PURPOSE-003 | SHOULD | | Screen order follows the five questions: what happened, why, what is at risk, what to do, how confident. | Review against contract | REVIEW |
| RPT-PURPOSE-004 | MUST | | Screen and A4 compositions are designed as separate products from the same canonical dataset. | Separate screen and print layouts exist | CONTRACT, PRINT |

## Metrics (METRIC)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-METRIC-001 | MUST | 02 | Every headline, exported or scheduled metric has an approved, versioned metric contract: identifier, business question, definition, numerator, denominator, inclusions and exclusions, unit, currency, rounding, date basis, grain, source, owner, freshness target, privacy class, comparison logic and validation tests. | Contract file per metric, approved by its owner | CONTRACT |
| RPT-METRIC-002 | MUST | 02 | Interfaces and exports read approved measures from one controlled layer; no screen recomputes a measure such as net sales on its own. | Code search finds no duplicate measure logic in presentation code | LINT, UIT |
| RPT-METRIC-003 | MUST | | Quantities in different units are never summed into one figure; totals are per unit or converted to value with the method stated. | Fixture with mixed units yields no cross-unit total | UIT |
| RPT-METRIC-004 | MUST | | Facts are kept apart from dimensions with declared keys and grain; joins are tested for fan-out and double counting. | Test with a one-to-many dimension leaves totals unchanged | UIT |
| RPT-METRIC-005 | SHOULD | | Historical exchange rates and slowly changing dimensions are used where a report spans changes in rate, price, branch or category. | Back-dated fixture reproduces historical totals | UIT |
| RPT-METRIC-006 | MUST | | Revenue, cash collected and profit are distinct measures; gross and net, discounts, tax, refunds, returns, voids, cost of goods, and accrual or cash basis are stated in each contract that uses them. | Contract review | CONTRACT, REVIEW |

## Scope and filters (SCOPE)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-SCOPE-001 | MUST | 03 | A persistent context row shows organisation, branch or outlet, exact period with dates, timezone, currency, data freshness and the active filters. | Screenshot at every width class | SHOT |
| RPT-SCOPE-002 | MUST | 03 | Filters are typed parameters with a stated scope (global or widget-local); applying one updates every scoped widget together; active filters are visible as a summary; reset returns to a documented default; the date scope never changes silently. | Interaction test | UIT |
| RPT-SCOPE-003 | SHOULD | | Saved views are offered for repeated analytical tasks. | Feature present or DDR | REVIEW |

## Periods and variance (PERIOD)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-PERIOD-001 | MUST | 03 | A comparison period is comparable: same duration, fiscal or calendar boundaries stated, same timezone, comparable weekday mix where trading depends on it. Month-to-date is never compared with a whole prior month without a label saying so. | Fixture comparing MTD with prior month shows the label | UIT, SHOT |
| RPT-PERIOD-002 | MUST | 03 | An incomplete period is marked as incomplete wherever it appears. | Current-day fixture shows the mark | SHOT |
| RPT-PERIOD-003 | MUST | | Variance is computed as actual minus baseline; favourable or adverse is decided by the metric's direction rule (expense over budget is adverse, revenue over budget is favourable), never by sign or by red alone. | Variance component test with both metric types | UIT |
| RPT-PERIOD-004 | MUST | | Percentage changes and percentage-point changes are never mixed; a change from zero reads "New this period". | Formatter tests | UIT |

## Reconciliation (RECON)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-RECON-001 | MUST | 01 | Each headline figure reconciles to its detail records and, where a ledger exists, to the ledger, for positive, zero, negative, reversed and missing-data cases. | Reconciliation run with all five fixture types | RECON |
| RPT-RECON-002 | MUST | 01 | A difference that cannot be resolved is shown as a reconciliation warning with the amount and the cause if known; it is never hidden or absorbed. | Forced-mismatch fixture shows the warning | UIT, SHOT |
| RPT-RECON-003 | MUST | 01 | Screen, PDF and spreadsheet values originate from the same canonical dataset; only formatting differs. | Compare the three outputs for one scope | RECON, EXPORT, PRINT |
| RPT-RECON-004 | SHOULD | | Drill-down reaches source transactions in a few clear steps, keeping the measure, scope and date context, and returns without losing scroll or filters. | Timed task with an authorised user | STUDY, UIT |

## States and trust (STATE)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-STATE-001 | MUST | 08 | Reporting surfaces implement, in addition to the Product Excellence state matrix: partial data, stale snapshot, reconciliation failure, source disconnected, access restricted and export pending. | State contract and screenshots per state | CONTRACT, SHOT |
| RPT-STATE-002 | MUST | 08 | No data, unknown and restricted are never shown as zero; the empty state says which of them applies and how to recover. | Fixtures for each case | UIT |
| RPT-STATE-003 | MUST | 08 | A failed reconciliation or validation shows a warning that cannot be dismissed until resolved, with the last good snapshot time and a retry. | Dismiss attempt fails | UIT |
| RPT-STATE-004 | MUST | | Freshness shows snapshot time, source lag, incomplete integrations and estimated versus actual values; no unqualified "confidence %" for data quality. | Screenshot review | SHOT |
| RPT-STATE-005 | SHOULD | | Refresh keeps the last valid figures visible with a refresh indicator; skeletons cover only regions awaiting data. | Refresh recording | SHOT |

## Charts, tables and components (VIEW)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-VIEW-001 | MUST | | The first row holds 3 to 5 headline measures; the page follows current situation, trend or comparison, exceptions, then records. | Screenshot review | SHOT |
| RPT-VIEW-002 | MUST | | Chart choice: bars for ranking and magnitude (zero baseline), lines for time, scatter for relationships, heatmaps for matrices; no 3D, no gauge or donut without exact labels; each chart has a precise title, units, period, legend, a text takeaway and a data-table alternative. | Chart review against contract | REVIEW, AT |
| RPT-VIEW-003 | MUST | | Statuses carry a label, a severity and the consequence or action; colour is never the only signal. | Greyscale screenshot | SHOT |
| RPT-VIEW-004 | MUST | | Exception queues sort by consequence and age, and show owner, due date and action. | Fixture order test | UIT |
| RPT-VIEW-005 | MUST | | Funnels and pipelines never mix incompatible stage denominators. | Contract review | CONTRACT |
| RPT-VIEW-006 | SHOULD | | A record preview drawer keeps the list position and focus, and shows only permitted fields. | Keyboard and screen-reader run | AT |
| RPT-VIEW-007 | MUST | | Presentation components contain no domain arithmetic; each has fixtures for normal, extreme-value, missing-data and permission-restricted cases. | Fixture set present; code review | UIT, REVIEW |

## Narrative and AI insights (NARR)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-NARR-001 | MUST | 07 | Every narrative claim cites the measure, filter and period it rests on. | Claim-to-evidence table | REVIEW |
| RPT-NARR-002 | MUST | 07 | Observation is separated from inference; a cause is stated only with supporting evidence, never from correlation alone; uncertainty is disclosed. | Review with the claim table | REVIEW |
| RPT-NARR-003 | MUST | 07 | Consequential financial, clinical or regulatory narrative needs named human approval before release; its status (draft, verified, disputed) is shown. | Approval record | REVIEW |
| RPT-NARR-004 | SHOULD | | Prompt, template and model versions are logged where policy allows. | Log sample | NET |

## Security and privacy (SEC)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-SEC-001 | MUST | 04 | Row-level and field-level authorisation is applied in the query and the export service, before data leaves the server; interface hiding is never the control. | Lower-role session calls the export API directly | UIT, NET |
| RPT-SEC-002 | MUST | 04 | Export, print and schedule rights are separate permissions from view rights where the domain requires; parity with the web permission map is kept. | Permission matrix test | UIT |
| RPT-SEC-003 | MUST | 04 | Share links expire; downloads, scheduled recipients and shares are logged; sensitive personal, payroll and clinical fields stay masked in previews, emails, file names and logs. | Link expiry and log sample | UIT, NET |

## Performance (PERF)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-PERF-001 | MUST | | Aggregation runs on the server; detail is paginated or virtualised; large exports run as background jobs. | Trace with production-scale data | TRACE |
| RPT-PERF-002 | MUST | | Query time, payload size and render time are budgeted per target device and dataset and measured; no invented universal millisecond promise. | Budget record and trace | TRACE |
| RPT-PERF-003 | SHOULD | | Caches state their freshness and are invalidated explicitly. | Cache test | UIT |

## Print and PDF (PRINT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-PRINT-001 | MUST | 06 | A4 output uses a dedicated print template, never a screenshot of the interactive screen; interaction-only controls and hover content are removed. | PDF inspection | PRINT |
| RPT-PRINT-002 | MUST | 03, 06 | Page one carries organisation and branch, title, report ID and version, exact period, basis of accounting where relevant, generation time with timezone, currency, filters and classification; later pages repeat a concise identity; every page shows "Page x of y". | PDF inspection | PRINT |
| RPT-PRINT-003 | MUST | 06 | Table headings repeat on each page; headings are not orphaned; a subtotal stays with its last lines and a total with its label; short records do not split across pages. | Multi-page fixture | PRINT |
| RPT-PRINT-004 | MUST | 06 | Legibility floor at 100% print scale (Chwezi values): body 9 pt, table text 8.5 pt, footnotes 8 pt; a schedule that does not fit drops nonessential columns or moves to a landscape annex instead of shrinking. | PDF inspection | PRINT |
| RPT-PRINT-005 | MUST | 06 | Charts and statuses read in black and white: direct labels or patterns, explicit values; no toner-heavy background blocks without meaning. | Greyscale print | PRINT |
| RPT-PRINT-006 | SHOULD | | Margins start at 15-20 mm (Chwezi values) and are adjusted for binding, printer limits and letterhead; portrait by default, landscape only when content width needs it. | PDF inspection | PRINT |
| RPT-PRINT-007 | SHOULD | | Tagged PDF with reading order, language, headings, table structure, alt text and bookmarks is the target; PDF/UA or PDF/A conformance is claimed only after validation with a checker and a manual review. | Validator report | PRINT, AT |
| RPT-PRINT-008 | MUST | | Print acceptance covers long tables, zero, negative and very large amounts, long names, missing values, more than one currency where supported, right-to-left where supported, and blank or error data. | Fixture set | PRINT |

## Exports and report lifecycle (EXPORT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-EXPORT-001 | MUST | | Data sheets have machine-readable column names, a stable schema, no merged cells and explicit date format and timezone; a metadata sheet or header block carries filters, period, definitions and generation time. | Open the file | EXPORT |
| RPT-EXPORT-002 | MUST | 05 | A text value that begins with `=`, `+`, `-`, `@`, tab, carriage return or line feed, or a full-width form of these, never becomes a formula. CSV: prefix a single quote to such text fields. XLSX: write such values as string-typed cells, never as formulas (no visible apostrophe is added). Numbers are written as numbers, not text. | Injection fixture opened in a spreadsheet program, CSV and XLSX | EXPORT, UIT |
| RPT-EXPORT-003 | MUST | 05 | Identifiers keep leading zeros and full precision (written as text); amounts are written as numbers with the currency in the header. | Fixture with leading-zero codes | EXPORT |
| RPT-EXPORT-004 | MUST | | Large exports run as jobs with progress, retry, expiry and de-duplication of identical requests; file names are deterministic and contain no personal data. | Job test | UIT |
| RPT-EXPORT-005 | MUST | | Each generation writes an immutable record: parameter snapshot, metric versions, source watermark, time, user or service identity, status, checksum and expiry; a scheduled report is distinguished from a downloaded copy. | Generation record sample | UIT |
| RPT-EXPORT-006 | MUST | 01 | Totals in the export equal the screen totals for the same scope. | Compare | EXPORT, RECON |
| RPT-EXPORT-007 | SHOULD | | A report definition registry holds ID, title, description, owner, domain, privacy class, parameter schema, export formats, default sort, allowed roles, metric versions and retention. | Registry entry | CONTRACT |

## Quality assurance (QA)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| RPT-QA-001 | MUST | | Verification uses representative data at production scale, extreme values, restricted roles, keyboard and assistive technology, and the printed A4 output where one exists. | Test log | UIT, AT, PRINT |
| RPT-QA-002 | MUST | | Financial, clinical and regulatory reports are reviewed by a human domain reviewer as well as an independent verifier (Product Excellence PX-GATE-12). | Sign-off | REVIEW |
| RPT-QA-003 | SHOULD | | After release, task completion, misreadings, report failures and feedback are tracked and fed into the next Kaizen cycle. | Metrics record | FIELD |

## Evidence/currentness

External facts behind RPT-PRINT-007 and RPT-EXPORT-002 are recorded in
[currentness-register.md](currentness-register.md). All numeric thresholds in this catalogue are
Chwezi values unless the register says otherwise. Engineering detail for these rules is in
[export-safety-checklist.md](export-safety-checklist.md) and
[print-pipeline-acceptance.md](print-pipeline-acceptance.md).
