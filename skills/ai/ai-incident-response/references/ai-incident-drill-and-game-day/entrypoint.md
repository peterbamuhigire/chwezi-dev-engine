> Consolidated from skills/ai-incident-drill-and-game-day/SKILL.md into ai-incident-response on 2026-05-13. Load this through skills/ai-incident-response/SKILL.md, not as an active skill entrypoint.

# AI Incident Drill and Game Day
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Designing the AI-incident drill program for a multi-tenant SaaS.
- Running a quarterly or monthly game day.
- Onboarding a new on-call engineer or rotation.
- Validating that a runbook update / new operator surface actually works.

## Do Not Use When

- The task is the live incident â€” `ai-incident-response-runbook`.
- The task is generic chaos engineering â€” `reliability-engineering`.
- The task is the eval / red-team â€” `ai-eval-harness`, `ai-prompt-injection-and-tenant-safety`.

## Required Inputs

- Functional detection signals (`ai-incident-detection-and-triage`).
- Functional mitigation primitives (`ai-incident-response-runbook`).
- Functional evidence bundle exporter (`ai-incident-evidence-capture`).
- A staging or shadow environment that can take the simulated load.
- On-call rotation that can spare 90 minutes for a scheduled drill.

## Workflow

1. Read this `SKILL.md`.
2. Pick the **drill scenario** (Â§1) from the catalogue.
3. Prepare the **drill plan** (Â§2) â€” objective, scope, scoring rubric, observers.
4. Inject the **failure** (Â§3) â€” synthetic signal or staged regression.
5. Run the **drill** (Â§4) â€” responders follow live runbook; observers score; do not coach.
6. Run the **debrief** (Â§5) â€” score, lessons, action items.
7. Flow into the **learnings flywheel** (Â§6) â€” drill findings become eng investment.
8. Set the **cadence** (Â§7).
9. Apply anti-patterns (Â§8).

## Quality Standards

- A drill runs at least monthly; sev-1 scenario at least quarterly.
- Every drill produces a scored result and at least one action item.
- Drill findings close within one quarter or are escalated to AI leadership.
- The on-call engineer drilled within the last quarter is the primary responder; not always the same engineer.
- Drill plans rotate the failure class so the team is not pattern-matched to one type.
- Drills include the comms-lead and (occasionally) legal / regulator-notification dry-run.

## Anti-Patterns

- "Drill" is reading the runbook in a meeting â€” not a drill, a review.
- Same scenario every quarter â€” pattern-matched response, no growth.
- Coaches whispering during the drill â€” drills test current state, not state-with-help.
- Observers grade leniently to spare feelings â€” drill findings stop being actionable.
- Action items from drills don't make it into engineering planning â€” flywheel doesn't turn.
- Drills never include comms / legal â€” operational muscle is half the response.
- Drill in production without a kill-switch on the drill itself â€” could become a real incident.

## Outputs

- Drill plan template.
- Scoring rubric.
- Drill scenario catalogue.
- Drill cadence calendar.
- Drill findings register feeding into postmortem-actions tracking.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Operability | Drill plan | Markdown | `drills/2026-05-cost-runaway-plan.md` |
| Operability | Drill scoresheet | Markdown | `drills/2026-05-cost-runaway-score.md` |
| Operability | Drill findings | DB rows | `ai_drill_findings` |
| Operability | Cadence calendar | YAML | `ops/ai/drill-cadence.yaml` |

## References

- `references/game-day-exercises.md` â€” full scenario catalogue with setup, injection, expected response, scoring.
- `references/drill-cadence.md` â€” cadence, rotation, success criteria, escalation.
- Companion: `ai-incident-detection-and-triage`, `ai-incident-response-runbook`, `ai-incident-evidence-capture`, `ai-incident-customer-comms`, `ai-incident-postmortem`, `ai-feature-rollout-and-experimentation`.

<!-- dual-compat-end -->

## Â§1 Drill Scenario Catalogue (Summary)

Full details in `references/game-day-exercises.md`. Scenarios:

1. **Token-cost runaway** â€” a prompt change inflates tokens-per-request 4Ã—; cost-anomaly fires.
2. **Foundation-model deprecation** â€” provider announces 30-day deprecation of pinned model; migration drill.
3. **Prompt-injection via tool output** â€” staged hostile content in a tool's response; observe whether agent obeys.
4. **Retrieval poison** â€” staged hostile content in the index; observe whether retrieval delivers it and whether output filter catches it.
5. **Hallucination spike** â€” staged prompt regression causes a faithfulness drop on a subset; triage to mitigation.
6. **Agent-action incident** â€” staged agent action outside approved scope; observe approval-bypass detection and kill-switch.
7. **Provider outage** â€” staged provider 5xx burst; observe fallback chain activation.
8. **Tool-vendor schema change** â€” staged tool response with a missing required field; observe schema-mismatch detection.
9. **Regulator-notification dry-run** â€” paper drill: confirmed data-exfil scenario; observe whether the 72h GDPR / 15-day EU AI Act clocks are tracked, templates pulled, legal looped in.
10. **Eval drift** â€” staged judge-vs-human kappa drop; observe whether release gates trigger.

