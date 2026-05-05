# ~/.claude/skills UX/UI Phase 2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Populate the empty `enterprise-ux-process/` placeholder with a real skill + extend the three top-level cross-cutting docs (`ux-standards.md`, `sdlc-lifecycle.md`, `doc-standards.md`) with book-derived UX foundations and rules.

**Architecture:** Markdown-only documentation upgrade. Each task creates or extends a markdown file. Verification = file exists, expected line count, grep markers pass. One commit at the end + push.

**Tech Stack:** Markdown only. Sources at `book-extractions/` (engine-local). Targets at `~/.claude/skills/` root + `enterprise-ux-process/`.

**Spec:** `docs/superpowers/specs/2026-05-06-claude-skills-uiux-phase2-design.md`

**Repo state:** `~/.claude/skills` is a git repo on `main` (remote `origin` → `peterbamuhigire/skills-web-dev.git`).

---

## File Map

```
~/.claude/skills/
├── enterprise-ux-process/
│   ├── SKILL.md                                       (create)
│   └── references/
│       └── maturity-checklist.md                      (create)
├── ux-standards.md                                    (extend — insert Section 0 near top)
├── sdlc-lifecycle.md                                  (extend — append at end)
└── doc-standards.md                                   (extend — append at end)
```

**5 file edits: 2 new + 3 extended.**

---

## Conventions

- New files start with provenance: cite `book-extractions/<name>-extraction.md` as source
- Each extension marks itself: `## <Section Title> (added 2026-05-06 from <book>)`
- Do NOT modify existing frontmatter on the 3 extended files
- Do NOT introduce emojis
- Append at end-of-file with leading blank line, EXCEPT `ux-standards.md` which gets a Section 0 insertion near the top

---

## Task 1: Create `enterprise-ux-process/SKILL.md`

**Files:**
- Create: `C:\Users\BIRDC\.claude\skills\enterprise-ux-process\SKILL.md`

- [ ] **Step 1: Write the file with this EXACT content:**

