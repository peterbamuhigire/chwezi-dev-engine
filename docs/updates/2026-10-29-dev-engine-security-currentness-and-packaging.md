# 2026-10-29: Dev Engine security, currentness and package evidence

This update is scoped to the Dev Engine repository. See the [Kaizen evidence index](../kaizen/2026-10-engine-kaizen/README.md) for the frozen baseline, retained decisions, test commands, limits and next-cycle work.

## Changes

- Replaced unsafe Next.js role-cookie, unscoped query, global private cache, and unchecked mutation examples with a server-only tenant data-access reference and a read-only example. Added structural and negative regression tests.
- Added a synthetic PHP, OpenAPI, Next.js and Compose tenant invoice slice. PHP reports `15` passing checks against PDO SQLite; this is not MySQL deployment evidence. Next.js and Compose were not built.
- Updated Android guidance to distinguish Google Play's target requirement from the compatibility platform, and removed an unsupported crash assertion.
- Added selected official currentness/security advisory records and runtime-selection guidance for Next.js, PHP, PostgreSQL, MySQL, Android, Kotlin and Compose.
- Added root Codex portable plugin and repository marketplace manifests, documented the measured invocation-level skill-list budget, and added checkout/package-oriented file cap checks.

## Verification boundary

The repository test suite reports `217 passed, 3 skipped`; routing and catalogue outcomes,
native prompt-input evidence, source links, exact command strings and all unassessed areas
are recorded in the Kaizen validation report. A local manifest shape check does not imply
public marketplace acceptance. The current checkout/package-oriented inventory is not a
generated archive count. Production database, Android, Next.js and account-specific plugin
behavior remain unassessed.
