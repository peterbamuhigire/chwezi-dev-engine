## Codex model and delegation policy

Peter's rule, effective 2026-11-17. Apply only in Codex; this overrides
generic model-class routing. Other hosts retain their models and domain gates.

- Prefer `gpt-6.2-sol` with medium reasoning for root/orchestrator, review and
  execution roles when the active host/account catalogue exposes it. If that
  surface lacks Sol 6.2, use available `gpt-6.1-terra`/medium and report the
  fallback. If neither is available, report the model limitation; do not guess
  a substitute or weaken acceptance checks. An announcement alone is not
  account or tool availability.
- `gpt-6.2-astra`/high is the optional model for Peter's explicit selection on
  demanding tasks. Never escalate to Astra automatically. Preserve a specific
  owner-selected model, including an older Astra session; do not silently
  upgrade it. New defaults do not change a running session.
- Before spawning, check the actual delegation catalogue and role constraints,
  which can differ from the CLI catalogue. Pin each new role to the available
  approved model and reasoning level. If overrides require a no-history fork,
  provide a sufficient bounded brief. Preserve the selected model through
  nested execution. This policy does not itself authorise delegation.
- Give each worker its outcome, context, exact scope, file ownership,
  constraints, acceptance checks and evidence handoff. Parallel writers need
  independent ownership. Keep trivial tasks with the root.
- Disclose missing files, unavailable tools/models, failed calls and other
  blockers promptly, with the affected outcome and next viable step. Record
  worker failures, inspect the cause and narrow or retry safely. Never imply
  delegation, verification or completion without observed evidence.
- Before final delivery, the assigned model reviews the real diff and relevant
  tests, resolves material findings and conflicts, and waits for required
  agents. Missing tests, sources or reviewers remain `NOT_ASSESSED`.
- Every Kaizen checks current official releases AND the active runtime/account
  catalogue. Record dated URLs, model IDs, availability by surface, task fit,
  cost/latency/quality evidence and uncertainty, and a retain/change decision.
  Use the retained research currentness workflow. Vendor benchmarks and API
  token prices do not establish local task savings or subscription charges.
- Keep stable prompt prefixes unchanged where the host supports it; append
  new instructions and task updates. Never let cache optimisation override
  current user instructions, compaction needs, privacy or correctness.
- These defaults remain until Peter authorises a verified replacement. Recheck
  on a release, catalogue or host change. Missing evidence stays `NOT_ASSESSED`.
  Preserve permissions, billing mode, tools, data boundaries and domain gates;
  no model update authorises publishing or administrative changes.

Release evidence checked 17 November 2026:
[OpenAI announcement](https://openai.com/index/introducing-gpt-6-2-astra-sol/).
Account availability must still be checked on the actual execution surface.
