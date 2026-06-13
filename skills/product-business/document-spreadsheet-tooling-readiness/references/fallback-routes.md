# Fallback Routes

## Preferred Routes

| Output | Preferred route | Fallback |
|---|---|---|
| DOCX | Documents plugin or python-docx/docxtpl | Markdown with clear structure. |
| XLSX | Spreadsheets plugin or openpyxl/XlsxWriter/pandas | CSV files plus Markdown data dictionary. |
| PDF from DOCX | LibreOffice/soffice when available | Pandoc route, reportlab direct PDF, or provide DOCX/Markdown and state PDF not generated. |
| PDF report | Pandoc or reportlab | Markdown plus print instructions if no converter works. |
| OCR/PDF extraction | PyMuPDF, pypdf, pdfplumber, tesseract where needed | Manual extraction note with limitations. |

## File Claim Rule

You may say a file was generated only after:

1. The write command completed.
2. The file exists at the stated path.
3. The file opens or can be parsed by a relevant library.
4. Any required formulas/tables/pages were checked.

## New Machine Note

Every engine should reference this skill before promising rich file outputs. If the skill is unavailable, run the package and binary checks manually and state the result.
