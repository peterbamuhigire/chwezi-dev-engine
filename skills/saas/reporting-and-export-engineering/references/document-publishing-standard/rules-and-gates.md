Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Document Reporting and Publishing Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Rules and gates

Every normative rule of the Chwezi Document Reporting and Publishing Standard, version 1.0.0,
adopted 8 November 2026. Binding text: `doctrine/document-publishing-standard.md`.

## How to read this catalogue

- **ID** `PUB-<AREA>-NNN` is stable and never reused. **Lvl**: MUST, SHOULD (departure needs a design
  decision record), MAY. **Gate**: the PUB hard gate a failure trips (blank = scored finding with an
  owner and a date).
- **Ev**: SHOT (browser screenshots at the acceptance viewports), PAGE (every page of the rendered PDF
  or DOCX inspected at 100% and in greyscale, reviewer named), RECON (reconciliation record across
  outputs and to the ledger), UIT (automated test), REVIEW (named review), RECORD (release or
  generation record), AT (assistive-technology or keyboard run).
- Values marked "Chwezi value" are internal defaults taken from the handbook, not external facts.

## Hard gates

| Gate | Short name | Main rules |
|---|---|---|
| PUB-GATE-01 | Output parity | PUB-RENDER-001/002, PUB-RENDER-008, PUB-FIN-005, PUB-MATH-007, PUB-QA-002 |
| PUB-GATE-02 | Fabricated content | PUB-CONTENT-001/002/003/006, PUB-FIN-003 |
| PUB-GATE-03 | Missing identity or data | PUB-IDENT-001/002, PUB-AGENT-003 |
| PUB-GATE-04 | Unreadable layout | PUB-PAGE-003/004/005, PUB-READER-004 |
| PUB-GATE-05 | Screenshot output | PUB-RENDER-002/003, PUB-DOCX-001 |
| PUB-GATE-06 | Uninspected output | PUB-QA-001, PUB-DOCX-004 |
| PUB-GATE-07 | Data leaked | PUB-SEC-001/002/003, PUB-CONTENT-004 |
| PUB-GATE-08 | Unrecorded or overwritten release | PUB-AUDIT-001/002, PUB-MATH-011 |

## Identity and metadata (IDENT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-IDENT-001 | MUST | 03 | Every output names its title, entity, period, applied filters, generation time with timezone, currency, owner and status; status is one of draft, provisional, final, revised or superseded and is unmistakable. | Identity block present | PAGE, SHOT |
| PUB-IDENT-002 | MUST | 03 | Every output names its source systems and as-of cutoff, and says whether dates are transaction dates or posting dates. | Present | PAGE |
| PUB-IDENT-003 | SHOULD | | Report ID, revision, prepared by, approved by and confidentiality classification are shown where the document is controlled. | Present | PAGE |
| PUB-IDENT-004 | MUST | | Multipage formal reports carry page numbers and the report identifier on every page; policies, manuals and handbooks carry document control (owner, approval, effective date, version, revision history). | Every page | PAGE |

## Archetypes and structure (ARCH)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-ARCH-001 | MUST | | Each output belongs to one archetype (transactional and operational; analytical and executive; editorial and institutional) and one family blueprint; no generic template is forced on every class. | Archetype and blueprint named | REVIEW |
| PUB-ARCH-002 | MUST | | Information follows the decision journey (orientation, summary, evidence, interpretation, action, provenance) and the narrative ladder: level 1 answer and most consequential numbers, level 2 explanation and exceptions, level 3 detail, method, reconciliation and appendices. | Review | REVIEW |
| PUB-ARCH-003 | MUST | | Transactional outputs put accurate amounts and printer reliability before artwork: compact header, identifiers, visible status and dates, parties, lines, totals, taxes, terms, authorisation; repeatable batch export with deterministic file names. | Review | PAGE |
| PUB-ARCH-004 | MUST | | Analytical outputs lead with the summary, use a small selected set of measures (3-6 in the handbook; 3-5 on Chwezi reporting surfaces), pair performance with risks, exceptions, owner and next step, and append full tables and definitions after the narrative. | Review | REVIEW |
| PUB-ARCH-005 | SHOULD | | Editorial outputs use a cover, contents, section openers, narrative spreads, captions and back matter (acknowledgements, references, copyright, contact); spreads read well yet every page stands alone in A4 print. | Review | PAGE |
| PUB-ARCH-006 | MUST | | Screen views become publications through the transformation rules: dashboard to report, filtered table to statement, interactive chart to print, multi-panel view to A4, document preview to mobile. | Review | REVIEW |

