---
name: ai-agent-compliance-controls
description: Use when mapping AI agent operations to SOC 2, ISO 27001, HIPAA, audit logs, control testing, attestations, and compliance evidence, including drill-cadence evidence, approval-completeness (PI1.1) gap checks, and signed agent-memory erasure proofs.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# AI Agent Compliance Controls

## Operating contract

## Inputs

| Input | Required | Purpose |
|---|---|---|
| Domain evidence | yes | system boundary, applicable frameworks, data classes, control owners, agent actions, and available evidence |

## Outputs

- Produce: control matrix, test procedures, exceptions, evidence index, and remediation owners.

## Capability and permission boundaries

Default to read-only analysis. Read only scoped records; redact secrets and regulated data. Writes, execution, network calls, production configuration, customer communication, billing changes, and delegation require explicit authority and an identified owner. Never widen tenant, time-window, or system scope implicitly.

## Degraded mode

When required telemetry, evidence, execution, network access, or write authority is unavailable, return a partial result with each unassessed item labelled, preserve the safest existing state, and state the evidence or approval needed to continue. Never convert missing evidence into a pass.

## Decision rules

| Condition | Action |
|---|---|
| Scope, owner, or threshold is missing | Stop the affected decision and request it |
| Evidence is incomplete but read-only analysis is safe | Produce a qualified partial result and gap list |
| A mutation exceeds authority or tenant boundary | Block it and route for approval |
| Evidence meets the stated threshold | Issue the output with provenance and owner |

## Anti-Patterns

- Treating absent evidence as success. Fix: mark the check unassessed and name the missing source.
- Expanding one tenant or workflow to all tenants. Fix: enforce supplied scope at every query and action.
- Performing a production write during analysis. Fix: emit a reviewed change plan until authority is explicit.
- Reporting a metric without population, window, or source. Fix: attach all three.
- Hiding a failed threshold inside an average. Fix: report failure slices and the remediation owner.

Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->

## Use When

- Design compliance controls for agent actions, logs, approvals, evidence, and access boundaries.
- Map agent operations to SOC 2, ISO 27001, HIPAA, or control testing requirements.
- Prepare control evidence and audit-ready narratives for agentic AI systems.
- Prove kill-switch, red-team, eval-drift, and restoration drills ran on cadence with signed pass/fail evidence (`references/ai-agent-drill-evidence-and-cadence/`).
- Prove every irreversible agent action had a prior, authorised, linked approval and emit the SOC 2 PI1.1 gap register (`references/ai-agent-approval-audit-completeness/`).
- Prove a data-subject erasure removed all agent memory tiers, vectors, replicas, and subprocessor copies, with a signed proof-of-erasure pack (`references/ai-agent-memory-erasure-proof/`).

## Do Not Use When

- The work is not AI-specific or agentic-AI-specific.
- A narrower retained AI parent skill fits the request better.

## Required Inputs

- Product, tenant, user, data, risk, and operational context relevant to the AI workflow.
- Target artifact: design, implementation plan, audit, test strategy, UX flow, commercial policy, or runbook.
- Constraints from security, privacy, reliability, billing, support, and compliance stakeholders when relevant.

## Workflow

1. Read this SKILL.md first.
2. Load [references/routing.md](references/routing.md) to select the absorbed child reference that matches the task.
3. Load only the selected child reference files needed for the current request.
4. Produce execution-oriented output with assumptions, risks, evidence, and next actions where relevant.

## Quality Standards

- Keep routing explicit: name which reference files were used when the work depends on absorbed material.
- Preserve tenant isolation, auditability, cost controls, safety gates, and operational evidence when they matter.
- Prefer concrete contracts, checklists, tables, schemas, runbooks, and decision records over broad summaries.

## Anti-Patterns

- Loading every absorbed reference by default.
- Treating AI-specific billing, compliance, safety, or UX concerns as generic SaaS work without checking AI failure modes.
- Hiding retired skill names; old slugs must remain discoverable through [references/routing.md](references/routing.md).

## Outputs

- A concrete deliverable matched to the request: architecture, implementation plan, audit, policy, runbook, UX flow, test strategy, or operating model.
- The selected consolidated reference files and any assumptions, risks, evidence requirements, or follow-up actions that affect execution.
## References

- [references/routing.md](references/routing.md) maps retired child skill slugs to their consolidated reference folders.
- Load [references/eu-ai-act-and-iso-42001-agent-overlay.md](references/eu-ai-act-and-iso-42001-agent-overlay.md) when a feature may be EU AI Act high-risk or a customer asks for ISO/IEC 42001 alignment: classification, Arts. 9-15/19/72/73 mapped to existing controls, application dates.
- Load [references/ai-agent-drill-evidence-and-cadence/entrypoint.md](references/ai-agent-drill-evidence-and-cadence/entrypoint.md) when turning drills into audit evidence: drill registry, minimum cadence, overdue paging, signed drill packs. Drill scenario design stays in `ai-agent-safety-and-red-team` and `ai-incident-response`.
- Load [references/ai-agent-approval-audit-completeness/entrypoint.md](references/ai-agent-approval-audit-completeness/entrypoint.md) when an auditor asks for proof that irreversible actions were approved before execution: gap-detection job, backfill detection, PI1.1 pack.
- Load [references/ai-agent-memory-erasure-proof/entrypoint.md](references/ai-agent-memory-erasure-proof/entrypoint.md) when an erasure request touches agent-derived memory: cascade verification job, residue probes, signed proof pack.
- Load [references/continuous-control-monitoring.md](references/continuous-control-monitoring.md) when proving controls stayed effective across an audit window: declared-vs-observed drift checks, compliance deploy gate, framework edition register, LLM provider re-verification.

## Consolidated Child References

- Load [references/routing.md](references/routing.md) to map retired AI child skill slugs to their reference modules.
## Evidence Produced

| Category | Artifact | Format | Example |
| --- | --- | --- | --- |
| Security | Agent control-to-evidence matrix | Markdown/YAML | control owner, test procedure, result, exception, and review date |

<!-- dual-compat-end -->
