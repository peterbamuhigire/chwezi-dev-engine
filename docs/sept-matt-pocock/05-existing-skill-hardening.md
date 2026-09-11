# Existing-Skill Hardening Map

## Engineering engine

| Existing owner | Improvement | New file or changed section | Proof required |
| --- | --- | --- | --- |
| `sdlc-meta/skill-writing` | Add context/cognitive load, pointer quality, leading words, completion criteria, lifecycle/invocation | Five references named in `04-new-skills-and-references.md`; update authoring workflow and tests | Positive/negative trigger evals; context-size comparison; adapter consistency |
| `sdlc-meta/skill-composition-standards` | Require explicit invocation ownership and completion criteria for composed workflows | Composition gate and generation template | Fixture where an explicit wrapper cannot be silently invoked by another skill |
| `sdlc-meta/project-requirements` | Replace long fixed interview lists with a decision-tree frontier and facts-versus-decisions split | New frontier interview reference | Same requirements case run before/after; fewer redundant questions with no lost branches |
| `product-business/product-discovery` | Treat prototypes as question-answering primary sources with disposal rules | `prototype-as-primary-source.md` | Three distinct variants or one logic harness; decision and cleanup evidence |
| `architecture/system-architecture-design` | Add ubiquitous language, context maps, ADR conflict handling, and deepening route | Domain context and module-deepening references | Fixture with ambiguous terms and a decision that must become an ADR |
| `sdlc-meta/advanced-testing-strategy` | Add pre-agreed seams, independent expected values, tautological-test detection | Testing-oracle reference | Negative fixture whose test passes by recomputing implementation logic |
| `execution-plan-scripts` | Add tracer-bullet work graph, blocking frontier, and expand-contract exception | Three planning references | Plan fixture with independent slices and a wide rename; graph stays green by stage |
| `sdlc-meta/ai-assisted-development` | Use one bounded issue/slice per worker and compose diagnosis/TDD/review rather than inline them | Workflow and handoff sections | Worker prompts have complete scope, disjoint writes, evidence, and final integration owner |
| `sdlc-meta/git-collaboration-workflow` | Resolve conflicts by intent and primary evidence | Merge-conflict reference | Conflict fixture where neither `ours` nor `theirs` is correct alone |
| `sdlc-meta/implementation-status-auditor` | Prioritise Git hot spots and user harm; apply deletion test before refactor proposals | Architecture audit branch | Candidate report distinguishes cold aesthetic cleanup from high-change friction |
| `sdlc-meta/world-class-engineering` | Add two-axis review and work-graph gate | Review and planning references | Spec-compliant/standards-bad and standards-good/spec-wrong fixtures both fail correctly |
| `sdlc-meta/engine-control-plane` | Add pointer-rich handoff and invocation semantics | Handoff contract | Fresh agent resumes without copied conversation or missing authority |
| `ai/coding-agent-optimization` | Measure description context load and explicit-command cognitive load | Runtime budget section | Exact assembled catalogue measurement for each supported host |
| `ai/ai-agent-multi-agent-coordination` | Add frontier scheduling and one-ticket claims | Coordination decision rules | Parallel fixture has no duplicate claims or dependent work started early |
| `frontend-ux/frontend-architecture` | Use deep-module vocabulary for frontend state/data seams | Reference pointer only | One real feature traced through interface, state, effects, errors, and tests |
| `devops-cloud/deployment-release-engineering` | Add human-operation wizard as a guarded degraded mode | Manual-operation reference | Bash and PowerShell static checks; no secret appears in output; resume is idempotent |

## Current compliance debt to clear first

The comparison is not permission to add more surface while known contract debt remains.

### Portable-contract exceptions

The scanner reports 26 skills with one or more missing requirements:

- 22 missing degraded-mode handling.
- 19 missing a structured input contract.
- 12 missing capability/permission treatment.
- 9 missing decision rules.
- 7 missing the expected portable section set.
- 7 missing at least five domain anti-patterns.

Most exceptions are in `game-development`; five short game skills score 8/14 on the mechanical
contract. Repair by judgement, not boilerplate. Each input, permission, fallback, and output must be
specific to the skill's actual risk and artefact.

### Evidence declarations

The contract gate reports 66 warnings for absent `## Evidence Produced`. Convert these warnings to
errors only after the backlog reaches zero and negative fixtures prove the gate. Highest-risk first:

1. Finance and fiscal routes.
2. AI commercial, compliance, SLA, incident, and tool-action routes.
3. Security, infrastructure, deployment, database operations, and mobile release routes.
4. Game security, build/release, live economy, and online backend.
5. Remaining product and orchestration skills.

### Routing precision

Top-3 routing is complete, but 14 of 158 fixtures do not put the expected skill first. Before adding
new skills, run collision output and classify each top-1 miss as:

- description problem;
- overlapping ownership;
- expected result too narrow;
- valid multi-skill composition.

Add a fixture for every new explicit/implicit invocation boundary and each neighbour pair created by
this programme.

## Email-route hardening completed in this study

The user removed the bundled Tabler email collection. Live references now route HTML email and
newsletter design to the design engine's `email-and-newsletter-design` skill. Engineering retains
lifecycle events, suppression, consent, deliverability, attribution, and operational evidence.

The historical audit and discovery documents still name the removed collection because they record
past repository state. The current decision is documented in
`docs/updates/2026-09-11-email-template-library-removal.md`.

Further email work:

- Correct the design skill's malformed frontmatter continuation (`copy).`) in the design engine.
- Currentness-check hard-coded deliverability thresholds, provider recommendations, DNS examples,
  privacy-law statements, and client support claims before retaining them.
- Add a plain-text alternative, consent-classification test, broken-link test, image-off review,
  dark-mode render, Outlook/Gmail/Apple Mail evidence, and one authored design rationale.
- Never replace the deleted collection with another template dump. Store generated client artefacts
  in the consuming project, not in the canonical skill engine.

## Documentation and catalogue mechanism

Adopt lifecycle states without copying the source's full docs duplication:

```text
active skill -> one canonical SKILL.md
experimental -> non-active incubation root, explicit install only
deprecated -> ALIAS.md plus migration target and removal review date
reference -> deep material reachable from one active owner
```

Generate human catalogue pages from frontmatter and a small curated explanation layer. Hand-write
only decision-rich pages. Add CI checks for lifecycle state, manifest inclusion/exclusion, adapter
existence, and docs ownership.
