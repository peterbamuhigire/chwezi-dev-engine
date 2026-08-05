# Image Compression Security

Parent skill: [`image-compression`](../SKILL.md).

Client checks improve feedback and save bandwidth; they do not establish trust. `File.type`, an
extension, browser dimensions, client compression, and magic-byte checks are attacker-controlled
or incomplete. The server decides acceptance.

## Server acceptance gate

1. Authenticate/authorize the upload and verify CSRF where browser sessions are used.
2. Rate-limit and bound request bytes before buffering. Write only to private quarantine under a
   cryptographically random name.
3. Detect content type from bytes and require an allow-listed decoder to parse the same content.
   Reject MIME/decoder mismatch, malformed/truncated data, SVG by default, and unexpected
   animation or multi-frame inputs.
4. Read dimensions safely and reject zero values, excessive width/height, excessive total pixels,
   decompression bombs, decoder memory exhaustion, and timeout.
5. Fully decode, apply orientation, strip metadata/profiles unless explicitly retained, and
   re-encode from pixel data to a canonical format. Never copy the uploaded byte stream into the
   durable object.
6. Enforce output dimensions and byte limit after re-encoding. Reject rather than storing the
   original or bypassing policy.
7. Optionally malware-scan the canonical output according to the application's risk policy.
8. Delete quarantine bytes on success and every failure path.

## Format policy

Use a narrow raster allow-list. JPEG/WebP suit opaque photographs; PNG or alpha-capable WebP suit
transparent logos and favicons. Do not accept SVG as an image shortcut without a separate active-
content sanitization and delivery threat model. Output MIME and extension come from the canonical
encoder, never from the original filename.

## Required negative tests

- spoofed extension/MIME and conflicting magic bytes;
- truncated/corrupt images and polyglots;
- huge dimensions or pixel count in a small compressed file;
- SVG, unexpected animation, and excessive frames;
- EXIF orientation and metadata stripping;
- alpha edges and transparent backgrounds;
- over-limit ingress and post-encode output;
- decoder timeout/memory failure and cleanup;
- path traversal, cross-tenant object ID, permission denial, and CSRF failure where applicable.

Return stable user-safe error codes. Log correlation ID, actor/scope, detected type, dimensions,
sizes, duration, and result; never log raw bytes, credentials, signed URLs, or sensitive original
filenames.
