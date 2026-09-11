# New Skills and References

## P0 new active skill: systematic bug diagnosis

Proposed path:
`skills/sdlc-meta/systematic-bug-diagnosis/SKILL.md`

Trigger boundary: hard bugs, performance regressions, intermittent failures, or diagnosis requests
where the cause is unknown. Do not trigger for an already-understood fix or a broad implementation
status audit.

Required workflow:

1. Frame the exact observed symptom, affected actor, environment, severity, and data sensitivity.
2. Build one red-capable feedback loop before proposing a cause.
3. Prove the loop exercises the exact symptom; record command, environment, output, duration, and
   redaction.
4. Minimise until each remaining input or step is load-bearing.
5. Generate three to five falsifiable hypotheses and rank them by evidence.
6. Instrument one prediction at a time; tag and remove temporary instrumentation.
7. Add a regression oracle at the correct seam, then implement only if the request authorises a fix.
8. Re-run the original and minimised loops; test one relevant failure or recovery path.
9. Record cause, fix, rollback, residual risk, and unavailable production evidence.

References to create:

- `references/feedback-loop-catalogue.md`: test, CLI, HTTP, browser, replay, fuzz, bisect,
  differential, and HITL loops.
- `references/minimisation-and-hypothesis-log.md`: delta-debugging, falsifiable predictions, evidence
  updates, and discarded hypotheses.
- `references/production-instrumentation-safety.md`: approval, privacy, cardinality, sampling,
  retention, cleanup, and rollback.
- `references/performance-regression-diagnosis.md`: baseline, profiler, query plan, resource and
  concurrency checks.
- `templates/diagnosis-evidence-pack.md`: symptom, loop, minimised case, hypotheses, probes, cause,
  regression, cleanup, rollback.
- `examples/intermittent-tenant-leak-diagnosis.md`: sanitised end-to-end normal and failure proof.

Acceptance: a hidden fixture must defeat plausible first guesses and pass only when the agent first
constructs a red-capable loop and identifies the evidenced cause.

## P1 conditional active skill: codebase design and deepening

Proposed path:
`skills/architecture/codebase-design-and-deepening/SKILL.md`

Only activate after one catalogue consolidation. It owns interface-level codebase design, not
system architecture, framework architecture, or implementation-status auditing.

Core reference set:

- `references/deep-module-vocabulary.md`: module, interface, implementation, seam, adapter, depth,
  leverage, locality.
- `references/deepening-decision-method.md`: deletion test, interface-as-test-surface, dependency
  categories, internal versus external seams, replace-not-layer tests.
- `references/design-it-twice.md`: independent radically different interface designs, common brief,
  comparison on leverage/locality/seam placement, final synthesis.
- `references/hotspot-selection.md`: use change frequency, incidents, test pain, and user impact;
  avoid refactoring cold code for aesthetics.
- `templates/deepening-candidate-register.md`.
- `examples/order-intake-deepening.md` with before/after interface, tests, rollback, and rejected
  alternatives.

Acceptance: on a fixture with one useful adapter and one speculative wrapper, the skill must retain
the useful seam and recommend deleting the speculative middle layer.

## P1 conditional active skill: domain modelling

Preferred ownership: SRS owns the canonical domain glossary and stakeholder semantics;
`skills-web-dev` owns engineering consumption and implementation-decision linkage.

If SRS already has a sufficient active owner, do not create a duplicate. Instead add an engineering
reference that requires:

- one approved term per concept plus rejected synonyms;
- relationships and invariants, not merely definitions;
- edge-case scenarios that expose ambiguous terms;
- ADR links for decisions that would surprise a future maintainer;
- context maps for genuinely multi-context systems;
- lazy creation only when a term or decision becomes load-bearing;
- conflict handling when code, requirement, and glossary disagree.

## P0 references for skill authoring

Add under `skills/sdlc-meta/skill-writing/references/`:

### `context-pointers-and-attention-budgets.md`

Define pointer identity, positive trigger branches, context load, human cognitive load, pointer
quality, always-load cost, and the rule to inline only when a sharpened pointer still fails.

### `completion-criteria-and-premature-completion.md`

Require every sequential step to end in a checkable, demanding completion criterion. Explain how
visible later steps can pull the model forward and when a real context split is justified.

### `leading-words-and-steering.md`

Explain how compact existing concepts can anchor behaviour; require behavioural evidence before
coining portfolio terminology. Reconcile positive steering with explicit prohibitions needed for
security, finance, privacy, and destructive-action controls.

### `invocation-ownership-and-skill-lifecycle.md`

Define portable semantics for explicit/user invocation, implicit/model invocation, wrappers,
dependencies, incubation, promotion, deprecation, and adapter mapping. Proposed local metadata:

```yaml
metadata:
  invocation: explicit   # or implicit
  lifecycle: active      # or experimental, deprecated, reference
```

Do not standardise these keys until Claude, Codex, and installed host behaviour is tested. Keep
vendor fields in adapters.

### `environment-as-source-of-truth.md`

Identify prose that merely caches config, scripts, package manifests, or directory listings. Keep
the reason and non-obvious convention; retrieve cheap facts from the environment.

## P0 references for execution planning

Add under `skills/execution-plan-scripts/references/` or the retained owner selected after collision
analysis:

- `tracer-bullet-work-graph.md`: complete user-visible slices, blockers, frontier, claim, merge
  point, acceptance evidence.
- `wide-refactor-expand-contract.md`: additive expansion, migration batches sized by blast radius,
  contract/delete phase, integration branch exception, rollback.
- `ticket-and-handoff-contract.md`: outcome, failure consequence, dependencies, owner, acceptance
  oracle, evidence, rollback, unresolved questions.

## P1 references for review and collaboration

- `two-axis-spec-and-standards-review.md` under `world-class-engineering`: independent findings,
  no masking, common fixed point, spec-source resolution, evidence severity.
- `merge-conflict-resolution-by-intent.md` under `git-collaboration-workflow`: map each hunk to
  originating requirement/commit/test, choose intent, verify combined behaviour, preserve abort as
  a safe option.
- `pointer-rich-handoff.md` under `engine-control-plane`: reference artefacts rather than copy them,
  include next action, selected skills, worktree state, blockers, recovery, and redaction.
- `manual-operation-wizard.md` under deployment/admin owners: human-only steps, stage contracts,
  secret handling, idempotence, resume, verification, and disposal.

## P1 references for discovery and design

- `decision-tree-frontier-interview.md`: breadth and depth, fact lookup, dependency frontier,
  recommended answer, confirmation gate, unresolved branches.
- `prototype-as-primary-source.md`: one question, throwaway location, structural variants, real
  content, user reaction, captured decision, disposal and rewrite.
- `expert-questionnaire.md`: sender/recipient frame, knowledge gap, most-important-first questions,
  partial answers, uncertainty, import and decision owner.

Visual prototype work must route to `design-system-skills`; domain content stays with the active
engine. The source's generic Tailwind/Mermaid report is not an approved visual template.
