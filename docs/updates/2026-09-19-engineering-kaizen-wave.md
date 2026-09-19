# Engineering Kaizen wave - 2026-09-19

This bounded wave implements the assigned engineering-owned slices from
B01-A01, B01-A02, B29-A01, B29-A03 and B30-A02. It extends the existing
approval gate and adds provider-neutral pure utilities under `tools/ai/`.

The shared-context packet is `shared-context.v1`; it hashes and renders the
same scoped snapshot for agent and reviewer and blocks stale, missing,
mismatched-objective, scope-mismatched and revoked context. The prompt card
preserves trusted instructions and untrusted data boundaries and returns a
replay hash. Tool calls carry argument provenance and bind consequential
approval to the exact payload hash. The approval gate now supports hard
step/cost/time limits, pause and circuit-breaker state, and rejects changed
payloads under a reused idempotency key. The planner returns deterministic
legal paths or explicit rejection/no-plan/budget results without executing
side effects.

Validation commands:

```powershell
python -X utf8 -m unittest tests.test_approval_control_plane tests.ai.test_shared_context tests.ai.test_prompt_context tests.ai.test_tool_provenance tests.ai.test_deterministic_planning
python -X utf8 scripts\validate_engine_control_plane.py --workspace-root C:\wamp64\www --engine skills-web-dev
python -X utf8 scripts\routing_smoke_test.py
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
```

The tests use synthetic fixtures. Host authentication, durable state,
provider/model currentness, live tool execution, production kill-switch
latency, and independent human review remain `NOT_ASSESSED`.
