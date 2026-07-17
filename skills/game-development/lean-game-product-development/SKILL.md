---
name: lean-game-product-development
description: Use when converting a game idea, mechanic, feature, vertical slice, production milestone, or live change into falsifiable hypotheses, prototypes, measurements, learning and go/narrow/pivot/stop decisions; use game-development-orchestration for the full programme and game-testing-polish for release QA.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---

# Lean Game Product Development

Reduce game risk through the smallest playable evidence that can change a decision. Preserve delight and production quality while refusing feature inventory as a substitute for learning.

## Prerequisites

Load `game-development-orchestration`, the product thesis, current risk/assumption register, `anti-ai-slop`, and applicable cultural/research governance.

<!-- dual-compat-start -->
## Use When

- Framing a concept, mechanic prototype, minimum viable/lovable game, vertical slice, pre-production gate or live experiment.
- Deciding what to build first when fun, comprehension, cultural safety, feasibility, cost or demand is uncertain.
- Creating an inception, hypothesis backlog, experiment card, evidence review or pivot/stop decision.

## Do Not Use When

- The work is routine implementation against an approved, low-risk specification; use the owning engineering skill.
- The request is final release QA; use `game-testing-polish`.
- Metrics or market claims would require unverified current evidence; use the Digital Research Skills Engine first.

## Inputs

| Artefact | Produced by | Required? | Why |
|---|---|---:|---|
| Player promise, creative pillars and non-goals | product/game direction | yes | Protects identity while scope changes |
| Risk and assumption register | `game-development-orchestration` | yes | Orders experiments by decision value |
| Constraints and target-player/device context | project discovery | yes | Prevents irrelevant evidence |
| Existing build and test evidence | implementation/QA | conditional | Avoids repeating answered questions |

## Workflow

1. Run a bounded inception: align the player, problem, promise, constraints, success, non-goals, risks and decision owners.
2. Convert assumptions into falsifiable statements with an observable signal, threshold, cohort/context, time box and decision consequence.
3. Rank by uncertainty multiplied by consequence and cost of being wrong; test the highest product-killing risk first.
4. Choose the cheapest valid evidence form: paper flow, rules spreadsheet, greybox, isolated mechanic, art/audio specimen, technical spike, concierge test, playable prototype or representative slice.
5. Prespecify the method, instrumentation, sample, exclusions and analysis before viewing results. Separate player value, usability, delight, technical feasibility, cultural safety and commercial evidence.
6. Build a thin complete loop with production-quality only where the hypothesis depends on it. Keep CI, automated rule tests and a playable mainline from the first code-bearing experiment.
7. Review evidence, contradictions and cost. Decide `go`, `narrow`, `pivot`, `repeat` or `stop`; update the assumption, decision and knowledge registers.
8. Consolidate what was learned into requirements, tests, reusable assets and production estimates before expanding content.

For educational claims, specify age/cohort, construct, comparator, measure, duration and transfer boundary; engagement is not a learning proxy. For advertising, prototype the least intrusive plausible placement and test expectation, decline, interruption, accidental taps, fairness, no-fill/failure, wellbeing and trust before revenue optimisation. A rewarded ad is not voluntary when progression or recovery makes declining punitive.

## Quality Standards

- Make every experiment answer a decision; activity, downloads and compliments are not evidence by themselves.
- Preserve a minimum lovable core: a rough build may still need representative feedback, readability, audio or art if the tested experience depends on them.
- Change one dominant variable where practical and keep immutable build/data identifiers.
- Segment observed behaviour from interview opinion and team interpretation.
- Do not optimise retention by pressure, loss aversion or monetised rescue; pair engagement measures with wellbeing and exit measures.

## Decision Rules

| Risk | Cheapest credible evidence | Advance when |
|---|---|---|
| Core verb may not be enjoyable | interactive greybox with target players | prespecified comprehension and voluntary-replay gate passes |
| Visual premise may not read on mobile | representative camera/art specimen on device panel | protected cues and performance gate pass together |
| System may be technically infeasible | isolated spike plus profiler/test harness | worst-case path fits provisional budget with known margin |
| Content/cultural premise may cause harm | research, consultation and low-cost representation review | disposition permits bounded prototype |
| Production pipeline may not scale | vertical slice with representative disciplines | throughput, rework, cost and quality evidence support expansion |
| Ad model may damage play or trust | instrumented placement prototype with decline/no-fill/kill-switch paths | all safety/privacy/access/trust gates pass before commercial interpretation |
| Educational outcome may be unsupported | bounded learning study reviewed by accountable specialist | prespecified construct measure supports only the stated population and transfer limit |

## Capability Contract

Read/search access to project context and evidence is required. Editing and execution are allowed only within the authorised experiment scope. Network research follows the external evidence engine. Without representative participants/devices or instrumentation, mark results provisional and do not issue a production go decision.

## Degraded Mode

If the decision owner, falsifiable threshold or consequence is missing, stop the build request and return an experiment brief with those gaps. If evidence is contaminated or the method changed after results, quarantine it and repeat or narrow the claim.

## Anti-Patterns

- Calling a feature list an MVP. Fix: name the decision and smallest complete evidence loop.
- Polishing every discipline before the fun question is answered. Fix: spend fidelity only where the hypothesis needs it.
- Testing many mechanics in one build. Fix: isolate the dominant uncertainty or define attribution limits.
- Choosing a flattering cohort. Fix: recruit the intended player and document exclusions.
- Changing thresholds after seeing results. Fix: prespecify or log the change and rerun.
- Treating analytics as player consent. Fix: use data-minimised, approved collection and a telemetry-free path.
- Expanding content before consolidating learning. Fix: update requirements, tests, estimates and reusable pipelines first.

## Outputs

| Artefact | Consumed by | Acceptance condition |
|---|---|---|
| Lean inception and hypothesis backlog | production leadership | Owners, risks, thresholds and decisions are explicit |
| Experiment cards and evidence packs | game/engineering/QA owners | Method, build, cohort/context, observations and limitations are reproducible |
| Gate decision and knowledge update | `game-development-orchestration` | Go/narrow/pivot/repeat/stop follows the prespecified rule or logs an exception |
| Updated requirements/tests/estimates | downstream production skills | Learning is converted into controlled delivery artefacts |

## References

- [Hypothesis and prototype loop](references/hypothesis-prototype-loop.md)
- [Game experiment and gate templates](references/game-experiment-gate-templates.md)
<!-- dual-compat-end -->

## Read Next

Use `mobile-game-design` for the player loop, the owning engine/system skills for implementation, and `game-testing-polish` for formal playtest and milestone evidence.
