# Documentation Update - 2026-05-30

## Summary

Production-readiness audit against the six-point delivery checklist, plus
concrete repairs to the validation and enforcement layer.

## Changes

- Added `docs/evaluation/2026-05-30-production-readiness-audit.md` - metrics,
  scorecard, and prioritised open work for all six checklist questions.
- Upgraded `scripts/skill_catalog_guardrails.py`:
  - `check_broken_references` - fails on `references/`/`templates/`/`scripts/`
    links that do not resolve (ignores `*`/`<>` template placeholders).
  - `check_alias_integrity` - fails on unrouted `ALIAS.md`, stale registry
    routes with no file, and dangling routes to non-existent skills.
- Added `.github/workflows/skill-guardrails.yml` - runs the guardrails
  (enforcing mode) on push/PR touching skills, doctrine, aliases, or the script.
- Corrected active-skill count drift (169 -> 172) in `README.md`, `AGENTS.md`,
  `docs/skill-routing-index.md`, and `docs/skill-aliases.yml`; reframed the
  script as the source of truth.

## First-run findings

- Broken references: **55** across 20 skills (now CI-blocking once repaired).
- Alias integrity: clean (47/47 routed, all targets resolve).
- Active count 172 - 2 over the 150-170 soft target, under the 200 hard cap.

## Same-day execution pass (multi-agent)

- Repaired all 55 broken references: 21 new production-grade SaaS reference
  files, 24 reorg breaks repointed to owning skills, plus
  `professional-word-output/scripts/create-reference-docx.py` and
  `00-meta-initialization/references/detection-rules.md`. Guardrail now reports
  **0 broken references catalog-wide**.
- Added the **Delivery Definition of Done** gate
  (`skill-composition-standards/references/delivery-definition-of-done.md`) and
  wired it into the standard-artifact table and the `world-class-engineering`
  Output Contract.
- Added `docs/USING-IN-A-PROJECT.md` (integrator guide) and
  `docs/CLIENT-VALUE-BRIEF.md` (client one-pager); linked both from `README.md`.

Scorecard after the pass: five of six checklist questions PASS; routing remains
PARTIAL pending consolidation and a routing smoke test (both P3, improvements to
an already-passing system).

## Routing pass (P3, completed same day)

- Added `scripts/routing_smoke_test.py` + `scripts/routing_fixtures.yml` (32
  fixtures); wired into the CI job. Headline: precision@1 84%, precision@3 100%.
  It caught two real defects (`ai-security`, `dpia-generator` descriptions
  missing user-facing trigger terms); both sharpened.
- Evidence-driven consolidation: the `--collisions` detector found no true
  duplicates (remaining high-similarity pairs are intentional platform/concern
  splits). Merged the one genuine overlap: `premium-product-positioning` ->
  `premium-software-product-execution` (172 -> 171 active; 48 aliases).
- All six checklist questions now PASS. Routing is measured, not asserted.

## Remaining

None of the six checklist questions remains open. Optional future hardening:
grow the fixture set with new skills; promote `--collisions` to an allowlisted
hard gate; revisit the 150-170 soft target now that precision is measured.
