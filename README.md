# Chwezi Dev Engine

Chwezi Dev Engine is the engineering catalogue of the Chwezi skill engines: 167 routed `SKILL.md` files that tell an AI coding agent, or the engineer directing one, how to design, build, review, secure and operate production software. It covers system and API architecture, relational databases, distributed systems, application and infrastructure security, Python, TypeScript/JavaScript, PHP, Java, C#/.NET, Kotlin and Swift, web, Android, iOS and cross-platform mobile clients, AI and agent systems, multi-tenant SaaS and ERP platforms, DevOps and cloud delivery, game development, GIS, and the product and commercial decisions around software. A root baseline, [`world-class-engineering`](skills/sdlc-meta/world-class-engineering/SKILL.md), applies to every change: small, explained changes, explicit failure handling, evidence scaled to risk, and a verify-before-done gate. The engine applies published standards where the work calls for them, including the OWASP Top 10 2025, OWASP ASVS 5.0.0, the OWASP Top 10 for LLM Applications and API Security Top 10, ISO/IEC 27001:2022, SOC 2 Trust Services Criteria, PCI DSS v4.0.1, the NIST AI RMF, ISO/IEC 42001:2023, the EU AI Act, GDPR and Uganda's Data Protection and Privacy Act 2019, WCAG 2.2 AA, OpenAPI 3.1, RFC 9457, SLSA v1.2, PSR-12, ISO/IEC/IEEE 29119 and the C4 model. Accounting treatment (IFRS/IAS) is owned by the separate [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine) engine; this engine implements it in software.

The engine produces working engineering artefacts rather than advice: architecture records and C4 diagrams whose claims are pinned to a commit and checked by `verify_diagram_evidence.py`; OpenAPI contracts; database schemas and migration plans; threat models, authorisation matrices, Data Protection Impact Assessments and severity-rated security audit reports; test strategies and Release Evidence Bundles; CI/CD pipelines, Terraform, Docker and Kubernetes configurations; traceable requirements with acceptance criteria and SDLC document sets; AI feature specifications, evaluation harnesses and cost models; game design and production plans; implementation-status audits with completion blueprints; CodeTour onboarding walkthroughs; and validated Word and Excel deliverables. It serves software engineers, technical leads, architects, product owners, QA and delivery reviewers, and the consultants of Chwezi Core Systems, working through Claude Code, Codex or any agent that can read Markdown. Repository tests check the catalogue count, evidence sections and routing fixtures on every change.

## Installation

**Prerequisites.** Git. Node.js 18 or later for the standalone installer (CI uses Node 24). Python 3.11 or later for the Codex model-policy helper; Python 3.12 with `pip install -r requirements-ci.txt` (pytest 9.0.3, PyYAML 6.0.2) to run the validators and tests.

**Claude Code plugin (recommended).** The repository is its own marketplace (`.claude-plugin/marketplace.json`, marketplace `chwezi-engineering`, plugin `engineering`):

```text
/plugin marketplace add peterbamuhigire/chwezi-dev-engine
/plugin install engineering@chwezi-engineering
```

The plugin manifest (`.claude-plugin/plugin.json`) ships the 165 skills under `skills/`, plus `agents/`, `hooks/` and `rules/`. The two project-initialisation skills in `00-meta-initialization/` are read from a clone.

**Standalone installer (no plugin system, or project-local scope).** `install.sh` and `install.ps1` delegate to `scripts/install-engine.js`, which copies skills, agents, hooks and rules into `~/.claude` (`--scope user`, the default) or `./.claude` (`--scope project`) and records every file it writes in `.chwezi/install-state.json`:

```sh
git clone https://github.com/peterbamuhigire/chwezi-dev-engine.git
cd chwezi-dev-engine
./install.sh --scope project --dry-run   # print the plan, write nothing
./install.sh --scope project
```

On Windows PowerShell, run `.\install.ps1 --scope project` (the same flags pass through to the Node installer). `node scripts/install-engine.js uninstall --engine chwezi-dev-engine`, `doctor` and `list-installed` manage an existing install; uninstall removes only files the installer recorded.

**Codex.** Point Codex at the clone; it reads [`AGENTS.md`](AGENTS.md) as the router. Before substantive work, run the bounded model-policy check described in [`.codex/README.md`](.codex/README.md):

```text
python <engine-root>/.codex/ensure_model_policy.py --runtime codex --check
```

Run `--apply` only if the check reports drift. Claude Code skips this step.

**Manual route.** Clone the repository, then have the agent read [`CLAUDE.md`](CLAUDE.md) (which imports `AGENTS.md`), the [skill routing index](docs/skill-routing-index.md), and only the `SKILL.md` files the task needs. Expose `skills/` and `00-meta-initialization/` to the working agent; [docs/USING-IN-A-PROJECT.md](docs/USING-IN-A-PROJECT.md) covers submodule, sibling-clone and read-only-mount wiring.

**Verify.**

```sh
python -X utf8 scripts/skill_catalog_guardrails.py
python -X utf8 -m pytest tests -q
python -X utf8 scripts/routing_smoke_test.py --min-rank1 88 --lint-fixtures
```

## Capabilities

Generated from the active `SKILL.md` files under `skills/` and `00-meta-initialization/`; the 78 inactive `ALIAS.md` redirects are excluded. The root [`SKILL.md`](SKILL.md) is the engineering baseline router and is not counted.

| Category | Folder | Skills |
|---|---|---:|
| Project initialisation | [`00-meta-initialization/`](00-meta-initialization/) | 2 |
| SDLC and engineering method | [`skills/sdlc-meta/`](skills/sdlc-meta/) | 20 |
| Execution planning | [`skills/execution-plan-scripts/`](skills/execution-plan-scripts/) | 1 |
| Architecture | [`skills/architecture/`](skills/architecture/) | 7 |
| Backend and databases | [`skills/backend-databases/`](skills/backend-databases/) | 4 |
| Security | [`skills/security/`](skills/security/) | 6 |
| Languages | [`skills/languages/`](skills/languages/) | 12 |
| Frontend and UX engineering | [`skills/frontend-ux/`](skills/frontend-ux/) | 9 |
| Android | [`skills/android/`](skills/android/) | 1 |
| iOS | [`skills/ios/`](skills/ios/) | 4 |
| Cross-platform mobile | [`skills/mobile-cross/`](skills/mobile-cross/) | 3 |
| AI and agent systems | [`skills/ai/`](skills/ai/) | 26 |
| SaaS platforms | [`skills/saas/`](skills/saas/) | 18 |
| Product and business | [`skills/product-business/`](skills/product-business/) | 15 |
| Finance implementation | [`skills/finance-accounting/`](skills/finance-accounting/) | 4 |
| DevOps and cloud | [`skills/devops-cloud/`](skills/devops-cloud/) | 8 |
| Game development | [`skills/game-development/`](skills/game-development/) | 25 |
| GIS | [`skills/gis/`](skills/gis/) | 2 |
| **Total** | | **167** |

