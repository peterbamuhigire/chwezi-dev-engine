# APIs for AI Agents, Data Science, and Model Serving

Parent skill: [`api-design-first`](../SKILL.md). Load this reference when an
API will be called by an LLM agent (directly, as function/tool calls, or via
an MCP server), consumed from notebooks and BI tools, or used to serve a
statistical/ML model. Tool-level naming and description conventions live in
`skills/ai/ai-agent-tooling-and-hitl/references/ai-agent-tool-catalogue-and-action-gating/references/tool-schema-conventions.md`;
MCP server wiring in a web app lives in `skills/ai/ai-web-apps/references/mcp-integration.md`.
This file owns the API-contract side: what the underlying HTTP/MCP surface must
guarantee so agents and data consumers can use it safely.

## Inputs

| Input | Source | If missing |
| --- | --- | --- |
| Consumer research: who calls, for which task, how fresh, read or write | Product / user research | Stop; do not publish tables because they exist |
| Data classification of every field | Data owner / privacy | Block exposure to agents and bulk export |
| Side-effect class of every operation (read, reversible write, irreversible write, spend) | Domain owner | Treat as irreversible |
| Model card or model version policy (for inference APIs) | ML owner | Block model endpoint release |

## Step 1: decide the product before the endpoints

1. Write consumer stories in the form "As a <consumer type>, I need <task>, so
   that <outcome>", then place each on two axes: update frequency (real-time,
   daily, historical) and access (read-only, read-write).
2. Ship the cheapest quadrant that serves real demand first. Read-only daily
   data is typically far cheaper to build and host than real-time read-write.
3. Record rejected stories with the reason (data not retained, legal basis
   missing, cost) so they are not re-proposed as "quick wins".
4. Choose the style with `api-style-selection.md`; REST remains the default
   for data and agent consumers because every notebook, BI tool, SDK
   generator, and agent framework can call it.

## Step 2: data-consumer API rules

| Rule | Why |
| --- | --- |
| Offer bulk export (daily files: CSV/Parquet with a data dictionary) alongside the per-record API | Analysts otherwise page through millions of records and hit rate limits |
| Stable, documented field semantics and units; changes go through versioning | Analysts' pipelines break silently on meaning changes |
| Filter by `updated_since` and return a stable sort key | Enables incremental loads instead of full re-pulls |
| Cursor pagination with stable ordering for large sets | Offset paging skips or duplicates rows under writes |
| Publish an SDK only after the HTTP contract is stable; generate it from OpenAPI and add retries with backoff, pagination iterators, and typed models by hand-review | A hand-written SDK drifts from the contract; a raw generated one is unpleasant to use |
| State data freshness in responses (`meta.as_of`) | Consumers otherwise mistake stale extracts for live data |

## Step 3: model-inference API rules

- Version the model separately from the API: request may pin
  `model_version`; response always echoes `model_version` and `request_id`.
- Return the prediction with its uncertainty or score and the feature
  inputs actually used (after defaults), so consumers can audit.
- Validate inputs against the training domain (ranges, categories); return a
  problem-details error for out-of-domain input rather than a confident
  nonsense prediction.
- Fast predictions: synchronous `POST /v1/predictions`. Slow or batch
  scoring: `202 Accepted` with a job resource and a webhook or polling URL.
- Log inputs and outputs for drift monitoring subject to the data
  classification; never log personal data the consumer was not entitled to.
- Generative endpoints stream tokens with SSE; state token and cost limits
  per call and per tenant (OWASP API4).

## Step 4: agent-consumer API rules

Agents read your descriptions as instructions and your errors as feedback.
Design for a caller that is literal, tireless, and can be manipulated by text
it reads elsewhere.

1. **Task-shaped operations.** Expose `invoice_create_draft`,
   `invoice_send_for_approval`, not `POST /sql` or a generic `execute`.
   One operation, one business intent, one side-effect class.
2. **Separate reads from writes.** Never combine lookup and mutation in one
   operation; an agent exploring should never mutate by accident.
3. **Closed, bounded input schemas.** JSON Schema 2020-12,
   `additionalProperties: false`, enums over free text, bounded strings and
   arrays, IDs that come from a prior lookup operation.
4. **Structured, bounded outputs.** Declare an output schema; return
   structured data plus a short human-readable summary; truncate with an
   explicit `truncated: true` and a cursor rather than dumping megabytes into
   the model context.
