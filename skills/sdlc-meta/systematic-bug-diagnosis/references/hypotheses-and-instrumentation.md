# Hypotheses and Instrumentation

Write each hypothesis as: `If cause C is active, observation O should differ from counterfactual N
under controlled test T.` Rank by existing evidence, discriminatory power, risk, and experiment cost.

| Hypothesis | Supporting evidence | Contradiction | Discriminating check | Reject when |
| --- | --- | --- | --- | --- |
| Example: cache key omits tenant | collisions follow shared IDs | single-tenant run is clean | log hashed tenant/key pair at lookup | failing pair uses distinct complete keys |

Instrumentation must have an owner, purpose, fields, sensitivity classification, scope, sample rate,
retention, correlation tag, enable/disable mechanism, and removal date. Prefer counters and structured
events over unrestricted payload logs. Never capture secrets or full personal data merely because a
bug is difficult.

Record negative experiments. A falsified attractive hypothesis is valuable evidence and prevents the
next agent from repeating the same work.