| Category | Skill | What it does |
|---|---|---|
| Project initialisation | [`00-meta-initialization`](00-meta-initialization/SKILL.md) | Selects Waterfall, Agile or Hybrid delivery and generates the governed document sequence for a new project. |
| Project initialisation | [`new-project`](00-meta-initialization/new-project/SKILL.md) | Scaffolds a new project using the engine's new-project workflow. |
| SDLC and engineering method | [`advanced-testing-strategy`](skills/sdlc-meta/advanced-testing-strategy/SKILL.md) | Designs risk-based unit, integration, contract, end-to-end and release-gate test strategy. |
| SDLC and engineering method | [`ai-assisted-development`](skills/sdlc-meta/ai-assisted-development/SKILL.md) | Coordinates AI-assisted planning, implementation and review of AI-generated changes. |
| SDLC and engineering method | [`ai-slop-audit`](skills/sdlc-meta/ai-slop-audit/SKILL.md) | Scores an artefact for AI slop with evidence, severity, fixes and an A/B/C/F verdict. |
| SDLC and engineering method | [`anti-ai-slop`](skills/sdlc-meta/anti-ai-slop/SKILL.md) | Applies real-time anti-slop controls to any human-facing artefact. |
| SDLC and engineering method | [`council`](skills/sdlc-meta/council/SKILL.md) | Convenes a four-voice council for ambiguous trade-offs and go/no-go decisions. |
| SDLC and engineering method | [`doc-architect`](skills/sdlc-meta/doc-architect/SKILL.md) | Generates and repairs AGENTS.md/CLAUDE.md guidance, project docs and CodeTour walkthroughs. |
| SDLC and engineering method | [`engine-control-plane`](skills/sdlc-meta/engine-control-plane/SKILL.md) | Coordinates multi-engine workflows, roles, hooks, evidence contracts and handoffs. |
| SDLC and engineering method | [`git-collaboration-workflow`](skills/sdlc-meta/git-collaboration-workflow/SKILL.md) | Plans branches, commits, reviews, conflict resolution, pull requests and releases. |
| SDLC and engineering method | [`github-ops`](skills/sdlc-meta/github-ops/SKILL.md) | Runs GitHub operations via gh: triage, CI status, releases, alerts and open-sourcing. |
| SDLC and engineering method | [`implementation-status-auditor`](skills/sdlc-meta/implementation-status-auditor/SKILL.md) | Audits real implementation status against requirements and plans with a completion blueprint. |
| SDLC and engineering method | [`kaizen-improvement-system`](skills/sdlc-meta/kaizen-improvement-system/SKILL.md) | Runs evidence-backed baselines, small experiments and re-audits of the engine or its products. |
| SDLC and engineering method | [`project-requirements`](skills/sdlc-meta/project-requirements/SKILL.md) | Interviews stakeholders and produces traceable requirements and acceptance criteria. |
| SDLC and engineering method | [`santa-method`](skills/sdlc-meta/santa-method/SKILL.md) | Requires output to pass two independent adversarial reviewers before it ships. |
| SDLC and engineering method | [`sdlc-documentation`](skills/sdlc-meta/sdlc-documentation/SKILL.md) | Produces and consolidates SDLC documentation from planning to maintenance. |
| SDLC and engineering method | [`skill-composition-standards`](skills/sdlc-meta/skill-composition-standards/SKILL.md) | Enforces house style, boundaries and input/output contracts for skills. |
| SDLC and engineering method | [`skill-engine-audit`](skills/sdlc-meta/skill-engine-audit/SKILL.md) | Audits, grades and benchmarks skill engines and safety-gates new or imported skills. |
| SDLC and engineering method | [`skill-writing`](skills/sdlc-meta/skill-writing/SKILL.md) | Authors and upgrades SKILL.md files with triggers, progressive disclosure and evidence contracts. |
| SDLC and engineering method | [`systematic-bug-diagnosis`](skills/sdlc-meta/systematic-bug-diagnosis/SKILL.md) | Reproduces defects and diagnoses causes from evidence before any fix. |
| SDLC and engineering method | [`world-class-bid-red-team-and-delivery-qc`](skills/sdlc-meta/world-class-bid-red-team-and-delivery-qc/SKILL.md) | Applies the final quality gate to high-stakes bids and consulting deliverables. |
| SDLC and engineering method | [`world-class-engineering`](skills/sdlc-meta/world-class-engineering/SKILL.md) | Sets the production engineering baseline and the verify-before-done gate. |
| Execution planning | [`execution-plan-scripts`](skills/execution-plan-scripts/SKILL.md) | Turns an approved long-running plan into self-contained, ordered execution prompts with checkpoints. |
| Architecture | [`api-design-first`](skills/architecture/api-design-first/SKILL.md) | Designs HTTP APIs with OpenAPI, versioning, auth, idempotency and error contracts. |
| Architecture | [`distributed-systems-patterns`](skills/architecture/distributed-systems-patterns/SKILL.md) | Designs message-driven systems with outbox/inbox, sagas, ordering and idempotency. |
| Architecture | [`ecommerce-platform-audit-requirements`](skills/architecture/ecommerce-platform-audit-requirements/SKILL.md) | Scopes e-commerce platform, payment, security and data-protection audits. |
| Architecture | [`graphql-patterns`](skills/architecture/graphql-patterns/SKILL.md) | Designs GraphQL schemas, resolvers, authorisation, federation and hostile-input controls. |
| Architecture | [`microservices-architecture`](skills/architecture/microservices-architecture/SKILL.md) | Sets microservice boundaries, communication, ownership and resilience. |
| Architecture | [`system-architecture-design`](skills/architecture/system-architecture-design/SKILL.md) | Defines system architecture: bounded contexts, modules, ports and adapters, evidence-pinned diagrams. |
| Architecture | [`validation-contract`](skills/architecture/validation-contract/SKILL.md) | Defines the seven evidence categories and the Release Evidence Bundle for specialist skills. |
| Backend and databases | [`database-design-engineering`](skills/backend-databases/database-design-engineering/SKILL.md) | Designs relational and document data models, tenancy, indexing and migrations. |
| Backend and databases | [`database-reliability`](skills/backend-databases/database-reliability/SKILL.md) | Sets database SLOs, backup verification, capacity policy and on-call practice. |
| Backend and databases | [`mysql-engineering`](skills/backend-databases/mysql-engineering/SKILL.md) | Designs, tunes, backs up, restores and troubleshoots MySQL in production. |
| Backend and databases | [`postgresql-engineering`](skills/backend-databases/postgresql-engineering/SKILL.md) | Designs, tunes, backs up, restores and troubleshoots PostgreSQL in production. |
| Security | [`code-safety-scanner`](skills/security/code-safety-scanner/SKILL.md) | Scans code and agent configuration before deployment for critical vulnerabilities. |
| Security | [`dpia-generator`](skills/security/dpia-generator/SKILL.md) | Produces Data Protection Impact Assessments, including for Uganda DPPA processing. |
| Security | [`linux-security-hardening`](skills/security/linux-security-hardening/SKILL.md) | Hardens and audits Debian/Ubuntu hosts against CIS controls. |
| Security | [`network-security`](skills/security/network-security/SKILL.md) | Designs firewalls, WAF, VPN, TLS/PKI, IDS/IPS, segmentation and DDoS controls. |
| Security | [`vibe-security-skill`](skills/security/vibe-security-skill/SKILL.md) | Produces threat models, abuse cases, authorisation matrices and OWASP-aligned evidence. |
| Security | [`web-app-security-audit`](skills/security/web-app-security-audit/SKILL.md) | Audits PHP/JavaScript web apps for vulnerabilities with a severity-rated report. |
| Languages | [`algorithm-selection-and-complexity`](skills/languages/algorithm-selection-and-complexity/SKILL.md) | Chooses and explains algorithms under explicit correctness and complexity constraints. |
| Languages | [`csharp-dotnet-development`](skills/languages/csharp-dotnet-development/SKILL.md) | Builds and modernises C#/.NET apps: ASP.NET Core, EF Core, MAUI and tests. |
| Languages | [`java-enterprise-development`](skills/languages/java-enterprise-development/SKILL.md) | Builds and modernises Java/JVM services with Spring Boot, Jakarta EE and Hibernate. |
| Languages | [`javascript-modern`](skills/languages/javascript-modern/SKILL.md) | Writes modern JavaScript: modules, async flows, error handling and performance. |
| Languages | [`nodejs-development`](skills/languages/nodejs-development/SKILL.md) | Builds Node.js services, APIs, workers and CLIs with logging, tests and scaling. |
| Languages | [`php-modern-standards`](skills/languages/php-modern-standards/SKILL.md) | Writes PHP 8+ and Laravel code to PSR standards with secure request handling. |
| Languages | [`python-data-analytics`](skills/languages/python-data-analytics/SKILL.md) | Computes KPIs, cohorts, financial maths and statistical tests in Python and pandas. |
| Languages | [`python-data-pipelines`](skills/languages/python-data-pipelines/SKILL.md) | Builds idempotent Python ETL, OCR and document-ingestion pipelines. |
| Languages | [`python-ml-predictive`](skills/languages/python-ml-predictive/SKILL.md) | Adds forecasting, classification and anomaly detection with scikit-learn, Prophet and statsmodels. |
| Languages | [`python-modern-standards`](skills/languages/python-modern-standards/SKILL.md) | Sets the Python baseline, packaging and frozen-executable release builds. |
| Languages | [`typescript-effective`](skills/languages/typescript-effective/SKILL.md) | Writes production TypeScript with strict configuration, migration and testing. |
| Languages | [`typescript-full-stack`](skills/languages/typescript-full-stack/SKILL.md) | Builds end-to-end type-safe TypeScript apps with tRPC/Zod, Prisma/Drizzle and monorepos. |
| Frontend and UX engineering | [`avalonia-desktop-development`](skills/frontend-ux/avalonia-desktop-development/SKILL.md) | Builds cross-platform .NET desktop apps with Avalonia, MVVM and headless tests. |
| Frontend and UX engineering | [`frontend-architecture`](skills/frontend-ux/frontend-architecture/SKILL.md) | Turns design systems and requirements into component, state and delivery architecture. |
| Frontend and UX engineering | [`frontend-performance`](skills/frontend-ux/frontend-performance/SKILL.md) | Sets per-flow frontend performance budgets, measurement plans and CI regression gates. |
| Frontend and UX engineering | [`image-compression`](skills/frontend-ux/image-compression/SKILL.md) | Implements client image optimisation with authoritative server-side validation and re-encoding. |
| Frontend and UX engineering | [`nextjs-app-router`](skills/frontend-ux/nextjs-app-router/SKILL.md) | Implements Next.js App Router server/client components, caching, auth and streaming. |
| Frontend and UX engineering | [`pos-sales-operations-engineering`](skills/frontend-ux/pos-sales-operations-engineering/SKILL.md) | Implements tenant-aware POS and sales entry with stock, payment and audit-safe posting. |
| Frontend and UX engineering | [`react-development`](skills/frontend-ux/react-development/SKILL.md) | Implements React components, hooks, state, forms and component tests. |
| Frontend and UX engineering | [`tailwind-css`](skills/frontend-ux/tailwind-css/SKILL.md) | Implements Tailwind CSS layouts, variants, theme tokens and build configuration. |
| Frontend and UX engineering | [`ux-content-strategy`](skills/frontend-ux/ux-content-strategy/SKILL.md) | Governs product content: voice, UI text patterns, error taxonomy and content measurement. |
| Android | [`android-development`](skills/android/android-development/SKILL.md) | Builds native Android apps with Kotlin, Compose, Room, offline sync and tests. |
| iOS | [`ios-development`](skills/ios/ios-development/SKILL.md) | Builds native iOS apps with Swift, SwiftUI, structured concurrency and tests. |
| iOS | [`ios-monetization`](skills/ios/ios-monetization/SKILL.md) | Implements StoreKit 2 purchases, subscriptions, entitlements and App Store server events. |
| iOS | [`ios-platform-capabilities`](skills/ios/ios-platform-capabilities/SKILL.md) | Integrates App Intents, SwiftData, notifications, Core ML, Vision and other iOS capabilities. |
| iOS | [`ios-security-and-rbac`](skills/ios/ios-security-and-rbac/SKILL.md) | Designs iOS authentication, Keychain, App Attest, privacy manifests and RBAC. |
| Cross-platform mobile | [`kmp-development`](skills/mobile-cross/kmp-development/SKILL.md) | Shares Kotlin business logic across Android and iOS with Kotlin Multiplatform. |
| Cross-platform mobile | [`mobile-platform-operations`](skills/mobile-cross/mobile-platform-operations/SKILL.md) | Coordinates Android/iOS signing, store review, TestFlight, staged release and rollback. |
| Cross-platform mobile | [`pwa-offline-first`](skills/mobile-cross/pwa-offline-first/SKILL.md) | Builds offline-first PWAs with Service Workers, Workbox, IndexedDB and Background Sync. |
| AI and agent systems | [`ai-agent-commercial-operations`](skills/ai/ai-agent-commercial-operations/SKILL.md) | Prices, bills and sets SLAs, credits and service evidence for agentic AI services. |
| AI and agent systems | [`ai-agent-compliance-controls`](skills/ai/ai-agent-compliance-controls/SKILL.md) | Maps agent operations to SOC 2, ISO 27001 and HIPAA controls with audit evidence. |
| AI and agent systems | [`ai-agent-governance-and-limits`](skills/ai/ai-agent-governance-and-limits/SKILL.md) | Sets agent budgets, step limits, blast-radius controls and kill switches. |
| AI and agent systems | [`ai-agent-multi-agent-coordination`](skills/ai/ai-agent-multi-agent-coordination/SKILL.md) | Designs supervisor/worker, debate and handoff topologies with conflict and deadlock handling. |
| AI and agent systems | [`ai-agent-observability-evaluation`](skills/ai/ai-agent-observability-evaluation/SKILL.md) | Measures, replays and evidences agent task, step and trace outcomes. |
| AI and agent systems | [`ai-agent-runtime-architecture`](skills/ai/ai-agent-runtime-architecture/SKILL.md) | Designs multi-tenant agent runtimes: control loops, state, retries, resumability and cancellation. |
| AI and agent systems | [`ai-agent-safety-and-red-team`](skills/ai/ai-agent-safety-and-red-team/SKILL.md) | Red-teams agent tool and data perimeters for injection, escalation and exfiltration. |
| AI and agent systems | [`ai-agent-tooling-and-hitl`](skills/ai/ai-agent-tooling-and-hitl/SKILL.md) | Designs agent tool catalogues, schemas, action gating and human approval. |
| AI and agent systems | [`ai-analytics`](skills/ai/ai-analytics/SKILL.md) | Designs AI analytics, SaaS AI metrics, predictive analytics and executive insight workflows. |
| AI and agent systems | [`ai-app-architecture`](skills/ai/ai-app-architecture/SKILL.md) | Chooses architecture, components and build-versus-buy for AI-powered applications. |
| AI and agent systems | [`ai-cost-and-metering`](skills/ai/ai-cost-and-metering/SKILL.md) | Models, meters, attributes and controls AI usage cost by tenant, plan and feature. |
| AI and agent systems | [`ai-economic-value-engine`](skills/ai/ai-economic-value-engine/SKILL.md) | Tests AI product ideas for measurable business value and ROI. |
| AI and agent systems | [`ai-evaluation`](skills/ai/ai-evaluation/SKILL.md) | Builds LLM evaluation harnesses, golden datasets, judge calibration and regression gates. |
| AI and agent systems | [`ai-feature-rollout-and-experimentation`](skills/ai/ai-feature-rollout-and-experimentation/SKILL.md) | Runs flagged, canary and A/B rollouts of AI features behind eval and SLO gates. |
| AI and agent systems | [`ai-feature-spec`](skills/ai/ai-feature-spec/SKILL.md) | Specifies one AI feature end to end: model, prompt contract, schema, fallbacks and evaluation. |
| AI and agent systems | [`ai-incident-response`](skills/ai/ai-incident-response/SKILL.md) | Detects, triages, recovers from and reviews AI incidents. |
| AI and agent systems | [`ai-llm-integration`](skills/ai/ai-llm-integration/SKILL.md) | Integrates LLM providers with streaming, structured output, tool calls, retries and caching. |
| AI and agent systems | [`ai-model-gateway`](skills/ai/ai-model-gateway/SKILL.md) | Designs an LLM gateway for routing, fallbacks, quotas, residency and audit logging. |
| AI and agent systems | [`ai-observability-and-debugging`](skills/ai/ai-observability-and-debugging/SKILL.md) | Traces prompts and responses, replays answers and breaks down AI latency and cost. |
| AI and agent systems | [`ai-opportunity-canvas`](skills/ai/ai-opportunity-canvas/SKILL.md) | Ranks AI use cases into an opportunity register by impact, effort, cost and risk. |
| AI and agent systems | [`ai-prompt-engineering`](skills/ai/ai-prompt-engineering/SKILL.md) | Writes and versions system prompts, templates, few-shot examples and defensive prompts. |
| AI and agent systems | [`ai-rag-patterns`](skills/ai/ai-rag-patterns/SKILL.md) | Builds retrieval-augmented generation: chunking, hybrid search, re-ranking and evaluation. |
| AI and agent systems | [`ai-security`](skills/ai/ai-security/SKILL.md) | Secures LLM features against prompt injection, tenant leakage, jailbreaks and PII exposure. |
| AI and agent systems | [`ai-web-apps`](skills/ai/ai-web-apps/SKILL.md) | Builds AI-enhanced web apps with chat, RAG, MCP tools, streaming and guardrails. |
| AI and agent systems | [`coding-agent-optimization`](skills/ai/coding-agent-optimization/SKILL.md) | Tunes Claude Code and Codex set-ups for context, model, permission and token efficiency. |
| AI and agent systems | [`openai-agents-sdk`](skills/ai/openai-agents-sdk/SKILL.md) | Builds Python agents on the OpenAI Agents SDK with tools, handoffs, guardrails and tracing. |
| SaaS platforms | [`full-coverage-saas-seeding`](skills/saas/full-coverage-saas-seeding/SKILL.md) | Seeds and verifies a realistic synthetic SaaS demo tenant across all modules. |
| SaaS platforms | [`modular-saas-architecture`](skills/saas/modular-saas-architecture/SKILL.md) | Designs tenant-selectable SaaS modules with dependency contracts and safe toggles. |
| SaaS platforms | [`multi-tenant-saas-architecture`](skills/saas/multi-tenant-saas-architecture/SKILL.md) | Designs tenant isolation, panel boundaries, zero-trust authorisation and audit trails. |
| SaaS platforms | [`saas-accounting-system`](skills/saas/saas-accounting-system/SKILL.md) | Designs double-entry accounting inside SaaS with automated postings and reconciliations. |
| SaaS platforms | [`saas-admin-backoffice-tooling`](skills/saas/saas-admin-backoffice-tooling/SKILL.md) | Designs audited back-office impersonation, tenant lifecycle and billing overrides. |
| SaaS platforms | [`saas-architecture-strategy`](skills/saas/saas-architecture-strategy/SKILL.md) | Chooses multi-tenant patterns, deployment mapping, scaling and blast-radius isolation. |
| SaaS platforms | [`saas-business-metrics`](skills/saas/saas-business-metrics/SKILL.md) | Defines SaaS revenue, retention, unit-economics and Rule-of-40 metrics. |
| SaaS platforms | [`saas-entitlements-and-plan-gating`](skills/saas/saas-entitlements-and-plan-gating/SKILL.md) | Gates seats, quotas, AI tiers and tools by plan with tenant overrides. |
| SaaS platforms | [`saas-erp-system-design`](skills/saas/saas-erp-system-design/SKILL.md) | Designs configurable SaaS/ERP platforms with workflows, approvals and tenant variation. |
| SaaS platforms | [`saas-lifecycle-email-orchestration`](skills/saas/saas-lifecycle-email-orchestration/SKILL.md) | Derives lifecycle email decisions from user state, events, consent and suppression. |
| SaaS platforms | [`saas-managed-visual-assets`](skills/saas/saas-managed-visual-assets/SKILL.md) | Implements secure upload, activation and audit of managed logos, favicons and backgrounds. |
| SaaS platforms | [`saas-rate-limiting-and-quotas`](skills/saas/saas-rate-limiting-and-quotas/SKILL.md) | Designs per-tenant rate limits, quota algorithms and fair queueing. |
| SaaS platforms | [`saas-sales-organization`](skills/saas/saas-sales-organization/SKILL.md) | Designs SaaS sales motions, roles, pipeline stages, territories and compensation. |
| SaaS platforms | [`saas-seeder`](skills/saas/saas-seeder/SKILL.md) | Bootstraps the multi-tenant SaaS Seeder Template with super admin and demo logins. |
| SaaS platforms | [`saas-sso-scim-enterprise-auth`](skills/saas/saas-sso-scim-enterprise-auth/SKILL.md) | Implements tenant-scoped SAML/OIDC SSO, SCIM provisioning and IP allowlists. |
| SaaS platforms | [`saas-tenant-data-portability-and-erasure`](skills/saas/saas-tenant-data-portability-and-erasure/SKILL.md) | Designs verified tenant data export, retention and erasure workflows. |
| SaaS platforms | [`stripe-payments`](skills/saas/stripe-payments/SKILL.md) | Integrates Stripe PaymentIntents, Checkout, SCA, idempotency and webhooks. |
| SaaS platforms | [`subscription-billing`](skills/saas/subscription-billing/SKILL.md) | Designs Stripe Billing subscriptions: trials, proration, dunning, metered usage and tax. |
| Product and business | [`bds-intake-and-monitoring-system-spec`](skills/product-business/bds-intake-and-monitoring-system-spec/SKILL.md) | Specifies intake, scoring, beneficiary registers and donor reporting for BDS programmes. |
| Product and business | [`consulting-delivery-control-room`](skills/product-business/consulting-delivery-control-room/SKILL.md) | Runs multi-workstream bids and programmes with RACI, RAID, registers and quality gates. |
| Product and business | [`content-writing`](skills/product-business/content-writing/SKILL.md) | Writes and reviews articles, web copy and headlines for readability and structure. |
| Product and business | [`customer-service-excellence`](skills/product-business/customer-service-excellence/SKILL.md) | Handles service recovery, escalations, complaints and CX measurement. |
| Product and business | [`document-spreadsheet-tooling-readiness`](skills/product-business/document-spreadsheet-tooling-readiness/SKILL.md) | Checks the machine can generate and validate promised DOCX, PDF and XLSX files. |
| Product and business | [`excel-spreadsheets`](skills/product-business/excel-spreadsheets/SKILL.md) | Generates and validates professional Excel workbooks, formulas and charts. |
| Product and business | [`hospitality-hotel-restaurant-systems`](skills/product-business/hospitality-hotel-restaurant-systems/SKILL.md) | Architects and audits hotel PMS, restaurant POS and food-service software. |
| Product and business | [`it-proposal-writing`](skills/product-business/it-proposal-writing/SKILL.md) | Plans and strengthens IT proposals, win strategy and pricing narrative. |
| Product and business | [`premium-software-product-execution`](skills/product-business/premium-software-product-execution/SKILL.md) | Designs, prices and builds premium software for high-ticket buyers. |
| Product and business | [`product-discovery`](skills/product-business/product-discovery/SKILL.md) | Tests whether a product or feature deserves investment through prototypes and research. |
| Product and business | [`product-led-growth`](skills/product-business/product-led-growth/SKILL.md) | Designs PLG motions: freemium, PQLs, activation, upgrade prompts and viral loops. |
| Product and business | [`product-strategy-vision`](skills/product-business/product-strategy-vision/SKILL.md) | Defines product vision, principles, OKRs and outcome roadmaps. |
| Product and business | [`professional-word-output`](skills/product-business/professional-word-output/SKILL.md) | Generates and validates professionally structured Word DOCX documents. |
| Product and business | [`software-business-models`](skills/product-business/software-business-models/SKILL.md) | Selects software business models: product, service, platform, subscription or open source. |
| Product and business | [`software-pricing-strategy`](skills/product-business/software-pricing-strategy/SKILL.md) | Designs software pricing, packaging, value metrics, tiers and willingness-to-pay tests. |
| Finance implementation | [`accounting-engine`](skills/finance-accounting/accounting-engine/SKILL.md) | Implements a double-entry ledger engine with balanced postings, reversals and period locks. |
| Finance implementation | [`accounting-finance-controller`](skills/finance-accounting/accounting-finance-controller/SKILL.md) | Coordinates accounting implementation reviews, doctrine routing and control evidence. |
| Finance implementation | [`electronic-fiscal-taxing`](skills/finance-accounting/electronic-fiscal-taxing/SKILL.md) | Implements electronic fiscal tax integrations (e.g. URA EFRIS) with adapters and offline queues. |
| Finance implementation | [`multicurrency-and-fx`](skills/finance-accounting/multicurrency-and-fx/SKILL.md) | Implements IAS 21 multicurrency accounting, rate tables and FX gain/loss revaluation. |
| DevOps and cloud | [`cicd-pipelines`](skills/devops-cloud/cicd-pipelines/SKILL.md) | Builds hardened CI/CD pipelines with security stages, promotion gates and short-lived credentials. |
| DevOps and cloud | [`cloud-architecture`](skills/devops-cloud/cloud-architecture/SKILL.md) | Designs AWS/GCP deployments, containerisation and multi-AZ topologies. |
| DevOps and cloud | [`deployment-release-engineering`](skills/devops-cloud/deployment-release-engineering/SKILL.md) | Designs rollout strategies, release gates, rollback and post-deploy verification. |
| DevOps and cloud | [`docker-development`](skills/devops-cloud/docker-development/SKILL.md) | Containerises PHP, Python and JavaScript services with multi-stage images and Compose. |
| DevOps and cloud | [`infrastructure-as-code`](skills/devops-cloud/infrastructure-as-code/SKILL.md) | Provisions infrastructure with Terraform modules, remote state and idempotent Ansible roles. |
| DevOps and cloud | [`kubernetes-platform`](skills/devops-cloud/kubernetes-platform/SKILL.md) | Runs production Kubernetes: workloads, RBAC, Pod Security, autoscaling, upgrades and recovery. |
| DevOps and cloud | [`observability-monitoring`](skills/devops-cloud/observability-monitoring/SKILL.md) | Designs logs, metrics, traces, alerts, SLOs and dashboards. |
| DevOps and cloud | [`reliability-engineering`](skills/devops-cloud/reliability-engineering/SKILL.md) | Sets timeout, retry, degradation, queue-safety and incident policy for production systems. |
| Game development | [`apple-game-platform-delivery`](skills/game-development/apple-game-platform-delivery/SKILL.md) | Ships games on iOS, iPadOS and macOS with Apple services, Metal diagnostics and notarisation. |
| Game development | [`game-2d-art-animation-and-vfx-pipeline`](skills/game-development/game-2d-art-animation-and-vfx-pipeline/SKILL.md) | Produces and optimises 2D sprites, atlases, animation, UI art and VFX. |
| Game development | [`game-3d-asset-pipeline`](skills/game-development/game-3d-asset-pipeline/SKILL.md) | Produces game-ready 3D assets, rigs, LODs and DCC-to-engine exports. |
| Game development | [`game-accessibility-localisation-and-player-safety`](skills/game-development/game-accessibility-localisation-and-player-safety/SKILL.md) | Designs accessible, localised games with chat safety, moderation and parental controls. |
| Game development | [`game-ai-behaviour-and-navigation`](skills/game-development/game-ai-behaviour-and-navigation/SKILL.md) | Designs NPC behaviour, navigation, perception, behaviour trees and utility AI. |
| Game development | [`game-audio-implementation`](skills/game-development/game-audio-implementation/SKILL.md) | Implements game music, dialogue, spatial and adaptive audio. |
| Game development | [`game-build-release-engineering`](skills/game-development/game-build-release-engineering/SKILL.md) | Builds reproducible Unity, Godot and Unreal pipelines with signing, patching and rollback. |
| Game development | [`game-data-analytics-and-live-economy`](skills/game-development/game-data-analytics-and-live-economy/SKILL.md) | Defines game telemetry, funnels, experiments and virtual-economy controls. |
| Game development | [`game-development-orchestration`](skills/game-development/game-development-orchestration/SKILL.md) | Governs a game project from concept through vertical slice, production and live operations. |
| Game development | [`game-math-and-simulation`](skills/game-development/game-math-and-simulation/SKILL.md) | Specifies vector, quaternion, collision, camera and numerical-simulation rules. |
| Game development | [`game-narrative-and-interactive-story-design`](skills/game-development/game-narrative-and-interactive-story-design/SKILL.md) | Designs interactive stories, quests, dialogue and branching narrative. |
| Game development | [`game-security-anti-cheat-and-abuse`](skills/game-development/game-security-anti-cheat-and-abuse/SKILL.md) | Threat-models games and designs anti-cheat, anti-bot and economy protection. |
| Game development | [`game-studio-delivery-and-commercial-operations`](skills/game-development/game-studio-delivery-and-commercial-operations/SKILL.md) | Runs game estimation, staffing, milestones, outsourcing and launch command. |
| Game development | [`game-testing-polish`](skills/game-development/game-testing-polish/SKILL.md) | Plans game QA, playtesting, balance, compatibility and release-candidate gates. |
| Game development | [`gameplay-systems-architecture`](skills/game-development/gameplay-systems-architecture/SKILL.md) | Specifies engine-neutral gameplay systems: movement, combat, inventory, saves and world state. |
| Game development | [`godot-mobile-game-development`](skills/game-development/godot-mobile-game-development/SKILL.md) | Builds, profiles and exports Godot mobile games for Android and iOS. |
| Game development | [`lean-game-product-development`](skills/game-development/lean-game-product-development/SKILL.md) | Turns game ideas into falsifiable hypotheses, prototypes and go/pivot/stop decisions. |
| Game development | [`level-world-and-content-production`](skills/game-development/level-world-and-content-production/SKILL.md) | Designs and produces levels, worlds, encounters and procedural content. |
| Game development | [`mobile-game-design`](skills/game-development/mobile-game-design/SKILL.md) | Designs mobile game loops, touch controls, progression, economy and ethical monetisation. |
| Game development | [`mobile-game-performance`](skills/game-development/mobile-game-performance/SKILL.md) | Enforces mobile-game frame, memory, battery and thermal budgets via device profiling. |
| Game development | [`mobile-game-release-liveops`](skills/game-development/mobile-game-release-liveops/SKILL.md) | Handles mobile game store submission, IAP, staged rollout and live operations. |
| Game development | [`online-multiplayer-and-game-backend`](skills/game-development/online-multiplayer-and-game-backend/SKILL.md) | Designs authoritative multiplayer, replication, prediction, matchmaking and game backends. |
| Game development | [`real-time-game-graphics`](skills/game-development/real-time-game-graphics/SKILL.md) | Designs and diagnoses render pipelines, shaders, lighting and GPU budgets. |
| Game development | [`unity-mobile-game-development`](skills/game-development/unity-mobile-game-development/SKILL.md) | Builds, profiles and packages Unity mobile games in C#. |
| Game development | [`unreal-game-development`](skills/game-development/unreal-game-development/SKILL.md) | Builds Unreal Engine games with C++, Blueprints, replication and packaging. |
| GIS | [`gis-enterprise-domain`](skills/gis/gis-enterprise-domain/SKILL.md) | Administers ArcGIS Enterprise and builds real-estate GIS features. |
| GIS | [`gis-platform-engineering`](skills/gis/gis-platform-engineering/SKILL.md) | Implements maps, geocoding, spatial APIs and PostGIS-backed platforms. |

