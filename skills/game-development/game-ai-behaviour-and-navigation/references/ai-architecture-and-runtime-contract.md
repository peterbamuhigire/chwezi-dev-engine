# AI Architecture and Runtime Contract

This reference distils durable patterns from *Artificial Intelligence in Unreal Engine 5* (2024) while remaining engine-neutral. The book targets UE 5.4; current engine documentation and the pinned project version override every API or maturity claim.

## Layer boundaries

| Layer | Owns | Must not silently own |
|---|---|---|
| Perception | stimuli, confidence, affiliation, age/forgetting | final decisions |
| Memory/world state | typed facts, provenance, lifetime | engine node configuration |
| Decision | state/tree/utility/planner selection | animation completion hacks |
| Action | bounded request, success/failure/cancel | global navigation policy |
| Navigation | agent geometry, costs, path status, recovery | gameplay victory conditions |
| Interaction | eligibility, reservation, use, release | orphaned permanent locks |
| Presentation | animation/audio/VFX/UI telegraph | authoritative behaviour state |
| Engine adapter | APIs, plugins, serialization, profiling | domain rules that prevent portability/testing |

## State/key registry

For every key record identifier, type, default, writer, readers, lifetime, replication/save rule, update trigger, invalid value and debug representation. Reject stringly typed or multiply-owned state.

## Navigation contract

Record agent radius/height/step/slope, generation mode, included/excluded geometry, area classes and costs, query filters, links/traversal actions, dynamic invalidation, partial-path policy, moving-target refresh, avoidance mode, stuck detector, recovery ladder and debug capture.

## Interaction reservation lifecycle

`discover → test eligibility → reserve atomically → approach → validate again → use → complete/cancel/timeout → release`.

Death, despawn, disconnect, level unload, failed path and interrupted animation must all release or transfer ownership deterministically.

## Unreal version overlay

For UE projects, record exact engine version and official documentation URLs for Behaviour Trees/Blackboards, Navigation, EQS, StateTree, Mass and Smart Objects. As of the 5.8 release, feature status must be checked in that pinned release rather than inherited from this 5.4 book. Isolate optional or experimental features behind adapters and retain a supported fallback.

## Durable Unreal-derived practices

- Meaningful node names and modular tasks/services/decorators.
- Runtime changing data in blackboards/state data, not shared node properties.
- Event-driven tree execution and bounded services.
- Controller/agent adapter separation from reusable decision logic.
- Frequent runtime debugging with state and execution traces.

These are engineering patterns, not proof that a specific Unreal subsystem fits another engine.
