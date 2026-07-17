---
name: game-accessibility-localisation-and-player-safety
description: Use when designing or testing accessible gameplay, remapping, visual/audio alternatives, difficulty assists, localisation/internationalisation, cultural review, chat/community safety, reporting, moderation, parental controls, or player-support escalation.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Accessibility, Localisation, and Player Safety

Treat access to gameplay, comprehension across languages, and community safety as system requirements tested with affected players.

<!-- dual-compat-start -->
## Use When
- Work covers controls, sensory/cognitive/motor access, text/voice localisation, culturalisation, chat/UGC, reporting, moderation, or child safety.

## Do Not Use When
- A menu-only checklist is being used to claim accessible gameplay.
- Automated translation or moderation is presented as sufficient human evidence.

## Required Inputs
Player/audience and age posture, game verbs/failure/monetisation loops, input/output/HUD inventory, target devices and viewing distances, languages/territories, content/string/voice pipeline, cultural fact/fiction/permission ledger, ads/analytics/social surfaces, legal/platform constraints, research plan, moderation/support capacity, and escalation/appeal policy.

## Workflow
1. Map every critical verb and feedback cue to motor, visual, auditory, cognitive, speech/language, and interruption barriers.
2. Specify remapping/alternate input, focus/navigation, timing/difficulty assists, redundant cues, readable HUD/menu/error presentation, motion/flash/haptic controls, captions/subtitles, and assist-state persistence from first launch through gameplay.
3. Externalise versioned text; support plural/gender/context, expansion, fonts/glyphs, bidi where required, audio timing, pseudo-localisation, and fallback.
4. Threat-model chat, voice, names, UGC, invitations, ads, purchases, analytics, blocking, reporting, parental gates, moderation, escalation, evidence minimisation, quiet/stopping cues, and appeals.
5. Route historical/living-culture meaning, terminology, motifs and permissions to named accountable reviewers; preserve disagreement and never treat repository research as approval.
6. Test core gameplay with representative players, assist settings, input methods, devices and viewing contexts; retain barriers, severity, fixes, residual exclusions, failed paths and regression cases.

## Quality Standards

- Critical gameplay, stopping, recovery and safety paths remain operable with the specified access settings and input methods.
- Text, speech, icon, colour, motion, audio and haptic information use tested alternatives where meaning would otherwise be lost.
- Localisation and cultural claims retain language, territory, reviewer, permission, build and unresolved-disagreement context.
- Child, social, advertising and purchase surfaces fail closed when age treatment, consent, moderation or vendor state is unknown.

## Anti-Patterns

- Accessible menus with inaccessible gameplay. Fix: test every critical verb and feedback channel end to end.
- Automated translation treated as release evidence. Fix: run linguistic, in-context and functional review on the identified build.
- Colour-only or audio-only meaning. Fix: add redundant visual, text, sound or haptic cues and verify comprehension.
- Cultural research treated as community permission. Fix: record named accountable consultation, rights and approval separately.
- Child-safe label with untested ads or social SDKs. Fix: verify age treatment, data flows, failure paths and kill switches on real devices.

## Degraded Mode

When representative-player, linguistic, cultural, moderation or device evidence is unavailable, document the requirement and prototype evidence only, disable the affected child/social/ad surface where safety is uncertain, and mark release fitness `not assessed` rather than passing the gate.

## Outputs
Accessibility requirement/test matrix; input/feedback map; localisation kit/glossary/build report; cultural review; safety/moderation runbook; player research and regression evidence.

## References
- [Access, localisation, and safety gates](references/access-localisation-safety-gates.md)
<!-- dual-compat-end -->
