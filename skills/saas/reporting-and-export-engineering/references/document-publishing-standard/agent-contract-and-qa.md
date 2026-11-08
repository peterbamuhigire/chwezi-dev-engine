Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Document Reporting and Publishing Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Agent contract, tests and release

Use this reference when an agent, developer or writer produces a document, and when it is tested
and released. Rule IDs: [rules-and-gates.md](rules-and-gates.md).

## Task 1: take the inputs (PUB-AGENT-001)

Name before work starts: report family, audience, purpose, entity, data source, period, currency,
classification, output formats and brand. A missing input is asked for, never invented.

```yaml
document_request:
  report_id: branch.monthly_review
  family: executive_performance_report
  audience: [owner, branch_manager]
  purpose: "Identify sales changes, margin pressure and operational actions"
  entity: {name: "Example Traders Ltd (fictional)", tenant: t_118}
  data_source: snapshot://sales/2026-10/r3     # validated, reconciled
  period: {from: 2026-10-01, to: 2026-10-31, timezone: Africa/Kampala}
  currency: UGX                                # 0 minor digits
  classification: internal
  output_formats: [html_reader, pdf_a4_portrait, docx, pdf_low_ink]
  brand: house-style/default
```

Machine values stay in machine form inside the request; every rendered output shows readable forms
(`31 Oct 2026`).

## Task 2: plan, build and refine (PUB-AGENT-002)

1. **Plan.** Choose the blueprint; draft the outline; map each visual to a reader question; define
   data lineage and validation.
2. **Build.** Create the semantic document model; implement the HTML layout and the PDF and DOCX
   mappings; keep all approved content.
3. **Kaizen, four passes.** (1) Simplify: remove duplicate measures, repeated prose, empty blocks,
   low-information charts and decorative images; replace fact tables with conclusions plus
   inspectable evidence. (2) Improve hierarchy and clarity: specific headings, aligned numbers and
   units, data definitions, exception notes, reading order and contrast. (3) Verify truth: reconcile
   totals, filters, comparison periods and revision metadata; show freshness and incomplete-data
   warnings; add visual and semantic regression tests. (4) Improve consistency and performance:
   central tokens, templates, schema and renderer contracts; reference outputs and page-image
   comparison.
4. **Evidence (PUB-AGENT-004).** Template source, schema mapping, populated example, PDF render,
   DOCX render, visual snapshots, numerical validation log, accessibility findings, known
   limitations, test coverage and unresolved issues.

**Stop conditions (PUB-AGENT-003).** Do not publish when totals mismatch, required data is missing,
sensitive data leaks or the layout is unreadable.

### Example brief (fictional)

| Field | Content |
|---|---|
| Objective | Monthly branch performance review: sales changes, margin pressure, operational actions |
| Audience | Owner and branch manager; one-page executive summary, then supporting evidence |
| Inputs | Validated sales, returns, stock and costs for the selected branches and dates |
| Outputs | Browser report, A4 PDF, editable DOCX, optional low-ink print profile |
| Structure | Summary; sales and margin trend; product and branch contribution; stock risks; actions; appendix |
| Gates | Numbers reconcile; each chart has context; nothing clipped; every export keeps its metadata |

## Task 3: run the financial test cases (PUB-FIN-004 to 007)

| Case | Rule |
|---|---|
| Negative amounts | One minus or parenthesis style throughout; never a negative zero |
| Rounding | Compute from full precision; round only at display; disclose an unavoidable reconciliation difference |
| Missing values | "Not available" with a reason; never silently zero |
| Currency | Currency and scaling shown (UGX, USD); never mixed without an explicit conversion basis |
| Totals | Line sums, subtotals, grand totals, comparative period and source ledger balances verified |
| Auditability | Report ID, source snapshot, prepared date, approver, correction history |

## Task 4: run the edge-case library (PUB-QA-003)

