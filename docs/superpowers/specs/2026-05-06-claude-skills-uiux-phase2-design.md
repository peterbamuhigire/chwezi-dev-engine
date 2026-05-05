# ~/.claude/skills UX/UI Phase 2 Upgrade — Design Spec
**Date:** 2026-05-06
**Author:** Claude (with peter.bamuhigire@gmail.com)
**Status:** Approved
**Phase:** 2 of 3

## Context

Phase 1 produced 5 UX/UI book extractions, with the canonical copies stored in this repo at `book-extractions/`. Phases 2 for `website-skills`, `social-media-skills`, and `srs-skills` have shipped. This spec defines the Phase 2 changes for `~/.claude/skills` itself — the foundational engine that other engines reference.

## Scope

5 file edits: 2 new + 3 extended. 1 commit.

```
~/.claude/skills/
├── enterprise-ux-process/
│   ├── SKILL.md                         (create — main skill)
│   └── references/
│       └── maturity-checklist.md        (create — quick-use checklist)
├── ux-standards.md                      (extend — philosophy layer)
├── sdlc-lifecycle.md                    (extend — UX maturity gate)
└── doc-standards.md                     (extend — UX declarations)
```

## Approach

This engine is the foundational layer. Unlike `website-skills`/`social-media-skills`/`srs-skills`, it owns the canonical book extractions and serves as the source-of-truth for the other engines. Therefore:
- **No new shared UX-foundations doc** — that would duplicate the canonical extractions
- **Skills cite the extractions directly** — `book-extractions/<name>-extraction.md`
- **Cross-cutting docs** (`ux-standards.md`, `sdlc-lifecycle.md`, `doc-standards.md`) gain pointers and operational rules, not new content bodies

The previously-empty `enterprise-ux-process/` placeholder (referenced by Phase 1 cross-references but never built) is filled in this phase.

## Per-file design

### 1. `enterprise-ux-process/SKILL.md` (NEW)

A first-class skill operationalizing Synechron's Enterprise UX process. Standard SKILL.md frontmatter (`name`, `description`). Sections:

- **Use when** — premium-priced enterprise projects: financial services, insurance, regulated industries, large internal apps, B2B SaaS.
- **Do not use when** — consumer products, prototypes, single-interaction landing pages (use simpler skills).
- **Required inputs** — problem definition, stakeholder list, business objective, success criteria, target maturity level (3 or 4).
- **Workflow** — 9 phases:
  1. Problem Definition + Business Objective
  2. Stakeholder Discussions / Interviews
  3. Success Criteria sign-off
  4. User Research (qualitative + quantitative)
  5. Competitor Analysis (cite Levy's 19-column matrix)
  6. Personas + User Journeys + Information Architecture
  7. Wireframes + Clickable Prototype + Visual Design Mockups
  8. Heuristic Evaluation
  9. Usability Testing + ADA/Section 508 verification
- **Outputs** — maturity-level declaration document + activity-by-level evidence pack + heuristic evaluation report + 5-outcomes pre-launch declaration.
- **Cross-references** — points to operational skills: `website-skills/skills/design-quality-score/` (Category 8), `srs-skills/01-strategic-vision/07-premium-product-positioning/`, and the canonical extraction `book-extractions/enterprise-ux-financial-insurance-extraction.md`.

### 2. `enterprise-ux-process/references/maturity-checklist.md` (NEW)

Quick-use checklist condensed from the canonical extraction's Activity-by-Level matrix. Standalone — usable in a project workspace where the canonical extraction is not local. Contents:

- 5-level model (Level 0 through Level 4) with one-line definitions
- Premium-pricing gate (Level 3 minimum)
- Activity-by-Level matrix (table with check-marks)
- Per-activity evidence requirements (one-liner per activity)
- 5-outcomes launch gate (Useful/Easy/Efficient/Pleasing/Accessible)

### 3. `ux-standards.md` (EXTEND)

The existing file (408 lines) is SaaS implementation patterns (Select2 dropdowns, etc.). It stays intact. Insert a new "Section 0: Foundational UX philosophy" near the top (immediately after the title block, before "Auto-Apply Rules"). Contents:

- One-paragraph framing: this file's bulk is implementation patterns; the philosophy lives in book-extractions
- Pointers to the 5 canonical extractions with one-line summaries
- Pointer to `enterprise-ux-process/SKILL.md` for the operational skill
- The four cross-cutting rules:
  1. Validated user research is non-negotiable (Levy)
  2. All 5 outcomes must hit, not 4 of 5 (Synechron)
  3. Recognition over recall + 4-stage cognitive affordance (Branson)
  4. Design is ongoing, not a project (Fekeshazi)
- Cross-engine consumption note: which engine/skill consumes which extraction

### 4. `sdlc-lifecycle.md` (EXTEND)

Append a new section "UX maturity gate (added 2026-05-06)" mapping the Synechron 5-level model onto SDLC phases:

- Discovery — Levels 3+ require user research, stakeholder interviews, success criteria signed
- Requirements — Levels 3+ require personas, journeys, IA, navigation flows
- Design — Levels 3+ require wireframes (low-fi + high-fi), clickable prototype, visual mockups
- Implementation — all levels require accessibility (ADA / Section 508 / WCAG 2.1 AA)
- Verification — Level 4 requires usability testing + test cases & scenarios
- Deployment — all levels require the 5 outcomes pre-launch declaration
- Maintenance — Level 4 requires experience-map updates per major release

Premium-priced engagements require Level 3 minimum across the lifecycle. Drop a tier if any phase fails to clear.

### 5. `doc-standards.md` (EXTEND)

Append "Required UX declarations in every document (added 2026-05-06)" — four short rules every doc-emitting skill must satisfy:

1. **Persona declaration** — Essential Persona named (per Branson's discipline). For docs without a user-facing surface, declare "N/A — internal infrastructure document" explicitly.
2. **Scope-level declaration** — Single Interaction / Journey / Relationship (per Deacon).
3. **Maturity-level declaration** — Level 3 / Level 4 / N/A (per Synechron).
4. **Affordance audit declaration** — for any UI-emitting doc, walk the 4 stages (Presence / Visibility / Recognizability / Intelligibility) on every primary CTA.

## Out of Scope

- Touching individual skills in `skills/` subdirectory (300+ files)
- `claude-guides/`, `blog-posts/`, `00-meta-initialization/`
- `orchestration-patterns-reference.md`, `prompting-patterns-reference.md`, `encoding-patterns-into-skills.md`
- Populating `enterprise-ux-process/assets/` and `scripts/` empty subdirs
- Modifying canonical book extractions

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| `enterprise-ux-process/SKILL.md` duplicates extraction content | SKILL.md is operational (use-when, workflow, outputs); the extraction is reference content. Different purposes. |
| `ux-standards.md` SaaS patterns drowned by philosophy | New Section 0 is short (~40 lines); impl patterns remain ~360 lines |
| Maturity gate in `sdlc-lifecycle.md` breaks existing flows | Gate applies only to "premium" tier; standard-tier flows unchanged |
| `doc-standards.md` declarations preachy | Keep to 4 short rules; provide explicit "N/A" escape hatch for non-UI docs |

## Success Criteria

- `enterprise-ux-process/SKILL.md` exists with full skill structure (frontmatter + use-when + workflow + outputs)
- `enterprise-ux-process/references/maturity-checklist.md` exists as standalone checklist
- 3 extended files contain "added 2026-05-06" markers
- One commit on `main` covers all 5 file edits
- Push to remote `origin` succeeds

## Approval

Approved by user 2026-05-06.

## Next Step

Invoke `superpowers:writing-plans`.
