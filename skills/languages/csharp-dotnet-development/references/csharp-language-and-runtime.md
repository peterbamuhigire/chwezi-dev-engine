# C# Language And Runtime

Self-contained reference prepared from the supplied C#/.NET markdown books and current Microsoft documentation. Do not depend on the original source files being present.

## Table Of Contents

- Version and target framework choices
- Project file baseline
- Language idioms
- Modern C# feature guidance
- Error handling
- Runtime and performance defaults
- Interop and legacy modernization

## Version And Target Framework Choices

Use the project constraints first, then prefer current LTS for production. As of the source set used for this skill, .NET 10 is an LTS line with C# 14 support. Do not silently change target frameworks in an existing system; record compatibility and deployment impact first.

| Situation | Default choice | Reason |
|---|---|---|
| New production web/API/service | Current LTS .NET | Long support window and modern runtime features. |
| Library consumed by many apps | Multi-target only when required | Multi-targeting increases test and support burden. |
| Legacy .NET Framework app | Incremental migration | Preserve behaviour, isolate seams, migrate leaf projects first. |
| Performance-sensitive library | Benchmark before feature choices | Spans, pooling, AOT, and unsafe code need evidence. |
| Experimental C# feature | Avoid unless project opts in | Preview language/runtime coupling can surprise builds. |

## Project File Baseline

Use a central `Directory.Build.props` for shared defaults:

```xml
<Project>
  <PropertyGroup>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>false</TreatWarningsAsErrors>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  </PropertyGroup>
</Project>
```

Turn `TreatWarningsAsErrors` on in CI only after the current warning baseline is clean or intentionally suppressed. Add `.editorconfig` rules before style churn.

## Language Idioms

- Prefer explicit domain names over technical placeholders: `InvoiceLine`, not `DataItem`.
- Use nullable reference types as design feedback. Do not silence nullability with `!` unless construction flow is proven.
- Use `record` or `record struct` for immutable value-like data, not entities with identity and lifecycle.
- Use `required` members for object initialization contracts where constructor overloads would become noisy.
- Use primary constructors only when they improve readability; do not hide complex initialization in parameter lists.
- Use pattern matching for shape checks and discriminated state, but avoid clever nested patterns that obscure failure handling.
- Use `switch` expressions for pure mapping and `switch` statements for workflows with side effects.
- Use `Span<T>`/`ReadOnlySpan<T>` for hot parsing and buffer work; keep ordinary business code readable.
- Prefer `IReadOnlyList<T>`, `IReadOnlyCollection<T>`, or `IAsyncEnumerable<T>` at boundaries when callers should not mutate data.

## Modern C# Feature Guidance

| Feature | Use for | Avoid when |
|---|---|---|
| C# 14 extension members | Cohesive extension properties/operators around external types | Hiding domain services or business rules as magic methods |
| `field` keyword | Validating simple auto-property setters | A type already has a member named `field` or logic is non-trivial |
| Null-conditional assignment | Optional UI/view-model state updates | Required domain invariants where absence should fail loudly |
| `nameof(List<>)` | Diagnostics and generated code | Replacing stronger typed contracts |
| Lambda parameter modifiers | `out`, `ref`, `scoped` delegates with concise syntax | Reducing clarity in public API examples |
| Partial constructors/events | Source generators and split generated/user code | Ordinary hand-written classes |
| Required members | DTOs and options that need complete initialization | EF entities or serializers that cannot set them reliably |
| Collection expressions | Small, readable literals | Large or performance-sensitive allocations without measurement |

## Error Handling

- Throw exceptions for programmer errors and unrecoverable infrastructure failures.
- Return result types for expected business declines: validation failures, insufficient balance, permission denial, duplicate idempotency key.
- Include actionable context in exception messages, but never secrets or personal data.
- Use exception filters sparingly for logging or policy decisions.
- Keep user-facing errors stable and localizable; keep diagnostic detail in logs/traces.

## Runtime And Performance Defaults

- Measure with BenchmarkDotNet, `dotnet-counters`, traces, or realistic load tests before micro-optimizing.
- Avoid allocations on hot paths: prefer pooled buffers, spans, and structured logging templates.
- Use `HttpClientFactory` for outbound HTTP; do not instantiate `HttpClient` per request.
- Use `TimeProvider` for testable time and timers.
- Avoid unbounded LINQ over large in-memory collections on request paths.
- Keep trimming and NativeAOT opt-in. They can reduce deployment size and startup time but require compatibility testing with reflection, serialization, DI, and libraries.

## Interop And Legacy Modernization

- Separate legacy adapters from new domain/application code.
- Replace Web Forms or framework-era static helpers with typed services only at seams, not through a rewrite-first plan.
- Port class libraries before UI hosts when possible.
- Keep WPF/WinForms on Windows-only paths; use MAUI, Avalonia, or web frontends only after product requirements justify the migration.
- Preserve public API and persistence behaviour with characterization tests before changing framework versions.
