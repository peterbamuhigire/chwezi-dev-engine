# Cross-Platform LibreOffice Headless Support

Date: 2026-07-17

## Change

Added a shared launcher under `skills/product-business/document-spreadsheet-tooling-readiness/scripts/libreoffice_headless.py` for isolated, verified background LibreOffice conversions on Windows, macOS, Debian/Ubuntu, and Fedora/RHEL-family environments.

## Decision

Use a temporary profile expressed as a URI from `Path.as_uri()` for each headless job. This avoids Windows interpreting a native path after `file://` as a corrupt `bootstrap.ini` configuration and prevents concurrent jobs from using the interactive LibreOffice profile.

## Operational contract

- Run `--check` before promising conversion on a new developer environment.
- Run conversions through the shared launcher with a bounded timeout and no shell.
- Refuse pre-existing derived output unless replacement is explicit.
- Capture diagnostics, confirm the output is non-empty, then perform deliverable-appropriate visual or semantic validation.
- Use `--keep-profile` only during diagnosis and remove the retained profile after investigation.

## Scope

The document-spreadsheet tooling readiness and professional Word-output skills now direct agents to this contract. Existing fallback routes remain in force if LibreOffice is unavailable or cannot faithfully export the source document.
