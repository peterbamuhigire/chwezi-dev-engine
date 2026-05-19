# LLM Gateway Design — Implementation Reference

This is the implementation companion to `ai-on-saas-architecture/references/llm-gateway-design.md`. Where that file explains *why*, this one is *what to build*.

## Module layout (Python example)

```
gateway/
├── api/
│   ├── http.py             # FastAPI routes
│   ├── sse.py              # streaming responses
│   └── auth.py             # service JWT validation
├── pipeline/
│   ├── resolve_binding.py
│   ├── entitlements.py
│   ├── kill_switch.py
│   ├── rate_limit.py
│   ├── caps.py
│   ├── render_prompt.py
│   ├── safety_in.py
│   ├── retrieval.py
│   ├── provider_call.py
│   ├── safety_out.py
│   ├── cost.py
│   ├── audit.py
│   └── pipeline.py         # composes the above
├── providers/
│   ├── base.py
│   ├── anthropic.py
│   ├── openai.py
│   ├── bedrock.py
│   └── vllm.py
├── pricing/
│   └── prices.yaml         # checked-in price table
├── prompts/                # references prompt registry service
└── infra/
    ├── redis.py
    ├── pg.py
    └── otel.py
```

## Pipeline composition

```python
from pipeline import (
    auth, resolve_binding, entitlements, kill_switch,
    rate_limit, caps, render_prompt, safety_in,
    retrieval, provider_call, safety_out, cost, audit,
)

PIPELINE = [
    auth.run,
    resolve_binding.run,
    entitlements.run,
    kill_switch.run,
    rate_limit.run,
    caps.run,
    render_prompt.run,
    safety_in.run,
    retrieval.run,
    provider_call.run,
    safety_out.run,
    cost.run,
    audit.run,
]

async def handle(req: GatewayRequest) -> GatewayResponse:
    ctx = Context(req=req)
    for step in PIPELINE:
        try:
            await step(ctx)
        except StepFailure as e:
            return ctx.to_error_response(e)
    return ctx.to_response()
```

Each step reads/writes the `Context`; failure short-circuits with a typed error.

## Price table format

```yaml
# pricing/prices.yaml — checked in; rolled forward when providers re-price
version: 2026-05-01
currency: USD
models:
  anthropic:claude-3.7-sonnet:
    input_per_1k:  0.003
    output_per_1k: 0.015
  anthropic:claude-3-haiku:
    input_per_1k:  0.00025
    output_per_1k: 0.00125
  openai:gpt-4o:
    input_per_1k:  0.005
    output_per_1k: 0.015
  openai:gpt-4o-mini:
    input_per_1k:  0.00015
    output_per_1k: 0.0006
```

Cost calc:
```python
def usd_cost(model, tokens_in, tokens_out):
    p = PRICES[model]
    return (tokens_in / 1000) * p["input_per_1k"] + \
           (tokens_out / 1000) * p["output_per_1k"]
```

When a provider changes pricing, the change lands as a PR with a `applies_from` field — historical cost stays correct.

## Streaming + final envelope

For SSE:

```
event: token
data: {"delta": "Hello"}
event: token
data: {"delta": " world"}
event: done
data: {"request_id": "...", "tokens_in": 24, "tokens_out": 18, "usd_cost": 0.000312, ...}
```

The `done` event is the auditable envelope. If the client disconnects before `done`, the gateway still completes the audit write server-side using best-known token counts (provider headers when available, else token counters from the streamed deltas).

## Failure semantics

| Stage failure | Behaviour |
|---|---|
| auth | 401 |
| entitlement | 403 with upgrade URL |
| kill-switch | 403 `AI_DISABLED` |
| rate limit | 429 + `Retry-After` |
| caps | 429 `quota:*` |
| safety_in (block) | 422 `unsafe_input` |
| provider_call | retry-then-fallback; if all fail → 503 |
| safety_out (block) | response replaced with safe stub; audit records the block |
| cost | hard fail — block response; emit alert |
| audit | hard fail — block response; on-call alert |

The hard-fail policy on cost + audit is deliberate: a gateway that returns a successful response without an audit row is unsafe.

## Lint rule (ban direct SDK use)

Add to repo's lint config:

```python
# .ruff.toml / custom linter
banned_imports_outside_gateway = [
    "anthropic", "openai", "google.generativeai", "boto3.client('bedrock-runtime')"
]
```

PRs touching any service folder that imports a banned package fail CI unless the file is `gateway/providers/*`.

## Backwards compat

Treat the gateway HTTP contract as v1; version every change. When you add a new field, default it. When you remove a field, deprecate for 90 days. Feature teams pin to a major version.