## Â§2 Drill Plan Template

```markdown
# Drill plan: <scenario name> â€” <date>

## Objective
What is being tested (specific runbook section, specific primitive, specific signal)?

## Scope
- Environment: staging / shadow-only / synthetic injection.
- Affected features: <list>.
- Affected tenants: <synthetic only>.

## Responders
- Incident commander (primary on-call): <name>.
- Ops-lead: <name>.
- Comms-lead: <name>.
- Scribe: <name>.

## Observers (do not coach)
- AI lead: <name>.
- Engineering manager: <name>.
- Optionally: legal (for regulator drills), CSM (for tenant-comms drills).

## Scoring Rubric
- Time-to-ack target: <value>.
- Time-to-classify target: <value>.
- Time-to-first-mitigation target: <value>.
- Containment-verified within <value>.
- Status-page entry within <value> (if applicable).
- Customer DM within <value> (if applicable).
- Regulator clock noted within <value> (if applicable).
- Evidence bundle exported within <value>.
- Postmortem opened by next business day.

## Drill Kill-Switch
If the drill threatens to become a real incident: <named operator>, <named primitive>, <named verification>.

## Drill Schedule
- T-1 day: brief observers; **do not brief responders**.
- T-0: inject.
- T+90 min: stop drill; begin debrief.

## Debrief Agenda
- Walk the timeline.
- Score against rubric.
- Lessons.
- Action items.
```

## Â§3 Failure Injection

Each scenario has a defined injection method in `references/game-day-exercises.md`. Common patterns:

- **Synthetic signal injection** â€” write a fake row to the metrics store that pages the on-call. No system change.
- **Shadow regression** â€” ship a degraded prompt or model to a shadow run; surface its metrics into the real alert path.
- **Staged data** â€” insert synthetic hostile content into a staging index.
- **Paper drill** â€” read a scenario aloud; responders work in shared doc; no system change.

Always: a **drill marker** is set on the alert so responders see "[DRILL] hallucination_burnâ€¦" â€” eliminates "is this real?" confusion. The marker can be stripped at the observer's discretion for harder drills, but only with prior leadership decision.

## Â§4 Running the Drill

- Start the clock at injection.
- Scribe records every action with timestamp + actor.
- Observers do not coach. They take notes.
- The drill kill-switch is held by a single observer who is **not** an active responder.
- The drill ends at T+90 minutes or when the responders declare "contained + recovery plan drafted".

## Â§5 Debrief

Within 24 hours, run a 60-minute debrief:

- Score against the rubric â€” quantitatively.
- Walk what went well and what didn't.
- Action items: at least one technical + at least one process.
- Note any rubric criterion that wasn't tested â€” schedule a future drill.

Findings go to `ai_drill_findings` with owner + due date.

## Â§6 Learnings Flywheel

- Drill findings join the postmortem action items in the same tracker.
- Monthly aggregate: drill scores trend, action-item closure rate, recurring weak spots.
- Each weak spot drives an engineering investment line item.
- Engineering investment unblocks the next drill to test a deeper layer.

## Â§7 Cadence

See `references/drill-cadence.md`. Summary:

| Scenario class | Cadence | Rotation |
|---|---|---|
| Drill (any class) | monthly | round-robin through scenarios |
| Sev-1 scenario | quarterly | high-impact rotation |
| Tabletop / paper drill | bi-monthly | per failure-class on a rolling list |
| Onboarding drill | once per new on-call | within first 30 days |

## Â§8 Anti-Patterns

- Drill becomes a meeting (review of the runbook).
- Same scenario every quarter; team pattern-matches.
- Drill kill-switch missing or unknown; observers hesitate to invoke when needed.
- Drill scored only by "responders did fine" â€” no rubric, no numbers, no learning.
- Drill findings never enter engineering planning â€” flywheel doesn't turn.
- Drills run only on weekdays at 10am; never test the 02:14 condition.
- Drill briefs responders â€” testing prepared response, not real response.

---

## Â§9 Drills as Compliance Evidence (Enhancement)

Every drill run is captured as **compliance evidence** by `ai-agent-drill-evidence-and-cadence`. Cadence is enforced at the platform level: a missed drill opens a `high` exception and pages the drill owner; persistent miss freezes deploys for the affected component.

What this skill is responsible for: the scenario definitions, the rubric, the post-drill review process.

What `ai-agent-drill-evidence-and-cadence` is responsible for: signed evidence pack per run, cadence policy, enforcer cron, paging, quarterly rollup pack.

Bridge: every scenario in this skill registers in `ops/compliance/drill-cadence.yaml` with its `min_cadence_days`, `pass_threshold`, `owner`, and `control_ids` (the SOC 2 / ISO 27001 / HIPAA controls the drill provides evidence for). A scenario without a cadence registration is not auditable.

Cross-links: `ai-agent-drill-evidence-and-cadence`, `ai-agent-soc2-controls` (CC7.4 incident response), `ai-agent-iso27001-controls` (A.16.1.5, A.17.1.3), `ai-agent-evidence-automation`.

