# Changelog

## 2026-11-08 - Chwezi Infographics Design and Production Quality Standard (generation side)

- Local copy of the Chwezi Infographics Design and Production Quality Standard 1.0.0, the fourth child standard of the Product Excellence Standard (the parent governs product UI/UX, tokens, accessibility, performance, brand adaptation and QA, including mobile and tablet UI; the children govern dashboards and analytics, documents and publishing, presentations and slide decks, infographics and visual communication), under `skills/saas/reporting-and-export-engineering/references/infographics-standard/`: doctrine with eight INFO gates, 82 INFO rules, archetypes and worked cases, mathematics and algorithms (type size about 23.6 pt per metre of reading distance, print ppi, phone canvas scale, lie factor, graph checks for flows, cycles and trees), production and export, agent workflow and QA, currentness register, worked review and the standard-library `check_infographic.py`; identical to chwezi-design-engine apart from parent lines, the local-copy notice and link targets. Linked from the skill's References and from professional-word-output and document-spreadsheet-tooling-readiness.

## 2026-11-08 - Chwezi Presentation and Slide Deck Design Standard (deck generation side)

- Local copy of the Chwezi Presentation and Slide Deck Design Standard 1.0.0 (built from the full handbook edition) under `skills/saas/reporting-and-export-engineering/references/presentation-standard/`: doctrine with eight DECK gates, 58 DECK rules, 29 blueprints by communication job, production contracts (editable PPTX with native objects and theme binding, landscape PDF parity, imagery, motion, devices, charts), mathematics and legibility (venue law: minimum size about 4.5 x farthest viewer distance / screen image height pt; display image size; type scale; grid; image resolution; measured white space; runtime budget), agent workflow and QA, currentness register and a worked review; identical to chwezi-design-engine apart from parent lines, the local-copy notice and link targets. The engine works without that repository. Linked from the skill's References and from professional-word-output and document-spreadsheet-tooling-readiness.

## 2026-11-08 - Chwezi Document Reporting and Publishing Standard (renderer side)

- Local copy of the Chwezi Document Reporting and Publishing Standard 1.0.0 (built from the full handbook edition) under `skills/saas/reporting-and-export-engineering/references/document-publishing-standard/`: doctrine, 87 PUB rules and eight gates, archetypes and blueprints, renderer contracts (one canonical model for HTML, print CSS, PDF and DOCX; determinism; metadata hygiene; Word and LibreOffice round trip), agent contract and QA, mathematics and algorithms (modular type scale, measure, optimal page breaking, largest-remainder rounding, exact arithmetic, nice axis ticks, content hashing, perceptual visual regression), currentness register and a worked review; identical to chwezi-design-engine apart from parent lines, the local-copy notice and link targets. The engine works without that repository. Linked from the skill's References.

## 2026-11-08 - Chwezi Reporting and Dashboards Standard (engineering side)

- New skill `skills/saas/reporting-and-export-engineering`: versioned metric catalogue and one server measure layer, fact and dimension grain with fan-out tests, reconciliation KPI to detail to ledger and screen = PDF = XLSX, report definition registry, immutable generation records, background export jobs, CSV/XLSX formula-injection safety (Chwezi single-quote rule; OWASP tab alternative recorded), A4 print and PDF pipeline with acceptance cases, report authorisation and audit, performance budgets, observability and tenant isolation. Rules cited by ID: RPT-PURPOSE, METRIC, SCOPE, PERIOD, RECON, STATE, VIEW, NARR, SEC, PERF, PRINT, EXPORT, QA; gates RPT-GATE-01..08.
- Local copy of the standard 1.0.0 inside the skill (`references/reporting-standard-doctrine.md`, `references/rules-and-gates.md`); rule IDs and wording identical to the `chwezi-design-engine` copy, including that engine's same-day correction of the "Also trips" column for RPT-GATE-03, 05 and 06. This engine works without that repository.
- Cross-references and corrections in `product-excellence-engineering-gates.md` (RPT gate section), `excel-spreadsheets` (export rule; KES and TZS formats corrected to 2 decimals; display date without leading zero), `saas-business-metrics`, `ai-analytics` (RPT-NARR rules), `python-data-analytics` (zero denominator is not comparable, not 0) and the report-print-pdf reference (legibility floor, ISO 4217 decimals, dates).
- Active catalogue 168 -> 169; plugin manifest 166 -> 167; routing fixtures 242 -> 245 (three owned negatives). Source register: two records and one quarantined record (ISO 14289-2, HTTP 403); `RECONCILED_ON` in `tests/test_source_register.py` moved to 2026-11-08 with a note.
- Validators on Windows 11, 2026-11-08: catalogue guardrails exit 0 (169 active, 0 errors, 16 pre-existing size warnings); guardrail unit tests 10 OK; routing precision@1 225/245, precision@3 245/245, negatives 85 pass 0 fail 4 not assessed; coverage 168 of 169 (`new-project` none, pre-existing); collision gate 0 errors; control plane 0 findings; source register 0 findings; contract gate 163 scanned, 0 errors; Node hook tests 61/61 and 7/7; `git diff --check` exit 0. pytest: 272 passed, 3 skipped, 1 failed (`test_current_checkout_is_under_file_budget`, pre-existing: ignored local folders push the checkout over the 5000-entry limit). Record: [`docs/updates/2026-11-08-reporting-and-dashboards-standard.md`](docs/updates/2026-11-08-reporting-and-dashboards-standard.md).

