# AI Trace Schema — Reference

OTel-aligned span names and attributes for AI requests.

## Spans

```
ai.gateway.request                      [root]
├── ai.auth
├── ai.binding.resolve
├── ai.entitlement
├── ai.kill_switch
├── ai.rate_limit
├── ai.caps
├── ai.prompt.render
├── ai.safety.in
├── ai.retrieval                        [nested children for chunk-level work]
│   ├── ai.retrieval.embed
│   ├── ai.retrieval.search
│   └── ai.retrieval.rerank
├── ai.provider.call
│   ├── ai.provider.call.attempt        [one per retry]
│   └── ai.provider.call.attempt.fallback [one per fallback]
├── ai.safety.out
├── ai.cost
└── ai.audit
```

## Root attributes (`ai.gateway.request`)

| Attribute | Type | Notes |
|---|---|---|
| ai.request_id | string | ulid |
| ai.tenant_id | int | |
| ai.user_id | int | nullable |
| ai.feature | string | namespaced |
| ai.intent | string | semantic intent for analytics |
| ai.prompt_id | string | |
| ai.prompt_version | string | |
| ai.model_requested | string | before fallback |
| ai.model_used | string | after fallback |
| ai.region | string | |
| ai.tokens_in | int | |
| ai.tokens_out | int | |
| ai.usd_cost | double | |
| ai.fallback_used | bool | |
| ai.latency_ms | int | end-to-end gateway time |
| ai.outcome | enum | ok / denied / error |
| ai.denial_reason | string | when denied |
| ai.eval_sampled | bool | |
| ai.grounding_score | double | if computed inline |
| ai.safety_findings_count | int | |
| ai.audit_s3_key | string | payload location |

## Per-stage attributes

`ai.entitlement`:
- `ai.entitlement.checked_keys` (string[])
- `ai.entitlement.denial_key` (string, on deny)

`ai.rate_limit`:
- `ai.rl.bucket_key` (string)
- `ai.rl.tokens_remaining` (int)
- `ai.rl.allowed` (bool)

`ai.retrieval`:
- `ai.retrieval.kb_partition` (string)
- `ai.retrieval.top_k` (int)
- `ai.retrieval.chunks_returned` (int)
- `ai.retrieval.rerank_top_score` (double)
- `ai.retrieval.rerank_cutoff` (double)

`ai.provider.call.attempt`:
- `ai.provider` (string)
- `ai.provider.model` (string)
- `ai.provider.region` (string)
- `ai.provider.status_code` (int)
- `ai.provider.retry_attempt` (int)
- `ai.provider.tokens_in` (int)
- `ai.provider.tokens_out` (int)
- `ai.provider.latency_ms` (int)
- `ai.provider.error` (string, when fail)

`ai.safety.in` / `ai.safety.out`:
- `ai.safety.classifier_version` (string)
- `ai.safety.score` (double)
- `ai.safety.findings` (string[]) — labels only, not content

`ai.cost`:
- `ai.cost.price_table_version` (string)
- `ai.cost.usd` (double)
- `ai.cost.tokens_in` (int)
- `ai.cost.tokens_out` (int)

`ai.audit`:
- `ai.audit.row_id` (string)
- `ai.audit.s3_key` (string)

## Conventions

- Attribute keys are lowercase dot-snake.
- Stable: no rename without a major version of the schema (and a dashboard migration).
- High-cardinality data (prompts, responses) NEVER goes in attributes — only references.
- PII never goes in attributes — only ids and counts.

## OTel example (Python)

```python
from opentelemetry import trace
tracer = trace.get_tracer("llm-gateway")

with tracer.start_as_current_span("ai.gateway.request") as root:
    root.set_attribute("ai.request_id", req.id)
    root.set_attribute("ai.tenant_id", req.tenant_id)
    root.set_attribute("ai.feature", req.feature)
    # ... pipeline stages set their own spans
    root.set_attribute("ai.outcome", "ok")
    root.set_attribute("ai.usd_cost", cost)
```

## Query examples (Honeycomb / Tempo / Jaeger)

- "All requests for tenant 8421 in the last hour"
  → `ai.tenant_id = 8421 AND duration > 0`
- "Slow retrieval"
  → `service.name = "llm-gateway" AND name = "ai.retrieval" AND duration_ms > 1500`
- "Fallback rate by feature"
  → `count(ai.gateway.request) WHERE ai.fallback_used = true GROUP BY ai.feature`
- "Cost top tenants today"
  → `sum(ai.usd_cost) GROUP BY ai.tenant_id ORDER BY desc LIMIT 20`

## Linking to logs and audit

- Trace ID is propagated to the AI audit log row (`ai_requests.trace_id` column).
- S3 payload object metadata includes `trace_id`.
- Support tool: paste `request_id` → look up `trace_id` → open trace.

## Sampling

Default: 100% for AI traces. If volume becomes high (> 5M traces/day per feature):
- Always-on: traces for errors, denials, safety findings, fallbacks, costs > p95.
- Sampled: 10% of the rest.

Never below 100% for safety / cost / fallback events — these are the high-signal traces.
