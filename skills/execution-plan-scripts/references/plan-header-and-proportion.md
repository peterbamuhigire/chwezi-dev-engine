# Plan Header and Proportion

Load when writing or reviewing the plan that execution prompts will be cut from. The header makes a
plan self-contained for a worker that has never seen the conversation; the proportion check stops a
plan from becoming a second copy of the code.

## Plan header (top of the plan, before any node)

| Field | Content | Rule |
|---|---|---|
| Spec pointer | Path and heading (or requirement IDs) of the approved spec this plan implements | One pointer. If there is no approved spec, stop: the plan is premature |
| Global constraints | The constraints every node must respect: stack versions, forbidden libraries, tenancy rule, money and audit rules, no-push rule, language standard | Copy them verbatim from the spec or project rules. Do not paraphrase; a paraphrase drifts |
| Ceremony class | spike, bounded or architectural (see `world-class-engineering` §2) | The class only goes up during the plan |
| Out of scope | What this plan will not touch | Stops a worker widening the change |

## Per-node interfaces

Each work-graph node (IDs as in [tracer-bullet-work-graphs.md](tracer-bullet-work-graphs.md)) states
what crosses its boundary:

- **Consumes:** the contracts, tables, endpoints or files the node reads, and which producer node
  supplies each one.
- **Produces:** the contracts, tables, endpoints or files the node creates or changes, named exactly
  (class, route, column, event name).

A node that consumes something no earlier node produces, and that does not exist yet, is a planning
defect. Fix the graph before cutting prompts. These fields live inside the node's existing
`acceptance` and `evidence` text, so `scripts/validate_work_graph.py` needs no schema change.

## Review focus

Add a short **Review focus** list to the header: at most five classes of input the spec does not
state but the code will meet. Examples for a PHP/MySQL ERP:

| Unstated input class | Pinned to test in node |
|---|---|
| Zero-quantity or negative-quantity lines | `N3` `test_rejects_zero_quantity_line` |
| A posting dated inside a locked period | `N4` `test_period_lock_rejects_post` |
| The same webhook delivered twice | `N5` `test_duplicate_webhook_is_idempotent` |
| A user from tenant A passing tenant B's ID | `N2` `test_cross_tenant_id_is_rejected` |
| Multi-byte text in names and narrations | `N3` `test_utf8mb4_round_trip` |

Each row names the owning node and one test. A class with no owning test is not "covered"; it is an
open risk and goes in the node's acceptance.

## One reasonable thing per step

Each step inside a node does one thing a reviewer can check on its own: add the migration, add the
repository method, wire the route, add the test. A step that says "implement the feature" is not a
step. A step that needs the word "and" twice is probably two steps.

## Proportion check

Run before handing the plan to workers:

1. **Length against spec.** A plan several times longer than its spec usually restates code or
   invents requirements. Trim it or send the new requirements back to the spec owner.
2. **No restated code.** The plan names classes, routes, columns and tests; it does not contain
   method bodies, full SQL or full components. Short signatures and contract shapes are fine.
3. **Every spec requirement lands in a node.** List the spec's requirement IDs and the node that
   owns each. An unowned requirement is a gap; a node with no requirement is scope creep unless it
   is enabling work (migration, fixture, seam).
4. **Evidence per node.** Each node's evidence names a command or artefact, or says
   `NOT ASSESSED` with the reason.

Record the result as one line in the plan header, for example
`Proportion: spec 3 pages, plan 4 pages; 14/14 requirements owned; no restated code.`

(Plan-header fields and proportion check adapted from obra/superpowers, MIT,
https://github.com/obra/superpowers, commit 8ca22dba9a94f28898bbce59f2537ff4d87c747d. Paraphrased;
no text copied.)
