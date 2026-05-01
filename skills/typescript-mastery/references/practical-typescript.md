# Practical TypeScript

This file is self-contained. It was prepared from local EPUB study notes and
must remain useful even if the EPUB is deleted.

Source input: local EPUB `C:\Users\Peter\Downloads\Documents\Learning TypeScript.epub`.

Use this reference when TypeScript work needs maintainable production judgement
instead of isolated type-system tricks.

## Type Design Rules

- Model impossible states as impossible with discriminated unions.
- Prefer `unknown` at trust boundaries, then narrow with runtime validation.
- Use `satisfies` for config objects where values should stay narrow while still
  conforming to a required shape.
- Avoid exporting overly clever conditional types unless they remove real
  duplication for callers.
- Keep inferred local types, annotate public APIs, and make domain DTOs explicit.
- Use branded or opaque types for IDs and units that must not be mixed.

## Core TypeScript Principles

- TypeScript checks static shapes; it does not change JavaScript runtime
  behaviour.
- Prefer precise types over broad `string`, `number`, `object`, or `Function`
  when the domain has known states.
- Let inference work for local variables; annotate exported functions, public
  interfaces, API DTOs, and generic helpers.
- Avoid `any`. If the value is unknown, use `unknown` and narrow it.
- Turn on strict mode for production code unless legacy migration requires a
  staged plan.
- Use type errors as design feedback. If a type is painful to use, the model may
  be hiding ambiguous states.

## Narrowing and Unions

Use narrowing intentionally:

- `typeof` for primitives
- `instanceof` for class instances and errors
- property checks for object unions
- user-defined type guards for reusable runtime checks
- assertion functions when invalid data should throw
- discriminant fields for workflow/state machines

Discriminated union pattern:

```typescript
type PaymentState =
  | { status: "draft" }
  | { status: "pending"; submittedAt: string }
  | { status: "paid"; paidAt: string; receiptId: string }
  | { status: "failed"; reason: string };
```

Review every `switch` over a discriminant for exhaustive handling.

## Boundary Discipline

| Boundary | TypeScript practice |
|----------|---------------------|
| HTTP input | parse and validate before domain use |
| database row | map to domain/read model intentionally |
| external SDK | wrap in project-owned interface |
| feature config | `as const` plus `satisfies` |
| state machine | discriminated union by status/kind |
| errors | typed result or known error hierarchy |

TypeScript does not validate runtime data. Pair static types with a schema
validator when data crosses process, network, database, file, or user boundaries.

## Object and Interface Guidance

| Need | Prefer |
|------|--------|
| public object contract | `interface` |
| union, tuple, mapped type, conditional type | `type` |
| immutable config | `as const` plus `satisfies` |
| partial update DTO | explicit patch type, not blind `Partial<T>` for all cases |
| external JSON | schema-validated parsed type |
| internal domain object | explicit domain type separate from persistence row |

Avoid deep inheritance. Use composition, discriminated unions, and small
interfaces when behaviour varies by state or capability.

## Generics and Utility Types

- Generic type parameters should represent real variability for callers.
- Constrain generics with `extends` when operations require fields.
- Use defaults only when they make the common case simpler.
- Avoid exposing nested conditional types as public API unless the benefit is
  clear and documented.
- Utility types are powerful but can hide intent; prefer named domain types for
  public contracts.

Good uses:

- `Pick`/`Omit` for view-specific DTOs when stable
- `Record` for total maps over known key unions
- `Readonly` for immutable inputs
- `NonNullable` after a boundary has been proven
- `ReturnType`/`Parameters` for internal helper derivation

Risky uses:

- `Partial<DomainEntity>` for write commands
- `Record<string, unknown>` where a real schema exists
- wide intersections that produce impossible or confusing shapes
- type assertions that bypass validation

## Async and Error Modeling

- Model expected failure as data when callers must branch on it.
- Throw for programmer errors and unexpected infrastructure failures when a
  higher layer owns recovery.
- Type `catch` values as `unknown`; narrow before reading fields.
- Prefer `Result<T, E>` for domain workflows where failure is common and
  meaningful.
- Include cancellation and timeout behaviour in async API design.

Example result shape:

```typescript
type Result<T, E extends { code: string; message: string }> =
  | { ok: true; value: T }
  | { ok: false; error: E };
```

## Configuration and tsconfig

Production defaults:

- `strict: true`
- `noImplicitAny: true`
- `strictNullChecks: true`
- `noUncheckedIndexedAccess: true` for safety-sensitive code
- `exactOptionalPropertyTypes: true` when optional vs `undefined` matters
- `useUnknownInCatchVariables: true`
- `noImplicitOverride: true` for class-heavy code

Migration rule: tighten compiler settings in stages, with a tracked list of
temporary exceptions. Do not silence broad areas with `skipLibCheck`, `any`, or
blanket assertions unless the risk is documented.

## Maintainability Checks

- If a type requires a long comment to explain, consider a simpler public shape.
- If inference produces `any`, fix the source instead of annotating downstream.
- If a generic has more parameters than the domain concept has variability,
  split it.
- If a utility type is used once and obscures intent, inline the type.
- If a type mirrors database structure exactly, check whether domain behaviour
  or API evolution needs a separate model.

## Framework and API Boundary Checks

- In React, type component props explicitly and avoid state shapes that allow
  contradictory UI states.
- In API clients, generate or validate DTOs from the contract and map them to
  UI/domain types.
- In backends, validate request bodies before casting and keep auth-derived
  tenant/user IDs separate from request input.
- In tests, add type-level tests for complex public generics and runtime tests
  for schema validators.

## Review Questions

- Are all nullable states intentional and handled?
- Are external inputs validated before being trusted?
- Are unions exhaustive in reducers, workflow handlers, and render branches?
- Does the type system protect tenant/user/resource IDs from accidental mixing?
- Are public exports stable enough for downstream callers?
- Are type assertions isolated and justified?
- Are public types documented by names and examples instead of cleverness?
