---
name: online-multiplayer-and-game-backend
description: Use when designing or implementing authoritative multiplayer topology, replication, RPCs, prediction, reconciliation, matchmaking, sessions, reconnect, game backend persistence, regional hosting, protocol evolution, or network tests.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Online Multiplayer and Game Backend

Make authority, replicated state, session transitions, persistence, and degraded network behaviour explicit and testable.

## Use When
- A game has remote players, lobbies, matchmaking, dedicated/listen servers, replicated actors/state, or backend-owned progression.

## Do Not Use When
- The request is local multiplayer only.
- Anti-cheat, moderation, or infrastructure deployment is the main task; compose with their specialist skills.

## Required Inputs
Engine/version, player/region/load envelope, topology, trust boundaries, tick/update budgets, gameplay state model, matchmaking rules, persistence ownership, privacy/security constraints, service objectives, cost limits, and version policy.

## Workflow
1. Choose topology from threat, fairness, latency, cost, and operational evidence; name the authority for every mutable field.
2. Specify session states from discovery through allocation, join, play, disconnect, reconnect, migration/termination, and cleanup.
3. Define replicated state, relevance/frequency, RPC direction/reliability/idempotency, prediction/reconciliation, and late-join snapshots.
4. Separate ephemeral match state from durable profile/economy state; make retries and ownership transfers safe.
5. Version protocol and content contracts; test compatible skew and reject incompatible clients with a recoverable message.
6. Exercise latency, loss, jitter, reorder, duplication, disconnect, reconnect, server crash, region loss, overload, and malicious input.

## Quality Standards
- The server validates consequential actions; a client request is never proof that an action was legal.
- Reliable delivery is used only for state that must arrive; queues must be bounded.
- Tests retain seed, build/protocol version, topology, network profile, server logs, and outcome.

## Outputs
Authority matrix; protocol/session contracts; replication budget; backend data ownership map; network test pack; capacity/region plan; compatibility and rollback runbook.

## References
- [Multiplayer authority and session gates](references/multiplayer-authority-session-gates.md)