## Catalogue size

The active count is a checked surface: `tests/test_engine_control_plane.py` compares it with the files on disk, so update it in the same change that adds or retires a skill. `scripts/skill_catalog_guardrails.py` enforces the maximum.

| Measure | Value |
|---|---:|
| Active `SKILL.md` files | 167 |
| Guardrail maximum | 200 |

Routing: the [skill routing index](docs/skill-routing-index.md) maps retired slugs to their current skills, and [`docs/skill-aliases.yml`](docs/skill-aliases.yml) holds the machine-readable form. Operating rules for agents are in [`AGENTS.md`](AGENTS.md); contribution rules are in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## References

Sources cited in this repository's skills, references, source registers, audits and continuous-improvement records. They are listed as citations only: the engine paraphrases operational guidance and stores no book text. Book entries give the author, year and publisher only where the repository records them. Books named only in purchase lists or suggested-reading lists are omitted.

### Books

384 books. 89 are recorded without an author and are listed after the authored entries.

- Aaron *Profitable Blog Topics*.
- Abella *250 Killer TypeScript One-Liners*.
- Agius and Clancey *Faster, Smarter, Louder*.
- Akintoye, A. (2024) *Mastering Design Patterns in TypeScript*. Juri Books.
- Aleks, N. and Farhi, D. (2023) *Black Hat GraphQL*. No Starch Press.
- Alves (2020) *Unity 3D*.
- Ross Anderson *Security Engineering*.
- Annable *Kubernetes: A Comprehensive Step-by-Step Guide*.
- Laurie Annis *Blender 3D for Jobseekers*.
- Antonio *Pro React*.
- Łapiński *Vulkan Cookbook*.
- Aremu (2025) *DeepSeek AI from Beginner to Paid Professional*.
- Dan Ariely *Predictably Irrational*.
- Tal Ater *Building Progressive Web Apps*. O'Reilly.
- Baker et al. *Computer Graphics with OpenGL*.
- Bandura, A. (1977) *Social Learning Theory*. Prentice Hall.
- Bean *The Accidental Instructional Designer*.
- Chris Belanger and Jawwad Ahmad *Mastering Git*.
- Arijan Belec (2022) *Blender 3D Incredible Models*.
- Adam Bellemare (2020) *Building Event-Driven Microservices*. O'Reilly.
- Benedict *How to Build a Business Warren Buffett Would Buy*.
- Betsy Beyer et al. *Site Reliability Engineering*.
- Bhat (2023) *Ultimate Tailwind CSS Handbook*. BPB.
- Bly *How to Write and Sell Simple Information*.
- Boeira (2023) *Lean Game Development*.
- Booz and Fritchey (2024) *Introduction to PostgreSQL for the Data Professional*.
- Borges, D. and Campbell, D. (2026) *AI Security Engineering*.
- Bornet *The Human-Agent Orchestrator*.
- Borromeo (2022) *Hands-On Unity 2022 Game Development*.
- Adrienne Braganza *Looks Good to Me: Constructive Code Reviews*.
- Steven Branson (2020) *UX / UI Design*.
- Brener, J. (2024) *Mastering RAG for AI Agents*.
- Yevgeniy Brikman (2025) *Fundamentals of DevOps and Software Delivery*.
- Yevgeniy Brikman *Terraform: Up & Running*.
- Bringhurst *The Elements of Typographic Style*.
- Simon Brown *Software Architecture for Developers*.
- Burns, Beda and Hightower *Kubernetes: Up and Running*.
- Wes Bush *Product-Led Growth*. Product-Led Alliance.
- Cacheaux and Berlin *Advanced iOS App Architecture*. Ray Wenderlich Press.
- Cagan, M. (2017) *INSPIRED: How to Create Tech Products Customers Love*. Wiley.
- Cagle (2024) *Architecting Enterprise AI Applications*.
- Craig Caldwell (2025) *Story Structure and Development*.
- Campbell and Majors (2017) *Database Reliability Engineering*. O'Reilly.
- Carman (2018) *Visual Design Concepts for Mobile Games*.
- Casciaro and Mammino (2020) *Node.js Design Patterns*. Packt.
- Alexio Cassani (2025) *Code Revealed*.
- Chakraborty (2025) *DeepSeek AI: A Comprehensive Guide*.
- Chen (2023) *Pandas for Everyone*.
- Boris Cherny (2019) *Programming TypeScript*. O'Reilly.
- Chintale *DevOps Design Patterns*.
- Ciceri et al. *Software Architecture Metrics*.
- Matt Cone (2023) *The Markdown Guide*.
- Coombs, P. (2005) *IT Project Proposals: Writing to Win*. Cambridge University Press.
- Lucas da Costa *Testing JavaScript Applications*. Manning.
- Croll and Yoskovitz *Lean Analytics*. O'Reilly.
- Joshua Crotts (2024) *Learning Java: A Test-Driven Approach*. Springer.
- Csikszentmihalyi, M. (1990) *Flow: The Psychology of Optimal Experience*. Harper & Row.
- Cusumano, M. A. (2004) *The Business of Software: What Every Manager, Programmer, and Entrepreneur Must Know to Thrive and Survive in Good Times and Bad*. Free Press.
- Aki D. (2024) *LLM, Transformer, RAG AI*.
- Anna Dahlström *Storytelling in Design*.
- Raj Abhijit Dandekar *Build a DeepSeek Model (From Scratch)*.
- R. Sarma Danturthi *Database and Application Security: A Practitioner's Guide*.
- Usama Dar *PostgreSQL Server Programming*. Packt.
- Dash, S. K. (2025) *Mastering Software Product Management*. Orange Education.
- Day (2024) *Hands-On APIs for AI and Data Science*.
- Pamala B. Deacon (2020) *UX and UI Design Strategy*.
- Despoudis, T. (2024) *Build AI-Enhanced Web Apps*. Packt.
- Devitt, Ryan et al. *Arrive: A Design Innovation Framework to Deliver Breakthrough Services, Products and Experiences*. Routledge.
- Stephanie Diamond *Claude For Dummies*.
- Dingare *CI/CD Pipeline Using Jenkins Unleashed*.
- Ray Dinwiddie (2022) *PHP Security and Session Management*.
- Dormehl (2014) *The Formula*.
- Dowling (2026) *Building Machine Learning Systems with a Feature Store*.
- Stéphane Duguin *Cybersecurity for NGOs*.
- Dynowski and Dulak (2025) *Learning API Styles*.
- Eddy *Blog It Right*.
- Ehrhardt et al. *Corporate Finance: A Focused Approach*.
- Sean Ellis and Morgan Brown *Hacking Growth*. Currency.
- Jessica Enders *Designing UX: Forms*.
- Eric Evans *Domain-Driven Design*.
- Eyal, N. and Hoover, R. (2014) *Hooked: How to Build Habit-Forming Products*. Portfolio/Penguin.
- Eyal, N. and Hoover, R. (2014) *Hooked: Supplemental Workbook*. NirAndFar.com.
- Zoltan Fekeshazi (c. 2017) *Product Managers' Guide to UX Design*. UX Studio.
- Felicia (2021) *Godot from Zero to Proficiency (Advanced)*.
- Fernandez, O. (2024) *Patterns of Application Development Using AI*.
- Fielding *The Brand Book*.
- Mike Fishbein *Growth Hacking with Content Marketing*.
- Neal Ford et al. *Building Evolutionary Architectures*.
- Nicole Forsgren, Jez Humble and Gene Kim *Accelerate*.
- Martin Fowler *Refactoring*.
- Fusco (2023) *Large Scale Apps with React and TypeScript*.
- Cory Gackenheimer (2013) *Node.js Recipes*. Apress.
- Garbugli *Find Your Market*.
- Garbugli *The SaaS Email Marketing Playbook*.
- Niranjan Gattupalli and RaviTeja Amerineni (2026) *Mastering Salesforce Quality*.
- Trisha Gee *What to Look for in a Code Review*.
- JJ Geewax *API Design Patterns*.
- George *Excel 2019 Advanced Topics*.
- Gerber *The E-Myth Enterprise*.
- Josh Goldberg (2022) *Learning TypeScript*. O'Reilly.
- Tod Golding *Building Multi-Tenant SaaS Architectures*.
- Goodwin (2016) *Polished Game Development*.
- Google *Building Secure and Reliable Systems*.
- Google *The Site Reliability Workbook*.
- Ian Gorton *Foundations of Scalable Systems*. O'Reilly.
- Gough, Bryant and Auburn *Mastering API Architecture*. O'Reilly.
- Trey Grainger (2024) *AI-Powered Search*. Manning.
- Grant (2018) *101 UX Principles*.
- Graves *Writing for Profit*.
- Greever (2020) *Articulating Design Decisions*.
- Rana Gujral *The AI Instinct*.
- Jason van Gumster and Stefan Maurus (2025) *Farming Simulator Modding With Blender*.
- Gurbani, N. (2024) *Mastering RESTful API Development with Go*.
- Felipe Gutierrez (2019) *Pro Spring Boot 2*. Springer/Apress.
- Felipe Gutierrez and DaShaun Carter (2026) *Pro Spring Boot 4*. Springer/Apress.
- Habib (2025) *Building Agents with OpenAI Agents SDK*. Packt.
- Armin Halač (2024) *A Complete Guide to Character Rigging for Games Using Blender*.
- Hamilton *Email Storyselling Playbook*.
- Stephen Haney (2015) *Game Development with Swift*. Packt.
- Hansen *How to Build a Subscription Business — 29 Steps to Subscription Mastery*.
- Hargis, Carey et al. *Developing Quality Technical Information*.
- Hartwell and Chen *Archetypes in Branding*.
- Hauge *Storytelling Made Easy*.
- Mark Heckler (2021) *Spring Boot: Up & Running*. O'Reilly.
- Jay Heizer *Operations Management*. Pearson.
- Theresa Hill *3D Game Development Practical Introduction*.
- Hill-Whittall (2015) *The Indie Game Developer Handbook*.
- Joseph Hocking (2022) *Unity in Action, Third Edition: Multiplatform Game Development in C#*. Manning.
- Celia Hodent (2022) *What UX Is Really About*. CRC Press.
- Hodjat, B. and Blondeau, A. (2026) *The Agentic Enterprise*.
- Hoffman *Web Application Security*.
- Daniel R. Holt *Modern Data Systems*.
- Alexandra Horowitz *On Looking*.
- Horton and Vice *Mastering React*.
- Drew Hoskins *The Product-Minded Engineer*.
- Paul Hudson *Swift Design Patterns*. Hacking with Swift.
- Humble and Farley (2010) *Continuous Delivery*. Addison-Wesley.
- Chip Huyen (2022) *Designing ML Systems*.
- Chip Huyen (2025) *AI Engineering*. O'Reilly.
- Indocan Publications (2022) *A Quick Guide to Software as a Service (SaaS): Beginner Insight*.
- Danny Iny *Blog Post Ideas: 21 Proven Ways*.
- Jain (2024) *Modern Web Applications with Next.js*.
- John *The Instant 2020–2021 Guide on Subscription Billing for SaaS*.
- Johnson (2025) *Practical JSON Design and Usage*.
- Johnson, P. (2024) *Modern API Design*.
- Jolowicz (2024) *Hypermodern Python Tooling*.
- Jones (2023) *Driving Data Quality with Data Contracts*.
- Jordan *ICDL Word*.
- Josyula et al. (2024) *Mastering Retrieval-Augmented Generation*. BPB.
- Kahneman, D. (2011) *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
- Metin Karatas (2024) *Developing AI Applications*.
- Almantas Karpavicius *Software Craftsmanship Using AI*.
- Vlad Khononov *Learning Domain-Driven Design*. O'Reilly.
- Kim (2023) *The Next.js Handbook*.
- Kim, Humble, Debois and Willis (2021) *The DevOps Handbook*. IT Revolution.
- Kim, W. C. and Mauborgne, R. (2005) *Blue Ocean Strategy*. Harvard Business School Press.
- King *Product Marketing Misunderstood*.
- Kirkpatrick *Four Levels of Training Evaluation*.
- Kits For Life (2025) *Mastering DeepSeek-v3*.
- Laura Klein (2013) *UX for Lean Startups*.
- Martin Kleppmann (2017) *Designing Data-Intensive Applications*. O'Reilly.
- Kohavi, Tang and Xu *Trustworthy Online Controlled Experiments*. Cambridge.
- van der Kooij and Pizarro *Blueprints for a SaaS Sales Organization*.
- Kothand *One Hour Content Plan*.
- Krause (2024) *The Complete Developer*.
- Jesper Wisborg Krogh (2020) *MySQL 8 Query Performance Tuning*. Apress.
- Megan Krone *Navigating the Dissertation Writing Process*.
- Krug, S. (2014) *Don't Make Me Think, Revisited: A Common Sense Approach to Web Usability*. New Riders/Peachpit.
- Kumar (2023) *Fluent React*. O'Reilly.
- Kumar et al. (2024) *Mastering MySQL Administration*.
- LaGrone, B. (2016) *Web Design Blueprints*. Packt.
- Langley et al. *The Improvement Guide*.
- Will Larson *Staff Engineer*.
- Laster (2023) *Learning GitHub Actions*.
- Levinson and McLaughlin (2004) *Guerrilla Marketing for Consultants*.
- Jaime Levy (2015) *UX Strategy*. O'Reilly.
- Li et al. (2021) *Creating Games with Unity, Substance Painter, & Maya*.
- Greg Lim *Next.js 13 + Prisma*.
- Lima *Fundamentals of Writing*.
- Liu *DNS and BIND*.
- Rebecca Livermore *Blogger's Quick Guide*.
- Lockridge and Van Ittersum *Writing Workflows*.
- Josh Long and Kenny Bastani (2017) *Cloud Native Java*. O'Reilly.
- Marko Luksa *Kubernetes in Action*. Manning.
- Maioli (2018) *Fixing Bad UX*.
- Charity Majors, Liz Fong-Jones and George Miranda *Observability Engineering*. O'Reilly.
- Manning and Buttfield-Addison (2017) *Mobile Game Development with Unity*.
- Martin (2023) *PHP Advanced*.
- Andrea De Mauro (2024) *AI Applications Made Easy*.
- Maxwell *7 Steps to Better Writing*.
- Malcolm McDonald *Web Security for Developers*.
- Mersch (2022) *Hacking SaaS*.
- Metts and Welfle (2020) *Strategic Writing for UX*.
- Jonathan Middaugh (2020) *255 Java Interview Success Questions*.
- David Millet et al. (2012) *Blender 3D: Noob to Pro*.
- Mark Moeykens (2024) *SwiftData Mastery in SwiftUI*. Big Mountain Studio.
- Sanjeev Mohan *Designing the AI-Driven Data Foundations*.
- Kief Morris *Infrastructure as Code*. O'Reilly.
- Tony Mullen (2011) *Introducing Character Animation with Blender*.
- Josef Müller-Brockmann (1981) *Grid Systems in Graphic Design*.
- Mark Murphy *Elements of Android Room*.
- Murray (2021) *C# Game Programming Cookbook for Unity 3D*.
- Nate Murray (2019) *Fullstack Node.js*. Leanpub.
- Nadalin *WASEC*.
- Nekrasov *Swift Recipes for iOS Developers*.
- Nelson (2024) *Software Engineering for Data Scientists*.
- Sam Newman *Building Microservices*.
- Daniel Nichter (2022) *Efficient MySQL Performance*. O'Reilly.
- Noble *How to Write a Grant*.
- Norman, D. (2013) *The Design of Everyday Things*. Basic Books.
- Greg Nudelman (2024) *UX for AI: A Framework for Product Design*. Wiley.
- Michael Nygard *Release It!*.
- Regina Obe and Leo Hsu *PostgreSQL: Up and Running*. O'Reilly.
- Joseph Okonkwo (2025) *Growth Engineering*. Wiley.
- Olesen-Bagneux (2023) *The Enterprise Data Catalog*.
- Oliveira (2024) *AI Strategies for Web Development*.
- Osmani (2026) *Web Performance Engineering in the Age of AI*.
- Paduraru, E. (2024) *Roots of UI/UX Design*. Creative Tim.
- Raghuvir Pai, Gopinath Chattopadhyay and Anne Gibbs (eds.) (2026) *Advances in Intelligent Asset Management and Maintenance*.
- Panzarella, L. (2022) *UI/UX Web Design Simply Explained*.
- Alex Petrov (2019) *Database Internals*. O'Reilly.
- La Piana *The Nonprofit Strategy Revolution*.
- Heydon Pickering and Andy Bell *Every Layout*.
- Matt Pocock (2026) *Total TypeScript*. No Starch Press.
- Porter, M. E. (1980) *Competitive Strategy*. Free Press.
- Van Der Post *Python in Excel Advanced*.
- Rambert (2024) *Advanced Next.js for Everyone*.
- Rawat *CI/CD Pipeline with Docker and Jenkins*.
- Gwynne Richards *Warehouse Management*. Kogan Page.
- Richards and Ford *Fundamentals of Software Architecture*.
- Marc Roche *Business English Speaking: Advanced Masterclass — Speak Advanced ESL Business English with Confidence & Elegance*.
- Marc Roche *Business English Vocabulary: Advanced Masterclass*. IDM Business and Law.
- Santana Roldán (2024) *React 18 Design Patterns and Best Practices*. Packt.
- Josh Rosso, Rich Lander, Alex Brand and John Harris *Production Kubernetes*. O'Reilly.
- Rowse *Problogger*.
- Sara Rubinelli (2026) *Institutional Health Communication in the Information Age*.
- Narendar Singh Saini *iOS Developer Solutions Guide*.
- Schmidlin *The Art of Company Valuation and Financial Statement Analysis*.
- Scolastici and Nolte (2013) *Mobile Game Design Essentials*.
- Adam D. Scott (2020) *JavaScript Everywhere*. O'Reilly.
- Marco Secchi (2023) *Multiplayer Game Development with Unreal Engine 5*. Packt.
- Marco Secchi (2024) *Artificial Intelligence in Unreal Engine 5*.
- Seid (2017) *Franchise Management For Dummies*.
- Derek Selander *Advanced Apple Debugging & Reverse Engineering*.
- Seok *Unity Game Development*.
- Sheehan *The Pocket Guide to Product Launches*.
- Sheth and Singh *Ace the Data Science Interview*.
- Len Silverston *The Data Model Resource Book*.
- Mark Simon (2023) *Leveling Up with SQL*. Apress.
- Smith, J. (2024) *RAG Generative AI: A Practical Guide*.
- Sommerfeld (2024) *Unlock PHP 8*.
- Manuel Spigolon *Accelerating Server-Side Development with Fastify*. Packt.
- David Spuler (2024) *Generative AI Applications*.
- Stallings *Network Security Essentials: Applications and Standards*.
- Stetson, C. (2017) *NGINX Microservices Reference Architecture*. NGINX Inc.
- Phil Sturgeon *Build APIs You Won't Hate*.
- Stuttard and Pinto *The Web Application Hacker's Handbook*.
- Synechron (2018) *Bridge the User Experience Gap in Enterprise Applications for Financial Services & Insurance*.
- Technology Grant News (2010) *Winning at IT: Grant Writing for Technology Grants*.
- Tidwell, J., Brewer, C. and Valencia, A. (2020) *Designing Interfaces*. O'Reilly.
- Trio *How to Run a SaaS Business*.
- D. Truman *JavaScript Object-Oriented Programming By Examples*.
- Tien Tzuo *Subscribed*.
- Urban *Advanced Excel for Productivity*.
- Bin Uzayr (2022) *Mastering GitHub Pages: A Beginner's Guide*.
- Bin Uzayr (ed.) (2023) *Mastering React Native: A Beginner's Guide*.
- Enrico Valenza (2015) *Blender 3D Cookbook*.
- Dan Vanderkam (2024) *Effective TypeScript*. O'Reilly.
- Vanier, Garnier and Hristov (2019) *Advanced MySQL 8*. Packt.
- Eric Vennaro *iOS Development at Scale*.
- Roberto Verganti (2016) *Overcrowded*. MIT Press.
- Vic *Microsoft Word 2022 for Beginners & Pros*.
- Walkenbach and Alexander *Microsoft Excel 365 Bible*.
- Walling (2023) *The SaaS Playbook*.
- Craig Walls *Spring in Action*.
- Donny Wals (2025) *Practical Swift Concurrency*.
- John Walsh, Uzi Ailon and Matt Barker *Identity Security for Software Development*.
- Watkinson *The Grid*.
- Watson et al. *Supply Chain Network Design*.
- Aniket Wattamwar (2026) *Algorithms Every Programmer Should Know*. Manning Early Access.
- Webb *What Customers Crave*.
- Dan Wellman (2023) *Ultimate TypeScript Handbook*.
- Wempen *Advanced Microsoft Word 2016*.
- Wengler (2026) *Automate Excel with Python*.
- John Whalen (2019) *Design for How People Think*. O'Reilly Media.
- Whitmell *Business Writing Essentials*.
- Karl Wiegers *Software Requirements Essentials*.
- Kristopher Wilson *The Clean Architecture in PHP*.
- Steve Wilson *The Developer's Playbook for Large Language Model Security*.
- Winning By Design *The SaaS Sales Method for Account Executives*.
- Winning By Design *The SaaS Sales Method Fundamentals*.
- Wood *The Marketing Plan Handbook*.
- Wroblewski (2008) *Web Form Design: Filling in the Blanks*.
- Yablonski, J. (2024) *Laws of UX*. O'Reilly.
- Yang, C. D. (2024) *Building User Interfaces for Modern Web Applications: React Programming*. PA-ADOPT open textbook.

