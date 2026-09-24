# Rollout Selection

Load this when choosing how a release reaches users, when writing the rollout
and rollback sections of a release plan, or when reviewing a plan that says
only "we will use blue-green". Traffic-shifting plumbing lives in
`cloud-architecture`; Kubernetes progressive delivery in `kubernetes-platform`.

## 1. Two layers: core strategy plus add-ons

Pick exactly one **core** strategy (how instances change version), then add any
number of **add-ons** (how exposure is limited). Plans that name only an add-on
("canary") without the core mechanism are incomplete.

### Core strategies

| Strategy | Mechanism | User experience | Stateless | Stateful (data on replica disk) | Extra capacity | Rollback speed |
|---|---|---|---|---|---|---|
| Downtime (maintenance window) | Stop all old, start all new | Outage | Yes | Yes | None | Slow (redeploy old) |
| Rolling, new-before-old | Start new replicas, pass health checks, then remove old | Mixed versions briefly | Yes | Poor fit | Some | Medium |
| Rolling, replace-in-place | Stop one old replica, start new on its volume, repeat | Mixed versions briefly | Yes | Yes (the usual choice for clustered data stores) | None to one node | Medium |
| Blue-green | Stand up full new set, switch all traffic at once | Clean cutover | Yes | Poor fit | Double during switch | Fast (switch back while blue lives) |

### Add-ons

| Add-on | What it limits | Precondition |
|---|---|---|
| Canary | Blast radius: one replica or small traffic slice compared against a control | Metrics that can distinguish canary from control within minutes; automatic abort threshold |
| Feature toggle | Separates deploy from release; enables per-cohort ramp and instant kill | Toggle service or config with audit log; removal discipline |
| Promotion (dev -> staging -> prod) | Catches defects before production with the same artifact | One immutable artifact; environment parity for the risky dimension |
| Dark launch | Exercises new code paths with real traffic, no visible output | Side-effect isolation (no duplicate payments, emails, SMS) |

## 2. Decision rules

| Condition | Choose |
|---|---|
| Stateless web/API, orchestrator supports it, capacity can double briefly | Blue-green core + canary add-on for high-risk changes |
| Stateless, capacity fixed (on-prem, single VPS pair, cost-constrained client) | Rolling new-before-old with max-surge 1 |
| Clustered data store or replica holds unique disk state | Rolling replace-in-place, one node at a time, with quorum checks between steps |
| Data migration that would need weeks of dual-write engineering to do online | A short announced downtime window is legitimate; state the window, the user notice, and the restore point |
| Infrastructure change (network, database creation, IAM) | Promotion through preproduction plus reviewed saved plan; no canary exists for "delete the database" |
| New user-visible behaviour in a product at scale | Feature toggle, ramp internal -> 1% -> 10% -> 50% -> 100% with a hold at each step |
| Mobile app release | Store staged rollout plus server-side toggle; binary rollback is not possible, so the toggle is the rollback |
| Regulated or financial logic (tax, interest, ledger postings) | Promotion with parallel-run comparison against the old version before any user exposure |

## 3. Rollback, roll-forward, or disable

Decide before release, per change, and write the answer into the release plan.

| Situation | Preferred reversal | Why |
|---|---|---|
| Code-only change, previous artifact still compatible | Roll back to previous digest | Fastest known-good state |
| Feature behind a toggle | Disable the toggle | Seconds, no deploy, reduced service instead of outage |
| Schema already contracted, or external side effects sent (payments, SMS, tax submissions) | Roll forward with a fix and compensating actions | Old code cannot run against new data; side effects cannot be recalled |
| Infrastructure change applied | Apply the previous configuration through the pipeline, never by console | Keeps state and code aligned |
| Unknown cause, user harm ongoing | Stop the rollout, shift traffic to the known-good set, then diagnose | Recovery first, root cause second |

Rollback triggers must be numbers observed in a named window, for example:
"abort if 5xx ratio on the canary exceeds control by 0.5 percentage points for
5 consecutive minutes, or p95 latency exceeds 800 ms". The on-call engineer may
abort without further approval.

## 4. Release plan fields this reference must fill

- Core strategy and add-ons, with the reason tied to statefulness, capacity, and risk.
- Health checks that gate each step (readiness, not just process liveness).
- Canary or ramp schedule with hold durations and abort thresholds.
- Reversal method per change class from section 3.
- Toggle owner and removal date for every new toggle (stale toggles are debt; schedule removal within one or two release cycles).
- Observation window and who watches it.

## 5. Senior versus generic

Generic: "Use blue-green deployment for zero downtime and roll back if there
are issues." Senior: names the core strategy and why the alternative was
rejected, gives numeric abort thresholds, distinguishes rollback from toggle
disable from roll-forward per change, and says what happens to in-flight
requests, queued jobs, and sessions during the switch.

Worked example (original): a Kampala school-fees platform releases a new
mobile-money reconciliation engine before term opening. Core: rolling
new-before-old on two app servers (no budget for a duplicate set). Add-ons:
the new engine sits behind a toggle, first enabled for three pilot schools,
with a dark-launch week in which both engines run and only the old one posts
to the ledger; any mismatch above 0.1% of transactions halts the ramp. Reversal:
toggle off; no rollback of the binary is needed. Term-opening week is a change
freeze.

## 6. Failure modes

- Blue-green with a shared database whose migration the blue side cannot read: the fast rollback is an illusion. Pair with expand-contract.
- Canary with too little traffic to be statistically different from control; the canary "passes" by silence. Size the slice or extend the window.
- Health check that returns 200 before caches, connections, or migrations are ready.
- Sticky sessions ignored during cutover, producing users who bounce between versions.
- Toggles never removed, multiplying untested code paths.

## Evidence and currentness

Concept-stable content; no versions or vendor capabilities asserted. Accessed
2026-09-24 for cross-check against the existing engine guidance in
`deployment-pipeline.md` and `../../cloud-architecture/references/deployment-patterns.md`.

Sources: Brikman (2025) *Fundamentals of DevOps and Software Delivery*; Humble
and Farley (2010) *Continuous Delivery*.
