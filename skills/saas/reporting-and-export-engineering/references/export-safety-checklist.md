Parent skill: [reporting-and-export-engineering](../SKILL.md)

# CSV and XLSX export safety checklist

Load this when building or reviewing any CSV or XLSX export, scheduled spreadsheet or "download
as Excel" action. It implements RPT-EXPORT-001/002/003/006 and closes RPT-GATE-05 (unsafe
spreadsheet) and part of RPT-GATE-01 (export totals equal screen totals). Workbook design and
formatting stay in `excel-spreadsheets`; this file owns the safety and schema rules.

## 1. Formula-injection neutralisation (RPT-EXPORT-002, RPT-GATE-05)

**Chwezi rule (binding):** a text value that begins with `=`, `+`, `-`, `@`, tab (0x09), carriage
return (0x0D) or line feed (0x0A), or a full-width form of these (U+FF1D, U+FF0B, U+FF0D, U+FF20),
never becomes a formula. CSV: prefix a single quote (`'`) to such text fields. XLSX: write the
value as a string-typed cell, never as a formula, and add no apostrophe. Numeric cells are written
as numbers, not text, so a negative amount is never mangled.

**External guidance differs.** The OWASP CSV Injection page (read 8 Nov 2026, no page date shown)
offers two approaches: wrap each field in double quotes, prefix a single quote and double any
embedded double quotes; or, to resist Microsoft Excel specifically, put a tab character inside the
quoted field before a leading `=`, `+`, `-` or `@`. It warns that the quote techniques are not
reliable in Excel after the CSV is saved and reopened, that the tab stays in the data and can
break programmatic import, and that no single method suits every spreadsheet program. The same
page also lists line feed (0x0A) and full-width forms of the trigger characters; the Chwezi rule
names them. For CSV Chwezi follows the single-quote prefix; do not switch to tab prefixing without
a change to the standard. For XLSX the string cell type does the work.

Implementation decision table:

| Cell | Do | Failure avoided |
|---|---|---|
| Text value (name, note, address, reference, phone) starting with a trigger | CSV: prefix `'`, quote the field and double inner `"`. XLSX: string-typed cell, no prefix | Formula execution on open (`=HYPERLINK(...)`, `=cmd|...`) |
| Text value containing a trigger later in the string | Quote the field; no prefix needed for the rule | Field-separator breakout |
| Amount, quantity, count | Write as a number cell (XLSX numeric type; CSV bare digits matching `^-?\d+(\.\d+)?$`) | `'-45000` stored as text, totals broken |
| Value that looks numeric but is an identifier | Treat as text (section 2), then apply the trigger rule for the format | `+256 784 ...` phone evaluated or reformatted |
| XLSX via a library | Write text with the library's explicit string type; no apostrophe | Library auto-detecting a leading `=` as a formula |
| Intended formulas | Only in a separate, documented calculation sheet, never in data sheets fed by user text | Mixing trusted and untrusted formulas |