## Tokens and themes (TOKEN)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-TOKEN-001 | MUST | | Publishing tokens are versioned and mapped to CSS variables, DOCX styles and PDF styles; brand accent, logo, cover imagery and product metadata may vary per product; structural semantics, table rules, accessibility, pagination and document control are locked. | Token map | REVIEW |
| PUB-TOKEN-002 | MUST | | Default neutrals (Chwezi values): ink #17324A, dark #0D2536, muted #526675, rule #D9E2E8, paper #FFFFFF, subtle fill #F3F7F9; accents pass contrast tests; the rule colour is decorative only and any line that carries meaning uses ink. | Contrast record | REVIEW |
| PUB-TOKEN-003 | SHOULD | | Light, greyscale and low-ink themes exist; dark pages are used only for intentional editorial sections. | Themes rendered | PAGE |
| PUB-TOKEN-004 | MUST | | Spacing comes from the scale (4, 8, 12, 16, 24, 32, 48 pt equivalents); no one-off spacing. | Style review | REVIEW |

## Page and typography (PAGE)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-PAGE-001 | SHOULD | | A4 portrait 210 x 297 mm by default, landscape 297 x 210 mm when justified; margins 16-22 mm with 18 mm as the start; header and footer safe zones 8-12 mm, adjusted for the printer's non-printable area (Chwezi values). | Page set-up | PAGE |
| PUB-PAGE-002 | SHOULD | | Type defaults (Chwezi values) above the Reporting floors: cover 26-36 pt, H1 17-22 pt, H2 12-16 pt, body 9.5-11 pt, notes 8-9 pt, leading 1.15-1.4; real paragraph and heading styles, never bold-only formatting. | Style sheet | PAGE, REVIEW |
| PUB-PAGE-003 | MUST | 04 | Figures are tabular and right-aligned; identifiers and dates are never truncated in formal outputs. | Long-value fixture | PAGE |
| PUB-PAGE-004 | MUST | 04 | No orphaned heading or isolated caption; table header rows repeat on continued pages; a KPI card, signature block or short chart caption never breaks across pages; no accidental blank page. | Multi-page fixture | PAGE |
| PUB-PAGE-005 | MUST | 04 | A desktop dashboard is never shrunk onto A4; charts, tables and summaries are recomposed; a table too wide for portrait moves to landscape or an appendix with a note, never silently truncated. | Wide-table fixture | PAGE |
| PUB-PAGE-006 | SHOULD | | Web uses a 12-column grid; print uses a one- or two-column editorial grid; magazine-style multi-column pages are not used for legal, invoice or accounting documents. | Review | PAGE |

## Charts and figures (CHART)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-CHART-001 | MUST | | Each chart has a specific question, labels, units, baseline, source, period, sample size where needed, and a one- or two-sentence interpretation; narrative figures carry number, caption, accessible description and method note. | Review | REVIEW |
| PUB-CHART-002 | MUST | | The simplest form that answers the question: line for time, bar for ranking, stacked bar for composition, scatter for relationships, tables for exact values, small multiples for comparisons; donuts sparingly; no 3D, misleading truncated axes or unexplained dual axes. | Review | REVIEW |
| PUB-CHART-003 | MUST | | Print resilience: direct labels or compact legends, series told apart by line pattern and marker, vector where possible, adequate resolution otherwise, legible in greyscale. | Greyscale print | PAGE |
| PUB-CHART-004 | MUST | | Interactive charts printed freeze their selection and annotation and replace hover-only values with labels or an appendix. | Print test | PAGE |
| PUB-CHART-005 | MUST | | Maps only where geography informs the decision, with scale or scope, labels, legend and a text alternative; never invented geography. | Review | REVIEW |

