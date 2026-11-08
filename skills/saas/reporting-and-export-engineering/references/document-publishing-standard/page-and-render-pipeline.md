Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Document Reporting and Publishing Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Publishing system and renderer contracts

Use this reference to set tokens and page geometry, build the browser reader, turn screens into
publications and implement the HTML, PDF and DOCX renderers. Rule IDs:
[rules-and-gates.md](rules-and-gates.md); facts: [currentness-register.md](currentness-register.md).

## Task 1: set tokens and themes (PUB-TOKEN-001 to 004)

| Token | Default (Chwezi value) | Rule |
|---|---|---|
| Ink | #17324A | Body text and every line that carries meaning (13.19:1 on paper, measured) |
| Dark | #0D2536 | Headings and covers (15.73:1) |
| Muted | #526675 | Secondary text (5.97:1 on paper, 5.54:1 on subtle fill) |
| Rule | #D9E2E8 | Decorative separators only (1.31:1, below the 3:1 non-text minimum) |
| Paper | #FFFFFF | Page |
| Subtle fill | #F3F7F9 | Panels and banding |
| Accent | Product brand | Passes contrast; never the only carrier of meaning |
| Type | One principal sans with a safe fallback; optional serif for pull quotes | Banned-font doctrine applies; state the typeface and the reason |
| Spacing | 4, 8, 12, 16, 24, 32, 48 pt equivalents | No one-off spacing |

Tokens are versioned and mapped to CSS variables, DOCX styles and PDF styles. Logo, accent, cover
imagery and product metadata vary per product; structural semantics, table rules, accessibility,
pagination and document control do not. Provide light, greyscale and low-ink themes; dark pages
only for intentional editorial sections.

## Task 2: set page geometry and type (PUB-PAGE-001 to 006)

- A4 portrait 210 x 297 mm; landscape 297 x 210 mm when justified.
- Margins 16-22 mm, starting at 18 mm; header and footer safe zones 8-12 mm; adjust for the
  printer's non-printable area.
- Web: 12-column grid. Print: one or two editorial columns; never magazine columns on legal,
  invoice or accounting documents.
- Type: cover 26-36 pt; H1 17-22 pt; H2 12-16 pt; body 9.5-11 pt; notes 8-9 pt; leading
  1.15-1.4. Never below the Reporting floors (body 9 pt, tables 8.5 pt, footnotes 8 pt).
- Real paragraph and heading styles; tabular, right-aligned figures; identifiers and dates never
  truncated.
- Pagination: no orphan headings or isolated captions; header rows repeat; never break a KPI card,
  signature block or short chart caption; page numbers and report identifiers on multipage formal
  reports.
- Never shrink a desktop dashboard onto A4: recompose charts, tables and summaries.

## Task 3: turn a screen into a publication (PUB-ARCH-006)

| From | To | How |
|---|---|---|
| Dashboard | Report | Replace navigation with title and period; lead with conclusions; expand measure context; reflow charts; append supporting tables |
| Filtered table | Statement | Show the filter snapshot; group and subtotal rows; add commentary, exception highlights and data definitions |
| Interactive chart | Print | Freeze selection and annotation; show units and sources; replace hover-only values with labels or an appendix |
| Multi-panel view | A4 | Order panels by narrative importance; stack across pages; repeat title and section context where needed |
| Document preview | Mobile | Reflow reading mode for text; page view optional; keep table zoom or an accessible table view |

## Task 4: build the browser reading workspace (PUB-READER-001 to 005)

- Centred paper-like pages on a neutral surface with responsive fit; toolbar for page navigation,
  zoom, search, print, download, share and view options; outline or bookmarks for long reports; a
  thumbnail rail for visual publications; keyboard operation throughout.
- Interactive filters sit outside the immutable print composition; applied filters are shown.
- Desktop: page with outline and an optional contextual panel. Laptop: collapsible side panels.
  Tablet: fit-width single page, large touch targets, persistent page navigation. Mobile: an
  accessible reflow reading mode; nobody pinches an A4 page to read prose.
- Long documents render progressively and virtualise; high-resolution pages are not all loaded at
  once.
- Print and export controls: preview, orientation, paper size, margins, optional low-ink output, the
  active filters, entity, date range, cutoff and status, selected pages or the full report, and a
  warning before a wide table is split. No navigation bar, floating control, tooltip or modal
  backdrop reaches the printed page.
