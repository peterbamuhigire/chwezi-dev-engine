---
name: opensource-pipeline
description: Fork, sanitize, and package a private project for safe public release — a 3-stage pipeline (fork/strip secrets, sanitize/verify clean, package for release). Use when a private project (including any of this consultancy's engines or client codebases) must be prepared for public GitHub release. Prerequisite before publishing any Chwezi engine publicly.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  origin: "Adapted from affaan-m/ECC skills/opensource-pipeline/SKILL.md; ECC's 3 dedicated subagent_types (opensource-forker/sanitizer/packager) do not exist in this engine, so each stage below is run as a scoped general-purpose agent invocation with the same protocol inlined, rather than a named subagent_type."
---

# Open-Source Pipeline Skill

Safely open-source any project through a 3-stage pipeline: **Fork** (strip secrets and internal
references) → **Sanitize** (verify clean, gate on failure) → **Package** (README, LICENSE, setup
instructions). This is the missing piece this Kaizen operation's own publishing work needs: secret
scanning already exists elsewhere in this estate (`skills/security/code-safety-scanner`,
`linux-skills`' secrets tooling), but the fork → sanitize → package chain and the git-history scrub
do not.

## When to Activate

- Preparing any private repo (a client project, or one of this consultancy's own skill engines) for
  public GitHub release
- Stripping secrets and internal references before a repo's first public push
- The user says "open source this", "make this public", or "prepare this for release"

## Commands

| Command | Action |
|---|---|
| `/opensource fork PROJECT` | Full pipeline: fork + sanitize + package |
| `/opensource verify PROJECT` | Run the sanitizer stage on an existing staged repo |
| `/opensource package PROJECT` | Generate README/LICENSE/setup docs only |
| `/opensource list` | Show all staged projects |
| `/opensource status PROJECT` | Show this project's stage reports |

## Protocol

### `/opensource fork PROJECT` — full pipeline

#### Step 1: Gather parameters

Resolve the project path (absolute/relative path, or check cwd, then `$HOME/PROJECT`, then ask).

```
SOURCE_PATH="<resolved absolute path>"
STAGING_PATH="$HOME/opensource-staging/${PROJECT_NAME}"
```

Ask the user: which project (if unresolved); license (MIT / Apache-2.0 / GPL-3.0 / BSD-3-Clause —
note this engine's own convention of MIT for public engines, "All Rights Reserved" for private
ones, per the Kaizen license pass); GitHub org/username (default: `gh api user -q .login`); repo
name (default: project name); a one-line description (draft one from the project, confirm with the
user).

#### Step 2: Create the staging directory

```bash
mkdir -p "$HOME/opensource-staging/"
```

#### Step 3: Fork stage

Run as a scoped agent invocation (or do it directly if the scope is small enough to stay
auditable in one pass) with this protocol:

1. Copy files, excluding `.git`, `node_modules`, `__pycache__`, `.venv`, and any project-specific
   build/cache directories.
2. Strip all secrets and credentials — grep for API key patterns, tokens, connection strings,
   `.env` contents; replace with `{{PLACEHOLDER}}` markers, never silently delete functionality.
3. Replace internal references with placeholders: internal hostnames, employee names, client names
   not cleared for disclosure, internal ticket/issue links.
4. Generate `.env.example` enumerating every environment variable the stripped code now expects,
   with placeholder values and a one-line purpose comment each.
5. Clean git history if the fork will carry history forward — either re-init a fresh repo (default,
   simplest and safest) or run a history-scrub tool (`git filter-repo`) if history must be
   preserved. **Default to a fresh `git init` unless the user explicitly needs history.**
6. Generate `{STAGING_PATH}/FORK_REPORT.md`: what was copied, what was stripped, what was
   placeholder-substituted, and any item that could not be automatically resolved.

#### Step 4: Sanitize stage — the safety gate

Run ALL scan categories against `{STAGING_PATH}`, with `{SOURCE_PATH}` available for diff reference:

1. **Secrets scan (CRITICAL)** — re-scan after forking; the fork stage can miss secrets embedded in
   binary files, minified bundles, or non-obvious config formats.
2. **PII scan (CRITICAL)** — names, emails, phone numbers, addresses in code, comments, test
   fixtures, or committed sample data.
3. **Internal references scan (CRITICAL)** — internal URLs, unreleased product names, client names,
   employee names not covered by the fork stage.
4. **Dangerous files check (CRITICAL)** — no `.env`, `*.pem`, `*.key`, `credentials.json`,
   database dumps, or backup files in the staged tree.
5. **Configuration completeness (WARNING)** — `.env.example` covers every variable the code reads;
   no orphaned references to files that were stripped.
6. **Git history audit** — if history was preserved, confirm no secret exists in any historical
   commit, not just the working tree (`git log -p` grep, or a dedicated history-scanning tool).

Generate `{STAGING_PATH}/SANITIZATION_REPORT.md` with a PASS / PASS WITH WARNINGS / FAIL verdict.

**If FAIL**: show findings to the user. Ask: fix and re-scan, or abort? If fixing, apply fixes and
re-run the sanitizer — maximum 3 retry attempts, after which present all findings and require
manual resolution rather than looping further (the same convergence discipline as
`sdlc-meta/santa-method`).

**If PASS or PASS WITH WARNINGS**: continue.

#### Step 5: Package stage

Generate for `{STAGING_PATH}`:
1. A project router doc (`README.md` at minimum; `CLAUDE.md`/`AGENTS.md` if the project is itself
   an agent-consumable skill engine) — commands, architecture summary, key files
2. `setup.sh` — one-command bootstrap, made executable
3. `README.md` (write fresh, or enhance an existing one) — what it is, install, usage, license
4. `LICENSE` matching the chosen license
5. `CONTRIBUTING.md`
6. `.github/ISSUE_TEMPLATE/` (`bug_report.md`, `feature_request.md`)

#### Step 6: Final review

Present to the user:

```
Open-Source Fork Ready: {PROJECT_NAME}

Location: {STAGING_PATH}
License: {license}
Files generated: README.md, LICENSE, CONTRIBUTING.md, setup.sh (executable), .env.example ({N} variables)
Sanitization: {verdict}

Next steps:
  1. Review: cd {STAGING_PATH}
  2. Create repo: gh repo create {org}/{repo} --public
  3. Push: git remote add origin ... && git push -u origin main

Proceed with GitHub creation? (yes / no / review first)
```

#### Step 7: GitHub publish — only on explicit user approval

```bash
cd "{STAGING_PATH}"
gh repo create "{github_org}/{github_repo}" --public --source=. --push --description "{description}"
```

### `/opensource verify PROJECT`

Run the sanitize stage independently against a resolved path (staging dir, then `$HOME/PROJECT`,
then cwd). Regenerate `SANITIZATION_REPORT.md`.

### `/opensource package PROJECT`

Run the package stage independently. Ask for license and description if not already known.

### `/opensource list` / `/opensource status PROJECT`

List `$HOME/opensource-staging/*/` with each project's pipeline progress (presence of
`FORK_REPORT.md`, `SANITIZATION_REPORT.md`, `README.md`), or print the reports for one project.

## Staging Layout

```
$HOME/opensource-staging/
  my-project/
    FORK_REPORT.md
    SANITIZATION_REPORT.md
    README.md
    setup.sh
    LICENSE
    CONTRIBUTING.md
    .env.example
    ...                      # sanitized project files
```

## Anti-Patterns

- Never push to GitHub without explicit user approval
- Never skip the sanitize stage — it is the safety gate, not an optional step
- Never proceed after a sanitizer FAIL without fixing all critical findings
- Never leave `.env`, `*.pem`, or `credentials.json` in the staging directory
- Never assume a fresh `git init` is unnecessary just because the user didn't mention history — ask

## Best Practices

- Run the full pipeline (fork → sanitize → package) for every new public release, not just the first
- The staging directory persists until explicitly cleaned up — use it for review before pushing
- Re-run the sanitizer after any manual fix, before publishing
- Parameterize secrets rather than deleting the functionality that needed them — preserve behavior,
  strip only the sensitive value

## Related Skills

- `skills/security/code-safety-scanner`, `skills/security/web-app-security-audit` — secret and
  vulnerability detection patterns the sanitize stage draws on
- `sdlc-meta/santa-method` — the convergence-loop discipline (fix, re-verify, max iterations,
  escalate) this pipeline's sanitize-retry loop follows
- `sdlc-meta/security-scan` — audits a `.claude/` directory's own configuration; run this on the
  staged project too before publishing, since a public repo's `.claude/` config is itself part of
  the attack surface
