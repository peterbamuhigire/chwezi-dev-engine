# Game Experiment and Gate Templates

Parent: [Lean Game Product Development](../SKILL.md)

This self-contained reference supplies concise templates for repeatable game experiments and decisions.

## Experiment card

```yaml
experiment:
  id: EXP-###
  decision: "What decision will this evidence change?"
  owner: "Accountable role"
  hypothesis: "For ..., when ..., we expect ..."
  risks_tested: [RISK-###]
  protected_constraints: [cultural, accessibility, privacy, wellbeing, device]
  prototype_scope:
    included: []
    excluded: []
    representative_fidelity: []
  method:
    cohort_or_device_context: ""
    sample_or_run_count: ""
    procedure: ""
    instrumentation: []
    raw_evidence_location: ""
  thresholds:
    pass: ""
    mixed: ""
    fail: ""
    veto: []
  decision_rules:
    pass: go
    mixed: narrow_or_repeat
    fail: pivot_or_stop
  timebox: ""
  build_id: ""
```

## Evidence review

Record facts before interpretation:

| Field | Contents |
|---|---|
| Build/context | Immutable build, device/configuration and test date |
| Participants/runs | Prespecified inclusion/exclusion and completed count |
| Observations | Behaviour, timing, errors and direct artefacts |
| Measures | Result against each threshold; no aggregate hiding vetoes |
| Contradictions | Evidence that supports a competing explanation |
| Method deviations | Any change after start and its consequence |
| Limitations | What this experiment cannot establish |
| Decision | Go, narrow, pivot, repeat or stop with owner/date |

## Gate ladder

### Prototype gate

- The core action is understood without developer coaching.
- The signal supports voluntary replay/continuation without pressure.
- Critical cultural, accessibility and safety vetoes are clear.
- The highest-risk technical assumption has a bounded next experiment.

### Vertical-slice gate

- The player promise appears in one complete session loop.
- Representative art, audio, controls, save/lifecycle and performance are present.
- The production pipeline yields measured throughput and rework.
- Minimum/target devices pass the prespecified sustained scenarios.
- Rights, cultural, privacy and wellbeing dispositions permit expansion.
- Cost and schedule are evidence-based ranges with contingency.

### Production-expansion gate

- High-risk systems and content pipelines are validated.
- Requirements, architecture, test plan and build pipeline reflect the learning.
- Content scale follows measured throughput, not aspirational counts.
- The team can keep mainline playable and recover failed changes.
- Funding/runway covers the next gate plus contingency.

## Engagement experiment pair

Pair every positive-return measure with a pressure/exit measure:

| Positive signal | Guardrail |
|---|---|
| voluntary replay | no prompt manipulation or reward loss |
| curiosity to continue | clear save/quit and non-expiring objective |
| mastery attempts | difficulty/assist access and readable failure |
| emotional attachment | no monetised rescue or guilt |
| longer session | comfort, thermal, battery and self-reported pressure |

A high engagement score never overrides a cultural, safety, privacy, accessibility or wellbeing veto.

## Stop/recovery rules

Quarantine evidence if the build changed mid-test without a new identifier, thresholds changed after results, raw data is missing, participants were coached inconsistently, telemetry exceeded consent, or a veto condition occurred. Preserve the raw record, name the defect and rerun only when the method can be repaired.
