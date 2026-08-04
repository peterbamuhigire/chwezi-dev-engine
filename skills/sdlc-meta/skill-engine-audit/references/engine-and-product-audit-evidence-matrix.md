<!-- Source basis: XP 2026; Platform Enterprise (early release, chapters 1-2 only); Designing for AI (early release, chapters 1-4 only); Applying the Kaizen in Africa (2018). Operational synthesis, not a source replacement. -->

# Engine and Product Audit Evidence Matrix

Use this matrix after the engine inventory and before scoring. A score is not evidence.
The evidence must show what was inspected, what was missing, and what changed.

| Audit area | Engine evidence | Product evidence | Minimum acceptance proof |
|---|---|---|---|
| Routing and ownership | Router, dependency graph, owner, escalation path | Artefact-to-skill route and accountable reviewer | A new task reaches the correct specialist within three routing probes |
| Value and problem fit | Output types, user/persona, decision the engine supports | Problem statement, target user, non-AI/non-platform alternative | Reviewer can state the user problem and why this output is the smallest useful response |
| Requirements and architecture | Contract, traceability, decision records, uncertainty register | Requirement-to-design-to-test links; failure and recovery paths | Every material requirement has an acceptance oracle and owner |
| Feedback and learning | Retrospective cadence, experiment register, standardisation rule | User, operator, test, telemetry, and incident feedback | One completed experiment has baseline, hypothesis, measure, result, decision, and next action |
| Platform/product health | Internal consumers, cognitive-load risks, maintenance owner, deprecation policy | Onboarding, golden path, service limits, docs, support and usage signals | Platform change is reversible and has consumer impact evidence |
| AI trust and control | Eval, human oversight, consent, escalation, drift and rollback guidance | Model/system/input/output map, uncertainty, correction, undo, audit events | Human can understand, correct, override or safely decline the AI action |
| Game/player quality | Narrative, gameplay, AI, art, accessibility and release handoffs | Playtest cohorts, comprehension, fun/friction, fairness, performance, failed paths | Same slice is tested with a normal, edge, and accessibility scenario |
| Release and operations | Build/release evidence, SLOs, rollback, incident learning | Exact artefact, checksum, rollout, monitoring, rollback rehearsal | Tested artefact is promoted unchanged and a rollback signal is explicit |
| Research and currency | Source register, dates, limitations, current-verification route | Claim provenance and unverified assumptions | Historical/early-release claims are labelled and not used as current standards |

## Scoring and plan rule

Score each applicable row with named evidence and a gap. Report
`min(raw_score, 65)` as the audit score. The remediation plan must name the gap,
root cause, owner, experiment, measure, risk, rollback, and acceptance evidence,
with a target of 95/100. Missing evidence is `not assessed`, never a pass.

## Review sequence

1. Inspect the smallest representative route and product artefact.
2. Test one happy path, one failure path, and one handoff path.
3. Record the defect as a process or system gap, not a person fault.
4. Run one reversible improvement experiment.
5. Standardise only after the affected validator, reviewer, or product measure passes.

## Provenance and limits

The XP 2026 source is an open-access 2026 proceedings volume. Platform Enterprise
and Designing for AI were early releases with unavailable chapters; their available
principles are used here only as design prompts. The matrix is an internal control
and must not be presented as a formal standard or as empirical proof of a book claim.
