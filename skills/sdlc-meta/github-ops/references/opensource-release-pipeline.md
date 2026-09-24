# Open-Source Release Pipeline

Parent skill: [github-ops](../SKILL.md). Absorbed from the retired `opensource-pipeline` skill
(2026-09-24; originally adapted from `affaan-m/ECC` `skills/opensource-pipeline/SKILL.md`, with
ECC's three dedicated subagent types replaced by scoped general-purpose agent runs). The original
text is retained in `skills/sdlc-meta/opensource-pipeline/ALIAS.md`.

Load this reference when a private project (client codebase or a Chwezi engine) is to be made
public on GitHub: "open source this", "make this repo public", "prepare this for release".
It is a prerequisite before publishing any Chwezi engine. Do not use it for an already public
repository or without publishing authority.

Three stages, each a gate: **Fork** (copy and strip) -> **Sanitise** (verify, fail closed) ->
**Package** (README, LICENCE, setup). Publishing is a fourth, user-approved step.

## Inputs to confirm with the user

- Source path (resolve absolute; ask if unresolved).
- Licence: MIT, Apache-2.0, GPL-3.0, or BSD-3-Clause. House convention: MIT for public engines,
  "All Rights Reserved" for private ones.
- GitHub owner (default `gh api user -q .login`), repository name, and a one-line description
  (draft it from the project, then confirm).
- Whether git history must be preserved (default: no).
- Client-disclosure clearance for any client or employee names in the code.

Staging path: `$HOME/opensource-staging/<project>/`. The staging tree persists for review until
explicitly cleaned.

## Stage 1 - Fork

1. Copy the project excluding `.git`, `node_modules`, `__pycache__`, `.venv`, `vendor/` caches,
   and build output.
2. Strip secrets and credentials (API-key patterns, tokens, connection strings, `.env` values).
   Replace each value with a `{{PLACEHOLDER}}`; never delete the functionality that used it.
3. Replace internal references: internal hostnames, employee names, uncleared client names,
   internal ticket links.
4. Generate `.env.example` listing every variable the code reads, with placeholder values and a
   one-line purpose comment each.
5. History: default to a fresh `git init`. If history must be kept, scrub it with
   `git filter-repo` and treat every historical commit as in scope for Stage 2. Ask; never assume.
6. Write `FORK_REPORT.md`: copied, stripped, substituted, and unresolved items.

## Stage 2 - Sanitise (the safety gate)

Scan the staging tree, with the source available for diffing:

| Check | Severity |
|---|---|
| Secrets re-scan, including binaries, minified bundles, unusual config formats | Critical |
| PII in code, comments, fixtures, and sample data (names, emails, phone numbers, addresses) | Critical |
| Internal references missed by Stage 1 (URLs, unreleased products, client names) | Critical |
| Dangerous files: `.env`, `*.pem`, `*.key`, `credentials.json`, database dumps, backups | Critical |
| Agent configuration (`.claude/`, `AGENTS.md`, hooks) exposing internal paths or permissive settings; use `security/code-safety-scanner` `references/agent-harness-config-scan.md` | Critical |
| `.env.example` covers every variable; no references to stripped files | Warning |
| Preserved history free of secrets in every commit (`git log -p` search or a history scanner) | Critical when history kept |

Write `SANITIZATION_REPORT.md` with PASS, PASS WITH WARNINGS, or FAIL.

On FAIL: show findings, ask whether to fix and re-scan or abort. Maximum three fix-and-rescan
cycles, then present all findings for manual resolution (the convergence discipline in
`sdlc-meta/santa-method`). Never proceed with an open critical finding.

A public Chwezi repository was once found with real client history on its public `main`;
`.gitignore` does not remove history already pushed. That is why the default is a fresh
repository and why history is scanned when kept.

## Stage 3 - Package

Generate in the staging tree:

1. `README.md` (fresh or enhanced): what it is, install, usage, licence.
2. Router docs (`CLAUDE.md` / `AGENTS.md`) when the project is itself an agent-consumable engine.
3. `setup.sh` one-command bootstrap, executable.
4. `LICENSE` matching the chosen licence.
5. `CONTRIBUTING.md`.
6. `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md`.

## Stage 4 - Final review and publish (explicit approval only)

Present: location, licence, generated files, `.env.example` variable count, sanitisation verdict,
and next steps. Publish only after the user says yes:

```bash
cd "$HOME/opensource-staging/<project>"
gh repo create "<owner>/<repo>" --public --source=. --push --description "<description>"
```

After publishing, enable secret scanning and Dependabot alerts and monitor them with the
Security Monitoring section of the parent skill.

## Sub-commands (when the runner supports slash commands)

| Command | Action |
|---|---|
| `/opensource fork PROJECT` | Stages 1-4 |
| `/opensource verify PROJECT` | Stage 2 only; regenerate the report |
| `/opensource package PROJECT` | Stage 3 only |
| `/opensource list` | List staged projects and report presence |
| `/opensource status PROJECT` | Print one project's reports |

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Pushing without explicit approval | Stop at Stage 4 and ask |
| Skipping Stage 2 | It is the gate, never optional |
| Proceeding after FAIL | Fix every critical finding, re-scan |
| Deleting functionality to remove a secret | Parameterise the value |
| Assuming history does not matter | Ask; default to a fresh repository |
| Publishing after a partial scan | Complete every check and keep the report |

Related: `security/code-safety-scanner` (secret and vulnerability patterns used in Stage 2),
`security/web-app-security-audit`, `sdlc-meta/santa-method`.

## Evidence and currentness

`gh repo create --public --source --push` and `git filter-repo` usage carried over from the
absorbed skill; not re-verified against docs.github.com / cli.github.com on 2026-09-24
(NOT_ASSESSED).
