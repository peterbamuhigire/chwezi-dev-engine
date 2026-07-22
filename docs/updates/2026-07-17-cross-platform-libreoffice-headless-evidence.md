# Cross-Platform LibreOffice Headless Evidence

## 1. Artifact Identity

| Field | Value |
|---|---|
| Project | Chwezi skills engine |
| Deliverable | Shared headless LibreOffice launcher and consuming skill updates |
| Owner | Peter Bamuhigire |
| Reviewer | Codex |
| Date | 2026-07-17 |
| Related skills | `document-spreadsheet-tooling-readiness`, `professional-word-output`, `skill-writing` |

## 2. Decision Record

| Decision | Rationale | Alternatives rejected | Reversal trigger |
|---|---|---|---|
| Use one standard-library Python launcher with an isolated temporary profile | Prevents profile contention and converts Windows paths to valid file URIs | Hand-built `soffice` commands, a shared interactive profile, and editing `bootstrap.ini` | LibreOffice publishes a portable background-job interface that removes profile URI requirements |

## 3. Contract Evidence

| Contract | Evidence | Location | Pass/fail |
|---|---|---|---|
| LibreOffice discovery | `--check` located `C:\Program Files\LibreOffice\program\soffice.exe` on Windows | `libreoffice_headless.py` | Pass |
| Isolated profile URI | A profile path containing spaces generated `file:///C:/Temp/Profile%20With%20Space` | `user_installation_argument` test | Pass |
| Output contract | A 473,289-byte PDF was created; pre-existing output was rejected unless `--overwrite` was explicit | Windows integration run | Pass |

## 4. Test Evidence

| Layer | Required evidence | Result |
|---|---|---|
| Unit | URI encoding for a Windows path with spaces | Pass |
| Integration | Convert `Medic8_Compliance.docx` to PDF through the shared launcher | Pass: 25-page PDF 1.7 |
| Static quality | `py_compile`, Ruff, no shell execution or placeholder-pattern hits | Pass |
| Skill contracts | `quick_validate.py` and `contract_gate.py` on both changed skills | Pass |
| Catalog and routing | Catalog guardrails and routing smoke test | Pass: 0 catalog findings; 168/168 top-three fixtures |
| Cross-platform runtime | macOS, Debian/Ubuntu, Fedora/RHEL live executions | Not assessed on this Windows host; each host must run `--check` before use |

## 5. Operational Evidence

| Area | Evidence required | Release blocker |
|---|---|---|
| Diagnostics | Captured stdout and stderr are included in launcher errors | No |
| Cleanup | Temporary profile root had zero entries after the successful conversion | No |
| Timeout | Default 120-second bounded conversion timeout; configurable per run | No |
| Recovery | `--keep-profile` preserves the profile only for diagnosis; fallback routes remain documented | No |

## 6. Source and Currency Evidence

No volatile external platform claim is required. The implementation uses Python standard-library path URI generation and validates the installed LibreOffice 26.2.4.2 behaviour directly on Windows.

## 7. Anti-Slop Gate

- The change records one concrete decision: isolated profile URI generation instead of path-string concatenation.
- The failure mode that names `bootstrap.ini` is documented with a specific invalid and valid URI form.
- The launcher rejects stale output, captures errors, applies a timeout, and does not use a shell.
- macOS and Linux execution remains explicitly unassessed rather than claimed as verified.

## 8. Release Verdict

| Gate | Verdict | Reviewer note |
|---|---|---|
| Architecture | Pass | One reusable launcher prevents duplicated platform-specific process construction |
| Security | Pass | Standard library only; process arguments are passed as a list without a shell |
| Reliability | Pass | Isolated profiles, timeout, output verification, and stale-output refusal are implemented |
| Data | Not applicable | No persistent application data changes |
| Docs/runbook | Pass | Readiness, fallback, Word output, and update records link to the shared contract |
| Anti-slop | Pass | Verdict A; low genericness, concrete evidence, no unsupported runtime claim |

Final release decision: ship for Windows; require `--check` and a smoke conversion on each macOS, Debian/Ubuntu, and Fedora/RHEL environment before production use.
