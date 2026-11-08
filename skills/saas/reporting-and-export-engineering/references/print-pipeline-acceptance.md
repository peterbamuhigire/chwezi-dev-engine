Parent skill: [reporting-and-export-engineering](../SKILL.md)

# A4 print and PDF pipeline, and print acceptance

Load this when building or reviewing a PDF or print output for a report, statement, register,
closeout or board pack. It implements RPT-PURPOSE-004, RPT-PRINT-001..008 and RPT-RECON-003, and
closes RPT-GATE-06 (print failure) and the print half of RPT-GATE-03 (ambiguous scope). The
renderer-specific detail (mPDF, browser print, Dompdf, Android or iOS PDF APIs) stays in the
platform skills; this file owns the pipeline and the acceptance test.

## 1. Pipeline shape

```text
canonical dataset (server, same as screen and XLSX; hash recorded)
  -> print view model (formatting only: minor units, readable dates, labels)
  -> dedicated print template per page system (never the interactive screen)
  -> paginating renderer (HTML+CSS paged media, a PDF library, or a layout engine)
  -> post-render checks (page count, overflow, fonts embedded, text selectable)
  -> generation record (checksum, page count, template version) -> storage with expiry
```

| Decision | Do | Failure avoided |
|---|---|---|
| Source of print figures | The canonical dataset the screen uses; template formats only | PDF total differing from the screen (RPT-GATE-01) |
| Template | Dedicated print template; remove filters, buttons, hover content and "tap to" text | A screenshot of the dashboard as the PDF (RPT-PRINT-001) |
| Orientation | Portrait by default; landscape only when content width needs it, or a landscape annex | Shrunk text in a too-wide table |
| Too-wide schedule | Drop nonessential columns or move to a landscape annex | Text below the legibility floor (RPT-PRINT-004) |
| Charts | Vector where the renderer allows; direct labels, patterns, explicit values | Unreadable greyscale prints (RPT-PRINT-005) |
| Fonts | Embedded, licensed for embedding, with the glyphs for every supported language | Missing glyphs, substituted fonts |
| Generation | Server side, as a job for large reports | Browser tab timing out on a 40-page register |

## 2. Page anatomy (RPT-PRINT-002, RPT-GATE-03)

Page one carries: organisation and branch, report title, report ID and version, exact period with
dates, basis of accounting where relevant, generation time with timezone, currency, applied
filters and classification. Later pages repeat a concise identity line (organisation, title,
period). Every page footer shows "Page x of y", the report ID and the generation record ID.
Dates read `4 Nov 2026`; amounts follow the currency's ISO 4217 minor unit; document numbers are
shown as issued.

Page systems (choose one per report; Chwezi starting points):

| Page system | Orientation | Order of content |
|---|---|---|
| Formal financial statement | Portrait | Identity, title and period, comparative columns, subtotal hierarchy, notes, approval, footer |
| Wide financial schedule | Landscape | Metadata, fixed key columns, grouped amount columns, totals, source notes, continuation |
| Executive scorecard | Portrait | One-page summary, 3 to 5 key measures, target comparison, risks, actions, evidence annex |
| Operational register | Portrait or landscape | Date and branch, numbered rows, repeated headers, group subtotals, totals, sign-off |
| Exception and audit report | Landscape | Scope and source watermark, exception summary, register, owner, actions and status |
| Invoice or statement | Portrait | Issuer and recipient, reference and dates, lines, tax and discounts, amount due, terms |
| Board pack | Portrait with landscape annexes | Cover, contents, summary, sections, decisions, annexes, glossary |

## 3. Pagination rules (RPT-PRINT-003, RPT-GATE-06)

