---
name: game-accessibility-localisation-and-player-safety
description: Use when designing or testing accessible gameplay, remapping, visual/audio alternatives, difficulty assists, localisation/internationalisation, cultural review, chat/community safety, reporting, moderation, parental controls, or player-support escalation.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Accessibility, Localisation, and Player Safety

Treat access to gameplay, comprehension across languages, and community safety as system requirements tested with affected players.

## Use When
- Work covers controls, sensory/cognitive/motor access, text/voice localisation, culturalisation, chat/UGC, reporting, moderation, or child safety.

## Do Not Use When
- A menu-only checklist is being used to claim accessible gameplay.
- Automated translation or moderation is presented as sufficient human evidence.

## Required Inputs
Player/audience and age posture, game verbs/failure loops, input/output inventory, target languages/territories, content/string/voice pipeline, online social surfaces, legal/platform constraints, research plan, moderation/support capacity, and escalation/appeal policy.

## Workflow
1. Map every critical verb and feedback cue to motor, visual, auditory, cognitive, speech/language, and interruption barriers.
2. Specify remapping, timing/difficulty assists, redundant cues, readable presentation, motion/flash controls, captions/subtitles, and assist-state persistence.
3. Externalise versioned text; support plural/gender/context, expansion, fonts/glyphs, bidi where required, audio timing, pseudo-localisation, and fallback.
4. Threat-model chat, voice, names, UGC, invitations, blocking, reporting, parental controls, moderation, escalation, evidence retention, and appeals.
5. Test core gameplay with representative players and devices; retain barriers, severity, fixes, residual exclusions, and regression cases.

## Outputs
Accessibility requirement/test matrix; input/feedback map; localisation kit/glossary/build report; cultural review; safety/moderation runbook; player research and regression evidence.

## References
- [Access, localisation, and safety gates](references/access-localisation-safety-gates.md)

