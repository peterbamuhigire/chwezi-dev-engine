---
name: skill-engine-audit
description: Use when auditing, grading, benchmarking, or conforming an entire skills engine. Measures taxonomy, doctrine, contracts, depth, routing, safety, references, output readiness, and normalisation priorities.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Skill Engine Audit
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com.

<!-- dual-compat-start -->
## Use When

- Asked to AUDIT, grade, benchmark, rank, or find gaps in a whole skills engine / skill catalog
  (not a single skill — for one skill's safety use `skill-safety-audit`).
- Deciding whether an engine is "world-class" and what to add/harden to get there.
- Producing a comprehensive, ranked, evidence-based report on an engine's quality and coverage.

## Do Not Use When

- Auditing ONE skill for unsafe/malicious instructions → use `skill-safety-audit`.
- Auditing produced artifacts (a website/app/document) for AI slop → use the design engine's
  `ai-slop-typography-audit` / `visual-product-slop-audit`.
- Writing or routing a new skill → use `skill-writing` / `skill-taxonomy-and-routing`.

## Required Inputs

- The engine's path(s) and what it is FOR (its domain and the OUTPUT TYPES it must produce —
  e.g. websites, iOS/Android/web apps, cross-platform apps, documents, proposals, presentations,
  brand systems, data products). The output-type list drives the readiness audit.
- The BAR to grade against (default: world-class / top 0.1% of the relevant domain).

## Workflow

0. **Inventory compliance first.** For conformance work, run `scripts/engine_compliance.py`
   before reading individual skill bodies. Use its compact exception register to minimise context loading.
   Also run the repository's source-ingestion guardrail and block the audit on
   raw ebooks, large book-extraction files, or likely reconstructive full text.
1. **Scope it.** Read the engine's router(s) (`README.md` / `CLAUDE.md` / `AGENTS.md`) and its
   doctrine. Glob `skills/**/SKILL.md` to list every group and skill. Identify the output types
   the engine is responsible for (audit ALL of them — web, iOS, Android, web apps, cross-platform,
   websites, documents, presentations, brand, data products, handoff — whichever apply).
2. **Lock the rubric.** Use `references/scoring-rubric.md`. The bar is the top 0.1% of the domain.
   **Default scores 45–65; any 70+ needs extraordinary, specific justification. If tempted to
   score 70+, you were not strict enough — find what is missing.** Every score is justified with
   concrete deficiencies, never vibes.
3. **Fan out parallel audit agents** (see `references/parallel-agent-method.md`) — one per concern,
   so strict scores emerge independently before synthesis. Standard fleet:
   (a) **standards benchmark** — what world-class looks like NOW for this domain, cited via a
   research engine under a no-hallucination rule; (b) **existing-skills audit** — read every
   SKILL.md, score each skill + group; (c) **taxonomy & gap analysis** — is the structure
   sufficient/exhaustive/balanced, what's missing; (d) **per-output-type readiness** — score each
   output type the engine must produce; (e) **hardening plan** — concrete `references/*` +
   `examples/*` to add; (f) **reading/source list** — material to buy and extract, cited.
4. **Rank every aspect** using the dimension list in `references/audit-dimensions.md` (taxonomy,
   doctrine, skill depth, worked examples, standards currency, output coverage, accessibility,
   production/handoff, redundancy/hygiene, discovery/routing, safety). Each /100.
5. **Synthesize** the connective verdict: executive summary, methodology, master scorecard
   (every dimension + group + output type + the overall engine score /100), and a phased roadmap.
6. **Write the report** as a multi-file set under `docs/initial-analysis/` (or a named audit
   folder) following `references/report-structure.md`. One concern per file; a README index.
7. **Make it actionable** — the roadmap must list specific new skills (with priority P0/P1/P2),
   hardening moves (named files), and the target score after each phase.

## Quality Standards

- Strict and evidence-based: every score cites concrete, named deficiencies.
- Comprehensive: ALL output types the engine touches are scored, none skipped.
- Cited where external: standards/benchmarks/reading verified under a no-hallucination rule.
- Actionable: ends with a prioritized roadmap and a believable target score per phase.
- Reproducible: the rubric and dimensions are fixed references, so re-audits are comparable.
- Rights-aware: source provenance is recorded, raw books are absent, and
  book-informed skills contain independent operational synthesis rather than a
  substitute for the source.

## Anti-Patterns

- Grading on vibes, or inflating scores (70+ without extraordinary justification).
- Auditing only the skills that exist while ignoring what's MISSING (coverage gaps).
- Skipping output types ("we only checked web") — audit every aspect the engine is for.
- A single monolithic opinion instead of independent parallel concerns + synthesis.
- A report with scores but no roadmap, or a roadmap with no target numbers.
- Treating committed book/OCR dumps as harmless research evidence.

## Outputs

- A `docs/<audit>/` folder: executive summary, methodology+rubric, per-group audit, taxonomy &
  gap analysis, per-output-type readiness, standards benchmark, hardening plan, reading list,
  master scorecard (overall engine /100), and a phased roadmap to the bar.

## References

- `references/compliance-normalisation-workflow.md` - reusable, token-efficient conformance process.
- `scripts/engine_compliance.py` - read-only inventory by default; narrowly scoped safe fixes with `--fix-safe`.
- `references/scoring-rubric.md` — the strict bar and bands.
- `references/audit-dimensions.md` — every aspect to rank + the output-type checklist.
- `references/parallel-agent-method.md` — the audit-agent fleet and how to brief it.
- `references/report-structure.md` — the multi-file report template.
- Sibling skills: `skill-safety-audit`, `skill-writing`, `skill-taxonomy-and-routing`,
  `ai-slop-audit`.
## Inputs

| Artefact | Required? | Purpose |
|---|---|---|
| Engine router and policies | yes | Establish scope and local rules |
| Active skill roots | yes | Define the audited catalogue |
| Compliance bar | yes | Keep re-audits comparable |

## Evidence Produced

| Category | Artifact | Format | Example |
|---|---|---|---|
| Release evidence | Engine compliance report | Scanner summary or JSON exception register with before/after counts | `engine-compliance.json` |
| Correctness | Normalisation evidence pack | Validator, routing, safety, diff, and remaining-exception results | `docs/audits/<engine>/evidence.md` |

<!-- dual-compat-end -->

## Capability contract

Read and search are required. Execution is optional but preferred for scanners and validators. Editing requires an explicit conformance request; network research is separate and source-disciplined.

## Decision rules

| Condition | Action | Failure avoided |
|---|---|---|
| Structural question spans the catalogue | Run machine inventory first | Token-heavy manual reading |
| Safe syntax defect has deterministic repair | Use `--fix-safe`, then inspect diff | Repetitive manual edits |
| Contract or domain judgement is missing | Normalise individually | Fabricated boilerplate compliance |