- Table headings repeat on every page (`thead { display: table-header-group; }` in HTML paged
  media; the library's repeat-header option otherwise).
- No heading is left alone at the foot of a page (`break-after: avoid` on headings).
- A subtotal stays with its last lines; a total stays with its label (`break-inside: avoid` on
  the total block; keep-with-previous where the library supports it).
- Short records do not split across pages (`break-inside: avoid` on rows below a height
  threshold).
- Carried-forward and brought-forward lines appear only where the document type needs them
  (ledgers, registers), never as decoration.
- Footnotes stay on the page of the figure they explain or are numbered into a notes section.
- "Page x of y" needs a two-pass render or the library's total-pages token; test it on a report
  long enough to paginate.

## 4. Legibility, colour and margins (RPT-PRINT-004/005/006)

Chwezi values at 100% print scale: body 9 pt, table text 8.5 pt, footnotes 8 pt minimum; margins
start at 15-20 mm, adjusted for binding, printer limits and letterhead. Print reads in black and
white: status words and patterns, not colour alone; no large tinted blocks without meaning.
Fit-to-page scaling is disabled; the template fits by design.

## 5. Tagged PDF and conformance profiles (RPT-PRINT-007)

Target a tagged PDF: logical reading order, document language, real headings, table structure
with header cells, alternate text for charts, bookmarks for multi-section reports, selectable
text. Conformance profiles are separate claims, each made only after a validator run and a manual
review:

| Profile | What it is | Status recorded on 8 Nov 2026 |
|---|---|---|
| PDF/UA-1 (ISO 14289-1) | Accessible PDF on PDF 1.7 (ISO 32000-1) | Edition history from a secondary source; primary ISO page not readable (HTTP 403): `NOT_ASSESSED` |
| PDF/UA-2 (ISO 14289-2:2024) | Accessible PDF on PDF 2.0; a separate profile from PDF/UA-1 | Adopting brief states publication in March 2024; the ISO and PDF Association pages refused automated access and the secondary source read was out of date: `NOT_ASSESSED` |
| PDF/A (ISO 19005) | Archival profiles; PDF/A-4 (ISO 19005-4:2020) is the current part, on PDF 2.0 (ISO 32000-2) | Library of Congress format description (read 8 Nov 2026): published November 2020, PDF 2.0 base, a formal dated revision being prepared by ISO TC 171 in 2025: `VERIFIED` (secondary authority; ISO page refused access); revision status `NOT_ASSESSED` |

Rules that do not depend on those dates: PDF/UA and PDF/A are independent; a file may target
both, but each needs its own validation. Never print "PDF/UA compliant" or "PDF/A" in a footer,
proposal or metadata field without a validator report and a named manual reviewer. Which
validators to use is a product decision; record the tool and version with the result.

## 6. Print acceptance cases (RPT-PRINT-008, RPT-QA-001)

Run every case for each print template; record PRINT evidence (every page inspected at 100% and
in greyscale, reviewer named) and keep the PDFs in the evidence folder.

| Case | Fixture | Pass when |
|---|---|---|
| Long table | Enough rows for 3+ pages | Headers repeat; page x of y correct; no orphaned heading or total |
| Zero | A day with no sales | Shows "No sales on 4 Nov 2026" or zero rows with the reason, not a blank page |
| Negative | Refunds exceed sales | Negative amounts clearly signed; variance status by direction rule |
| Very large | Totals of 12+ digits in UGX | No overflow, no truncation, no compact K/M/B on a total |
| Long names | 80-character product and branch names | Wrap without breaking the grid |
| Missing values | Unsynced branch, null cost | Reads "Not available" with the reason; never 0 |
| Restricted | Lower-role generation | Only permitted rows and fields; masked fields read "Restricted" |
| Multi-currency (where supported) | UGX and USD lines | Separate totals per currency; no mixed sum |
| Right-to-left (where supported) | Arabic labels | Mirrored layout; numbers and document numbers keep left-to-right order |
| Blank or error data | Source down at generation | Job fails visibly or the PDF carries an integrity warning; never a silent partial report |
| Greyscale | Any report with status colour | Every status still readable |
| Physical print | Representative office printer | Margins and legibility hold at 100%; record printer model (or `NOT_ASSESSED`) |

Compare the PDF text layer totals with the screen API and XLSX totals for the same scope
(RPT-RECON-003); record the comparison as RECON evidence.
