# Python Desktop Distribution

Parent: [Python Modern Standards](../SKILL.md)

Last verified: 2026-07-17
Primary target: Windows desktop suites
Default packager: PyInstaller one-folder multipackage bundle

## Contents

1. Outcome and decision
2. Architecture contract
3. Frozen-runtime rules
4. Manifest-driven automation
5. Generated project files
6. Build and release workflow
7. CI and signing
8. Validation matrix
9. Failure handling
10. Alternatives and revisit triggers
11. Sources

## Outcome and decision

Use this workflow when users need to distribute one Python desktop application or a suite of related tools without requiring customers to install Python.

For a suite, generate one installed product containing a launcher executable, one executable per independently runnable tool, and one shared `_internal` directory. Package that directory as both a portable ZIP and a Windows installer.

```text
Example Suite/
|-- ExampleSuite.exe
|-- ExampleEditor.exe
|-- ExampleConverter.exe
|-- ExampleCLI.exe
`-- _internal/
    |-- Python runtime
    |-- shared extension modules
    `-- bundled application data
```

Distribute one installer to normal users. Expose only the launcher shortcut unless a tool has a justified direct shortcut.

Do not treat auto-py-to-exe as the release definition. It is a useful PyInstaller interface for experiments, but the durable release contract is a committed manifest plus generated spec, installer, CI, and verification files.

## Architecture contract

### Required boundaries

| Boundary | Owns | Must not own |
|---|---|---|
| Product manifest | identity, applications, data files, bundle options, release gates | executable Python logic |
| Generated launcher | display and child-process start | document-processing or business rules |
| Application entry point | one process and its argument contract | installation or self-update logic |
| PyInstaller spec | analyses, data collection, executables, shared `COLLECT` | secrets or user configuration |
| Installer | installation, shortcuts, uninstall, version metadata | mutable user data |
| Release workflow | clean build, tests, packaging, hashes, signing, evidence | application feature logic |

### Process model

- Run each tool in its own process when it owns a GUI event loop, local HTTP server, watch loop, or long-running worker.
- Use a generated launcher for suites unless an existing launcher already starts installed executables safely.
- Pass arguments as arrays and keep `shell=False`.
- Resolve child executables relative to `Path(sys.executable).resolve().parent` in a frozen application.
- Keep user data under an operating-system user-data directory, not beside the executable or under `_internal`.
- Bind local web adapters to `127.0.0.1`; disable debug mode and development reloaders.

## Frozen-runtime rules

PyInstaller changes runtime meanings:

- `sys.executable` is the frozen bootloader or application executable, not `python.exe`.
- `sys._MEIPASS` is the bundle directory used by PyInstaller.
- A bundled module's `__file__` points inside the bundle and is appropriate for read-only bundled resources.
- `Path(sys.executable).parent` identifies the installed executable directory.

Never use this source-mode pattern in a frozen launcher:

```python
subprocess.Popen([sys.executable, "other_tool.py"])
```

Use an installed child executable:

```python
from pathlib import Path
import subprocess
import sys

suite_dir = Path(sys.executable).resolve().parent
subprocess.Popen([str(suite_dir / "ExampleConverter.exe")], shell=False)
```

If one frozen executable intentionally starts a fresh independent copy of itself, define and test an explicit argument-dispatch contract. Follow PyInstaller's environment-reset guidance for a child that must not inherit the current bootloader environment.

Treat bundled data as read-only. Copy an editable default to the user's configuration directory on first use; never edit the copy inside a one-file extraction directory or `_internal`.

## Manifest-driven automation

Use `../scripts/desktop_suite_packager.py` from the skill directory.

### Initialise a project

```powershell
python -X utf8 desktop_suite_packager.py init `
  --project-root C:\source\ExampleSuite `
  --product-name "Example Suite" `
  --publisher "Example Ltd" `
  --app "editor=src/example_suite/editor_app.py" `
  --app "converter=src/example_suite/converter_app.py"
```

This creates `packaging/desktop-suite.toml`. The command refuses to overwrite an existing manifest unless `--force` is supplied.

### Manifest shape

```toml
schema_version = 1

[product]
name = "Example Suite"
slug = "example-suite"
version = "0.1.0"
publisher = "Example Ltd"
audience = "external"
license_file = "LICENSE"
notices_file = "THIRD_PARTY_NOTICES.md"
icon = "packaging/app.ico"
# Optional when the project already has a frozen-safe launcher:
# launcher_script = "index-app.py"

