# Cross-Platform LibreOffice Headless Conversion

This reference belongs to `document-spreadsheet-tooling-readiness`. Read it before converting or rendering Office documents in the background with LibreOffice.

## Supported environments

The shared launcher supports Windows, macOS, Debian or Ubuntu, and Fedora or RHEL-family developer environments. It discovers `soffice` or `libreoffice` on `PATH`; on Windows it also checks the standard Program Files locations, and on macOS it checks the standard LibreOffice application bundle. It does not alter the machine-wide `PATH` or any installed LibreOffice files.

Run this readiness check from the skills repository root before promising conversion on a new environment:

```powershell
python -X utf8 skills/product-business/document-spreadsheet-tooling-readiness/scripts/libreoffice_headless.py --check
```

```bash
python3 skills/product-business/document-spreadsheet-tooling-readiness/scripts/libreoffice_headless.py --check
```

If discovery fails, install LibreOffice through the approved package or application-management route for that environment, then rerun `--check`. Do not edit `bootstrap.ini` as a first response to a headless startup error.

## Required background-conversion contract

Use the shared launcher instead of constructing a raw `soffice` command. It creates a unique temporary profile for every job, uses a standards-compliant file URI, runs without a shell, captures stdout and stderr, applies a timeout, verifies the expected output exists and is non-empty, and removes the temporary profile by default.

```powershell
python -X utf8 skills/product-business/document-spreadsheet-tooling-readiness/scripts/libreoffice_headless.py `
  --input path/to/source.docx `
  --output-dir tmp/converted `
  --to pdf `
  --timeout 120
```

```bash
python3 skills/product-business/document-spreadsheet-tooling-readiness/scripts/libreoffice_headless.py \
  --input path/to/source.docx \
  --output-dir tmp/converted \
  --to pdf \
  --timeout 120
```

Use `--overwrite` only when replacement of the derived output file is intentional. Use `--keep-profile` only for diagnosis; record and delete that profile when the investigation ends.

## Windows bootstrap.ini symptom

The error naming `bootstrap.ini` can be caused by an invalid temporary-profile URI, even when the installation file is valid. Never create the setting with string concatenation such as `file://C:\\temp\\profile`. Generate it through `Path(profile_dir).resolve().as_uri()` so Windows receives `file:///C:/temp/profile` and paths containing spaces are percent-encoded.

Do not reuse the interactive user's LibreOffice profile for background work. Concurrent jobs can collide on profile locks, recovery state, and extension state. An isolated profile is mandatory for each conversion job.

## Failure handling and validation

| Finding | Action | Do not do |
|---|---|---|
| `--check` reports unavailable | Install or expose LibreOffice, then rerun readiness | Assume a GUI launch proves headless conversion is ready |
| Conversion times out | Preserve diagnostics with `--keep-profile`, inspect the input and retry with a bounded higher timeout | Wait indefinitely or leave a shared profile locked |
| Non-zero exit or missing output | Read captured stdout and stderr, verify the requested filter and source format, then use the documented fallback route | Claim a PDF or spreadsheet was generated |
| Existing derived output | Choose a fresh output directory or make replacement explicit with `--overwrite` | Treat an old output as proof of a new conversion |
| Conversion succeeds | Open or parse the output and inspect rendered pages, tables, formulas, or text appropriate to the deliverable | Treat file existence alone as visual validation |

Use `references/fallback-routes.md` when LibreOffice is unavailable or cannot convert the input faithfully.
