# Changelog

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
