# Intermittent, Performance, and Production Cases

## Intermittent failures

Measure failures/runs with confidence limits where useful. Freeze inputs, seeds, clocks, concurrency,
network conditions, and resource pressure separately. A single passing run does not establish repair;
compare the stated pre/post run count and rate.

## Performance regressions

Define workload, dataset, machine/device, build, warm-up, cache state, concurrency, duration, and
percentile. Compare against a relevant baseline and noise floor. Profile the limiting resource before
optimising; rerun the identical scenario after one change.

## Production-only symptoms

Prefer existing telemetry, trace IDs, sampled structured events, redacted replay, shadow traffic, or a
production-like lab. New telemetry requires operator approval, bounded cardinality, cost and privacy
review, rollback, and removal. Do not change user-visible behaviour as a diagnostic experiment without
release authority.

If production evidence cannot distinguish the cause, report the safest next observation and keep the
diagnosis unresolved.
