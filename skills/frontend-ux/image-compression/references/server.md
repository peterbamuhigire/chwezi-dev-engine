# Authoritative Server Image Processing

Parent skill: [`image-compression`](../SKILL.md).

Use Sharp, GD, ImageMagick, or another maintained decoder/encoder available in the target stack.
The library name is secondary to the contract: bounded ingress, content detection, bounded decode,
canonical re-encode, and final limit enforcement.

## Processing profile

Define each usage profile explicitly:

| Profile | Geometry | Preferred output | Alpha | Typical concern |
|---|---|---|---|---|
| Auth/content background | Fit inside 1920 px long edge, no upscale | WebP/JPEG | no | LCP bandwidth and photographic quality |
| Light/dark logo | Fit inside product envelope, no upscale | PNG/WebP | yes | crisp edges and transparency |
| Favicon/app mark | Square canonical sizes | PNG/WebP/ICO as platform requires | yes | small-size legibility |

The common background starting point is quality 75 and 512 KB maximum. Iterate quality within a
documented floor and reject when output still exceeds policy. Do not silently change geometry or
quality below the accepted visual threshold merely to force success.

## Ordered server flow

```text
authorization -> bounded ingress -> private quarantine -> byte detection -> decoder probe
-> width/height/pixel/frame budgets -> full decode -> orientation -> metadata strip
-> resize without enlargement -> profile-aware canonical encode -> final size/dimension check
-> optional scan/hash -> immutable storage -> metadata commit -> quarantine cleanup
```

Apply timeout and memory budgets to probe and full decode. Where processing cannot safely fit the
request budget, enqueue a job and keep the candidate unavailable until completion. A processing
failure is a client-visible recoverable error, not permission to save the original.

## Response and evidence

Return the opaque asset ID/URL, canonical MIME, width, height, byte size, original byte size,
compression ratio, and a stable result/error code. Avoid exposing storage paths, decoder stack
traces, or signed origin credentials. Measure processing duration by stage so operations can
distinguish ingress, decode, encode, scan, storage, and metadata latency.

Tests must use the production decoder and profile configuration. Include representative visual
comparison, malformed corpus, alpha, orientation, exact boundary dimensions/bytes, quality-floor
failure, resource exhaustion, storage failure, and retry/idempotency cases.