- Final cross-engine sync (same day): local copies brought to the final canonical 1.0.0 text (narrative rules carried in every engine, copies section, engine-neutral change-record wording, RPT-PRINT-002 under RPT-GATE-03 and RPT-GATE-06, RPT-EXPORT-002 covering line feed and full-width triggers with a single-quote prefix in CSV and string-typed cells in XLSX); six more canonical references copied verbatim so the engine carries the whole capability (`currentness-register.md`, `metric-contract-and-reconciliation.md`, `screen-composition-and-components.md`, `report-blueprints.md`, `print-export-and-lifecycle.md`, `engineering-and-verification.md`); `export-safety-checklist.md` and `excel-spreadsheets` updated to the corrected injection rule. Re-run: guardrails exit 0, routing rank-1 floor 89% met with 0 failures, contract gate 0 errors, pytest 272 passed, 3 skipped, 1 failed (the pre-existing checkout file-budget test).

## 2026-11-08 - Chwezi Product Excellence Standard wiring

- `AGENTS.md` binding rule: any app or system UI work (Android, iOS, KMP/Compose Multiplatform, web front ends, desktop) follows the Chwezi Product Excellence Standard owned by `chwezi-design-engine` (`doctrine/product-excellence-standard.md` and skill `chwezi-product-excellence-standard`), effective 01 Nov 2026, resolved through the engine-routing table.
- New reference `frontend-architecture/references/product-excellence-engineering-gates.md`: hard gates PX-GATE-01..13 mapped to engineering checks (state model, contract and screenshot tests, Baseline Profiles and Macrobenchmark, Android vitals, Core Web Vitals, targetSdk 36, AGP 9 `androidApp`, offline idempotency, mobile-money states, ISO 4217 minor units, token export, backend authorisation), citing the design engine currentness register by ID.
- Mandatory cross-reference block in 14 UI-facing skills; house-style `full` money formatters now take decimals from the ISO 4217 minor unit (UGX 0) instead of a fixed two. Routing index row and section, release-blocking gate row. No new skill; catalogue stays at 168.
- Validators on Windows 11 (Python 3.13.7), 2026-11-08: catalogue guardrails exit 0 (168 active, 0 errors, 16 size warnings, all pre-existing); guardrail unit tests 10 OK; routing precision@1 222/242, precision@3 242/242; coverage, collision gate, control plane, source register (0 findings), contract gate (162 scanned, 0 errors), source-ingestion guardrail, both Node hook tests and `git diff --check` all exit 0. pytest: 272 passed, 3 skipped, 1 failed (`test_current_checkout_is_under_file_budget`: 8214 entries against a 5000 limit, caused by ignored local folders in this checkout such as `benchmarks-private/` and caches; tracked files are 2,540; not caused by this change). Record: [`docs/updates/2026-11-08-product-excellence-standard.md`](docs/updates/2026-11-08-product-excellence-standard.md).
- Wave 2 audit: gate map gains PX-GATE-13 (document numbering); thirteen PX-STATE-001 state IDs from the design policy file with a specified state-matrix CI test; `kmp-development` body rewritten to Compose Multiplatform shared UI with platform adapters and the AGP 9 `androidApp` layout; `android-development` targetSdk 36 rules (no edge-to-edge opt-out, predictive back, sw600dp locks ignored); concrete screenshot, Baseline Profile, Macrobenchmark, web vitals and axe gates with tool versions `NOT_ASSESSED`. Validators unchanged from wave 1 (same pre-existing file-budget pytest failure).

## 2026-11-07 - PHP deployment reference repair

- Corrected the broken relative deployment-reference pointer in `php-modern-standards`. Reused the existing reference; no new skill or copied content. [Validation and recovery](docs/updates/2026-11-07-php-reference-repair.md).

