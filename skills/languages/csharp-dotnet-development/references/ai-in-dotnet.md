# AI In .NET

Self-contained reference prepared from the supplied AI/.NET source placeholder, broader C#/.NET materials, and current Microsoft AI documentation. Use for .NET apps that call LLMs, embedding models, agents, tools, or RAG systems.

## Table Of Contents

- Choose the integration level
- Semantic Kernel and Microsoft.Extensions.AI
- RAG and embeddings
- Tool/function calling
- Safety and governance
- Testing and observability

## Choose The Integration Level

| Need | Default shape |
|---|---|
| Simple chat or summarization | Typed AI client behind an application service |
| Enterprise workflow with tool use | Semantic Kernel or an explicit orchestration layer |
| Search over private documents | RAG pipeline with chunking, embeddings, vector store, reranking where useful |
| Agentic automation | Tools with authorization, budgets, human review, audit logs, and rollback |
| Multi-provider portability | Adapter around provider SDKs or `Microsoft.Extensions.AI` abstractions |

Keep AI code out of controllers and UI pages. Treat model calls as external dependencies with latency, cost, privacy, and failure modes.

## Semantic Kernel And Microsoft.Extensions.AI

Semantic Kernel is useful when the app needs plugins/tools, prompt orchestration, connectors, telemetry hooks, and enterprise workflow composition. `Microsoft.Extensions.AI` style abstractions are useful when the app needs provider-agnostic chat, embeddings, and dependency-injection integration.

Rules:

- Hide provider-specific SDKs behind interfaces used by application services.
- Keep prompts, schemas, and tool definitions versioned.
- Validate structured model outputs before use.
- Separate model choice from business rules.
- Add cancellation, timeouts, retries, and cost budgets.

## RAG And Embeddings

- Ingest documents with stable IDs, source metadata, timestamps, permissions, and chunk hashes.
- Chunk by semantic structure first, token size second.
- Store embeddings with model/version metadata so re-embedding is manageable.
- Enforce tenant and permission filters before retrieval and again before answer composition.
- Return citations/source references when the workflow depends on evidence.
- Add evaluation fixtures for expected answer, refusal, hallucination, and stale-source cases.

EF Core 10 and SQL Server/Azure SQL vector features can be useful for .NET shops already standardised on SQL Server. Validate index support, query latency, embedding dimensions, and operational cost before choosing database-native vector search.

## Tool And Function Calling

Tool calls are application actions, not text generation. Gate them like APIs:

- Define narrow tools with typed inputs and outputs.
- Validate model-proposed arguments.
- Authorize every action using the real user/tenant context.
- Require human approval for irreversible, expensive, privileged, or externally visible actions.
- Make side effects idempotent where possible.
- Log prompt version, model, tool name, arguments summary, decision, and result.

## Safety And Governance

- Do not send secrets, credentials, or unnecessary personal data to model providers.
- Use data classification to decide which providers and regions are allowed.
- Add prompt-injection defenses for retrieved or user-supplied content.
- Keep system/developer instructions separate from user and retrieved text.
- Enforce output schemas and refusal behaviour for regulated or high-risk decisions.
- Track cost per tenant/user/workflow.

## Testing And Observability

- Unit-test prompt builders, schema validators, and tool authorization.
- Golden-test representative prompts with deterministic settings where available.
- Add regression evaluations for safety-critical flows.
- Log model/provider/version, latency, token usage, refusal, validation failures, and tool calls.
- Use traces to connect HTTP request -> retrieval -> model call -> tool call -> persisted result.

## Anti-Patterns

- Letting a model write directly to the database.
- Treating retrieved documents as trusted instructions.
- Unbounded agent loops.
- No cost limits or rate limits.
- Provider SDK calls scattered through controllers.
- No audit trail for tool calls or generated business decisions.
