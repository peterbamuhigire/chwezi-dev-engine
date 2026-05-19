# Strategy Altitude and Guiding Policy

Altitude is the most common silent failure in engineering strategy. A strategy written at the wrong altitude is either too vague to bind decisions or too prescriptive to survive new information. This reference provides operational rules for picking altitude and shaping the guiding policy to match.

## The Four Altitudes

| Altitude | Scope | Time Horizon | Policy Density | Typical Owner |
|---|---|---|---|---|
| Corporate | The whole company; cross-functional | 2-5 years | Low (3-7 clauses) | CEO / CTO |
| Portfolio | A division, a product line, or a platform group | 12-24 months | Medium (5-12 clauses) | VP / Director |
| Product | A single product or major capability | 6-12 months | Medium-high (8-20 clauses) | Senior EM / Staff |
| Component | A system, library, or service | 3-9 months | High (10-30 clauses) | Tech lead / Staff |

Higher altitude means **fewer, more permissive** policies that defer specifics to the next altitude down. Lower altitude means **denser, more prescriptive** policies that close out ambiguity.

### Picking Altitude

Ask three questions, in order:

1. **Who is bound?** If the answer crosses divisions, you are at portfolio or above. If it stays inside one team's repo, you are at component.
2. **What is the smallest change in policy that resolves the diagnosis?** Write at the altitude where that policy lives. Do not write higher to feel more important; do not write lower to feel safer.
3. **What is the cost of being wrong?** High-cost mistakes (years to undo) belong at higher altitude with explicit review loops; low-cost mistakes belong lower, with faster iteration.

### Altitude Mismatch Symptoms

- A corporate-altitude strategy that prescribes a specific framework: too low. Lift the policy and let portfolios choose frameworks.
- A component-altitude strategy that talks about culture: too high. The component cannot enforce culture; rewrite at portfolio altitude or move the concern out.
- A portfolio strategy that names individual on-call rotations: too low. The portfolio sets policy; the team sets the rota.

## Guiding Policy

The guiding policy is the small set of decisions that, once made, eliminate large classes of downstream debate. A good policy:

- **Closes a question.** Reading it makes some prior debate moot.
- **Has a stated reason.** Each clause cites the diagnosis line it follows from.
- **Names a default.** What happens absent further specification.
- **Names an exception path.** Who can grant exceptions and on what evidence.

### Policy Clause Shape

Use this shape for every policy clause:

> *We will <do / not do / require / forbid> <X>, because <diagnosis link>. Default: <Y>. Exception: <named owner> may grant on <evidence>.*

A clause without a default is a slogan. A clause without an exception path is brittle. A clause without a diagnosis link is opinion.

### Policy Density by Altitude

- **Corporate**: 3-7 clauses, each broad. Example: "We will operate one production substrate. Exceptions require CTO approval with a 12-month sunset."
- **Portfolio**: 5-12 clauses, scoped to the portfolio. Example: "Services in this portfolio will use the platform identity layer; bespoke auth requires a documented compliance gap."
- **Product**: 8-20 clauses, including specific patterns. Example: "Background jobs longer than 60 seconds run in the queue tier; synchronous handlers must reject them."
- **Component**: 10-30 clauses, including code and config defaults. Example: "All HTTP clients will set a 5-second connect timeout and 30-second read timeout; deviations require a written justification in the service README."

## Coherent Actions

Coherent actions are the small set of moves that follow from the guiding policy. They are *not* the backlog. Tests for coherent actions:

- **Traceable.** Each action cites the policy clause it implements.
- **Mutually reinforcing.** Each action makes the others easier, not harder.
- **Bounded.** A handful, not a list of everything in flight.
- **Sequenced.** The order matters and is stated.
- **Owned.** Each has a named accountable person and a visible due date.

If the action list could equally well implement a *different* policy, the actions are not coherent — they are activity.

## When Policy Should Be Permissive

Permissive policies allow local variation; prescriptive policies forbid it. Default to permissive when:

- The diagnosis is uncertain and you need teams to learn locally.
- Local context varies enough that a single rule will fit no one well.
- The cost of policy enforcement exceeds the cost of variance.

Default to prescriptive when:

- Variation creates compounding cost (security, identity, data residency, observability schemas).
- Coordination across teams depends on shared interface guarantees.
- The diagnosis points squarely at variance itself as the obstacle.

## Anti-Patterns at the Altitude Layer

- **Altitude inflation.** Writing component policy as if it were corporate strategy. Tell: corporate-sounding prose, no defaults.
- **Altitude collapse.** Corporate strategy that reads like a runbook. Tell: code snippets in an executive memo.
- **Floating policy.** Clauses with no diagnosis link, hovering above any specific problem.
- **Cascade fiction.** Pretending lower altitudes will derive specifics from a vague higher altitude when no one is staffed to do that derivation.
