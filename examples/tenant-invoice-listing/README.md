# Tenant-scoped invoice listing teaching slice

This read-only example follows a server-authenticated tenant boundary across a PHP service/controller, OpenAPI contract, Next.js App Router page/handler, and Compose screen. The fixture uses synthetic data only. The listing path does not create or post ledger entries; accounting treatment and posting rules remain owned by Chwezi Accounting Doctrine.

The [manual review exercise](review-exercise.md) contains the unsafe synthetic specimen
from the practitioner review and the four expected finding groups. It is marked
non-executable and must not be copied into an application.

## Evidence and limits

The PHP source and executable test are copied from the prepared disposable fixture. The 15-check test runs against PDO SQLite by default. An optional test mode applied the illustrative MySQL migration and ran those checks against a disposable MySQL 8.4 database. This does not validate production deployment, backup/restore, or an application-specific migration framework. The schema requires matching column types, existing identity/session verification, and a reviewed rollback plan before use.

The OpenAPI contract describes the PHP fixture response mounted at `GET /api/invoices`. The Next.js source uses a page at `/invoices` and a separate Route Handler at `/api/invoices`; keeping them on separate route segments is required by the App Router. The handler is an illustrative server-only pattern requiring the project’s actual `auth` provider, database client, schema, and verified session claims. It intentionally has no mutation or shared user cache. The Android source is a Compose screen excerpt, not a complete application or Gradle project. Its UI state must be connected to an authenticated API repository and ViewModel in a real application.

The Next.js source built in a disposable project with Next.js 16.4.3 and passed a TypeScript check. Unauthenticated and invalid-query HTTP checks passed against the production-mode server. This does not integrate a real identity provider or database.

The Android source is a Compose screen excerpt, not a complete application. The excerpt compiled in a disposable Gradle project using AGP 9.1.1, Gradle 9.3.1, Kotlin 2.4.21, Compose BOM 2026.09.00, and compileSdk 37. No emulator rendering or Play release validation was performed. Its UI state must be connected to an authenticated API repository and ViewModel in a real application. Compile SDK and Play target API are separate decisions; confirm current Play requirements before release.

This artifact does not prove production readiness, MySQL deployment compatibility, Android release compliance, or protection against all security vulnerabilities. Validate the exact dependency and runtime versions, advisories, identity provider, schema, accessibility, and deployment before adopting it.

## Check

```sh
php examples/tenant-invoice-listing/php/test.php
```

By default the fixture runs in in-memory PDO SQLite mode. To exercise the illustrative
MySQL migration against a disposable, empty database, set `INVOICE_TEST_DSN`,
`INVOICE_TEST_USER`, and `INVOICE_TEST_PASSWORD`; the fixture applies the migration and
runs the same checks. Do not point it at a production or user-data database.

Expected result: 15 passing checks, with the selected PDO driver identified in the final
line. No paid model evaluation was run.
