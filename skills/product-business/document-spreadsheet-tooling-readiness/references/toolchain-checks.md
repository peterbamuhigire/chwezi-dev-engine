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

```powershell
where.exe pandoc
where.exe soffice
where.exe wkhtmltopdf
where.exe tesseract
```

## Smoke Test Requirement

Generate and reopen:

- One trivial `.docx` with `python-docx`.
- One trivial `.xlsx` with `openpyxl`.

If either fails, do not promise production file output until fixed or use a fallback.
