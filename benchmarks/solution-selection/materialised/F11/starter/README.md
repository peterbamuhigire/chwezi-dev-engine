# Notification job

`notify.job.NotificationJob` delivers one notification through an injected transport. Tests use
`notify.clock.FakeClock` and a fake transport; there is no real provider.

## Contract

- `NotificationJob(transport, store, clock, rng=None, max_attempts=5, base_delay=1.0, max_delay=30.0)`
- `process(notification) -> dict` returns the stored record for `notification["id"]`:
  `{"id", "state", "attempts", "last_error", "provider_id"}` where `state` is one of
  `pending`, `sent`, `dead_letter`.
- `request_shutdown()` asks the job to stop at the next safe point.

## Delivery policy (agreed with the product owner)

- The idempotency key for a notification is its `id`, on every attempt.
- `TransientError` (and its subclass `RetryAfter`) and `TimeoutError` are retryable.
  `PermanentError` is not retried.
- At most `max_attempts` send attempts. After the last failed attempt the record moves to
  `dead_letter` with `last_error` set, so an operator can inspect and replay it.
- Delay before attempt n+1: `d = min(max_delay, base_delay * 2 ** (n - 1))`, jittered uniformly in
  `[d / 2, d]` using the injected `rng`. A `RetryAfter.seconds` hint raises the delay to at least
  the hint (still capped at `max_delay`).
- A `TimeoutError` from `send` is ambiguous: the provider may have accepted the message. Query
  `transport.status(key)` before retrying; `"accepted"` means the notification is sent.
- On shutdown the record stays `pending` with its attempt count, and nothing further is sent.
