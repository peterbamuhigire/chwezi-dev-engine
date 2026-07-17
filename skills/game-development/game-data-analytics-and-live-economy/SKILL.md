---
name: game-data-analytics-and-live-economy
description: Use when defining game telemetry, player funnels, retention or progression metrics, experiments, remote configuration, virtual economy sources and sinks, live events, anomaly controls, or ethical data-driven decisions.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Data, Analytics, and Live Economy

Collect the minimum trustworthy game data needed for named decisions, and change live systems through reversible controls.

<!-- dual-compat-start -->
## Use When
- Defining telemetry schemas, KPI/experiment plans, progression/economy simulation, remote config, live events, or anomaly detection.

## Do Not Use When
- Data collection has no stated decision, consent/legal basis, retention, or owner.
- The request seeks manipulative monetisation or fabricated benchmarks.

## Required Inputs
Decision questions, player journey, audience/age and territory, event/version taxonomy, separate Ads/Analytics/vendor identity/privacy/consent models, economy and ad-placement ledgers, cohorts, wellbeing/trust guardrails, experiment rules, data-quality thresholds, remote-config access, rollback/kill switches, and incident owners.

## Workflow
1. Map each question to a metric, event fields, denominator, cohort/window, quality check, owner, and action threshold.
2. Version schemas and validate client/server events for duplicates, loss, ordering, clock skew, bots, test traffic, and late arrival.
3. Model currency/item sources, sinks, balances, caps, prices, grants, refunds, and non-paying paths; reconcile consequential events.
4. Model every ad format/placement with trigger, opt-in/decline, cap/pace, reward, no-fill/error/offline path, audience treatment and removal switch. Never infer consent across SDKs.
5. Pre-register experiments and guardrails; prevent overlapping contamination and stop on privacy, accessibility, child-safety, wellbeing, trust or data-quality failure even when revenue/retention rises.
6. Route remote config, economies, offers, ads and events through approval, typed validation, staged exposure, monitoring, expiry, reconciliation and rollback.

## Quality Standards

- Every metric names its player or operational decision, denominator, version, cohort/window, owner and quality threshold.
- Economy, offer, event and ad changes are reproducible, staged, auditable and reversible.
- Consent, deletion, age treatment and data minimisation are verified separately for each SDK and territory.
- Commercial results are paired with fairness, accessibility, wellbeing, trust and failure-path evidence.

## Decision Rules

| Condition | Action |
|---|---|
| Metric has no named decision or denominator | Do not collect or publish it |
| Engagement rises while regret, harmful spend, inability to stop, sleep disruption, complaints, refunds or child incidents worsen | Stop or roll back; do not call the experiment a win |
| Rewarded ad is technically opt-in but progression makes decline punitive | Classify it as coercive and redesign the economy |
| Consent, deletion or SDK failure path is unverified | Keep collection/ads disabled and return the gap |
| Economy mutation cannot reconcile or reverse | Block remote release |

## Degraded Mode

When consent state, age treatment, network, vendor or telemetry is unavailable, use privacy-minimised defaults, preserve play without ads/analytics where feasible, queue only explicitly permitted operations, and expose a tested kill switch. Mark commercial and behaviour conclusions `not assessed` when data quality fails.

## Anti-Patterns

- Dashboard without a decision. Fix: bind metric, owner, threshold and action.
- Retention as a solitary north star. Fix: pair it with player value, wellbeing, trust and exit measures.
- One privacy toggle for multiple vendors. Fix: map each SDK's data, purpose, consent and deletion separately.
- Live economy edit without version/reconciliation. Fix: stage, audit and rehearse reversal.
- Revenue-positive intrusive ad. Fix: treat interruption or coercion as a blocking product defect.

## Outputs
Measurement plan; event/schema and SDK-purpose registry; data-quality tests; economy/ad-placement model and reconciliation; wellbeing/trust guardrails; experiment record; remote-config/event change log; rollback evidence; qualified decision readout.

## References
- [Live data and economy controls](references/live-data-economy-controls.md)
<!-- dual-compat-end -->
