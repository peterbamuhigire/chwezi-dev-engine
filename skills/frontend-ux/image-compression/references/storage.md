# Canonical Image Storage

Parent skill: [`image-compression`](../SKILL.md).

## Storage contract

- Generate a cryptographically random opaque key after canonical encoding. Derive the extension
  and content type from the encoder, not from the original filename.
- Keep quarantine, originals, and private canonical objects outside a public web root or in a
  private bucket/container. Do not make an entire upload prefix public.
- Write immutable objects. Replacement writes a new object and swaps metadata only after the new
  object is durable.
- Publish through a controlled endpoint, signed URL/CDN policy, or manifest of opaque immutable
  URLs. Set the canonical MIME, `X-Content-Type-Options: nosniff`, and bounded cache headers.
- Store width, height, bytes, MIME, checksum, processing profile/version, creator/scope, and audit
  timestamps. Keep original filenames only as protected metadata when there is a real requirement.
- Scope keys and metadata by server-derived tenant/platform context; never concatenate an
  untrusted tenant, path, or filename into a durable location.

## Commit and cleanup sequence

1. Create private quarantine object.
2. Canonicalize and write a new immutable object under a random key.
3. Commit metadata/reference in the database or authoritative manifest.
4. Mark a superseded object for a documented rollback grace period.
5. Delete asynchronously only after verifying that no current metadata references the object.

If metadata commit fails, remove or enqueue cleanup of the new orphan and keep the prior reference.
If cleanup fails after a successful commit, retain the logical result and retry with alerting.
Never delete the current object before replacement commit.

## Local and object-store safeguards

For local storage, resolve the destination and verify it remains under the configured asset root
before writes or deletes; use restrictive directory/file permissions. For object stores, use a
fixed application prefix, least-privilege service identity, encryption, lifecycle policy, access
logging, and explicit public-delivery rules. In both cases, deletion consumes a trusted stored key,
not a client path.

Test path traversal, prefix escape, wrong-tenant IDs, stale signed URLs, cache invalidation,
metadata/object divergence, storage write failure, duplicate retries, and orphan reconciliation.
