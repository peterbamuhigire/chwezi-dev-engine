# UX Book Study - Skill Improvements (Batch 5)

**Status:** Completed March 2026; trimmed 2026-09-24. This file is a historical
plan record only. The detailed rule lists it once carried were book-derived
content and have been removed under the engine's "Never store book extractions"
rule (see `AGENTS.md`). Do not re-execute this plan.

**Where the capability lives now:** UI/UX design practice has migrated to the
design engine (`design-system-skills`, resolved through the global engine
routing table). The `ux-for-ai` route is now an inactive alias resolved through
`docs/skill-aliases.yml`. Form, POS, healthcare, Compose and web GUI visual rules
are owned by the design engine; engineering skills here link to it rather than
restating visual doctrine.

## Goal (as planned)

Upgrade six existing design-adjacent skills and create three new ones
(`ux-psychology`, `ux-for-ai`, `lean-ux-validation`) so that generated
applications avoid templated "AI slop" interfaces.

## Sources named (titles only; no content stored)

- Celia Hodent, *What UX Is Really About*
- Jessica Enders, *Designing UX: Forms*
- Paduraru, *Roots of UI/UX Design*
- Panzarella, *UI/UX Web Design Simply Explained*
- Greg Nudelman, *UX for AI*
- Laura Klein, *UX for Lean Startups*

## Task list (as planned)

| Task | Target | Topic |
| --- | --- | --- |
| 1 | `ux-psychology` (new) | Cognitive foundations for interface decisions |
| 2 | `ux-for-ai` (new) | Trust, transparency, oversight and failure states for AI features |
| 3 | `lean-ux-validation` (new) | Hypothesis-driven validation before build |
| 4 | `form-ux-design` | Field anatomy, validation messaging, gateway and confirmation screens |
| 5 | `cognitive-ux-framework` | Attention, memory, bias and dark-pattern checks |
| 6 | `webapp-gui-design` | Visual fundamentals and mental-model alignment |
| 7 | `jetpack-compose-ui` | Mobile visual standards |
| 8 | `pos-sales-ui-design` | Checkout journey stages |
| 9 | `healthcare-ui-design` | Clinical motivation and cognitive load |
| 10 | Root docs | Index the new skills |

## Currentness note

Any numeric threshold or "law" once listed for these tasks must be re-verified
against current primary sources (for example W3C WAI for accessibility, and
platform guidance from developer.apple.com and developer.android.com) before
reuse. Popular figures such as "images are processed 60,000 times faster than
text" have no primary source and must not be used.