```markdown
---
name: enterprise-ux-process
description: Operationalize Synechron's enterprise UX process for premium-priced enterprise engagements (financial services, insurance, regulated industries, large internal apps, B2B SaaS). Produces maturity-level declaration + activity evidence pack + heuristic evaluation + 5-outcomes pre-launch declaration. Cite when scoping, executing, or auditing premium enterprise UX work.
---

# Enterprise UX Process Skill
**Source:** Operationalizes `book-extractions/enterprise-ux-financial-insurance-extraction.md` (Synechron, 2018; derived from The Design Ladder + Natalie Hanson's UX Maturity Model).

---

## Use when

- Scoping or executing a premium-priced enterprise UX engagement (financial services, insurance, healthcare, regulated industries, large internal apps, B2B SaaS)
- Auditing whether an enterprise project is positioned correctly on the maturity scale
- Defending a premium-pricing claim against an internal or external review
- Bridging strategy (Levy) and tactical UX work (Branson, Deacon, Fekeshazi) into a single enterprise-grade process

## Do not use when

- The work is consumer-grade (single-interaction, low-stakes) — use simpler skills
- The artifact is a prototype or experiment, not a production deliverable
- The project is explicitly priced as standard tier and the team has agreed not to pursue premium positioning

## Required inputs

Before invoking this skill, the following must be available or generated:

- Problem definition statement (what is the need; why now; for whom)
- Stakeholder list with roles (funder, owner, executor)
- Business objective (what success means in measurable terms)
- Success criteria (signed off by stakeholders)
- Target maturity level: **3 (UX Design)** for standard premium, **4 (Experience Design)** for top-tier

## Workflow — 9 phases

The process maps directly to Synechron's Activity-by-Level matrix. All 9 phases must produce documented evidence at Level 3+; the additional Level 4 activities are noted inline.

### Phase 1 — Problem Definition + Business Objective
- UX team meets with business stakeholders and product owners
- Answer: What is the need? Why now? For whom? How does this make life easier for the end user?
- Document vision, hopes, aspirations, and fears from the business perspective
- Output: signed problem-definition document

### Phase 2 — Stakeholder Discussions / Interviews
- Identify funders, owners, executors
- Conduct focused-group discussions OR individual interviews
- Capture: roles, expectations from UX, problem perception, end-user identification, collective goals, organizational/competitive/scope context
- Output: stakeholder-interview transcripts + summary brief

### Phase 3 — Success Criteria sign-off
- Checklist of measures the deliverable must hit to be successful
- Documented and agreed by all stakeholders
- Treat as non-negotiable acceptance criteria
- Output: signed success-criteria document

### Phase 4 — User Research (qualitative + quantitative)
- Methodologies: interviews, contextual inquiries, eye tracking, surveys, A/B testing, web analytics, field studies
- Quantitative: how many, what %
- Qualitative: why behaviors occur, what users notice
- Output: user-research report with both data types

### Phase 5 — Competitor Analysis
- Use Levy's 19-column competitive matrix (cite `book-extractions/levy-ux-strategy-extraction.md` Part VII or, in `website-skills`, `skills/design-reference/references/levy-competitive-matrix.md`)
- Minimum: 5 direct + 3 indirect competitors
- Output: filled matrix + 1-page distilled brief

### Phase 6 — Personas + User Journeys + Information Architecture
- Personas: apply Branson's discipline (Essential Persona declared, Mechanics floor — name, demographics, goals, environment, pain points, stress points)
- User Journeys: chronological touch-point sequence per primary persona
- Information Architecture: organization, structure, labelling of all content; navigation strategy/flow; site map; content buckets; intuitive labels
- **Level 4 also requires:** Experience Maps
- Output: persona deck + journey deck + IA deck

### Phase 7 — Wireframes + Clickable Prototype + Visual Design Mockups
- Wireframes: low-fidelity (paper) + high-fidelity (no color, focus on flow)
- Clickable prototype: stitched screens behaving like the real product per crucial user scenarios
- Visual design mockups: full-scale static representation with colors, branding, graphics
- **Level 4 also requires:** Mood Boards
- Output: wireframe pack + interactive prototype + mockup set

### Phase 8 — Heuristic Evaluation
- UX expert reviews against Nielsen-style heuristics:
  1. Visibility of System Status
  2. Match Between System and the Real World
  3. User Control and Freedom
  4. Consistency and Standards
  5. Error Prevention & Error Handling
  6. Recognizing Rather than Recall
  7. Flexibility and Efficiency of Use
  8. Aesthetic and Minimal Design
  9. Help and Documentation
- Plus Branson's 4-stage cognitive affordance audit per primary CTA (Presence → Visibility → Recognizability → Intelligibility)
- Output: heuristic evaluation report listing flaws + improvements

### Phase 9 — Usability Testing + ADA / Section 508 verification (Level 4 + all-levels accessibility)
- Usability testing: moderated in-person, moderated remote, OR unmoderated remote
- Test scenarios derived from actual use cases and task flows
- ADA / Section 508 / WCAG 2.1 AA verification — required at ALL maturity levels
- Output: usability test report + accessibility audit

## Outputs

A complete enterprise-ux-process engagement produces:

1. **Maturity-level declaration** — single sentence at the top of the engagement summary: "This engagement operates at UX Maturity Level [3 / 4], per Synechron's 5-level model."
2. **Activity-by-level evidence pack** — see `references/maturity-checklist.md` for the matrix and required evidence per activity
3. **Heuristic evaluation report** — Phase 8 output
4. **Five-outcomes pre-launch declaration** — Yes/No with evidence per outcome:
   - Useful (persona-validated)
   - Easy to use (first-task success without coaching)
   - Efficient (task time benchmarked)
   - Pleasing (≥ 4/5 first-impression rating)
   - Accessible (ADA/Section 508/WCAG 2.1 AA)
   - **Rule:** 4-of-5 disqualifies premium pricing. One No = no launch.

## Cross-references

### Canonical extraction (source-of-truth)
- `book-extractions/enterprise-ux-financial-insurance-extraction.md`

### Related skills in this engine
- `book-extractions/levy-ux-strategy-extraction.md` — strategy framing (Four Tenets) that should sit upstream of this process
- `book-extractions/branson-ux-ui-design-extraction.md` — persona discipline + working memory + 4-stage affordance applied within phases 6 and 8
- `book-extractions/deacon-ux-ui-strategy-extraction.md` — 3 levels of UX scope; declare in Phase 1
- `book-extractions/fekeshazi-pm-ux-guide-extraction.md` — PM collaboration rules and the "design is ongoing" stance

### Operational skills in other engines
- `website-skills/skills/design-quality-score/` — Category 8 (UX Maturity) scores the same artifacts independently
- `website-skills/skills/premium-ui-ux-design/references/enterprise-five-outcomes.md` — same 5-outcomes gate applied to website templates
- `srs-skills/01-strategic-vision/07-premium-product-positioning/` — premium-positioning gate using the same 5+5 model
- `srs-skills/03-design-documentation/05-ux-specification/` — UX spec produced under this process

### Quick-use checklist
- `references/maturity-checklist.md` — standalone activity-by-level checklist for use in project workspaces
```