## Financial and regulated outputs (FIN)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-FIN-001 | MUST | | Every statement shows entity, statement name, period, currency and unit scaling; comparative columns; indentation; subtotal rules; one negative-value convention; note references; current and comparative periods separated; restatements disclosed. | Review | PAGE |
| PUB-FIN-002 | MUST | | Statutory tax invoices, payroll and regulatory returns use configurable templates; source data, generation history and approver identity are preserved. | Template record | RECORD |
| PUB-FIN-003 | MUST | 02 | No IFRS, tax or statutory compliance claim without legal or accounting review. | Review record | REVIEW |
| PUB-FIN-004 | MUST | | Negative amounts use one consistent minus or parenthesis style; a negative zero is never shown. | Fixture | UIT |
| PUB-FIN-005 | MUST | 01 | Figures are computed from full-precision values and rounded only for display; an unavoidable rounding difference is disclosed; line sums, subtotals, grand totals, comparatives and ledger balances are verified. | Reconciliation | RECON, UIT |
| PUB-FIN-006 | MUST | | Missing values are never treated as zero; they read "Not available" with a reason (Chwezi policy). | Fixture | UIT |
| PUB-FIN-007 | MUST | | Currency and scaling are displayed; currencies are never mixed without an explicit conversion basis. | Fixture | UIT |

## Browser reading (READER)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-READER-001 | MUST | | A purpose-built reading workspace: centred paper-like pages on a neutral surface with responsive fit; toolbar for page navigation, zoom, search, print, download, share and view options; outline or bookmarks for long reports and a thumbnail rail for visual publications. | Screenshots | SHOT |
| PUB-READER-002 | MUST | | Interactive filters stay outside the immutable print composition, and applied filters are shown clearly. | Review | SHOT |
| PUB-READER-003 | MUST | | Desktop shows the page with outline and optional panel; laptop collapses side panels; tablet fits the width with large touch targets and persistent page navigation; mobile offers an accessible reflow reading mode, never pinch-zooming an A4 page for prose; long documents render progressively. | Screenshots at each width | SHOT |
| PUB-READER-004 | MUST | 04 | Print and export controls: preview, orientation, paper size, margins, optional low-ink output, active filters, entity, date range, cutoff and status, selected pages or the full report; a warning before a wide table is split; navigation bars, floating controls, tooltips and modal backdrops never reach the printed document. | Preview test | UIT, PAGE |
| PUB-READER-005 | MUST | | Offline, the reader shows the last verified snapshot with a clear as-of indicator where permitted and never implies live data. | Offline test | UIT |

## Rendering (RENDER)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-RENDER-001 | MUST | 01 | One pipeline: query, authorise, validate, normalise, calculate, narrative, layout, render, check, publish; a schema with metadata, sections, blocks, tables, charts, notes and provenance; one semantic model mapped to HTML, print CSS, PDF and DOCX. | Architecture record | REVIEW |
| PUB-RENDER-002 | MUST | 01, 05 | Every figure in every output comes from the validated dataset, never from displayed strings. | Code review and test | UIT |
| PUB-RENDER-003 | MUST | 05 | PDF pages are true A4 pages with selectable, searchable text, embedded or safe fonts, consistent Unicode, metadata, bookmarks and working links; charts and diagrams are vectors where possible; no page is a screenshot. | Inspect PDF | PAGE |
| PUB-RENDER-004 | MUST | | HTML uses semantic structure (main, article, section, headings, figure and figcaption, table with thead and tbody, accessible navigation); print styles set A4 size and margins, hide chrome, avoid breaks inside short blocks and repeat table headers; pagination is tested with long names, empty data, huge tables and unexpected notes, never on viewport height. | Engine test | PAGE |
| PUB-RENDER-005 | MUST | | Rendering is deterministic: the same approved snapshot and template version give the same numbers, content and order. | Repeat render | UIT |
| PUB-RENDER-006 | SHOULD | | Transparent backgrounds and colour management are tested; a low-ink profile and a branded premium profile exist. | Both rendered | PAGE |
| PUB-RENDER-007 | MUST | | Tagged structure, heading order, table headers, alt text and reading order are evaluated against PDF/UA expectations; conformance is stated only after validation. | Validator record | PAGE, AT |
| PUB-RENDER-008 | MUST | 01 | Browser, PDF, print and DOCX are visually coherent and preserve the same facts. | Compare | RECON, PAGE |

## DOCX (DOCX)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-DOCX-001 | MUST | 05 | Native Word elements, never page screenshots: named Title, Subtitle, Heading 1-3, Body, Caption, Table Header, Note, Quote and Footer styles; editable text and native tables; images only for true visual assets. | Open in Word | PAGE |
| PUB-DOCX-002 | MUST | | Fields for page numbers, optional contents and document metadata update on open; document properties, language and alt descriptions are set; headings give navigation and logical reading order. | Open and update | PAGE |
| PUB-DOCX-003 | MUST | | Tables are native and editable with header repeat, row integrity, totals and stable widths; figures are inline and anchored with captions; no full-page raster. | Inspect | PAGE |
| PUB-DOCX-004 | MUST | 06 | Round trip: reopen in Microsoft Word and LibreOffice where available, check page count and line wraps, render every page, test navigation, edit text, inspect tables, re-render to PDF and compare with the design. | Round-trip record | PAGE |
| PUB-DOCX-005 | SHOULD | | Tracked revisions and template versioning are supported where the workflow needs them. | Review | REVIEW |

