# Python Desktop-Suite Automation Update

Date: 2026-07-17
Owner: skills-web-dev maintainers

## Decision

Route PyInstaller, auto-py-to-exe, Nuitka, frozen desktop applications, multi-tool executable suites, portable ZIPs, Windows installers, signing, and packaging CI through `python-modern-standards`.

Keep this as a reference and deterministic script under the existing Python baseline instead of adding another active skill. This avoids routing competition while giving downstream projects a reproducible release system.

## Delivered

- `references/python-desktop-distribution.md` records the architecture, frozen-runtime rules, manifest contract, release gates, failure handling, and alternative-selection triggers.
- `scripts/desktop_suite_packager.py` creates a project manifest and generates a standard-library launcher, PyInstaller multipackage spec with shared `COLLECT`, Inno Setup definition, PowerShell build, GitHub Actions verification workflow, and manifest staleness hash.
- The generated build verifies declared executables and data paths, runs configured quality commands and smoke arguments, creates a portable ZIP, exposes Authenticode hooks, compiles an installer when available, and writes SHA-256 artifact evidence.
- Routing fixtures cover executable-suite and failed auto-py-to-exe launcher prompts.
- The framework source register records dated official PyInstaller, auto-py-to-exe, Nuitka, Microsoft signing, and Inno Setup sources.

## Verification

The generator was exercised against a disposable two-application project on Windows with Python 3.12 and PyInstaller 6.21. The generated launcher and spec passed Python parsing, the PowerShell build passed its parser, PyInstaller produced three executables in one shared bundle, both child executables exited successfully, and the launcher remained running until intentionally terminated.

Repository catalog, contract, routing, and anti-slop gates remain required before release.

## Delivery evidence pack

### Artifact identity

| Field | Value |
|---|---|
| Project | skills-web-dev |
| Deliverable | Reusable Python desktop-suite distribution automation |
| Owner | Peter Bamuhigire / skills-web-dev maintainers |
| Date | 2026-07-17 |
| Related skills | `python-modern-standards`, `skill-writing`, `skill-composition-standards`, `world-class-engineering` |

### Decision record

| Decision | Rationale | Alternatives rejected | Reversal trigger |
|---|---|---|---|
| Extend `python-modern-standards` with a reference and deterministic generator | Executable distribution is a Python baseline concern and does not justify another routing entrypoint | auto-py-to-exe configuration alone; unrelated new active skill; literal one-file bundle as the default | Routing evidence shows a distinct skill is needed, or PyInstaller one-folder multipackage builds fail measured requirements |
| Generate project-local release files from one TOML manifest | CI remains independent of the local skills engine while product metadata and tool mappings stay declarative | CI reading files directly from a workstation skills path; hand-maintained duplicate build files | Generated-file maintenance becomes harder than a supported package or central action |

### Contract evidence

| Contract | Evidence | Location | Result |
|---|---|---|---|
| Trigger and routing | Updated skill description, routing index, and two edge fixtures | `python-modern-standards/SKILL.md`, `docs/skill-routing-index.md`, `tests/routing/edge-fixtures.yml` | pass |
| Manifest schema | Safe relative paths, unique IDs and executable names, explicit product/build/CI/application/data tables | `desktop_suite_packager.py` | pass |
| Generated release contract | Launcher, PyInstaller spec, Inno Setup definition, PowerShell build, CI workflow, and manifest hash | `desktop_suite_packager.py` | pass |
| Release evidence | Generated build emits version, manifest hash, artifact hashes and sizes, smoke results, and signing state | generated `desktop-suite-evidence.json` | pass |

### Test evidence

| Check | Evidence | Result |
|---|---|---|
| Generator Python compile | `python -X utf8 -W error -m py_compile desktop_suite_packager.py` | pass |
| Ruff lint and format | `ruff check`; `ruff format --check` | pass |
| Generated launcher compile | disposable fixture `suite_launcher.py` | pass |
| Generated spec parse | Python AST parse | pass |
| Generated PowerShell parse | PowerShell language parser | pass |
| Real multipackage build | PyInstaller 6.21.0, Python 3.12.10, Windows 11 | pass |
| Child executable smoke | `Editor.exe` and `Converter.exe` returned exit code 0 | pass |
| Launcher smoke | generated launcher remained running for two seconds and was intentionally terminated | pass |
| Skill validator | `quick_validate.py` | pass |
| Contract validator | `contract_gate.py` | pass |
| Catalog guardrail | 168 active skills, 0 findings | pass |
| Routing smoke | 167 fixtures, precision@1 92%, precision@3 100%, 0 failures | pass |

### Operational evidence

| Area | Evidence | Residual requirement |
|---|---|---|
| Rollback | Generated files are derived; revert the engine change or regenerate from the prior manifest | Downstream projects must commit manifest and generated files together |
| Diagnostics | `doctor` reports missing entry scripts, data, legal files, uv, Inno Setup, and risky source patterns | Deep dynamic-import and GUI behaviour still require project tests |
| Signing | Build script requires certificate thumbprint and timestamp URL for signed external releases | Each publisher must configure its approved certificate or signing service |
| Clean-machine release | Reference requires a supported Windows VM with no Python installed | Not run against a real downstream product in this engine-only change |

### Source and currency evidence

Official PyInstaller, auto-py-to-exe, Nuitka, Microsoft signing, and Inno Setup sources are recorded with 2026-07-17 verification and 2026-10-17 review dates in `docs/source-registers/ai-platforms.md`.

### Anti-slop gate

Verdict: A - clean. Genericness score: 8/100, manual assessment. The update names the concrete manifest, generated artifacts, commands, versions, failure modes, and release blockers. The banned-phrase scan returned no matches. No dependency, capability, or test result is presented without a corresponding source or executed check.

### Release verdict

| Gate | Verdict | Note |
|---|---|---|
| Architecture | pass | One manifest drives isolated executables and shared collection output |
| Security | pass with downstream conditions | Unsafe source patterns are scanned; public signing and project dependency audit remain downstream gates |
| Reliability | pass | Generated files are hash-guarded and the multipackage build was executed |
| Documentation | pass | Skill, reference, source register, routing, overview, and update record align |
| Anti-slop | pass | A verdict; no blocking markers |

Final release decision: ship the skills-engine update. Treat generated unsigned packages as development artifacts until a downstream project satisfies signing, licence, notices, clean-machine, and GUI acceptance gates.
