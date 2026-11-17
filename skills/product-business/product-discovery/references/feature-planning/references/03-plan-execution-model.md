## 🔄 The Plan Execution Model

### Phase 1: Plan Creation

```
USER REQUEST
    ↓
ANALYZE: "What needs to be done?"
    ↓
DECOMPOSE: Break into executable steps
    ↓
IDENTIFY DEPENDENCIES: Which steps need which outputs?
    ↓
CREATE DAG: Map the dependency graph
    ↓
PLAN OBJECT: { steps: [...], dependencies: {...} }
```

### Phase 2: Plan Execution

For a blocked dependency, keep verified sibling outputs with their revision and acceptance evidence. On resume, check whether changed inputs invalidate any of them and rerun the affected checks. Record the missing artifact, who can supply it and the next recovery action. A handoff is ready when the consumer can use its verified input.

```
PLAN OBJECT
    ↓
TOPOLOGICAL SORT: Order steps respecting dependencies
    ↓
SCHEDULE: Identify which steps can run in parallel
    ↓
EXECUTE: Run steps (sequentially or in parallel)
    ↓
VALIDATE: Check each step's output
    ↓
HANDLE ERRORS: If validation fails, decide what to do
    ↓
AGGREGATE RESULTS: Combine all step outputs
    ↓
RETURN FINAL RESULT
```
