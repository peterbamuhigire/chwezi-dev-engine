---
name: game-development-orchestration
description: Use when initiating, replanning, or governing a complete game project from concept through vertical slice, production, certification, and post-launch; routes specialist game skills and prevents premature full-production commitment.
metadata:
  portable: true
  compatible_with:
    - claude-code
    - codex
---

# Game Development Orchestration

Coordinate a game as an evidence-gated product programme. Convert the creative premise into a playable risk-reduction sequence, then route each discipline to the narrowest specialist skill.

## Prerequisites

Load `world-class-engineering`, `anti-ai-slop`, `lean-game-product-development`, and the project's cultural/research governance before making irreversible product decisions.

<!-- dual-compat-start -->
## Use When

- Starting a mobile, PC, console, web, 2D, or 3D game project.
- Converting research or a narrative premise into a game concept and production plan.
- Defining an MVP, prototype, vertical slice, milestone plan, staffing model, or backlog.
- Auditing whether a project is ready to move from discovery to production.
- Coordinating design, engineering, art, audio, QA, release, and live operations.

## Do Not Use When

- A bounded implementation task already has an approved design; use the relevant engine or discipline skill.
- The request is only for generic mobile application development; use the Android, iOS, or mobile-cross family.
- The game depends on unverified living-culture, historical, legal, market, or platform claims; research and verify those claims before locking content.

## Required Inputs

| Input | Required | If absent |
|---|---:|---|
| Player, platform, business and cultural context | yes | Run discovery and record assumptions |
| Creative pillars and non-goals | yes | Draft and obtain owner confirmation |
| Target device classes and connectivity posture | yes for mobile | Commission a device study |
| Team, schedule, cash and rights constraints | yes | Keep estimates conditional |
| Existing prototype, repository and evidence | conditional | Inspect before planning changes |

## Workflow

1. Load `world-class-engineering`, `anti-ai-slop`, and `ai-slop-audit`.
2. For culturally grounded, historical, legal, market, or current-platform work, use the Digital Research Skills Engine and preserve its source and claim trail.
3. Frame the player promise, core interaction, target platform, age/education posture, business model, safety/wellbeing boundaries, and definition of success.
4. Create the concept brief, design pillars, fact/fiction/permission ledger, high-risk assumption register, evidence-class map, and prototype questions.
5. Slice work into paper test, technical spike, playable prototype, vertical slice, pre-production, production, alpha, beta, release candidate, launch, and support.
6. Route hypotheses, prototypes and learning gates to `lean-game-product-development`; do not use a feature list as proof of viability.
7. Route mechanics to `mobile-game-design` and `gameplay-systems-architecture`; route interactive narrative, agent AI/navigation and Blender production to their specialist skills; route mathematical contracts to `game-math-and-simulation`; route technology to one approved engine after the bake-off gate.
8. Route graphics implementation to `real-time-game-graphics`; route player-facing HUD, art direction, game feel and children's/educational experience to the game route in `design-system-skills`. Route lifecycle requirements and traceability to `srs-skills`; do not duplicate either engine's craft.
9. If advertising is a candidate, apply the non-intrusive-ad gate before vendor or placement selection: clearly label it, require explicit choice or a predictable non-critical break, cap and pace it, preserve core play and exit/save/recovery, and define a no-ads/degraded path. Apply stricter child, privacy, store and owner rules.
10. Hold a gate at every phase. Advance only when the named evidence exists; otherwise narrow scope or run another experiment.
11. Close each milestone with the repository Delivery Definition of Done evidence pack.

## Quality Standards

