# Short paths for scripts users run - 2026-10-24

## Change

A script the user is asked to run is now launched by one line with the shortest path that resolves from where they already are: a package or task command, a project-root-relative `./scripts/<name>.sh`, a bare command on `PATH`, or `~/<name>.sh` for a one-off. Skills-directory, scratch and temp paths are no longer handed to users, and no script may require an output-path argument.

- New always-on rule [`rules/common/user-run-scripts.md`](../../rules/common/user-run-scripts.md), listed in `rules/README.md` and in the `AGENTS.md` read-first table.
- `skills/execution-plan-scripts` gains an anti-pattern and an Authoring Checklist item, so operator commands inside generated plans follow the same rule.
- The Linux-host procedure (installed `sk-*` first, one-off collectors copied to `~/<name>.sh`, default output beside the script, checksum and cleanup line for root scripts) lives in the `linux-skills` engine under `linux-bash-scripting`. This engine links to it and does not copy it.

## Why

A long path wraps in a terminal and picks up stray newlines when copied. In the sibling engine a documented long path had also drifted to a file that no longer exists. Keeping operator commands short and rooted where the user already is removes both failure modes.

## Evidence

| Check | Result |
|---|---|
| `scripts/skill_catalog_guardrails.py --report-only` | Exit 0 after the edit. The report-only skill-size warnings concern other skills; none names a file changed here |
| `scripts/routing_smoke_test.py` | Precision at 3 is 191 of 191, no failures |

## Limits and follow-up

- The rule files in `~/.claude/rules` on a developer machine are installed copies. They are not updated by this change and will not carry the new rule until reinstalled.
- No external standard, vendor claim or version was admitted, so the Digital Research currentness gate had nothing to verify. This is a user-directed convention.
- Existing skills that tell users to run project commands were not audited one by one for path length. Apply the rule when each is next edited.
