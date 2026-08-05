---
name: image-compression
description: Use when implementing or reviewing client image optimisation plus authoritative server decode, validation, resize, metadata stripping, and canonical re-encoding. Use saas-managed-visual-assets for administrative asset lifecycle and frontend-performance for page budgets.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

## Platform Notes

- Optional helper plugins may help in some environments, but they must not be treated as required for this skill.

# Image Compression
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Client-side image compression before upload using Squoosh with Canvas fallback and server-side Sharp validation. Use for web apps needing max width 1920px, max size 512KB, transparent UX, and consistent compression stats.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Performance | Image compression policy | Markdown doc covering Squoosh client-side targets, Canvas fallback, and Sharp server-side validation budgets | `docs/images/compression-policy.md` |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
<!-- dual-compat-end -->
Use a hybrid image-compression path:
- **Client primary:** Squoosh (WASM)
- **Client fallback:** Canvas API
- **Server safety net:** Sharp

**Common defaults:** 1920 px long-edge envelope, 512 KB canonical output maximum, quality 75
(adjust down inside an explicit quality floor). Product profiles override these values when the
rendering context, transparency, or small-scale legibility requires it.

## When to Use

✅ Web apps that upload user images and must reduce bandwidth
✅ Need transparent UX (no user action)
✅ Want modern codecs but must support older browsers

## When Not to Use

❌ Server-only batch pipelines (use Sharp directly)
❌ Large-scale media processing with complex transforms (use ImageMagick/FFmpeg)

## Core Rules

1. Maintain aspect ratio; never upscale.
2. Target max width $1920$px and max size $512$ KB.
3. Start at quality $75$; reduce in steps to meet size.
4. Prefer JPEG for compatibility; try WebP if size remains too large.
5. Log compression stats (ratio, saved, processing time).
6. Treat client MIME, extension, dimensions, and compressed bytes as untrusted hints.
7. On the server, detect content from bytes, constrain dimensions/pixels/resources, fully decode,
   strip metadata, and re-encode to a canonical allow-listed raster format.
8. Preserve alpha for logos/favicons; never force transparent artwork through JPEG.
9. Store canonical output under an opaque random key outside a public web root, then publish only
   through an authorized delivery policy.

## Decision Flow

1. **Client attempt (Squoosh)**
   - Resize → compress → check size.
   - Decrease quality until size limit met.
   - If still too large, try WebP.
2. **Client fallback (Canvas)**
   - Resize → toBlob JPEG → reduce quality if needed.
3. **Authoritative server pipeline (Sharp, GD, ImageMagick, or equivalent)**
   - Bound ingress before decode; detect MIME from bytes and require decoder success.
   - Reject excessive width, height, total pixels, frames, memory, or processing time.
   - Decode, orient, strip metadata, resize without enlargement, and canonicalize from pixels.
   - Preserve alpha where required; enforce final dimensions and byte limit after re-encode.
   - Never fall back to storing the original when processing fails.

## Implementation Steps (High Level)

1. **Client compression service**
   - Expose `compressImage(file, options)`.
   - Use Squoosh with dynamic import.
   - Fallback to Canvas on error.
2. **Upload hook / handler**
   - Validate input is image.
   - Compress transparently.
   - Upload compressed blob.
3. **Server middleware**
   - Use Sharp to enforce limits.
   - Return 413 if still too large.
   - Attach compression stats to logs.

## Required Defaults

- `maxWidth`: 1920
- `maxHeight`: 1920
- `maxSize`: $512 * 1024$
- `quality`: 75
- `minDimensions`: 200x200 (server-side)

## Anti-Patterns

- ❌ Skipping server validation
- ❌ Uploading original file on failure without logging
- ❌ Enlarging images
- ❌ Using blocking UI (must be transparent to user)

## References (Load as Needed)

- Client implementation: references/client.md
- Client usage example: references/client-usage.md
- Server middleware + routes: references/server.md
- Storage adapters (S3/local): references/storage.md
- Security checks: references/security.md
- Managed SaaS background/logo/favicon lifecycle: `saas-managed-visual-assets`
- Monitoring & analytics: references/monitoring.md
- Performance targets: references/performance.md
- Quality examples: references/quality-metrics.md
- Environment variables: references/env.md
- Docker (Sharp): references/docker.md
- Implementation checklist: references/implementation-checklist.md

## Output Expectations

- Client compression completes in $100$–$500$ ms typical
- Server compression $50$–$200$ ms typical
- Bandwidth reduction $85$–$97\%$

## Checklist

## Anti-Patterns

- Trusting client output. Fix: decode and validate media on the server.
- Treating `file.type`, extension, or magic bytes alone as authoritative. Fix: require content
  detection plus a successful bounded decode and canonical re-encode.
- Uploading the original after failure without consent. Fix: show a recoverable error and record the reason.
- Enlarging a small source. Fix: preserve its original dimensions.
- Blocking the interface during compression. Fix: provide asynchronous progress, cancellation, and retry.
- Applying one quality value to every format. Fix: tune by codec and inspect representative images.
- Converting transparent logos/favicons to JPEG. Fix: use PNG or alpha-capable WebP.
- Naming durable objects from the original filename. Fix: generate opaque random keys and store
  original names only as protected metadata when required.

## Capability contract

Read and search the upload path first. Edit only when authorised; execute codec, size-limit, malformed-file, and server-validation tests when supported. Network access is optional for dependency verification.

- [ ] Client: Squoosh primary + Canvas fallback
- [ ] Client: size/dimension limits enforced
- [ ] Server: authoritative content detection, bounded decode, canonical re-encode, and final limits
- [ ] Server: pixel/frame/time/memory budgets and malformed/polyglot test corpus
- [ ] Transparency: alpha preserved for logo/favicon profiles
- [ ] Storage: random immutable keys, private origin, controlled delivery, and cleanup
- [ ] Logging: compression stats & processing time
- [ ] Storage: image saved with metadata
- [ ] Tests: JPEG/PNG/WebP, large images, mobile
## Inputs
| Artefact | Required? | Purpose |
|---|---|---|
| Source images, display sizes, quality targets, formats, and delivery constraints | yes | Choose safe optimisation |
## Outputs
- Produce optimised assets and measured size, quality, format, and rendering evidence.
## Degraded mode
Fallback without visual inspection or target rendering: retain originals and mark quality comparison unverified.
## Workflow
Inventory usages, choose formats and dimensions, compress non-destructively, render representative states, compare quality and size, then update references.
