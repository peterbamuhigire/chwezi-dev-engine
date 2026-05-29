# Fair-Queueing Patterns (Reference)

Deep-dive for `saas-rate-limiting-and-quotas` section 7. Covers per-tenant queues,
weighted fair queueing (WFQ), deficit round robin (DRR), per-tenant concurrency
caps, and how each avoids starvation in a shared worker pool.

Problem: a shared async worker pool processes jobs from all tenants. Without
fairness, one tenant's 50,000-job batch monopolises every worker and every other
tenant's SLA collapses (their jobs sit behind the batch). The job of fair
queueing is: bounded wait for every tenant regardless of any one tenant's volume.

## The wrong baseline (why a single FIFO fails)

```text
single shared FIFO:  [t1 t1 t1 ... (50,000) ... t1 t1 | t2 t3 t4]
                      ^ t2/t3/t4 wait behind 50,000 t1 jobs
```

Failure mode: head-of-line blocking. A light tenant's single urgent job waits
behind a heavy tenant's batch. This is the anti-pattern the parent skill calls
out ("one big tenant's batch destroys SLA for the rest").

## Pattern 1: per-tenant queues + round-robin dispatcher

Split the single FIFO into one queue per active tenant; a dispatcher visits
queues in rotation, pulling one job per visit into the shared worker pool.

```text
producers -> push to per-tenant queue   q:tenant:<id>   (Redis list per tenant)
active set -> Redis set of tenant ids with non-empty queues
dispatcher loop:
  for tenant in round_robin(active_set):
    job = LPOP q:tenant:tenant
    if job: submit(job) to worker pool
    else: remove tenant from active_set
```

- Guarantees every active tenant gets served each cycle -> bounded wait
  proportional to the number of active tenants, not to the largest queue.
- Equal share by default. A 50k-job tenant and a 1-job tenant each get one slot
  per round; the heavy tenant simply takes many rounds to drain.
- Cost: a dispatcher process and a queue per active tenant. Keep an "active set"
  so you iterate only tenants with work, not every tenant that ever existed.

Use for: the common case. Equal fairness, simple to reason about.

## Pattern 2: weighted fair queueing (WFQ)

Plain round robin gives every tenant an equal share. WFQ gives each tenant a
share proportional to a weight (plan tier, seat count) while still never starving
the smallest.

```text
weight(tenant) = tier_factor   # e.g. free=1, pro=3, enterprise=10
              or = ceil(seats / 10)
per cycle, tenant t may dispatch up to weight(t) jobs before the dispatcher
moves on.
```

- Bigger/paying tenants get more throughput; small tenants still get at least one
  slot per cycle (their weight floor is 1) -> no starvation.
- Set the weight floor to >= 1 for every tenant. Failure mode of a 0 weight: that
  tenant is never served -> starvation, the exact thing you are preventing.

Use for: when throughput should track plan tier but you must still guarantee
liveness for the smallest tenant.

## Pattern 3: deficit round robin (DRR)

WFQ by job COUNT is unfair when job COST varies (one tenant's jobs are 10x more
expensive). DRR allocates a quantum of WORK (cost units) per tenant per round and
carries unused/overspent budget forward as a deficit.

```text
each tenant has: deficit_counter (starts 0), quantum (work units per round)
round:
  for tenant in active:
    deficit += quantum
    while head_job_cost(tenant) <= deficit:
       job = pop(tenant); deficit -= job.cost; dispatch(job)
    # leftover deficit carries to next round
```

- Fair by WORK, not by job count. A tenant submitting few-but-huge jobs cannot
  starve a tenant submitting many-but-tiny jobs, and vice versa.
- `quantum` should be >= the largest typical job cost so progress is made each
  round; too small a quantum stalls big jobs across many rounds (slow but not
  starved).

Use for: heterogeneous job costs (reports vs single-row updates vs large
exports).

## Pattern 4: per-tenant concurrency cap (back-pressure, not scheduling)

Cap how many of a tenant's jobs run CONCURRENTLY. Overflow waits in the tenant's
own queue and never enters the shared pool, so it cannot crowd out others.

```text
on dispatch attempt for tenant t:
  n = INCR running:tenant:t
  if n > cap(t): DECR; leave job in q:tenant:t; skip
  else: dispatch; on job completion DECR running:tenant:t
cap(t) = plan-derived (free 1, pro 5, enterprise 20)
```

- Simplest effective isolation: even with a naive shared pool, a per-tenant cap
  bounds any one tenant's footprint.
- Combine with per-tenant queues: the cap controls share; the queue holds the
  backlog. Always DECR in a finally block + a reconciliation janitor (a leaked
  counter permanently throttles that tenant).

Use for: the cheapest meaningful fairness guarantee; pairs well with any of the
above.

## Choosing a pattern

| Situation | Choose | Why / failure mode of alternative |
|---|---|---|
| Equal fairness, uniform job cost | Per-tenant queue + RR | Simple; single FIFO would head-of-line block |
| Throughput should track plan tier | WFQ | RR ignores tier; tier-by-cap alone wastes idle capacity |
| Job costs vary widely | DRR | Count-based WFQ over-serves cheap-job tenants |
| Minimal change, strong isolation | Per-tenant concurrency cap | Bounds blast radius without a dispatcher rewrite |
| Best of both | Per-tenant queue + cap + weights | Share, backlog, and isolation together |

## Starvation avoidance checklist

- Every tenant weight / quantum >= 1 (no zero share).
- Dispatcher iterates an ACTIVE set, so empty tenants do not waste cycles but
  newly-active ones join immediately.
- Idle-capacity fill: if some tenants are idle, let active tenants use the spare
  workers (work-conserving) rather than holding slots empty. Failure mode of a
  non-work-conserving scheduler: capacity sits idle while jobs wait.
- Aging / priority floor: a job that has waited beyond a threshold gets a
  priority bump so a steadily-busy heavy tenant cannot indefinitely defer a light
  tenant's occasional job.
- Cap the per-tenant queue depth; on overflow, shed with a clear
  `usage.queue_full` event rather than growing unboundedly (memory blow-up).

## Engines and where the logic lives

| Engine | Fairness primitive |
|---|---|
| Sidekiq Pro/Enterprise | Concurrency limits + rate limiters per group |
| Temporal | Per-namespace / per-task-queue concurrency limits |
| Celery | Per-queue routing + worker concurrency per queue |
| Custom | Redis lists per tenant + a dispatcher implementing RR/WFQ/DRR |

In a pooled multi-tenant SaaS the dispatcher owns fairness; workers stay dumb
(pull from the shared pool). Keeping the policy in one dispatcher makes WFQ/DRR
tunable without touching worker code.

## Anti-patterns

- Single shared FIFO -> head-of-line blocking by the heaviest tenant.
- Zero or missing weight for any tenant -> starvation.
- Non-work-conserving scheduling -> idle workers while jobs wait.
- Unbounded per-tenant queues -> a runaway producer exhausts memory.
- Concurrency counter without finally-DECR + janitor -> permanent throttle on
  crash.
- Fairness by job count when costs are wildly uneven -> effective unfairness;
  use DRR.