- Offline: the last verified snapshot with a clear as-of indicator where permitted; never implied to
  be live.

## Task 5: one pipeline, three renderers (PUB-RENDER-001 to 008)

Pipeline: query, authorise, validate, normalise, calculate, narrative, layout, render, check,
publish. The report schema holds metadata, sections, blocks, tables, charts, notes and provenance;
one semantic model maps to HTML, print CSS, PDF and DOCX. Record the renderer version, template
version, source snapshot and generation ID with every output. Never compute a figure from displayed
strings.

### HTML and print CSS

- Semantic structure: main, article, section, headings, figure and figcaption, table with thead and
  tbody, accessible navigation.
- Print styles: A4 page size, controlled margins, hidden chrome, no breaks inside short blocks,
  repeated table headers, page-break rules. Support for paged-media and fragmentation features
  differs by rendering engine: test the chosen engine (currentness PB1-PB3).
- Pagination is tested with long names, empty data, huge tables and unexpected notes, never by
  relying on viewport height.

### PDF

- True A4 pages; embedded or safe fonts; selectable, searchable text; consistent Unicode; correct
  metadata and bookmarks; working links; vector charts and diagrams where possible; transparency and
  colour management tested.
- Accessibility: tagged structure, heading order, table headers, alt text and reading order
  evaluated against PDF/UA expectations; claim conformance only after validation (PB4).
- Security: authorisation, secure temporary files, redaction, expiry, access logging, classification;
  no raw SQL, internal paths, secrets or hidden fields in metadata.
- Print verification: A4 dimensions, page numbers, no clipped columns, low-ink and greyscale proof,
  printer-safe margins.
- Determinism: the same approved snapshot and template version give the same numbers, content and
  order.

### DOCX

- Named styles: Title, Subtitle, Heading 1-3, Body, Caption, Table Header, Note, Quote, Footer.
- Fields: page numbers, optional contents and document metadata, updated on open; document
  properties and language set.
- Native editable tables with header repeat, row integrity, totals and stable widths; inline anchored
  figures with captions and alt descriptions; no full-page raster.
- Round trip: reopen in Microsoft Word and LibreOffice where available; check page count and line
  wraps; render every page; test navigation; edit text; inspect tables; re-render to PDF and compare
  with the design; export again (PUB-DOCX-004).
- Tracked revisions and template versioning where the workflow needs them.

## Task 6: accessibility, localisation, performance and security

- Accessibility: WCAG 2.2 AA in the browser; meaningful headings, keyboard, visible focus,
  screen-reader labels, contrast, semantic tables, alt text; status never by red and green alone; in
  PDF test reading order, title, language and selectable text.
- Localisation for East African operations: UGX and other currencies with consistent rounding and
  grouping; locale date and time formats with the timezone when material; long names and
  translations never clip headers; right-to-left mirroring and numeral direction for Arabic.
- Performance: no client-side rendering of long PDFs as images; server pagination or streaming for
  large exports with capped synchronous work; cached fonts and safe assets; optimised photographs;
  background jobs with progress and retry; budgets measured on ordinary devices.
- Security: tenant isolation and record-level authorisation at export time; expiring,
  permission-scoped links; secure temporary storage; audit logs, watermarking and retention by
  classification.

## Task 7: financial and regulated outputs

- Statements carry entity, statement name, period, currency and unit scaling; comparative columns,
  indentation, subtotal rules in ink, one negative-value convention, note references; current and
  comparative periods separated; restatements disclosed; totals reconcile to the ledger and to the
  rows shown (PUB-FIN-001).
- Statutory tax invoices, payroll and regulatory returns use configurable templates; laws and
  standards vary by entity and jurisdiction, so IFRS, tax or statutory compliance is claimed only
  after legal or accounting review (PUB-FIN-002/003).
- Source data, generation history and approver identity are preserved; corrections are new
  versions, never silent overwrites (PUB-AUDIT-002).

## Evidence/currentness

Paged-media status: PB1-PB3; PDF/UA: PB4; WCAG: PB5; ISO 32000: PB7. Contrast ratios were computed
on 2026-11-08 with the WCAG relative-luminance formula. Type, margin and spacing values are Chwezi
values from the handbook.
