# Book-Informed AI Collaboration and Execution

This reference is a self-contained operational synthesis prepared from Alexio
Cassani, *Code Revealed* (2025), and Stephanie Diamond, *Claude For Dummies*.
It turns their practical guidance into a model-neutral delivery loop; current
vendor features and performance claims still require independent verification.

## Select the interaction mode

| Mode | Suitable work | Control boundary |
|---|---|---|
| Exploration | Low-risk prototypes, option discovery, disposable drafts | Sandbox, no production credentials, throwaway branch or workspace |
| Assisted development | Bounded implementation, refactoring, tests, documentation | Human-owned plan, reviewable diff, tests and security checks |
| Agent-supervised development | Multi-step work with tools or delegation | Explicit plan, tool allow-list, checkpoints, logs, approval and rollback |

Escalate control as consequence, data sensitivity, autonomy, and reversibility
decrease. Never infer permission from a successful draft.

## Execution record

Before acting, record the goal, context, constraints, allowed files/tools,
success measure, stop condition, reviewer, and rollback. During work, retain
the plan, material decisions, tool results, failed attempts, and changed
artefacts. At handoff, report what was verified, what remains uncertain, and
what the next agent must not assume.

## Prompt and context loop

1. Name the audience, task, input, desired output, constraints, and examples.
2. Start with one coherent objective; split overloaded requests into stages.
3. Ask for assumptions, trade-offs, sources, and uncertainty where they matter.
4. Inspect the result against the acceptance criteria before revising the prompt.
5. Save only successful, tested patterns in a versioned library with an owner.

## Trust ramp

Begin with reversible, low-risk work. Verify results, measure quality and cost,
then expand scope only when the fallback remains available. Preserve human
ownership of architecture, security, data rights, consequential decisions, and
release approval.
