# Repositories, standards, official sources and articles

Sources other than books that this repository's skills, references, source registers and audits cite. Citations only: mechanisms are paraphrased and no upstream text is copied. Volatile facts such as versions and dates are held in the dated records under [`docs/source-registers/`](../source-registers/ai-platforms.md) and checked by `scripts/check_source_register.py`.

See [Cited sources](README.md) for the other source lists.

## Repositories

The ten repositories studied in the my-10-kaizen operation (29 September 2026) were superpowers, ponytail, ui-ux-pro-max-skill, graphify, caveman, agent-skills, Understand-Anything, awesome-claude-skills, archify and Impeccable. The first list below records what this engine adapted from each; the per-file record is [docs/source-registers/m10-06-third-party-attributions.md](../source-registers/m10-06-third-party-attributions.md).

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

## Standards and official sources

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

## Websites and articles

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
