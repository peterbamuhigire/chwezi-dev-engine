# Tenant-scoped invoice listing teaching slice

This read-only example follows a server-authenticated tenant boundary across a PHP service/controller, OpenAPI contract, Next.js App Router page/handler, and Compose screen. The fixture uses synthetic data only. The listing path does not create or post ledger entries; accounting treatment and posting rules remain owned by Chwezi Accounting Doctrine.

## Evidence and limits

The PHP source and executable test are copied from the prepared disposable fixture. The 15-check test runs against PDO SQLite. The MySQL migration is illustrative and has not been applied to MySQL. It requires an application-specific migration framework, matching column types, existing identity/session verification, and a reviewed rollback plan before use.

The API contract describes the PHP fixture response. The Next.js source is an illustrative server-only pattern requiring the project’s actual `auth` provider, database client, schema, and verified session claims. It intentionally has no mutation or shared user cache. The Android source is a Compose screen excerpt; it is not a complete Gradle project and has not been built or rendered on an emulator. Its UI state must be connected to an authenticated API repository and ViewModel in a real application.

This artifact does not prove production readiness, MySQL compatibility, Android release compliance, or protection against all security vulnerabilities. Validate the exact dependency and runtime versions, advisories, identity provider, schema, accessibility, and deployment before adopting it.

## Check

```sh
php examples/tenant-invoice-listing/php/test.php
```

Expected result: 15 passing checks and an explicit PDO SQLite limitation. No paid model evaluation was run.
