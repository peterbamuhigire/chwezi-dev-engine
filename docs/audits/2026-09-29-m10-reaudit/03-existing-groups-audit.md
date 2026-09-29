# Existing groups and sampled skills

All scores judged. Structural inputs are measured: "Compliant" is the count of skills with zero
failures in `engine_compliance.py --root . --json`; "WE" is the count of active skills whose
SKILL.md or first-level reference mentions a worked example. Basis column: **sampled** means at
least one SKILL.md in the group was read in depth; **structural** means the score rests on the
measured inputs and group composition only.

## Group scores

| Group | Active | Compliant | WE | Score | Basis | Justification |
|---|---:|---:|---:|---:|---|---|
| ai | 26 | 26/26 | 8 | 57 | sampled | Broad RAG, eval, gateway, agent coverage; RAG has a real curated-corpus worked example. 19 skills share one identical generic operating contract; 12 `ai-agent-*` skills over-split; eval guidance plans runs it cannot prove. |
| android | 1 | 1/1 | 1 | 44 | sampled | One deep skill (455 lines, 17 references) but Target SDK 35 fails the Play requirement in force since 31 Aug 2026, and the edge-to-edge "crashes immediately" claim is contradicted by Android documentation. |
| architecture | 7 | 7/7 | 2 | 60 | sampled | `api-design-first` is strong: OpenAPI 3.1/3.2, RFC 9457, decision tables for auth, versioning, idempotency, caching. Duplicated contract sections; worked examples in 2 of 7. |
| backend-databases | 4 | 4/4 | 1 | 50 | sampled | MySQL 8.4 cited; PostgreSQL stops at 16, `gen_random_uuid()`/`pgcrypto` contradiction between two references, operations depth only reachable through a circular alias pointer. |
| devops-cloud | 8 | 8/8 | 3 | 58 | sampled | `cicd-pipelines` verified 2026-09-24, OIDC federation, SLSA, DORA; all 8 carry references. Three SKILL.md files over the 20 KB report threshold; no executed pipeline evidence. |
| execution-plan-scripts | 1 | 1/1 | 0 | 48 | structural | Group-level SKILL.md without a skill folder; no references; no worked example. |
| finance-accounting | 4 | 3/4 | 0 | 52 | sampled | `accounting-engine` has a clear posting-service contract and integrity checks and correctly defers doctrine to the external engine; `electronic-fiscal-taxing` lacks a capability contract; no worked example. |
| frontend-ux | 9 | 8/9 | 2 | 48 | sampled | `nextjs-app-router` uses APIs removed in Next.js 15, the middleware convention Next.js 16 deprecates, middleware-only route protection, and pins no version; 3 migrated design skills linger as aliases. |
| game-development | 25 | 3/25 | 1 | 46 | sampled | Router and gates in the orchestrator are thoughtful; 22 skills fail contract checks; `online-multiplayer-and-game-backend` is 54 lines with one reference and names no engine networking stack or version. |
| gis | 2 | 2/2 | 0 | 50 | sampled | Correct CRS, SRID and payload rules; SKILL.md is a thin router over three references; no worked example; no named standard (OGC API, EPSG registry versions). |
| ios | 4 | 4/4 | 0 | 58 | sampled | Best currency in the engine: dated WWDC26 baseline, Xcode 27, Swift 6.4, availability policy. No worked example; `ios-monetization` 489 lines while other iOS skills are about 100. |
| languages | 12 | 12/12 | 4 | 56 | structural + grep | All carry references; PHP 8.x, Java 25, .NET 10, Node 24 cited; residual PHP 7.x mentions. |
| mobile-cross | 3 | 3/3 | 1 | 44 | sampled | PWA skill is long (460 lines) and practical but versionless; KMP present; React Native only as a reference checklist; Flutter absent; no OWASP MASVS anywhere in the engine. |
| product-business | 15 | 14/15 | 2 | 49 | sampled | Useful document and spreadsheet tooling, but `professional-word-output` registers Inter and recommends Arial (both hard-banned by the engine's own doctrine); grab-bag composition; `hospitality-hotel-restaurant-systems` fails five contract checks. |
| saas | 18 | 17/18 | 6 | 58 | sampled | Deepest domain group: tenancy, billing, SSO/SCIM, quotas, portability; FieldOps Ledger exemplar. Duplicated contract sections in `multi-tenant-saas-architecture`; five SKILL.md files over 20 KB. |
| sdlc-meta | 20 | 17/20 | 8 | 57 | sampled | Strong catalogue tooling (contract gate, compliance script, audit and skill-writing skills). `council`, `github-ops`, `santa-method` fail five or six contract checks each; grab-bag scope. |
| security | 6 | 6/6 | 0 | 50 | sampled | `web-app-security-audit` is a usable 8-layer PHP/JS procedure with ASVS v5.0.0 version-qualified in a reference, but no CVSS scoring, severity by prose only, bare-slug cross-references to retired skills, and no worked example; DPIA is Uganda-only. |
| 00-meta-initialization | 2 | n/a | n/a | 50 | structural | Entry skills for SDLC documentation; formal SRS correctly routed external. Not in the compliance script's `skills/` scope. |

Unweighted group mean: 51.9 (18 rows).

## Sampled skills

| Skill | Score | References | Worked example | Cites doctrine | Deep or stub | One-line justification |
|---|---:|---:|---|---|---|---|
| ai/ai-rag-patterns | 60 | 6 | yes (curated corpus) | yes | deep via references | Clear RAG-vs-fine-tune rules, production gates; generic boilerplate contract and bare-slug links to retired children. |
| ai/ai-evaluation | 58 | 4 | no | yes | deep | Evaluation contract and slice reporting are right; same generic contract block; no worked eval result. |
| architecture/api-design-first | 62 | 17 | partial | yes | deep | Current RFCs and decision tables; duplicated Inputs/Outputs/Anti-patterns sections; 21.9 KB. |
| backend-databases/postgresql-engineering | 45 | 6 | no | partial | thin router | 97 lines; generic "Do Not Use When"; circular alias for operations; versions stop at 16; `pgcrypto` contradiction. |
| devops-cloud/cicd-pipelines | 60 | 17 | no | yes | deep | Dated verification, OIDC, SLSA; 23.9 KB entrypoint. |
| game-development/game-development-orchestration | 58 | 3 | no | yes | deep | Phase gates, evidence classes and ad gate are well reasoned; missing degraded mode. |
| game-development/online-multiplayer-and-game-backend | 42 | 1 | no | no | thin | Correct principles, but no tick-rate, rollback/lockstep choice, engine netcode or hosting service named; fails four contract checks. |
| gis/gis-platform-engineering | 50 | 6 | no | partial | thin router | Sound decision rules; generic "Do Not Use When"; content in references. |
| frontend-ux/nextjs-app-router | 40 | 0 | no | no | long but stale | Removed `request.ip`/`request.geo`; deprecated `middleware.ts`; auth enforced in middleware alone; no references, no version. |
| security/web-app-security-audit | 52 | 10 | no | partial | deep | Structured layers and report template; no CVSS; PHP-centric; generic quality standards. |
| sdlc-meta/council | 45 | 0 | no | no | adapted | Clear anti-anchoring mechanism; fails six contract checks including trigger. |
| product-business/professional-word-output | 46 | 8 | no | contradicts | deep | Practical DOCX tooling; banned fonts in code and watermark guidance. |
| android/android-development | 44 | 17 | no | partial | deep but stale | Target SDK 35 below Play's API 36 requirement; unsupported crash claim. |
| ios/ios-development | 60 | 8 | no | yes | medium | Current WWDC26 baseline and availability policy; no worked example. |
| saas/multi-tenant-saas-architecture | 58 | 4 | no | yes | deep | Tenant isolation rules and query enforcement; duplicated contract sections; 21.6 KB. |
| finance-accounting/accounting-engine | 56 | 3 | no | yes (external) | medium | Posting contract and integrity checks; correct doctrine hand-off; no worked journal example. |

No sampled skill reaches 70.

Fan-in per skill (`skill_fanin.py`): `NOT_ASSESSED` (not run in this audit).