Recorded without an author:

- *.NET MAUI Projects: A guide to building applications for Windows, macOS, Android, and iOS* (2025).
- *97 Things Every Application Security Professional Should Know*.
- *The AI Cybersecurity Handbook*.
- *AI for Game Developers* (2005).
- *Analyzing Websites*.
- *Applying the Kaizen in Africa* (2018).
- *ArcGIS Pro Manual*.
- *Artificial Intelligence for .NET*.
- *Bandit Algorithms for Website Optimization*.
- *Basic Math for Game Development with Unity 3D*.
- *Become an Effective Software Engineering Manager*.
- *A Bug Hunter's Diary*.
- *Building a Data and AI Platform with PostgreSQL* (2025).
- *Building and Distributing Agentic AI Solutions*.
- *C# 12 for Cloud, Web, and Desktop Applications*.
- *C# 14 and .NET 10 - Modern Cross-Platform Development Fundamentals*.
- *The Chicago Manual of Style*.
- *CI/CD Unleashed*.
- *Clean Code with TypeScript*.
- *Clear Written Communication*. 50Minutes.
- *Continuous Deployment*.
- *Core C# and .NET Quick Reference*.
- *Decoding JavaScript Design Patterns*.
- *Designing for AI*.
- *DevOps for PHP Developers*.
- *Digital Image Processing*.
- *Digital Storytelling*.
- *Docker for PHP Developers*.
- *The Effective Engineer*.
- *Excel 2025 All-in-One Step-by-Step Guide*.
- *Full-Stack Web Development with TypeScript 5*.
- *Fullstack GraphQL*.
- *Fullstack React with TypeScript*. Newline.
- *The Fundamentals of UX Writing*.
- *Generating Efficient PHP* (2023). php[architect].
- *GIS Succinctly*.
- *Git Fundamentals for New Developers*.
- *Git Mastery Accelerated Crash Course*.
- *Google Maps JavaScript API Cookbook*.
- *Grokking Web Application Security*. Manning.
- *HashiCorp Vault: The Definitive Guide*.
- *HTTP: The Definitive Guide*.
- *Information Dashboard Design*.
- *Internet and Web Application Security*.
- *Introduction to Information Retrieval*.
- *iOS 18 Programming for Beginners*.
- *iOS Application Security: The Definitive Guide for Hackers and Developers*.
- *iOS TDD by Tutorials*. RayWenderlich.
- *Kubernetes Best Practices*.
- *KUBERNETES: A Simple Guide*.
- *Leaflet in Practice*.
- *Learning C# Through Small Projects* (2024).
- *Learning JavaScript Data Structures and Algorithms*.
- *Leveling Up as a Tech Lead*.
- *Master Software Architecture*.
- *Mastering ArcGIS Enterprise*.
- *Mastering Java Spring Boot: Advanced Techniques and Best Practices*.
- *Mastering Linux Security and Hardening*.
- *Mastering Local SEO with Google Maps*.
- *Mastering PostgreSQL*. Manning.
- *Mastering Prompt Engineering*.
- *Microsoft Excel Bible 2026*.
- *Microsoft Visual C#: Introduction to Object Oriented Programming*.
- *Modern DevOps Practices*.
- *Modern Software Engineering*.
- *Modern Web Cartography*.
- *Network Security Firewalls and VPNs*. Jones & Bartlett.
- *Node.js Fundamentals*.
- *Parallel Programming with C# and .NET*.
- *PCI DSS: A Practical Guide*.
- *Perfect Software and Other Illusions About Testing*.
- *PHP 8: Principles and Practices of Object-Oriented Programming*.
- *Platform Enterprise*.
- *Practical Linux Security Cookbook*.
- *Pro Git*.
- *Python Tricks*.
- *Real Estate and GIS*.
- *Retention Point*.
- *Security Automation with Ansible 2*.
- *Software Design*.
- *Software Development Pearls*.
- *Software Engineering at Google*.
- *Strategic DevOps*.
- *TypeScript Mini Reference*.
- *Ultimate Excel Formula & Function Reference Guide*.
- *UNIX Internals: The New Frontiers*.
- *Video Game Storytelling*.
- *Wicked Cool Shell Scripts*.
- *Zero to Mastery in Network Security*.

