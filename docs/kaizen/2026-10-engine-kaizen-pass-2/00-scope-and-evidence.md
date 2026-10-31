# Scope and evidence (pass 2)

**Cycle:** 2026-10 Dev Engine kaizen, pass 2 (continuation of the 2026-10-29 pass)
**Date and access date:** 2026-10-31
**Branch:** `kaizen/2026-10-pass2`, created from `main`
**Starting HEAD:** `27a602b8306ff7aa6e84b5890a59abd57c8e2f4a`
**Owner:** Chwezi Dev Engine
**Status:** observations and baseline frozen before any change; see
[01-baseline-scorecard.md](01-baseline-scorecard.md).

## Step 0: preconditions

- `git status --porcelain` at start: empty. No other person's uncommitted files needed
  to be preserved or excluded.
- Starting branch `main`, HEAD as above. The pass-1 branch `kaizen/2026-10` has no
  commits that `main` lacks, so the 29 October evidence is on `main`.
- Standard and gate read: the Portfolio Kaizen Standard (August 2026) and the Digital
  Research currentness gate. The research `source-evaluation` and `source-verification`
  skills were located in the sibling Digital Research checkout.
- Pass-1 inputs read: [05-final-report.md](../2026-10-engine-kaizen/05-final-report.md),
  [06-next-cycle.md](../2026-10-engine-kaizen/06-next-cycle.md), its baseline, backlog,
  experiment log and validation record.
- `AGENTS.md` and `skills/sdlc-meta/kaizen-improvement-system/SKILL.md` read. That skill
  has no `prompts/full-kaizen-operation.md`; the prompt names a file this checkout does not
  contain (finding, minor).

### Environment and limits

Linux workstation, Python 3.14.8, Node 22.23.1, PHP 8.5.12 CLI. There is no `pytest`, no
`pwsh`, no Gradle or Android SDK and no network installs. Consequences, all recorded as
`NOT_ASSESSED` unless stated: a real `pytest` run, the Next.js build, the Compose build,
the MySQL migration run, and any live-model routing run.

Substitute used for `pytest`: a local stand-in that implements only the pytest features
this repository's tests use (`parametrize`, `skipif`, `fixture`, `tmp_path`, `monkeypatch`,
`capsys`). It lives outside the repository and is not a pytest result. It is labelled
"shim-run" everywhere. As a cross-check, it collected and passed exactly the counts that
pass 1 recorded under real pytest (`220 passed, 3 skipped`) on the same tree.

For the control-plane validator the sibling parent is the `skill-engines` folder in the
user's home directory; the Dev Engine and Linux checkouts live in the skills folder under
`.claude`. Both roots were tried (results in the baseline).

## Step 1: practitioner tasks

Method: the engine was used through its router (`SKILL.md`, `docs/skill-routing-index.md`)
and its own routing proxy (`scripts/routing_smoke_test.py` ranking), not through a live
model. Routing results below are lexical-proxy ranks over `name` and `description`; they
indicate what the descriptions signal, not what a model would choose.

### Task 1: tenant-scoped invoice listing, PHP house stack

Request: migration, repository, service, controller, API contract, tests and UI.

Router choice (proxy, full request text): `typescript-full-stack` 0.32, `advanced-testing-strategy`
0.20, `ai-feature-spec` 0.18, `php-modern-standards` 0.16. A shorter database-focused
phrasing ranks `mysql-engineering` then `php-modern-standards` first. **Judgement: the full
request misroutes at rank 1** (the word "stack" and "UI" pull toward TypeScript), although the
right skills are in the top five. The human route (`world-class-engineering`,
`php-modern-standards`, `mysql-engineering`, `multi-tenant-saas-architecture`,
`api-design-first`) is correct.

