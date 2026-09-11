---
name: systematic-bug-diagnosis
description: Use when a defect, regression, intermittent failure, or performance symptom needs evidence-led reproduction and causal diagnosis before a fix; use advanced-testing-strategy to design broader test coverage.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Systematic Bug Diagnosis

Convert a reported symptom into a small red-capable feedback loop, falsify ranked hypotheses, and
return a supported cause or an explicit evidence gap. Diagnosis is read-only by default; fixing is a
separate authorised action.

<!-- dual-compat-start -->
## Use When

- A bug report, regression, flaky test, crash, data discrepancy, latency spike, memory growth, or
  production-only symptom needs diagnosis.
- Several plausible causes exist and changing code before reproducing the symptom would be guesswork.
- A prior fix failed, moved the symptom, or introduced a neighbour regression.

## Do Not Use When

- The task is broad test strategy without a concrete symptom; use `advanced-testing-strategy`.
- The cause is already proved and the user has asked for implementation; route to the owning domain
  skill while retaining the reproduction as a regression oracle.
- Production instrumentation, sensitive data access, or disruptive execution lacks authority.

## Required Inputs

| Input | Required | Missing-input response |
| --- | --- | --- |
| Exact observed symptom and expected behaviour | yes | Clarify or extract from logs/tests before causal claims |
| Environment, version, scope, and first/last known state | yes | Record unknowns and narrow the claim |
| Fastest available reproduction or observation command | preferred | Build one, instrument safely, or stop as `NOT ASSESSED` |
| Recent changes and relevant code/data flow | preferred | Inspect history and boundaries without treating correlation as cause |
| Mutation and production authority | for changes | Remain read-only and return a diagnosis plan |

## Workflow

1. Restate the symptom as observable input, action, actual result, expected result, environment, and
   frequency. Separate reporter interpretation from observed evidence.
2. Establish one deterministic, red-capable loop that can fail for the reported reason and pass when
   the behaviour is healthy. Record command, duration, isolation, and reproduction rate.
   For a structured handoff, run `python scripts/diagnostic_gate.py <record.yml>` from this skill
   directory before asserting a cause or authorising mutation.
3. Minimise the loop while preserving the symptom. Reject mocks, assertions, or fixtures that merely
   restate the implementation.
4. Trace the smallest relevant flow across interfaces, state transitions, logs, data, dependencies,
   and recent changes. Mark every uninspected boundary.
5. Rank falsifiable hypotheses by evidence and cost. For each, name a discriminating observation and
   the result that would reject it.
6. Run one experiment at a time. Prefer read-only inspection; tag temporary instrumentation and
   define removal or retention before adding it.
7. Stop when one cause explains the evidence and alternatives are falsified, or when missing access,
   non-determinism, risk, or environment prevents a supportable conclusion.
8. If fix authority exists, hand the proved cause and red loop to the owning implementation skill.
   Re-run the same loop, neighbour tests, and failure path after the smallest fix.
9. Remove temporary instrumentation, preserve useful regression coverage, and publish the diagnostic
   record, uncertainty, rollback, and follow-up owner.

## Decision Rules

| Condition | Action | Failure avoided |
| --- | --- | --- |
| Loop cannot fail for the reported reason | Repair the oracle before hypotheses | Green tautology |
| Failure is intermittent | Measure reproduction rate and vary one controlled factor | Anecdotal flake claims |
| Symptom exists only in production | Use approved low-risk telemetry or replay; never experiment on users silently | Unsafe live debugging |
| Performance regressed | Fix workload, warm-up, machine, percentile, and comparison boundary | Noisy benchmark conclusion |
| Data may be sensitive | Minimise, redact, aggregate, and record access | Privacy leakage |
| No hypothesis survives | Report disproved hypotheses and next discriminating evidence | Plausible-story diagnosis |
| Cause is proved but mutation is not authorised | Return the fix boundary and regression oracle without editing | Scope expansion |

## Quality Standards

- No causal statement precedes a red-capable reproduction or a clearly labelled observational limit.
- The reproduction tests externally meaningful behaviour and has an independent expected value.
- Commands, environment, duration, rate, evidence locators, and uncertainty are reproducible.
- Experiments change one discriminating factor at a time and record negative results.
- Production diagnostics are proportionate, reversible, privacy-aware, and operator-approved.
- A fix is not accepted until the original loop and relevant neighbour/failure checks pass.

## Anti-Patterns

- Editing the first suspicious line. Fix: establish the red loop and inspect the flow.
- Listing causes without falsification tests. Fix: pair each hypothesis with a rejecting observation.
- A test that copies the same formula or stub as production. Fix: use an independent oracle.
- Adding unbounded logging in production. Fix: scoped, tagged, sampled instrumentation with removal.
- Declaring an intermittent issue fixed after one pass. Fix: compare reproduction rate over a stated run.

## Outputs

| Artifact | Consumer | Acceptance condition |
| --- | --- | --- |
| Diagnostic record | Implementer/reviewer | Symptom, loop, hypotheses, experiments, cause or stop reason, uncertainty |
| Reproduction asset | Test owner | Red-capable, bounded, rerunnable, and linked to expected behaviour |
| Fix handoff or evidence-gap plan | Domain owner | Smallest change boundary, regression checks, permissions, rollback, next evidence |

## Evidence Produced

| Category | Artifact | Format | Example |
| --- | --- | --- | --- |
| Correctness | Reproduction and hypothesis log | Markdown plus commands/results | `docs/diagnostics/INC-142.md` |
| Operability | Instrumentation and recovery record | Markdown/table | tags, sampling, owner, removal and rollback |
| Release evidence | Before/after regression result | Command output or CI link | original red, corrected green, neighbour checks |

## References

- [Tight-loop construction](references/tight-loop-construction.md)
- [Hypotheses and instrumentation](references/hypotheses-and-instrumentation.md)
- [Intermittent, performance, and production cases](references/hard-cases.md)
- [Diagnostic record template](templates/diagnostic-record.md)
- [Machine-checkable diagnostic gate record](templates/diagnostic-record.yml)
<!-- dual-compat-end -->

## Capability Contract

Repository search and read access are required for code diagnosis. Execution is preferred in a
disposable or approved environment. Writes, production telemetry changes, credentials, user-data
access, destructive commands, deployment, and external communication require explicit authority.

## Degraded Mode

If the exact environment, reproduction, logs, data, dependency, or authority is unavailable, return
the observed facts, attempted checks, ranked unresolved hypotheses, safest next observation, and
consequence. Mark causal diagnosis `NOT ASSESSED`; do not fill the gap from familiarity.

## Stop Conditions

Stop before mutation when the symptom is not defined, the oracle is tautological, the experiment can
damage data or users, sensitive access is unapproved, or evidence cannot distinguish hypotheses.

The workflow adapts the tight-loop diagnosis mechanism studied in Matt Pocock's
`mattpocock/skills` repository at commit `3cca18b` and adds Chwezi permission, privacy, degraded-mode,
evidence, and production-recovery controls.
