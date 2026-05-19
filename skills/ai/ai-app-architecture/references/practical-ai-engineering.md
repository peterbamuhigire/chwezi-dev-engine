# Practical AI Engineering

This file is self-contained. It was prepared from local EPUB study notes and
must remain useful even if the EPUB is deleted.

Source input: local EPUB `C:\Users\Peter\Downloads\Documents\AI Engineering.epub`.

Use this reference when designing, reviewing, or hardening AI-enabled products.

## Production AI System Shape

Treat the model call as one component in a larger engineered workflow:

1. define the task, user value, and unacceptable failure modes
2. select model, tools, retrieval, memory, and guardrails for that task
3. instrument every call for quality, latency, cost, and safety
4. evaluate with representative examples before release
5. monitor drift, cost, and regressions after release

The architecture should optimise the full loop, not only prompt quality.

## AI Feature Planning

| Question | Required answer |
|----------|-----------------|
| User value | What decision, workflow, or content improves? |
| Failure harm | What happens if the answer is wrong, slow, unsafe, or unavailable? |
| Ground truth | What examples or records define correctness? |
| Latency budget | Is the feature interactive, background, or batch? |
| Cost budget | What is acceptable cost per user, tenant, request, or workflow? |
| Data boundary | What data may be sent to the model or stored in traces? |
| Human role | Who reviews low-confidence or high-risk outputs? |

Set expectations explicitly. AI output is probabilistic; the product must define
when to answer, ask a clarifying question, use a tool, cite uncertainty, or
escalate.

## Evaluation First

Before refining prompts or adding agents, create an evaluation set:

| Evaluation type | Use for |
|-----------------|---------|
| Golden examples | known good responses for common tasks |
| Edge cases | ambiguous, adversarial, malformed, or sparse inputs |
| Regression set | bugs that must never return |
| Human rubric | subjective quality, helpfulness, tone, or compliance |
| Automated checks | schema validity, citation coverage, forbidden content, latency, cost |

Every AI feature should have a release threshold and a rollback trigger.

Evaluation criteria to consider:

- task success / functional correctness
- instruction following
- factuality and source grounding
- completeness and concision
- format/schema validity
- refusal correctness
- safety/policy compliance
- latency and cost
- robustness to ambiguous, adversarial, multilingual, or low-context input

AI-as-judge can help triage, but it must be calibrated with human-reviewed
examples and spot checks. Do not let a judge model be the only release gate for
high-risk domains.

Model selection process:

1. Define evaluation set and rubric.
2. Run candidate models with the same prompts/tools/context.
3. Compare quality, cost, latency, context length, structured-output reliability,
   safety behaviour, and operational constraints.
4. Choose the cheapest model that clears the release threshold.
5. Re-run the regression set on prompt, model, retrieval, and tool changes.

## RAG Design Checks

- Retrieval quality beats prompt length. Inspect misses, near misses, and noisy
  chunks before changing models.
- Chunk by semantic unit where possible: section, policy, API endpoint, decision,
  or example. Avoid arbitrary splitting that destroys context.
- Store metadata that supports filtering: tenant, source, version, author,
  date, access rights, document type.
- Evaluate retrieval and generation separately. A good answer can hide bad
  retrieval; bad generation can hide good retrieval.
- Enforce access control before retrieval results reach the model.
- Include freshness strategy: re-index trigger, stale-source warning, and source
  version in answer metadata.

RAG failure modes:

| Failure | Symptom | Fix |
|---------|---------|-----|
| missing source | answer omits known fact | improve ingestion, chunking, metadata filters |
| noisy retrieval | answer cites irrelevant content | tune ranking, filters, chunk size, reranker |
| stale source | answer uses outdated policy | version sources and re-index on change |
| access leak | user sees forbidden information | enforce ACL before retrieval and at display |
| weak synthesis | retrieved facts are right but answer is bad | improve prompt, structure, or model |

Retrieval metrics:

- recall at k for known-answer examples
- precision/noise rate in top results
- citation coverage
- freshness lag
- access-control violations
- answer quality conditioned on retrieval success

## Agentic Workflow Checks

- Use agents only when the task needs planning, tool use, or multi-step state.
  A direct model call or deterministic workflow is cheaper and easier to verify.
- Give tools narrow schemas and explicit permission boundaries.
- Require checkpoints before irreversible actions: sending email, spending
  money, changing production data, deleting data, or contacting users.
- Log plan, tool calls, observations, final answer, cost, and user-visible state.
- Detect loops with maximum step count, repeated-tool-call guard, and timeout.
- Prefer deterministic code for validation, parsing, calculations, and policy
  checks.

Agent design table:

| Need | Use |
|------|-----|
| one-shot answer over prompt context | direct model call |
| answer over private/fresh docs | RAG |
| structured extraction/transformation | model call plus schema validation |
| deterministic calculation or policy | code/tool, not free-form model reasoning |
| multi-step external action | agent loop with tool permissions and checkpoints |
| high-risk decision | model assistance plus human approval |

Agent logs must reconstruct what happened: user request, plan, tool calls,
tool results, model outputs, validation failures, approvals, and final state.

## AI Safety and Product Fit

- Define user-visible confidence behaviour: answer, ask a question, cite
  uncertainty, escalate, or refuse.
- Design fallbacks for model outage, tool outage, low retrieval confidence, and
  schema validation failure.
- Separate safety filters from business rules. Both must be testable.
- Make cost controls tenant-aware: feature gates, per-feature budgets, alerts,
  and abuse throttles.
- Do not treat "human in the loop" as a vague safety net. Specify who reviews,
  when, with what evidence, and how feedback updates the system.

Guardrail layers:

- input: classify task, detect injection, redact or block sensitive data
- retrieval: enforce permissions and source filters
- tool: restrict schemas, permissions, rate, and irreversible operations
- output: validate schema, citations, policy, PII, and unsafe advice
- UX: show uncertainty, source links, review state, and undo/approval controls
- operations: monitor abuse, cost spikes, drift, model/provider outages

Latency and cost controls:

- stream interactive answers when full validation is not required first
- cache exact safe responses and retrieval results where tenant isolation allows
- route simple tasks to cheaper/faster models
- summarise or compress context only after measuring quality impact
- set tenant/user/feature budgets and alert thresholds
- record token usage and cost for every model call

Feedback loop:

1. Capture user rating, edit, rejection reason, escalation, and task outcome.
2. Separate product feedback from model-quality feedback.
3. Add confirmed failures to regression tests.
4. Review drift periodically by segment, tenant, language, and source corpus.
5. Use feedback to improve prompts, retrieval, tools, UX, or policy before
   considering fine-tuning.

## Output Upgrade

When producing an AI architecture, include:

- task and failure-mode definition
- evaluation plan and release thresholds
- retrieval/tool/agent decision rationale
- guardrail and fallback design
- telemetry, cost ledger, and incident response path

Also include:

- model selection rationale and fallback model/provider
- evaluation dataset shape and minimum pass thresholds
- prompt/version registry expectations
- data retention policy for prompts, traces, embeddings, and feedback
- human review workflow for high-impact decisions
