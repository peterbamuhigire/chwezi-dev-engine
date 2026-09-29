# Bundled-Script Safety

Parent skill: [Skill Writing](../SKILL.md).

Load this reference when a skill ships scripts under `scripts/`, or when you review one that does.

## Invocation

Call bundled scripts through their interpreter, for example `python -X utf8 scripts/quick_validate.py <skill-dir>` or `node scripts/check.mjs`. Never rely on a bare path, a shebang or a file association: packagers can strip executable bits, and Windows hosts do not honour shebangs.

## Quarantine, not delete

Adapted from Egonex-AI/Understand-Anything (MIT, https://github.com/Egonex-AI/Understand-Anything, commit b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0). No text copied.

- A script that removes intermediate files moves them to `.trash-<UTC timestamp>/` inside its work directory and purges only entries older than seven days.
- Check every path variable used in a removal as non-empty and inside the work root before use. An empty variable must stop the script, never widen the target.
- Removing a directory the same process created with `mkdtemp`, or one inside a test fixture's temporary directory, is exempt. Put a comment beside the call that names the exemption.
- A cleanup that runs on production servers is changed only with a test on that platform; until then it is recorded as a waiver.

Existing cleanups across the public engines, with their dispositions, are listed in `chwezi-engine-agents/docs/operations/destructive-cleanup-register.md`. Add a row there when a new script needs a removal that this rule does not cover.
