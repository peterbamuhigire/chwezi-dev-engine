# AI-on-Multi-Tenant-SaaS Engineering Skills Audit — May 2026

**Lens:** AI features (RAG, agents, copilots, LLM analytics, autocomplete, summarisation, classification, AI search) built **inside** a multi-tenant SaaS — meaning tenant-isolated, cost-attributed, observable, gated by entitlements, safe (no prompt injection / no leakage / hallucination-bounded), evaluated continuously, and metered for billing.

**Inputs:** The 10 new SaaS skills (`saas-control-plane-engineering`, `saas-tenant-onboarding-automation`, `saas-deployment-models`, `saas-entitlements-and-plan-gating`, `saas-transactional-email-infrastructure`, `saas-lifecycle-email-orchestration`, `saas-admin-backoffice-tooling`, `saas-sso-scim-enterprise-auth`, `saas-tenant-data-portability-and-erasure`, `saas-rate-limiting-and-quotas`) and the 25+ existing `ai-*` skills.

**Prior agents' verdict:** the engine has both an AI stack and a SaaS stack, but **no skill** combines (tenant isolation + per-tenant cost + model gateway + eval + hallucination SLO) into a single coherent engineering discipline. AI features ship single-tenant and then leak, blow budgets, or hallucinate at enterprise customers.

## Existing `ai-*` Skill Audit — Multi-Tenancy Coverage

| Skill | Mentions tenant? | Multi-tenant coverage | Gap |
|---|---|---|---|
| `ai-agentic-ui` | weak | none operationalized | needs per-tenant agent budgets, per-tenant tool allow-lists |
| `ai-agents-tools` | weak | none | needs per-tenant tool gating, tenant-scoped action scopes |
| `ai-analytics-dashboards` | weak | none | needs per-tenant data scope on dashboards |
| `ai-analytics-saas` | partial | tenant-aware data scope mentioned | gap on cost attribution per tenant |
| `ai-app-architecture` | partial (MT module gating mentioned) | architecture-level only | no LLM gateway, no per-tenant model selection |
| `ai-architecture-patterns` | partial (Token Ledger / Budget Guard / Module Gate) | strong on metering; weak on gateway, eval, hallucination | no unifying AI-on-SaaS architecture skill, no model gateway |
| `ai-cost-modeling` | 12 mentions; covers per-tenant cost | strong | missing operational attribution pipeline + real-time spend ceilings |
| `ai-economic-value-engine` | partial | business-value lens | not engineering execution |
| `ai-error-handling` | none | single-tenant | needs MT addendum |
| `ai-error-prevention` | none | single-tenant | needs MT addendum |
| `ai-evaluation` | weak (0 hits) | golden datasets at product level only | no per-tenant golden datasets, no eval CI gate, no drift alarms |
| `ai-feature-spec` | partial | feature-level | no tenant isolation specification template |
| `ai-llm-integration` | 4 mentions; mostly minor | single-tenant integration code | no gateway pattern, no per-tenant routing, no audit logging |
| `ai-metering-billing` | strong | token ledger, per-tenant aggregation | overlaps with `ai-saas-billing`; lacks Stripe metered billing recipe |
| `ai-nlp-analytics` | weak | none | tenant scope on text analytics needed |
| `ai-output-design` | none | UI only | citation/grounding UX needs lifting into dedicated skill |
| `ai-predictive-analytics` | weak | none | tenant scope needed |
| `ai-prompt-engineering` | partial | prompt versioning mentioned | no per-tenant prompt namespaces, no injection threat model |
| `ai-rag-patterns` | 2 mentions (weak) | single-tenant RAG | no per-tenant vector-store partitioning, no retrieval-security pattern |
| `ai-saas-billing` | strong | module gating + token metering | needs cross-link to `ai-usage-metering-and-billing` (new) and Stripe recipe |
| `ai-security` | 5 mentions (weak) | mentions prompt injection, PII scrubbing | no full prompt-injection threat model, no red-team test suite, no tenant-isolation safety pattern |
| `ai-slop-prevention` | none | UI only | not the gap target |
| `ai-ux-patterns` | none | UI only | not the gap target |
| `ai-web-apps` | partial | app-level | no per-tenant model gateway |

## Existing `saas-*` Skill Audit — AI Coverage

