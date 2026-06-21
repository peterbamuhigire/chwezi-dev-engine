---
name: document-spreadsheet-tooling-readiness
description: Check whether this machine can generate and validate Word, PDF, Excel, DOCX, XLSX, spreadsheet, workbook, application register, scoring matrix, price schedule, budget, dashboard, report, proposal, or annex files before promising them.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Document Spreadsheet Tooling Readiness
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

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
