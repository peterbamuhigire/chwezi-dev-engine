# Agent Governance And Human Oversight

Load when deciding how much an agent may do on its own, who is accountable for
it, how humans stay in control as the number of agents grows, and how that maps
to NIST AI RMF evidence. The autonomy ladder and use-case scorecard already
live in `ai-agent-runtime-architecture/references/agentic-ai-operating-model-source-synthesis.md`;
this file adds the decision rules around them.

## 1. Code-versus-model split (decide per responsibility)

For each responsibility inside an agent, assign it to code or to the model:

| Responsibility needs... | Assign to | Reason |
|---|---|---|
| Consistent rule application, arithmetic, authorisation, limits, sequencing that must not vary | Code | Must behave the same every time and be testable |
| Understanding unstructured input, choosing among tools, drafting, judging ambiguous cases | Model | This is the only reason to have a model |
| Data that must pass between agents without being reinterpreted (IDs, amounts, record references) | Code-carried side channel, not the prompt | Prevents paraphrase and injection of values |

Decision rule: if a component is allowed no discretion at all, it is not an
agent; replace it with a software module. If it is allowed discretion, bound
that discretion with code on both sides.

Two wrapping styles, chosen deliberately:

- **Rules first**: code decides when the model may reason (default for
  regulated, financial and customer-affecting flows).
- **Model first**: the model reasons and code intervenes on defined triggers
  (acceptable for internal, reversible, low-stakes work).

## 2. When to defer to a human, a rule, or the model

Use more than the model's self-reported confidence, which is poorly calibrated.

| Signal | How to measure | Route |
|---|---|---|
| Disagreement across samples | Run the decision several times; measure agreement on the outcome field | Low agreement: rule-based fallback or human |
| Policy trigger | Deterministic: amount, customer tier, irreversible action, regulated data | Human approval |
| Independent check fails | Separate safeguard component or grader, different model or deterministic rules | Block and escalate |
| Novelty | Input far from eval-set distribution, new tool, new tenant | Shadow mode or human |

Calibrate thresholds on the eval set; record the threshold and its evidence in
the agent's registry entry.

## 3. Safeguard components (checks and balances)

- A safeguard reviews another agent's proposed action against policy before it
  executes. Pairing a doer with an independent checker is more reliable than
  instructing one agent to "be careful".
- Independence is the point: different model or deterministic rules, different
  prompt, no ability to be addressed by the doer's output as instructions, and
  its own audit trail.
- A safeguard never replaces deterministic policy for authorisation; it adds a
  layer for judgement-type policy (tone, compliance interpretation, plausibility).

## 4. Human-in-the-loop versus human-on-the-loop

| Mode | Human role | Use when |
|---|---|---|
| In the loop | Approves each gated action before it runs | Irreversible, financial, external, regulated, or new agents |
| On the loop | Monitors live, can pause, override or roll back | Proven, reversible flows with good telemetry |
| Out of the loop | Periodic audit only | Low-impact, reversible, well-evaluated tasks |

Rules: the approval screen shows the exact effect, the evidence and what the
model wrote as its own rationale, labelled as such; approvals are bound to
exact arguments and expire; approval rates, overrides and time-to-decision are
monitored to detect rubber-stamping. See the approval UX references in
`ai-agent-tooling-and-hitl`.

## 5. Accountability and the agent registry

Humans remain accountable for agent actions. Every production agent has a
registry entry:

- owner (named person) and accountable executive;
- task contract, non-goals and autonomy level with promotion evidence;
- tools, scopes and credentials (by reference), data classes touched;
- budgets, kill switch location and last drill date;
- eval set IDs, red-team plan ID, last pass date;
- model and prompt versions, change log;
- review cadence and next review date (controls decay; scopes widen quietly).

No registry entry, no production traffic.

## 6. Scaling from one agent to many

- Specialise: several narrow agents with small contexts are easier to test,
  safeguard and swap models for than one agent with every tool.
- Cost of granularity is latency and spend; stop splitting when an extra hop
  adds no independent test, scope or safeguard.
- Inter-agent messages are typed and authenticated; the receiver re-applies its
  own policy and never inherits authority from message text.
- Put circuit breakers and per-run budgets on the whole graph, not only per
  agent, to stop cascades (`references/ai-agent-cost-and-step-budgets`).

## 7. Where agents are the wrong answer

Decline or keep in assist mode when critical information is tacit or held in
people's heads, when judgement is highly subjective and personal, or when one
mistake costs more than the whole programme saves. Record the decision; it is a
valid outcome of the assessment.

## 8. Organisational readiness check

Rate each Red/Amber/Green before scaling beyond a pilot; any Red blocks scale-up:

1. Leadership alignment on where autonomy ends and humans intervene.
2. Technical foundations: data access, APIs, evaluation and observability.
3. Governance and risk: documented principles, enforcement and a named
   accountable forum.
4. Architecture: modular agents that integrate with legacy systems.
5. Skills: people who can design, evaluate and operate agents.
6. Change management: roles and workflows updated for a mixed human-agent workforce.

## 9. Mapping to NIST AI RMF

| Function | Agent artefacts that evidence it |
|---|---|
| Govern | Registry, owners, risk tolerance, approval policy, review cadence, incident roles |
| Map | Task contract, context of use, affected people, data flow, threat model (OWASP LLM 2025 and ASI 2026 crosswalk) |
| Measure | Eval sets and results, red-team findings, calibration of deferral thresholds, drift monitoring |
| Manage | Controls, budgets, kill switch drills, incident response, rollback, decommissioning |

For generative-AI-specific risks use NIST AI 600-1 as the checklist of risk
areas and suggested actions when writing the Map and Measure artefacts.

## 10. Worked example: district health referral assistant

An agent drafts referral letters from clinic notes for a district hospital.

- Split: the model extracts findings and drafts text; code fills patient
  identifiers, facility codes and dates from the record system.
- Oversight: human in the loop; the clinician signs every letter. Sample
  agreement across three runs below threshold highlights the draft for closer
  reading.
- Safeguard: a rules check confirms that every medication in the draft exists in
  the source note; mismatches block submission.
- Registry: owner is the medical records lead; the agent is never promoted
  beyond assist for clinical content.

## Evidence/currentness

Access date 2026-09-24.

- NIST AI RMF 1.0 (released 2023-01-26; revision announced, not published at access date) and NIST AI 600-1 Generative AI Profile (2024-07-26): nist.gov/itl/ai-risk-management-framework - verified. Revision content `NOT_ASSESSED`.
- OWASP Top 10 for Agentic Applications 2026 (published 2025-12-09): genai.owasp.org - publication verified.
- Sample-agreement deferral is a practice pattern; any specific threshold must come from the project's own eval data (`NOT_ASSESSED` in general).

Sources: Hodjat, B. and Blondeau, A. (2026, early release) *The Agentic Enterprise*; Borges, D. and Campbell, D. (2026, early release) *AI Security Engineering*; Fernandez, O. (2024) *Patterns of Application Development Using AI*; NIST.