## Accessibility and localisation (A11Y)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-A11Y-001 | MUST | | WCAG 2.2 AA in the browser: meaningful headings, keyboard operation, visible focus, screen-reader labels, contrast, semantic tables, alt text for informative images; status never by red and green alone. | AT run | AT |
| PUB-A11Y-002 | MUST | | PDF checks: reading order, document title, language and selectable text. | PDF check | AT, PAGE |
| PUB-A11Y-003 | MUST | | Localisation: UGX and other currencies with consistent rounding and grouping; locale date and time formats; timezone shown when material; long names and translations never clip headers; right-to-left mirroring and numeral direction planned for Arabic. | Locale fixtures | PAGE, SHOT |

## Performance (PERF)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-PERF-001 | MUST | | Long PDFs are never rendered client-side as images; large exports use server pagination or streaming with capped synchronous work; long exports run as background jobs with progress and retry. | Large-report test | UIT |
| PUB-PERF-002 | SHOULD | | Fonts and safe assets are cached; photographs are optimised; repeated illustrations reused; budgets are acceptance targets measured on ordinary devices, not promises. | Measurement | UIT |

## Security (SEC)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-SEC-001 | MUST | 07 | Tenant isolation and record-level authorisation are enforced at export time. | Lower-role export test | UIT |
| PUB-SEC-002 | MUST | 07 | Download links expire and are permission-scoped; temporary files are stored securely; redaction applied by policy; access logged. | Link and log test | UIT |
| PUB-SEC-003 | MUST | 07 | No raw SQL, internal path, secret or hidden field reaches PDF or DOCX metadata or content. | Metadata scan | UIT |
| PUB-SEC-004 | SHOULD | | Audit logs, watermarking and retention follow the document's classification. | Review | RECORD |

## Content (CONTENT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-CONTENT-001 | MUST | 02 | No invented facts, sources, statistics, totals or compliance claims. | Claim-to-source table | REVIEW |
| PUB-CONTENT-002 | MUST | 02 | Imagery is authentic, licensed and in context; client marks, testimonials and case studies need recorded permission and evidence; case studies state context, challenge, intervention, measured outcome, lessons and evidence limits. | Permission record | REVIEW |
| PUB-CONTENT-003 | MUST | 02 | No signature, seal or approval is rendered unless the approval exists in the record. | Approval record | RECORD |
| PUB-CONTENT-004 | MUST | 07 | Health outputs carry audience-specific de-identified aggregates with scope, method, denominator and privacy restrictions; payroll and personal data are limited to the purpose and role. | Role fixture | UIT, REVIEW |
| PUB-CONTENT-006 | MUST | 02 | Insight text is computed deterministically or labelled AI-assisted, and states its figures and comparison scope; AI text is never presented as a clinician-approved diagnosis or an approved opinion. | Review | REVIEW |
| PUB-CONTENT-005 | SHOULD | | Generic section labels are rewritten as specific headings; duplicate metrics, repeated prose, empty blocks, low-information charts and decorative imagery are removed (Kaizen waves 1 and 2). | Review | REVIEW |

## Audit (AUDIT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-AUDIT-001 | MUST | 08 | Each release records report ID, version, generation ID, renderer version, template version, source snapshot, actor, parameter hash, prepared date, approver, correction history and retention. | Release record | RECORD |
| PUB-AUDIT-002 | MUST | 08 | Revisions, cancellations and corrected versions are issued as new versions with history; a published document is never silently overwritten. | Lifecycle test | UIT, RECORD |

## Agent contract (AGENT)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-AGENT-001 | MUST | | Inputs named before work starts: family, audience, purpose, entity, data source, period, currency, classification, output formats and brand. | Input object | REVIEW |
| PUB-AGENT-002 | MUST | | Planning maps each visual to a reader question and defines data lineage and validation; the build creates the semantic model and the HTML, PDF and DOCX mappings; the agent runs four Kaizen passes (simplify, improve hierarchy, verify truth, improve consistency and performance). | Plan and log | RECORD |
| PUB-AGENT-003 | MUST | 03 | Stop conditions: do not publish when totals mismatch, required data is missing, sensitive data leaks or the layout is unreadable. | Stop record | RECORD |
| PUB-AGENT-004 | MUST | | Deliverables: template source, schema mapping, populated example, PDF render, DOCX render, visual snapshots, numerical validation log, accessibility findings, known limitations and unresolved issues. | Deliverable set | RECORD |

