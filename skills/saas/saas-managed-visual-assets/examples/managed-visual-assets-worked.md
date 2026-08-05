# Worked Example: Platform Auth Assets with Tenant Fallback

Parent skill: [`saas-managed-visual-assets`](../SKILL.md).

Corevia exposes platform-managed auth imagery. Super Admin can store up to 20 backgrounds and one
light-surface logo, dark-surface logo, and favicon. Tenant overrides are planned but disabled; the
domain model still distinguishes platform scope so a later tenant layer does not require unsafe
client-provided IDs.

The upload endpoint resolves platform authority from the authenticated session, requires the
platform permission and CSRF token, streams to private quarantine, detects and decodes the image,
fits backgrounds inside 1920 px without enlargement, strips metadata, and re-encodes to a
canonical raster under 512 KB. Logos/favicons preserve alpha. The new random immutable object is
committed before metadata changes; a failed replacement leaves the old logo live.

The public auth manifest contains only opaque delivery URLs and a version. Sign-in chooses one
active background once and persists its ID for the journey. Forgot-password places its logo on
the dark blurred surface and requests the dark-surface slot; a logo inside the light card requests
the light-surface slot. Missing managed assets resolve to bundled defaults.

## Evidence excerpt

| Gate | Result |
|---|---|
| 20-background limit | Requests 1-20 accepted; request 21 rejected; concurrent boundary test passes |
| Replacement safety | Injected decoder/storage/metadata failures leave prior slot live |
| Scope/RBAC/CSRF | Unauthenticated, unprivileged, and forged-scope requests denied |
| Content security | Spoofed MIME, SVG, truncated data, pixel bomb, and over-limit output rejected |
| Delivery | Opaque IDs, correct MIME, nosniff, caching, and bundled fallback verified |
| Audit | Upload/delete/replace success and denial events include actor/scope/result without raw names |

Release remains conditional until the full browser/assistive visual matrix and the deployment
environment's malware-scanner path have run. The feature can be merged behind its mutation flag;
it must not be described as production-ready before those external checks complete.
