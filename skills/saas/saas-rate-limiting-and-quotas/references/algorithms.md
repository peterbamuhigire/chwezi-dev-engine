# Rate-Limiting Algorithms (Reference)

Deep-dive for `saas-rate-limiting-and-quotas` section 3. Compares token bucket, sliding
window (log and counter), fixed window, and leaky bucket, with concrete
thresholds, the failure mode of each wrong choice, and which limit type each
fits.

## At a glance

| Algorithm | Burst behaviour | Memory per key | Accuracy | Best limit type | Wrong-choice failure mode |
|---|---|---|---|---|---|
| Token bucket | Allows burst up to bucket size | O(1): tokens + timestamp | High | Request rate w/ burst | Too-small bucket rejects legit cron bursts |
| Leaky bucket (queue) | Smooths; no burst out | O(1) counter or O(N) queue | High | Outbound smoothing | Adds latency; rejects on full queue |
| Fixed window | 2x burst at boundary | O(1): one counter | Low at edges | Cheap period counters | Boundary burst = 2x limit in one instant |
| Sliding window log | Exact | O(N): one entry per request | Exact | Strict low-volume limits | Memory blows up at high request rates |
| Sliding window counter | Near-exact | O(1): two counters | Approx (good) | Period quota, high volume | Slight over/under at window edge |

## Token bucket

A bucket holds up to `capacity` tokens and refills at `refill_rate` tokens per
second. Each request costs N tokens; allow if enough tokens, else reject.

```text
state: tokens (float), last_refill_ts
on request(cost):
  now = monotonic_now()
  tokens = min(capacity, tokens + (now - last_refill_ts) * refill_rate)
  last_refill_ts = now
  if tokens >= cost: tokens -= cost; ALLOW
  else: REJECT, retry_after = (cost - tokens) / refill_rate
```

- Tune `capacity` to the largest legitimate burst (e.g. a cron client firing 200
  jobs at the top of the minute) and `refill_rate` to the sustained allowance.
- Example: sustained 100 req/s with 200-burst tolerance -> `refill_rate=100`,
  `capacity=200`.
- Failure mode of `capacity == refill_rate` (no burst headroom): legitimate
  bursty clients get 429s for traffic that is within their average budget. This
  is the most common rate-limit complaint.

Use for: API request rate. It is the default for "N requests per second/minute
with reasonable burst". Implement atomically (see `redis-implementation.md`).

## Leaky bucket

Two framings. As a meter it is equivalent to token bucket. As a QUEUE it admits
requests into a fixed-size buffer that drains at a constant rate -- this is the
smoothing variant.

```text
state: queue (size <= capacity), drains at leak_rate per second
on request: if queue not full: enqueue; else REJECT
worker: dequeue at exactly leak_rate -> constant downstream rate
```

- Output rate is perfectly constant regardless of input burstiness -- ideal when
  the protected resource cannot tolerate spikes (a fragile downstream API, a DB
  write path).
- Cost: adds queueing latency, and a full queue rejects. Do not use it where
  callers expect immediate accept/reject with no added latency.

Use for: smoothing outbound work to a fixed rate (webhook delivery, calls to a
rate-limited third party), and as the basis for fair drain in worker pools.

## Fixed window

Count requests in the current calendar window (e.g. per minute); reset at the
boundary.

```text
key = "rl:" + tenant + ":" + floor(now / window)
n = INCR key ; EXPIRE key window
ALLOW if n <= limit
```

- Cheapest possible: one counter, one INCR.
- Boundary-burst flaw: a client can send `limit` requests at 11:59:59.9 and
  another `limit` at 12:00:00.1 -- 2x the intended rate in a ~200ms span. Failure
  mode: a "100/min" limit permits 200 requests across a one-second boundary, which
  can overwhelm a downstream sized for 100.

Use for: per-day / per-month counters where the boundary burst is benign (e.g. a
monthly quota that is really about the total, not instantaneous protection).

## Sliding window log

Store the timestamp of every request; count those within the trailing window.
Exact, but O(N) memory per key.

```text
ZADD zkey now now ; ZREMRANGEBYSCORE zkey 0 (now-window) ; n = ZCARD zkey
ALLOW if n <= limit
```

- Perfectly accurate, no boundary artefact.
- Memory and CPU scale with request volume: a 10k req/min key stores 10k members.
  Failure mode at scale: Redis memory and ZADD/ZREMRANGEBYSCORE cost explode;
  the limiter becomes the bottleneck it was meant to protect.

Use for: strict, low-volume limits where exactness matters (e.g. 5 login attempts
per minute, sensitive operations) -- never for high-traffic API rate limits.

## Sliding window counter (the practical compromise)

Approximate a sliding window using the current and previous fixed-window counts,
weighted by how far into the current window we are. O(1) memory, near-exact, no
boundary doubling.

```text
cur   = count(current_window)
prev  = count(previous_window)
elapsed_frac = (now mod window) / window
estimate = cur + prev * (1 - elapsed_frac)
ALLOW if estimate <= limit
```

- Smooths the fixed-window boundary burst while keeping two counters.
- Slight over- or under-count near the edge (bounded, typically < a few percent);
  acceptable for almost all SaaS rate limiting and period quotas.

Use for: high-volume rate limits and rolling period quotas where you want
sliding-window fairness without sliding-window-log memory.

## Concurrency limit (not a windowed algorithm)

Gate the number of IN-FLIGHT requests, not a rate. Atomic INCR on entry, DECR on
exit, reject above limit.

```text
on enter: n = INCR concurrent:tenant ; if n > limit: DECR; REJECT
on exit:  DECR concurrent:tenant      (in a finally/defer block)
janitor:  reconcile counter vs real in-flight every few minutes (handles crashes)
```

- Failure mode if DECR is missed (crash, exception path): the counter leaks
  upward and eventually rejects everything. Always DECR in a finally block AND run
  a reconciliation janitor; optionally use short-TTL keys per in-flight token.

Use for: max concurrent requests, max concurrent heavy reports, DB-pool caps.

## Choosing per limit type

| Limit type | Choose | Reason |
|---|---|---|
| API requests/sec with burst | Token bucket | Burst tolerance + sustained rate in one model |
| Rolling monthly quota, high volume | Sliding window counter | O(1), no boundary doubling |
| Per-day/month total, burst benign | Fixed window | Cheapest; boundary burst harmless for a total |
| Login attempts / sensitive ops | Sliding window log | Exactness matters; volume is low |
| Outbound to fragile downstream | Leaky bucket (queue) | Constant output rate |
| Max in-flight / concurrency | Atomic counter | It is a level, not a rate |

Default stack for a typical SaaS: token bucket for request rate, sliding window
counter for period quotas, atomic counter for concurrency, leaky-bucket drain in
the worker pool for outbound smoothing.

## Clock and distribution notes

- Use a single time source for the limiter (the Redis server clock via
  `redis.call('TIME')`), not each app node's wall clock -- app clocks drift and
  produce inconsistent decisions across nodes. See `redis-implementation.md`.
- Token bucket and sliding-window-counter need read-modify-write to be ATOMIC.
  A check-then-increment across two round trips races and lets requests slip
  past the limit under load. Use a Lua script or `INCR`-based primitives.
- TTL every key so abandoned tenant buckets do not accumulate in Redis.
