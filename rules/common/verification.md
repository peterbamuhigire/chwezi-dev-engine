# Verification — Common Rules

> Distilled from: `sdlc-meta/advanced-testing-strategy`,
> `sdlc-meta/implementation-status-auditor`, and the practice actually followed
> while building this engine's own installer and hooks (see
> `kaizen-engines/ECC-audit-2026-09-20/`, where three real bugs were only found
> because the installer and both hooks were run, not just read).

## A claim of "done" requires evidence produced by running something

"The installer works" is not evidence. "`node hooks/test-destructive-bash-gate.js`
→ 12/12 passed" is evidence. Before stating that code, a script, or a hook is
correct, run it — against a case designed to fail if the logic is wrong, not only
a case designed to succeed.

This is not a hypothetical: the manifest generator this engine's installer relies
on silently dropped 17 of 111 real skills in `proposal-skills` because it stopped
recursing at the first `SKILL.md` per branch — a bug invisible from reading the
code, caught only by counting installed files against the source tree and finding
they disagreed.

## Cross-check generated output against ground truth, not against itself

A generator's own count agreeing with its own manifest proves nothing — both
came from the same logic. Verify against an independent count: `find` the raw
filesystem, diff two independently-computed lists, or run the consumer (the
installer) against the producer (the manifest) and check they agree.

## State what has and has not been tested

"Verified end-to-end" and "written but not run" are different claims and must be
labelled as such. In particular: static portability review (no CRLF, no GNU-only
flags, cross-platform APIs only) is evidence that code is *unlikely* to break on
an untested platform, not evidence that it *was tested* there. Say which one you
mean.

## Claim, required evidence, not sufficient

| Claim | Required evidence | Not sufficient |
|---|---|---|
| Tests pass | The exact command and its output, run after the last edit | "Should pass"; a run from before the change |
| Build succeeds | The build command's exit status and output | The editor showing no red marks |
| Bug fixed | The original failing reproduction, now passing | A new test written after the fix that never failed |
| Migration safe | A dry run on a copy of the data and a written rollback path | Reading the migration file |
| Hook works | The hook's own test file run, including a case built to fail | Running the hook once on a happy path |
| Delegated agent reported success | The diff read by you and the delegated agent's check rerun by you | The agent's summary |
| Document rendered | The output file opened, or its structure extracted and checked | The generator exiting with status 0 |
| Requirement met | The acceptance check named in the plan, run and recorded | The code "looking complete" |

Banned success phrasing, unless the same sentence cites the evidence above: "should pass", "looks correct", "probably works", "seems fine". Write what was run and what it returned instead. A check that could not run is `NOT_ASSESSED`, never a pass.

(Claim table adapted from obra/superpowers, MIT, https://github.com/obra/superpowers, commit 8ca22dba9a94f28898bbce59f2537ff4d87c747d.)

*Full testing-strategy decision framework (unit / integration / contract / e2e /
regression / risk-based):* `sdlc-meta/advanced-testing-strategy`.