| Skill | Has AI extension? | Gap |
|---|---|---|
| `saas-control-plane-engineering` | none — control plane lists 7 services, none AI | **Critical gap.** LLM gateway and AI knowledge-base service are control-plane services. |
| `saas-tenant-onboarding-automation` | none | AI features (knowledge-base ingestion, embeddings, default prompts) belong in the onboarding saga. |
| `saas-deployment-models` | none | Silo vs pool also applies to vector stores, embeddings indexes, fine-tunes. |
| `saas-entitlements-and-plan-gating` | none | AI entitlements (model tier, context length, generations/day) are first-class. |
| `saas-transactional-email-infrastructure` | n/a | not the gap target |
| `saas-lifecycle-email-orchestration` | n/a | not the gap target |
| `saas-admin-backoffice-tooling` | none | Back office needs AI-specific surfaces: see prompt diffs, force model fallback, replay trace, kill-switch a tenant's AI. |
| `saas-sso-scim-enterprise-auth` | n/a | not the gap target |
| `saas-tenant-data-portability-and-erasure` | mentions cascade but no AI stores | **Critical gap.** Embeddings, conversation logs, fine-tunes, eval datasets must be in the erasure cascade. |
| `saas-rate-limiting-and-quotas` | mentions "AI token budget" once | **Gap.** Tokens/min + generations/day + concurrent agent sessions are distinct AI quotas with their own algorithms. |
| `multi-tenant-saas-architecture` | none | AI services are now a tenant-bearing class of services and need explicit isolation pattern guidance. |

## Cross-Cutting Gaps

1. **No unifying AI-on-SaaS architecture skill.** AI feature decisions get made in `ai-app-architecture` (architecture style) and `ai-architecture-patterns` (Token Ledger / Module Gate) but neither encodes the control-plane / application-plane split for AI, the LLM gateway as a control-plane service, or per-tenant model/prompt/KB binding.
2. **No tenant-isolation patterns skill for AI assets.** Vector stores, prompt namespaces, fine-tunes, eval datasets, conversation logs, citation grounding — every one needs isolation guidance equivalent to `multi-tenant-saas-architecture` for transactional data.
3. **No LLM gateway skill.** Provider abstraction, model selection per tier, fallback chains, retries, rate limiting per tenant, request signing, audit logging, regional routing (data residency) — all missing as a coherent control-plane service design.
4. **No per-tenant cost attribution skill.** `ai-cost-modeling` is design-time; `ai-metering-billing` ledgers tokens but is light on operational attribution (token accounting pipeline, anomaly detection, real-time spend ceilings, kill-switch).
5. **No AI-usage-to-Stripe-metered-billing skill.** Tokens / calls / generations → billable units → overage → prepaid credits → Stripe meter records.
6. **No AI entitlements skill.** Plan-tier model selection (Pro gets GPT-4-class, Free gets distilled), context-length limits per tier, request rate per tier, gated agent tools.
7. **No AI eval-harness skill.** Golden datasets per tenant, prompt regression tests, A/B prompt evaluation, judge-LLM patterns, eval CI gate before deploy, drift detection.
8. **No hallucination SLO skill.** Citation grounding as product feature, "I don't know" thresholds, retrieval-rerank cutoffs, max-allowed-hallucination-rate SLO, incident response.
9. **No prompt-injection / tenant-safety skill.** `ai-security` mentions injection at a checklist level; the engine lacks a threat model, instruction hierarchy, output content filtering, jailbreak detection, red-team test patterns.
10. **No AI feature rollout / experimentation skill.** Flags for AI features, % rollout, auto-rollback on quality regression, canary cohorts, tenant-level opt-out/consent.
11. **No AI observability skill.** Prompt/response tracing, semantic logging, replay tools, "show me why", cost-per-trace, latency-per-stage, ticket→trace tie-back.
12. **No multi-tenant RAG skill.** Per-tenant ingestion pipelines, chunking per tier, embedding model per tier, partitioning, retrieval security, citation UX.

## NEW SKILLS (12)

| # | Skill | Purpose |
|---|---|---|
| 1 | `ai-on-saas-architecture` | Unifying architecture skill: control-plane bindings for AI (per-tenant models, prompts, KBs, eval datasets); application-plane patterns; LLM gateway as control-plane service. |
| 2 | `ai-tenant-isolation-patterns` | Per-tenant vector stores vs shared+filtered; prompt namespaces; fine-tunes vs adapters; leakage prevention; data-bleed tests. |
| 3 | `ai-model-gateway` | LLM-routing service: provider abstraction, model selection per tier, fallback chains, per-tenant rate limiting, request signing, audit logging, regional routing. |
| 4 | `ai-cost-per-tenant-attribution` | Token accounting pipeline, model price tables, cost-per-tenant dashboards, anomaly detection, plan-cost guardrails, real-time spend ceilings, kill-switch. |
| 5 | `ai-usage-metering-and-billing` | Tokens/calls/generations → billable units; overage; prepaid credits; fair-use ceilings; Stripe metered billing integration. |
| 6 | `ai-entitlements-and-feature-gating` | Gating AI features by plan tier; model selection by tier; context-length limits; request rate; gated agent tools. |
| 7 | `ai-eval-harness` | Golden dataset construction per tenant; prompt regression; A/B prompt eval; judge-LLM patterns; eval CI gate; drift detection. |
| 8 | `ai-hallucination-slo-and-grounding` | Citation grounding as product feature; "I don't know" thresholds; rerank cutoffs; hallucination SLOs; incident response. |
| 9 | `ai-prompt-injection-and-tenant-safety` | Threat model for multi-tenant prompts; input sanitisation; instruction hierarchy; output filtering; jailbreak detection; red-team test patterns. |
| 10 | `ai-feature-rollout-and-experimentation` | Feature flags for AI; % rollout; auto-rollback on quality regression; canary cohorts; tenant-level opt-out / consent. |
| 11 | `ai-observability-and-debugging` | Prompt/response tracing; semantic logging; replay tools; "show me why"; cost-per-trace; latency-per-stage; ticket→trace tie-back. |
| 12 | `ai-rag-multi-tenant` | Multi-tenant RAG specifically: per-tenant ingestion, chunking by tier, embedding model by tier, partitioning, retrieval security, citation UX. |

