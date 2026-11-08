Parent skill: [reporting-and-export-engineering](../SKILL.md)

> Local copy of the Chwezi Reporting and Dashboards Standard 1.0.0, kept identical to the version
> in chwezi-design-engine; this engine works without that repository.

# Print, export and report lifecycle

Use this reference when a report leaves the screen: A4 print and PDF, CSV and XLSX, scheduled
delivery, share links, and written or AI-generated narrative. Rule IDs:
[rules-and-gates.md](rules-and-gates.md); facts: [currentness-register.md](currentness-register.md).

## Task 1: design the A4 composition

A4 is a separate design product built from the same dataset as the screen; never a screenshot of
the dashboard (RPT-PRINT-001, RPT-PURPOSE-004).

**Geometry.** A4 portrait 210 x 297 mm, landscape 297 x 210 mm. Margins start at 15-20 mm and are
adjusted for binding, printer limits and letterhead. Portrait by default; landscape only when
content width needs it (RPT-PRINT-006).

**Page one anatomy** (RPT-PRINT-002): legal entity and branch; report title; report ID and
version; exact period; basis of accounting where relevant (cash or accrual); generation date and
time with timezone; currency; applied filters; classification (for example "Internal",
"Restricted: payroll"); status (draft, final, revised). Later pages repeat a one-line identity.
Running footer on every page: "Page x of y", report ID, generation time. Optional signature and
approval block at the end.

**Legibility floor at 100% print scale** (RPT-PRINT-004, Chwezi values): body text never below 9 pt
(usual range 9-11 pt), financial tables never below 8.5 pt (usual range 8.5-10 pt), footnotes
never below 8 pt. A schedule that does not fit drops nonessential
columns or moves to a landscape annex. Shrink-to-fit is not allowed.

**Pagination** (RPT-PRINT-003): table headings repeat on every page; a heading never sits alone at
the foot of a page; a subtotal stays with at least its last lines; a total stays with its label;
short records do not split; "brought forward" and "carried forward" appear only where the
business meaning needs them; footnotes stay on the page of the figure they explain.

**Colour and charts** (RPT-PRINT-005): legible in black and white: direct labels, line patterns,
explicit values. Vector charts where the tool allows, otherwise high-resolution images; labels
readable at actual size. No toner-heavy background blocks that carry no meaning.

### The eight page types

| Page type | Orientation | Structure |
|---|---|---|
| Formal financial statement | Portrait | Company identity, title and period, comparative columns, subtotal hierarchy, notes, approval, footer |
| Wide financial schedule | Landscape | Metadata, fixed key columns, grouped money columns, totals, source notes, continuation |
| Executive scorecard | Portrait | One-page summary, 3-5 measures against target, risks, recommended actions, evidence annex |
| Operational register | Portrait or landscape | Exact date and branch, numbered rows, repeated headings, group subtotals, totals, sign-off |
| Analytical management report | Portrait | Main finding, trend figure, interpretation, contributing entities, caveats, next steps |
| Exception and audit report | Landscape | Scope and source watermark, exception summary, detailed register, owner, actions and status |
| Invoice or statement | Portrait | Issuer and recipient, references and dates, lines, taxes and discounts, amount due, terms |
| Board pack | Portrait with landscape annexes | Cover, contents, summary, sections, decisions required, annexes, glossary |

## Task 2: make the PDF accessible and archivable

- Target a tagged PDF: reading order, document language, real headings and table structure, alt
  text for figures, bookmarks for long documents, selectable text (RPT-PRINT-007).
- PDF/UA-1 and PDF/UA-2 are different conformance profiles (PDF/UA-2 is ISO 14289-2:2024, for
  PDF 2.0); PDF/A is a separate archival choice (current edition PDF/A-4, ISO 19005-4:2020). A
  file may aim at both. Claim conformance only after a validator run and a manual check, and
  record both as evidence; otherwise say "designed to the tagged-PDF target, not validated".
- Fonts embedded and licensed for embedding; check the fonts the PDF actually embeds.

## Task 3: test the print

