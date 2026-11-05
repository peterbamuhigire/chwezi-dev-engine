# Chwezi Dev Engine

Chwezi Dev Engine is a catalogue of 168 routed `SKILL.md` files. They tell an AI coding agent, or the engineer directing one, how to design, build, review, secure and operate production software. The skills cover architecture, databases, security, languages, web and mobile clients, AI and agent systems, multi-tenant SaaS, DevOps, game development and GIS.

It is for software engineers, technical leads, architects, product owners, QA and delivery reviewers, and the consultants of Chwezi Core Systems. Use it through Claude Code, Codex or any agent that can read Markdown, when work should follow a written method and leave evidence a reviewer can check.

A root baseline, [`world-class-engineering`](skills/sdlc-meta/world-class-engineering/SKILL.md), applies to every change: small, explained changes, explicit failure handling, evidence scaled to risk and a verify-before-done gate.

**Contents**

- [At a glance](#at-a-glance)
- [Start here](#start-here)
- [Capabilities](#capabilities)
- [Find the right skill](#find-the-right-skill)
- [How it works](#how-it-works)
- [What is inside](#what-is-inside)
- [Installation](#installation)
- [Verify](#verify)
- [Quality and improvement](#quality-and-improvement)
- [What the October 2026 kaizen improved](#what-the-october-2026-kaizen-improved)
- [Date-triggered gates](#date-triggered-gates)
- [References](#references)
- [Contributing and licence](#contributing-and-licence)

## At a glance

- **168 active skills** in 18 categories, plus 78 retired names kept as redirects.
- **166 skills** ship in the Claude Code plugin. The two project-initialisation skills are read from a clone.
- **242 routing fixtures.** Each pairs a sample task with the skill that should win it. The expected skill ranks first for 222 (91.7%) and in the top three for all 242. The test matches words in skill descriptions, so it is not live routing.
- **273 tests pass and 3 are skipped** (pytest 9.2.0, Python 3.14.10, Linux, 2026-11-05).
- **72 dated source records** back volatile facts. A continuous-integration (CI) step fails when one passes its review date. It failed from 2026-11-04, when five Next.js records went overdue, until 2026-11-05, when the 14 overdue records were re-read; it exits 0 on 2026-11-06 (see [Date-triggered gates](#date-triggered-gates)).
- **Latest published rating: 62.5/100.** It is a practitioner's judgement, not an external audit, and the 95/100 target is not reached.

## Start here

1. **Install.** In Claude Code, add the repository as a marketplace, then install the plugin. Other routes (Codex, standalone installer, manual) are under [Installation](#installation).

   ```text
   /plugin marketplace add peterbamuhigire/chwezi-dev-engine
   /plugin install engineering@chwezi-engineering
   ```

2. **Check.** From a clone, run the catalogue check. It needs Python and PyYAML, reports `active SKILL.md files: 168` and exits 0 on the current tree.

   ```sh
   python3 -X utf8 scripts/skill_catalog_guardrails.py
   ```

3. **Use.** Name the skill in your request, for example: "Use `api-design-first` to define the contract for the invoice listing endpoint." Pick the name from [Find the right skill](#find-the-right-skill).

## Capabilities

The engine holds 168 active skills in 18 categories (166 ship in the Claude Code plugin), grouped under [What is inside](#what-is-inside). The [skill catalogue](docs/skill-catalogue.md) lists each one. The table under Find the right skill is the capability map: common tasks and the skill that handles each.

### Find the right skill

Use this engine when software work needs a repeatable method and evidence a reviewer can check: a design, a review, a security audit or a release gate. The names below come from the routing fixtures, so each task is one the engine's routing test already uses.

| Task | Skill |
|---|---|
| Define an API contract first, with versioning, idempotency and an error model | [`api-design-first`](skills/architecture/api-design-first/SKILL.md) |
| Design the data model, tenancy and indexes for a multi-tenant ERP | [`database-design-engineering`](skills/backend-databases/database-design-engineering/SKILL.md) |
| Check a web application for OWASP vulnerabilities | [`web-app-security-audit`](skills/security/web-app-security-audit/SKILL.md) |
| Threat-model a payment API and write abuse cases | [`vibe-security-skill`](skills/security/vibe-security-skill/SKILL.md) |
| Review a pull request that an AI agent wrote | [`ai-assisted-development`](skills/sdlc-meta/ai-assisted-development/SKILL.md) |
| Run build, types, lint, tests and diff review before claiming a fix is done | [`world-class-engineering`](skills/sdlc-meta/world-class-engineering/SKILL.md) |
| Diagnose an intermittent production bug | [`systematic-bug-diagnosis`](skills/sdlc-meta/systematic-bug-diagnosis/SKILL.md) |
| Design the unit, integration and end-to-end test strategy for a service | [`advanced-testing-strategy`](skills/sdlc-meta/advanced-testing-strategy/SKILL.md) |
| Build a CI/CD pipeline with build, test and deployment stages | [`cicd-pipelines`](skills/devops-cloud/cicd-pipelines/SKILL.md) |
| Add retrieval-augmented generation with chunking, embeddings and a vector store | [`ai-rag-patterns`](skills/ai/ai-rag-patterns/SKILL.md) |
| Add SAML single sign-on and SCIM provisioning for enterprise customers | [`saas-sso-scim-enterprise-auth`](skills/saas/saas-sso-scim-enterprise-auth/SKILL.md) |
| Charge monthly with proration, trials and dunning for failed cards | [`subscription-billing`](skills/saas/subscription-billing/SKILL.md) |

Every skill is listed in the [skill catalogue](docs/skill-catalogue.md).

Some work belongs to a neighbouring engine:

- Visual design, typography and UI appearance: the Chwezi design engine.
- IFRS and IAS rules, statutory values and period close: the [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine) engine. This engine implements that treatment in software.
- Complete website delivery, content and SEO: the Chwezi website engine.
- Formal SRS and lifecycle specifications: the Chwezi SDLC documentation engine.

## How it works

- The router is the root [`SKILL.md`](SKILL.md), with [`AGENTS.md`](AGENTS.md) and [`CLAUDE.md`](CLAUDE.md), which imports `AGENTS.md`. It maps an intent to a skill family.
- The agent loads one skill's `SKILL.md` and only the `references/` files that the task needs.
- Two always-on skills govern output quality. `anti-ai-slop` applies while an artefact is produced. `ai-slop-audit` runs after each major iteration and at release.
- Retired skill names redirect to current skills. The [skill routing index](docs/skill-routing-index.md) explains the map, and [`docs/skill-aliases.yml`](docs/skill-aliases.yml) holds the machine-readable form.
- Volatile facts such as versions, dates and vendor policies come from the dated records in `docs/source-registers/`, not from skill text.
- Repository tests check the catalogue count, evidence sections and routing fixtures on every change.

The file model and the policy behind it are in [`docs/overview/ARCHITECTURE.md`](docs/overview/ARCHITECTURE.md).

## What is inside

[`SKILL.md`](SKILL.md) at the root is the router and is not counted. The 168 active skills sit in 18 categories. The [skill catalogue](docs/skill-catalogue.md) lists each skill with a one-line description. The 78 inactive `ALIAS.md` redirects are excluded.

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
| SaaS platforms | [`skills/saas/`](skills/saas/) | 19 |
| Product and business | [`skills/product-business/`](skills/product-business/) | 15 |
| Finance implementation | [`skills/finance-accounting/`](skills/finance-accounting/) | 4 |
| DevOps and cloud | [`skills/devops-cloud/`](skills/devops-cloud/) | 8 |
| Game development | [`skills/game-development/`](skills/game-development/) | 25 |
| GIS | [`skills/gis/`](skills/gis/) | 2 |
| **Total** | | **168** |

### Catalogue size

The active count is a checked surface. `tests/test_engine_control_plane.py` compares it with the files on disk, so update it in the same change that adds or retires a skill. `scripts/skill_catalog_guardrails.py` enforces the maximum.

| Measure | Value |
|---|---:|
| Active `SKILL.md` files | 168 |
| Guardrail maximum | 200 |
| Inactive `ALIAS.md` redirects | 78 |
| Skills shipped by the Claude plugin manifest | 166 |
| Routing fixtures | 242 |

### What the skills produce

The engine produces working engineering artefacts, not advice:

- Architecture records and C4 diagrams whose claims are pinned to a commit and checked by `verify_diagram_evidence.py`.
- OpenAPI contracts, database schemas and migration plans.
- Threat models, authorisation matrices, Data Protection Impact Assessments and severity-rated security audit reports.
- Test strategies and Release Evidence Bundles.
- CI/CD pipelines, Terraform, Docker and Kubernetes configurations.
- Traceable requirements with acceptance criteria, and SDLC document sets.
- AI feature specifications, evaluation harnesses and cost models.
- Game design and production plans.
- Implementation-status audits with completion blueprints, and CodeTour onboarding walkthroughs.
- Validated Word and Excel deliverables.

### Standards applied

The engine applies published standards where the work calls for them:

- **Security and assurance:** OWASP Top 10 2025, OWASP ASVS 5.0.0, the OWASP Top 10 for LLM Applications and API Security Top 10, ISO/IEC 27001:2022, SOC 2 Trust Services Criteria, PCI DSS v4.0.1 and SLSA v1.2.
- **AI and privacy:** the NIST AI RMF, ISO/IEC 42001:2023, the EU AI Act, GDPR and Uganda's Data Protection and Privacy Act 2019.
- **Web, API and code:** WCAG 2.2 AA, OpenAPI 3.1, RFC 9457 and PSR-12.
- **Testing and design records:** ISO/IEC/IEEE 29119 and the C4 model.

### Beyond the skills

- `agents/` holds 10 reviewer and planning agents, such as `security-reviewer` and `tdd-guide`.
- `hooks/` holds a destructive-command gate and the plugin hook configuration, each with a test.
- `rules/` holds the always-on rules. Start at [`rules/README.md`](rules/README.md).
- `templates/` holds API, architecture, delivery, reliability and security templates, and a work-graph template.
- `examples/` holds a full-stack SaaS reference and a synthetic tenant invoice slice.
- `docs/` holds the records. Start at the [documentation index](docs/README.md).

## Installation

This repository was formerly named `skills-web-dev`. An older clone may still sit in a folder of that name. Every command below works from whatever the folder is called.

**Prerequisites.**

- Git.
- Node.js 18 or later, for the standalone installer and the hook tests. CI uses Node 24. The checks in this file were last run on Node 22.
- Python 3.11 or later, for the Codex model-policy helper.
- For the validators and tests, `pip install -r requirements-ci.txt` installs pytest 9.0.3 and PyYAML 6.0.2. CI runs them on Python 3.12. The 2026-10-31 run on Linux used Python 3.14 with PyYAML 6.0.3.
- Commands use `python3`. On Windows, use `python` or `py -3`.

### Claude Code plugin (recommended)

The repository is its own marketplace: `.claude-plugin/marketplace.json`, marketplace `chwezi-engineering`, plugin `engineering`.

```text
/plugin marketplace add peterbamuhigire/chwezi-dev-engine
/plugin install engineering@chwezi-engineering
```

The plugin manifest (`.claude-plugin/plugin.json`) ships the 166 skills under `skills/`, plus `agents/`, `hooks/` and `rules/`. The two project-initialisation skills in `00-meta-initialization/` are read from a clone.

### Codex

Root `plugin.json` uses the portable Agent Plugins format. The repo-scoped catalogue is `.agents/plugins/marketplace.json`. It discovers the root `skills/` directory. The two `00-meta-initialization/` workflows stay clone-based entry points. Codex and Claude keep separate host catalogues.

Adding the repo marketplace changes the user's Codex marketplace state. This repository does not edit that state or submit a public listing.

Point Codex at the clone. It reads [`AGENTS.md`](AGENTS.md) as the router. Before substantive work, run the bounded model-policy check described in [`.codex/README.md`](.codex/README.md):

```text
python3 <engine-root>/.codex/ensure_model_policy.py --runtime codex --check
```

Run `--apply` only if the check reports drift. It exits 1 and prints `DRIFT` when the Codex configuration is missing or differs. Claude Code skips this step: `--runtime claude --check` prints `NOT_APPLICABLE` and exits 0.

An offline `debug prompt-input` check may need to list the whole plugin skill manifest. Use the measured invocation in [the October 2026 validation record](docs/kaizen/2026-10-engine-kaizen/04-validation-record.md):

```sh
codex -m gpt-6-luna -c model_reasoning_effort="high" -c skills.max_context_tokens=10000 debug prompt-input
```

This invocation-level budget affects the initial skill list only. The checked default loaded 130 of 165 declared plugin skill paths. The explicit budget loaded all 165 in the isolated offline run. It does not alter persistent user settings.

### Standalone installer

Use this when there is no plugin system, or when you want project-local scope.

`install.sh` and `install.ps1` delegate to `scripts/install-engine.js`. It copies skills, agents, hooks and rules into `~/.claude` (`--scope user`, the default) or `./.claude` (`--scope project`). It records every file it writes in `.chwezi/install-state.json` inside that folder.

```sh
git clone https://github.com/peterbamuhigire/chwezi-dev-engine.git
cd chwezi-dev-engine
bash install.sh --scope project --dry-run   # print the plan, write nothing
bash install.sh --scope project
```

- Run the wrapper with `bash`. The file is tracked without its executable bit, so `./install.sh` fails with "Permission denied" on a fresh Linux clone.
- On Windows PowerShell, run `.\install.ps1 --scope project`. The same flags pass through to the Node installer. This was not run in the October 2026 passes.
- `node scripts/install-engine.js uninstall --engine <name>`, `doctor` and `list-installed` manage an existing install. `<name>` is the folder the engine was cloned into (`chwezi-dev-engine` for the clone above). `list-installed` prints it.
- Uninstall removes only files the installer recorded.
- On 2026-10-31, a real install into an empty home folder, `doctor`, a dry-run uninstall and a real uninstall all exited 0. The uninstall left only the install-state record.

### Manual route

Clone the repository. Have the agent read [`CLAUDE.md`](CLAUDE.md), the [skill routing index](docs/skill-routing-index.md), and only the `SKILL.md` files the task needs. Expose `skills/` and `00-meta-initialization/` to the working agent.

[`docs/USING-IN-A-PROJECT.md`](docs/USING-IN-A-PROJECT.md) covers submodule, sibling-clone and read-only-mount wiring.

## Verify

Run from the repository root. These are the steps of the CI workflow (`.github/workflows/skill-guardrails.yml`), in its order, plus `git diff --check` from [`CONTRIBUTING.md`](CONTRIBUTING.md). On 2026-11-05 every step exited 0 on the current tree on Linux (Fedora, Python 3.14.10, Node 22.23.1) except the source-register check, which exited 1 until the 14 overdue records were re-read that evening. It exits 0 on 2026-11-06 (see the table and [Date-triggered gates](#date-triggered-gates)).

```sh
python3 -m pip install -r requirements-ci.txt
python3 -X utf8 scripts/skill_catalog_guardrails.py
python3 -X utf8 -m unittest tests/test_skill_catalog_guardrails.py
python3 -X utf8 -m pytest tests -q -p no:cacheprovider
python3 -X utf8 scripts/routing_smoke_test.py --min-rank1 89 --lint-fixtures
python3 -X utf8 scripts/routing_smoke_test.py --coverage --max-zero-positive 1
python3 -X utf8 scripts/routing_smoke_test.py --collisions --collision-gate --threshold 0.5
python3 -X utf8 scripts/validate_engine_control_plane.py
python3 -X utf8 scripts/check_source_register.py
node hooks/test-destructive-bash-gate.js && node hooks/test-plugin-hook-config.js
python3 -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --all
git diff --check
```

| Check | Needs | Result, 2026-11-05 |
|---|---|---|
| Catalogue guardrails (the script also runs the host-path, duplicate-heading and broken-link ratchets) | Python, PyYAML | 168 active skills, 0 errors, 14 size warnings (warnings never change the exit status) |
| Guardrail unit tests | Python | 10 tests OK |
| Test suite | Python, pytest, PyYAML, Git | 273 passed, 3 skipped |
| Routing smoke test (a lexical proxy, not live routing) | Python, PyYAML | 242 fixtures; precision@1 222/242 (91.7%), precision@3 242/242; 86 owned negatives (82 pass, 4 `NOT_ASSESSED`) |
| Fixture coverage | Python, PyYAML | 167 of 168 skills have a positive fixture; `new-project` has none |
| Description collisions | Python, PyYAML | 1 pair above 0.5 (`mysql-engineering` and `postgresql-engineering`, 0.627), allow-listed |
| Control-plane registry | Python | 12 registry entries; installed checkouts are `NOT ASSESSED` unless parent folders are given (below) |
| Source registers | Python | Exit 0 on 2026-11-06: 73 active sources, 0 findings, 16 warnings for dates within 14 days. It exited 1 before the 14 overdue records were re-read; see the [calendar](#date-triggered-gates) |
| Hook tests | Node | 61/61 and 7/7 |
| Evidence-declaration contract gate | Python | 162 skills scanned, 0 errors, 6 exempt |

The 3 skipped tests are the opt-in installed-portfolio checks (`SKILL_ENGINE_LIVE_TESTS=1`). `NOT ASSESSED` means a check could not be run here. It is never reported as a pass.

A ratchet is a recorded baseline of known problems. A new problem fails the check, and the baseline may only shrink.

### Checks beyond CI

None of these is part of CI.

- **Sibling checkouts.** Give the validators the folders that hold the other engines, once per folder or as `CHWEZI_ENGINES_ROOT` (folders separated by `:`, or `;` on Windows). `scripts/engine_roots.py` finds former directory names such as `srs-skills`.

  List the eleven public engines with `--engine`. The twelfth, `political`, is private and not installed on most hosts, so an unscoped run exits 1:

  ```sh
  python3 -X utf8 scripts/validate_engine_control_plane.py --workspace-root <parent-1> --workspace-root <parent-2> \
    --engine accounting --engine business-plan --engine chwezi-dev-engine --engine design --engine digital-research \
    --engine linux --engine proposal --engine social-media --engine srs --engine website --engine windows-admin
  python3 -X utf8 scripts/validate_approval_adapters.py --workspace-root <parent-1> --workspace-root <parent-2>
  ```

  Both exited 0 on 2026-10-31 (11 engines in scope; 11 adapters, 0 findings). Without parent folders, the adapter validator exits 1 unless the siblings sit next to this checkout.
- **Applied examples.** `python3 -X utf8 scripts/validate_tenant_invoice_example.py` needs only Python and prints `PASS`. `php examples/tenant-invoice-listing/php/test.php` needs the PHP CLI with PDO SQLite and printed `15 checks passed`.
- **Not re-run here.** The Next.js, Compose, MySQL and Android layers of that example need their own toolchains (`NOT ASSESSED`).
- **Other scripts.** `scripts/check_package_file_budget.py`, `scripts/source_ingestion_guardrail.py` and `scripts/validate_work_graph.py templates/work-graph.yml` need only Python and exited 0.
- **Not needed.** No validator in this repository calls PowerShell (`pwsh`), Pandoc, Mermaid, LibreOffice, a browser or a container. Skills mention those tools only as downstream project requirements.
- **Windows helpers.** `install.ps1` and `scripts/install-pdf-binaries.ps1` were not run in the October 2026 passes.

## Quality and improvement

Improvement work (kaizen, the Japanese term for continuous improvement) follows the Observe, Baseline, Select, Experiment, Check, Standardise, Teach, Re-measure cycle in [`kaizen-improvement-system`](skills/sdlc-meta/kaizen-improvement-system/SKILL.md).

Evidence for the October 2026 passes lives in two folders. Each holds a scope record, a frozen baseline scorecard, a backlog, an experiment log, a validation record, a final report and a next-cycle handoff.

- [`docs/kaizen/2026-10-engine-kaizen/`](docs/kaizen/2026-10-engine-kaizen/README.md), the 29 October pass.
- [`docs/kaizen/2026-10-engine-kaizen-pass-2/`](docs/kaizen/2026-10-engine-kaizen-pass-2/README.md), the 31 October pass. Its [final report](docs/kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md) is the source of the scores below.

Read the validation records before you treat an example as production proof.

### Changes after the October kaizen (1 to 6 November 2026)

- **Tenant document numbering (5 November, `13e4cc9` and `f9e7a46`).** The new skill [`tenant-document-numbering`](skills/saas/tenant-document-numbering/SKILL.md) sets one contiguous, never-resetting series per tenant and document type for every user-facing number, kept apart from the database id.
  - Its references cover the schema and allocator (MySQL 8, PostgreSQL, PHP, retry, lifecycle, lock order), seeding and capacity, API and offline guardrails, and retrofit and rollout.
  - The commit removed guidance that contradicted it: the `MAX+1` journal-number trigger, "gaps are acceptable" and id-derived reversal references.
  - 17 related skills and the AI code review gate each gained a cross-reference. Three routing fixtures with three owned negatives cover the skill.
  - `f9e7a46` warns that a bound integer inside `GREATEST()` compares as text and can lower a counter.
  - Record: [`docs/updates/2026-11-05-tenant-document-numbering-standard.md`](docs/updates/2026-11-05-tenant-document-numbering-standard.md).
- **Source register re-read (5 and 6 November).** The 14 records that had gone overdue were re-read from their primary pages and the check exits 0 again.
  - Nine pages were unchanged and were renewed in place. Four had moved on and were superseded: Next.js 16.4.5 and its 3 November security release, the Android November bulletin, and AGP 9.5.0.
  - One page, the MySQL 8.4.13 release notes, returned HTTP 403 to every attempt and is quarantined with a replacement source.
  - Record: [`docs/updates/2026-11-06-source-register-reread.md`](docs/updates/2026-11-06-source-register-reread.md).
- **MCP transport dating (6 November, `284b0f2`, `f44848c`, `6592901`).** Two statements presented MCP revision 2026-07-28 as the start of the HTTP+SSE deprecation. They now say it has been deprecated since protocol version 2025-03-26 and was reclassified as Deprecated under the lifecycle policy (SEP-2596) in 2026-07-28, as the changelog read on 2026-11-05 states.
  - A third commit separates the changelog's removals (protocol sessions and the `initialize` handshake) from its additions in the same bullet.
  - Record: [`docs/updates/2026-11-06-mcp-http-sse-dating.md`](docs/updates/2026-11-06-mcp-http-sse-dating.md). The SDK snippets and whether SEP-2596 has reached Final are `NOT_ASSESSED`.
- **Signup bot controls (1 November, `74c9bda`).** A shared reference, [`signup-human-validation.md`](skills/security/vibe-security-skill/references/signup-human-validation.md), sets the defaults.
  - Web: Cloudflare Turnstile Managed mode with server-side validation.
  - Android: Firebase App Check with Play Integrity, with Turnstile in a WebView as the fallback.
  - The provider claims were checked against official documentation on 1 November 2026. Review them by 1 February 2027. Record: [`docs/updates/2026-11-01-signup-human-validation-standard.md`](docs/updates/2026-11-01-signup-human-validation-standard.md).
- **Verify figures re-measured (5 November).** Every figure in [Verify](#verify) was re-run on 2026-11-05. The one change in outcome was the source-register check, which exited 1; it was fixed the same evening (see the next item and [Date-triggered gates](#date-triggered-gates)). Record: [`docs/updates/2026-11-05-readme-measured-refresh.md`](docs/updates/2026-11-05-readme-measured-refresh.md).

### Latest published score

Pass 2 rated the engine 62.5/100 raw, the mean of ten dimension ratings. The Portfolio Standard cap, `min(raw, 65)`, leaves 62.5/100. The 29 October pass published 59.5 raw and 59.5 capped.

The two figures are not a trend. Pass 2 scored the whole tree afresh and found items the first pass had not checked. The ratings are a practitioner's judgement, not an external audit or benchmark. The 95/100 target was not reached and remains a target.

### Open findings that matter to a reader

The full list, with reasons, is the pass-2 [next-cycle handoff](docs/kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md).

- **Local settings file.** `.claude/settings.local.json` is a user-local settings file. It is tracked in this public repository and names Windows user-profile paths. It is escalated to the maintainer. Untracking keeps the file on disk but does not remove it from Git history. Do not copy it.
- **Invoice slice gaps.** `examples/tenant-invoice-listing/` has known contract gaps: no pagination, errors not in RFC 9457 form, raw minor units shown to users, `LIKE` wildcards in search, no migration rollback, accessibility semantics and no evidence pack. Its README lists them. Do not copy the slice as a finished listing.
- **Hygiene ratchets.** 24 skills still carry a duplicate `##` heading. 84 relative links in 52 files do not resolve. Ratchets in `docs/quality-gates/` hold both counts, and they may only shrink.
- **Thin routing coverage.** 14 of 168 skills have three positive fixtures and two owned negatives (measured 2026-11-05). `new-project` has no fixture.
- **Currency rows not re-read in pass 2.** These are the legacy hospitality register (review date 2026-10-14, now past), the Apple developer documentation row, the OpenAI Codex availability article (quarantined after an HTTP 403) and the Kubernetes latest version (inferred, not labelled by the source).
- **Builds not repeated.** The 29 October validation record reports a Next.js build, a Compose build and a MySQL fixture run of the invoice slice. Each ran in a disposable environment outside this repository. Pass 2 and the documentation round that followed could not repeat them.
- **Not established by any pass:** emulator or browser rendering, authenticated database integration, live-model routing, production behaviour and independent human review. These are `NOT_ASSESSED`, never a pass.

## What the October 2026 kaizen improved

Each item is a kept change on `main`, with its commit confirmed in Git history. The evidence is in the [29 October](docs/kaizen/2026-10-engine-kaizen/03-experiment-log.md) and [pass-2](docs/kaizen/2026-10-engine-kaizen-pass-2/03-experiment-log.md) experiment logs.

"Re-measured" means the check was run again on 2026-10-31, on the tree before pass 2 (`27a602b`) and on the current tree. Other figures are copied from the evidence file named. Fixtures and static checks support most items. None is production proof, and the open findings above are not fixed by them.

### Defects fixed in guidance

Most severe first.

- **Next.js tenant boundary** (`e00f12f`, `e0cc114`, `b7177be`).
  - Before: the skill taught a role cookie as authority, a global users cache, an unscoped read and an unchecked mutation.
  - Now: session, tenant-membership and permission checks sit at the server-only data-access boundary ([`tenant-data-security.md`](skills/frontend-ux/nextjs-app-router/references/tenant-data-security.md)).
  - Re-measured: `scripts/validate_tenant_invoice_example.py` prints `PASS`, and `tests/test_tenant_invoice_example.py` passes (7 tests). A disposable `next build` on 29 October found a page and route-handler collision at `/invoices`. It was fixed with a regression test ([validation record](docs/kaizen/2026-10-engine-kaizen/04-validation-record.md); not re-run here).
- **Next.js 16 drift** (`e00f12f`).
  - Before: examples used synchronous `params` and a `middleware.ts` that read `request.ip` and `request.geo`.
  - Now: they use async `params` and `proxy.ts`, and say that a Proxy redirect is only a navigation aid.
  - Checked against the official upgrade guide on 2026-10-29 (source record `next16-upgrade-2026-10-29`).
- **Android currency** (`4ba4c2d`).
  - Before: the skill gave API 35 as the Play target. It claimed that omitting one edge-to-edge helper crashes the app.
  - Now: it separates the Play target (API 36 or higher, verified 2026-10-29; re-read before release) from the latest platform release (Android 17, API 37), which is a compatibility target. The unsupported crash claim is gone. The same commit added an advisory-check line to the PHP and PostgreSQL skills.
  - Checked: a disposable Compose excerpt built with `:app:assembleDebug` on 29 October. There was no emulator run.
- **Overdue source records** (`f970df0`).
  - Before: 27 of 65 records were past review, including AI-platform rows the router names as a first stop.
  - Now: each primary page was re-read on 2026-10-31. 26 snapshots moved to `superseded_sources`, one record was quarantined after an HTTP 403, and two claims were narrowed where the page no longer supported them. The pages show OpenAI's Evals platform and `v1/prompts` due to shut down on 2026-11-30, and Bedrock Agents closed to new customers. No skill depended on them.
  - Re-measured: 27 findings (exit 1) on the earlier register, 0 (exit 0) now. The check covers dates and metadata, not whether a page supports a claim.

### Tooling that failed on this host

- **Cross-engine validators** (`9979773`).
  - Before: the control-plane and approval validators hard-coded one Windows layout and former repository names, so both exited 1 here.
  - Now: `scripts/engine_roots.py` takes repeatable parent folders, `CHWEZI_ENGINES_ROOT`, former directory names and per-engine overrides.
  - Re-measured for the eleven public engines: control plane exit 1 (5 findings; the old script accepts one parent folder) to exit 0 with both of this host's parent folders. Approval adapters exit 1 (10 findings) to exit 0 (11 adapters). A twelve-engine run still exits 1 because the private `political` checkout is not installed (`NOT_ASSESSED`).
- **Host paths and leaked markup** (`39a6898`, `3b7b3f6`).
  - Before: router and skill text named one machine's drive-rooted checkout, and eight references ended in leaked tool markup.
  - Now: both are removed, and `scripts/content_hygiene.py` fails the catalogue gate on host paths.
  - Re-measured with that guard: 54 findings on the earlier tree, 0 now. The evidence counts 30 real lines by hand. The guard also covers the validators and pass-1 evidence links.
- **Package checks** (`f162535`, `27a602b`).
  - Before: the Codex plugin shape and the package entry limit had no check in this repository.
  - Now: root `plugin.json`, `.agents/plugins/marketplace.json` and `scripts/check_package_file_budget.py`, with an over-cap failure test and a fail-closed case for unreadable paths.
  - Re-measured: 2524 package-oriented entries against a limit of 5000. The documented context-budget invocation raised the skill paths that an offline Codex `debug prompt-input` loads from 130 to 165 of 165 (validation record; invocation-level, not re-run). Public marketplace acceptance is not assessed.

### Checks that only tighten

- **Source-register gate** (`ca94e6b`, `842965b`).
  - `scripts/check_source_register.py` and a CI step fail when an active record is past its review date, a claim cites a superseded or quarantined record, or a quarantine has no reason. The [calendar](#date-triggered-gates) shows when it next fires.
  - The same pass recorded the 2026-10-31 model-currentness review: Luna/high pin retained, comparison `NOT_ASSESSED`, due by 2026-12-28.
- **Duplicate headings** (`feccc13`, `d12c250`, `f3b0705`).
  - Normalising skills to the contract appended blocks to existing sections and left repeated `##` headings.
  - 57 skills were merged, with a per-file check that only one heading and one label changed. A ratchet blocks new duplicates.
  - Re-measured: files with an exact duplicate H2 fell from 65 to 24.
- **Broken links** (`0ca42e0`, `625e5e7`).
  - The old check read only `references/` and `templates/` links. 33 links in 19 files were repaired where the target resolved uniquely. The check now covers all Markdown under the active roots.
  - Re-measured: broken file-and-target pairs fell from 111 in 70 files to 84 in 52.
- **Routing fixtures** (`9f0369e`, `c4e691f`).
  - 42 skills had no positive fixture. Each gained one. `--coverage` reports the gap, and CI enforces a ceiling of one and a rank-1 floor of 89 (was 88).
  - Re-measured: skills with no positive fixture fell from 43 to 1 (`new-project`). Precision@1 rose from 177/196 (90.3%) to 219/239 (91.6%). Precision@3 was 100% both times. The proxy is lexical, not live routing.

### Routing and examples

- **Review route** (`a6735a5`).
  - Before: a review that crosses SQL, tenant scope, query shape, output encoding and ledger writes had no route to the five owning checks. The exercise also named a posting service that differed from the owning skill.
  - Now: a router row, a routing-index section, one fixture, 4 tests, and a table in [`ai-generated-code-review-gate.md`](skills/sdlc-meta/ai-assisted-development/references/ai-generated-code-review-gate.md) that names the owning skill for each defect class. Renaming one table link fails a test.
  - The full original review request still misroutes at rank 1 under the proxy.
- **Invoice slice** (`2288c75`, `bd4a03b`, `8bec17a`).
  - Before: the practitioner task had no reproducible cross-layer proof of tenant isolation.
  - Now: a synthetic PHP, OpenAPI, Next.js and Compose slice in `examples/tenant-invoice-listing/`, a PHP fixture and an unsafe-code review exercise.
  - Re-measured: the fixture prints `15 checks passed` against a PDO SQLite synthetic database. A disposable MySQL 8.4.13 run also passed 15 checks on 29 October (validation record). Pass 2 then listed the slice's unfixed gaps in its README so it is not copied as finished.

### Overall measures

| Measure | Before | After | Basis |
|---|---|---|---|
| Rating, raw and capped at `min(raw, 65)`, ten dimensions | 29 Oct 46.5 and 46.5; pass 2 55.0 and 55.0 | 29 Oct 59.5 and 59.5; pass 2 62.5 and 62.5 | Copied from both [final reports](docs/kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md). The cap did not bind. The passes scored different trees, so the figures are not a trend |
| Test suite, pytest 9.0.3 | 220 passed, 3 skipped | 273 passed, 3 skipped | Re-measured on both trees in a scratch virtual environment. The system `python3` has no pytest |
| 29 October suite and routing precision@1 | 207 passed; 173/191 | 220 passed; 177/196 | Copied from the 29 October [baseline](docs/kaizen/2026-10-engine-kaizen/01-baseline-scorecard.md) and [validation record](docs/kaizen/2026-10-engine-kaizen/04-validation-record.md) |

Tried and reverted in pass 2, so not counted above:

- Widening the `accounting-engine` description (no gain under the proxy).
- Merging `Anti-Patterns` pairs in 19 skills (text landed outside its section).
- One `skill-writing` merge (it crossed the 20,480-byte report threshold).
- An over-broad link repair.

The [pass-2 log](docs/kaizen/2026-10-engine-kaizen-pass-2/03-experiment-log.md) has the details.

## Date-triggered gates

`scripts/check_source_register.py` fails when an active source record's `review_after` date is before the check date. The **Check source registers** CI step runs it. A pass proves dates and metadata only. It does not prove that a page supports a claim.

Each row below was checked on 2026-11-06 by running the check with `--as-of` on its first failing date and on the day before, and comparing the number of findings. On the first date of a row, the check exits 1 with the total shown:

```sh
python3 -X utf8 scripts/check_source_register.py --as-of 2026-11-14
```

| First failing `--as-of` date | Records lapsing that day | Failing in total | Topics |
|---|---:|---:|---|
| 2026-11-12 | 1 | 1 | PowerShell support lifecycle |
| 2026-11-14 | 8 | 9 | Next.js October advisory and November release post, PHP security, Brotli and upload-progress advisories, PostgreSQL security, Android November bulletin, Oracle MySQL alert |
| 2026-11-21 | 7 | 16 | Android 17, Compose setup and compiler migration, AGP 9.5.0, Next.js 16.4.5 release, support policy and upgrade guide |
| 2026-11-30 | 6 | 22 | OpenAI changelog, model selection, skills context budget, plugin format and submission, Claude plugin marketplace |
| 2026-12-01 | 34 | 56 | The main batch: Play target, Kotlin, PHP supported versions, PostgreSQL support, OpenAI, Anthropic, Gemini and Bedrock guidance, Windows, Intune, PowerShell, Cisco, BIND, Kubernetes, React, MySQL 8.4 index |
| 2026-12-02 | 6 | 62 | WCAG 2.2, ASVS, IFRS 18, Windows security baselines and server documentation |
| 2026-12-17 | 1 | 63 | W3C validator user documentation |
| 2026-12-18 | 1 | 64 | W3C validator user documentation (second record) |
| 2026-12-30 | 1 | 65 | Impeccable slop catalogue |
| 2027-01-01 | 5 | 70 | NIST AI RMF, OWASP Top 10 2025, ASVS 5.0.0, PCI DSS 4.0.1, SLSA 1.2 |
| 2027-01-30 | 2 | 72 | Next.js authentication and data-security guides |
| 2027-09-02 | 1 | 73 | IETF DNSSEC best practice |

**Status on 2026-11-06.** The check exits 0: 73 active sources and 0 findings. The 14 records that were overdue were re-read from their primary pages on 2026-11-05 between 22:11 and 22:13 UTC (01:11 to 01:13 on 6 November in East Africa). Record dates use the UTC date, so a CI run in UTC never sees a future date. No date was extended unread.

- **Renewed in place, page unchanged (9):** `next16-upgrade-2026-10-29`, `nextjs-support-policy-2026-10-29`, `next-security-oct14-2026`, `android-17-release-2026-10-29`, `compose-setup-2026-10-29`, `kotlin-compose-migration-2026-10-29`, `php-security-oct21-2026`, `php-windows-brotli-2026` and `postgresql-security-2026-10-29`.
- **Superseded by a new dated record (4):**
  - `nextjs-release-2026-10-29` (v16.4.3) by `nextjs-release-2026-11-05` (v16.4.5, published 2026-11-03).
  - `next-security-november-notice-2026` by `next-security-november-2026-release-2026-11-05`. The planned release shipped on 2026-11-03: one High and six Medium advisories, fixed in 16.4.5 and 15.5.29.
  - `android-security-bulletin-october-2026` by `android-security-bulletin-november-2026` (patch level 2026-11-05 or later).
  - `android-agp-9-1-notes-2026-10-29` by `android-agp-9-5-notes-2026-11-05` (AGP 9.5.0, October 2026).
- **Quarantined, page unreadable (1):** `mysql-8413-security-2026-10-29`. The MySQL documentation site returned HTTP 403 ("Technical Difficulties") to every attempt, so the 8.4.13 release date and security notes are `NOT_ASSESSED` until it is read again, by 2026-11-13. `oracle-cpu-oct-2026-mysql-2026-11-05` records what the readable Oracle October 2026 alert says: MySQL Server 8.4.0 to 8.4.12 affected, 8.4.13 outside that range. It does not name 8.4.13 as the fix.
- **Added (1):** `php-session-upload-progress-advisory-2026-11-05`, the PHP informational advisory of 2026-10-23 (CVE-2026-115560, full advisory to follow).

The cure is to re-read the primary page, add a dated record and move the old one to `superseded_sources`. Never extend a date unread. The security records and the MySQL quarantine come due on 2026-11-13, and the release, setup and migration records on 2026-11-20. Also due: the next full re-audit on or before 2026-11-30, and the model comparison by 2026-12-28 (both from the handoff).

## References

The skills, source registers, audits and improvement records cite 384 books, 49 repositories, 53 standards and official-source entries, and 13 websites and articles. The lists are citations only: the engine paraphrases operational guidance and stores no book text.

- [Books](docs/references/books.md): 384 entries, authored books first.
- [Repositories](docs/references/sources.md#repositories): 14 whose mechanisms were adapted and 35 cited without adaptation.
- [Standards and official sources](docs/references/sources.md#standards-and-official-sources): standards bodies, regulators and vendor documentation.
- [Websites and articles](docs/references/sources.md#websites-and-articles).
- [Third-party attributions](docs/source-registers/m10-06-third-party-attributions.md): the per-file record of what was adapted from each repository.

The [reference index](docs/references/README.md) explains the lists.

## Contributing and licence

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`AGENTS.md`](AGENTS.md) before you change the engine. They set the catalogue cap (150 to 180 active skills, hard cap 200), the skill-writing standard and the rule against storing book extractions.

Run the [Verify](#verify) steps, and report any you could not run as `NOT ASSESSED`.

To keep this README readable, follow the conventions in the Standardise section of the [README kaizen record](docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md).

Author: Peter Bamuhigire. Licence: MIT, see [`LICENSE`](LICENSE).