## 2026-11-07 - House style implementation references

- New references for the Chwezi business-app house style (canonical in `chwezi-design-engine`): `android-development/references/house-style-compose.md` (Compose + Material 3 roles, amount type, components, motion gate, guardrail tests G1-G9) and `tailwind-css/references/house-style-web.md` (CSS tokens, Tailwind mapping, amount utilities, components, reduced motion, CI checks W1-W9). Pointers in both parent skills and in `ui-design-system.md`. No new skill; catalogue stays at 168. Record: [`docs/updates/2026-11-07-house-style-implementation-references.md`](docs/updates/2026-11-07-house-style-implementation-references.md).

## 2026-11-06 - Journal descriptions carry the document number

- Rule 12 added to `tenant-document-numbering`: every journal entry posted by a numbered document ends its description with `(NUMBER)`, enforced once in the ledger writer, with a generated test over every posting type and a falling CI ratchet on id-interpolating builders. New reference `journal-descriptions.md`; pointer in `saas-accounting-system`. Record: [`docs/updates/2026-11-06-journal-description-rule.md`](docs/updates/2026-11-06-journal-description-rule.md).

## 2026-11-06 - Source register re-read

- The 14 records that had gone overdue were re-read from their primary pages on 2026-11-05 (22:11 to 22:13 UTC). `check_source_register.py` went from exit 1 with 14 findings to exit 0 with 0 findings.
- Nine pages were unchanged and renewed in place. Four had moved on and were superseded: Next.js v16.4.5 and its 2026-11-03 security release, the Android November bulletin, and AGP 9.5.0. The MySQL 8.4.13 release notes returned HTTP 403, so that record is quarantined and `oracle-cpu-oct-2026-mysql-2026-11-05` was added. A PHP informational advisory was added.
- Skill text updated for the Next.js tenant data security reference, the Android version currency note and the PHP runtime upgrades reference. The README date-gate calendar was recomputed. Record: [`docs/updates/2026-11-06-source-register-reread.md`](docs/updates/2026-11-06-source-register-reread.md).

## 2026-11-06 - MCP HTTP+SSE deprecation dating

- `mcp-integration.md` (line 7) and `apis-for-ai-agents-and-data.md` (line 164) presented MCP revision 2026-07-28 as the point at which the HTTP+SSE transport was deprecated. Both now say it has been deprecated since protocol version 2025-03-26 and that 2026-07-28 reclassifies it under the feature lifecycle policy (SEP-2596). The Roots, Sampling, Logging, handshake and schema clauses are unchanged.
- Re-read from `modelcontextprotocol.io` (changelog, deprecated-features registry, tools page) on 2026-11-05 at 21:25 UTC. Validators unchanged: all exit 0 except the source-register check (the same 14 overdue records before and after). Record: [`docs/updates/2026-11-06-mcp-http-sse-dating.md`](docs/updates/2026-11-06-mcp-http-sse-dating.md).
- `apis-for-ai-agents-and-data.md` (line 164): the bullet listed `server/discover`, `subscriptions/listen`, the Multi Round-Trip Request pattern and a required `resultType` as removals. The changelog (re-read 2026-11-05 at 21:30 UTC) removes only protocol sessions and the `initialize` handshake; the others are additions or a requirement. Reworded; a separate commit.

## 2026-11-05 - README measured refresh

- README "At a glance", "Verify", "Date-triggered gates" and "Quality and improvement" re-measured on Linux (Python 3.14.10, pytest 9.2.0, Node 22.23.1): 168 active skills, 242 routing fixtures (precision@1 222/242, precision@3 242/242), 273 tests passed and 3 skipped, contract gate 162 skills scanned with 0 errors.
- The source-register check exits 1 since 2026-11-04: five Next.js records are past `review_after` 2026-11-03. No record was re-read or extended. Record: [`docs/updates/2026-11-05-readme-measured-refresh.md`](docs/updates/2026-11-05-readme-measured-refresh.md).
- README now describes the tenant document numbering skill and the signup bot-control standard shipped on 5 and 1 November 2026.

## 2026-11-05 - Tenant document numbering standard

- New skill `skills/saas/tenant-document-numbering`: one contiguous, never-reset series per tenant and document type for every user-facing document number, with the counter allocator, issue-time numbering, clash handling, lock order, separate platform and credit-note series, durable idempotency, offline provisional tags, capacity sizing, retrofit rollout, CI ratchet and gap report. Active catalogue 167 -> 168; plugin manifest 165 -> 166; routing fixtures 239 -> 242.
- Removed contradicting guidance: the `MAX+1` journal-number trigger and "gaps are acceptable" rule in `saas-accounting-system`, id-derived reversal references, per-sales-point receipt numbering, and procedure-generated invoice numbers in the SDLC templates.
- Cross-reference lines in 17 related skills and the AI code review gate. Record: [`docs/updates/2026-11-05-tenant-document-numbering-standard.md`](docs/updates/2026-11-05-tenant-document-numbering-standard.md).