Output assessed: the existing teaching slice `examples/tenant-invoice-listing/` (the
artefact the engine's own guidance produced in pass 1). Reproduced now:
`php examples/tenant-invoice-listing/php/test.php` printed `15 checks passed` (PDO SQLite).
Verify-before-done gate: the slice ships its own check command and states its limits, but no
evidence pack from `templates/delivery-dod/evidence-pack.md`, which the router lists as
non-negotiable foundation item 3 for implementation deliverables (D-09).

### Task 2: review of a flawed snippet (injection, missing tenant filter, N+1, ledger write)

Specimen: `examples/tenant-invoice-listing/review-exercise.md`.

Router choice (proxy, task text): `php-modern-standards` 0.14, `customer-service-excellence` 0.10,
`multi-tenant-saas-architecture` 0.08, `ai-security` 0.07. The ledger-boundary phrasing alone
ranks no accounting skill in the top five. A generic "code review of this pull request"
phrasing ranks `ai-assisted-development`, `code-safety-scanner`, `web-app-security-audit`.
The root router has no review row (D-02).

Does the engine catch all four? Yes, but only by loading four separate places that the
router does not connect for a review task:

| Defect | Where the engine states the check |
|---|---|
| SQL injection | `ai-assisted-development/references/ai-generated-code-review-gate.md`, Security row ("string-built SQL"); `php-modern-standards` |
| Missing tenant predicate | same gate, Security row ("missing authorisation or tenant scope"); `multi-tenant-saas-architecture` |
| N+1 query | same gate, Data access row; `php-modern-standards/references/database-orm-patterns.md` |
| Ledger write outside the posting service | `finance-accounting/accounting-engine/SKILL.md` Hard Rules and `references/chwezi-finance-engine-skeletons/reviewer-checklist.md`; not linked from the review gate |

Naming drift: the review exercise says `JournalPostingService`; the engine's accounting
skill defines `LedgerPostingService::post()` "or the project-equivalent single posting
service". No skill defines the first name (D-03).

### Task 3: Compose screen and Next.js page, supported platform versions

Both artefacts exist in the slice. Versions confirmed against official pages on 2026-10-31
(details in the currency table below): Play target API 36 or higher for general apps;
Android 17 is API 37; Kotlin 2.4.21; Compose BOM 2026.09.00; Next.js 16.4.3 is the latest
stable release and 16.x is Active LTS. The Android and Next.js skills state these correctly
and separate Play target from compile API. Router choice was correct (`android-development`,
`nextjs-app-router`).

## Defects found (file and line, at the starting HEAD)

Severity: critical = safety, privacy, legal, financial or release blocker; major = wrong or
incomplete output a reviewer would reject; minor = polish or hygiene.

| ID | Sev. | Location | Defect |
|---|---|---|---|
| D-01 | major | `examples/tenant-invoice-listing/php/invoice-list.php:28`; `api.yaml:10-22`, `37-47` | `ORDER BY i.id LIMIT :limit` with no cursor and no next-page field: the listing cannot reach row 101. The README calls it a listing end to end. |
| D-02 | major | `SKILL.md` route-by-intent table | No review or pull-request-review row; a review task has no connected route to the four owning checks. |
| D-03 | minor | `examples/tenant-invoice-listing/review-exercise.md:21` vs `skills/finance-accounting/accounting-engine/SKILL.md:81` | Posting-service name differs between the exercise and the owning skill. |
| D-04 | major | `api.yaml:48-50`; `php/invoice-list.php:66,73,75`; `nextjs/app/api/invoices/route.ts:159,169,172` | Error bodies are `{error: ...}` with no declared schema; the engine cites RFC 9457 and does not follow it in its own contract. No `securitySchemes` or `security` in `api.yaml`. |
| D-05 | major | `php/invoice-list.php:83`; `nextjs/app/invoices/page.tsx:132,136`; `android/InvoiceListScreen.kt:233` | End users see raw minor units ("Amount in minor units"); no currency exponent in the contract, so correct display is impossible. |
| D-06 | minor | `php/invoice-list.php:31` | `%` and `_` in the search text act as LIKE wildcards. |
| D-07 | minor | `php/2026_10_29_create_tenant_invoices.sql` | No rollback statement or stated rollback path for the migration. |
| D-08 | minor | `nextjs/app/invoices/page.tsx:119`; `android/InvoiceListScreen.kt:216-233` | Denied state has no landmark; Compose strings are hard-coded English; loading and failed states carry no live-region semantics. |
| D-09 | minor | `examples/tenant-invoice-listing/README.md` | No evidence pack per router foundation item 3. |
| D-10 | major | `scripts/validate_engine_control_plane.py:12-26,49`; `scripts/validate_approval_adapters.py:12-21` | Hard-coded Windows checkout names and paths (`C:\wamp64\www\...`, `D:/political-skills`), and old repository names. On this machine `--workspace-root` cannot succeed for any sibling layout; the approval validator fails with 10 findings that vanish when the same paths are supplied by `--engine-root`. Environment-only failure, not a contract failure. |
| D-11 | major | `AGENTS.md:40,171,275,285`; `SKILL.md:25`; `docs/engine-control-plane.md:18,38,74,78,121`; `docs/skill-routing-index.md:142-143`; `skills/sdlc-meta/kaizen-improvement-system/SKILL.md:121,132`; `skills/sdlc-meta/world-class-engineering/references/solution-selection.md:50,53,56`; `skills/product-business/hospitality-hotel-restaurant-systems/SKILL.md:124-125`; `skills/sdlc-meta/advanced-testing-strategy/references/accessibility-testing-automated-and-manual.md:9`; `skills/frontend-ux/ux-principles-101/ALIAS.md:13` | Machine-specific absolute paths to sibling engines in router and active skill content. The engine's own rule says to resolve per device. |
| D-12 | minor | `skills/sdlc-meta/custom-sub-agents/references/01-...md:781` to `08-...md:1786` (8 files, last two lines of each) | Leaked tool-call markup (`</content>`, `<parameter name="filePath">`) naming a client ERP project path, inside a code fence. |
| D-13 | major (privacy, escalated) | `.claude/settings.local.json` (tracked) | A user-local permission list with 48 Windows user-profile path occurrences (two profile names) is tracked in a public repository. Not a secret, but personal data and machine-specific. Untracking is a decision for Peter (see escalation below). |
| D-14 | minor | `docs/kaizen/2026-10-engine-kaizen/*.md` | Pass-1 evidence cites a temporary folder that no longer exists (26 citations across four files) and holds two absolute home-directory paths in `04-validation-record.md`. The claims are not re-checkable from the repository. |
| D-15 | major | `docs/source-registers/skills-engine-currentness-2026-09.json` | 27 of 65 source records are past `review_after` (the 27 pass-1 carried forward). |
| D-16 | major | `docs/source-registers/ai-platforms.md` | Page last verified 2026-07-08; 11 of 13 rows are past their next-review date (earliest 2026-08-08); two rows fall due on 2026-11-02. Three canonical URLs have moved (below). The router names this register as foundation item 4. |
| D-17 | major | `skills/**/SKILL.md` (65 files) | Exact duplicate H2 headings (`references` 26, `anti-patterns` 25, `outputs` 16, `required inputs` 15, others). The catalogue gate does not detect it. |
| D-18 | minor | `skills/**` markdown (142 of 1,599 relative links) | Broken relative links, mostly in merged-skill reference folders (`../SKILL.md` and `references/...` that no longer resolve). The guardrail checks only part of the tree. |
| D-19 | major | `scripts/routing_fixtures.yml`, `tests/routing/edge-fixtures.yml` | 43 of 167 skills have no positive routing fixture; 13 have three positives and two owned negatives. No repository-owned coverage measure exists. |

No critical defect was found. D-13 is a privacy hygiene issue judged major and escalated,
because it needs a decision about tracked user content and history.

## Guidance missing, contradictory or ignored

- Missing: a review route that ties generic review checks to domain-owned checks (D-02).
- Contradictory: posting-service name (D-03); the router lists `docs/source-registers/ai-platforms.md`
  as a first stop while that register is past review (D-16).
- Ignored by the engine's own artefact: RFC 9457 and minor-unit display (D-04, D-05).
- Prompt text refers to `prompts/full-kaizen-operation.md` in the kaizen skill; the file is absent.

## Confirmation of the prompt's open findings

| Finding in the prompt | State at 2026-10-31 |
|---|---|
| Android target SDK 35 | Fixed in pass 1 (`android-development/SKILL.md:50,209` say API 36 or higher, Play target separate from compile API). Re-confirmed against the Play page today. |
| Next.js removed APIs and middleware convention | Fixed in pass 1 (async request APIs, `proxy.ts`, server-side tenant guard). |
| PostgreSQL stopped at version 16 | Not a version pin: `postgresql-engineering/SKILL.md` tells the reader to check supported majors before selecting. Official page today lists majors 14 to 18 (18.6 current; 14 reaches final release 2026-11-12). Acceptable; recorded in the register. |
| Duplicated Inputs/Outputs/Decision-rules headings in 59 skills | Open. Fresh exact-H2 count is 65 files (D-17). |
| Applied proof sparse (42/100) | Partly improved by the invoice slice. Heading-based worked-example count is 40 of 167 skills; game development 0 of 25 by the same test. Open. |
| `professional-word-output` registers Inter and Arial | Fixed (no `Inter` or `Arial` match under that skill). |
| Routing fixture coverage (11 with three positives and two owned negatives; 43 with none) | Open. Fresh: 13 and 43 (D-19). |

## Pass-1 backlog confirmation

Pass-1 carry-forward items 1 to 8 were checked. Item 1 (Next.js notice dated 2026-11-03) cannot
be actioned before that date. Items 2 to 4 and 6 need installs, a database container or a Gradle
project that this host forbids (`NOT_ASSESSED`). Item 5 needs an independent human. Item 7 is
covered by the model-currentness check below. Item 8 is this cycle's S01.

## Currency spot checks (2026-10-31)

All values come from the named page on the access date; page text was read through a fetch
tool, so figures are as that tool reported them. None were guessed.

| Claim | Source | Result |
|---|---|---|
| Play target API | Google Play Console Help, "Target API level requirements" | API 36 or higher for new apps and updates for general apps by 2026-08-31; Wear OS and Automotive API 35; extension to 2026-11-01 may be requested. |
| Next.js | GitHub releases and nextjs.org support policy | Latest stable v16.4.3 (page shows 23 Oct); 16.x Active LTS; 15.x Maintenance LTS, security releases through 2027-01-31. Canary 16.5.0 exists. The 2026-11-03 notice is not yet published. |
| PHP | php.net supported versions | 8.2 security only to 2026-12-31; 8.3 security to 2027-12-31; 8.4 active to 2026-12-31; 8.5 active to 2027-12-31. |
| PostgreSQL | postgresql.org versioning | Majors 14 to 18; current minors 14.24, 15.19, 16.15, 17.11, 18.6; 14 final release 2026-11-12. |
| MySQL | MySQL 8.4 release notes | Latest 8.4.13 (2026-10-20). |
| OWASP Top 10 | top10.owasp.org | OWASP Top 10:2025, ten categories A01 to A10; no day-level date shown. |
| OWASP ASVS | asvs.owasp.org | 5.0.0, stable, published 2025-05-30. |
| PCI DSS | PCI SSC document library | v4.0.1 featured as current; publication date not shown by the fetch; no newer version listed. |
| SLSA | slsa.dev/spec | Version 1.2, status Approved; release date not shown. |
| Kotlin | kotlinlang.org releases | 2.4.21 (2026-10-08); previous 2.4.20 (2026-09-07). |
| Compose BOM | developer.android.com BOM mapping | 2026.09.00 latest; previous 2026.08.00. |
| Android Gradle Plugin | developer.android.com AGP page | 9.5 listed as newest stable, 9.6 preview; API 37 needs AGP 9.1.1 or later. Pass-1 records say 9.1.1 as the minimum for API 37 and did not claim latest. |
| NIST AI RMF | nist.gov AI RMF page | AI RMF 1.0 (2023-01-26), page says it is being revised; Generative AI Profile 2024-07-26. |
| OpenAI model catalogue | developers.openai.com models page | `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna` listed; four audio models deprecated. Model policy unchanged (see model review in the validation record). |
| Moved canonical URLs | HTTP redirects | OpenAI changelog now at `developers.openai.com/api/docs/changelog` (301); OpenAI Codex docs now at `learn.chatgpt.com/docs` (308); Claude Code docs now at `code.claude.com/docs/en/` (301). |
| Bedrock Agents | AWS docs | Now "Bedrock Agents Classic", closed to new customers, AgentCore recommended. No skill hard-codes it; only the register row mentions it. |

## Measured inputs (frozen)

See [01-baseline-scorecard.md](01-baseline-scorecard.md).

## Escalation for Peter

D-13: the tracked `.claude/settings.local.json` holds user-profile paths. Options:
`git rm --cached` plus a `.gitignore` entry (the file stays on disk, history still holds it),
or leave it. Not actioned: it is user-authored configuration and the history question is
Peter's call.
