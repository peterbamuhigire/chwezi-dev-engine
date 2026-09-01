# 24-Book Cross-Engine Kaizen Implementation Plan

## Wave 0 — evidence and control-plane repair

1. Add the portfolio study record at `docs/continuous-improvement/book-driven-kaizen-wave-2-2026-09-01.md` with the 24-source ledger, completeness statuses, book-to-engine crosswalk, backlog, and re-audit handoff.
2. Add `docs/continuous-improvement/business-system-and-learning-loop-2026-09.md` as the central, independently authored vocabulary for PDSA, system trade-offs, replication, learning transfer, and agent orchestration.
3. Add `docs/source-registers/skills-engine-currentness-2026-09.json` with verified primary sources for WCAG, DNS/BIND, DNSSEC, OWASP ASVS, IFRS, and AI risk guidance.
4. Correct the Digital Research directory in `scripts/validate_engine_control_plane.py` and restore the Windows Admin checkout; keep live/lab evidence gaps claim-specific.

## Wave 1 — domain reference upgrades

Add one concise, directly linked reference in each of the 11 engines:

- SRS: `09-governance-compliance/31-kaizen-engine-and-product-improvement/references/book-driven-improvement-and-adoption.md`.
- Business: `skills/meta-strategy/references/book-driven-commercial-system-and-validation.md`.
- Business: `skills/meta-strategy/references/marketing-plan-handbook-operating-loop.md` (recovered PDF study; customer-first planning, segmentation, strategy/program alignment, forecasting, budgeting, metrics, control, and audit).
- Website: `skills/brand/brand-strategy/references/book-driven-positioning-story-and-proof.md`.
- Social: `skills/meta-utility/references/book-driven-campaign-learning-and-retention.md`.
- Linux: `03-networking-and-dns/linux-dns-server/references/current-dns-operations-and-source-gate.md`.
- Proposal: `skills/meta/references/book-driven-value-story-and-evaluator-journey.md`.
- Accounting: `doctrine/references/book-driven-value-cash-and-working-capital.md`.
- Design: `doctrine/references/book-driven-brand-story-and-visual-evidence.md`.
- Digital Research: `skills/source-evaluation/references/book-driven-source-admission-and-currentness.md`.
- Engineering: `skills/sdlc-meta/references/book-driven-system-decision-and-agent-orchestration.md`.
- Windows Admin: `docs/research/book-driven-kaizen-operating-system.md`.

Each reference must be a concise synthesis, include source limitations, distinguish durable principles from volatile claims, and provide an operational checklist rather than copied book prose. The recovered Marketing Plan Handbook PDF was reviewed through temporary OCR; raw OCR remains outside all repositories.

## Wave 2 — owning-skill links and narrow workflow changes

Update only the owning Kaizen/meta/domain skills identified in the crosswalk. Add currentness checks to volatile technical, financial, standards, and policy routes. Add routing fixtures only when a changed description or new route could collide.

## Wave 3 — verification and re-audit

Run the Digital Research source-currency validator, each engine's native contract validator and routing smoke test, the central control-plane validator, source-ingestion guardrails, skill safety audits, and relevant repository tests. Record positive, negative, and unavailable evidence. Re-score the affected dimensions and schedule the next review. Include the Business Marketing Plan Handbook contract test in the evidence bundle.

## Stop and rollback

Stop if a source cannot be verified, a new route steals traffic from an existing owner, a validator finds structural debt, a reference becomes a raw-text surrogate, or a domain change weakens safety. Revert the affected reference/link change and retain the gap in the Kaizen record.
