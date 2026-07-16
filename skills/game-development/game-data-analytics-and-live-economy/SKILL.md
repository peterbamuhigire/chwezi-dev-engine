---
name: game-data-analytics-and-live-economy
description: Use when defining game telemetry, player funnels, retention or progression metrics, experiments, remote configuration, virtual economy sources and sinks, live events, anomaly controls, or ethical data-driven decisions.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Data, Analytics, and Live Economy

Collect the minimum trustworthy game data needed for named decisions, and change live systems through reversible controls.

## Use When
- Defining telemetry schemas, KPI/experiment plans, progression/economy simulation, remote config, live events, or anomaly detection.

## Do Not Use When
- Data collection has no stated decision, consent/legal basis, retention, or owner.
- The request seeks manipulative monetisation or fabricated benchmarks.

## Required Inputs
Decision questions, player journey, event/version taxonomy, identity/privacy/consent model, economy ledger/rules, cohorts, experiment guardrails, data quality thresholds, remote-config access, rollback, and incident owners.

## Workflow
1. Map each question to a metric, event fields, denominator, cohort/window, quality check, owner, and action threshold.
2. Version schemas and validate client/server events for duplicates, loss, ordering, clock skew, bots, test traffic, and late arrival.
3. Model currency/item sources, sinks, balances, caps, prices, grants, refunds, and non-paying paths; reconcile consequential events.
4. Pre-register experiments and guardrails; prevent overlapping contamination and stop on harm/data-quality thresholds.
5. Route remote config and events through approval, validation, staged exposure, monitoring, expiry, and rollback.

## Outputs
Measurement plan; event/schema registry; data-quality tests; economy model/reconciliation; experiment record; remote-config/event change log; decision readout.

## References
- [Live data and economy controls](references/live-data-economy-controls.md)

