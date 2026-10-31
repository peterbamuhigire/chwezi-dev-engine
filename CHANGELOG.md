# Changelog

## 2026-10-31 - Dev Engine documentation wave after kaizen pass 2

- Install and validation instructions corrected for Linux: `python3` throughout, the ten CI steps with the pinned dependencies and what each needs, `--min-rank1 89` (was 88), and `bash install.sh` because the file is tracked without its executable bit (`fa5c972`, `ef47b6a`).
- New root README sections "Quality and improvement" and "Date-triggered gates": evidence folders, the latest published score (62.5/100 raw and capped), open findings, and the calendar of source-register review dates from 2026-11-04, each date checked by running `scripts/check_source_register.py --as-of` (`fa5c972`).
- Measured figures replace stale ones in the overview documents: 239 routing fixtures at 91.6% precision@1 (was 184 at 96%), CI gate list, tool table, completed items moved out of the open list; new `docs/README.md` index and `docs/kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md` (`17280b9`, `844bef8`).
- Engine names corrected where a document named the research or design engine by a former name or a link outside the repository (`844bef8`).
- README section "What the October 2026 kaizen improved": 13 kept changes from the 29 October and pass-2 cycles, each with its commit, supporting check and before and after figure, marked as re-measured on 2026-10-31 or copied from a named evidence file. The open-findings bullet that said no pass had built the invoice slice's Next.js, Compose or MySQL layers now matches the 29 October validation record, which reports disposable builds that were not repeated (`f3d8a7c`).
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
