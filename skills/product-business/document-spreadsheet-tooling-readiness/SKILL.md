---
name: document-spreadsheet-tooling-readiness
description: Use when checking whether this machine can generate and validate requested DOCX, PDF, XLSX, workbook, register, budget, or dashboard outputs.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Document Spreadsheet Tooling Readiness
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.


## Required Inputs

| Input | Required | Use |
|---|---|---|
| Decision, audience, and deliverable | yes | Bound the business outcome |
| Source evidence, constraints, and owner | yes | Ground recommendations and accountability |
| Approved budget, customer data, or production artefacts | conditional | Support high-impact execution |

## Capability and permission contract

Default to read-only analysis and drafting. Do not publish, send, price, promise, alter customer records, commit budget, or modify production artefacts without explicit authority and a named approver. Minimise confidential data, preserve provenance, and keep reversible copies.

## Degraded mode

If evidence, stakeholder decisions, specialist tooling, or authoritative commercial data are unavailable, deliver a labelled draft, checklist, or decision memo. State what was not verified and do not claim approval, publication, financial accuracy, or customer acceptance.

## Decision rules

| Condition | Action | Stop condition |
|---|---|---|
| Output creates a commercial, customer, or delivery commitment | Obtain named approval before release | Authority or terms are unclear |
| Evidence supports a reversible draft | Produce it with assumptions and owner | Required evidence conflicts |
| Tooling or data is incomplete | Specify validation | A final executable artefact is expected |

## Domain Anti-Patterns

- Inventing customer evidence, prices, benchmarks, or approvals. Fix: cite the source or mark the gap.
- Publishing or sending a draft without authority. Fix: retain draft status and name the approver.
- Hiding assumptions inside polished prose. Fix: expose them beside each affected decision.
- Polishing presentation while the decision remains unclear. Fix: resolve audience, owner, and acceptance criteria.
- Treating unavailable tooling as passed validation. Fix: record the unassessed check.


<!-- dual-compat-start -->
## Use When

- Before promising or creating `.docx`, `.pdf`, `.xlsx`, application registers, scoring matrices, budgets, dashboards, price schedules, CV packs, reports, or annexes.
- When moving an engine to a new machine and confirming whether document/spreadsheet tooling is installed.

## Do Not Use When

- The user only asks for plain Markdown or a conceptual outline and no generated file is claimed.

## Required Inputs

- Desired output formats, local tooling access, plugin/connector availability, and any required templates.

## Workflow

- Check plugins/connectors first, then Python packages, then binaries.
- Run a one-file smoke test before production export.
- Choose a route and state fallback honestly.
- Never claim a file exists until it was generated and opened or validated.

## Quality Standards

- File-output claims are factual claims.
- Fallbacks are explicit, not silent.
- PDF conversion route must be known before promising PDF.

## Anti-Patterns

- Saying a Word, PDF, or Excel file was generated when only Markdown exists.
- Assuming LibreOffice, Pandoc, or a plugin exists without checking.
- Shipping a workbook without reopening or formula/control checks.

## Outputs

- Toolchain check, smoke-test result, route decision, fallback plan, and validation note.

## References

- `references/toolchain-checks.md`: Commands and package/binary checklist.
- `references/fallback-routes.md`: Output routes and fallback decision tree.
<!-- dual-compat-end -->

## Core Workflow

1. Confirm requested formats and whether a generated file is actually required.
2. Prefer built-in document/spreadsheet plugins where available.
3. Check Python packages: openpyxl, XlsxWriter, pandas, python-docx, docxtpl, docxcompose, pypandoc, markdown, beautifulsoup4, lxml, pillow, PyMuPDF, pypdf, pdfplumber, reportlab.
4. Check binaries: pandoc, soffice/LibreOffice, wkhtmltopdf where needed, and tesseract for OCR tasks.
5. Run a minimal DOCX and XLSX smoke test before production output on a new machine.
6. Pick the generation route and record it in the deliverable notes.
7. Open, parse, or otherwise validate the generated file before telling the user it was created.
