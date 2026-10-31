# Improvement backlog (pass 2)

Date: 2026-10-31. Scope: this repository only. Owner for every item: Chwezi Dev Engine.
Due dates are review points, not claims that work is scheduled. Target contribution is a
judgement of how far the named dimension can move, towards the 95/100 improvement target;
the capped audit score stays at or below 65.

Selection rule: every critical defect and every still-open P0 from the last audit must be in
the cycle (none critical were found; D-15 is the open P0 carried from pass 1 as D09). At most
ten items are selected. Structural or high-risk work is moved to
[06-next-cycle.md](06-next-cycle.md).

## Selected for this cycle

| ID / priority | Gap and root cause (5 Whys, condensed) | Exact change | Hypothesis and acceptance evidence | Risk and rollback | Target |
|---|---|---|---|---|---|
| S01 / P0 | D-15, D-16. Source records were created per snapshot with a 30-day review window, and nothing in this repository fails when one expires, so 27 lapsed unnoticed. Root cause: tooling (no repository-owned check) plus process (no refresh step). | Re-verify each overdue source against its primary page on 2026-10-31; add a fresh dated record where the claim is confirmed; keep old snapshots as history outside `sources`; mark unverifiable ones `NOT_ASSESSED`; update `ai-platforms.md` rows and moved URLs; add `scripts/check_source_register.py`, its tests and a CI step. | Overdue count falls from 27 to the number honestly left `NOT_ASSESSED`, and the checker fails when a record lapses. Evidence: checker output, Digital Research validator exit code, unit tests. | Renewing without reading the page would create false currency; each renewal cites what the page showed. Revert the commit; old records stay in history. | Standards currency +15, hygiene +3 |
| S02 / P1 | D-10. Two validators hard-code one Windows layout and old repository names. Root cause: tooling written for one machine, with no shared resolver. | New `scripts/engine_roots.py` (repeatable roots, known repository aliases, per-engine environment override); both validators use it; remove the hard-coded drive paths; tests. | Control-plane validator exits 0 on this machine with the two real parent folders and no per-engine flags; approval validator exits 0 likewise; tests cover aliases, roots and failure. | Behaviour change for the CI registry-only form must be nil: verified by running it unchanged. Revert the commit. | Production and handoff +8, hygiene +2 |
| S03 / P1 | D-02, D-03. The router groups skills by domain; a review crosses four domains and nobody owns the join. Root cause: routing gap plus a name introduced in an exercise without checking the owning skill. | Add a review row to the root router and routing index; add a domain-owned checks section to the review-gate reference linking tenant, SQL, ledger and output checks; align the exercise name with the owning skill; add routing fixtures. | A fresh reader following only the router reaches all four checks; fixtures rank the review skill in the top three; contract gate and guardrails stay clean. | Prose can drift from owning skills; the links are checked by the guardrail. Revert the commit. | Doctrine +5, routing +4, safety +3 |
| S04 / P1 | D-11, D-12, D-14. No check scans for machine-specific paths, so each cycle adds some. Root cause: tooling gap. | Add a machine-path check to the catalogue guardrails over router files and active skill content (explicit allowance for teaching examples); replace sibling-engine paths with per-device resolution wording; remove leaked tool markup from eight references; replace pass-1 temporary-path citations and home paths with a note. | Guardrail reports zero sibling-engine machine paths and fails on a planted one (test). | Reference-only prose edit plus a new gate; the allow-list could hide a real path, so each entry needs a reason. Revert the commit. | Hygiene +10, doctrine +3 |
| S05 / P2 | D-19. Fixture coverage is measured by hand each cycle. Root cause: tooling gap. | Add a `--coverage` report and an optional floor to `routing_smoke_test.py`; add positive fixtures and owned negatives for the skills touched this cycle and for a bounded set with none. | Zero-positive count falls below 43 and the metric is reproducible by command; p@1 does not fall. | A weak fixture can pin a bad route; lint stays on and every fixture is checked. Revert the commit. | Routing +8 |
| S06 / P2 | D-17. Skill normalisation appended contract blocks to existing sections. Root cause: process (the gate checks presence only). | Add a duplicate-heading check with a recorded baseline that may only shrink; merge the duplicates in a bounded batch of skills. | New duplicates fail the gate; baseline shrinks by the batch; contract gate stays at 0 errors. | Merging sections can lose content; each merge keeps every line and only changes headings. Revert the commit. | Skill depth +6, hygiene +3 |
| S07 / P2 | D-18. The link check covers only `references/` and `templates/` links from `SKILL.md`. Root cause: tooling gap. | Extend link checking to all Markdown under active skills with a baseline that may only shrink; repair a bounded batch. | New broken links fail the gate; baseline shrinks. | Mechanical link repair can point at the wrong file; each repair is checked to exist and read for sense. Revert the commit. | Hygiene +4 |
| S08 / P2 | D-01, D-05, D-09 are not fixed this cycle (they need a build, a device or a database). Root cause: proof boundary. | Add a "Known gaps" section to the slice README naming each, so the slice does not claim more than it does. | A reader sees pagination, money display, error format and evidence-pack gaps before copying. | Documentation only. Revert the commit. | Output readiness +3 |

## Not selected (carried to the next cycle, with reason)

| ID / priority | Item | Reason |
|---|---|---|
| P1 | D-01 pagination, D-04 RFC 9457 errors and security schemes, D-05 money display, D-06 wildcard escaping, D-07 rollback, D-08 accessibility semantics | Changing five layers together is a structural change to a teaching slice whose Next.js, Compose and MySQL layers cannot be rebuilt on this host. Do it in one slice with a build available. |
| P1 | D-13 tracked user-local settings file | User-authored content and a history question; needs Peter's decision. |
| P2 | Next.js advisory (due 2026-11-03), real Next build, MySQL run, Compose build, independent review, archive count | Date-gated or blocked by the host rules. |
| P2 | Worked examples for the 25 game-development skills | Content that cannot be verified here; a hollow example would be padding. |

## Root-cause note (S01, inference)

1. Why did 27 records lapse? Review dates passed with no action.
2. Why no action? No script in this repository reads the register; the only validator is in
   another checkout and is not in this repository's CI.
3. Why was the register built that way? Records were added per snapshot to preserve provenance
   and the checker lived with the research engine.
4. Why did that matter now? The router names the AI-platform register as a first stop, so stale
   rows are read as current.
5. Why is the fix a repository-owned check plus a re-verification? Re-verification clears the
   present debt; the check stops it recurring.

## Target ratchet

The 95/100 target remains the plan. The [final report](05-final-report.md) records the
capped result and what is still open.
