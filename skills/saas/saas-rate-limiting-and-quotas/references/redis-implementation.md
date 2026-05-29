# Redis Implementation (Reference)

Deep-dive for `saas-rate-limiting-and-quotas` section 5. Atomic Lua scripts for token
bucket and sliding window, key design for per-tenant limits, clock and race
handling, TTLs, and cluster considerations.

Redis is the default store: sub-millisecond, shared across app instances, and it
executes Lua scripts atomically (single-threaded command execution, no
interleaving). Atomicity is the whole point -- a check-then-increment over two
round trips races under load and lets requests slip past the limit.

## Key design

```text
rl:rate:{tenant_id}:{route}            token bucket for an API route
rl:rate:{tenant_id}:{route}:{api_key}  if you also limit per key
rl:concurrent:{tenant_id}              in-flight counter
quota:period:{tenant_id}:{metric}:{yyyymm}   monthly fixed-window counter
rl:swc:{tenant_id}:{metric}:{window_id}      sliding-window-counter buckets
```

Rules:

- Always include `{tenant_id}`. Per-IP-only or per-API-key-only keys are the
  anti-patterns in the parent skill: one NATed tenant penalises others; one
  tenant's multiple keys evade the aggregate. If you limit per key, ALSO keep a
  per-tenant aggregate key.
- In Redis Cluster, keep all keys touched by one script in the same hash slot by
  wrapping the routing portion in a hash tag: `rl:rate:{ten_123}:search`. The
  `{...}` is the slot-hashed part; everything a single EVAL touches must share it,
  or the cluster rejects the multi-key script (CROSSSLOT error).
- TTL every key. A bucket with no PEXPIRE leaks one key per tenant forever.

## Atomic token bucket (Lua)

```lua
-- KEYS[1] = bucket key            e.g. rl:rate:{ten_123}:search
-- ARGV[1] = capacity (tokens)
-- ARGV[2] = refill_per_second
-- ARGV[3] = cost (tokens this request needs)
-- Uses Redis server TIME for a single authoritative clock.
local capacity    = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local cost        = tonumber(ARGV[3])

local t      = redis.call('TIME')                  -- {seconds, microseconds}
local now_ms = (tonumber(t[1]) * 1000) + math.floor(tonumber(t[2]) / 1000)

local b       = redis.call('HMGET', KEYS[1], 'tokens', 'ts')
local tokens  = tonumber(b[1])
local last_ms = tonumber(b[2])
if tokens == nil then tokens = capacity; last_ms = now_ms end

local elapsed = now_ms - last_ms
if elapsed < 0 then elapsed = 0 end                -- guard clock going backwards
tokens = math.min(capacity, tokens + (elapsed / 1000.0) * refill_rate)

local allowed = 0
local retry_after_ms = 0
if tokens >= cost then
  tokens = tokens - cost
  allowed = 1
else
  retry_after_ms = math.ceil(((cost - tokens) / refill_rate) * 1000)
end

redis.call('HMSET', KEYS[1], 'tokens', tokens, 'ts', now_ms)
-- TTL = time to fully refill an empty bucket, doubled, so idle keys expire.
redis.call('PEXPIRE', KEYS[1], math.ceil((capacity / refill_rate) * 1000 * 2))

return { allowed, math.floor(tokens), retry_after_ms }
```

Why it is correct:

- One EVAL = one atomic operation. No other client observes the half-updated
  bucket, so there is no check/increment race.
- `redis.call('TIME')` uses the server clock, not the app node's clock. Failure
  mode of passing `now` from each app node: nodes drift, the same bucket refills
  inconsistently depending on which node served the request, and the limit is
  effectively wrong.
- `elapsed < 0` guard: if the server clock steps backward (NTP adjustment), do
  not credit negative tokens.

Caller (Python redis-py), loaded once via `register_script` so it runs through
`EVALSHA`:

```python
import redis
r = redis.Redis(...)
token_bucket = r.register_script(open("token_bucket.lua").read())

def allow(tenant_id, route, capacity, refill_per_sec, cost=1):
    key = f"rl:rate:{{{tenant_id}}}:{route}"   # {tenant_id} = cluster hash tag
    allowed, remaining, retry_ms = token_bucket(
        keys=[key], args=[capacity, refill_per_sec, cost]
    )
    return bool(allowed), remaining, retry_ms
```

`register_script` sends the body once; subsequent calls use the cached SHA. On a
`NOSCRIPT` error (after a Redis restart or failover) redis-py auto-reloads it.

