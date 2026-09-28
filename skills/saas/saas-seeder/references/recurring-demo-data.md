# Recurring demo data standard

Use this contract whenever a SaaS has a demo or sales environment.

## Required layers

1. Stable baseline: tenants, staff, roles, permissions, reference data, and the canonical walkthrough story.
2. Rolling activity: fictional tenant-scoped activity through a caller-selected date. Default to the latest 14 days.

## Command contract

Adapt the executable name to the host SaaS:

```text
php bin/demo-seed.php --to=YYYY-MM-DD --days=14
php bin/demo-seed.php --from=YYYY-MM-DD --to=YYYY-MM-DD
php bin/demo-seed.php --dry-run
```

The command accepts an explicit tenant/facility scope. `--force` is reserved
for deliberate reconciliation. Migrations and baseline/reference seeds run
before rolling activity.

## Safety and idempotency

- Use stable natural keys/idempotency keys for staff/login, patients, visits,
  OPD, IPD, labs, procedures, prescriptions, inventory/pharmacy, bills, and
  payments.
- Use a deterministic, realistic name pool for fictional people. Enforce
  unique full names across demo history, reserve canonical walkthrough names,
  and audit the generated name pool after each refresh.
- Never truncate, delete, or alter non-demo rows.
- Refuse production by default; require explicit opt-in for any override.
- Store each window in a run ledger with tenant, profile, dates, status,
  counts, and failure detail.
- A completed duplicate window returns `SKIPPED`; a failed window remains
  retryable. A later end date adds history without deleting old demo activity.

## Verification

After writing, assert tenant scope and at least one discoverable record for
each required workflow. Record the command, window, counts, migration status,
and idempotent rerun result as concise evidence.

## Demo login and second server

Demo sign-in follows [`demo-one-click-login.md`](demo-one-click-login.md): on a
demo host the page shows only one-click profile buttons, each posting a profile
key that the server maps through an allow-list to a demo user and signs in through
the normal authentication path (same RBAC, password step skipped). Gates:
`DEMO_LOGIN_ENABLED=true` in that server's `.env` and a demo host. No password is
ever written in code, pages, docs, evidence or commits. The server-side shortcut
seeder must be explicit opt-in and development/demo only, using the same named
accounts as the allow-list.

To use a second demo server, configure its own database connection, a strong
non-empty `PASSWORD_PEPPER`, and the demo-host flag, then run the same
migrations, baseline seeds, shortcut seed, and rolling window command. Avoid
absolute local paths and keep all writes tenant-scoped.