## 2026-10-31 - Dev Engine documentation wave after kaizen pass 2

- Install and validation instructions corrected for Linux: `python3` throughout, the ten CI steps with the pinned dependencies and what each needs, `--min-rank1 89` (was 88), and `bash install.sh` because the file is tracked without its executable bit (`fa5c972`, `ef47b6a`).
- New root README sections "Quality and improvement" and "Date-triggered gates": evidence folders, the latest published score (62.5/100 raw and capped), open findings, and the calendar of source-register review dates from 2026-11-04, each date checked by running `scripts/check_source_register.py --as-of` (`fa5c972`).
- Measured figures replace stale ones in the overview documents: 239 routing fixtures at 91.6% precision@1 (was 184 at 96%), CI gate list, tool table, completed items moved out of the open list; new `docs/README.md` index and `docs/kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md` (`17280b9`, `844bef8`).
- Engine names corrected where a document named the research or design engine by a former name or a link outside the repository (`844bef8`).
- README section "What the October 2026 kaizen improved": 13 kept changes from the 29 October and pass-2 cycles, each with its commit, supporting check and before and after figure, marked as re-measured on 2026-10-31 or copied from a named evidence file. The open-findings bullet that said no pass had built the invoice slice's Next.js, Compose or MySQL layers now matches the 29 October validation record, which reports disposable builds that were not repeated (`f3d8a7c`).
- Root README reorganised for readers: a front door (purpose, six measured facts, three-step start), a contents list, a 12-row task-to-skill table, and separate Installation, Verify, Quality, improvements and date-gate sections. The 167-row skill table moved to `docs/skill-catalogue.md` and the book, repository, standards and website lists to `docs/references/`, with summaries and links left in the README. Words fell from 12,579 to 4,685; every command and link target is kept or re-based, and the heading anchors that other files link still resolve (record: `docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md`).
- Portfolio-managed router sentences checked with the shared renderer: nothing to change.
- Pass-2 commits by theme, for reference: currency `f970df0`, `ca94e6b`, `842965b`; portable validators `9979773`; review route `a6735a5`; host paths `39a6898`, `3b7b3f6`; duplicate headings `feccc13`, `d12c250`, `f3b0705`; links `0ca42e0`, `625e5e7`; routing fixtures `9f0369e`, `c4e691f`; invoice slice gaps `8bec17a`; evidence `5eb55c8`, `79df717`.

## 2026-10-31 - Dev Engine kaizen pass 2: currency, tooling portability and hygiene gates

- Re-read all 27 overdue source records against primary pages and reconciled the AI-platform register; overdue records 27 to 0. Added `scripts/check_source_register.py` and a CI step so a lapsed review date fails the build.
- Added `scripts/engine_roots.py`: the control-plane and approval validators now resolve sibling engines from repeatable parent folders, `CHWEZI_ENGINES_ROOT`, former directory names and per-engine overrides, with no drive paths built in.
- Connected review work to its owning checks: a root router row, a domain-owned checks table in the review gate, and the posting-service name aligned with the accounting skill.
- Added `scripts/content_hygiene.py` (host-specific paths, duplicate H2 headings, broken relative links; ratchets that may only shrink). Removed host paths and leaked tool markup from active content, merged 57 skills' duplicate sections losslessly (65 to 24 files with a duplicate), repaired 33 links.
- Added a first positive routing fixture for 42 skills and `--coverage` with a CI ceiling; precision@1 177/196 to 219/239.
- Evidence, scores and open items: [`docs/kaizen/2026-10-engine-kaizen-pass-2/`](docs/kaizen/2026-10-engine-kaizen-pass-2/README.md).

## 2026-10-29 - Dev Engine security, currentness and package evidence