### Repositories

The ten repositories studied in the my-10-kaizen operation (29 September 2026) were superpowers, ponytail, ui-ux-pro-max-skill, graphify, caveman, agent-skills, Understand-Anything, awesome-claude-skills, archify and Impeccable. The first list below records what this engine adapted from each; the per-file record is [docs/source-registers/m10-06-third-party-attributions.md](docs/source-registers/m10-06-third-party-attributions.md).

Third-party repositories whose mechanisms were adapted (mechanisms paraphrased; the attribution index records that no upstream text was copied):

- obra/superpowers — https://github.com/obra/superpowers — MIT, 8ca22db — adapted: ceremony ratchet, claim/evidence table, Excuse/Reality table, dispatch and review controls, worktree safety, receiving review, plan header and proportion check; CONTRIBUTING guidance paraphrased from its `AGENTS.md`
- addyosmani/agent-skills — https://github.com/addyosmani/agent-skills — MIT, 2686b62 — adapted: written quality bar, check placement by cost, weakening-diff guard, upward ratchet; routing smoke-test/eval pattern and eval-readiness rubric
- JuliusBrussee/caveman — https://github.com/JuliusBrussee/caveman — MIT (skill text), 2fd153c — adapted: output registers R0/R1/R2 and preserve list; per-lane report shapes and status tokens
- Graphify-Labs/graphify — https://github.com/Graphify-Labs/graphify — Apache-2.0, d6eaa8a — adapted: query-first codebase comprehension, staleness rules, EXTRACTED/INFERRED/AMBIGUOUS tags, advisory-hook properties
- Egonex-AI/Understand-Anything — https://github.com/Egonex-AI/Understand-Anything — MIT, b05cc3b — adapted: topology-ordered code tours, tour validation, change classes, pathspec-scoped staleness
- tt-a1i/archify — https://github.com/tt-a1i/archify — MIT, 0e4949f — adapted: evidence pinned to a full SHA, "a citation is not a proof", doctrine-as-tests, update-awareness properties used in the skill safety gate
- nextlevelbuilder/ui-ux-pro-max-skill — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — MIT, 09170ee — adapted: retrieval-harness design only (curated corpus, lexical ranking, abstention, graded golden set); no rows, font or palette data
- pbakaus/impeccable — https://github.com/pbakaus/impeccable — Apache-2.0, 114ea1d — adapted: responsive-design and UX-writing references (Paul Bakaus); slop catalogue and 61-rule detector registry registered as evidence for bans only
- DietrichGebert/ponytail — https://github.com/DietrichGebert/ponytail — MIT, e3ba2aa — adapted: checker self-test discipline (reference_good must pass, reference_bad must fail) for the solution-selection benchmark
- ComposioHQ/awesome-claude-skills — no URL recorded in repo — licence not recorded — adapted: ecosystem-scan and third-party intake procedure, paraphrased from the my-10-kaizen study (report 08, sections 5.6 and 5.8)
- donvito/codex-astra-luna-orchestrator — https://github.com/donvito/codex-astra-luna-orchestrator — licence not recorded, 21f4561 — concept reference only for the Codex Astra/Luna model-role topology; independently implemented, upstream installer read but not run
- affaan-m/ECC — https://github.com/affaan-m/ECC — licence not recorded — adapted: `rules/` layer pattern; agentic-engineering rule; install.sh/install.ps1 linked-path fix; plugin-manifest schema notes; skills council, github-ops, santa-method (credited to Ronald Skelton, RapportScore.ai), code-tour, opensource-pipeline, inherit-legacy-style, documentation-lookup, parallel-execution-optimizer, regex-vs-llm-structured-text, iterative-retrieval, hexagonal-architecture, strategic-compact, verification-loop, security-scan
- anthropics/skills — https://github.com/anthropics/skills — Apache-2.0, 3337550 — adapted: MCP tool-surface evaluation method (mcp-builder `reference/evaluation.md`); also named as an ecosystem-scan source
- mattpocock/skills — https://github.com/mattpocock/skills — licence not recorded, 3cca18b — comparison study; adapted: deep-module, seam, deletion-test and design-it-twice mechanisms, tracer-bullet work graphs, human-only operation wizards