[build]
python_version = "3.12"
generated_dir = "packaging/generated"
work_dir = "build/desktop-suite"
dist_dir = "release"
portable_zip = true
installer = true
signing_required = true
paths = [".", "src"]
hidden_imports = []
collect_all = ["customtkinter"]

[ci]
enabled = true
workflow_path = ".github/workflows/windows-desktop-suite.yml"
uv_sync_args = ["sync", "--locked", "--all-extras", "--group", "desktop-build"]

[[applications]]
id = "editor"
display_name = "Example Editor"
description = "Edit example documents"
script = "src/example_suite/editor_app.py"
executable = "ExampleEditor"
console = false
smoke_args = []

[[applications]]
id = "converter"
display_name = "Example Converter"
description = "Convert example documents"
script = "src/example_suite/converter_app.py"
executable = "ExampleConverter"
console = false
smoke_args = ["--help"]

[[data]]
source = "templates"
destination = "templates"
```

Keep every manifest path relative to the project root. Reject absolute paths and `..` traversal so generation remains portable and cannot collect files outside the project.

### Generate and inspect

```powershell
python -X utf8 desktop_suite_packager.py generate --config C:\source\ExampleSuite\packaging\desktop-suite.toml
python -X utf8 desktop_suite_packager.py doctor --config C:\source\ExampleSuite\packaging\desktop-suite.toml
```

Commit the manifest and generated files. The generated build script verifies the manifest hash and fails if generation is stale.

## Generated project files

| File | Purpose |
|---|---|
| `packaging/generated/suite_launcher.py` | Standard launcher; omitted when `launcher_script` reuses an existing frozen-safe launcher |
| `packaging/generated/<slug>.spec` | PyInstaller one-folder multipackage build with shared `COLLECT` |
| `packaging/generated/<slug>.iss` | Inno Setup installer definition |
| `scripts/build-desktop-suite.ps1` | Tests, builds, verifies, hashes, zips, signs, and optionally creates the installer |
| `.github/workflows/windows-desktop-suite.yml` | Clean Windows CI build and artifact upload |
| `packaging/generated/manifest.sha256` | Staleness guard for all generated files |

Generated files contain a header naming the manifest and its hash. Regenerate; do not hand-edit them. Put project-specific changes in the manifest or application entry points.

## Build and release workflow

### Project prerequisites

Create a locked build group containing PyInstaller and the application's runtime extras. Example:

```toml
[dependency-groups]
desktop-build = [
  "pyinstaller>=6.21,<7",
]
```

Retain GUI frameworks, PDF libraries, web adapters, and optional tool dependencies in normal project dependency or extra groups. `desktop-build` adds release tooling; it does not replace runtime declarations.

### Local development build

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build-desktop-suite.ps1 -UnsignedDevelopmentBuild
```

Unsigned builds are for local verification only. Do not upload or label them as public releases.

### Release build

```powershell
$env:WINDOWS_CERT_SHA1 = "<certificate thumbprint supplied by the release environment>"
$env:WINDOWS_TIMESTAMP_URL = "<approved RFC 3161 timestamp URL>"
powershell -ExecutionPolicy Bypass -File scripts\build-desktop-suite.ps1
```

The build must:

1. Verify the manifest has not changed since generation.
2. Restore the locked environment.
3. Run configured quality commands before packaging.
4. Build the one-folder suite.
5. Confirm every declared executable and data destination exists.
6. Run non-interactive smoke arguments where declared.
7. Produce a portable ZIP when enabled.
8. Sign generated executables when required.
9. Compile and sign the installer when enabled.
10. Write artifact hashes, sizes, smoke results, dependency versions, and signing status to `desktop-suite-evidence.json`.

Build separately on every target operating system. PyInstaller output is operating-system and Python-version specific; do not build Windows executables on Linux and claim equivalent validation.

## CI and signing

The generated GitHub Actions workflow uses a Windows runner and a locked uv environment. Pin third-party actions to reviewed revisions when the project security policy requires immutable references. Re-verify action versions during scheduled release-tool maintenance.

Keep certificate material outside the repository. Supply a certificate thumbprint or signing-service identity through protected CI secrets. Never place a PFX password, private key, certificate blob, or signing token in the manifest, workflow, spec, or source tree.

For public Windows distribution:

- sign every release with a consistent publisher identity;
- timestamp signatures;
- sign the installer after its final bytes are produced;
- verify signatures with an independent command before upload;
- publish SHA-256 hashes beside release artifacts;
- expect new publisher or file hashes to receive SmartScreen scrutiny initially;
- consider Microsoft Store distribution when it fits the product and audience.

## Validation matrix

| Layer | Minimum evidence | Release blocker |
|---|---|---|
| Manifest | schema, unique IDs and executable names, safe relative paths | invalid or ambiguous application mapping |
| Source | every entry script imports or executes in the locked environment | missing import or runtime package installation |
| Static process scan | no launcher `sys.executable + .py`, unsafe `shell=True`, public debug server, or bundle-relative writes | unresolved high-risk match |
| Build | PyInstaller completes without untriaged warnings | missing hidden import, binary, or data file |
| Structure | all declared EXEs and data destinations present | incomplete bundle |
| Smoke | CLI exits successfully; GUI/server starts without immediate crash | declared smoke test fails |
| Clean machine | launch on a supported Windows VM with no Python installed | dependency on developer machine state |
| Security | dependency audit, secret scan, Authenticode verification | critical advisory, secret, or required signature absent |
| Installer | install, repair/upgrade, uninstall, shortcut, user-data preservation | destructive or unrecoverable installer behaviour |
| Evidence | version, hashes, sizes, tests, signature state, residual risks | evidence file missing or contradicts artifact state |

Perform manual GUI checks for window display, file dialogs, error states, high-DPI behaviour, taskbar icon, browser opening, child-process lifecycle, and shutdown. Automation reduces repeated mechanics; it does not prove interactive usability.

## Failure handling

| Failure | Response |
|---|---|
| Frozen launcher opens itself recursively | replace source-script launch with installed child executable or explicit self-dispatch mode |
| Tool works from source but not bundle | inspect PyInstaller warnings, hidden imports, dynamically loaded plugins, and data mappings |
| Flask/Jinja template missing | map `templates` and `static` to the module's expected bundle-relative destinations |
| Application writes into `_internal` | move mutable state to `platformdirs` or another operating-system user-data path |
| Antivirus removes an unsigned build | verify provenance and dependencies; sign release artifacts; never advise disabling protection globally |
| One-file startup is slow or leaves temporary files | return to one-folder mode or justify a measured one-file requirement |
| External executable loads incompatible bundled libraries | sanitise the child environment according to PyInstaller runtime guidance |
| CI bundle differs from local bundle | compare lockfile, Python version, PyInstaller version, spec hash, and artifact inventory |

## Alternatives and revisit triggers

| Option | Use when | Revisit trigger |
|---|---|---|
| PyInstaller one-folder multipackage | default suite distribution; fast diagnosis and shared resources | bundle cannot meet measured size, startup, or platform requirements |
| PyInstaller one-file dispatcher | a literal single file is a contractual requirement and all tools share one window/console model | extraction cost, independent child processes, or mutable resources become problematic |
| Nuitka standalone | measured performance, source transformation, or PyInstaller incompatibility justifies compiler complexity | build time, plugin maintenance, or binary compatibility costs exceed benefit |
| Briefcase/MSIX/Store path | native package management or Store distribution is a primary requirement | unsupported dependency or application model blocks delivery |
| Unified PySide6 shell | product is ready to replace several legacy GUIs with one workspace over shared services | application-service seams or feature parity are not mature |

Do not switch packagers to avoid refactoring unsafe launcher or resource assumptions. Fix the application boundaries first, then compare tools with the same smoke corpus and release gates.

## Sources

- PyInstaller 6.21 run-time information: https://pyinstaller.org/en/stable/runtime-information.html
- PyInstaller 6.21 operating modes: https://pyinstaller.org/en/stable/operating-mode.html
- PyInstaller 6.21 spec and multipackage guidance: https://pyinstaller.org/en/stable/spec-files.html
- PyInstaller 6.21 common subprocess pitfalls: https://pyinstaller.org/en/stable/common-issues-and-pitfalls.html
- auto-py-to-exe project description and configuration export: https://github.com/brentvollebregt/auto-py-to-exe
- Nuitka standalone and one-file modes: https://nuitka.net/user-documentation/user-manual.html
- Microsoft SmartScreen reputation guidance: https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation
- Inno Setup signed uninstaller guidance: https://jrsoftware.org/ishelp/topic_setup_signeduninstaller.htm