| Area | Cases |
|---|---|
| Volume | 0, 1, 25, 1,000 and 100,000 rows; asynchronous export and pagination |
| Text | Very long company names, multi-line addresses, URLs, accented characters, Arabic right to left |
| Dates | Month end, leap day, timezone boundary, inverted date range |
| Financial | Large numbers, decimals, negative values, zero denominators, mixed currency |
| Graphics | Missing image, wide chart, tall chart, long legend, greyscale printing |
| Lifecycle | Draft, approved, revised, cancelled, superseded, expired download, permission revoked |

## Task 5: pass the acceptance matrix (PUB-QA-002)

| Dimension | Pass when |
|---|---|
| Content | Title, scope, period, units, owner, narrative and references are correct |
| Numbers | Totals, filters, comparison periods, precision and calculations match the validated dataset |
| Layout | No clipping, overlap, orphan heading, broken table, stretched image or hidden text |
| Navigation | Headings, bookmarks, links, contents, page numbers and browser controls work |
| Accessibility | Keyboard, contrast, reading order, alt text, headings and table semantics pass review |
| Export | HTML, PDF, print and DOCX are visually coherent and preserve the same facts |
| Performance | Large reports do not freeze older devices; asynchronous exports report progress and retry safely |
| Security | Tenant boundaries, access controls, document metadata and download expiry are enforced |
| Human approval | Financial, legal, medical and externally issued controlled documents have documented review |

For each dimension the reviewer confirms the required fields and reading order in the browser
preview, the PDF and the DOCX, and records any exception with its approval.

## Task 6: write the QA manifest

```yaml
qa_manifest:
  report_id: branch.monthly_review
  version: 3
  generation_id: gen_01JC9A
  renderer_version: "2.4.1"
  template_version: "exec-report@1.3"
  snapshot: snapshot://sales/2026-10/r3
  parameter_hash: sha256:...
  generated_at: 2026-11-03T09:14:00+03:00
  actor: user_442
  outputs:
    - {format: pdf, pages: 6, inspected_pages: 6, greyscale: true, long_data_fixture: true}
    - {format: docx, pages: 6, reopened_word: true, reopened_libreoffice: true, rerendered_pdf_compared: true}
    - {format: html, viewports: [1440, 1024, 820, 360]}
  matrix: {content: pass, numbers: pass, layout: pass, navigation: pass, accessibility: pass,
           export: pass, performance: pass, security: pass, human_approval: pass}
  gates: {PUB-GATE-01: MEASURED, PUB-GATE-02: MEASURED, PUB-GATE-03: MEASURED, PUB-GATE-04: MEASURED,
          PUB-GATE-05: MEASURED, PUB-GATE-06: MEASURED, PUB-GATE-07: MEASURED, PUB-GATE-08: MEASURED}
  approval: {state: final, by: "Owner (role)", at: 2026-11-03T11:02:00+03:00}
  retention: "per classification (owner to set)"
```

A gate that was not measured is written `NOT_ASSESSED`, which blocks publication.

## Task 7: track the adoption checklist

The handbook's sign-off checklist, with its status in the engines on 8 November 2026:

| Item | Status |
|---|---|
| The standard is approved and version-controlled | Done: adopted on the owner's instruction and versioned 1.0.0 |
| Three golden templates (operational statement, executive analysis, editorial proposal) implemented and visually reviewed | NOT_ASSESSED |
| Every report has a semantic source-to-output data contract | NOT_ASSESSED |
| PDF and DOCX exports preserve all material information and numbers | NOT_ASSESSED |
| A4 output inspected on ordinary office printers and in greyscale preview | NOT_ASSESSED |
| Browser reading usable on desktop, laptop, tablet and mobile | NOT_ASSESSED |
| Security, accessibility and large-report performance gates met | NOT_ASSESSED |
| Owners and reviewers assigned for future template changes | NOT_ASSESSED: the roles are defined in the doctrine; names are for the owner to assign |

## Evidence/currentness

No external fact is cited here. Version numbers, identifiers and times in the examples are
fictional.
