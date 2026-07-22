# Universal Agent and Skill Authoring Upgrade

Date: 2026-07-12

The `skill-writing` route now distinguishes agents, skills, tools, workflows, project instructions, and vendor adapters. It defines a five-part reusable instruction contract, capability-based canonical wording, minimum-permission defaults, thin-adapter rules, multi-agent reconciliation requirements, and routing/contract tests.

The new `references/universal-agent-skill-architecture.md` provides the detailed source-of-truth and compatibility-layer pattern. Two routing fixtures cover cross-runner instruction libraries and specialist-role conversion.

## Engine conformance follow-up

- Corrected repository-root resolution in skill validators and maintenance scripts.
- Replaced machine-specific external-engine paths with logical external target prefixes resolved by Codex or Claude instructions on each device.
- Added `skill-engine-audit/scripts/engine_compliance.py`, a read-only-first cross-engine scanner with compact JSON output and narrowly scoped `--fix-safe` repairs.
- Added a reusable cross-engine normalisation workflow and cohort strategy.
- Normalised the governing meta-skills with capability, degraded-mode, decision, input/output, and anti-pattern contracts.
- Removed exact repeated compatibility boilerplate across the active catalogue and repaired detected mojibake without replacing domain bodies.
- Hardened `upgrade_dual_compat.py` so it never replaces an existing marked block wholesale.

## First domain cohort

The first judgement-heavy normalisation cohort completed all six security skills, all three local finance/accounting wrappers, and six high-risk AI-control skills: runtime architecture, safety/red-team, tool/HITL gating, governance limits, multi-agent coordination, and AI security. Each now declares domain inputs, capability limits, degraded behaviour, decision rules, and concrete anti-patterns. Engine-wide full compliance increased from 9 to 24 skills.
