# Roadmap and Acceptance Gates

## Wave 0: freeze and select

Owner: root/orchestrator.

1. Record exact Git state for every engine in scope.
2. Run each engine's native guardrails and the portfolio runtime-budget validator.
3. Freeze the comparison baseline at 58/100.
4. Run routing collisions and select at least two consolidation candidates before adding active
   skills.
5. Resolve currentness sources for every affected standard, runtime, package, CLI, and provider.
6. Create one work graph with owners, blockers, acceptance evidence, rollback, and re-audit dates.

Exit evidence: baseline report, collision report, source register, selected ownership map, and clean
or explained worktrees.

## Wave 1: attention and diagnosis

Target comparison score: 64.

### Slice 1: skill-writing attention model

- Add the five P0 authoring references.
- Update `skill-writing`, `skill-composition-standards`, and authoring validators.
- Add positive, negative, collision, missing-tool, and explicit-invocation fixtures.

Acceptance:

- A fresh agent can identify what loads always, what loads by branch, and why.
- Pointer descriptions contain one trigger per real branch.
- Sequential workflows have checkable completion criteria.
- Runtime adapters agree on invocation state.
- Context metadata does not exceed the configured budget.

Rollback: remove new metadata enforcement but retain references until host compatibility is resolved.

### Slice 2: systematic diagnosis

- Consolidate one active catalogue slot.
- Add the skill, references, template, and hidden fixture.
- Route diagnosis requests from root and relevant domain skills.

Acceptance:

- Agent refuses unsupported causal claims before a red-capable loop exists.
- Normal bug, intermittent bug, performance regression, missing environment, and production-only
  instrumentation cases all produce the correct action.
- Diagnostic edits occur only when fix authority exists.

Rollback: retain the reference pack under `advanced-testing-strategy` and deactivate the route.

### Slice 3: close current contract debt

- Repair the 26 portable-contract exceptions by risk cohort.
- Add 66 missing evidence declarations.
- Promote evidence warnings to errors only after the backlog is zero.

Acceptance: compliance and contract gates pass in enforcing mode with negative fixtures.

## Wave 2: decisions, work graphs, and review

Target comparison score: 69.

### Slice 4: frontier questioning

- Add the shared SRS-owned frontier reference.
- Integrate it into project requirements and product discovery.
- Add proposal/business-plan/website wrappers only where domain outputs differ.

Measure: branch coverage, redundant-question rate, user corrections, unresolved assumptions, and
time to confirmed scope. Do not optimise only for fewer questions.

### Slice 5: domain language and ADRs

- Establish canonical glossary/context and decision-record ownership.
- Add lazy creation and conflict rules.
- Add a multi-context example and one code-to-requirement disagreement fixture.

Measure: naming consistency in specs, tickets, code, tests, and review findings.

### Slice 6: tracer-bullet work graphs

- Harden execution planning with blocking edges and frontier queries.
- Add expand-contract for wide refactors.
- Test local Markdown, GitHub, and one unavailable-tracker fallback without making external writes.

Measure: independently shippable slices, blocked-work violations, merge conflicts, and context-window
overflow.

### Slice 7: two-axis review

- Separate spec fidelity and engineering standards.
- Add security/evidence overlays after the independent axes report.
- Keep final risk ranking with the orchestrator.

Measure: planted missed requirement and planted standards violation both detected; neither is hidden
by the other axis.

## Wave 3: deepening, prototypes, and portfolio rollout

Target: 75+ only with cross-engine applied proof.

- Pilot codebase deepening on one frequently changed module.
- Run design-it-twice with three independent interface constraints.
- Pilot question-answering prototypes in one website/app flow.
- Add questionnaires and manual-operation wizards to two non-engineering domains.
- Add lifecycle/invocation validation to coordination tooling.
- Re-measure routing, context budgets, diagnosis outcomes, review escape rates, and handoff success.

## Required test matrix

| Capability | Normal case | Failure/counter-case | Evidence |
| --- | --- | --- | --- |
| Invocation | Model auto-loads implicit skill | Explicit skill is not auto-loaded or called transitively | Host-specific trace |
| Frontier interview | Independent decisions asked together | Dependent decision waits for prerequisite | Transcript fixture |
| Domain model | New term is ratified and linked | Unconfirmed term remains proposed | Context/ADR diff |
| Diagnosis | Exact symptom goes red then green | No loop available stops causal speculation | Commands and outputs |
| Work graph | Independent slices form frontier | Blocked slice cannot start | Graph fixture |
| Wide refactor | Expand and batches stay green | Premature contract phase fails | CI history |
| Code review | Both axes pass | One planted defect on each axis is detected | Review reports |
| Prototype | Question resolved and prototype disposed | Similar variants or production mutation rejected | Render and cleanup diff |
| Handoff | Fresh agent resumes | Missing authority or evidence is visible | Resume evaluation |
| Lifecycle | Promoted skill ships | Experimental/deprecated skill excluded | Manifest validator |

## Measurement plan

| Metric | Baseline | Target | Counter-metric |
| --- | --- | --- | --- |
| Routing precision@1 | 91% | >=95% without reducing top-3 | Description characters and collisions |
| Fully portable skills | 153/179 | 179/179 | Boilerplate similarity |
| Missing evidence declarations | 66 | 0 | Evidence specificity and usefulness |
| Active skill count | 179 | 170 or fewer before net additions | Capability loss and alias failures |
| Diagnosis causal claims before repro | Not measured | 0 in fixtures | Time to useful escalation |
| Spec-fidelity planted defects detected | Not measured | 100% fixture set | False-positive rate |
| Fresh-agent handoff completion | Not measured | >=90% representative tasks | Handoff length/context load |
| Currentness overdue entries | At least two identified | 0 | Research maintenance effort |

## Release rule

No wave is complete because Markdown was added. It completes only when the named behaviour is
tested, the relevant route is discoverable, a consuming project demonstrates the result, rollback
is available, and a fresh reviewer accepts the evidence. Missing live/runtime/stakeholder evidence
is `NOT ASSESSED`.