## Mathematics and algorithms (MATH)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-MATH-001 | SHOULD | | Type sizes come from a modular scale (size = body x ratio^n, rounded to 0.5 pt) recorded as tokens; body 10.5 pt with ratio 1.25 lands every role inside the handbook ranges. | Token record | REVIEW |
| PUB-MATH-002 | MUST | | Running prose keeps a measure of 45-75 characters per line, computed from the chosen font's average character width; on A4 portrait this means a text block of about 110-135 mm or two columns, with full width kept for tables and figures. | Measure calculation | REVIEW, PAGE |
| PUB-MATH-003 | SHOULD | | Vertical spacing sits on a baseline grid (multiples of half the leading); page budgets use lines per page = floor(text height / leading). | Style review | PAGE |
| PUB-MATH-004 | SHOULD | | Justified text is set only with a whole-paragraph line-breaking algorithm and hyphenation; otherwise body text is ragged-right. | Render review | PAGE |
| PUB-MATH-005 | SHOULD | | Page breaks are chosen by minimising total break cost over candidate break points, with infinite penalties for the hard pagination rules and recorded weights for the rest. | Renderer record | REVIEW |
| PUB-MATH-006 | MUST | | Displayed parts that must add to a displayed whole (shares of 100%, allocations, split bills) are rounded with the largest-remainder method; single-value rounding mode is a stated policy. | Fixture (three equal shares give 34, 33, 33) | UIT |
| PUB-MATH-007 | MUST | 01 | Money and quantities are computed in exact arithmetic (integer minor units or exact decimals), never binary floating point. | Code review and fixture | UIT |
| PUB-MATH-008 | SHOULD | | Axis ticks use nice numbers (1, 2 or 5 x 10^k); bars start at zero; line charts are banked so the median segment slope is about 45 degrees. | Chart review | REVIEW |
| PUB-MATH-009 | MUST | | Colour contrast is computed with the WCAG relative-luminance formula; sequential palettes are interpolated in a perceptually uniform space with monotonic lightness; categorical colours are checked for difference, colour-vision deficiency and greyscale. | Contrast record | REVIEW |
| PUB-MATH-010 | SHOULD | | Photographs reach 300 ppi at printed size and never fall below 150 ppi (Chwezi values); charts, diagrams and logos are vectors; oversized images are downsampled. | Image check | UIT |
| PUB-MATH-011 | MUST | 08 | Each output carries a content identity: a SHA-256 hash of the canonically serialised model with the template and renderer versions; numeric parity compares exact decimal strings from the text layers; visual regression compares pages with a perceptual similarity index against golden pages. | Release record | RECORD, UIT |

## Quality assurance (QA)

| ID | Lvl | Gate | Rule | Check | Ev |
|---|---|---|---|---|---|
| PUB-QA-001 | MUST | 06 | Browser reports are inspected at desktop 1440, laptop 1024 and tablet 820 CSS px and at the Product Excellence compact width; every A4 page at 100% zoom, in A4 print preview, in greyscale and with a long-data fixture. | Screenshots and page record | SHOT, PAGE |
| PUB-QA-002 | MUST | 01 | The acceptance matrix passes for content, numbers, layout, navigation, accessibility, export, performance, security and human approval, with each exception recorded and approved. | QA manifest | RECORD |
| PUB-QA-003 | MUST | | The edge-case library is run: volume, long and right-to-left text, date boundaries, financial extremes, graphics and lifecycle states. | Test log | UIT |
| PUB-QA-004 | MUST | | Financial, legal, medical and externally issued controlled documents have documented human review and sign-off. | Sign-off | REVIEW |
| PUB-QA-005 | SHOULD | | Golden-page visual regression, accessibility checks and arithmetic checks run on every renderer or template change. | CI record | UIT |

## Evidence/currentness

External facts behind PUB-RENDER-004, PUB-RENDER-007 and PUB-A11Y-001 are recorded in
[currentness-register.md](currentness-register.md); the methods behind the MATH rules are in
[mathematics-and-algorithms.md](mathematics-and-algorithms.md). All numeric defaults are Chwezi values.
