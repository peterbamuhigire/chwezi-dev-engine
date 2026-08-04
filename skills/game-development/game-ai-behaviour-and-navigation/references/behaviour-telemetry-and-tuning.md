<!-- Source basis: AI for Game Developers (2005); Video Game Storytelling; XP 2026 engineering/AI evidence. Algorithms are evergreen foundations, not current engine APIs. -->

# Game AI Behaviour Telemetry and Tuning

Use deterministic or probabilistic behaviour deliberately. Choose the simplest
model that produces the intended player experience, then instrument it so tuning
is evidence-led.

## Behaviour contract

For each agent or controller record:

| Contract item | Required content |
|---|---|
| Goal and belief | What the character wants, believes, and can currently do |
| Decision model | Steering, pathfinding, FSM, utility/rule system, planner, or learned model |
| Inputs | Perception, navigation, world state, player state, difficulty and accessibility modifiers |
| State transitions | Entry, exit, interruption, timeout, recovery, and animation/audio handoff |
| Player impact | Readability, challenge, fairness, narrative intent, performance and failure cost |
| Tuning controls | Designer-authored parameters, safe ranges, version and rollback owner |

## Instrument before tuning

Record bounded, privacy-safe events for state transitions, goal selection,
path failures, stuck time, reaction latency, steering correction, perception
confidence, damage/death outcomes, difficulty modifiers, and player escape or
retry. Compare telemetry with replay or observation; do not treat a single
aggregate as proof of fun or fairness.

## Test matrix

Run the same behaviour through open space, obstacles, multiple agents, missing
path, target loss, teleports, frame-rate stress, save/load, network delay where
applicable, accessibility modifiers, and narrative interruption. Capture a
baseline, one hypothesis, a guardrail, a stop rule, and the exact build/config.

## Algorithm currency boundary

Chasing, evasion, flocking, A*, finite-state machines, scripting, fuzzy logic,
Bayesian reasoning, neural-network orientation, and genetic algorithms are useful
conceptual foundations from the 2005 book. Verify engine APIs, hardware limits,
modern model training, security, and performance with current technical sources
before implementation. Never replace a deterministic, debuggable controller
with learned behaviour without a human-visible fallback and rollback path.