- Replaced unsafe Next.js role-cookie/global-cache examples with server-side tenant authorization guidance and a tested illustrative read-only invoice path; added routing and regression checks.
- Added a synthetic PHP/OpenAPI/Next.js/Compose invoice slice, with a [15-check PDO SQLite fixture](examples/tenant-invoice-listing/php/test.php) and an explicit unverified MySQL/Android/Next build boundary.
- Added a non-executable [manual review exercise](examples/tenant-invoice-listing/review-exercise.md) with four grouped findings drawn from the frozen practitioner specimen.
- Updated Android Play target and platform-currentness guidance; added selected PHP/PostgreSQL advisory checks and source records.
- Added portable Codex plugin and repository marketplace manifests, file-budget checks, and the measured prompt-input context-budget invocation.
- Evidence, limits and scorecard: [`docs/kaizen/2026-10-engine-kaizen/`](docs/kaizen/2026-10-engine-kaizen/README.md).

## 2026-09-29 - Kaizen M10-06: methodology and comprehension absorption

- Engine-native design gate replaces the mandatory Superpowers step in `new-project`; ceremony
  classes, claim/evidence table, Excuse/Reality table, dispatch controls, worktree safety,
  receiving review, plan header, quality-bar guard, output registers and lane report shapes.
- Comprehension: graph-first reference, evidence tags, topology-ordered tours, tour validator,
  architecture-as-code with a commit-pinned evidence verifier, and a read-only PHP/MySQL route map
  (pilot KEEP). Active catalogue unchanged at 167; aliases 76 -> 78; routing fixtures 184 -> 187.
- 45 tracked orphan folders dispositioned (merge, quarantine, alias). See
  `docs/updates/2026-09-29-m10-06-methodology-and-comprehension.md`.

## 2026-09-24 - Kaizen: book-extraction retirement, currentness, consolidation

- Removed `book-extractions/`; knowledge folded into task references; guardrail rejects extraction
  folders, links and local-ebook citations. See `docs/updates/2026-09-24-book-extraction-removal-and-kaizen.md`.
- Restored 126 `compatible_with` corruptions to `claude-code`; validators use the canonical engine
  id `chwezi-dev-engine`; 88 GitHub Actions pins moved to current majors.
- Ingested 20+ engineering titles as paraphrased references (API styles, JSON/schema, OWASP API,
  MCP 2026-07-28, LLM/agent security, performance, React/TS, React Native, DevOps, Python/pandas 3,
  ML feature pipelines, data contracts, lineage, accessibility testing).
- OWASP LLM citations re-mapped to the Top 10 for LLM Applications 2026 (published 2026-08-03);
  every citation now carries its edition year.
- Consolidation (authorised by Peter Bamuhigire): 18 overlapping skills merged into their owners as
  references with inactive `ALIAS.md` routes; active catalogue 185 -> 167. Target range raised
  to 150-180 (hard cap 200). Routing fixtures 160 -> 184, precision@3 100%.

## 2026-08-05 - Managed SaaS Visual Assets

- Added `saas-managed-visual-assets` as the engineering owner for scoped background pools,
  light/dark logos, favicons, admin lifecycle, concurrency-safe quotas, audit, and rollback.
- Strengthened `image-compression` so browser preflight is explicitly non-authoritative and the
  server must bound, detect, decode, canonicalize, preserve alpha where needed, and store private
  random-keyed output.
- Added positive and collision routing fixtures plus an end-to-end worked example.

## 2026-07-08 - Engine Upgrade Foundation

- Added root `SKILL.md` router for the active engineering catalog, cross-engine handoffs, evidence-pack workflow, and stop conditions.
- Added July 2026 upgrade directories for source registers, quality gates, world-class exemplars, shared templates, full-workflow examples, and routing tests.
- Added empty-directory disposition guidance for the remaining active-looking empty paths without deleting user-visible compatibility directories.
- Added the FieldOps Ledger running example for architecture, API, database, security, reliability, and release-evidence artifacts.
- Added Digital Research Skills Engine integration logging and path correction from the prompt's unavailable path to the verified local engine at `C:\wamp64\www\digital-research-engine`.

## 2026-07-08 - Engine Upgrade Completion

- Added architecture, API, security, reliability, and delivery evidence-pack templates.
- Added the completed FieldOps Ledger full-stack SaaS exemplar and negative quality fixtures.
- Expanded routing smoke coverage to 117 fixtures with precision@1 97%, precision@3 100%, and 0 failures.
- Added engineering anti-slop governance, release-blocking gates, and benchmark/cross-engine standards reference.
- Added Phase 1, Phase 2, and final upgrade reports.
- Rebuilt the root `README.md` around the July 2026 operating model.
# 2026-11-01

- Added the signup human-validation standard to the engineering skills and threat model, with Turnstile as the web default and Play Integrity plus Turnstile fallback for Android.

- 2026-11-07: Repair posting-skeleton audit/idempotency atomicity; synthetic failure and retry proof in `docs/updates/2026-11-07-posting-atomicity.md`.