Repositories cited (referenced, not adapted):

- android/architecture-samples — https://github.com/android/architecture-samples — licence not recorded — cited
- android/compose-samples — https://github.com/android/compose-samples — licence not recorded — cited (incl. JetNews)
- android/nowinandroid — https://github.com/android/nowinandroid — licence not recorded — cited
- anthropics/anthropic-cookbook — https://github.com/anthropics/anthropic-cookbook — licence not recorded — cited
- openai/openai-cookbook — https://github.com/openai/openai-cookbook — licence not recorded — cited
- mitre-atlas/atlas-data — https://github.com/mitre-atlas/atlas-data — licence not recorded — cited (release v2026.09)
- bitol-io/open-data-contract-standard — https://github.com/bitol-io/open-data-contract-standard — licence not recorded — cited (ODCS releases)
- standard-webhooks — https://github.com/standard-webhooks — licence not recorded — cited (Standard Webhooks specification)
- google-ai-edge/mediapipe-samples — https://github.com/google-ai-edge/mediapipe-samples — licence not recorded — cited
- GoogleChrome/lighthouse-ci — https://github.com/GoogleChrome/lighthouse-ci — licence not recorded — cited
- dequelabs/axe-core and dequelabs/axe-core-npm — https://github.com/dequelabs/axe-core — licence not recorded — cited
- stripe/stripe-php and stripe/stripe-node — https://github.com/stripe/stripe-php — licence not recorded — cited
- mockito/mockito-kotlin — https://github.com/mockito/mockito-kotlin — licence not recorded — cited
- open-telemetry/opentelemetry-swift — https://github.com/open-telemetry/opentelemetry-swift — licence not recorded — cited
- nodejs/Release — https://github.com/nodejs/Release — licence not recorded — cited (Node.js release schedule)
- helidon-io/helidon — https://github.com/helidon-io/helidon/releases — licence not recorded — cited (release source)
- eclipse-ee4j/glassfish — https://github.com/eclipse-ee4j/glassfish/releases — licence not recorded — cited
- payara/Payara — https://github.com/payara/Payara/releases — licence not recorded — cited
- pgvector/pgvector — https://github.com/pgvector/pgvector — licence not recorded — cited
- CrunchyData/pg_tileserv — https://github.com/CrunchyData/pg_tileserv — licence not recorded — cited
- coreruleset/coreruleset — https://github.com/coreruleset/coreruleset — licence not recorded — cited (OWASP CRS)
- owasp-modsecurity/ModSecurity and ModSecurity-nginx — https://github.com/owasp-modsecurity/ModSecurity — licence not recorded — cited
- SpiderLabs/ModSecurity — https://github.com/SpiderLabs/ModSecurity — licence not recorded — cited
- corazawaf/coraza — https://github.com/corazawaf/coraza — licence not recorded — cited
- argoproj/argo-cd — https://github.com/argoproj/argo-cd — licence not recorded — cited (HA install manifest)
- kubernetes/ingress-nginx — https://github.com/kubernetes/ingress-nginx — licence not recorded — cited
- kubernetes-sigs/metrics-server — https://github.com/kubernetes-sigs/metrics-server — licence not recorded — cited
- open-policy-agent/gatekeeper — https://github.com/open-policy-agent/gatekeeper — licence not recorded — cited
- kubecost/cost-analyzer-helm-chart — https://github.com/kubecost/cost-analyzer-helm-chart — licence not recorded — cited
- ducktors/turborepo-remote-cache — https://github.com/ducktors/turborepo-remote-cache — licence not recorded — cited
- astral-sh/ruff-pre-commit and astral-sh/uv-pre-commit — https://github.com/astral-sh/ruff-pre-commit — licence not recorded — cited
- pre-commit/pre-commit-hooks — https://github.com/pre-commit/pre-commit-hooks — licence not recorded — cited
- brentvollebregt/auto-py-to-exe — https://github.com/brentvollebregt/auto-py-to-exe — licence not recorded — cited
- DerekSelander/LLDB — https://github.com/DerekSelander/LLDB — licence not recorded — cited
- AvaloniaUI (organisation) — https://github.com/avaloniaui — licence not recorded — cited

