# Tracer-Bullet Work Graphs

A tracer bullet is the smallest independently demonstrable path through the layers required for one
user or operator outcome. It is not a horizontal task such as "build the database" with no usable
flow. Represent the plan as a directed acyclic graph so dependency and parallelism are explicit.

## Node contract

| Field | Required content |
| --- | --- |
| ID/outcome | User-visible or operator-visible behaviour |
| Failure consequence | Harm if the slice is incomplete or wrong |
| Inputs | Approved contracts and producer evidence |
| Layers | Minimal UI/API/domain/data/operations path needed |
| Owner/write set | One accountable owner and non-overlapping files |
| Blocking edges | Producer node IDs that must pass first |
| Acceptance | Normal, failure, security, and rollback oracles |
| Evidence | Commands, artefacts, render/system proof, or `NOT ASSESSED` |

The runnable frontier contains only incomplete nodes whose blocking edges are accepted. Starting a
blocked node is a planning defect. Recompute the frontier after every accepted, failed, or changed node.

## Expand-contract exception

Some live changes cannot be one end-to-end commit. Model them as linked nodes:

1. Expand: add backward-compatible schema or contract and dual-read/write observability.
2. Migrate: move bounded cohorts with reconciliation and restartable checkpoints.
3. Switch: change consumers or traffic only after compatibility evidence.
4. Contract: remove the old path after version skew and rollback windows close.

Each node keeps the declared green boundary. A calendar date does not close a compatibility window;
measured consumer state and rollback evidence do.

## Adapters

The graph is canonical Markdown/YAML. GitHub, GitLab, Jira, or another tracker is an optional adapter.
External issue creation or mutation requires explicit authority. When unavailable, preserve the graph
locally and mark tracker synchronisation `NOT ASSESSED`.

Start from `templates/work-graph.yml` at the repository root and validate it with:

```powershell
python -X utf8 scripts\validate_work_graph.py <graph.yml>
```

This reference adapts tracer-bullet, blocking-edge, frontier, and expand-contract mechanisms studied
in Matt Pocock's `mattpocock/skills` repository at commit `3cca18b`.
