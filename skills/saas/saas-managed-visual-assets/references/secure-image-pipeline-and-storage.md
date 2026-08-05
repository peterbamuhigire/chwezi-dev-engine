# Secure Image Pipeline and Storage

Parent skill: [`saas-managed-visual-assets`](../SKILL.md).

## Trust boundary

Treat every upload as hostile bytes. Browser MIME, extension, dimensions, client compression,
and original filename are hints only. Authoritative acceptance happens after server-side content
detection and successful decoding within explicit resource budgets.

## Canonical pipeline

1. Authenticate, authorize the resolved scope, verify CSRF where applicable, rate-limit, and
   enforce a bounded request body before buffering or writing substantial data.
2. Stream to a private quarantine location with a cryptographically random temporary key. Never
   place the candidate under a public web root.
3. Detect type from bytes with the platform's content detector and require agreement with an
   allow-listed decoder. Reject SVG by default because it is active content; reject unexpected
   animation and multi-frame content unless the product has a separately reviewed need.
4. Read dimensions under decoder limits before full rasterization. Reject zero/negative values,
   oversized dimensions, excessive pixel count, decompression bombs, and decoder timeout/memory
   exhaustion.
5. Fully decode. Apply orientation, strip metadata/profiles unless deliberately retained, resize
   without enlargement, and re-encode from pixels to an approved canonical format.
6. Preserve alpha for logos and favicons with PNG or alpha-capable WebP. Use WebP/JPEG for opaque
   photographic backgrounds. Never choose an output extension from the original filename.
7. Iterate quality inside documented floors until the canonical output meets the hard byte limit.
   Reject rather than silently bypassing the limit or uploading the original.
8. Optionally scan the canonical output with the approved malware/content scanner. Hash it, write
   it under a new random immutable key, then commit metadata. Delete quarantine data on all paths.

The common default for auth backgrounds is a 1920 px long-edge envelope, quality starting near
75, and 512 KB hard output maximum. Logo and favicon profiles differ because transparency and
small-scale sharpness matter. Product-specific thresholds must be explicit and tested.

## Resource budgets

Define separate limits for ingress bytes, output bytes, width, height, total pixels, frames,
decoder memory, processing time, requests per actor/scope, and concurrent workers. Ingress may be
larger than canonical output, but it must remain bounded before decode. Keep processing outside a
latency-sensitive request when the chosen limits exceed the application's safe synchronous budget.

## Storage and delivery

- Use opaque random keys and immutable canonical objects. Keep quarantine, originals, and private
  canonical assets non-public.
- Publish through a controlled endpoint, signed URL/CDN transform, or generated public manifest
  that resolves opaque IDs. Authorize admin previews separately from public active assets.
- Return the canonical MIME, `X-Content-Type-Options: nosniff`, an explicit content disposition
  where appropriate, and a cache policy tied to immutable IDs/manifest versions.
- Do not execute, include, or reflect uploaded content as HTML, CSS, JavaScript, or templates.
- Restrict local paths with resolved-prefix checks and object-store keys with fixed prefixes.
  Database metadata is not proof that an arbitrary path is safe.

## Replacement and deletion

Never overwrite the current object in place. Write a new immutable object, commit the slot or
record swap, retain the old object for a short documented grace period if rollback requires it,
then enqueue garbage collection. Cleanup workers verify that no current metadata references an
object before deletion. Failed cleanup is retried and alerted; it must not roll back a successful
logical update.

## Security tests

Exercise valid JPEG/PNG/WebP, spoofed MIME/extension, truncated data, polyglots, SVG, animated or
multi-frame files, huge dimensions with tiny bytes, EXIF orientation, alpha edges, metadata
stripping, over-limit ingress/output, decoder timeout, concurrent quota races, path traversal,
cross-tenant IDs, CSRF failure, permission denial, cache invalidation, and failed storage/DB
commits. Fuzz or corpus-test the actual decoder where the risk warrants it.