## Atomic sliding-window counter (Lua)

Two fixed sub-windows, weighted by position. O(1) memory, no boundary doubling.

```lua
-- KEYS[1] = base key   e.g. rl:swc:{ten_123}:apicalls
-- ARGV[1] = limit
-- ARGV[2] = window_seconds
local limit  = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

local t   = redis.call('TIME')
local now = tonumber(t[1])                          -- seconds
local cur_id  = math.floor(now / window)
local elapsed = (now % window) / window             -- 0..1 into current window

local cur_key  = KEYS[1] .. ':' .. cur_id
local prev_key = KEYS[1] .. ':' .. (cur_id - 1)

local cur  = tonumber(redis.call('GET', cur_key))  or 0
local prev = tonumber(redis.call('GET', prev_key)) or 0
local estimate = cur + prev * (1 - elapsed)

if estimate >= limit then
  return { 0, math.floor(estimate) }               -- reject; do NOT increment
end

redis.call('INCR', cur_key)
redis.call('EXPIRE', cur_key, window * 2)          -- keep prev available next window
return { 1, math.floor(estimate) + 1 }
```

In Redis Cluster, `cur_key` and `prev_key` share the `{ten_123}` hash tag, so the
multi-key script stays in one slot.

## Concurrency counter (atomic, with leak protection)

```lua
-- KEYS[1] = rl:concurrent:{ten_123}   ARGV[1] = max
local n = redis.call('INCR', KEYS[1])
if n == 1 then redis.call('EXPIRE', KEYS[1], 86400) end   -- floor TTL, refreshed below
if n > tonumber(ARGV[1]) then
  redis.call('DECR', KEYS[1])
  return 0
end
return 1
```

```python
def acquire(tenant_id, maximum):
    return bool(acquire_script(keys=[f"rl:concurrent:{{{tenant_id}}}"], args=[maximum]))

def release(tenant_id):
    # MUST run in a finally block on every terminal path.
    r.decr(f"rl:concurrent:{{{tenant_id}}}")
```

Leak handling: if a process crashes between acquire and release, the counter
drifts upward and eventually rejects everything. Mitigations:

- Always `release` in a finally/defer block.
- A janitor every few minutes recomputes the true in-flight count (from a source
  of truth such as a per-request token set with short TTLs) and resets the
  counter. Document this drift-reconciliation; it is the difference between a
  toy and a production limiter.

## Period quota (monthly) with reset safety

```text
key = quota:period:{tenant}:{metric}:{yyyymm}
INCR key
EXPIRE key (seconds to end of period + grace)
ALLOW if value <= plan_limit
```

- The `{yyyymm}` in the key gives automatic rollover: a new month is a new key
  that starts at zero. This avoids the "counters never reset -> permanent block"
  anti-pattern.
- Set the TTL to the remaining period plus a grace margin so end-of-month
  reconciliation can still read it.
- For billing-grade accuracy, treat Redis as the fast path and reconcile against
  the durable DB counter periodically (Redis is not your system of record for
  billing).

## Clock and race summary

| Hazard | Cause | Fix |
|---|---|---|
| Over-limit slip-through | check then incr in two round trips | One atomic Lua EVAL |
| Inconsistent buckets across nodes | per-node wall clock | `redis.call('TIME')` inside the script |
| Negative refill | clock steps backward | `if elapsed < 0 then 0` guard |
| Counter leak -> total block | crash between INCR/DECR | finally-release + janitor reconcile |
| Key accumulation | no TTL | PEXPIRE/EXPIRE on every key |
| Cluster CROSSSLOT error | multi-key script across slots | hash tag `{tenant_id}` on all keys |

## Operational notes

- Latency: a single EVAL is sub-millisecond; keep scripts small (no loops over
  large structures) so they do not block Redis's single thread.
- Availability: if Redis is briefly unavailable, decide fail-open (allow, risk
  over-limit) vs fail-closed (deny, risk false 429s). For request rate limiting,
  fail-open with an alert is usually correct; for hard plan quotas, fail-closed.
  Make it an explicit, documented choice, not an accident.
- Managed options: ElastiCache, Upstash, Redis Cloud. Upstash's per-request
  pricing suits spiky limiter traffic; ElastiCache suits steady high volume.
- Do not use in-process counters in a multi-instance deployment: each instance
  has its own count, so the effective limit is N x the intended limit.
