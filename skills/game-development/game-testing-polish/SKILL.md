---
name: game-testing-polish
description: Use when planning or executing game QA, playtesting, balance, usability, compatibility, accessibility, localisation, save migration, regression, bug triage, polish prioritisation, alpha, beta, or release-candidate gates.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Testing and Polish
Treat polish as a discipline-level definition of done and testing as a continuous evidence system, not a late bug hunt.

## Prerequisites

Load the build manifest, acceptance criteria, risk register, performance budgets and owning implementation skills.
<!-- dual-compat-start -->
## Use When
- Creating test plans, device matrices, playtests, bug reports, balance experiments, polish backlogs, external QA packs, alpha/beta/RC gates, or release verdicts.
## Do Not Use When
- The request is only to implement a feature; pair with the owning skill and return here for verification.
## Required Inputs
Build ID, acceptance criteria, risks, systems/content map, device/localisation/accessibility matrix, known issues, telemetry, performance budgets and release stage.
## Workflow
1. Build a risk-based test matrix across unit/component, integration, gameplay, UX, save/lifecycle, device, performance, localisation, accessibility, monetisation/ads, privacy/safety, compliance and regression.
2. Automate deterministic rules, schema validation, build smoke and repeatable flows; preserve exploratory and fresh-player testing for human judgement.
3. Run playtests with hypotheses, target cohorts, consent, observed behaviour and non-leading debriefs. Separate comprehension, appeal, learning, culture, wellbeing, ad interruption/trust and commercial questions.
4. Record defects with build/device, preconditions, exact steps, expected/actual, frequency, severity, evidence, owner and retest scope.
5. Tune one data variable per experiment, keep the change log, and retest dependent systems.
6. Rank polish by frequency, visibility, severity, thematic importance, accessibility and cost.
7. Gate alpha, beta and release candidate with explicit entrance/exit criteria and independent verification.
## Quality Standards
- Keep the mainline releasable and identify every test result with an immutable build.
- Use fresh players; developer familiarity is not usability evidence.
- Do not send unstable, untriaged builds to external QA.
- Test install/update, corruption, nearly full storage, offline, permission denial, suspend/resume, localisation expansion and long-session thermal behaviour.
- Identify evidence as documented, prototype-observed, build-executed, device-measured, player-observed or accountable-expert-approved; never imply a stronger class.
- For each ad placement test load, disclosure, input/focus, decline/close, reward, cap/pace, pause/resume, save/recovery/exit, no-fill/offline/SDK failure, child treatment, accessibility and kill switch on real devices.
## Anti-Patterns
- “Feels polished” as acceptance. Fix: discipline-specific criteria and evidence.
- Severity based on developer inconvenience. Fix: player impact, reach and recovery.
- Balance changes without versioned data. Fix: one-variable experiment log.
- Closing bugs without independent retest. Fix: verify exact build and regression area.
- Testing only happy path. Fix: destructive and recovery scenarios.
- Passing an ad because it renders. Fix: test expectation, interruption, accidental tap, coercion, regret and trust with the real game flow.
## Outputs
Test strategy/matrix; automated and manual evidence; playtest protocol/findings; bug register; balance log; polish backlog; alpha/beta/RC gate report; residual-risk handoff.
## References
- [QA, playtest and bug operations](references/qa-playtest-bug-operations.md)
- [Polish, balance and milestone gates](references/polish-balance-release-gates.md)
<!-- dual-compat-end -->
## Decision Rules
| Stage | Cannot advance while |
|---|---|
| Prototype | Core action is not understood or enjoyable |
| Vertical slice | Representative pipeline, performance or cultural gate fails |
| Alpha | Core systems or full completion path is missing |
| Beta | Major compatibility, balance, localisation or accessibility defects remain |
| RC | Build is non-reproducible or blocker/critical risks are unresolved |
| Any ad/economy gate | Privacy, child safety, accessibility, stopping, fairness or trust fails, regardless of revenue |
## Read Next
Use `lean-game-product-development` for hypothesis and pivot decisions, then `mobile-game-release-liveops` for signing, store, rollout and support readiness.
