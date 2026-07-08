# Anti-Slop Governance for Engineering Outputs

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 anti-slop gate
Benchmark: staff/principal-engineer review notes from mature software organisations: specific, evidenced, trade-off aware, and operationally accountable.

This file adapts the repository's `skills/sdlc-meta/anti-ai-slop` guardrail to engineering artifacts.

## Prohibited Patterns

- "Scalable", "secure", "resilient", or "production-ready" without test, architecture, or operational evidence.
- Architecture diagrams or descriptions that do not name data ownership.
- API guidance that omits idempotency, pagination, versioning, error semantics, or compatibility when those are relevant.
- Security sections that name OWASP but do not tie risks to controls and tests.
- Reliability sections that name SLOs but omit the error-budget consequence.
- Release notes that list changes without rollback, monitoring, or support impact.
- Skill docs that duplicate statutory, finance, design, or research doctrine owned by another Chwezi engine.

## Required Engineering Specificity

Every major section must contain at least one of:

- a named entity, service, endpoint, table, queue, role, SLO, test, or source;
- a decision and rejected alternative;
- an edge case and expected behavior;
- a failure mode and release consequence;
- a validation artifact path.

## Language Rules

Use direct engineering prose. Avoid motivational language, vague maturity claims, filler intros, and ritual caveats. If uncertainty remains, name the missing evidence and the decision that depends on it.

## Anti-Slop QA

| Question | Pass condition |
|---|---|
| Could this section apply to any SaaS project? | No; it names the actual domain transaction or artifact |
| Can a reviewer test the claim? | Yes; test, source, path, or decision record is named |
| Does it cover the hard part? | Yes; edge case, failure mode, or rollback appears |
| Does it route external doctrine correctly? | Yes; finance, design, and research engines are linked rather than copied |
| Is the conclusion useful to a decision-maker? | Yes; it names the decision, risk, or release consequence |

## Release Blockers

- Any invented statistic, source, vendor feature, standard version, or statutory value.
- Any deliverable-producing artifact without an evidence pack.
- Any current platform guidance without source-register entry.
- Any UI, document, or visual-formatting instruction that violates the external design-system engine font and visual rules.
- Any finance/statutory guidance hardcoded into this engine.
