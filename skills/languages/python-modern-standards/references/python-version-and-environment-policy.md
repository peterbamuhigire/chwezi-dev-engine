# Python Version and Environment Policy

Load when choosing the Python version for a new or existing service, setting `requires-python`, deciding which versions CI must cover, provisioning interpreters on Windows/Ubuntu/Debian, or diagnosing "wrong interpreter / module not found / installed but not importable" problems.

## Inputs

| Input | Where it comes from | If absent |
| --- | --- | --- |
| Deployment targets (Debian/Ubuntu release, container base, Windows desktop) | Ops runbook, Dockerfile | Assume container with uv-managed Python |
| Heaviest native dependencies (numpy, pandas, torch, pyarrow, psycopg) | `pyproject.toml` | Check their wheel matrix before choosing a version |
| Whether the code is a library (published) or an application (deployed) | Repo purpose | Treat as application |

## Support status (verify every cycle)

Python ships one feature release each October and supports it for five years: roughly two years of bugfix releases with binaries, then security-only source releases until end-of-life (PEP 602). Status at 2026-09-24 from devguide.python.org/versions:

| Branch | Status | End of life |
| --- | --- | --- |
| 3.15 | prerelease (final due 2026-10-01) | 2031-10 |
| 3.14 | bugfix | 2030-10 |
| 3.13 | bugfix | 2029-10 |
| 3.12 | security only | 2028-10 |
| 3.11 | security only | 2027-10 |
| 3.10 | security only, EOL imminent | 2026-10 |
| 3.9 and older | end-of-life | - |

## Decision rules

1. **New application:** pin the interpreter to the newest *bugfix* branch that every runtime dependency ships wheels for. Today that is 3.13 by default, 3.14 once your numeric/ML stack has wheels (check PyPI "Download files" for `cp314`). Record it in `.python-version` with `uv python pin`.
2. **`requires-python` is a floor, never a ceiling.** Set it to the oldest version CI actually tests. An upper cap (`<3.13`) blocks resolvers and users for no safety gain; packaging.python.org warns against it. If a new version breaks you, fix forward or pin the interpreter, not the metadata.
3. **Library:** support every non-EOL version your dependencies support, and test all of them in a CI matrix. Drop a version in the release after its EOL, with a changelog line.
4. **Existing service on a security-only branch:** allowed, but open a migration ticket with a date at least six months before EOL. A service on an EOL interpreter is a security finding, not technical debt.
5. **Never develop against the OS Python.** Debian 12+ and Ubuntu 23.04+ mark the system interpreter as externally managed (PEP 668); `pip install` into it is refused or breaks OS tools. Use uv-managed interpreters (`uv python install 3.13`) or python.org installers, plus a project virtual environment.
6. **Prereleases** (3.15 today) belong in an allowed-to-fail CI job for libraries, not in production.

## Environment model an agent must hold

- An *environment* is an interpreter plus its `site-packages`. Packages install into the environment of the interpreter that runs the installer. This is why `python -m pip` (or `uv pip --python ...`) is safer than a bare `pip`: the bare command may belong to a different interpreter on `PATH`.
- A virtual environment is a directory with its own `site-packages` and a `pyvenv.cfg` pointing at the base interpreter. It borrows the standard library; it does not copy Python. Deleting and recreating it is always safe; commit the lockfile, never the venv.
- Activation only edits `PATH` and the prompt. Scripts and CI should call `.venv/bin/python` (or `.venv\Scripts\python.exe`) or `uv run` directly instead of relying on activation.
- Imports resolve through `sys.path`: the script's directory (or cwd for `-m`), `PYTHONPATH`, the standard library, then `site-packages`. The src layout exists so tests import the *installed* package rather than a stray local directory.
- Entry points (`[project.scripts]`) replace hand-written shebang scripts; the installer generates a launcher bound to the right interpreter.

## Per-platform provisioning

| Platform | Preferred | Acceptable | Avoid |
| --- | --- | --- | --- |
| Windows developer box | `uv python install` + `uv run`; the `py` launcher (`py -3.13`, `py --list`) for ad-hoc work | python.org installer, 64-bit, per-user | Microsoft Store Python for services; mixing Anaconda base with project work |
| Ubuntu/Debian server | Container image with uv-managed Python, or `uv python install` per service user | deadsnakes PPA (Ubuntu only) with a venv | `sudo pip install`; relying on the distro's version matching your pin |
| CI | `astral-sh/setup-uv` + `uv python install` from `.python-version` | `actions/setup-python` | Unpinned "latest" images |
| Data science workstation | uv project per analysis with a Jupyter kernel from that venv | conda/mamba when a binary-only dependency (e.g. GDAL stacks) requires it | One global environment shared by every notebook |

## Worked example

A Kampala logistics client runs a route-costing worker on Ubuntu 22.04 (system Python 3.10, EOL 2026-10). The dependency audit shows pandas 3.0 (needs 3.11+), pyarrow and psycopg all publish `cp313` wheels; one geospatial dependency lacks `cp314`. Decision: pin 3.13, set `requires-python = ">=3.13"`, build a container from a slim base with `uv python install`, leave the host interpreter untouched, and add a quarterly check for `cp314` wheels. Acceptance: `uv run python -c "import sys; print(sys.version)"` inside the image prints 3.13.x; CI job `py313` green; no `pip` invocation targets `/usr/bin/python3`.

## Quality gate

- [ ] `.python-version` exists and matches the CI interpreter.
- [ ] `requires-python` has a floor only; the floor is tested in CI.
- [ ] No production or CI path uses an EOL interpreter; security-only branches carry a dated migration ticket.
- [ ] No step installs into the OS interpreter.
- [ ] Heavy native dependencies confirmed to publish wheels for the pinned version.

## Senior vs generic output

Generic: "Use Python 3.x and create a virtualenv." Senior: names the branch and its EOL, justifies it against the wheel matrix, separates the interpreter pin from the metadata floor, and states how the environment is provisioned on each target without touching the system Python.

## Evidence/currentness

Access date 2026-09-24. Branch status and PEP 602 phases: devguide.python.org/versions. Upper-bound caution: packaging.python.org/en/latest/guides/writing-pyproject-toml. Wheel availability for 3.14 per dependency: `NOT_ASSESSED` (project-specific; check PyPI per dependency). Review by 2026-10-15 (3.15 final release, 3.10 EOL).

Sources: Jolowicz (2024) *Hypermodern Python Tooling* (early release); Python Developer's Guide; Python Packaging User Guide; uv documentation.
