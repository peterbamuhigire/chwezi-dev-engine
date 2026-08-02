# Claude Code Adapter

Parent: [Coding Agent Optimisation](../SKILL.md)

Load this adapter only after the device inventory. Claude Code settings and
installation behaviour are version-sensitive, so discover the installed CLI
and validate each key against local help or current official documentation.

## Surfaces to inspect

- The global `CLAUDE.md` and project `CLAUDE.md` files.
- Global and project `.claude/settings.json` or `settings.local.json` files.
- `.claude/agents/` role definitions and any project skills they reference.
- The resolved Claude configuration directory and its non-secret metadata.

Do not read API keys, OAuth tokens, credential stores, transcripts, or session
databases. Do not use a credential file as proof that a model or feature is
available.

## Discovery sequence

1. Resolve the configured Claude directory and project root.
2. Run `claude --version` and inspect `claude --help`. Run `claude doctor`
   only when the user authorises diagnostics and the installed help exposes it.
3. Record supported model aliases or identifiers, turn limits, permission
   modes, agent controls, and settings-file locations.
4. Read the existing instruction and settings files while preserving local and
   project precedence. Identify duplicated instructions that cause context
   bloat.
5. Prepare a minimal JSON or Markdown delta and a rollback copy before editing.

## Safe optimisation rules

- Keep durable `CLAUDE.md` guidance short: project rules, routing, safety, and
  links. Move deep procedures into skills or references.
- Use one bounded worker for independent read-heavy work only when the runner
  exposes the required agent control. Reconcile its report in the primary
  thread; do not run dependent decisions in parallel.
- Set a model or turn cap only when the local CLI and user policy support it.
  Prefer a verified alias over a stale full model name.
- Default analysis, review, and planning to read-only or plan permission modes.
  Never treat `--dangerously-skip-permissions` as an optimisation.
- Keep project agents thin: mission, permissions, required context, output
  schema, and a link to the canonical skill. Do not duplicate this full skill
  body in every agent file.
- Do not resume or fork a conversation when the goal is a fresh bounded worker;
  start a new context if the runner can guarantee that behaviour.

## Patch boundaries

Safe candidates are concise instruction routing, explicit agent boundaries,
verified model/turn settings, and read-only permission defaults. Avoid changing
MCP servers, shell paths, authentication, auto-updaters, firewall policy, or
global permission bypasses as part of token optimisation.

If Claude Code is absent, do not install it. Return the missing-runner finding
and the verified installation or support requirement instead.

## Verification

After a patch:

1. Parse each changed JSON settings file and inspect the Markdown diff.
2. Run the CLI help or a harmless version/startup check.
3. Confirm the selected model alias, turn cap, permission mode, and agent path
   are recognised by this installation.
4. Check global-to-project precedence and confirm no secret file was changed.
5. Record restart, new-session, and user-approval requirements.

Restore the timestamped backup if JSON parsing or startup validation fails.
Keep unsupported or unverified settings out of the patch and list them as
follow-up work.
