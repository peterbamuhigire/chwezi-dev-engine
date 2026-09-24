# 2026-09-24 - Book-extraction removal and Kaizen repairs

## Copyright cleanup

- Removed `book-extractions/` (21 tracked files). Durable knowledge was folded
  as paraphrased, task-oriented references:
  - `skills/sdlc-meta/world-class-engineering/references/slice-review-and-recovery-practice.md`
    (replaces the 2026-09-14 practice note; five skills repointed);
  - `skills/saas/subscription-billing/references/price-versioning-and-plan-migration.md`;
  - `skills/saas/saas-business-metrics/references/revenue-lifecycle-data-contract.md`;
  - `skills/ai/ai-agent-compliance-controls/references/eu-ai-act-and-iso-42001-agent-overlay.md`
    and `continuous-control-monitoring.md`;
  - `skills/ai/ai-agent-sla-and-customer-commitments/references/provider-recourse-and-multi-agent-attribution.md`;
  - UX practice folded into the design engine (`design-system-skills`).
- The two game-development source-disposition records (titles only, no book
  content) moved to `docs/game-dev-analysis/source-disposition-*.md`.
- Local ebook paths and shadow-library file names removed from eight source
  registers and from `docs/game-dev-analysis/source-register.md`.
- Book-derived rule catalogues trimmed from
  `docs/plans/2026-03-21-ux-book-study-improvements.md` and
  `docs/superpowers/plans/2026-05-06-claude-skills-uiux-phase2.md`; three
  UX specs marked superseded.
- "Never store book extractions" added to `AGENTS.md` and `CLAUDE.md`.
- `scripts/source_ingestion_guardrail.py` now fails on any file in an
  extraction folder, `*-extraction.md` book files, Markdown links into an
  extraction folder, and local-ebook or shadow-library citations (tests added).

## Registry and currentness repairs

- Validators and tests used the stale engine id `skills-web-dev`; aligned to
  the canonical `chwezi-dev-engine` already used by the registry, manifest,
  approval adapter and `chwezi-engine-agents` catalogue.
- Active count surfaces updated from 171 to the measured 185 (15 above the
  150-170 soft target; consolidation is an open item in `NEXT_FEATURES.md`).
- 126 files carried `compatible_with: [Codex, codex]` (claude-code corrupted
  to Codex); restored to `claude-code, codex`. Eleven prose corruptions
  (for example `platform.Codex.com`, `Codex-haiku-4-5`) corrected.
- ISO/IEC 27001 Annex A numbers moved to the 2022 edition; PHP supported-branch
  baseline added to `php-modern-standards`; working-memory guidance corrected
  from 7 plus/minus 2 to about four chunks (Cowan 2001).
