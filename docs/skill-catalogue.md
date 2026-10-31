# Skill catalogue

Every active skill in this engine, by category: 167 skills in 18 categories. An active skill is a `SKILL.md` under `skills/` or `00-meta-initialization/`. The 78 inactive `ALIAS.md` redirects are excluded, and [`skill-routing-index.md`](skill-routing-index.md) maps retired names to current skills. The root [`SKILL.md`](../SKILL.md) is the engineering baseline router and is not counted.

Not sure which skill you need? Start with [Find the right skill](../README.md#find-the-right-skill) in the root README.

When a skill is added or retired, update this page and the count in the root README section "Catalogue size" in the same change. The test suite checks the README count against the files on disk. It does not check this page.

Jump to a category:

- [Project initialisation](#project-initialisation)
- [SDLC and engineering method](#sdlc-and-engineering-method)
- [Execution planning](#execution-planning)
- [Architecture](#architecture)
- [Backend and databases](#backend-and-databases)
- [Security](#security)
- [Languages](#languages)
- [Frontend and UX engineering](#frontend-and-ux-engineering)
- [Android](#android)
- [iOS](#ios)
- [Cross-platform mobile](#cross-platform-mobile)
- [AI and agent systems](#ai-and-agent-systems)
- [SaaS platforms](#saas-platforms)
- [Product and business](#product-and-business)
- [Finance implementation](#finance-implementation)
- [DevOps and cloud](#devops-and-cloud)
- [Game development](#game-development)
- [GIS](#gis)

## Project initialisation

2 skills in [`00-meta-initialization/`](../00-meta-initialization/).

| Skill | What it does |
|---|---|
| [`00-meta-initialization`](../00-meta-initialization/SKILL.md) | Selects Waterfall, Agile or Hybrid delivery and generates the governed document sequence for a new project. |
| [`new-project`](../00-meta-initialization/new-project/SKILL.md) | Scaffolds a new project using the engine's new-project workflow. |

## SDLC and engineering method

20 skills in [`skills/sdlc-meta/`](../skills/sdlc-meta/).

| Skill | What it does |
|---|---|
| [`advanced-testing-strategy`](../skills/sdlc-meta/advanced-testing-strategy/SKILL.md) | Designs risk-based unit, integration, contract, end-to-end and release-gate test strategy. |
| [`ai-assisted-development`](../skills/sdlc-meta/ai-assisted-development/SKILL.md) | Coordinates AI-assisted planning, implementation and review of AI-generated changes. |
| [`ai-slop-audit`](../skills/sdlc-meta/ai-slop-audit/SKILL.md) | Scores an artefact for AI slop with evidence, severity, fixes and an A/B/C/F verdict. |
| [`anti-ai-slop`](../skills/sdlc-meta/anti-ai-slop/SKILL.md) | Applies real-time anti-slop controls to any human-facing artefact. |
| [`council`](../skills/sdlc-meta/council/SKILL.md) | Convenes a four-voice council for ambiguous trade-offs and go/no-go decisions. |
| [`doc-architect`](../skills/sdlc-meta/doc-architect/SKILL.md) | Generates and repairs AGENTS.md/CLAUDE.md guidance, project docs and CodeTour walkthroughs. |
| [`engine-control-plane`](../skills/sdlc-meta/engine-control-plane/SKILL.md) | Coordinates multi-engine workflows, roles, hooks, evidence contracts and handoffs. |
| [`git-collaboration-workflow`](../skills/sdlc-meta/git-collaboration-workflow/SKILL.md) | Plans branches, commits, reviews, conflict resolution, pull requests and releases. |
| [`github-ops`](../skills/sdlc-meta/github-ops/SKILL.md) | Runs GitHub operations via gh: triage, CI status, releases, alerts and open-sourcing. |
| [`implementation-status-auditor`](../skills/sdlc-meta/implementation-status-auditor/SKILL.md) | Audits real implementation status against requirements and plans with a completion blueprint. |
| [`kaizen-improvement-system`](../skills/sdlc-meta/kaizen-improvement-system/SKILL.md) | Runs evidence-backed baselines, small experiments and re-audits of the engine or its products. |
| [`project-requirements`](../skills/sdlc-meta/project-requirements/SKILL.md) | Interviews stakeholders and produces traceable requirements and acceptance criteria. |
| [`santa-method`](../skills/sdlc-meta/santa-method/SKILL.md) | Requires output to pass two independent adversarial reviewers before it ships. |
| [`sdlc-documentation`](../skills/sdlc-meta/sdlc-documentation/SKILL.md) | Produces and consolidates SDLC documentation from planning to maintenance. |
| [`skill-composition-standards`](../skills/sdlc-meta/skill-composition-standards/SKILL.md) | Enforces house style, boundaries and input/output contracts for skills. |
| [`skill-engine-audit`](../skills/sdlc-meta/skill-engine-audit/SKILL.md) | Audits, grades and benchmarks skill engines and safety-gates new or imported skills. |
| [`skill-writing`](../skills/sdlc-meta/skill-writing/SKILL.md) | Authors and upgrades SKILL.md files with triggers, progressive disclosure and evidence contracts. |
| [`systematic-bug-diagnosis`](../skills/sdlc-meta/systematic-bug-diagnosis/SKILL.md) | Reproduces defects and diagnoses causes from evidence before any fix. |
| [`world-class-bid-red-team-and-delivery-qc`](../skills/sdlc-meta/world-class-bid-red-team-and-delivery-qc/SKILL.md) | Applies the final quality gate to high-stakes bids and consulting deliverables. |
| [`world-class-engineering`](../skills/sdlc-meta/world-class-engineering/SKILL.md) | Sets the production engineering baseline and the verify-before-done gate. |

## Execution planning

1 skills in [`skills/execution-plan-scripts/`](../skills/execution-plan-scripts/).

| Skill | What it does |
|---|---|
| [`execution-plan-scripts`](../skills/execution-plan-scripts/SKILL.md) | Turns an approved long-running plan into self-contained, ordered execution prompts with checkpoints. |

## Architecture

7 skills in [`skills/architecture/`](../skills/architecture/).

| Skill | What it does |
|---|---|
| [`api-design-first`](../skills/architecture/api-design-first/SKILL.md) | Designs HTTP APIs with OpenAPI, versioning, auth, idempotency and error contracts. |
| [`distributed-systems-patterns`](../skills/architecture/distributed-systems-patterns/SKILL.md) | Designs message-driven systems with outbox/inbox, sagas, ordering and idempotency. |
| [`ecommerce-platform-audit-requirements`](../skills/architecture/ecommerce-platform-audit-requirements/SKILL.md) | Scopes e-commerce platform, payment, security and data-protection audits. |
| [`graphql-patterns`](../skills/architecture/graphql-patterns/SKILL.md) | Designs GraphQL schemas, resolvers, authorisation, federation and hostile-input controls. |
| [`microservices-architecture`](../skills/architecture/microservices-architecture/SKILL.md) | Sets microservice boundaries, communication, ownership and resilience. |
| [`system-architecture-design`](../skills/architecture/system-architecture-design/SKILL.md) | Defines system architecture: bounded contexts, modules, ports and adapters, evidence-pinned diagrams. |
| [`validation-contract`](../skills/architecture/validation-contract/SKILL.md) | Defines the seven evidence categories and the Release Evidence Bundle for specialist skills. |

## Backend and databases

4 skills in [`skills/backend-databases/`](../skills/backend-databases/).

| Skill | What it does |
|---|---|
| [`database-design-engineering`](../skills/backend-databases/database-design-engineering/SKILL.md) | Designs relational and document data models, tenancy, indexing and migrations. |
| [`database-reliability`](../skills/backend-databases/database-reliability/SKILL.md) | Sets database SLOs, backup verification, capacity policy and on-call practice. |
| [`mysql-engineering`](../skills/backend-databases/mysql-engineering/SKILL.md) | Designs, tunes, backs up, restores and troubleshoots MySQL in production. |
| [`postgresql-engineering`](../skills/backend-databases/postgresql-engineering/SKILL.md) | Designs, tunes, backs up, restores and troubleshoots PostgreSQL in production. |

## Security

6 skills in [`skills/security/`](../skills/security/).

| Skill | What it does |
|---|---|
| [`code-safety-scanner`](../skills/security/code-safety-scanner/SKILL.md) | Scans code and agent configuration before deployment for critical vulnerabilities. |
| [`dpia-generator`](../skills/security/dpia-generator/SKILL.md) | Produces Data Protection Impact Assessments, including for Uganda DPPA processing. |
| [`linux-security-hardening`](../skills/security/linux-security-hardening/SKILL.md) | Hardens and audits Debian/Ubuntu hosts against CIS controls. |
| [`network-security`](../skills/security/network-security/SKILL.md) | Designs firewalls, WAF, VPN, TLS/PKI, IDS/IPS, segmentation and DDoS controls. |
| [`vibe-security-skill`](../skills/security/vibe-security-skill/SKILL.md) | Produces threat models, abuse cases, authorisation matrices and OWASP-aligned evidence. |
| [`web-app-security-audit`](../skills/security/web-app-security-audit/SKILL.md) | Audits PHP/JavaScript web apps for vulnerabilities with a severity-rated report. |

## Languages

12 skills in [`skills/languages/`](../skills/languages/).

| Skill | What it does |
|---|---|
| [`algorithm-selection-and-complexity`](../skills/languages/algorithm-selection-and-complexity/SKILL.md) | Chooses and explains algorithms under explicit correctness and complexity constraints. |
| [`csharp-dotnet-development`](../skills/languages/csharp-dotnet-development/SKILL.md) | Builds and modernises C#/.NET apps: ASP.NET Core, EF Core, MAUI and tests. |
| [`java-enterprise-development`](../skills/languages/java-enterprise-development/SKILL.md) | Builds and modernises Java/JVM services with Spring Boot, Jakarta EE and Hibernate. |
| [`javascript-modern`](../skills/languages/javascript-modern/SKILL.md) | Writes modern JavaScript: modules, async flows, error handling and performance. |
| [`nodejs-development`](../skills/languages/nodejs-development/SKILL.md) | Builds Node.js services, APIs, workers and CLIs with logging, tests and scaling. |
| [`php-modern-standards`](../skills/languages/php-modern-standards/SKILL.md) | Writes PHP 8+ and Laravel code to PSR standards, with current security-patch and staged runtime-upgrade guidance. |
| [`python-data-analytics`](../skills/languages/python-data-analytics/SKILL.md) | Computes KPIs, cohorts, financial maths and statistical tests in Python and pandas. |
| [`python-data-pipelines`](../skills/languages/python-data-pipelines/SKILL.md) | Builds idempotent Python ETL, OCR and document-ingestion pipelines. |
| [`python-ml-predictive`](../skills/languages/python-ml-predictive/SKILL.md) | Adds forecasting, classification and anomaly detection with scikit-learn, Prophet and statsmodels. |
| [`python-modern-standards`](../skills/languages/python-modern-standards/SKILL.md) | Sets the Python baseline, packaging and frozen-executable release builds. |
| [`typescript-effective`](../skills/languages/typescript-effective/SKILL.md) | Writes production TypeScript with strict configuration, migration and testing. |
| [`typescript-full-stack`](../skills/languages/typescript-full-stack/SKILL.md) | Builds end-to-end type-safe TypeScript apps with tRPC/Zod, Prisma/Drizzle and monorepos. |

## Frontend and UX engineering

9 skills in [`skills/frontend-ux/`](../skills/frontend-ux/).

| Skill | What it does |
|---|---|
| [`avalonia-desktop-development`](../skills/frontend-ux/avalonia-desktop-development/SKILL.md) | Builds cross-platform .NET desktop apps with Avalonia, MVVM and headless tests. |
| [`frontend-architecture`](../skills/frontend-ux/frontend-architecture/SKILL.md) | Turns design systems and requirements into component, state and delivery architecture. |
| [`frontend-performance`](../skills/frontend-ux/frontend-performance/SKILL.md) | Sets per-flow frontend performance budgets, measurement plans and CI regression gates. |
| [`image-compression`](../skills/frontend-ux/image-compression/SKILL.md) | Implements client image optimisation with authoritative server-side validation and re-encoding. |
| [`nextjs-app-router`](../skills/frontend-ux/nextjs-app-router/SKILL.md) | Implements Next.js App Router server/client components, caching, auth and streaming. |
| [`pos-sales-operations-engineering`](../skills/frontend-ux/pos-sales-operations-engineering/SKILL.md) | Implements tenant-aware POS and sales entry with stock, payment and audit-safe posting. |
| [`react-development`](../skills/frontend-ux/react-development/SKILL.md) | Implements React components, hooks, state, forms and component tests. |
| [`tailwind-css`](../skills/frontend-ux/tailwind-css/SKILL.md) | Implements Tailwind CSS layouts, variants, theme tokens and build configuration. |
| [`ux-content-strategy`](../skills/frontend-ux/ux-content-strategy/SKILL.md) | Governs product content: voice, UI text patterns, error taxonomy and content measurement. |

## Android

1 skills in [`skills/android/`](../skills/android/).

| Skill | What it does |
|---|---|
| [`android-development`](../skills/android/android-development/SKILL.md) | Builds native Android apps with Kotlin, Compose, Room, offline sync and tests. |

## iOS

4 skills in [`skills/ios/`](../skills/ios/).

| Skill | What it does |
|---|---|
| [`ios-development`](../skills/ios/ios-development/SKILL.md) | Builds native iOS apps with Swift, SwiftUI, structured concurrency and tests. |
| [`ios-monetization`](../skills/ios/ios-monetization/SKILL.md) | Implements StoreKit 2 purchases, subscriptions, entitlements and App Store server events. |
| [`ios-platform-capabilities`](../skills/ios/ios-platform-capabilities/SKILL.md) | Integrates App Intents, SwiftData, notifications, Core ML, Vision and other iOS capabilities. |
| [`ios-security-and-rbac`](../skills/ios/ios-security-and-rbac/SKILL.md) | Designs iOS authentication, Keychain, App Attest, privacy manifests and RBAC. |

## Cross-platform mobile

3 skills in [`skills/mobile-cross/`](../skills/mobile-cross/).

| Skill | What it does |
|---|---|
| [`kmp-development`](../skills/mobile-cross/kmp-development/SKILL.md) | Shares Kotlin business logic across Android and iOS with Kotlin Multiplatform. |
| [`mobile-platform-operations`](../skills/mobile-cross/mobile-platform-operations/SKILL.md) | Coordinates Android/iOS signing, store review, TestFlight, staged release and rollback. |
| [`pwa-offline-first`](../skills/mobile-cross/pwa-offline-first/SKILL.md) | Builds offline-first PWAs with Service Workers, Workbox, IndexedDB and Background Sync. |

## AI and agent systems

26 skills in [`skills/ai/`](../skills/ai/).

| Skill | What it does |
|---|---|
| [`ai-agent-commercial-operations`](../skills/ai/ai-agent-commercial-operations/SKILL.md) | Prices, bills and sets SLAs, credits and service evidence for agentic AI services. |
| [`ai-agent-compliance-controls`](../skills/ai/ai-agent-compliance-controls/SKILL.md) | Maps agent operations to SOC 2, ISO 27001 and HIPAA controls with audit evidence. |
| [`ai-agent-governance-and-limits`](../skills/ai/ai-agent-governance-and-limits/SKILL.md) | Sets agent budgets, step limits, blast-radius controls and kill switches. |
| [`ai-agent-multi-agent-coordination`](../skills/ai/ai-agent-multi-agent-coordination/SKILL.md) | Designs supervisor/worker, debate and handoff topologies with conflict and deadlock handling. |
| [`ai-agent-observability-evaluation`](../skills/ai/ai-agent-observability-evaluation/SKILL.md) | Measures, replays and evidences agent task, step and trace outcomes. |
| [`ai-agent-runtime-architecture`](../skills/ai/ai-agent-runtime-architecture/SKILL.md) | Designs multi-tenant agent runtimes: control loops, state, retries, resumability and cancellation. |
| [`ai-agent-safety-and-red-team`](../skills/ai/ai-agent-safety-and-red-team/SKILL.md) | Red-teams agent tool and data perimeters for injection, escalation and exfiltration. |
| [`ai-agent-tooling-and-hitl`](../skills/ai/ai-agent-tooling-and-hitl/SKILL.md) | Designs agent tool catalogues, schemas, action gating and human approval. |
| [`ai-analytics`](../skills/ai/ai-analytics/SKILL.md) | Designs AI analytics, SaaS AI metrics, predictive analytics and executive insight workflows. |
| [`ai-app-architecture`](../skills/ai/ai-app-architecture/SKILL.md) | Chooses architecture, components and build-versus-buy for AI-powered applications. |
| [`ai-cost-and-metering`](../skills/ai/ai-cost-and-metering/SKILL.md) | Models, meters, attributes and controls AI usage cost by tenant, plan and feature. |
| [`ai-economic-value-engine`](../skills/ai/ai-economic-value-engine/SKILL.md) | Tests AI product ideas for measurable business value and ROI. |
| [`ai-evaluation`](../skills/ai/ai-evaluation/SKILL.md) | Builds LLM evaluation harnesses, golden datasets, judge calibration and regression gates. |
| [`ai-feature-rollout-and-experimentation`](../skills/ai/ai-feature-rollout-and-experimentation/SKILL.md) | Runs flagged, canary and A/B rollouts of AI features behind eval and SLO gates. |
| [`ai-feature-spec`](../skills/ai/ai-feature-spec/SKILL.md) | Specifies one AI feature end to end: model, prompt contract, schema, fallbacks and evaluation. |
| [`ai-incident-response`](../skills/ai/ai-incident-response/SKILL.md) | Detects, triages, recovers from and reviews AI incidents. |
| [`ai-llm-integration`](../skills/ai/ai-llm-integration/SKILL.md) | Integrates LLM providers with streaming, structured output, tool calls, retries and caching. |
| [`ai-model-gateway`](../skills/ai/ai-model-gateway/SKILL.md) | Designs an LLM gateway for routing, fallbacks, quotas, residency and audit logging. |
| [`ai-observability-and-debugging`](../skills/ai/ai-observability-and-debugging/SKILL.md) | Traces prompts and responses, replays answers and breaks down AI latency and cost. |
| [`ai-opportunity-canvas`](../skills/ai/ai-opportunity-canvas/SKILL.md) | Ranks AI use cases into an opportunity register by impact, effort, cost and risk. |
| [`ai-prompt-engineering`](../skills/ai/ai-prompt-engineering/SKILL.md) | Writes and versions system prompts, templates, few-shot examples and defensive prompts. |
| [`ai-rag-patterns`](../skills/ai/ai-rag-patterns/SKILL.md) | Builds retrieval-augmented generation: chunking, hybrid search, re-ranking and evaluation. |
| [`ai-security`](../skills/ai/ai-security/SKILL.md) | Secures LLM features against prompt injection, tenant leakage, jailbreaks and PII exposure. |
| [`ai-web-apps`](../skills/ai/ai-web-apps/SKILL.md) | Builds AI-enhanced web apps with chat, RAG, MCP tools, streaming and guardrails. |
| [`coding-agent-optimization`](../skills/ai/coding-agent-optimization/SKILL.md) | Tunes Claude Code and Codex set-ups for context, model, permission and token efficiency. |
| [`openai-agents-sdk`](../skills/ai/openai-agents-sdk/SKILL.md) | Builds Python agents on the OpenAI Agents SDK with tools, handoffs, guardrails and tracing. |

## SaaS platforms

18 skills in [`skills/saas/`](../skills/saas/).

| Skill | What it does |
|---|---|
| [`full-coverage-saas-seeding`](../skills/saas/full-coverage-saas-seeding/SKILL.md) | Seeds and verifies a realistic synthetic SaaS demo tenant across all modules. |
| [`modular-saas-architecture`](../skills/saas/modular-saas-architecture/SKILL.md) | Designs tenant-selectable SaaS modules with dependency contracts and safe toggles. |
| [`multi-tenant-saas-architecture`](../skills/saas/multi-tenant-saas-architecture/SKILL.md) | Designs tenant isolation, panel boundaries, zero-trust authorisation and audit trails. |
| [`saas-accounting-system`](../skills/saas/saas-accounting-system/SKILL.md) | Designs double-entry accounting inside SaaS with automated postings and reconciliations. |
| [`saas-admin-backoffice-tooling`](../skills/saas/saas-admin-backoffice-tooling/SKILL.md) | Designs audited back-office impersonation, tenant lifecycle and billing overrides. |
| [`saas-architecture-strategy`](../skills/saas/saas-architecture-strategy/SKILL.md) | Chooses multi-tenant patterns, deployment mapping, scaling and blast-radius isolation. |
| [`saas-business-metrics`](../skills/saas/saas-business-metrics/SKILL.md) | Defines SaaS revenue, retention, unit-economics and Rule-of-40 metrics. |
| [`saas-entitlements-and-plan-gating`](../skills/saas/saas-entitlements-and-plan-gating/SKILL.md) | Gates seats, quotas, AI tiers and tools by plan with tenant overrides. |
| [`saas-erp-system-design`](../skills/saas/saas-erp-system-design/SKILL.md) | Designs configurable SaaS/ERP platforms with workflows, approvals and tenant variation. |
| [`saas-lifecycle-email-orchestration`](../skills/saas/saas-lifecycle-email-orchestration/SKILL.md) | Derives lifecycle email decisions from user state, events, consent and suppression. |
| [`saas-managed-visual-assets`](../skills/saas/saas-managed-visual-assets/SKILL.md) | Implements secure upload, activation and audit of managed logos, favicons and backgrounds. |
| [`saas-rate-limiting-and-quotas`](../skills/saas/saas-rate-limiting-and-quotas/SKILL.md) | Designs per-tenant rate limits, quota algorithms and fair queueing. |
| [`saas-sales-organization`](../skills/saas/saas-sales-organization/SKILL.md) | Designs SaaS sales motions, roles, pipeline stages, territories and compensation. |
| [`saas-seeder`](../skills/saas/saas-seeder/SKILL.md) | Bootstraps the multi-tenant SaaS Seeder Template with super admin and demo logins. |
| [`saas-sso-scim-enterprise-auth`](../skills/saas/saas-sso-scim-enterprise-auth/SKILL.md) | Implements tenant-scoped SAML/OIDC SSO, SCIM provisioning and IP allowlists. |
| [`saas-tenant-data-portability-and-erasure`](../skills/saas/saas-tenant-data-portability-and-erasure/SKILL.md) | Designs verified tenant data export, retention and erasure workflows. |
| [`stripe-payments`](../skills/saas/stripe-payments/SKILL.md) | Integrates Stripe PaymentIntents, Checkout, SCA, idempotency and webhooks. |
| [`subscription-billing`](../skills/saas/subscription-billing/SKILL.md) | Designs Stripe Billing subscriptions: trials, proration, dunning, metered usage and tax. |

## Product and business

15 skills in [`skills/product-business/`](../skills/product-business/).

| Skill | What it does |
|---|---|
| [`bds-intake-and-monitoring-system-spec`](../skills/product-business/bds-intake-and-monitoring-system-spec/SKILL.md) | Specifies intake, scoring, beneficiary registers and donor reporting for BDS programmes. |
| [`consulting-delivery-control-room`](../skills/product-business/consulting-delivery-control-room/SKILL.md) | Runs multi-workstream bids and programmes with RACI, RAID, registers and quality gates. |
| [`content-writing`](../skills/product-business/content-writing/SKILL.md) | Writes and reviews articles, web copy and headlines for readability and structure. |
| [`customer-service-excellence`](../skills/product-business/customer-service-excellence/SKILL.md) | Handles service recovery, escalations, complaints and CX measurement. |
| [`document-spreadsheet-tooling-readiness`](../skills/product-business/document-spreadsheet-tooling-readiness/SKILL.md) | Checks the machine can generate and validate promised DOCX, PDF and XLSX files. |
| [`excel-spreadsheets`](../skills/product-business/excel-spreadsheets/SKILL.md) | Generates and validates professional Excel workbooks, formulas and charts. |
| [`hospitality-hotel-restaurant-systems`](../skills/product-business/hospitality-hotel-restaurant-systems/SKILL.md) | Architects and audits hotel PMS, restaurant POS and food-service software. |
| [`it-proposal-writing`](../skills/product-business/it-proposal-writing/SKILL.md) | Plans and strengthens IT proposals, win strategy and pricing narrative. |
| [`premium-software-product-execution`](../skills/product-business/premium-software-product-execution/SKILL.md) | Designs, prices and builds premium software for high-ticket buyers. |
| [`product-discovery`](../skills/product-business/product-discovery/SKILL.md) | Tests whether a product or feature deserves investment through prototypes and research. |
| [`product-led-growth`](../skills/product-business/product-led-growth/SKILL.md) | Designs PLG motions: freemium, PQLs, activation, upgrade prompts and viral loops. |
| [`product-strategy-vision`](../skills/product-business/product-strategy-vision/SKILL.md) | Defines product vision, principles, OKRs and outcome roadmaps. |
| [`professional-word-output`](../skills/product-business/professional-word-output/SKILL.md) | Generates and validates professionally structured Word DOCX documents. |
| [`software-business-models`](../skills/product-business/software-business-models/SKILL.md) | Selects software business models: product, service, platform, subscription or open source. |
| [`software-pricing-strategy`](../skills/product-business/software-pricing-strategy/SKILL.md) | Designs software pricing, packaging, value metrics, tiers and willingness-to-pay tests. |

## Finance implementation

4 skills in [`skills/finance-accounting/`](../skills/finance-accounting/).

| Skill | What it does |
|---|---|
| [`accounting-engine`](../skills/finance-accounting/accounting-engine/SKILL.md) | Implements a double-entry ledger engine with balanced postings, reversals and period locks. |
| [`accounting-finance-controller`](../skills/finance-accounting/accounting-finance-controller/SKILL.md) | Coordinates accounting implementation reviews, doctrine routing and control evidence. |
| [`electronic-fiscal-taxing`](../skills/finance-accounting/electronic-fiscal-taxing/SKILL.md) | Implements electronic fiscal tax integrations (e.g. URA EFRIS) with adapters and offline queues. |
| [`multicurrency-and-fx`](../skills/finance-accounting/multicurrency-and-fx/SKILL.md) | Implements IAS 21 multicurrency accounting, rate tables and FX gain/loss revaluation. |

## DevOps and cloud

8 skills in [`skills/devops-cloud/`](../skills/devops-cloud/).

| Skill | What it does |
|---|---|
| [`cicd-pipelines`](../skills/devops-cloud/cicd-pipelines/SKILL.md) | Builds hardened CI/CD pipelines with security stages, promotion gates and short-lived credentials. |
| [`cloud-architecture`](../skills/devops-cloud/cloud-architecture/SKILL.md) | Designs AWS/GCP deployments, containerisation and multi-AZ topologies. |
| [`deployment-release-engineering`](../skills/devops-cloud/deployment-release-engineering/SKILL.md) | Designs rollout strategies, release gates, rollback and post-deploy verification. |
| [`docker-development`](../skills/devops-cloud/docker-development/SKILL.md) | Containerises PHP, Python and JavaScript services with multi-stage images and Compose. |
| [`infrastructure-as-code`](../skills/devops-cloud/infrastructure-as-code/SKILL.md) | Provisions infrastructure with Terraform modules, remote state and idempotent Ansible roles. |
| [`kubernetes-platform`](../skills/devops-cloud/kubernetes-platform/SKILL.md) | Runs production Kubernetes: workloads, RBAC, Pod Security, autoscaling, upgrades and recovery. |
| [`observability-monitoring`](../skills/devops-cloud/observability-monitoring/SKILL.md) | Designs logs, metrics, traces, alerts, SLOs and dashboards. |
| [`reliability-engineering`](../skills/devops-cloud/reliability-engineering/SKILL.md) | Sets timeout, retry, degradation, queue-safety and incident policy for production systems. |

## Game development

25 skills in [`skills/game-development/`](../skills/game-development/).

| Skill | What it does |
|---|---|
| [`apple-game-platform-delivery`](../skills/game-development/apple-game-platform-delivery/SKILL.md) | Ships games on iOS, iPadOS and macOS with Apple services, Metal diagnostics and notarisation. |
| [`game-2d-art-animation-and-vfx-pipeline`](../skills/game-development/game-2d-art-animation-and-vfx-pipeline/SKILL.md) | Produces and optimises 2D sprites, atlases, animation, UI art and VFX. |
| [`game-3d-asset-pipeline`](../skills/game-development/game-3d-asset-pipeline/SKILL.md) | Produces game-ready 3D assets, rigs, LODs and DCC-to-engine exports. |
| [`game-accessibility-localisation-and-player-safety`](../skills/game-development/game-accessibility-localisation-and-player-safety/SKILL.md) | Designs accessible, localised games with chat safety, moderation and parental controls. |
| [`game-ai-behaviour-and-navigation`](../skills/game-development/game-ai-behaviour-and-navigation/SKILL.md) | Designs NPC behaviour, navigation, perception, behaviour trees and utility AI. |
| [`game-audio-implementation`](../skills/game-development/game-audio-implementation/SKILL.md) | Implements game music, dialogue, spatial and adaptive audio. |
| [`game-build-release-engineering`](../skills/game-development/game-build-release-engineering/SKILL.md) | Builds reproducible Unity, Godot and Unreal pipelines with signing, patching and rollback. |
| [`game-data-analytics-and-live-economy`](../skills/game-development/game-data-analytics-and-live-economy/SKILL.md) | Defines game telemetry, funnels, experiments and virtual-economy controls. |
| [`game-development-orchestration`](../skills/game-development/game-development-orchestration/SKILL.md) | Governs a game project from concept through vertical slice, production and live operations. |
| [`game-math-and-simulation`](../skills/game-development/game-math-and-simulation/SKILL.md) | Specifies vector, quaternion, collision, camera and numerical-simulation rules. |
| [`game-narrative-and-interactive-story-design`](../skills/game-development/game-narrative-and-interactive-story-design/SKILL.md) | Designs interactive stories, quests, dialogue and branching narrative. |
| [`game-security-anti-cheat-and-abuse`](../skills/game-development/game-security-anti-cheat-and-abuse/SKILL.md) | Threat-models games and designs anti-cheat, anti-bot and economy protection. |
| [`game-studio-delivery-and-commercial-operations`](../skills/game-development/game-studio-delivery-and-commercial-operations/SKILL.md) | Runs game estimation, staffing, milestones, outsourcing and launch command. |
| [`game-testing-polish`](../skills/game-development/game-testing-polish/SKILL.md) | Plans game QA, playtesting, balance, compatibility and release-candidate gates. |
| [`gameplay-systems-architecture`](../skills/game-development/gameplay-systems-architecture/SKILL.md) | Specifies engine-neutral gameplay systems: movement, combat, inventory, saves and world state. |
| [`godot-mobile-game-development`](../skills/game-development/godot-mobile-game-development/SKILL.md) | Builds, profiles and exports Godot mobile games for Android and iOS. |
| [`lean-game-product-development`](../skills/game-development/lean-game-product-development/SKILL.md) | Turns game ideas into falsifiable hypotheses, prototypes and go/pivot/stop decisions. |
| [`level-world-and-content-production`](../skills/game-development/level-world-and-content-production/SKILL.md) | Designs and produces levels, worlds, encounters and procedural content. |
| [`mobile-game-design`](../skills/game-development/mobile-game-design/SKILL.md) | Designs mobile game loops, touch controls, progression, economy and ethical monetisation. |
| [`mobile-game-performance`](../skills/game-development/mobile-game-performance/SKILL.md) | Enforces mobile-game frame, memory, battery and thermal budgets via device profiling. |
| [`mobile-game-release-liveops`](../skills/game-development/mobile-game-release-liveops/SKILL.md) | Handles mobile game store submission, IAP, staged rollout and live operations. |
| [`online-multiplayer-and-game-backend`](../skills/game-development/online-multiplayer-and-game-backend/SKILL.md) | Designs authoritative multiplayer, replication, prediction, matchmaking and game backends. |
| [`real-time-game-graphics`](../skills/game-development/real-time-game-graphics/SKILL.md) | Designs and diagnoses render pipelines, shaders, lighting and GPU budgets. |
| [`unity-mobile-game-development`](../skills/game-development/unity-mobile-game-development/SKILL.md) | Builds, profiles and packages Unity mobile games in C#. |
| [`unreal-game-development`](../skills/game-development/unreal-game-development/SKILL.md) | Builds Unreal Engine games with C++, Blueprints, replication and packaging. |

## GIS

2 skills in [`skills/gis/`](../skills/gis/).

| Skill | What it does |
|---|---|
| [`gis-enterprise-domain`](../skills/gis/gis-enterprise-domain/SKILL.md) | Administers ArcGIS Enterprise and builds real-estate GIS features. |
| [`gis-platform-engineering`](../skills/gis/gis-platform-engineering/SKILL.md) | Implements maps, geocoding, spatial APIs and PostGIS-backed platforms. |
