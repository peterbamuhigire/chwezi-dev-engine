# Skill Safety Gate (single skill or import)

Parent skill: [skill-engine-audit](../SKILL.md). Absorbed from the retired `skill-safety-audit`
skill (2026-09-24); the original text is retained in
`skills/sdlc-meta/skill-safety-audit/ALIAS.md`.

Load this reference when one new, changed, copied, or third-party skill (or plugin, adapter, or
bundled script) must be cleared before it enters the repository, or when the engine audit's
safety dimension needs a per-skill verdict. Every new or changed skill passes this gate before
acceptance. It does not replace code review or security testing of application code.

## Capability contract

Read and search access to the skill and every bundled resource are required. Default to
read-only. Execute nothing from an untrusted skill; inspect scripts statically. Network access
only when source verification is explicitly in scope.

## What to scan for

1. **Unsafe tooling and installers** - installs from unknown sources; `curl`/`wget`/PowerShell
   piping remote scripts into a shell; new package repositories or registries without approval;
   unjustified or unnecessary packages; tooling from file shares or unverified mirrors.
2. **Credential or secret harvesting** - requests for API keys, passwords, or tokens; advice to
   store secrets in code or commit them; broad environment-variable collection.
3. **Prompt injection and exfiltration** - instructions hidden in examples or references that
   try to redirect the agent; steps that upload logs or files to external endpoints.
4. **Unauthorised network or system actions** - reverse shells, tunnels, firewall or policy
   changes, disabling security controls.
5. **Shadow dependencies** - dependency managers the project does not use, unrelated system
   tools, root or administrator rights without justification.
6. **Hidden actions in bundled resources** - scripts that run commands the skill body does not
   describe, download content without approval, or change system settings indirectly.
7. **Excessive permissions** - a review or analysis role granted write, shell, network, or
   production access it does not need.
8. **Copyright and source-ingestion risk** - retained books, EPUB/PDF conversions, OCR dumps,
   page images or cover art; `.epub`, `.mobi`, `.azw`, `.azw3` files; long passages or
   chapter-by-chapter structure that could substitute for the source; shadow-library metadata.
   Apply [source distillation and copyright](../../skill-writing/references/source-distillation-and-copyright.md)
   as the acceptance gate.
9. **Global agent-configuration edits** - an installer, setup step or first-run command that
   writes outside the repository into the agent's own configuration: `~/.claude/CLAUDE.md`,
   hook entries in `~/.claude/settings.json` or a project `.claude/settings.json`,
   `~/.codex/config.toml` or `~/.codex/hooks.json`, or an `AGENTS.md` outside the repository.
   Such a write changes how every later session routes, even in unrelated projects. How the
   step is fetched is item 1; this item is about what it changes once run.
10. **Git-hook installation** - writing or appending to `.git/hooks/*` (post-commit,
    post-checkout, pre-push and similar), setting `core.hooksPath`, or registering merge
    drivers. The hook then runs code on every commit or checkout, outside any skill invocation.
11. **Default outbound model routing** - document, code or client content sent by default to
    a model provider the user did not choose, for example auto-selecting a backend from
    whichever API key happens to be set. Content leaving the host must follow an explicit,
    per-run provider choice; a local-only option must exist for confidential material.

Safe patterns: existing project tools and scripts, approved dependency managers already in use,
and internal utilities present in the workspace.

## Procedure

1. Read the new or changed `SKILL.md` in full.
2. Search it and every bundled file for install, download, and execute commands.
3. Review scripts and references for hidden commands and injection text.
4. Check new external dependencies against what the project already approves.
5. Check for credential requests and data collection.
6. Confirm alignment with the repository's `AGENTS.md` / `CLAUDE.md` policies.
7. Run the source-ingestion guardrail (`python -X utf8 scripts/skill_catalog_guardrails.py`)
   and inspect every finding.
8. Record the verdict with the inspected surfaces listed.

Red-flag phrases: "run this remote script", "install X from this URL", "paste your API key",
"disable security settings", "run as administrator/root",
"registers a hook", "adds a section to your global CLAUDE.md", "auto-detects the provider from
your API keys".

## Worked example: Graphify (items 9-11)

