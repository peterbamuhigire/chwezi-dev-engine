---
name: ai-rag-patterns
description: Use when building features that answer questions from private data, documents, policies, or time-sensitive information — RAG architecture, chunking strategies, hybrid search, re-ranking, vector databases, evaluation, agentic RAG, multimodal RAG...
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# RAG Patterns — Retrieval-Augmented Generation

## Operating contract

## Inputs

| Input | Required | Purpose |
|---|---|---|
| Domain evidence | yes | question set, authoritative corpus, tenancy and access rules, freshness target, citation needs, and evaluation set |

## Outputs

- Produce: retrieval architecture, ingestion/chunking policy, index and filter contract, grounded-answer schema, and evaluation report.

## Capability and permission boundaries

Default to read-only analysis. Read only scoped records; redact secrets and regulated data. Writes, execution, network calls, production configuration, customer communication, billing changes, and delegation require explicit authority and an identified owner. Never widen tenant, time-window, or system scope implicitly.

## Degraded mode

When required telemetry, evidence, execution, network access, or write authority is unavailable, return a partial result with each unassessed item labelled, preserve the safest existing state, and state the evidence or approval needed to continue. Never convert missing evidence into a pass.

## Decision rules

| Condition | Action |
|---|---|
| Scope, owner, or threshold is missing | Stop the affected decision and request it |
| Evidence is incomplete but read-only analysis is safe | Produce a qualified partial result and gap list |
| A mutation exceeds authority or tenant boundary | Block it and route for approval |
| Evidence meets the stated threshold | Issue the output with provenance and owner |

## Anti-Patterns

- Treating absent evidence as success. Fix: mark the check unassessed and name the missing source.
- Expanding one tenant or workflow to all tenants. Fix: enforce supplied scope at every query and action.
- Performing a production write during analysis. Fix: emit a reviewed change plan until authority is explicit.
- Reporting a metric without population, window, or source. Fix: attach all three.
- Hiding a failed threshold inside an average. Fix: report failure slices and the remediation owner.

Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Use when building features that answer questions from private data, documents, policies, or time-sensitive information — RAG architecture, chunking strategies, hybrid search, re-ranking, vector databases, evaluation, agentic RAG, multimodal RAG...

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | RAG retrieval evaluation report | Markdown doc covering recall / precision / answer-quality on a fixed eval set | `docs/ai/rag-eval-2026-04-16.md` |
| Data safety | Index ingestion + tenancy isolation note | Markdown doc covering chunking, source filtering, and per-tenant index segregation | `docs/ai/rag-tenancy-note.md` |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
<!-- dual-compat-end -->
## Overview

RAG solves the core LLM limitation: they only know what they were trained on. Use RAG to inject private data (invoices, menus, policies, reports) into every AI response.

**Core principle:** RAG = look up a database + LLM synthesises the results. The LLM never needs to "know" your data.

---

## When to Use RAG

| Condition | Action |
|---|---|
| Knowledge base < 200K tokens (~500 pages) | Include everything in context — no RAG needed |
| Knowledge base > 200K tokens | Use RAG |
| Data changes frequently (menus, prices, stock) | RAG (update documents, not model) |
| Data is private/confidential | RAG (keeps data out of training pipelines) |
| Need source citations | RAG (chunks are traceable to source) |
| Model needs brand voice / domain jargon | Fine-tune instead |

---

## RAG vs Fine-Tuning

| Factor | RAG | Fine-Tuning |
|---|---|---|
| Up-to-date content | ✅ Yes (add docs anytime) | ❌ Stale until retrained |
| Hallucinations | ✅ Lower (document-grounded) | ❌ Higher |
| Source citations | ✅ Yes | ❌ No |
| Brand voice control | ❌ Weak | ✅ Strong |
| Domain jargon | ❌ Weak | ✅ Strong |
| Up-front cost | ✅ Lower | ❌ High |

**Default: start with RAG.** Fine-tune only when RAG + prompt engineering cannot deliver the required tone or vocabulary.

---

## Additional Guidance

Guidance is split across two reference files so this entrypoint stays compact.

**[references/skill-deep-dive.md](references/skill-deep-dive.md)** — architecture, chunking, retrieval, schema:

- `Pipeline Architecture`
- `Chunking Strategies`
- `Embedding Model Selection`
- `Vector Database Selection`
- `Retrieval Algorithms`
- `Re-Ranking`
- `Full RAG Query Algorithm`
- `Query Rewriting (Multi-Turn)`
- `RAG Schema (Multi-Tenant)`
- `Evaluation Framework`
- `Production Patterns`
- `Agentic RAG`
- `Multimodal RAG`, `Edge Cases`, `Cost Optimisation`, `Sources`

**[references/production-rag.md](references/production-rag.md)** — the progression from draft to production and the gates before shipping:

- `RAG Maturity Model` — Naive → Advanced → Modular
- `Query Transformation` — HyDE, Multi-Query, Step-Back
- `Contextual Compression`
- `Self-RAG`
- `RAGAS Evaluation` — 4 metrics with production thresholds
- `Embedding Pipeline` — batching, upserts, re-embed triggers, $/1M-token table
- `Cost Management Decision Tree` — concrete dollar figures per branch
- `Failure Mode Playbook` — empty, irrelevant, hallucinated, stale
- `Gates Before Shipping`

Load the production file when building a RAG system that has to pass evaluation gates, survive multi-tenant review, or hit a cost budget under load.
## Multi-Tenant Addendum

This skill describes RAG patterns in general. When the RAG feature ships inside a multi-tenant SaaS, the production answer is `ai-rag-multi-tenant` — per-tenant ingestion pipelines, vector store partitioning, tier-specific chunking and embedding models, defence-in-depth retrieval security, and citation grounding tied to live sources.

Cross-references:
- `ai-rag-multi-tenant` — multi-tenant RAG end-to-end.
- `ai-tenant-isolation-patterns` — vector-store partitioning tradeoffs and data-bleed tests.
- `ai-on-saas-architecture` — KB service as a control-plane service.
- `ai-hallucination-slo-and-grounding` — citation grounding + faithfulness SLO.
- `ai-model-gateway` — gateway-mediated retrieval calls.
- `saas-tenant-data-portability-and-erasure` — KB erasure cascade for embeddings.
## Consolidated Child References

- Load [references/routing.md](references/routing.md) to map retired AI child skill slugs to their reference modules.
