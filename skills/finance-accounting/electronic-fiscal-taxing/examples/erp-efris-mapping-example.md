# Worked Example: ERP to Uganda EFRIS Boundary

This example uses fictional identifiers and is not a production claim.

## Source

An approved ERP invoice has a tenant resolved by authenticated context, a
tenant-scoped fiscal profile, seller branch/device, customer classification,
governed tax codes, product-to-authority mappings, payment, and an immutable
source hash.

## Processing

The canonical service validates the snapshot, creates one outbox row with a
tenant/profile-scoped idempotency key, and calls the Uganda adapter. The adapter
adds its versioned envelope and protected transport. A test fixture may return a
test-labelled FDN/QR, but production code cannot wire the fake adapter.

## Failure and reconciliation

On timeout, the queue retains `unknown` evidence and retries the same key only
after query/reconciliation. On acceptance, the ERP atomically stores the
provider artefacts and exposes a read-only fiscal status to Android. A changed
payload under the same key is quarantined. The close report compares invoice,
tax control, queue, provider evidence, and correction records.

## Acceptance

The contract test proves mapping and safe error shape; the isolation test proves
tenant B cannot read or submit tenant A's profile; the replay test proves one
commercial document and one fiscal acceptance; the release record names the
remaining current-source and UAT gates.
