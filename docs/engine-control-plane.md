# Ten-Engine Control Plane

The ten local engines remain separate sources of truth. This control plane
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
| Tool adapters and native hooks | Host adapter or CI; never duplicated in domain doctrine |

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
checks all ten engines and, when run with `--workspace-root C:\wamp64\www`,
verifies their routers and adoption documents are present:

```powershell
python scripts/validate_engine_control_plane.py --workspace-root C:\wamp64\www
```

This is intentionally a small control plane. It prevents duplicated persona
catalogues while making missing controls visible and testable.
