# User-Run Scripts - Common Rules

> Distilled from: `skills/execution-plan-scripts` (its Path-Resolution Rule and
> Operator-Action Surfacing already keep environment-specific paths out of what an
> operator is told to run), `docs/ai-prompting/domain-prompt-compilation-contract.md`
> (a ready-to-paste handoff must be runnable as written), and the sibling rule in
> the `linux-skills` engine, `rules/common/core.md`. Added 2026-10-24 on Peter's
> instruction. Kept separate from `security.md` and `verification.md` because it
> governs how a command is handed over, not what the command does.

## A script handed to a user starts with the shortest possible command

A script the user is asked to run is launched by one line with the shortest path
that resolves from where they already are: a package or task command
(`npm run audit`, `composer audit`, `make audit`), a project-root-relative
`./scripts/<name>.sh`, a bare command on `PATH`, or `~/<name>.sh` for a one-off.
Never hand over a path through a skills directory, a scratch or temp directory,
or any location that exists for one session only, and never require an
output-path argument; default the output next to the script. A script that
writes its results to a file prints one line to the terminal before and after,
naming the file, because silence reads as failure. Long paths wrap in terminals
and pick up stray newlines when copied. Commands run by a machine (CI,
cron, cloud-init) are exempt.

For a script that runs as root or changes state, also give the user a short
checksum of the validated file, so they can confirm it was not altered after
review, and the one-line command that removes the script and its output
afterwards.

*Full procedure for Linux hosts:* the `linux-skills` engine, skill
`linux-bash-scripting`, section "Handing a script to a user".
*Authoring plans and prompts that contain operator commands:*
`skills/execution-plan-scripts`.