- [ ] **Step 2: Verify**

Run: `wc -l "C:/Users/BIRDC/.claude/skills/enterprise-ux-process/SKILL.md"`
Expected: ≥ 100 lines.

Run: `grep -c "^## Phase \|^### Phase " "C:/Users/BIRDC/.claude/skills/enterprise-ux-process/SKILL.md"`
Expected: ≥ 9.

---

## Task 2: Create `enterprise-ux-process/references/maturity-checklist.md`

**Files:**
- Create: `C:\Users\BIRDC\.claude\skills\enterprise-ux-process\references\maturity-checklist.md`

- [ ] **Step 1: Write the file with this EXACT content:**

```markdown
# Enterprise UX Maturity Checklist (quick-use)
**Source:** Condensed from `book-extractions/enterprise-ux-financial-insurance-extraction.md` Parts VIII + IX.
**Used by:** `enterprise-ux-process` skill.

---

## The 5-level model (one-line definitions)

- **Level 0 — No Design:** ignored entirely
- **Level 1 — Uninformed UI Styling:** cosmetic only
- **Level 2 — Style & Color (Problem Solving):** UX approach defined; goals integrated
- **Level 3 — UX Design:** flow drives behavior; problems solved effectively
- **Level 4 — Experience Design (Innovation):** wow factor; design thinking process

## Premium-pricing gate

A project may not score as premium unless documented activities align with **Level 3 (UX Design) at minimum**. Top-tier (luxury, regulated, mission-critical) requires **Level 4 (Experience Design)**.

## Activity-by-Level Matrix

| Activity | L1 Styling | L2 Problem Solving | L3 UX Design | L4 Experience Design |
|---|---|---|---|---|
| Problem Definition & Business Objective |  |  | ✓ | ✓ |
| Stakeholder Discussions / Interviews |  |  | ✓ | ✓ |
| Success Criteria |  |  | ✓ | ✓ |
| User Research |  |  | ✓ | ✓ |
| Competitor Analysis |  |  | ✓ | ✓ |
| User Interviews |  |  | ✓ | ✓ |
| Personas |  |  | ✓ | ✓ |
| Experience Maps |  |  |  | ✓ |
| User Journeys |  |  | ✓ | ✓ |
| Information Architecture |  |  | ✓ | ✓ |
| Navigation Flow |  |  | ✓ | ✓ |
| Task Flows |  |  | ✓ | ✓ |
| Wireframes (low-fi + high-fi) |  |  | ✓ | ✓ |
| Clickable Prototype |  |  | ✓ | ✓ |
| Visual Design Mockups | ✓ | ✓ | ✓ | ✓ |
| Mood Boards |  |  |  | ✓ |
| Design Templates & Style Guides | ✓ | ✓ | ✓ | ✓ |
| Heuristic / Expert Evaluation |  |  | ✓ | ✓ |
| Usability Testing |  |  |  | ✓ |
| Test Cases & Scenarios |  |  |  | ✓ |
| ADA / Section 508 Compliance | ✓ | ✓ | ✓ | ✓ |

## Per-activity evidence requirements (one-liner each)

- **Problem Definition** — signed answer to: what is the need, why now, for whom, how does this make life easier?
- **Stakeholder Discussions** — interview transcripts + summary brief
- **Success Criteria** — signed checklist of measurable success conditions
- **User Research** — qualitative + quantitative report with methodology disclosed
- **Competitor Analysis** — Levy's 19-column matrix filled (5 direct + 3 indirect minimum)
- **User Interviews** — process / device usage / preference / industry exposure / context-of-use questions
- **Personas** — Essential Persona declared per primary user role with Branson Mechanics floor
- **Experience Maps** — visual flow with feelings, frustrations, expectations
- **User Journeys** — chronological touch-point sequence per primary persona
- **Information Architecture** — organized labelled content + navigation strategy + sitemap
- **Navigation Flow** — persistent / sequential / hierarchical drill-down patterns documented
- **Task Flows** — diagrams showing tasks user performs to meet goals
- **Wireframes** — low-fi (paper) + high-fi (no color, focus on flow)
- **Clickable Prototype** — stitched screens per crucial scenarios; behaves like real product
- **Visual Design Mockups** — full-scale static with colors, branding, graphics
- **Mood Boards** — themes/moods using digital, abstract, physical references
- **Design Templates & Style Guides** — working models for layout/page/screen consistency
- **Heuristic Evaluation** — Nielsen-style 9-point review + Branson's 4-stage affordance audit
- **Usability Testing** — moderated in-person OR moderated remote OR unmoderated remote
- **Test Cases & Scenarios** — derived from actual use cases; goal/task oriented
- **Accessibility (ADA / Section 508 / WCAG 2.1 AA)** — required at all levels; verified, not implied

## 5-outcomes launch gate (in addition to maturity gate)

A project also passes a launch gate based on Synechron's 5 outcomes:

| # | Outcome | Pass criterion |
|---|---|---|
| 1 | **Useful** | Persona-validated; tested against documented goals |
| 2 | **Easy to use** | First-task success in usability test without coaching |
| 3 | **Efficient** | Task time benchmarked against competitor or prior baseline |
| 4 | **Pleasing** | Subjective rating ≥ 4/5 on initial-impression test |
| 5 | **Accessible** | ADA / Section 508 / WCAG 2.1 AA verified |

**Rule:** 4-of-5 disqualifies premium pricing. One No = no launch.

## Procedure when a gate fails

1. Identify the missing activity or outcome
2. Either close the gap (add the missing evidence) and re-engage, OR
3. Re-position at a lower tier (standard / mid-tier) honestly

Premium claims that fail either gate damage credibility on first audit.
```

