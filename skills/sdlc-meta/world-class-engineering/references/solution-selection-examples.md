# Solution-selection examples

These examples are original teaching cases. They demonstrate the decision
process and its limits; they are not universal technology mandates.

## Reuse an existing normaliser

If a repository already exposes a customer-identifier normaliser with callers,
search its contract and tests before adding another formatter. Reuse is the
smallest option when the output and error behaviour match. Add a new adapter
only when the existing contract cannot represent the new context, and record
the incompatible invariant and removal trigger.

## Use a native date control with a server boundary

For a date-only field with no time-of-day semantics, a native date control can
provide keyboard and mobile behaviour cheaply. It still needs an associated
label, error state, server-side ISO validation, and tests that prevent UTC
midnight conversion. A custom calendar is justified only when the required
range, blackout, or interaction model is not expressible by the supported
native control; accessibility and focus recovery then become explicit tests.

## Prefer a suitable standard-library parser, but bound it

For a simple, documented CSV shape, a standard-library parser may be enough.
Bound input size, preserve source row errors, and test quoted separators and
embedded newlines. If the repository already has a locked mature parser with
the required dialect and security behaviour, adding a second parser is usually
unnecessary. A specialised dependency becomes reasonable when the required
format or Unicode behaviour exceeds the supported standard-library contract;
record licence, version, support and removal evidence.

## Preserve a database constraint and retry identity

An application check can improve the error message, but it must not replace a
database uniqueness or foreign-key constraint that protects concurrent writers.
Likewise, retrying a payment, webhook or queue job requires a durable idempotency
key and a replay-safe result. A shorter method that removes the constraint,
identity, audit event, or reconciliation path is a failed simplification.
