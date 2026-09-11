# Kaizen Agent Runbook

This file is the execution handoff. A fresh agent should be able to start the improvement operation
without reconstructing this study.

## Objective

Improve the Chwezi skills portfolio using the selected workflow mechanisms from Matt Pocock's
`skills` repository, while preserving canonical domain ownership, currentness, safety, runtime
budgets, and evidence gates.

## Start here

1. Read the active engine's router and local `AGENTS.md`.
2. Read `docs/sept-matt-pocock/README.md` and files `00` through `08` in order.
3. Read the Digital Research source-evaluation, source-verification, and Kaizen currentness gate.
4. Read `skills/sdlc-meta/anti-ai-slop`, `ai-slop-audit`, `kaizen-improvement-system`,
   `skill-engine-audit`, `skill-writing`, `skill-composition-standards`, and `skill-safety-audit`.
5. Load the portfolio craft standard.
6. Check the Codex model policy and record official/current runtime evidence; do not silently change
   model pins.
7. Inspect Git status in every target engine and preserve unrelated changes.

## Source identity

Use the local comparison source at:

`C:\Users\Peter\Downloads\skills-main\skills-main`

It matches upstream commit `3cca18b368ae95cdbdebbff572ccafa662551015` after line-ending
normalisation. If the work begins after 2026-10-11, refresh and re-diff upstream before relying on
this report.

## Work graph

| ID | Slice | Blocked by | Owner | Output |
| --- | --- | --- | --- | --- |
| K0 | Re-run baseline and currentness | None | Orchestrator | Evidence register |
| K1 | Select two safe catalogue consolidations | K0 | Skill librarian | Alias/consolidation decision |
| K2 | Add skill-attention references and tests | K0 | Skill authoring owner | References, validator changes, fixtures |
| K3 | Add systematic diagnosis skill | K1, K2 | SDLC owner | Skill, references, template, hidden tests |
| K4 | Repair portable-contract exceptions | K0 | Domain owners | 26 judgement-based repairs |
| K5 | Complete evidence declarations | K0 | Domain owners | 66 evidence sections and negative tests |
| K6 | Add frontier questioning to SRS | K2 | SRS owner | Canonical reference and fixtures |
| K7 | Add engineering/domain wrappers | K6 | Relevant engine owners | Minimal pointers and domain outputs |
| K8 | Add tracer-bullet work graph | K2 | Execution-planning owner | References, templates, tracker adapters |
| K9 | Add two-axis review | K2, K8 | Engineering review owner | Review reference and planted-defect tests |
| K10 | Pilot deepening and prototypes | K3, K6, K8 | Architecture/design owners | Applied before/after evidence |
| K11 | Add lifecycle/invocation validators | K2 | Coordination owner | Cross-runtime checks |
| K12 | Portfolio re-audit | K3-K11 | Astra reviewer | Raw score, capped score, blockers, next cycle |

Run K4 and K5 in parallel by disjoint skill families when compliant Luna workers are available.
Do not delegate architecture, ownership, scoring synthesis, or final acceptance.

## Slice contract

For every K item record:

| Field | Required content |
| --- | --- |
| Outcome | User or maintainer capability that changes |
| Failure consequence | What goes wrong if the slice is shallow or incorrect |
| Existing context | Exact files, routes, fixtures, and data inspected |
| Smallest change | One skill/reference/validator/fixture cohort |
| Normal check | Representative intended task |
| Hard check | Failure, denied, unavailable, collision, stale-source, or rollback case |
| Evidence | Command, result, diff, render, source, or `NOT ASSESSED` |
| Owner/reviewer | Named role; worker self-review is not independent |
| Rollback | Alias, revert, disabled gate, or previous reference path |
| Re-audit | Date and measurement |

## Decision rules

- If an existing skill can own the mechanism without an ambiguous trigger, harden it instead of
  adding a skill.
- If a new active skill is justified, consolidate or alias an equal number in the same wave until
  the catalogue is at or below 170.
- If a source mechanism requires external mutation, split advisory design from execution and obtain
  action-specific authority.
- If a claim depends on a current standard, package, CLI, model, provider, platform, law, or
  benchmark, verify it through Digital Research before editing doctrine.
- If a runtime cannot enforce explicit/implicit invocation, leave the semantic policy documented
  and mark runtime enforcement `NOT ASSESSED`.
- If a validator encourages generic boilerplate, stop and add a semantic negative fixture before
  further rollout.
- If visual output is involved, load the design engine and state the purpose-fit visual decisions
  before production.
- If finance, tax, ledger, pricing recognition, or statutory behaviour appears, load Chwezi
  accounting doctrine in addition to the domain engine.

## Required commands

At minimum, after each Chwezi engineering cohort:

```powershell
python -X utf8 scripts\skill_catalog_guardrails.py
python -X utf8 scripts\routing_smoke_test.py
python -X utf8 skills\sdlc-meta\skill-writing\scripts\contract_gate.py --all --strict
python -X utf8 -m pytest tests -q -p no:cacheprovider
python scripts\validate_engine_control_plane.py --workspace-root C:\wamp64\www
```

Run the coordination package's runtime-budget validator against the exact roots and enabled plugin
cache exposed by the target host. Do not infer runtime safety from a repository-local pass.

## Mandatory fixtures

1. Explicit skill cannot auto-trigger or be transitively invoked.
2. Implicit skill auto-triggers on a positive case and stays silent on a neighbour case.
3. Frontier interview delays a dependent decision.
4. Fact lookup does not ask the human for discoverable repository information.
5. Missing stakeholder decision remains unresolved.
6. Diagnosis without a red-capable loop stops before causal claims.
7. Intermittent failure raises reproduction rate and records uncertainty.
8. Tautological test is rejected.
9. Work graph exposes parallel frontier and blocks dependent work.
10. Wide refactor uses expand-contract and keeps the declared green boundary.
11. Standards-pass/spec-fail and spec-pass/standards-fail are both detected.
12. Prototype variants differ structurally and are removed or rewritten before release.
13. Handoff lets a fresh agent resume without copied artefact bodies.
14. Experimental/deprecated skill is excluded from promoted runtime roots.
15. Stale source entry produces `NOT ASSESSED`, not a pass.

## Stop conditions

Stop the wave when:

- ownership between two engines is unresolved;
- a new skill increases runtime count without a consolidation decision;
- current source or normative text is unavailable for a material claim;
- a worker model/role cannot be guaranteed by the spawn interface;
- production, tracker, publication, credential, or destructive authority is missing;
- a security, privacy, financial, legal, data-loss, or accessibility blocker remains;
- a Grade F anti-slop verdict appears;
- a validator passes structure while the behavioural fixture still fails.

## Final handoff format

Return:

- before and after raw/capped scores;
- changed skills, references, validators, fixtures, aliases, and routers;
- exact test and runtime evidence;
- failed or rolled-back experiments;
- source/currentness register;
- active skill and metadata budgets;
- unresolved blockers and `NOT ASSESSED` items;
- independent reviewer verdict;
- rollback paths and next re-audit date.