- Prove fun, comprehension, cultural safety, technical feasibility, cost, and market access separately.
- Treat the vertical slice as production-risk evidence, not a miniature content dump.
- Maintain one decision register, one dependency map, one playable build lineage, and one prioritised backlog.
- Make every milestone answer a decision. Do not fund activity without a learning or delivery outcome.
- Preserve version-sensitive engine and store facts as dated, verified constraints.
- Keep documentation, prototype, build, device, observed-player and accountable-expert evidence separate; never promote one class into another.
- Keep learning, engagement, retention, wellbeing and commercial measures separate. A retention pass fails when regret, harmful spend, inability to stop, sleep disruption, child-safety incidents, refunds or trust materially worsen.

## Anti-Patterns

- Starting full production from a narrative document. Fix: prototype the highest-risk interaction first.
- Calling a greybox a vertical slice. Fix: require representative art, audio, controls, pipeline, performance, and release evidence.
- Choosing an engine by preference. Fix: run the same representative scene on target devices.
- Treating research as lore decoration. Fix: keep claim, creative adaptation, consultation, and permission ledgers.
- Planning every feature as mandatory. Fix: use must/should/could/will-not and define the smallest complete player promise.
- Hiding uncertainty inside precise schedules. Fix: use ranges, confidence, dependencies, and contingency.
- Letting discipline plans diverge. Fix: reconcile them at milestone and change-control reviews.
- Calling a platform-compliant ad non-intrusive. Fix: also test expectation, interruption, accidental-tap risk, decline/recovery, frequency, wellbeing and trust in the actual game.

## Outputs

| Artefact | Acceptance condition |
|---|---|
| Game concept and player-promise brief | Names player, action, emotion, platform, differentiation, exclusions |
| Game design document map | Links controlled system specifications rather than one stale monolith |
| Risk and assumption register | Has owner, test, evidence, date, impact, disposition |
| Prototype and vertical-slice plan | Each build answers explicit product, cultural, technical, and commercial questions |
| Production roadmap and backlog | Scope, dependencies, roles, estimates, gates, contingency and exit criteria are visible |
| Decision and release evidence | Another team can reproduce why the project advanced |

## References

- [Project lifecycle and gates](references/project-lifecycle-and-gates.md)
- [Game documentation set](references/game-documentation-set.md)
<!-- dual-compat-end -->

## Decision Rules

| Evidence state | Decision |
|---|---|
| Core player action is not enjoyable or understood | Iterate or stop; do not increase content |
| Art direction works but target-device frame and memory budgets fail | Simplify pipeline and content before staffing up |
| Cultural or rights gate is unresolved | Use a fictional substitute, obtain permission, or remove the content |
| Learning claim lacks an age/construct/measure/comparator | Keep it a hypothesis; obtain educational-method approval and evidence |
| Ad interrupts play, learning, narrative, save, recovery, stopping, or safety | Remove or redesign it; platform minimums do not override the Chwezi gate |
| Vertical slice meets player, pipeline, device, cost, and governance gates | Approve bounded pre-production or production |
| Budget runway cannot cover milestone plus contingency | Reduce scope or fund the gate before committing |

## Read Next

- `mobile-game-design` for interaction, sessions, controls, UX, accessibility, economy, and player testing.
- `lean-game-product-development` for inception, hypotheses, prototypes, learning and gate decisions.
- `game-math-and-simulation` and `real-time-game-graphics` for mathematical and rendering contracts.
- `unity-mobile-game-development`, `godot-mobile-game-development`, or `unreal-game-development` after the engine decision.
- `apple-game-platform-delivery`, `online-multiplayer-and-game-backend`, `game-build-release-engineering`, and `game-security-anti-cheat-and-abuse` for their platform, online, release, and trust boundaries.
- `game-2d-art-animation-and-vfx-pipeline`, `game-3d-asset-pipeline`, `blender-game-asset-production`, `game-narrative-and-interactive-story-design`, `game-ai-behaviour-and-navigation`, `level-world-and-content-production`, `game-data-analytics-and-live-economy`, `game-studio-delivery-and-commercial-operations`, and `game-accessibility-localisation-and-player-safety` when those production lines are in scope.
- `game-testing-polish` and `mobile-game-release-liveops` before any ship claim.
