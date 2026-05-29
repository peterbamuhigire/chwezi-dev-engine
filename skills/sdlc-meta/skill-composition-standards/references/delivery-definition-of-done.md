# Delivery Definition of Done - the handoff gate

The single closing artifact for any meaningful piece of work. It exists to make
one thing true: **a team that did not write this change can run it, watch it,
recover it, and maintain it without asking the author.** That is the difference
between agent output that impresses in a demo and output a team can actually own.

This is a gate, not a suggestion. Produced at the end of meaningful work by the
orchestrating skill (typically `world-class-engineering`). Each line either
points at a concrete artifact (using the standard template) or is explicitly
marked N/A with a one-line reason. "Probably fine" is not an allowed value.

## When it applies

| Change class | DoD pack required? | Why |
|---|---|---|
| Feature, endpoint, schema change, infra change | Yes, full pack | Has runtime behaviour a team must operate |
| Bug fix with behaviour change or migration | Yes, full pack | Can fail in production; needs rollback path |
| Library/dependency upgrade | Yes, minus user-facing items | Operational risk without UI surface |
| Typo, comment, log-only, dead-code removal | No | No runtime behaviour changes |

Skipping the pack on a change that has runtime behaviour is the core
anti-pattern. The failure mode is silent: the work merges, looks complete, and
the gap only surfaces at 2 a.m. when on-call has no runbook.

## The pack

Each item names the artifact, its template, and the failure mode if it is
absent. Link the real artifact; do not restate it inline.

| # | Item | Template | Failure mode if missing |
|---|---|---|---|
| 1 | Problem frame + success criteria | (inline, one paragraph) | Work is judged on code, not on whether it solved the problem |
| 2 | Tests + evidence bundle | `test-plan-template.md` | "Tests pass" asserted, never shown; regressions ship |
| 3 | Release plan | `release-plan-template.md` | Deployer advances on instinct; no go-criteria |
| 4 | Rollback plan | `rollback-plan-template.md` | Recovery is improvised during the incident, when it is too late |
| 5 | Runbook + ownership | `runbook-template.md` | On-call has no procedure; every alert escalates to the author |
| 6 | Observability hooks | `slo-template.md` | Failure is reported by customers, not dashboards |
| 7 | Maintenance notes | (inline, see below) | The next change re-derives context the author already had |
| 8 | Security/data review (if boundary touched) | `threat-model-template.md` | A new trust boundary ships unmodelled |

### Maintenance notes (item 7) - the inline minimum

The one item with no separate template, because it is short and specific to the
change. It must answer, in a few lines each:

- **What this change assumes** that a future editor would not guess (invariants,
  ordering, idempotency keys, why a "boring" choice was made over a clever one).
- **What will break it** - the inputs, scale, or config that this design does not
  cover and would need rework.
- **Where to look first** when it misbehaves - the log line, metric, or table.
- **What is deliberately not done** - deferred work, known limits, and why they
  were acceptable to defer.

## Evidence standard

The pack is only as good as its evidence. Each claim is backed by an observation,
not an assertion.

| Claim | Acceptable evidence | Not acceptable |
|---|---|---|
| "Tests pass" | the command run + its output/summary | "I ran the tests" |
| "Rollback works" | rollback rehearsed in staging, or a reasoned step list with the exact revert command | "we can just revert" |
| "SLOs hold" | dashboard link or query + baseline numbers | "looks fine" |
| "Migration is safe" | applied on prod-size data in staging with timing | "it is additive" |

## Decision rule: how much pack for how much change

| Risk level | Stages 1-8 | Notes |
|---|---|---|
| Low (flag-gated, reversible, no data change) | 1, 2, 4, 7 minimum | Rollback can be "flip flag off" but must be written |
| Medium (schema-additive, new endpoint) | 1-7 | Full pack except threat model unless a boundary changed |
| High (destructive migration, auth/payment, new trust boundary) | 1-8, all | No stage may be skipped; item 8 mandatory |

Choosing a lighter pack than the risk level warrants is itself a finding. The
wrong direction to err is downward: a high-risk change with a low-risk pack is
how outages with no rollback path happen.

## How to use it

1. At the start of meaningful work, paste the pack table as a checklist.
2. As each artifact is produced, link it and tick the row.
3. Before claiming the work is complete, every row is either linked or N/A with a
   reason. Pair this with `verification-before-completion`: do not assert "done"
   until the pack is whole and the evidence is real.
4. The completed pack is the handoff. It travels with the PR, not in someone's
   head.

## Anti-patterns

- **Demo-complete, not done** - the feature works on the author's machine; there
  is no rollback plan, no runbook, no owner. It cannot be operated by anyone else.
- **Evidence by assertion** - "tests pass", "rollback is easy", "SLOs are fine"
  with nothing to point at. Replace every adjective with an observation.
- **Rollback written during the rollback** - the plan is drafted while the
  incident is live. Write it before the release, rehearse the risky ones.
- **Runbook that restates the code** - a runbook is for the operator who did not
  write the code: symptoms, first check, recovery action, escalation. Not a
  narration of the implementation.
- **Pack scaled to the author's confidence, not the change's risk** - a payment
  path shipped with a typo-grade pack.
- **N/A with no reason** - "N/A" is a claim that the item does not apply; it
  needs the same one-line justification as any other claim.

## Read next

- `release-plan-template.md`, `rollback-plan-template.md`, `runbook-template.md`,
  `test-plan-template.md`, `slo-template.md`, `threat-model-template.md` - the
  artifacts this pack links.
- `validation-contract` skill - produces the canonical Release Evidence Bundle
  that items 2 and 6 draw on.
- `verification-before-completion` skill - the discipline that stops "done" being
  claimed before the pack is whole.
