# PHP security and runtime upgrades — 2026-10-22

## Change

The PHP standards skill now links to an application-focused runtime migration guide. It separates emergency vendor security patching from minor-version migration, checks Composer constraints and the real target interpreter, includes the intervening 8.4/8.5 migration guides, tests extensions/framework/application behaviour in staging, and hands host/package/handler changes to `linux-webstack`.

The Linux skills engine owns OS packages, repositories, service restarts, request-path verification and site cutover. The PHP engineering skill owns compatibility evidence, code/dependency remediation and release acceptance. A web page passing is not proof that a queue, cron process or container uses the same PHP runtime.

## Security event

The PHP project published GHSA-w8hw-w9fx-j79w / CVE-2026-109618 (OOM-related memory-state corruption) and GHSA-6wmf-4rv5-p3rp / CVE-2026-109619 (stale worker state/use-after-free) on 2026-10-21. Each is rated Critical at CVSS 4.0 9.2/10 in the PHP project advisory. The threat warrants emergency patch priority across public PHP handlers and long-running workers. The claim “biggest security vulnerability ever found” is not included: no comparison set or supporting source establishes that superlative.

## Currentness evidence

| Claim ID | Source ID / publication date | Scope | Access / verification | Freshness / support / confidence | Uncertainty / review date |
|---|---|---|---|---|---|
| PHPAPP-001 | PHP-GHSA-001 + PHP-GHSA-002 / 2026-10-21 | Both vulnerabilities' CVSS 4.0 severity and RCE impact | 2026-10-22 / 2026-10-22 | Incident-specific; supported; high confidence | SAPI and app reachability vary; recheck during response |
| PHPAPP-002 | Ubuntu-USN-8948-1 / 2026-10-21 | Ubuntu Noble fixed PHP package revision | 2026-10-22 / 2026-10-22 | Time-sensitive; supported; high confidence | Verify exact host and repository before patch |
| PHPAPP-003 | Debian-DSA-6574-1 / 2026-10-21 | Debian Trixie fixed PHP package revision | 2026-10-22 / 2026-10-22 | Time-sensitive; supported; high confidence | Verify exact host and repository before patch |
| PHPAPP-004 | PHP-supported-versions / accessed 2026-10-22 | Upstream PHP 8.5 lifecycle | 2026-10-22 / 2026-10-22 | Lifecycle-sensitive; supported; high confidence | Recheck before target selection; distro support differs |
| PHPAPP-005 | PHP-downloads / released 2026-10-21 | Upstream PHP 8.5.12 version | 2026-10-22 / 2026-10-22 | Volatile; supported; high confidence | Recheck exact release/package before staging |
| PHPAPP-006 | PHP migration guides 8.4/8.5 / accessed 2026-10-22 | Incompatibilities and deprecated behaviour across minor versions | 2026-10-22 / 2026-10-22 | Versioned manuals; supported; high confidence | Read all intervening guides before each migration |
| PHPAPP-007 | Composer CLI manual / accessed 2026-10-22 | `check-platform-reqs` validates actual PHP/extensions | 2026-10-22 / 2026-10-22 | Tool-version dependent; supported; high confidence | Verify installed Composer and run under target PHP |

Primary references: [PHP OOM advisory](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w), [PHP stale-global-state advisory](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp), [Ubuntu USN-8948-1](https://ubuntu.com/security/notices/USN-8948-1), [Debian DSA-6574-1](https://lists.debian.org/debian-security-announce/2026/msg00489.html), [PHP supported versions](https://www.php.net/supported-versions.php), [PHP downloads](https://www.php.net/downloads.php), [PHP migration 8.4](https://www.php.net/manual/en/migration84.php), [PHP migration 8.5](https://www.php.net/manual/en/migration85.php), [Composer CLI](https://getcomposer.org/doc/03-cli.md).

The local Digital Research checkout was unavailable. Its canonical public source-evaluation, source-verification and currentness-gate instructions were retrieved on 2026-10-22; primary source content and version claims were checked directly. Source-tier metadata-manifest replay and local engine execution remain `NOT ASSESSED`. The “biggest ever” comparison remains unsupported.

## Follow-up and limits

- Recheck volatile PHP support, package availability, migration and Composer guidance before applying it to a project.
- No PHP application was migrated in this work; application-level PHP 8.5 compatibility remains `NOT ASSESSED` until a project runs the staged checks.
- This update adds guidance, not a runtime package or executable installer.
- Model-policy currentness was checked for this Kaizen. No model-policy change was proposed; account-level access and comparative model quality/latency evidence were not evaluated for this PHP work.
