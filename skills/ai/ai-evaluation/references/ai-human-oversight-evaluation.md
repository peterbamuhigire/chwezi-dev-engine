<!-- Source basis: Designing for AI (early release, chapters 1-4 only); XP 2026 AI-augmented engineering and AI-in-Agile papers. Current legal/platform claims require Digital Research verification. -->

# AI Human-Oversight Evaluation

Use this addendum when an AI feature can recommend, generate, classify, rank,
automate, or trigger an action affecting a person, customer, regulated record,
or production system.

## Evaluation contract

Do not evaluate only model output quality. Separate the system into:

| Layer | Questions | Evidence |
|---|---|---|
| Problem | Is AI necessary, and what non-AI option was rejected? | Opportunity comparison and intended outcome |
| Human | Who relies on, reviews, corrects, contests, or is affected by the result? | Actor/decision map and consent or notice state |
| System | Which policies, tools, retrieval, prompts, queues, and fallback paths surround the model? | System map and dependency contract |
| Model | What model/version, capability, limitations, and evaluation set apply? | Model/version register and eval report |
| Inputs | Which user-provided and inferred data are used, and with what confidence? | Input schema, provenance, privacy and data-quality evidence |
| Outputs | Is the output advice, content, ranking, or an executable action? | Output schema, uncertainty and action boundary |

## Human-control tests

For each material action, test that the product provides the appropriate controls:

- preview before irreversible action;
- explanation of relevant inputs and uncertainty without false precision;
- correction or contest path that does not silently disappear;
- undo, rollback, or safe fallback where technically possible;
- escalation to a named human owner;
- consent, opt-out, or disclosure at the system boundary, not only in copy;
- audit event containing actor, version, decision, override, and outcome.

## Release gate

Add separate metrics for task quality, human acceptance, correction rate,
override rate, harmful failure rate, subgroup performance, latency, cost,
and trust/calibration feedback. A feature cannot promote when the primary metric
improves but a safety, control, accessibility, or subgroup guardrail breaches.
Use offline evaluation, shadow mode, supervised exposure, limited release,
then wider rollout. Monitor input/data shift and outcome drift after release.

## Evidence and limits

Retain the prompt/model/system version, cohort, test set, thresholds, failed
examples, reviewer decision, and rollback result. Do not infer legal compliance
from this reference. The Designing for AI input is an early release with later
chapters unavailable; verify current law, policy, vendor behavior, and standards
through `digital-research-skills`.