- [ ] **Step 2: Verify**

Run: `wc -l "C:/Users/BIRDC/.claude/skills/enterprise-ux-process/references/maturity-checklist.md"`
Expected: ≥ 60 lines.

Run: `grep -c "^- \*\*Level " "C:/Users/BIRDC/.claude/skills/enterprise-ux-process/references/maturity-checklist.md"`
Expected: 5.

Run: `grep -c "^| [A-Z]" "C:/Users/BIRDC/.claude/skills/enterprise-ux-process/references/maturity-checklist.md"`
Expected: ≥ 21 (the matrix activity rows).

---

## Task 3: Insert "Section 0" near top of `ux-standards.md`

**Files:**
- Modify: `C:\Users\BIRDC\.claude\skills\ux-standards.md`

The current top of the file looks like:
```
# UX Standards Enforcement Skill

**Skill Name:** `ux-standards`
**Purpose:** Enforce mandatory UX patterns for web SaaS development
**Priority:** CRITICAL - Auto-apply to all web UI development

---

## Auto-Apply Rules
```

Insert the new Section 0 between the `---` separator and `## Auto-Apply Rules`.

- [ ] **Step 1: Read the file head**

Run: `head -10 "C:/Users/BIRDC/.claude/skills/ux-standards.md"`

Confirm the structure shown above.

- [ ] **Step 2: Insert Section 0**

Use Edit tool to replace this exact block:

OLD:
```
---

## Auto-Apply Rules
```