Library notes (behaviour to verify in the product's pinned version; `NOT_ASSESSED` here):
openpyxl treats a string beginning with `=` as a formula unless the cell type is forced to string;
PhpSpreadsheet `setCellValue` may infer a formula, so use `setCellValueExplicit(..., DataType::TYPE_STRING)`;
in XlsxWriter use `write_string` rather than `write`; in exceljs set the value as a plain string,
never `{ formula: ... }`. Do not write a literal leading `'` into an XLSX string cell: it is visible
to the reader and adds nothing once the cell is string-typed.

Hardening beyond the rule (engineering practice, recommended, not an RPT requirement): also
check the first character after trimming leading whitespace.

Reference sketch (Python, CSV):

```python
TRIGGERS = ("=", "+", "-", "@", "\t", "\r", "\n", "\uff1d", "\uff0b", "\uff0d", "\uff20")
NUMERIC = re.compile(r"-?\d+(\.\d+)?")

def csv_cell(value, column_kind):
    if column_kind in ("amount", "quantity", "count") and NUMERIC.fullmatch(str(value)):
        return str(value)                      # numbers stay numbers
    text = "" if value is None else str(value)
    if text.startswith(TRIGGERS):
        text = "'" + text                      # Chwezi rule for CSV: single-quote prefix
    return text                                # csv.writer(quoting=csv.QUOTE_ALL) quotes and doubles "
```

Fixture (UIT + EXPORT): rows with `=1+1`, `+256784000000`, `-12 (refund note)`, `@SUM(A1)`,
`\tcmd`, `\r=1`, `\n=1`, a full-width `\uff1d1+1`, a real negative amount `-45000`, and a leading-zero code `00125`. Open the file
in the spreadsheet programs the customers use; record that no formula evaluates, the amount is
numeric and the code keeps its zeros.

## 2. Identifiers, amounts and dates (RPT-EXPORT-003, RPT-EXPORT-001)

- Identifiers (document numbers, product codes, phone numbers, account numbers, national IDs)
  are written as text with full precision and leading zeros. Document numbers appear exactly as
  issued (`INV-00012841`), contiguous per tenant and document type, never renumbered.
- Long numeric identifiers are always text. Spreadsheet programs keep a limited number of
  significant digits in a number cell (commonly cited as 15 for Excel; not re-read for this
  change, `NOT_ASSESSED`), so a long code written as a number loses its tail.
- Amounts are numbers, unformatted in the cell value, with the currency in the column header
  (`net_sales_ugx`) and, in XLSX, a number format matching the ISO 4217 minor unit (UGX `#,##0`;
  KES `#,##0.00`). Never write `1.5M` or other compact forms into a data cell.
- Quantities carry their unit in a separate column; a mixed-unit column has no total row.
- Dates: XLSX true date cells with an explicit format; CSV ISO 8601 with offset
  (`2026-11-04T18:30:00+03:00`) because CSV is a machine format. The metadata sheet and any human
  heading use the readable form `4 Nov 2026`.

## 3. Stable schema and metadata (RPT-EXPORT-001)

- Data sheets: one header row of machine-readable column names (`snake_case`, ASCII), no merged
  cells, no blank spacer rows or columns, no subtotal rows mixed into data (put totals on a
  separate summary sheet or a clearly typed total row the schema declares).
- The schema is versioned (`export_schema: sales_register/3`); adding a column is minor,
  renaming or removing one is major and announced to integrators.
- A `metadata` sheet (XLSX) or a header block or sidecar file (CSV) carries: report ID and
  title, tenant and branch, exact period with timezone, filters applied, metric IDs and versions,
  currency, generation time, generated by, source watermark, schema version, classification,
  generation record ID and checksum. CSV for machine import prefers a sidecar
  `*.metadata.json` so the data file stays parseable.
- Encoding: UTF-8; add a byte-order mark only when the product's users open CSV in a program
  that needs it, and record the decision.

## 4. Totals and reconciliation (RPT-EXPORT-006, RPT-RECON-003, RPT-GATE-01)

- The export is generated from the same canonical dataset as the screen and PDF; the dataset
  hash is in the generation record.
- A CI or job-level check compares export totals with the screen API totals for the same scope
  and fails on any difference.
- Totals in XLSX are written as values computed by the server; a convenience formula may sit
  beside them only on a non-data sheet.

## 5. Authorisation and privacy in exports (RPT-SEC-001/002/003, RPT-GATE-04)

- Row and field filtering happen in the export query, with the requester's server-side
  authorisation, before a file is written. Hiding a column in the screen is not a control.
- Export permission is separate from view permission where the domain requires.
- File names are deterministic and contain no personal data: `sales-register_t42_2026-11-04_v3_8f3a1c.xlsx`
  (tenant key, period, schema version, short checksum), never a customer or employee name.
- Masked fields stay masked in the file, previews, emails and logs.

## Review checklist

- [ ] Every text cell passes the neutraliser; numbers are numbers
- [ ] Identifiers and document numbers are text with leading zeros and full precision
- [ ] No merged cells or spacer rows in data sheets; schema version recorded
- [ ] Metadata sheet or sidecar complete; period, timezone and filters exact
- [ ] Export totals equal screen totals (RECON and EXPORT evidence)
- [ ] Lower-role session calling the export API directly gets only permitted rows and fields
- [ ] File name holds no personal data
- [ ] Injection fixture opened in the customers' spreadsheet programs, result recorded