Every report with a print output passes (RPT-PRINT-008): real office printer at 100% (not "fit to
page"), portrait and landscape, a long table over several pages, zero, negative and very large
amounts, long names, missing values, more than one currency where supported, right-to-left where
supported, blank and error data. Compare screen totals with the PDF and the spreadsheet for the
same scope (RPT-RECON-003). Evidence code PRINT: every page inspected, reviewer named.

## Task 4: export to CSV and XLSX safely

| Rule | Why | ID |
|---|---|---|
| Machine-readable column names; stable schema across releases | Downstream users build on it | RPT-EXPORT-001 |
| No merged cells in data sheets; one header row | Merged cells break sorting and import | RPT-EXPORT-001 |
| Dates in an explicit format with the timezone named in the header | Locale reinterprets ambiguous dates | RPT-EXPORT-001 |
| Metadata sheet (XLSX) or header block (CSV where the consumer allows): period, filters, definitions with metric versions, generation time, report ID | The file must stand alone | RPT-EXPORT-001 |
| Text beginning with `=`, `+`, `-`, `@`, tab, carriage return or line feed (or a full-width form) never becomes a formula: CSV prefixes a single quote; XLSX writes a string-typed cell; numbers stay numbers | Spreadsheet formula injection | RPT-EXPORT-002 |
| Identifiers (phone numbers, codes, account numbers) written as text so leading zeros and precision survive | Spreadsheets drop leading zeros and round long numbers | RPT-EXPORT-003 |
| Amounts as numbers with the currency in the header; decimals per ISO 4217 minor unit | Users re-total the column | RPT-EXPORT-003 |
| Formulas only when the export deliberately offers them | Hidden logic and injection risk | RPT-EXPORT-001 |
| Export totals equal screen totals for the same scope | One canonical dataset | RPT-EXPORT-006 |

Guidance differs on the neutralising character for CSV (a single quote or a leading tab); the
Chwezi rule is the single quote. In XLSX the cell type does the work, so no apostrophe is written
into the value. See the currentness register (RP3).

## Task 5: run exports as jobs and keep a record

- Large reports are queued with progress, retry on transient failure, expiry, and de-duplication
  of identical requests; the screen stays usable while the job runs (RPT-EXPORT-004).
- File names are deterministic and free of personal data: `sales-register_kampala_2026-11-03_r42.pdf`
  rather than `John_Okello_payslip.pdf` (the ISO date in a file name is a machine string and is
  allowed; on screen the same date reads `3 Nov 2026`).
- Every generation writes an immutable record: parameter snapshot, metric versions, source
  watermark, generation time, user or service identity, status, checksum and expiry. A scheduled
  report is recorded separately from a copy someone downloaded (RPT-EXPORT-005).
- A report definition registry holds ID, title, description, owner, domain, privacy class,
  parameter schema, export formats, default sort, allowed roles, metric versions and retention
  (RPT-EXPORT-007). Report, configuration, generation, distribution, retention and access are
  separate objects.

## Task 6: secure every exit

- Row- and field-level authorisation runs in the query and in the export service, before data
  leaves the server. Hiding a column in the interface is not a control (RPT-SEC-001, RPT-GATE-04).
- Export, print and schedule may be separate permissions from view; keep them identical to the
  web permission map for the same action (RPT-SEC-002).
- Share links expire; downloads, scheduled recipients and external shares are logged; patient,
  payroll and personal fields stay masked in previews, emails, file names and logs (RPT-SEC-003).

## Task 7: govern written and AI-generated narrative

| Rule | Example | ID |
|---|---|---|
| Each claim cites measure, filter and period | "Net sales rose 12.5% (sales.net_sales v1.2, all branches, 1-8 Nov vs 1-8 Oct 2026)" | RPT-NARR-001 |
| Observation separate from inference | "Observed: Kireka sales fell 30% on Sunday. Possible reason (not verified): the branch opened at 14:00." | RPT-NARR-002 |
| No cause from correlation alone | Not "Rain caused the fall" without evidence | RPT-NARR-002 |
| Uncertainty disclosed | "Two outlets have not synced; the total may rise." | RPT-NARR-002 |
| Status shown; human approval for consequential content | Draft, verified or disputed; finance, clinical or regulatory narrative signed off by a named person | RPT-NARR-003 |
| Versions logged where policy allows | Prompt template v3, model name, generation time | RPT-NARR-004 |

## Evidence/currentness

PDF/UA-2, PDF/A-4 and the formula-injection characters cite RP1-RP3 in the currentness register.
Margins, the type floor and the job behaviours are Chwezi values.