5. **Errors the model can act on.** Validation and business errors carry the
   field, the rule, and the acceptable range ("due_date must be on or after
   2026-09-24"); protocol failures are separate from business failures.
6. **Idempotency and dry runs.** Side-effecting operations accept an
   idempotency key; offer `validate_only` / preview so an agent can show the
   user what will happen before committing.
7. **Explicit state handles.** Cross-call state (a basket, an open import, a
   draft) is an opaque, expiring handle returned by a create operation and
   passed back as an argument. Authorise the caller against the handle on every
   call; state the expiry in the operation description.
8. **The model is never the authoriser.** Authorisation uses the end user's
   delegated credential (OAuth scopes) evaluated server-side on every call.
   Tool descriptions, annotations, and model output are not security controls.
9. **Human confirmation for irreversible or spending actions.** Enforce it in
   the application flow (approval step, signed confirmation), not by asking the
   model to ask.
10. **Treat returned content as untrusted.** Data returned by your API can
    carry prompt-injection text (a customer note saying "ignore previous
    instructions"). Mark free-text fields as user content, keep them out of
    instruction positions, and never let returned text widen permissions.
11. **Deterministic listings.** Return the tool/operation list in a stable
    order and cache it; changes are versioned like any contract change.

### MCP-specific rules (specification 2026-07-28)

- MCP is now stateless: no `initialize` handshake and no protocol session
  (`Mcp-Session-Id` removed); every request carries protocol version and client
  capabilities in `_meta`; servers implement `server/discover`. Do not design
  servers that depend on per-connection state; use explicit handles (rule 7).
- Tool `inputSchema` and `outputSchema` default to JSON Schema 2020-12. For a
  tool with no parameters use `{"type": "object", "additionalProperties": false}`.
- Tool names: 1-128 characters from `A-Z a-z 0-9 _ - .`, case-sensitive,
  unique per server. Prefix by domain to avoid collisions in multi-server hosts.
- Return `structuredContent` conforming to `outputSchema` and also a text
  block with the serialised JSON for older clients.
- Use `isError: true` tool results for business and validation errors the
  model can fix; use JSON-RPC errors only for protocol faults (unknown tool,
  malformed request).
- Annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`,
  `openWorldHint`) are hints. Clients must treat them as untrusted unless the
  server is trusted; set them accurately anyway because hosts use them for
  approval UX.
- Mid-call user input uses the Multi Round-Trip Request pattern
  (`resultType: "input_required"` with `inputRequests`, client retries with
  `inputResponses`). Roots, Sampling, and Logging are deprecated; the old
  HTTP+SSE transport is deprecated in favour of Streamable HTTP.
- Do not mirror sensitive parameters into HTTP headers with `x-mcp-header`;
  intermediaries can read them.
- Server obligations from the spec: validate all tool inputs, enforce access
  control, rate limit invocations, sanitise outputs.

## Original worked example: cooperative produce-price API for agents

A Mbarara dairy cooperative exposes milk collection data to an extension
officer's AI assistant and to analysts.

| Surface | Design |
| --- | --- |
| Analysts | `GET /v1/collections?updated_since=...&cursor=...` plus a nightly Parquet export with a data dictionary; `meta.as_of` on every response |
| Agent read tool | `collection_summary_get(farmer_id, month)` returns litres, fat percentage, payout in UGX as a decimal string, `readOnlyHint: true` |
| Agent write tool | `payout_adjustment_propose(farmer_id, amount, reason)` creates a draft only; an approved human confirms in the cooperative app; `destructiveHint: false`, `idempotentHint: true` with an idempotency key |
| Rejected | `payout_send` as an agent tool: irreversible mobile-money spend without human approval |

## Premium vs generic output

| Generic AI output | Senior-grade output |
| --- | --- |
| Wraps every database table as a tool | Consumer-researched, task-shaped operations with read/write separation |
| "The agent will ask the user before deleting" | Server-enforced approval step and scoped delegated credentials |
| Free-text tool results of unbounded size | Output schema, bounded size, truncation marker, cursor |
| Describes MCP sessions and `initialize` | Uses the stateless 2026-07-28 model with explicit handles |

## Quality gate

- [ ] Consumer stories and quadrant decision recorded; rejected stories kept with reasons.
- [ ] Every agent-callable operation has a side-effect class, closed input schema, output schema, and bounded output.
- [ ] Irreversible and spending operations require a server-enforced human approval.
- [ ] Authorisation uses the user's delegated scopes per call; tested with a prompt-injected record.
- [ ] Model endpoints echo `model_version` and reject out-of-domain inputs with problem details.
- [ ] MCP servers (if any) validated against the 2026-07-28 specification; older-client behaviour `NOT_ASSESSED` unless tested.

## Evidence and currentness

Accessed 2026-09-24:

- modelcontextprotocol.io/specification/latest resolves to revision 2026-07-28 (previous 2025-11-25). The changelog records removal of protocol sessions and the initialise handshake, `server/discover`, `subscriptions/listen`, the Multi Round-Trip Request pattern, required `resultType`, 2020-12 schema loosening for tool schemas, and deprecation of Roots, Sampling, Logging, and the HTTP+SSE transport. `ToolAnnotations` fields confirmed in the published `schema.ts` for 2026-07-28.
- SDK support for 2026-07-28 varies by language and version; verify the SDK changelog before coding. The snippet in `mcp-integration.md` predates this revision (`NOT_ASSESSED` against it).
- PyPI: FastAPI latest 0.141.1 (requires Python 3.10+); Pydantic latest 2.13.5 (2026-08-28). Correction: book examples pin FastAPI 0.103 and Pydantic 2.3; do not copy those pins. FastAPI remains 0.x, so pin exact versions and read release notes before upgrades.
- Correction: some sources invert the terms; serialisation converts in-memory objects to JSON text, deserialisation parses JSON into objects.
- Survey figures on API-style popularity quoted in books (2023) are dated; do not cite them as current.

Sources: Day (2024, early release) *Hands-On APIs for AI and Data Science*; Dynowski and Dulak (2025) *Learning API Styles*; Model Context Protocol specification 2026-07-28; OWASP API Security Top 10 2023; engine references `tool-schema-conventions.md`, `mcp-integration.md`.
