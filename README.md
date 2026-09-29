# Chwezi Dev Engine

Chwezi Dev Engine is a routed engineering skills catalogue for building, reviewing, and operating software. Its baseline engineering workflow composes specialist guidance across architecture, languages, databases, AI and agents, security, cloud delivery, SaaS, mobile, games, GIS, and product work.

The engine serves developers, technical leads, product teams, and delivery reviewers. It supports outputs such as requirements and architecture records, implementation guidance, security and reliability reviews, test and release plans, operational evidence, and product/business decisions. Its standards emphasise small understandable changes, explicit user and failure needs, secure and maintainable designs, relevant normal and failure-path checks, and evidence scaled to risk; finance/accounting work routes to the canonical Chwezi Accounting Doctrine engine.

## Installation

For Claude Code, install the Engineering plugin from its marketplace:

```text
/plugin marketplace add peterbamuhigire/chwezi-dev-engine
/plugin install engineering@chwezi-engineering
```

For a local clone, use the included installer with Node.js 18 or later:

```sh
git clone https://github.com/peterbamuhigire/chwezi-dev-engine
cd chwezi-dev-engine
./install.sh --scope project
```

On Windows PowerShell, run `./install.ps1 -scope project`. The wrappers expose scope and dry-run options; consult their help before installing. The active catalogue is routed by the [skill index](docs/skill-routing-index.md) and current `SKILL.md` files.

## Capabilities

| Category | Skill groups | Coverage |
|---|---|---|
| Software delivery and governance | [`sdlc-meta/`](skills/sdlc-meta/), [`execution-plan-scripts/`](skills/execution-plan-scripts/), [`00-meta-initialization/`](00-meta-initialization/), root [`SKILL.md`](SKILL.md) | Project setup, engineering practice, requirements, skill standards, testing, diagnosis, Git/release work, and delivery review. |
| Architecture, data, and security | [`architecture/`](skills/architecture/), [`backend-databases/`](skills/backend-databases/), [`security/`](skills/security/) | System and API design, databases, distributed systems, application and network security, privacy, and reliability. |
| Languages and application development | [`languages/`](skills/languages/), [`frontend-ux/`](skills/frontend-ux/), [`android/`](skills/android/), [`ios/`](skills/ios/), [`mobile-cross/`](skills/mobile-cross/) | Python, TypeScript/JavaScript, PHP, Java, C#/.NET, Android, iOS, Kotlin Multiplatform, and progressive web apps. |
| AI and agent systems | [`ai/`](skills/ai/) | AI application architecture and integration, agent runtime/tooling/governance, evaluation, observability, security, cost, and compliance. |
| SaaS and business software | [`saas/`](skills/saas/) | Multi-tenant platforms, ERP/accounting implementation, billing, identity, entitlements, operations, metrics, and product architecture. |
| Product, commercial, and finance implementation | [`product-business/`](skills/product-business/), [`finance-accounting/`](skills/finance-accounting/) | Discovery, strategy, pricing, growth, customer service, consulting delivery, proposals, document/spreadsheet readiness, and finance implementation; accounting treatment remains owned by the separate doctrine engine. |
| DevOps and cloud | [`devops-cloud/`](skills/devops-cloud/) | Cloud architecture, containers, Kubernetes, infrastructure as code, CI/CD, release engineering, observability, and reliability. |
| Games and GIS | [`game-development/`](skills/game-development/), [`gis/`](skills/gis/) | Game architecture, production, platform release and live operations; GIS platform and enterprise engineering. |

The catalogue is discovered from active `SKILL.md` files under `skills/` and `00-meta-initialization/`; the root `SKILL.md` supplies the engineering baseline. Browse the [skills](skills/) and [initialisation](00-meta-initialization/) directories for current entries. The [routing index](docs/skill-routing-index.md) distinguishes active routes, aliases, and finance-engine ownership.

The catalogue size below is a checked count surface: the test suite compares it with the files on disk, so update it in the same change that adds or retires a skill.

| Measure | Value |
|---|---:|
| Active `SKILL.md` files | 167 |
| Guardrail maximum | 200 |

## References

- [Chwezi Dev Engine source repository](https://github.com/peterbamuhigire/chwezi-dev-engine)
- [Repository operating guide](AGENTS.md)
- [Skill routing index](docs/skill-routing-index.md)
- [World-Class Engineering baseline](skills/sdlc-meta/world-class-engineering/SKILL.md)
- [Accounting doctrine router boundary](https://github.com/peterbamuhigire/chwezi-accounting-doctrine)
- [Installer scripts](install.sh), [Windows installer](install.ps1)
