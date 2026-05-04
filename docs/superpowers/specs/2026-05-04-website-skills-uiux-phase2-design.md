# Website-Skills UX/UI Phase 2 Upgrade — Design Spec
**Date:** 2026-05-04
**Author:** Claude (with peter.bamuhigire@gmail.com)
**Status:** Approved
**Phase:** 2 of 3 (Phase 1 = book extractions, Phase 3 = implementation per writing-plans output)

## Context

Phase 1 produced 5 UX/UI book extractions (Levy, Enterprise UX, Branson, Deacon, Fekeshazi) located at:
- Canonical: `C:\Users\BIRDC\.claude\skills\book-extractions\`
- Engine copy: `C:\wamp64\www\website-skills\book-extractions\`

This Phase 2 spec defines the concrete website-skills changes that translate those extractions into skill upgrades. Goal: world-class UX/UI baked into the engine so products it produces command premium pricing.

## Scope

Five core UX skills + two universal-guideline documents.

**Target skills (in `C:\wamp64\www\website-skills\skills\`):**
1. `premium-ui-ux-design`
2. `ux-psychology`
3. `design-quality-score`
4. `design-reference`
5. `design-system`

**Target guideline docs (in `C:\wamp64\www\website-skills\universal-guidelines\`):**
6. `UNIVERSAL-DESIGN-GUIDELINES.md`
7. `ux-laws-and-psychology.md`

## Approach

Mixed strategy — new reference files where the topic is genuinely new; extensions to existing files where the topic deepens what's there. Minimal SKILL.md edits to ensure new references are discoverable.

## Per-Skill Changes

### 1. `premium-ui-ux-design`

**New references (3 files in `references/`):**

- **`levy-four-tenets.md`** — Source: `levy-ux-strategy-extraction.md`. Contents: the four-tenet formula (Business Strategy + Value Innovation + Validated User Research + Killer UX Design), the four misinterpretations (with kickoff-meeting use), and the Top-10 anti-patterns ("Not-UX Strategies") used to reject weak briefs upfront.

- **`enterprise-five-outcomes.md`** — Source: `enterprise-ux-financial-insurance-extraction.md`. Contents: the 5 mandatory outcomes (Useful, Easy to use, Efficient, Pleasing, Accessible) restated as a pre-launch checklist with Yes/No verification per outcome.

- **`pm-collaboration-rules.md`** — Source: `fekeshazi-pm-ux-guide-extraction.md`. Contents: the 5+1 PM rules ("design is not pretty skin", "5-10 min to explain", "experimentation needs many prototypes", "teamwork requires client participation", "must be measured", "ongoing not project"), plus "don't hide important functions in menus" rule with the Trace case study reference.

**SKILL.md edit:** Append a "World-class UX foundations" subsection under existing structure, listing the three new references with one-line summaries. No rewrite of skill purpose.

### 2. `ux-psychology`

**New references (2 files in `references/`):**

- **`three-paradigms-of-hci.md`** — Source: `branson-ux-ui-design-extraction.md`. Contents: Building / HIP / Design Thinking paradigms; the cockpit-voice example showing all three lenses; rule that all three are complementary, not exclusive. Used as a stakeholder-alignment tool when teams disagree about "good design."

- **`three-levels-of-ux-scope.md`** — Source: `deacon-ux-ui-strategy-extraction.md`. Contents: Single Interaction / Journey / Relationship levels with examples. Used at engagement scoping to set expectations between client and designer.

**Extend existing file:**

- **`references/legacy-guidance.md`** — Append two new sections at end:
  - "Working memory and cognitive load" — Miller's 7±2, chunking, stacking (with phone-number and `001 010 110 111 000` examples), cognitive load (Sweller), recognition over recall.
  - "Four-stage cognitive affordance discipline" — Presence → Visibility/Perceivability → Recognizability → Intelligibility, with the "where the hell is the sign in" anti-pattern.

**SKILL.md edit:** Update description to mention "Three Paradigms framing and working-memory limits"; add the three new/extended file references in a "Required reading" line.

### 3. `design-quality-score`

**New reference (1 file in `references/`):**

- **`enterprise-ux-maturity-checklist.md`** — Source: `enterprise-ux-financial-insurance-extraction.md`. Contents: the 5-level UX maturity model (No Design / Uninformed UI Styling / Style & Color Problem-Solving / UX Design / Experience Design Innovation) plus the full activity-by-level matrix (Problem Definition, Stakeholder Discussions, Success Criteria, User Research, Competitor Analysis, etc.). Becomes a complementary gate: a project's process maturity is scored alongside its rendered-output rubric.

**Extend existing files:**

- **`references/rubric.md`** — Add a new 8th category: "UX Maturity" with explicit guidance: a project may not score ≥8/10 on premium claims unless documented activities align with Level 3 (UX Design) at minimum. Note that this category is *additive* — it does not retroactively fail prior 7-category scores; existing scored templates remain valid.

- **`references/score-calibration.md`** — Append a "Resolving scorer disagreements" section using Fekeshazi's research-as-arbiter principle: when two scorers disagree, the tiebreaker is fresh user-test data rather than seniority.

**SKILL.md edit:** Mention "UX Maturity (process)" in the rubric overview line.

### 4. `design-reference`

**New reference (1 file in `references/`):**

- **`levy-competitive-matrix.md`** — Source: `levy-ux-strategy-extraction.md`. Contents: the full attribute list (URL/app store, throwaway login, purpose of site, year founded, funding rounds, revenue streams, monthly traffic, # of SKUs/listings, primary categories, social networks, content types, personalization features, community/UGC features, competitive advantage, heuristic A–F evaluation, customer reviews, general notes, questions to team). Includes targets (5 direct + 3 indirect competitors minimum) and the 30-min-per-row pacing rule.

**Extend existing file:**

- **`references/competitor-analysis-worksheet.md`** — Restructure column headings to use Levy's matrix columns. Preserve any local sector-specific adaptations as additional rows in a separate "Local additions" subsection.

**SKILL.md edit:** Mention the Levy matrix as the canonical worksheet format; add file reference.

### 5. `design-system`

**New reference (1 file in `references/`):**

- **`enterprise-data-viz-rules.md`** — Source: `enterprise-ux-financial-insurance-extraction.md`. Contents: dashboard/data-viz rules (no 3D widgets, avoid heavy shadows/gradients on charts, color enhances meaning not decoration, pick chart type for the data not the deck, pre-attentive attributes — size, color, orientation, proximity, similarity, connections). Necessary because website-skills produces dashboards via the dashboards/ engine.

**Extend existing files:**

- **`references/ux-quality-checklist.md`** — Add a "First-impression and orientation" section combining Deacon's UI considerations (consistency in colors/borders/fonts/effects, responsiveness with loading indicators, familiar words like sign-up/login, streaming with contact info on every page) and Fekeshazi's "5-10 minutes to explain at first use" rule.

- **`references/ai-slop-prevention.md`** — Add an "Enterprise anti-patterns" section listing the 5 patterns from Enterprise UX (feature overload, uninformed design, inconsistent, old-fashioned look, cluttered information) with one-line detection cues for each.

**SKILL.md edit:** Add a sentence acknowledging dashboard/data-viz coverage and pointer to the new rules file.

### 6. `universal-guidelines/UNIVERSAL-DESIGN-GUIDELINES.md`

**Extend** — Add a new top-level section, "World-class UX foundations (book-derived)", before the closing/appendix material if any. Section contents:
- One sentence per book naming the extraction file
- The 4 cross-cutting rules:
  1. Levy: "Validated user research is non-negotiable — no Field of Dreams launches."
  2. Enterprise UX: "All 5 outcomes (useful, easy, efficient, pleasing, accessible) must hit, not 4 of 5."
  3. Branson: "Recognition over recall; 4-stage cognitive affordance must pass at every stage."
  4. Fekeshazi: "Design is ongoing, not a project — plan for continuous design alongside continuous dev."

### 7. `universal-guidelines/ux-laws-and-psychology.md`

**Extend** — Append two new sections:
- **"Working-memory laws"** — Miller's 7±2 with concrete bound implications (limit primary nav to ≤7, chunk longer lists), Sweller's cognitive load, stacking and task-decomposition rule.
- **"Three Paradigms of HCI design"** — short framing of Building / HIP / Design Thinking with the cockpit-voice example abbreviated to one paragraph.

## Deliverables Summary

| Type | Count | Files |
|---|---|---|
| New reference files | 8 | levy-four-tenets, enterprise-five-outcomes, pm-collaboration-rules, three-paradigms-of-hci, three-levels-of-ux-scope, enterprise-ux-maturity-checklist, levy-competitive-matrix, enterprise-data-viz-rules |
| Extended existing files | 8 | ux-psychology/legacy-guidance, design-quality-score/rubric, design-quality-score/score-calibration, design-reference/competitor-analysis-worksheet, design-system/ux-quality-checklist, design-system/ai-slop-prevention, UNIVERSAL-DESIGN-GUIDELINES, ux-laws-and-psychology |
| Minimal SKILL.md edits | 5 | premium-ui-ux-design, ux-psychology, design-quality-score, design-reference, design-system |

**Total file edits: 21.**

## Out of Scope

- `cro-audit`, `form-ux-design`, `experimentation`, `long-form-sales-copy` (conversion cluster — separate Phase 2 spec if desired later)
- `page-builder`, `website-builder`, `premium-website-product` (downstream build skills)
- Modifying the 30+ existing book-extraction summaries
- New skills creation
- Modifying `social-media-skills` or `srs-skills` (those have their own Phase 2 specs)

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Rubric.md edit re-scores existing "8/10" templates retroactively | Make UX Maturity *additive* — explicit note that prior scores remain valid; new category applies to new work |
| Three new files in `premium-ui-ux-design/references/` causes folder bloat | Topics are cleanly separated; each file stays under ~300 lines |
| Extension to `legacy-guidance.md` could conflict with existing tone | Append at end with clear section breaks; do not rewrite earlier content |
| `competitor-analysis-worksheet.md` restructure may lose local adaptations | Preserve adaptations under a "Local additions" subsection |

## Success Criteria

- All 21 files edited / created and verifiable via `ls` + line-count diffs
- Each new reference file cites its source extraction at the top (provenance)
- Each modified SKILL.md still passes its own structural conventions (frontmatter, "Use when", "Required inputs")
- A spot-test: pick one upgraded skill (e.g., `ux-psychology`) and verify its references actually load via the existing skill mechanism

## Approval

Approved by user 2026-05-04 ("yes" after design presentation).

## Next Step

Invoke `superpowers:writing-plans` skill to create a detailed implementation plan for the 21 file edits.
