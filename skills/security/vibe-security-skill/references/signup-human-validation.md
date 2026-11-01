# Signup Human Validation Standard

Parent skill: [vibe-security-skill](../SKILL.md). Apply when protecting account creation, signup verification, or signup-related resend endpoints on web or Android.

## Default pattern

| Client | Default validation | Fallback |
|---|---|---|
| Web browser | Cloudflare Turnstile in Managed mode | Retry the challenge; apply the documented service-outage policy if Siteverify is unavailable. |
| Android app distributed through Google Play | Firebase App Check using the Play Integrity provider | Turnstile in an app WebView when the app cannot obtain an acceptable attestation. |
| Android debug or test build | Firebase App Check debug provider, restricted to non-production builds | Never allow the debug provider for production builds. |

These checks help reduce bot-driven and other unauthorised automated use. They establish risk signals about the client; they do not prove a person's legal identity or replace authentication, email confirmation, authorisation, or abuse controls.

## Required implementation controls

1. Protect every endpoint that creates a pending signup or sends a signup-related message, including resend flows. Put the decision in shared server-side validation so alternate clients cannot skip it.
2. Verify each Turnstile token on the server through Cloudflare Siteverify. Check success and the expected hostname; check action or custom data when the integration uses them. Tokens are single-use and expire after five minutes. A client widget alone is not a security control.
3. Verify Firebase App Check tokens on the backend using a supported verifier or a documented equivalent. Validate the expected Firebase project and app identity. For an Android client that cannot obtain the expected attestation, offer Turnstile fallback; an invalid attestation remains a denial. Do not accept a client-supplied device ID or device binding as proof of a genuine app.
4. Keep Turnstile secrets and any server credentials outside client code, logs, screenshots, and source control. Restrict widgets to owned hostnames and separate development, staging, and production credentials.
5. Keep independent controls: rate limits by IP and relevant account identifiers, email confirmation, and a honeypot where suitable. Tune limits for shared mobile-carrier IPs; do not make Turnstile the only abuse control.
6. Distinguish an invalid, expired, or replayed token from a verifier outage. Reject invalid tokens with a retry path. During a confirmed provider outage, permit a pending signup only under stricter rate limits and mandatory email confirmation; emit an operational alert and record the temporary mode, owner, and expiry. Never log the request as verified or treat an invalid token as an outage.
7. Roll out with `off`, `monitor`, and `enforce` modes where the system supports them. Monitor before enforcement, review real-device failure and completion data, and ramp enforcement in stages with a rollback switch.
8. Test valid, invalid, missing, expired, duplicate, and provider-error responses; web host mismatch; Android Play-installed, sideloaded, emulator, debug, low-end, and poor-network cases. Use vendor test credentials only outside production.
9. Review privacy notices and applicable app-store disclosures for data sent to the verification providers. Reassess the policy when distribution channels, providers, or signup flows change.

## Decision rules

| Condition | Action | Failure avoided |
|---|---|---|
| Browser signup | Managed Turnstile plus server-side Siteverify | Treating a browser-generated token as trusted without server verification |
| Android signup from a supported Play install | App Check Play Integrity, verified by the backend | Treating invented device identifiers as attestation |
| Android cannot obtain the expected attestation | Offer the Turnstile WebView fallback and preserve a usable retry path | Locking out users who cannot complete Play attestation |
| Verification service is unavailable | Apply the documented outage fallback, stricter limits, logging, and alerting | Confusing an outage with a valid verification result |
| Provider returns an invalid or replayed token | Deny the request and let the user obtain a fresh token | Reusing or accepting forged proof |
| Enforcement is proposed | Require monitor evidence, staged rollout, support review, and rollback readiness | Blocking legitimate users without measured impact |

## Source and currentness record

Checked against official provider documentation on 1 November 2026. Review by 1 February 2027, or earlier after a provider change or relevant release.

| Claim | Source scope and publication/update | Access and verification | Freshness / support | Uncertainty |
|---|---|---|---|---|
| Siteverify is mandatory; tokens are single-use and expire after 300 seconds | Cloudflare, [Server-side validation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/), last updated 16 September 2026 | Accessed and checked 1 November 2026 | Time-sensitive; verified for Cloudflare Turnstile | Recheck implementation details and error codes before adopting code examples. |
| Turnstile requires a browser environment and native apps use a WebView | Cloudflare, [Mobile implementation](https://developers.cloudflare.com/turnstile/get-started/mobile-implementation/), last updated 5 May 2026 | Accessed and checked 1 November 2026 | Context-bound; verified for documented WebView use | Low-end device performance and accessibility need project testing. |
| Firebase App Check supports Play Integrity on Android and requires backend verification for custom resources | Firebase, [Play Integrity provider](https://firebase.google.com/docs/app-check/android/play-integrity-provider/) (updated 28 October 2026) and [custom backend verification](https://firebase.google.com/docs/app-check/custom-resource-backend/) (updated 6 October 2026) | Accessed and checked 1 November 2026 | Time-sensitive; verified for Firebase App Check | Console setup, quotas, signing fingerprints, and SDK compatibility vary by project and must be checked at implementation time. |

The source files provided for this standard are implementation inputs, not runtime dependencies. Provider details, prices, quotas, account ownership, and project-specific configuration must be verified again before deployment.
