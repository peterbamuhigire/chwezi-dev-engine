Parent skill: [reporting-and-export-engineering](../SKILL.md)

> Local copy of the Chwezi Reporting and Dashboards Standard 1.0.0, kept identical to the version
> in chwezi-design-engine; this engine works without that repository.

# Currentness register (reporting)

Use this register when citing a standards fact in reporting work. WCAG, platform and width-class
facts are not repeated here: they are in the Product Excellence
currentness register of the Chwezi Product Excellence Standard
(A1-A12, W5, M3). A fact not listed, or marked NOT_ASSESSED, is not stated as fact.

| ID | Fact | Source | Accessed | Status | Review by |
|---|---|---|---|---|---|
| RP1 | PDF/UA-2 is ISO 14289-2:2024, published March 2024 (edition 1), defining tagged PDF for PDF 2.0 (ISO 32000-2); it grew from the PDF Association's WTPDF specification. PDF/UA-1 (ISO 14289-1) remains a separate profile for earlier PDF versions | https://www.iso.org/standard/82278.html ; https://pdfa.org/iso-14289-2-pdf-ua-2-the-gold-standard-for-accessibility-in-pdf-2-0-has-arrived/ | 2026-11-08 (search summary of the primary pages) | VERIFIED (UA-2 date and scope); NOT_ASSESSED (current edition date of ISO 14289-1) | 2027-05-08 |
| RP2 | PDF/A-4 is ISO 19005-4:2020, built on PDF 2.0, with PDF/A-4f and PDF/A-4e variants; ISO lists a revision (ISO/DIS 19005-4.2) in development | https://www.iso.org/standard/71832.html ; https://www.loc.gov/preservation/digital/formats/fdd/fdd000532.shtml | 2026-11-08 (search summary) | VERIFIED (edition); NOT_ASSESSED (revision status) | 2027-05-08 |
| RP3 | Spreadsheet programs treat cells beginning with `=`, `+`, `-` or `@` as formulas; tab, carriage return and line feed, and full-width variants of the trigger characters, are also listed; published mitigations differ (single-quote prefix or leading tab) | https://owasp.org/www-community/attacks/CSV_Injection ; https://symfony.com/cve-2021-41270 | 2026-11-08 (search snippets, not full pages) | VERIFIED (trigger characters); NOT_ASSESSED (current OWASP preferred mitigation) | 2027-02-08 |

Method: claim-level support from search results that quoted the primary pages on 2026-11-08; the
full ISO and OWASP pages were not read in full. Re-read the primary pages at the review date and
change the status if they cannot be read.
