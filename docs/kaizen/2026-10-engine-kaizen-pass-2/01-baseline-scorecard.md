# Frozen baseline scorecard (pass 2)

**Snapshot:** `main` at `27a602b8306ff7aa6e84b5890a59abd57c8e2f4a`, before any change
**Date:** 2026-10-31
**Scoring:** each dimension /100, overall is the arithmetic mean. Scores are practitioner
judgement anchored to the evidence named, not test-pass percentages. Defect IDs refer to
[00-scope-and-evidence.md](00-scope-and-evidence.md). This file is frozen before the first
experiment; later results go in the validation record and final report.

## Scores

| Dimension | Raw | Evidence | One-line deficiency |
|---|---:|---|---|
| Doctrine | 72 | `world-class-engineering`, `AGENTS.md`; D-02, D-03, D-11 | A review task has no connected route, the posting-service name drifts, and router text hard-codes one machine's layout. |
| Taxonomy and routing | 62 | p@1 177/196 (90.3%), p@3 196/196; 82 owned negatives (78 pass, 4 `NOT_ASSESSED`); 13 of 167 skills at three positives plus two owned negatives; 43 with none; full Task 1 request misroutes at rank 1 (proxy) | Rank-1 and coverage gaps, and no repository-owned coverage measure (D-19). |
| Skill depth | 50 | 65 `SKILL.md` files with an exact duplicate H2 (D-17) | Duplicated sections dilute task-specific instructions; the gate does not see them. |
| Applied proof | 52 | PHP fixture `15 checks passed` reproduced; shim-run `220 passed, 3 skipped` equals pass 1's real-pytest count; 40 of 167 skills have a worked-example heading, 0 of 25 in game development; Next, Compose and MySQL runs not reproducible here | Strong proof for one slice, thin elsewhere; three of four layers cannot be re-run on this host. |
| Standards currency | 50 | 27 of 65 register records overdue; `ai-platforms.md` 11 of 13 rows overdue, three moved URLs (D-15, D-16); platform spot checks on 2026-10-31 all matched pass-1 values | Overdue AI-platform and model records, including those the router names as a first stop. |
| Output readiness | 55 | Slice defects D-01, D-04, D-05, D-06, D-07, D-08, D-09 | No pagination, non-standard errors, raw minor units shown to users. |
| Accessibility and inclusion | 58 | Semantic table and explicit Compose states (pass 1); D-08 | Hard-coded strings, missing landmark and live regions; no assistive-technology run. |
| Production and handoff | 45 | Control-plane and approval validators fail on this host for path reasons (D-10); `pytest` absent so the CI test command cannot run; file budget 2498 of 5000 package entries | Validators are not portable across the user's own machines; no deployment, recovery or MySQL evidence. |
| Hygiene | 40 | D-11 (path lines in active content), D-12, D-13, D-14, D-17, D-18 | Machine paths, leaked tool markup, tracked local settings, 142 broken links, duplicate headings. |
| Safety and integrity | 66 | PHP tenant, auth, input and escaping checks pass; no critical defect; D-13 personal data in a public repository; ledger check not routed from review | Tenant and authorisation guidance is sound; review route and personal-data hygiene are weaker. |

**Raw mean:** (72 + 62 + 50 + 52 + 50 + 55 + 58 + 45 + 40 + 66) / 10 = **55.0**.
**Portfolio Standard cap:** min(55.0, 65) = **55.0/100**.
**For comparison, 29 October final (pass 1):** raw mean 59.5, capped 59.5. The two are not a
trend: pass 1 scored the engine as it stood after its fixes without checking the items found
here, and this baseline scores the full tree afresh.
The 95/100 target stays an improvement target, not an achievement claim.

## Measured inputs (all re-measured on 2026-10-31)

| Measure | Value | Command or method |
|---|---|---|
| Active skills | 167 | catalogue guardrails |
| Catalogue guardrails | exit 0; 0 errors, 14 report-only size warnings | `python3 -X utf8 scripts/skill_catalog_guardrails.py` |
| Routing | exit 0; 196 fixtures, p@1 177/196 (90.3%), p@3 196/196; negatives 82 (owned 82; pass 78, fail 0, not assessed 4); fixture lint 0 | `python3 scripts/routing_smoke_test.py --lint-fixtures` |
| Collision gate | exit 0; one pair, allow-listed | `... --collisions --collision-gate --threshold 0.5` |
| Contract gate | exit 0; 161 scanned, 0 errors, 6 exempt | `python3 -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --all` |
| Control plane, default parent | exit 1; 11 findings, all "no candidate contains router" | `... validate_engine_control_plane.py --workspace-root ..` |
| Control plane, `skill-engines` root | exit 1; 6 findings (4 old repository names, Linux checkout elsewhere, private entry absent) | `... --workspace-root <home>/skill-engines` |
| Control plane, registry only | exit 0; 12 entries, 0 findings (CI form) | `... validate_engine_control_plane.py` |
| Approval adapters, defaults | exit 1; 10 findings, all missing Windows paths | `... validate_approval_adapters.py` |
| Approval adapters, explicit roots | exit 0; 11 adapters, 0 findings | same with ten `--engine-root` overrides |
| Hook tests | 61/61 and 7/7 | `node hooks/test-destructive-bash-gate.js`, `node hooks/test-plugin-hook-config.js` |
| Tenant example structure check | PASS | `python3 scripts/validate_tenant_invoice_example.py` |
| PHP fixture | `15 checks passed` (SQLite) | `php examples/tenant-invoice-listing/php/test.php` |
| File budget | 2827 checkout entries, 2498 package-oriented, limit 5000 | `python3 scripts/check_package_file_budget.py` |
| Unit tests under `unittest` | 55 collected; 6 modules need `pytest`; many modules use plain test functions that `unittest` does not collect | `python3 -m unittest discover` (partial) |
| Whole suite, stand-in runner | `220 passed, 3 skipped, 0 failed` (shim-run, not pytest) | local stand-in runner |
| Real `pytest` | `NOT_ASSESSED`: module not installed | `python3 -c "import pytest"` fails |
| Overdue source records | 27 of 65 | Digital Research `validate_source_currency.py --as-of 2026-10-31` on the register, exit 1 |
| Routing coverage | 124 skills with at least one positive; 43 with none; 13 with three positives and two owned negatives | script over `routing_fixtures.yml` and `tests/routing/edge-fixtures.yml` |
| Worked-example depth | 40 of 167 skills have a worked-example heading (SKILL.md or references) | heading search; definition-dependent |
| Exact duplicate H2 | 65 `SKILL.md` files | fenced-code-aware scan |
| Machine-specific paths | 56 files with a `wamp64` path (208 hits); in active scopes (router, skills, scripts) 58 lines, of which about 30 are real sibling-engine or client-project paths, the rest are deliberate examples | pattern scan of tracked files |
| Broken relative links | 142 of 1,599 in tracked Markdown; 16 more point outside the repository | link scan |
| Dangling cross-engine references | 0 of the 15 path-style references; each resolves in the sibling checkout (two use skill-name shorthand) | path check against sibling checkouts |
| Expired source records | 27 (same list as pass 1) | as above |

## Blockers and `NOT_ASSESSED`

- Blockers: none critical. D-13 (personal data in tracked file) is escalated, not fixed.
- `NOT_ASSESSED`: real `pytest` run; Next.js build and runtime; Compose build; MySQL
  migration run; live-model routing; Tier 3 behavioural runs; four cross-engine owner
  negatives (evaluated in union mode elsewhere); the Next.js notice due 2026-11-03;
  independent review.
