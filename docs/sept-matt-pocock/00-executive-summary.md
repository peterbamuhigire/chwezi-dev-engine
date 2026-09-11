# Executive Summary

## Verdict

The Matt Pocock repository is a compact engineering-workflow system, not a deep technical doctrine
library. Its 25 promoted skills create a coherent path from an unclear idea to a reviewed change:

```text
setup -> grill -> domain language and decisions -> spec -> tracer-bullet tickets
      -> implement with TDD -> two-axis review -> handoff
```

Side routes handle hard bugs, architecture deepening, prototypes, large decision maps, issue
triage, primary-source research, and manual setup wizards. The system is memorable because each
route has a leading concept: frontier, fog, tracer bullet, tight loop, seam, depth, and handoff.

Chwezi should adopt this process vocabulary and its routing mechanics, while retaining Chwezi's
stronger safeguards. The source repository does not meet the Chwezi skill contract: the local
compliance scanner found zero of 37 skills fully conformant because it lacks Chwezi portability,
input, output, decision, capability, degraded-mode, and evidence sections. This is a schema and
governance difference, not proof that the source workflows are ineffective.

## What the source does better

1. **Invocation is designed, not accidental.** Human-only orchestrators are explicitly separated
   from model-invoked disciplines. Every skill has matched Claude and Codex invocation metadata.
2. **Questions follow dependency order.** `grilling` maps decisions as a tree and asks only the
   current frontier. Facts are researched; decisions stay with the human.
3. **Domain language persists.** `CONTEXT.md` and ADRs are created lazily as terms and decisions
   become load-bearing, then consumed by later planning, coding, review, and triage.
4. **Work is sliced as a graph.** `to-tickets` creates complete tracer bullets with explicit
   blocking edges; wide refactors use expand-contract rather than forced vertical slices.
5. **Debugging starts with evidence.** `diagnosing-bugs` forbids theorising until one red-capable,
   deterministic, fast command reproduces the exact symptom.
6. **Architecture has a compact vocabulary.** Deep modules, interfaces, seams, adapters, leverage,
   locality, and the deletion test make refactoring discussions sharper.
7. **Review keeps independent questions independent.** Code standards and spec fidelity run as
   separate axes so strength in one cannot mask failure in the other.
8. **Skill maintenance has a product model.** Promoted, miscellaneous, in-progress, and deprecated
   buckets control what ships. Plugin, docs, router, and adapter surfaces are synchronised.

## What Chwezi already does better

- 179 skills across AI, SaaS, architecture, data, DevOps, mobile, games, languages, security, and
  business delivery, compared with 37 mostly process-oriented source skills.
- Required inputs, outputs, capabilities, permission boundaries, degraded modes, stop conditions,
  release evidence, rollback, and `NOT ASSESSED` semantics.
- Currentness routing to the Digital Research Engine and additive finance/design doctrine.
- Catalogue and reference guardrails, routing fixtures, source-ingestion checks, control-plane
  validation, and a 72-pass local test suite.
- Portfolio craft and anti-slop gates that distinguish structural, behavioural, rendered, system,
  production, and handoff evidence.

## The five immediate gaps

| Gap | Evidence | Consequence |
| --- | --- | --- |
| No dedicated systematic bug-diagnosis route | No active `diagnosing-bugs` equivalent found | Agents can jump from symptom to plausible fix without a red-capable loop |
| No reusable frontier/grilling primitive | Searches for `grill`, `design tree`, and `frontier` found no active equivalent | Interviews can be linear, repetitive, or dependency-blind |
| No active codebase-deepening vocabulary | No `deep module`, `deletion test`, or `design it twice` route | Architecture reviews risk broad advice without an interface-level decision method |
| Work planning lacks explicit dependency graphs | No `tracer bullet` or `blocking edges` language in active skills | Plans can be vertical in prose but cannot expose safe parallel frontiers |
| Skill authoring under-specifies attention mechanics | `skill-writing` mentions progressive disclosure but not pointer quality, context/cognitive load, leading words, or premature completion | Correct content can still be loaded late, over-loaded, or ignored |

## Baseline scorecard

This score is limited to the comparison objective. Scores above 70 are withheld without applied
task evaluations.

| Dimension | Weight | Score | Evidence-backed deficiency |
| --- | ---: | ---: | --- |
| Workflow coverage and output readiness | 20% | 58 | Strong delivery gates, but missing dedicated diagnosis, work-graph, and domain-language flows |
| Skill depth and applied examples | 15% | 55 | Deep references exist unevenly; worked examples remain the weakest broad dimension |
| Invocation and routing | 15% | 61 | Routing is 91% top-1 and 100% top-3, but explicit versus implicit invocation is not governed portfolio-wide |
| Skill authoring and context economy | 10% | 54 | Progressive disclosure exists; pointer quality and attention-budget mechanics are thin |
| Evidence and validation | 15% | 60 | Structural checks pass, but 66 skills lack `Evidence Produced` and 3 tests are skipped |
| Safety, permissions, and recovery | 10% | 64 | Strong contracts, but 26 skills still miss at least one portable-contract requirement |
| Standards currency and provenance | 10% | 49 | Currentness framework exists, but some source-register reviews are overdue and installed checks are skipped |
| Cross-engine composition | 5% | 63 | Ownership routing and assembled-runtime budget pass; live cross-engine task proof is incomplete |
| **Weighted raw score** | **100%** | **58** | Rounded from the weighted comparison baseline |

Published baseline: `min(58, 65) = 58`.

## Expected outcome after the recommended waves

The first implementation wave should target 64, not 95. A 95 score remains a goal until real
projects show faster diagnosis, fewer routing errors, smaller context loads, better spec fidelity,
and reliable handoffs. Proposed targets are:

- Wave 1: 64, after P0 references, diagnosis route, current contract repairs, and fixtures.
- Wave 2: 69, after domain modelling, work graphs, review split, and applied examples.
- Wave 3 target: 75+, only after cross-engine task evaluations and production evidence.
- Long-term target: 95, explicitly unachieved.
