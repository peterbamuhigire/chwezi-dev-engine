# Twelve-Engine Control Plane

The twelve local engines remain separate sources of truth. This control plane
provides the shared operating vocabulary for agents, commands, hooks, evidence,
handoffs, and bounded recovery. Its registry is
[`engine-control-plane.json`](engine-control-plane.json).

## Ownership

| Concern | Owner |
|---|---|
| Domain doctrine and specialist output | The routed domain engine |
| Agent topology and handoff protocol | `skills-web-dev` control plane |
| Source/currentness verification | `digital-research-skills` |
| Finance/accounting controls | `chwezi-accounting-doctrine` |
| Visual/presentation controls | `design-system-skills` |
| Windows host, domain, fleet, and hybrid administration | `windows-admin-engine-skills` |
| Political doctrine and political writing | `D:\political-skills` |
| Tool adapters and native hooks | Host adapter or CI; never duplicated in domain doctrine |

## Portfolio Kaizen currentness gate

Every Kaizen operation across all twelve engines—engine audits, skill or
reference edits, validator changes, routing changes, and standardisation
decisions—must begin with the Digital Research Engine's source-evaluation and
source-verification workflow. The canonical contract is
[`kaizen-currentness-gate.md`](../../digital-research-skills/docs/continuous-improvement/kaizen-currentness-gate.md).
Current standards, policies, laws, technologies, versions, commands, security
controls, benchmarks, and lifecycle claims require dated, scoped, reviewable
primary-source evidence. Missing or ambiguous evidence is `NOT_ASSESSED` and
blocks standardisation.

## Windows administration engine status

`windows-admin` is a first-class registry engine covering Windows workstations and
servers, Active Directory, identity/security, networking, storage, recovery, fleet,
and hybrid administration. Its canonical local checkout is
`C:\wamp64\www\windows-admin-engine-skills`; the registry contract is present, but
the checkout, `AGENTS.md`, and `docs/control-plane-adoption.md` are now present.
Its native catalogue, routing, source-ingestion, and control-plane checks pass;
live Windows/domain/fleet lab evidence remains claim-specific and must be marked
`NOT ASSESSED` when unavailable. Do not fabricate Windows procedures from Linux
or generic engineering guidance.

See [Windows administration engine status](engine-status/windows-admin-engine.md).

## Hook implementation policy

The registry describes the contract, not a claim that every host supports
native hooks. Implement each event using the strongest available adapter:

1. native lifecycle hook;
2. repository script or pre-commit check;
3. CI release gate;
4. explicit skill step with a recorded result.

Safety, evidence, destructive-action, and release hooks must fail closed or
return `NOT ASSESSED`. Advisory context and cost telemetry may fail open.

## Standard agent topology

`Router/Planner → Domain Worker → Evidence Collector → Adversarial Reviewer →
Gatekeeper/Release Captain`.

Use parallel workers only for independent evidence streams. One coordinator
owns the final synthesis and gate. The `Skill Librarian` may propose durable
improvements from repeated failures, but promotion requires a fixture, a
validation result, and an owner.

## Adoption matrix

Each engine registry entry identifies its domain agents, thin command surfaces,
minimum hooks, evidence types, and adoption document. The registry validator
checks all twelve engines and, when run with `--workspace-root C:\wamp64\www`,
verifies their routers and adoption documents are present:

```powershell
python scripts/validate_engine_control_plane.py --workspace-root C:\wamp64\www
```

This is intentionally a small control plane. It prevents duplicated persona
catalogues while making missing controls visible and testable.

## Human approval enforcement

Side-effecting tools must also use the versioned policy and executable gate in
[`approval-contract.md`](approval-contract.md), [`approval-policy.json`](approval-policy.json),
and [`../tools/approval_control_plane.py`](../tools/approval_control_plane.py).
Each domain adapter is validated by `scripts/validate_approval_adapters.py`.
The registry and skill text alone do not claim runtime enforcement: every host
path must route through the gate and pass the no-approval, stale-approval,
scope-change, self-approval, audit, kill-switch, idempotency, and verification
tests before it is marked enforced.
