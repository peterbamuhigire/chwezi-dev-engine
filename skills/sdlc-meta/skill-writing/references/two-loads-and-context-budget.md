# Two Loads and Context Budget

Treat skill use as two separate loads.

1. Discovery load: name and description compete for routing attention before selection.
2. Execution load: the selected body and branch-specific references compete for reasoning attention.

## Budget rules

- Discovery text contains the user goal, strongest trigger, and nearest boundary. It does not contain
  the procedure, examples, or praise.
- The entrypoint contains decisions shared by most executions: inputs, ordered workflow, permissions,
  failure handling, evidence, and routing pointers.
- Deep detail loads only after a real branch condition is observed.
- Repeated policy has one canonical owner and short pointers elsewhere.
- Measure the assembled runtime catalogue; repository-local counts do not prove host safety.

## Failure tests

Reject a skill when its description tries to teach the workflow, its body requires every reference,
or a reference repeats the parent without changing a decision. Compare the positive route with a
near neighbour and record both ranking and loaded-character cost.

Derived from the two-load attention model studied in Matt Pocock's `mattpocock/skills` repository
at commit `3cca18b`; adapted to the Chwezi runtime-budget gate.
