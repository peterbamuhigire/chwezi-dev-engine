Parent skill: [reporting-and-export-engineering](../../SKILL.md)

> Local copy of the Chwezi Document Reporting and Publishing Standard 1.0.0, kept identical to the
> version in chwezi-design-engine; this engine works without that repository.

# Worked review: monthly finance pack (fictional)

All names and figures are fictional. A Chwezi POS product exports an October 2026 monthly finance
pack for "Example Traders Ltd" as a browser report, an A4 PDF and a DOCX (family: financial
statement; blueprint: monthly finance pack).

## Findings

| # | Finding | Rule | Gate | Evidence | Fix |
|---|---|---|---|---|---|
| 1 | The PDF profit-or-loss total was parsed from the formatted browser string "4.82M", so it read 4,820,000 against a ledger figure of 4,823,500 | PUB-RENDER-002, PUB-FIN-005 | PUB-GATE-01, 05 | RECON | All renderers read the validated snapshot; totals recomputed |
| 2 | The DOCX had no status, owner or as-of cutoff; page 3 onwards had no page number or report ID | PUB-IDENT-001/002/004 | PUB-GATE-03 | PAGE | Identity block and running header and footer from the specification |
| 3 | The receivables ageing table cut its last two columns on A4 portrait without warning | PUB-PAGE-005 | PUB-GATE-04 | PAGE | Ageing schedule moved to a landscape annex with a note in the body |
| 4 | A heading "Notes" sat alone at the foot of page 6, and the approval block split across pages 8 and 9 | PUB-PAGE-004 | PUB-GATE-04 | PAGE | Keep-with-next on headings; approval block kept whole |
| 5 | The cover showed a director's scanned signature before approval | PUB-CONTENT-003 | PUB-GATE-02 | RECORD | Signature block rendered only from the approval record |
| 6 | Payroll totals listed each employee's name and net pay in a pack shared with all managers | PUB-CONTENT-004 | PUB-GATE-07 | UIT | Payroll summarised by department; detail restricted by role |
| 7 | Pages 8-9 of the PDF were never opened before the pack was emailed, and the DOCX was never reopened | PUB-QA-001, PUB-DOCX-004 | PUB-GATE-06 | PAGE | Every page inspected; DOCX round trip in Word and LibreOffice; record in the QA manifest |
| 8 | No release record: no generation ID, template version, parameter hash or approval state; the September pack had been overwritten in place | PUB-AUDIT-001/002 | PUB-GATE-08 | RECORD | QA manifest on each release; corrections issued as a revised version |
| 9 | Insight "Sales grew because of the new menu" was AI text without a label or comparison scope | PUB-CONTENT-006 | PUB-GATE-02 | REVIEW | "Observed: net sales up 8.2% on September (1-31 Oct vs 1-30 Sep). Cause not verified. AI-assisted." |
| 10 | Zero, null and not applicable all printed as "-" in the cash flow notes | PUB-FIN-006 | | UIT | `0`, "Not available (reason)" and "Not applicable" shown distinctly |

## Verdict

Before fixes: BLOCKED (PUB-GATE-01 to 08 all open). After fixes and a re-run with every gate on
`MEASURED` evidence, a reconciliation of the 14 critical totals and the finance lead's sign-off:
ready for release.
