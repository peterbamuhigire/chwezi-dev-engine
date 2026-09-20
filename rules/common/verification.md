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

*Full testing-strategy decision framework (unit / integration / contract / e2e /
regression / risk-based):* `sdlc-meta/advanced-testing-strategy`.