NEW:
```
---

## Section 0 — Foundational UX philosophy (added 2026-05-06)

The bulk of this file (Sections 1+) is SaaS implementation patterns. The philosophy that grounds those patterns lives in the canonical book extractions at `book-extractions/`. Read this section first when evaluating whether a project needs the implementation patterns at all.

### The 5 canonical book extractions

- `book-extractions/levy-ux-strategy-extraction.md` — UX strategy as upstream gate (Four Tenets, Top-10 anti-patterns, Funnel Matrix, landing-page experiments)
- `book-extractions/enterprise-ux-financial-insurance-extraction.md` — enterprise process (5-level maturity, 5 outcomes, activity-by-level matrix)
- `book-extractions/branson-ux-ui-design-extraction.md` — psychology (Three HCI Paradigms, working memory, 4-stage cognitive affordance, persona discipline)
- `book-extractions/deacon-ux-ui-strategy-extraction.md` — UX history + 3 levels of UX scope
- `book-extractions/fekeshazi-pm-ux-guide-extraction.md` — PM collaboration rules and design-as-ongoing-process

### The four cross-cutting rules

1. **Validated user research is non-negotiable** (Levy). No "Field of Dreams" launches. Confront target customers with an MVP/landing page before scaling.
2. **All 5 outcomes must hit, not 4 of 5** (Synechron). Useful + Easy + Efficient + Pleasing + Accessible. One No = no premium launch.
3. **Recognition over recall + 4-stage cognitive affordance** (Branson). Show, don't make users remember. Every interactive element must pass Presence → Visibility → Recognizability → Intelligibility.
4. **Design is ongoing, not a project** (Fekeshazi). Plan for continuous design alongside continuous dev.

### Operational skill

For premium-priced enterprise engagements, invoke `enterprise-ux-process/SKILL.md` — operationalizes the Synechron process into 9 phases with declared maturity-level + 5-outcomes evidence pack.

### Cross-engine consumption map

- `website-skills/` — consumes Levy + Synechron + Branson + Deacon + Fekeshazi (5 skills upgraded; see `website-skills/universal-guidelines/`)
- `social-media-skills/` — consumes Branson personas + Levy tenets + Synechron 5 outcomes (Persona + Strategy clusters; see `social-media-skills/docs/ux-foundations.md`)
- `srs-skills/` — consumes all 5 (UX-spec + Strategic-vision clusters; see `srs-skills/docs/ux-foundations.md`)

### When to apply Sections 1+ (the implementation patterns)

The implementation patterns below (searchable dropdowns, etc.) apply when (a) the project is web SaaS AND (b) the philosophy gate above has been cleared. Don't apply patterns to a project that hasn't yet validated user research.

---

## Auto-Apply Rules
```

- [ ] **Step 3: Verify**

Run: `grep -c "Section 0 — Foundational UX philosophy" "C:/Users/BIRDC/.claude/skills/ux-standards.md"`
Expected: 1.

Run: `grep -c "book-extractions/" "C:/Users/BIRDC/.claude/skills/ux-standards.md"`
Expected: ≥ 5.

Run: `grep -c "^## Auto-Apply Rules" "C:/Users/BIRDC/.claude/skills/ux-standards.md"`
Expected: 1 (the existing section preserved).

---

## Task 4: Append to `sdlc-lifecycle.md`

**Files:**
- Modify: `C:\Users\BIRDC\.claude\skills\sdlc-lifecycle.md`

- [ ] **Step 1: Inspect end of file**

Run: `tail -5 "C:/Users/BIRDC/.claude/skills/sdlc-lifecycle.md"`

- [ ] **Step 2: Append exactly this content (with leading blank line)**

```markdown

## UX maturity gate (added 2026-05-06 from Synechron Enterprise UX)

Source: `book-extractions/enterprise-ux-financial-insurance-extraction.md` Parts VIII + IX.

**Premium-priced engagements require Level 3 (UX Design) minimum across the SDLC.** Top-tier engagements (regulated, mission-critical) require Level 4 (Experience Design). Standard-tier engagements are unaffected by this gate.

### Phase-by-phase mapping

| SDLC phase | Level 3 minimum activities | Level 4 additional activities |
|---|---|---|
| **Discovery** | User research, stakeholder interviews, success criteria signed | Experience maps |
| **Requirements** | Personas (Essential Persona declared), user journeys, IA, navigation flows | Mood boards |
| **Design** | Wireframes (low-fi + high-fi), clickable prototype, visual mockups, heuristic evaluation | — |
| **Implementation** | ADA / Section 508 / WCAG 2.1 AA (required at all levels) | — |
| **Verification** | Heuristic evaluation report | Usability testing + test cases & scenarios |
| **Deployment** | 5-outcomes pre-launch declaration (Useful/Easy/Efficient/Pleasing/Accessible) | — |
| **Maintenance** | — | Experience-map updates per major release |

### Drop-tier rule

If any phase fails to clear the Level 3 activities for a premium-tier engagement, drop the engagement to standard tier. Do not paper over the gap with stronger marketing — premium claims fail credibility on first audit when the activities are missing.

### Operational skill

For full enterprise engagements, invoke `enterprise-ux-process/SKILL.md` — operationalizes the 9-phase process with full evidence pack. Quick-use checklist at `enterprise-ux-process/references/maturity-checklist.md`.

### Cross-references

- `book-extractions/enterprise-ux-financial-insurance-extraction.md` — canonical source
- `website-skills/skills/design-quality-score/references/rubric.md` Category 8 — engine-level scoring
- `srs-skills/01-strategic-vision/07-premium-product-positioning/SKILL.md` — premium positioning gate
```

