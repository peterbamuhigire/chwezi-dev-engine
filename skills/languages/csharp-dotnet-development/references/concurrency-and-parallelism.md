# Concurrency And Parallelism

Self-contained reference prepared from the supplied parallel programming and C# project books. Use for async, parallel loops, channels, locks, and high-throughput services.

## Table Of Contents

- Decide async vs parallel
- Async rules
- Cancellation and timeouts
- Channels and pipelines
- Parallel CPU-bound work
- Thread safety
- Diagnostics

## Decide Async Vs Parallel

| Work type | Tool | Reason |
|---|---|---|
| I/O-bound HTTP/database/file call | `async`/`await` | Releases threads while waiting. |
| Many independent I/O jobs | Async with bounded concurrency | Avoids dependency overload. |
| CPU-bound transformation | `Parallel.ForEach`, PLINQ, or TPL | Uses multiple cores. |
| Producer/consumer workflow | `Channel<T>` or TPL Dataflow | Makes backpressure explicit. |
| Periodic service loop | `BackgroundService` + async delay | Supervised lifecycle and shutdown. |
| UI event | Async command/event handler | Keeps UI responsive. |

## Async Rules

- Async all the way down. Do not block on `Task`.
- Return `Task` or `Task<T>`; use `ValueTask<T>` only when profiling proves it helps and the API rules are understood.
- Use `ConfigureAwait(false)` in reusable libraries that do not need a synchronization context; app code can usually omit it.
- Never use `async void` except UI event handlers.
- Capture and observe all tasks. Fire-and-forget must be queued to supervised infrastructure.
- For streams, use `IAsyncEnumerable<T>` with cancellation.

## Cancellation And Timeouts

- Accept `CancellationToken` in every async boundary.
- Pass tokens to EF, HTTP, file, queue, and delay calls.
- Use timeouts at dependency boundaries. Cancellation is caller intent; timeout is policy.
- Distinguish user cancellation from dependency timeout in logs and responses.
- On shutdown, decide whether to drain, abandon, or checkpoint in-flight work.

## Channels And Pipelines

Use bounded channels for in-process queues:

```csharp
var channel = Channel.CreateBounded<Job>(new BoundedChannelOptions(100)
{
    FullMode = BoundedChannelFullMode.Wait
});
```

Rules:

- Bound the queue.
- Define retry and poison-message behaviour.
- Emit queue length and processing latency metrics.
- Do not use in-memory channels as durable queues for business-critical commands.
- For durable workflows, use a broker or database-backed outbox.

## Parallel CPU-Bound Work

- Use `Parallel.ForEachAsync` for many independent async operations with `MaxDegreeOfParallelism`.
- Use `Parallel.ForEach`/PLINQ for CPU-bound loops only after measuring.
- Avoid parallelism inside ASP.NET request handlers unless bounded and justified; the server is already concurrent.
- Do not mutate shared collections from parallel loops without concurrent structures or partitioned aggregation.
- Benchmark with realistic input size. Parallel overhead can make small workloads slower.

## Thread Safety

- Prefer immutability and message passing to locks.
- Keep lock scope tiny; never await while holding a `lock`.
- Use `SemaphoreSlim` for async-compatible throttling.
- Use `ConcurrentDictionary` and friends for shared state, but still design lifecycle and memory bounds.
- Be careful with `AsyncLocal`; it is useful for request context but can create hidden coupling and performance cost.

## Diagnostics

- Log task failures with operation name, correlation ID, and input identifiers safe for logs.
- Track queue length, worker count, duration, retry count, timeout count, cancellation count, and dead letters.
- Use `dotnet-trace`, `dotnet-counters`, and profiler traces for thread pool starvation, allocation pressure, and lock contention.

## Anti-Patterns

- `Task.Run` around I/O to "make it async".
- Unbounded `Task.WhenAll` over thousands of network calls.
- Sync-over-async in ASP.NET or UI apps.
- Hidden static mutable caches with no eviction.
- Retrying non-idempotent operations after partial success.