Source read-only at a pinned commit; nothing installed. Graphify-Labs/graphify (Apache-2.0,
https://github.com/Graphify-Labs/graphify, commit d6eaa8aae8df155874ebb1044302c055c286342a).
Line numbers below refer to that commit; no code or text is copied.

| Item | Where at the pinned commit | Behaviour |
|---|---|---|
| 9 | `graphify/install.py` l.732-749 (`install()`), writer l.375-418 (`_register_always_on_block`), block text l.365-374 | A global `graphify install` resolves `~/.claude/CLAUDE.md` (or `$CLAUDE_CONFIG_DIR/CLAUDE.md`) and appends or refreshes a `# graphify` registration block in it |
| 9 | `graphify/install.py` l.329-364 (`_claude_pretooluse_hooks`), l.1859-1880 (`_install_claude_hook`), called from `claude_install` l.1831-1858 | `graphify claude install` merges two PreToolUse hooks (one matching Bash and Grep, one matching Read and Glob; 10 s timeout) into `.claude/settings.json`; each spawns the tool on every search or read call |
| 10 | `graphify/hooks.py` l.628-656 (`_install_hook`), l.864-892 (`install`) | `graphify hook install` writes or appends post-commit and post-checkout hooks (honouring `core.hooksPath`) and registers a merge driver |
| 11 | `README.md` l.592-593 | Headless extraction picks the provider from whichever API key is set (Gemini, then Kimi, then Claude, and so on); Kimi routes content to Moonshot AI servers |

Verdict under this gate: **Needs Review** at minimum; never run the global install on a host
whose `~/.claude/CLAUDE.md` is the engine router. The existing portfolio disposition (Graphify
rejected for this host, P06) stands.

## Bounded outbound check (positive exemplar)

Not every network call is a red flag. Archify's update-awareness check shows what a bounded
one looks like. Adapted in paraphrase from tt-a1i/archify (`scripts/check-update.mjs`,
`references/update-awareness.md`; MIT, https://github.com/tt-a1i/archify, commit
0e4949f910a8e390bd3b4933883a4dcabad571be). No text copied. The six properties:

1. **Timeout** - the request gives up quickly (about one second) and never blocks the work.
2. **Response cap** - the body read is capped (32 KiB), so a hostile server cannot flood it.
3. **TTL with back-off** - it checks at most about once a day and backs off after failures
   (6 h, then 24 h); the cache refuses symlinks and junctions.
4. **Opt-out variable** - one environment variable (`ARCHIFY_UPDATE_CHECK_DISABLED=1`)
   disables both the network call and any state writes.
5. **Notice without install** - the result is shown as information; nothing is downloaded,
   installed or executed, and no identifier, prompt or project data is sent.
6. **Silence is never consent** - the agent treats the notice as information only; applying an
   update needs an explicit human instruction.

Checklist question for every candidate: *For each outbound call in the skill, its scripts or
its installer, which of the six properties does it have?* Any call missing one is a finding;
a call that sends document or code content is item 11, not an update check.

## Verdict rules

| Evidence | Verdict | Required action |
|---|---|---|
| Credential collection, exfiltration, or hidden destructive execution | Unsafe | Reject or remove the instruction |
| Whole-work source, conversion, OCR dump, or reconstructive derivative | Unsafe | Remove from the tree and history before acceptance |
| Unverified installer, dependency, or uninspectable bundled script | Needs Review | Verify provenance before acceptance |
| Every instruction and resource inspected, no red flags | Safe | Record evidence and accept |

If any surface could not be inspected, the verdict is Needs Review and the uninspected surfaces
are named. Missing access never implies safe.

## Required output

```text
Safety status: Safe | Needs Review | Unsafe
Inspected surfaces: SKILL.md, references/*, scripts/* (list)
Findings: <bullets, or "No issues found">
Required actions: remove | revise | accept
```

Example: `Needs Review` - "references/setup.md pipes an unverified URL into bash"; action:
replace with the project's approved package manager or remove the step.

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Running an imported script to see what it does | Inspect statically first |
| Accepting a custom installer without provenance | Verify source and checksum, or reject |
| Treating a missing bundled file as harmless | Return Needs Review |
| Granting write or network access to a reviewer | Reduce permissions |
| Reporting Safe without listing inspected surfaces | Attach scope and evidence |