- [ ] **Step 3: Verify**

Run: `grep -c "UX maturity gate (added 2026-05-06" "C:/Users/BIRDC/.claude/skills/sdlc-lifecycle.md"`
Expected: 1.

Run: `grep -c "Discovery\|Requirements\|Design\|Implementation\|Verification\|Deployment\|Maintenance" "C:/Users/BIRDC/.claude/skills/sdlc-lifecycle.md"`
Expected: ≥ 7.

---

## Task 5: Append to `doc-standards.md`

**Files:**
- Modify: `C:\Users\BIRDC\.claude\skills\doc-standards.md`

- [ ] **Step 1: Inspect end of file**

Run: `tail -5 "C:/Users/BIRDC/.claude/skills/doc-standards.md"`

- [ ] **Step 2: Append exactly this content (with leading blank line)**

```markdown

## Required UX declarations in every document (added 2026-05-06)

Source: synthesis of `book-extractions/branson-ux-ui-design-extraction.md` (personas + affordance), `book-extractions/deacon-ux-ui-strategy-extraction.md` (scope levels), `book-extractions/enterprise-ux-financial-insurance-extraction.md` (maturity).

Every doc-emitting skill must satisfy four short rules. Each rule has an explicit "N/A" escape hatch for cases where the rule does not apply.

### Rule 1 — Persona declaration (Branson)

Every document must name its target persona using Branson's discipline:
- Essential Persona named (single primary persona per role)
- Branson Mechanics floor: name, demographics, goals, environment, pain points, stress points

**N/A escape hatch:** for internal infrastructure documents with no user-facing surface (e.g., a database migration log, a CI configuration), declare explicitly: "Persona: N/A — internal infrastructure document. No user-facing surface."

### Rule 2 — Scope-level declaration (Deacon)

Every document declares which of Deacon's 3 levels of UX scope applies:
- **Single Interaction** — one product/device for one specific task
- **Journey** — multiple channels/devices to achieve a goal over time
- **Relationship** — overall organization-wide experience

**N/A escape hatch:** "Scope: N/A — non-UX document" (e.g., a contract template).

### Rule 3 — Maturity-level declaration (Synechron)

For documents tied to premium-priced engagements, declare the target UX maturity level:
- **Level 3 (UX Design)** — standard premium
- **Level 4 (Experience Design)** — top-tier premium

**N/A escape hatch:** "Maturity: N/A — non-premium engagement" or "Maturity: N/A — non-UX deliverable".

### Rule 4 — Affordance audit (Branson) — UI-emitting docs only

For any document that emits UI (wireframes, screen specs, prototype briefs), declare a 4-stage affordance audit on every primary CTA:
1. **Presence** — does the affordance exist? Yes/No
2. **Visibility / Perceivability** — can it be seen at first glance? Yes/No
3. **Recognizability** — can it be detected without searching? Yes/No
4. **Intelligibility** — is the meaning clear once read? Yes/No

Any No on any stage = redesign required before sign-off.

**N/A escape hatch:** "Affordance audit: N/A — non-UI document".

### Where to place the declarations

Place all four declarations in a **single block at the top of the document**, immediately under the title and before the body. Format:

```
**UX declarations:**
- Persona: [Essential Persona name + Mechanics floor confirmation OR N/A reason]
- Scope: [Single Interaction / Journey / Relationship / N/A reason]
- Maturity: [Level 3 / Level 4 / N/A reason]
- Affordance audit: [Yes — passes 4 stages / No — flagged for redesign / N/A reason]
```

This block is auditable, machine-readable (for skill chains downstream), and visible to every reader.

### Cross-references

- `book-extractions/branson-ux-ui-design-extraction.md` — persona discipline + 4-stage affordance
- `book-extractions/deacon-ux-ui-strategy-extraction.md` — 3 levels of UX scope
- `book-extractions/enterprise-ux-financial-insurance-extraction.md` — maturity model
- `enterprise-ux-process/SKILL.md` — operational skill that produces these declarations as part of its 9-phase workflow
```

