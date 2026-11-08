# 2026-11-08 - Chwezi Reporting and Dashboards Standard (engineering side)

## What changed

The Chwezi Reporting and Dashboards Standard 1.0.0 was adopted on 8 November 2026 on the
instruction of Lead Developer Peter Bamuhigire (Chwezi Core Systems), as the reporting companion
to the Chwezi Product Excellence Standard. Owner decision of the same day: every Chwezi engine
carries the full capability itself. This engine therefore holds a complete local copy of the
standard and does not depend on any other repository at run time. The visual layer (type,
colour, chart styling) is maintained in `chwezi-design-engine`.

New skill `skills/saas/reporting-and-export-engineering` (active catalogue 168 -> 169; plugin
manifest 166 -> 167; routing fixtures 242 -> 245):

| File | Purpose |
|---|---|
| `SKILL.md` | Engineering procedure, gate map (RPT-GATE-01..08 with the PX gates each also trips, explained in this engine's own words), owner rules, decision rules, evidence contract |
| `references/reporting-standard-doctrine.md` | Local copy of the doctrine: output contracts, five questions, precedence, eight gates, owner rules, change control |
| `references/rules-and-gates.md` | Local copy of the full rule catalogue; every RPT ID, level, gate, check and evidence code identical to the design-engine copy; local glossary of MUST/SHOULD/MAY and evidence codes |
| `references/metric-contract-and-semantic-layer.md` | Metric contract template, one measure layer, grain and fan-out tests, unit and currency rules, reconciliation harness, periods and variance, fictional Kampala daily-close example |
| `references/export-safety-checklist.md` | Formula-injection neutralisation, typed cells, identifiers, schema, metadata sheet, export authorisation |
| `references/print-pipeline-acceptance.md` | A4 pipeline, page anatomy and page systems, pagination, legibility floor, PDF/UA and PDF/A profiles, print acceptance cases |
| `references/generation-records-and-export-jobs.md` | Report definition registry, immutable generation record schema, export jobs, privacy-safe file names, delivery, share links and audit |
| `references/verification-performance-and-observability.md` | Component fixtures, reporting state type, verification matrix, budgets and caching, telemetry, tenant isolation |

Neighbour updates (short cross-references and corrections):

- `frontend-architecture/references/product-excellence-engineering-gates.md`: new section
  "Reporting surfaces: RPT gates" with when each gate applies and its engineering check.
- `excel-spreadsheets`: description exclusion; programmatic rule 7 (export safety); number-format
  table corrected to ISO 4217 minor units (KES and TZS have 2, not 0), display date `D MMM YYYY`
  (`5 Apr 2026`), compact `M` format limited to charts and tiles.
- `saas-business-metrics`: description pointer; metric-contract requirement (RPT-METRIC-001/002/006,
  RPT-RECON-001).
- `ai-analytics`: description exclusion; RPT-NARR-001..004 and RPT-GATE-07 in Quality Standards.
- `python-data-analytics`: a zero denominator returns "not comparable", not 0 (RPT-STATE-002,
  RPT-PERIOD-004); no cross-unit or cross-currency sums; output handoff pointer.
- `professional-word-output/references/report-print-pdf/entrypoint.md`: dates `j M Y` without a
  leading zero; print sizes raised to the legibility floor (9 pt body, 8.5 pt table, 8 pt
  footnotes; the previous 7-11 px values were below it); money decimals follow ISO 4217 instead of
  "2 decimals for non-whole numbers"; pointer to the print pipeline.
- Registration: root `SKILL.md`, `docs/skill-catalogue.md`, `docs/skill-routing-index.md`,
  `docs/skill-aliases.yml`, `.claude-plugin/plugin.json` (regenerated), `.skills-engine/engine-manifest.yaml`,
  `AGENTS.md`, `README.md`, `docs/overview/{README,PROJECT_BRIEF,TECH_STACK}.md`,
  `docs/plans/NEXT_FEATURES.md`, three count tests, three routing fixtures with three owned
  negatives.

## Sources and currentness (accessed 8 Nov 2026)

| Claim | Source | Status |
|---|---|---|
| Spreadsheet trigger characters and the two published mitigations (single-quote prefix with quoting; tab inside the quoted field for Excel); quote methods unreliable in Excel after save and reopen; line feed and full-width variants also listed | OWASP Community, CSV Injection, https://community.owasp.org/attacks/CSV_Injection (the owasp.org URL redirects there with HTTP 308; no page date) | `VERIFIED` at access; register id `owasp-csv-injection-2026-11-08`; review by 2027-02-08 |
| PDF/A-4 is ISO 19005-4:2020, published November 2020, on PDF 2.0; a dated revision in preparation in 2025 | Library of Congress format description fdd000532 | `VERIFIED` (secondary authority; ISO page HTTP 403); register id `loc-pdfa4-fdd-2026-11-08` |
| PDF/UA-2 is ISO 14289-2:2024, published March 2024, separate from PDF/UA-1 | ISO 82278 and PDF Association pages | `NOT_ASSESSED`: HTTP 403 to automated fetch; quarantined as `iso-14289-2-2024-2026-11-08`, re-verify by 2027-02-08 |
| Library behaviour (openpyxl, PhpSpreadsheet, XlsxWriter, exceljs formula inference) and Excel's significant-digit limit | Not read | `NOT_ASSESSED`; skill text says so |

All thresholds in the skill (legibility floor, margins, freshness target, retention) are Chwezi
values, not external facts. The source book (design bible Edition 1.0, November 2026) is Chwezi's
own standard; its content enters only as task-oriented paraphrase; no extraction is stored.

## Issues found in the canonical design-engine text (reported, not worked around)

1. RPT-EXPORT-002 names `=`, `+`, `-`, `@`, tab and carriage return. The OWASP page read on
   8 Nov 2026 also lists line feed and full-width variants. The skill recommends neutralising them
   as engineering hardening, labelled as beyond the rule; the rule text is unchanged.
2. RPT-EXPORT-002's single-quote prefix: in XLSX a literal `'` written into a string cell is
   visible to the reader, whereas typing `'` in Excel sets a hidden quote-prefix attribute. The
   rule does not say which is intended for XLSX; the skill applies the rule literally and records
   the visible apostrophe as its cost. A wording decision is needed.
3. The rules catalogue cites `currentness-register.md`; it was absent when first read and present
   later the same day (no action needed here; this engine records its own sources).
4. The doctrine's gate table first mapped RPT-GATE-03, 05 and 06 to PX-GATE-02, 04 and 06; the
   design engine corrected these to "None (reporting-specific)" on 8 Nov 2026 and the local copy
   follows the correction.

## Validation

See `CHANGELOG.md` (2026-11-08, Reporting and Dashboards Standard) for the commands and results.
