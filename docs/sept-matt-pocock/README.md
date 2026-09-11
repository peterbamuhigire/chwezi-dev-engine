# Matt Pocock Skills Comparison and Kaizen Handoff

Study date: 2026-09-11

## Outcome

This study compares the Chwezi engineering engine at `C:\wamp64\www\skills-web-dev` with
Matt Pocock's `skills` repository at `C:\Users\Peter\Downloads\skills-main\skills-main`.
The comparison source was verified byte-for-byte after line-ending normalisation against a fresh
clone of upstream commit `3cca18b368ae95cdbdebbff572ccafa662551015`.

The main conclusion is not to import the source repository wholesale. Chwezi already has stronger
domain breadth, evidence contracts, permission boundaries, currentness controls, and CI guardrails.
The source repository is better at a different layer: compact workflow ergonomics. Its strongest
ideas are invocation ownership, design-tree questioning, domain language as persistent context,
tracer-bullet work graphs, tight bug feedback loops, deep-module vocabulary, two-axis review, and
explicit skill lifecycle buckets.

Comparison-specific Chwezi baseline: **58/100 raw, 58/100 published**. The permanent-audit cap is
`min(raw, 65)`. This is not a replacement for the broader July portfolio score; it measures the
engine's readiness to provide the compact engineering workflow demonstrated by the source.

## Read order

1. [Executive summary](00-executive-summary.md)
2. [Method, evidence, and currentness](01-methodology-evidence-and-currentness.md)
3. [Source structure and mechanism](02-source-structure-and-mechanism.md)
4. [Skill-by-skill disposition](03-skill-disposition-register.md)
5. [New skills and references](04-new-skills-and-references.md)
6. [Existing-skill hardening](05-existing-skill-hardening.md)
7. [Cross-engine application](06-cross-engine-portfolio-map.md)
8. [Roadmap and acceptance gates](07-roadmap-and-acceptance.md)
9. [Risks, rejected imports, and evidence](08-risk-and-evidence-register.md)
10. [Execution runbook for the next Kaizen agent](09-kaizen-agent-runbook.md)
11. [Source inventory](10-source-inventory.md)

## Highest-value actions

| Priority | Action | Canonical owner |
| --- | --- | --- |
| P0 | Add a systematic bug-diagnosis skill centred on a tight, red-capable feedback loop | `skills-web-dev` |
| P0 | Add design-tree/frontier questioning to requirements and discovery workflows | SRS plus domain engines |
| P0 | Add context-pointer, completion-criterion, and invocation-governance references to skill authoring | `skills-web-dev` |
| P0 | Add domain-language and decision-record maintenance as an active architecture workflow | SRS plus `skills-web-dev` |
| P0 | Add tracer-bullet work graphs and expand-contract handling to execution planning | `skills-web-dev` |
| P0 | Finish the current evidence and portable-contract rollout before increasing the active count | `skills-web-dev` |
| P1 | Add deep-module/deepening and design-it-twice references | `skills-web-dev` plus design engine |
| P1 | Split code review into spec fidelity and engineering-standard axes | `skills-web-dev` |
| P1 | Adopt lifecycle buckets and promotion gates without duplicating the entire documentation tree | Coordination package |
| P1 | Adapt questionnaires, handoffs, prototypes, and manual-operation wizards by domain | Relevant engines |

## Non-negotiable constraint

The engineering catalogue currently has 179 active skills, nine above its soft target ceiling of
170. New active skills must be paid for by a proven consolidation or alias in the same Kaizen wave.
Most source ideas should first land as references or hardening inside existing owners.
