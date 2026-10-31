# Tech Stack

## Repository Type

This is a documentation and skills repository. Most source files are Markdown
and YAML, with a small amount of Python, Node.js and PowerShell for maintenance.
The catalog now includes C#/.NET implementation guidance, but .NET is not a
runtime dependency of this repository.
It includes enterprise Java/JVM guidance, but the JDK, Maven, Gradle, Spring,
Jakarta runtimes, application servers, and databases are downstream project
toolchains rather than repository dependencies.
It also includes WWDC26-era Apple development guidance, but Xcode, Swift, and
Apple SDKs are downstream project toolchains rather than runtime dependencies
of this repository.
PHP runtime and Composer references are downstream application toolchains;
the repository records current PHP lifecycle/security sources and migration
checks without adding a PHP runtime dependency.
Android, Kotlin, Compose, Next.js, and database versions are also downstream
toolchains. The 2026-10 Kaizen's dated currentness and security applicability
records live in `docs/kaizen/2026-10-engine-kaizen/04-validation-record.md` and
`docs/source-registers/skills-engine-currentness-2026-09.json`; neither is a
substitute for checking the target project's exact runtime and dependency set.

## Tooling

The local AI contract utilities use Python standard-library dataclasses,
canonical JSON and SHA-256 hashes; no provider SDK or package was added.

| Tool | Use |
| --- | --- |
| Git | Version control. |
| PowerShell | Windows only: `install.ps1` and the optional `scripts/install-pdf-binaries.ps1`. No validator needs it; not run in the October 2026 passes. |
| Node.js | 18 or later for the standalone installer (`scripts/install-engine.js`) and the hook tests in `hooks/`. CI uses Node 24; the 2026-10-31 run used Node 22. |
| Python 3 | Catalog, routing, work-graph, two-axis review, diagnosis, lifecycle, source-register and control-plane validation. CI uses 3.12; the 2026-10-31 run used 3.14. Invoke as `python3` on Linux. |
| pytest | Repository validator tests (273 passed, 3 skipped on 2026-10-31), including temporary portfolio fixtures and malformed-input cases. Pinned to 9.0.3 in `requirements-ci.txt`. Live installed-portfolio checks are opt-in (`SKILL_ENGINE_LIVE_TESTS=1`) and report unavailable execution separately. |
| PyYAML | YAML parsing for the guardrail, routing and register scripts. Pinned to 6.0.2 in `requirements-ci.txt`; 6.0.3 also passed. |
| PHP CLI | Optional: runs the invoice example's PDO SQLite fixture (`php examples/tenant-invoice-listing/php/test.php`). Not used by CI. |
| GitHub Actions | CI: runs ten validation steps on every push to `main` and every pull request (`.github/workflows/skill-guardrails.yml`). |
| ripgrep | Optional file and text search; not installed on the Fedora validation host, where `find` does the same job. |
| Markdown | Skill bodies, plans, references, guides, and docs. |
| YAML | Skill frontmatter, alias registry, and routing fixtures. |
| JSON | Machine-readable twelve-entry control-plane registry; local checkout validation can target an explicit subset. |
| PyInstaller/Inno Setup guidance | Downstream Windows executable-suite generation; neither tool is a runtime dependency of this repository. |

## Important Commands

```sh
find skills 00-meta-initialization -name SKILL.md | wc -l   # active skills; 167 on 2026-10-31
python3 -X utf8 scripts/skill_catalog_guardrails.py --report-only
python3 -X utf8 scripts/routing_smoke_test.py
python3 -X utf8 scripts/routing_smoke_test.py --collisions
python3 -X utf8 scripts/validate_work_graph.py templates/work-graph.yml
python3 -X utf8 skills/languages/python-modern-standards/scripts/desktop_suite_packager.py --help
```

The root `README.md` section "Verify" lists the complete CI set and what each check
needs.

The routing smoke test has no external dependency beyond PyYAML; it models the
routing signal (skill name + description) as TF-IDF and asserts fixtured tasks
match the expected skill. It does not call an LLM, so CI stays deterministic.

Optional PDF helper setup (Windows only; not run in the October 2026 passes):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install-pdf-binaries.ps1
```

## Runtime And Deployment Context

| Environment | Role | Requirements |
| --- | --- | --- |
| Windows | Editing and maintenance environment on the maintainer's Windows machines. | PowerShell, Git, Python 3, ripgrep recommended; not re-run in the October 2026 passes. |
| Fedora Linux | Editing and validation environment on the maintainer's Linux workstation. | Git, Python 3, Node.js; every CI step ran here on 2026-10-31. |
| Ubuntu | Secondary validation target. | Python 3, Git, shell-compatible paths where possible. |
| Debian | Production-like downstream environment. | Keep docs and scripts portable. |

There is no repository-owned application runtime, database server, web server,
or package manager manifest. Database references inside skills describe
downstream project patterns rather than this repository's infrastructure.
The desktop-suite packager is a standard-library generator; PyInstaller, uv,
Inno Setup, and signing tools are validated in the downstream project where the
generated release pipeline runs.

## Cross-Platform Rules

- Prefer relative paths in documentation.
- Use forward slashes in prose unless showing a Windows command.
- Keep scripts explicit about encoding when reading Markdown or YAML.
- Do not assume case-insensitive paths.
- Avoid OS-specific instructions unless the section is clearly labeled.
