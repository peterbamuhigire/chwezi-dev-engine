# Codex Adapter

Parent: [Coding Agent Optimisation](../SKILL.md)

Load this adapter only after the device inventory. Codex changes frequently;
use the installed CLI's help and model discovery as the local source of truth,
then consult the current official Codex documentation when the local surface is
ambiguous. This adapter describes inspection and decision logic, not a model
roster that should be copied between machines.

## Surfaces to inspect

- Global `config.toml` under the resolved Codex home.
- Global `AGENTS.md` under the resolved Codex home and any closer project files.
- `agents/*.toml` role files referenced by the config.
- A user-provided model catalogue, if `model_catalog_json` is configured.
- Project-level `.codex/config.toml` and `.codex/agents/` where present.

Do not read `auth.json`, session databases, history, logs, or other credential
and transcript stores as part of optimisation. Record their existence only if a
diagnostic needs to distinguish configuration from authentication state.

## Discovery sequence

1. Resolve `CODEX_HOME`; on a normal installation fall back to the platform's
   user Codex directory.
2. Run `codex --version` and, when supported, `codex debug models`.
3. Record the advertised model identifiers, reasoning levels, context and
   maximum-context values, effective context percentage, feature flags, and
   multi-agent version. Treat unavailable fields as unknown.
4. Check whether the installed client recognises custom roles, explicit agent
   selection, and fresh-context controls. Do not infer these from a blog post.
5. Parse the existing TOML and inspect the proposed diff before writing.

## Safe optimisation rules

- Select the strongest parent model that the user has authorised and the local
  catalogue actually exposes. Preserve the current model when availability is
  uncertain.
- Select a smaller child model only in a role file that pins it explicitly and
  only when the spawn interface can select that role. Never silently replace a
  parent model with a child model.
- Set context no higher than the selected model's advertised maximum. A custom
  catalogue that claims a larger value than the installed live catalogue is a
  portability risk and must be reported, not copied automatically.
- Keep one worker as the default. Set a larger cap only when device resources,
  usage limits, and independent work justify it.
- Require a complete initial child prompt: bounded task, applicable rules,
  paths, symbols, write set, proof requirements, and output format.
- With a V1 interface, use the documented no-fork option. With a V2 interface,
  use the documented no-history option. If the interface cannot guarantee the
  selected role and fresh context, do not spawn.
- Keep explorers and reviewers read-only. Give workers only their exclusive
  write set. Keep deep roles opt-in and never use them for routine lookups.

## Patch boundaries

Prefer these changes when the local schema supports them:

- global model and reasoning defaults;
- a model-catalogue path with an internally consistent, verified catalogue;
- multi-agent enablement and a device-sized concurrency cap;
- explicit role files with model, reasoning, sandbox, and bounded instructions;
- a short global delegation policy in `AGENTS.md`.

Do not change MCP servers, plugins, project trust, sandbox policy, notification
commands, authentication, or unrelated project settings unless separately
requested. Do not add undocumented keys merely because another Codex build
accepted them.

## Verification

After a patch:

1. Parse the TOML and every referenced role file.
2. Run the CLI help or a harmless startup path to catch schema errors.
3. Run model discovery against the configured catalogue and confirm the parent
   and role models resolve.
4. Confirm every role path is absolute after resolution and every role has a
   name, description, and developer instructions.
5. Inspect the diff for unrelated changes and record that a restart or new
   thread is required when applicable.

Restore the timestamped backup if parsing, startup, model resolution, or role
selection fails. Leave the failed evidence in the handoff rather than claiming
that the optimisation is active.
