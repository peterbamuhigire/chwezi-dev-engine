---
name: kaizen-improvement-system
description: Use when auditing or improving this engineering engine or any website, app, AI system, SaaS, database, DevOps, mobile, desktop, or game product it produces.
---

# Kaizen Improvement System
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com.

## Use when

- Auditing the engineering catalogue or a product made with it.
- Turning defects, incidents, user feedback, playtest evidence, or new books into a tested improvement.
- Planning a quarterly engine review or a product release improvement cycle.

## Do not use when

- A single skill safety review is the only task; use `skill-safety-audit`.
- A current external claim is needed without first routing through Digital Research Skills Engine source evaluation and verification.

## Required inputs

| Input | Required | Purpose |
|---|---:|---|
| Engine/product path and intended output types | Yes | Sets the audit scope |
| Evidence, tests, user feedback, and current references | Yes | Prevents opinion-only scoring |
| Target and constraints | Yes | Defines the 95/100 improvement plan |

## Workflow

1. Read `docs/continuous-improvement/kaizen-adoption-2026-08.md` and the portfolio standard at `C:\wamp64\www\digital-research-engine\docs\continuous-improvement\portfolio-kaizen-standard-2026-08.md`.
2. Inventory routes, active skills, references, validators, output types, and known failure evidence before reading deeply.
3. Score every applicable dimension with named evidence. Publish `min(raw score, 65)`; keep raw scores visible and record blockers.
4. For a product, audit requirements, architecture/code or document correctness, security/privacy, accessibility, reliability, performance, user value, deployment/handoff, and rollback evidence as applicable.
5. Build a P0/P1/P2 plan to 95/100. Each action names the exact skill/reference/fixture/test to change, owner, measure, acceptance evidence, and rollback.
6. Run one small reversible experiment. Check it with the relevant engineering tests, anti-slop gate, evidence pack, and independent review.
7. Standardise successful learning in a skill, reference, template, fixture, router, or release gate; record the next review date.

## Outputs

- capped engine or product scorecard;
- evidence and blocker register;
- 95/100 improvement plan;
- experiment result and standardisation record;
- re-audit date and cross-engine handoffs.

## Quality standards

No 70+ score without extraordinary proof. No claim of production readiness without executable or rendered evidence. Product findings must distinguish defects, risks, assumptions, and unassessed areas. Current platform, security, AI, legal, or standards claims require Digital Research verification.

## Mandatory 65-to-95 gate

The first pass is an initial analysis: calculate raw findings, publish only
`min(raw_score, 65)`, and keep blockers and unassessed dimensions visible. Freeze
that baseline before improvement. Then target 95/100 through one reversible change
at a time, with root cause, exact skill/reference/fixture/test, owner, measure,
guardrails, stop/rollback rule, acceptance evidence, standardisation decision, and
re-audit date. This applies at two levels: the skills engine and each product it
produces.

## Anti-patterns

- Adding skills without proving a routing gap. Fix: inventory first.
- Calling a feature “AI-ready” without model/system/input/output controls. Fix: require evals, limits, and fallback paths.
- Treating a green unit test as product proof. Fix: add user, failure-path, security, and handoff evidence.
- Closing an action when prose changed only. Fix: require named acceptance evidence.
- Keeping lessons in chat. Fix: standardise them in the owning skill or reference.

## References

- [Local adoption plan](../../../docs/continuous-improvement/kaizen-adoption-2026-08.md)
- [Portfolio standard](C:/wamp64/www/digital-research-engine/docs/continuous-improvement/portfolio-kaizen-standard-2026-08.md)
- `skills/sdlc-meta/skill-engine-audit/`
- `skills/sdlc-meta/skill-safety-audit/`