- [ ] **Step 3: Verify**

Run: `grep -c "Required UX declarations" "C:/Users/BIRDC/.claude/skills/doc-standards.md"`
Expected: 1.

Run: `grep -c "Rule 1\|Rule 2\|Rule 3\|Rule 4" "C:/Users/BIRDC/.claude/skills/doc-standards.md"`
Expected: ≥ 4.

Run: `grep -c "N/A escape hatch" "C:/Users/BIRDC/.claude/skills/doc-standards.md"`
Expected: 4.

---

## Task 6: Single commit + push

- [ ] **Step 1: Stage and commit**

```bash
cd "C:/Users/BIRDC/.claude/skills"
git add enterprise-ux-process/ ux-standards.md sdlc-lifecycle.md doc-standards.md
git status
git commit -m "$(cat <<'EOF'
~/.claude/skills: populate enterprise-ux-process + extend cross-cutting docs

Phase 2 UX upgrade per spec 2026-05-06-claude-skills-uiux-phase2-design.md.
- New enterprise-ux-process/SKILL.md (9-phase Synechron workflow)
- New enterprise-ux-process/references/maturity-checklist.md (quick-use)
- ux-standards.md: Section 0 added (philosophy + book pointers + 4 cross-cutting rules)
- sdlc-lifecycle.md: UX maturity gate appended (Level 3+ premium-engagement gate)
- doc-standards.md: required UX declarations appended (4 rules with N/A escape hatches)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git log -1 --stat
```

Expected: 5 files changed (2 new + 3 modify).

- [ ] **Step 2: Push to remote**

```bash
cd "C:/Users/BIRDC/.claude/skills"
git push origin main
```

Expected: push succeeds to `peterbamuhigire/skills-web-dev.git`.

---

## Task 7: End-to-end verification

- [ ] **Step 1: Files exist**

```bash
cd "C:/Users/BIRDC/.claude/skills"
test -f enterprise-ux-process/SKILL.md && echo "OK: SKILL.md"
test -f enterprise-ux-process/references/maturity-checklist.md && echo "OK: maturity-checklist.md"
echo "--- Files with 2026-05-06 marker ---"
grep -l "2026-05-06" ux-standards.md sdlc-lifecycle.md doc-standards.md
```

Expected: 2 OK lines + 3 file paths.

- [ ] **Step 2: Concept references**

```bash
cd "C:/Users/BIRDC/.claude/skills"
for f in enterprise-ux-process/SKILL.md enterprise-ux-process/references/maturity-checklist.md ux-standards.md sdlc-lifecycle.md doc-standards.md; do n=$(grep -ciE "Synechron|Branson|Levy|Deacon|Fekeshazi|book-extractions|Maturity|Five Outcomes|Essential Persona|enterprise-ux-process" "$f"); echo "$f: $n"; done
```

Expected: 5 lines, each count ≥ 1.

- [ ] **Step 3: Final report**

Print one paragraph:
- Number of new files (expect 2)
- Number of files extended (expect 3)
- Commit SHA + push status
- Any verification step that did not match expectation

---

## Self-Review

**1. Spec coverage:**
- enterprise-ux-process/SKILL.md → Task 1 ✓
- enterprise-ux-process/references/maturity-checklist.md → Task 2 ✓
- ux-standards.md Section 0 → Task 3 ✓
- sdlc-lifecycle.md UX maturity gate → Task 4 ✓
- doc-standards.md UX declarations → Task 5 ✓
- Commit + push → Task 6 ✓
- Verification → Task 7 ✓

**2. Placeholder scan:** No "TBD"/"TODO"/"implement later"/"add validation" present. Each section has full content.

**3. Type consistency:** Section names ("Section 0", "Phase 1" through "Phase 9", "Rule 1" through "Rule 4") consistent throughout. File paths use forward slashes consistently. The phrase "Essential Persona" capitalized consistently.

No issues to fix.