### Standards and official sources

Standards bodies and regulators:

- OWASP — https://owasp.org/ — ASVS 5.0.0 (project page, https://owasp.org/projects/asvs); OWASP Top 10 2025 (also Top 10:2021 for legacy mappings); OWASP Top 10 for LLM Applications 2026 (genai.owasp.org); OWASP Top 10 for Agentic Applications 2026 (ASI01-ASI10); OWASP API Security Top 10 2023; OWASP MASVS; OWASP Cheat Sheet Series (OS Command Injection Defense, PHP Configuration); OWASP ZAP, Dependency-Check, Core Rule Set, ModSecurity
- W3C and WHATWG — https://www.w3.org/TR/WCAG22/ — WCAG 2.2 (AA; WCAG 2.1 AA and 2.0 also named), WCAG 2.2 Understanding (error identification), WAI-ARIA Authoring Practices (dialog modal), WAI images tutorial, Trace Context, WebXR, W3C Markup Validator docs; WHATWG HTML Living Standard (server-sent events)
- ISO/IEC — https://www.iso.org/ — ISO/IEC 27001:2022 (27001:2013 for legacy), ISO/IEC 42001:2023 (EN ISO/IEC 42001:2026 CEN adoption), ISO/IEC 40500:2025, ISO/IEC 25010, ISO/IEC/IEEE 29119-3:2013, ISO/IEC 14764:2022, ISO/IEC 12207, ISO 9241-110:2020, ISO 9241-210:2019, ISO 26514, ISO 26262, ISO 8601, ISO 4217
- IEEE — IEEE Std 830-1998, IEEE Std 29148-2018, IEEE Std 1016-2009, IEEE Std 1012-2016, IEEE 829, IEEE Std 1233-1998, IEEE Std 610, IEEE 42010, IEEE 754 (named standards, no URLs)
- IETF / RFC Editor — https://www.rfc-editor.org/ — RFC 9457 (Problem Details for HTTP APIs, obsoletes RFC 7807), RFC 9110-9114 (HTTP semantics, caching, HTTP/1.1, HTTP/2, HTTP/3), RFC 9745 (Deprecation header), RFC 8594 (Sunset), RFC 8259 (JSON), RFC 7493 (I-JSON), RFC 7396 (JSON Merge Patch), RFC 9562 (UUIDs, obsoletes RFC 4122), RFC 3339, RFC 3986, RFC 4180 (CSV), RFC 5322, RFC 5987, RFC 2119, RFC 7208 (SPF), RFC 6376 (DKIM), RFC 9989 (DMARC; RFC 7489 earlier), RFC 8058 (one-click unsubscribe), RFC 9364 (DNSSEC BCP), RFC 7643/7644 (SCIM 2.0), RFC 6238 (TOTP), RFC 3161, RFC 8996, RFC 7465, RFC 9091, RFC 793 (TCP)
- NIST — https://www.nist.gov/ and https://csrc.nist.gov/ — AI Risk Management Framework 1.0 and NIST AI 600-1 (Generative AI Profile); SP 800-218 SSDF 1.1 (and 1.2 initial public draft); SP 800-207 Zero Trust Architecture; SP 800-63B; SP 800-57; NIST CSF
- PCI Security Standards Council — https://www.pcisecuritystandards.org/document_library/ — PCI DSS v4.0.1 (v4.0 also named)
- AICPA — aicpa-cima.com — SOC 2, 2017 Trust Services Criteria (With Revised Points of Focus)
- IFRS Foundation — https://www.ifrs.org/ — IFRS 18 (page cited); also named IFRS 3, 9, 15, 16; IAS 1, 2, 7, 8, 10, 12, 16, 17, 19, 20, 21, 23, 24, 34, 36, 37, 39, 40, 41; IPSAS
- European Union — https://eur-lex.europa.eu/eli/reg/2026/1744/oj and artificialintelligenceact.eu — EU AI Act (Regulation (EU) 2024/1689), Regulation (EU) 2026/1744 (Digital Omnibus deferrals); GDPR (Arts. 5, 12, 17, 20, 33)
- U.S. HHS — hhs.gov/hipaa — HIPAA Security Rule (45 CFR §164) and NPRM
- Uganda Personal Data Protection Office — https://pdpo.go.ug/ — Data Protection and Privacy Act 2019 (DPPA) and Data Protection and Privacy Regulations 2021
- Uganda Revenue Authority — https://ura.go.ug/en/efris/ — EFRIS overview, EFRIS handbook, EFRIS registration (efris.ura.go.ug also named)
- Other privacy laws named without URLs — Kenya Data Protection Act 2019, South Africa POPIA, Nigeria NDPR, CCPA
- CIS (Center for Internet Security) — https://www.cisecurity.org/cis-benchmarks — CIS Benchmarks (incl. CIS Debian 12), CIS Controls
- OpenAPI Initiative — spec.openapis.org — OpenAPI 3.1 (3.1.2), OpenAPI 3.2, 3.0
- AsyncAPI Initiative — asyncapi.com — AsyncAPI 3.1.0
- JSON Schema — https://json-schema.org/specification — JSON Schema 2020-12 (Draft 07 also named)
- Model Context Protocol — modelcontextprotocol.io/specification — MCP specification revision 2026-07-28
- OpenSSF SLSA — https://slsa.dev/spec/v1.2/ — SLSA v1.2 build requirements (v1.0 also named)
- OpenTelemetry — https://opentelemetry.io/ — Java intro/status, docs, specification; OpenLineage 2-0-2 JSON schema (https://openlineage.io/)
- DORA — https://dora.dev/guides/dora-metrics/ — five software delivery metrics
- FinOps Foundation — https://www.finops.org/framework/ — FinOps Framework
- Agent Skills — https://agentskills.io/specification — Agent Skills specification
- MITRE — MITRE ATLAS (atlas-data releases v2026.09)
- Other named specifications without URLs — OAuth 2.0/2.1, OpenID Connect, SAML 2.0, SCIM 2.0, WebAuthn/FIDO2, SPIFFE/SPIRE (spiffe.io), Sigstore, CycloneDX, SPDX, PSR-1/4/5/7/11/12/15, PEP 602/612/639/668/695/735, ECMAScript (ES2022), E.164, GS1, Keep a Changelog (https://keepachangelog.com/), Semantic Versioning, 12-Factor App, IEC 62304, DO-178C, Relay cursor connection spec (relay.dev), Standard Webhooks
- WHO — https://www.who.int/activities/promoting-safe-food-handling/five-key-to-safer-food — Five Keys to Safer Food
- Cisco — https://sec.cloudapps.cisco.com/security/center/resources/IOS_XE_hardening — Cisco IOS XE Software Hardening Guide
- ISC — https://www.isc.org/bind/ — BIND 9 status and downloads

Official vendor and project documentation:

- OpenAI — https://developers.openai.com/ and https://platform.openai.com/ — API docs, models catalogue (GPT-6 Astra, GPT-6 Luna, GPT-5.6 Luna, all models), latest-model guidance, prompt engineering, evals, safety best practices, image generation and prompting, structured outputs, embeddings, crawlers (bots), changelog, Codex docs; help.openai.com (ChatGPT Work and Codex availability; Codex with ChatGPT plan); learn.chatgpt.com (subagents, config reference); GPT-6 Astra safety overview (openai.com/index)
- Anthropic — https://docs.anthropic.com/, https://platform.claude.com/, https://code.claude.com/ — Claude Code docs and best practices, prompt templates and variables, tool use overview, prompt caching, structured outputs (docs.claude.com also named)
- Google — https://developers.google.com/ and https://ai.google.dev/ — Search Essentials, AI-features optimisation guide, generative-AI content, snippets, crawlable links, LocalBusiness structured data; ML Kit (text recognition v2), MediaPipe, LiteRT, Gemini function calling, Play services setup; Gmail sender guidelines and FAQ (support.google.com); Google Cloud Billing docs; web.dev (Web Vitals, Optimize LCP, bfcache, Fetch Priority, PWA install criteria); developer.chrome.com (Long Animation Frames, Prerender pages, Workbox)
- Android Developers — https://developer.android.com/ — AICore, Compose side effects, edge-to-edge, games optimisation and frame pacing, Room, DataStore, testing and Espresso
- Apple Developer — https://developer.apple.com/documentation/ — Apple Developer Documentation, WWDC26 design and iOS guides, WWDC26 session 262, WWDC24 session 10179, Xcode what's new, Swift Testing, SwiftData, ARKit, visionOS, Human Interface Guidelines, upcoming requirements
- Microsoft Learn — https://learn.microsoft.com/ — Microsoft Lifecycle, PowerShell support lifecycle, ShouldProcess, PSScriptAnalyzer approved verbs, Windows security baselines, Security Compliance Toolkit, Intune security baselines, Windows Server docs, SmartScreen reputation; TypeScript devblog (devblogs.microsoft.com)
- Oracle — https://docs.oracle.com/ and https://www.oracle.com/java/ — Java SE Support Roadmap, JDK 25/26 release notes, Java SE 25/26 API docs (virtual threads, StructuredTaskScope, records, pattern matching), JLS/JVMS SE 25, JDBC tutorial, Oracle Database 26ai JDBC and UCP guides (Application Continuity), WebLogic Server 15.1.1, JDBC downloads
- OpenJDK and Adoptium — https://openjdk.org/ (JEP 444), https://jdk.java.net/, https://adoptium.net/support/
- Spring — https://spring.io/projects/ and https://docs.spring.io/ — Spring Boot (actuator, external config, graceful shutdown), Framework (beans, transactions, WebMVC, WebFlux), Security, Data JPA/Commons, Batch, Integration, Kafka (exactly-once), Modulith, Spring AI, release highlights
- Eclipse Foundation Jakarta EE — https://jakarta.ee/ — release index, Jakarta EE 11 (platform spec), EE 9/10, Persistence 3.2, Messaging 3.1, Transactions 2.0, compatibility
- Java ecosystem projects — Hibernate ORM (https://hibernate.org/orm/ and docs.hibernate.org user guide), Apache Maven (download), Gradle (releases), Quarkus (releases, native image, virtual threads), Micronaut (release index, guide), Helidon (docs v4), GraalVM (release calendar, Native Image reference), JUnit 6.1 release notes, Testcontainers for Java, ArchUnit, Micrometer support, jOOQ manual, Flyway (documentation.red-gate.com), Liquibase preconditions, Red Hat JBoss EAP 8.1, Open Liberty, IBM WebSphere Liberty support, Apache Kafka design docs, Kotlin coding conventions
- Kubernetes and CNCF projects — https://kubernetes.io/docs/ — components, resource quotas, Pod Security Standards, RBAC, kubeadm create/upgrade; Helm charts docs, cert-manager, kind, krew, metrics-server, Kyverno, OPA Gatekeeper, Argo CD, Flux, Prometheus naming practices, OpenCost, Falco, Trivy, Karpenter, vCluster (loft.sh)
- Stripe — https://docs.stripe.com/ — Payments, PaymentIntents, accept a payment, idempotent requests, webhooks and event types, testing, currencies, Stripe Tax, tax IDs, Billing subscriptions and schedules, Invoicing, prices API
- PostgreSQL — https://www.postgresql.org/ — versioning policy; docs on identity columns, JSON types, text search, pattern matching, UUID functions, RETURNING, continuous archiving; PgBouncer features
- PHP — https://www.php.net/ — supported versions, security manual, ini list; Composer
- Python — https://docs.python.org/3/ — pathlib; devguide versions; packaging.python.org (pyproject.toml); pytest (skipping); uv (docs.astral.sh); pandas 3.0.0 what's new; PyInstaller (spec files, operating mode, runtime info, pitfalls); Nuitka user manual; Inno Setup (jrsoftware.org, signed uninstaller)
- React and front-end — https://react.dev/ (docs, versions, blog), https://nextjs.org/docs (upgrading to v15 and v16), React Native (new architecture, accessibility, versions), Expo (EAS, versions), Vite (Vite 8 announcement, releases), Playwright (intro, locators, fixtures, parallel, network, auth, snapshots, accessibility testing, ARIA snapshots, CI), Cypress, MDN (prefers-reduced-motion, Service Worker API), Material Design 3 (m3.material.io), shadcn/ui, Radix UI, Dexie.js, Fastify, Prisma, Apollo GraphQL, Turborepo schema, DataTables, Vico chart guide, Stryker, fast-check
- GitHub and GitLab — https://docs.github.com/ — Actions workflow syntax, reusable workflows, GITHUB_TOKEN, secure use; GitHub CLI; GitLab CI docs
- Cloud and infrastructure — AWS (Bedrock Agents, WAF developer guide, Well-Architected), HashiCorp (Terraform backends and module registry, Vault docs), OpenTofu state encryption, Ansible playbooks and roles, Docker build cache, Terratest, Infracost, Caddy automatic HTTPS, NGINX docs (beginner's guide, limit_req), HAProxy 3.0 configuration and management, Kong Gateway, Traefik middlewares, Cloudflare (WAF, Workers, IP lists), Let's Encrypt, Hetzner Cloud, Debian Hardening wiki, Ubuntu Security, nftables wiki, GNU Bash manual, ShellCheck wiki, Git docs, smallstep, Jenkins packages, Chocolatey
- AI and data tooling — Pinecone, Weaviate, Qdrant, Chroma, pgvector, LangChain (RAG tutorial), LlamaIndex (production RAG, LlamaParse), Ragas metrics, Evidently, Cohere (Rerank, embeddings), Voyage AI, Supabase (AI guides, RLS), Ollama, n8n, Temporal (retry policies), BullMQ, Apache Airflow, gRPC (core concepts, deadlines, cancellation), RabbitMQ (confirms, reliability)
- Observability and security tools — SigNoz, Sentry, Grafana alerting, VictoriaMetrics, PostHog docs, Metabase docs, Snyk (tool named), Mozilla Observatory, securityheaders.com, SSL Labs, HSTS preload, DNSViz, WireGuard, fastlane, semantic-release
- GIS and mapping — OpenStreetMap Nominatim usage policy (operations.osmfoundation.org), Geofabrik downloads, OSRM, Photon, Esri ArcGIS Online, EPSG.io, Mapbox and Google Maps Platform APIs
- Games and graphics — Vulkan specification and guide (docs.vulkan.org), Unity 6 support and Profiler manual
- Email deliverability — Yahoo Sender Best Practices (https://senders.yahooinc.com/best-practices/)

### Websites and articles

- C4 model — https://c4model.com/ — Simon Brown's C4 model; container and component abstractions (/abstractions/container, /abstractions/component); site licence CC BY 4.0
- Impeccable — https://impeccable.style/slop/ — Impeccable Slop catalogue (first-party web-interface AI-slop taxonomy)
- arXiv — https://arxiv.org/ — Kobak et al., "Delving into LLM-assisted writing in biomedical publications through excess vocabulary" (abs/2406.07016); "Interpretable Stylistic Variation in Human and LLM Writing Across Genres, Models, and Decoding Strategies" (abs/2604.14111); Liang et al., "GPT detectors are biased against non-native English writers" (abs/2304.02819); Gao, Ma, Lin & Callan, "Precise Zero-Shot Dense Retrieval without Relevance Labels" (HyDE, abs/2212.10496); Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" (abs/2310.11511)
- Anthropic news — anthropic.com/news/contextual-retrieval — "Contextual Retrieval"
- Eleken blog — https://www.eleken.co/blog-posts/ — product-idea validation, launching a SaaS business, startup scaling from a product-design view, AI design workflow, 18 UX improvements that move product metrics, 16 best dashboard design examples, "Compelling Design Takes More Than 'Making It Like Stripe'"
- Instrument — https://www.instrument.com/about — About page
- PagerDuty Incident Response — response.pagerduty.com — severity levels and incident roles
- Snyk ToxicSkills scan (5 Feb 2026) — cited without URL (534 of 3,984 public skills with at least one critical issue)
- OpenView PLG Index — openviewpartners.com
- Baremetrics Open Benchmarks — baremetrics.com/open
- Square POS product docs — squareup.com (industry reference)
- Wikipedia — en.wikipedia.org/wiki/FIFO_and_LIFO_accounting — FIFO and LIFO accounting
- Name-data sources for synthetic seeding — U.S. Social Security Administration baby-name data (https://www.ssa.gov/oact/babynames/limits.html), UK Office for National Statistics 500 most common surnames (https://www.ons.gov.uk/), Behind the Name Arabic names and surnames (https://www.behindthename.com/)