## ENHANCEMENTS TO EXISTING SKILLS

| Skill | Enhancement |
|---|---|
| `ai-rag-patterns` | Add multi-tenant addendum + cross-link to `ai-rag-multi-tenant`. |
| `ai-llm-integration` | Add cross-link to `ai-model-gateway` (gateway pattern as the production answer). |
| `ai-evaluation` | Add cross-link to `ai-eval-harness` (per-tenant goldens, CI gate). |
| `ai-cost-modeling` | Add cross-link to `ai-cost-per-tenant-attribution` (operational pipeline). |
| `ai-saas-billing` | Cross-link to `ai-usage-metering-and-billing`; clarify scope (gating + metering) vs new skill (billable units + Stripe). |
| `ai-metering-billing` | Same cross-link; clarify it is the engineering ledger and the new skill is the commercial-billing recipe. |
| `ai-security` | Cross-link to `ai-prompt-injection-and-tenant-safety` (full threat model + red-team suite). |
| `ai-error-handling`, `ai-error-prevention`, `ai-slop-prevention` | Multi-tenant addendum reference + cross-links. |
| `saas-control-plane-engineering` | Add AI services (LLM gateway, KB service, eval harness, prompt registry) to the control-plane service inventory. |
| `saas-entitlements-and-plan-gating` | Cross-link to `ai-entitlements-and-feature-gating`. |
| `saas-tenant-data-portability-and-erasure` | Add AI-specific erasure: embeddings, fine-tunes, conversation logs, eval data, prompt logs. |
| `saas-rate-limiting-and-quotas` | Add AI-specific quotas (tokens/min, generations/day, concurrent agent sessions). |
| `multi-tenant-saas-architecture` | Add AI services isolation pattern reference. |

## RECOMMENDED NEXT-SESSION GAPS

- `ai-fine-tuning-and-adapter-engineering` — when to fine-tune per tenant vs use shared base + adapters; LoRA/PEFT operations; eval gates before promotion.
- `ai-data-residency-and-regional-ai` — model availability per region; embeddings region pinning; cross-border-data avoidance.
- `ai-agent-safety-and-action-scopes` — tool allow-lists per tenant; reversible action gating; multi-step plan approval.
- `ai-customer-support-copilot` — vertical skill for the support agent class of AI features.
- `ai-knowledge-base-ingestion-pipelines` — beyond RAG, the ingestion side as its own dedicated skill (currently inside `ai-rag-multi-tenant`).
- `ai-model-card-and-disclosure` — what the SaaS publishes about which models it uses per feature/tier; for regulated buyers.

## Session Execution Status (resume pass complete)

All 12 new skills created with full SKILL.md and dedicated `references/` content. All 15 enhancement targets received an addendum section with cross-links. Reference files written for `ai-on-saas-architecture` (2), `ai-tenant-isolation-patterns` (2), `ai-model-gateway` (2), `ai-cost-per-tenant-attribution` (2), `ai-usage-metering-and-billing` (1), `ai-eval-harness` (3), `ai-hallucination-slo-and-grounding` (2), `ai-prompt-injection-and-tenant-safety` (2), `ai-observability-and-debugging` (1), `ai-rag-multi-tenant` (2). Skills that did not need additional references (`ai-entitlements-and-feature-gating`, `ai-feature-rollout-and-experimentation`) have all material in `SKILL.md`.

Recommended next-session priorities remain those listed above. The engine now covers the full multi-tenant AI engineering discipline: control-plane architecture, isolation, gateway, cost, billing, entitlements, eval, hallucination SLO, prompt-injection safety, rollout/experimentation, observability, and multi-tenant RAG.
