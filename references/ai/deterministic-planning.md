# Bounded deterministic planning

`tools.ai.deterministic_planning.DeterministicPlanner` implements a pure,
bounded A* search over string nodes. Callers provide start, goal predicate,
neighbour function, non-negative edge cost, optional heuristic and an expansion
budget. The result reports a legal path, cost, expanded node count, or one of
`rejected`, `no_plan`, and `budget_exhausted` with a reason.

Neighbour ordering and queue tie-breaking are deterministic. Negative,
non-finite or malformed costs/edges are rejected. The planner never invokes an
action executor; a separate approval-gated runtime must consume any returned
plan before a side effect.

The utility is a local fixture/planning primitive. Optimality beyond the
provided finite graph, performance under production workloads and integration
with a live executor are `NOT_ASSESSED`.
