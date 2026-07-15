---
name: game-audio-implementation
description: Use when designing, recording, licensing, editing, integrating, mixing, localising, profiling, or testing game music, ambience, dialogue, UI, Foley, spatial audio, and adaptive audio systems.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Audio Implementation
Create an audible feedback and storytelling system that remains legible, culturally permissioned, memory-conscious, localisable and useful even when the device is muted.

## Prerequisites

Load the approved game-state map, narrative/cultural governance, rights policy, localisation plan and selected engine integration constraints.
<!-- dual-compat-start -->
## Use When
- Building an audio bible, event map, buses, adaptive score, ambience, Foley, voice pipeline, subtitle timing, spatial mix, or audio performance budget.
## Do Not Use When
- Audio is only a late asset-drop or living/restricted repertoire has not been cleared.
## Required Inputs
Game states and event taxonomy, narrative/cultural boundaries, rights and performer agreements, device/speaker/headphone contexts, localisation plan, engine/middleware, memory/voice budgets and accessibility needs.
## Workflow
1. Define audio pillars, listener perspective, silence policy, event vocabulary and required non-audio equivalents.
2. Map music, ambience, Foley, UI, dialogue and creature/character states to gameplay events and priorities.
3. Commission or record only after repertoire, performers, consent, credits, territories and reuse rights are clear.
4. Edit, name, loudness-check, loop, tag and version source/master/runtime files.
5. Implement buses, snapshots, concurrency, variation, ducking, spatial ranges, occlusion and adaptive transitions.
6. Integrate subtitles, pronunciation guides, localisation context and lip/gesture timing where required.
7. Profile voices, decoding, streaming, memory, CPU and package size on target devices; test speakers, headphones, mute and interruption.
## Quality Standards
- Pair every gameplay-critical sound with visual or haptic communication.
- Prevent repeated sounds from becoming fatiguing through variation and concurrency control.
- Preserve source, licence, performer, consent and cultural restriction metadata.
- Make mix states recover correctly across pause, focus loss, calls, backgrounding and route changes.
## Anti-Patterns
- Music carrying required information. Fix: redundant communication.
- Sacred recording used as generic ambience. Fix: permission, contextual limits or original commissioned substitute.
- Unlimited simultaneous voices. Fix: priorities, caps and virtualisation.
- MP3/streaming/compression choice by habit. Fix: measure per asset class and engine.
- Voice recorded before final terminology. Fix: language and cultural gate first.
## Outputs
Audio bible; rights ledger; event/bus map; recording and localisation pack; integrated banks/assets; mix and accessibility test; performance evidence and release stems.
## References
- [Audio production and implementation](references/audio-production-implementation.md)
- [Cultural, rights and localisation gates](references/audio-rights-localisation.md)
<!-- dual-compat-end -->
## Decision Rules
| Asset | Default treatment |
|---|---|
| Short frequent effect | Memory-resident only if measured and bounded |
| Long music/ambience | Evaluate streaming and transition cost |
| Critical dialogue | Subtitle, context note, pronunciation and fallback |
| Restricted or unclear repertoire | Do not record or ship |
## Read Next
Use `game-testing-polish` for perceptual QA and `mobile-game-release-liveops` for privacy and download-pack policy.
