# UI/UX Book Extractions — Phase 1 Design
**Date:** 2026-05-04
**Author:** Claude (with peter.bamuhigire@gmail.com)
**Status:** Approved

## Context

Four skill engines need world-class UI/UX capability so products command premium pricing:
- `C:\Users\BIRDC\.claude\skills\` (canonical / shared)
- `C:\wamp64\www\website-skills\`
- `C:\wamp64\www\social-media-skills\`
- `C:\wamp64\www\srs-skills\`

Five EPUBs supply the source material:
1. UX Strategy (Levy) — `UX Strategy.epub`
2. UX Design for Enterprise Apps — Financial Services / Insurance
3. UX & UI Strategy (Pamala B Deacon)
4. Product Managers' Guide to UX Design (Zoltan Fekeshazi)
5. UX/UI Design (Steven Branson)

## Decomposition

This design covers **Phase 1 only**. Subsequent phases each get their own spec.

- **Phase 1 (this spec):** Extract all 5 books into the existing `*-extraction.md` knowledge base pattern.
- **Phase 2 (later, per engine):** Write upgrade specs that translate extractions into concrete skill changes.
- **Phase 3 (later):** Implement skill changes per Phase 2 specs.

## Phase 1 Scope

### Tier per book

| Book | Tier | Slug |
|---|---|---|
| UX Strategy (Levy) | **Full** | `levy-ux-strategy-extraction.md` |
| UX Design for Enterprise Apps (Financial / Insurance) | **Full** | `enterprise-ux-financial-insurance-extraction.md` |
| UX & UI Strategy (Deacon) | Focused | `deacon-ux-ui-strategy-extraction.md` |
| Product Managers' Guide to UX (Fekeshazi) | Focused | `fekeshazi-pm-ux-guide-extraction.md` |
| UX/UI Design (Branson) | Focused | `branson-ux-ui-design-extraction.md` |

- **Full tier:** every actionable rule, every framework, every named technique. Target 400–600 lines per file.
- **Focused tier:** only material that's *new or distinct* relative to the existing 30+ extractions in `website-skills/book-extractions/`. Skip rules already well-covered (e.g., 12-column grids, "don't make me think" heuristics). Target 150–250 lines per file.

### Output locations (per file)

1. **Canonical:** `C:\Users\BIRDC\.claude\skills\book-extractions\<slug>.md`
2. **Copy:** `C:\wamp64\www\website-skills\book-extractions\<slug>.md`
3. **Copy:** `C:\wamp64\www\social-media-skills\book-extractions\<slug>.md`

`srs-skills` is excluded from copies — it's a requirements-doc engine with no `book-extractions/` folder. Phase 2 SRS spec will reference the canonical path.

### Format

Match the existing pattern (see `roots-of-uiux-design-extraction.md`):
- Header: title, source, subtitle, coverage note
- Body: dense bullets grouped by part / chapter / topic
- Prefer specific rules and numeric thresholds over abstract advice
- Include named frameworks verbatim (CUBI, Levy's 4 tenets, etc.)

### Method

1. Convert each EPUB → markdown via `pandoc` (already installed at `/c/ProgramData/chocolatey/bin/pandoc`).
2. Read converted text; for focused tier, cross-reference 2–3 existing UX extractions to identify gaps.
3. Write extraction file to canonical location.
4. After all 5 are written, copy to website-skills and social-media-skills `book-extractions/` folders.

## Out of Scope (Phase 1)

- Modifying any actual skill files
- Writing `*-upgrade-2026.md` roll-up files
- Any work in `srs-skills`
- Frontend implementation, design tokens, component code

## Risks

| Risk | Mitigation |
|---|---|
| EPUB conversion drops structure | Spot-check first 100 lines per book; fall back to alternate parser if needed |
| "Focused" judgment may exclude useful overlapping rules | When in doubt, include it — overlap is cheap; loss is expensive |
| Files become long (~600 lines) | Acceptable; matches existing pattern |
| Drift between canonical and engine copies | Phase 2 specs will treat canonical as source of truth |

## Deliverables

- 5 extraction files at canonical location
- 10 copies (5 books × 2 engines)
- This spec, committed (no git repo here, so just saved)
- 3 retained extraction files per book for future Phase 2 reference

## Approval

Approved by user 2026-05-04.
