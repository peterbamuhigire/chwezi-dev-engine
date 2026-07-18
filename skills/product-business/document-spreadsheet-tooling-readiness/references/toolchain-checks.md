# Toolchain Checks

## Python Package Check

Use the active Python environment and check versions:

```powershell
python - <<'PY'
import importlib.metadata as m
packages = ['openpyxl','XlsxWriter','pandas','python-docx','docxtpl','docxcompose','pypandoc','Markdown','beautifulsoup4','lxml','pillow','PyMuPDF','pypdf','pdfplumber','reportlab']
for p in packages:
    try:
        print(f'{p}: {m.version(p)}')
    except Exception:
        print(f'{p}: NOT FOUND')
PY
```

## Approved Install/Update Command

Use standard package managers only. Do not run remote install scripts.

```powershell
python -m pip install --user --upgrade openpyxl XlsxWriter pandas python-docx docxtpl docxcompose pypandoc markdown beautifulsoup4 lxml "pillow<11,>=10.2.0" PyMuPDF pypdf pdfplumber reportlab
```

Pillow is held below 11 where `surya-ocr` compatibility matters.

## Binary Check

Run the cross-platform LibreOffice readiness check from the skills repository root. It checks the `PATH` and standard Windows/macOS installation locations without changing the system configuration:

```powershell
python -X utf8 skills/product-business/document-spreadsheet-tooling-readiness/scripts/libreoffice_headless.py --check
```

```bash
python3 skills/product-business/document-spreadsheet-tooling-readiness/scripts/libreoffice_headless.py --check
```

Use the native command for the current developer environment only when diagnosing discovery:

```powershell
where.exe pandoc
where.exe soffice
where.exe wkhtmltopdf
where.exe tesseract
```

```bash
command -v pandoc
command -v soffice || command -v libreoffice
command -v wkhtmltopdf
command -v tesseract
```

On Windows, use `where.exe`; on macOS, Debian/Ubuntu, and Fedora/RHEL, use `command -v`. Install missing binaries through the environment's approved package or application-management route, rerun the readiness check, then run the smoke test. Do not permanently change `PATH` merely to make a one-off conversion work.

## Smoke Test Requirement

Generate and reopen:

- One trivial `.docx` with `python-docx`.
- One trivial `.xlsx` with `openpyxl`.

If either fails, do not promise production file output until fixed or use a fallback.

For any DOCX-to-PDF conversion, use the isolated-profile launcher in `references/libreoffice-headless.md`, then reopen or render the output for validation.
