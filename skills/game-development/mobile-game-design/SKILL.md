---
name: mobile-game-design
description: Use when designing or validating a mobile game's player fantasy, core loop, touch controls, sessions, onboarding, accessibility, progression, economy, retention, and ethical monetisation; use engine skills for implementation.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Mobile Game Design
Design a game around fingers, interruptions, small screens, varied devices, unreliable connectivity, and a player promise that remains enjoyable without coercive monetisation.

## Prerequisites

Load `game-development-orchestration` and the approved product thesis; use `design-system-skills` for interface appearance.
<!-- dual-compat-start -->
## Use When
- Defining genre, player fantasy, core loop, session cadence, controls, camera, tutorial, difficulty, progression, economy, or accessibility.
- Prototyping a mobile-first 2D or 3D experience or translating an existing game to touch.
## Do Not Use When
- Implementing engine code; use the Unity, Godot, or gameplay-systems skill.
- Treating store trends or player behaviour as current facts without verified research.
## Required Inputs
Player segments and age posture, intended learning outcomes if any, device/connectivity range, orientation, genre, business model, creative pillars, content/safety/wellbeing boundaries, cultural permissions, and available prototype evidence.
## Workflow
1. State the player fantasy as actor, repeated action, stakes, and desired emotion.
2. Prototype the one-minute verb loop before meta-progression, content scale, or monetisation.
3. Specify camera, gesture vocabulary, touch zones, handedness, interruption recovery, pause and save behaviour.
4. Map a 30-second first experience, first session, repeat session, failure recovery, and return path.
5. Design progression as mastery, knowledge, relationships, expression, capability, or authored content before numerical inflation.
6. Define economy sources, sinks, pacing, price/value presentation, caps, non-paying path and abuse cases; reject pay-to-win and gambling-like pressure.
7. For ads, define each placement, trigger, expected break, decline/close, cap/pace, reward, no-fill/offline/failure path, age/privacy treatment and kill switch. Reject any interruption of critical play, learning, narrative, save, recovery, stopping or safety.
8. Test with target players on physical low-, middle-, and high-tier devices; capture comprehension, completion, error, comfort, ad interruption/regret where applicable, and failed paths.
## Quality Standards
- Keep input count and simultaneous demands proportional to screen, posture and session context.
- Make controls discoverable, remappable where feasible, forgiving at touch edges, and operable with accessibility options.
- Design offline, suspend/resume, incoming-call, battery, heat, text scaling, colour, hearing and motor-access needs deliberately.
- Separate retention through value from retention through punishment or fear of loss.
- Separate learning evidence from engagement evidence and place wellbeing/trust guardrails beside retention and revenue.
## Anti-Patterns
- Desktop controls shrunk onto glass. Fix: redesign verbs and camera for touch.
- Tutorial text before meaningful action. Fix: teach through staged interaction and safe failure.
- Reward calendar before a fun loop. Fix: prove the repeated action first.
- One ideal device. Fix: test the defined device panel.
- Sacred or cultural knowledge as disposable currency. Fix: use narrative relationships and consultation gates.
- Rewarded ad presented as the only practical recovery. Fix: preserve a clear decline and viable core-play path without payment or ad viewing.
## Outputs
Player-promise brief; core-loop and session maps; touch-control specification; FTUE storyboard; progression/economy model; accessibility matrix; prototype hypotheses; playtest protocol and findings.
## References
- [Mobile design operating playbook](references/mobile-design-playbook.md)
- [Ethical progression and economy](references/progression-economy.md)
<!-- dual-compat-end -->
## Decision Rules
| Condition | Choice |
|---|---|
| Action needs precision unavailable on touch | Add assistance, simplify, change camera, or remove it |
| Session cannot survive interruption | Add safe checkpoint, state restore and explicit recovery |
| Progression changes numbers but not decisions | Redesign around capability, expression or knowledge |
| Monetisation damages fairness or narrative trust | Reject it |
| Ad cannot pass expectation, decline, interruption, child/privacy or no-fill tests | Disable the placement or the ad model |
| Learning claim has no construct and measure | Treat it as an untested design intention |
## Read Next
Use `lean-game-product-development` for falsifiable loop/engagement experiments, `gameplay-systems-architecture` for system specifications, and `game-testing-polish` for measured validation.
