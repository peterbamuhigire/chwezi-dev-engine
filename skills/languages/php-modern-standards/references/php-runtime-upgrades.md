# PHP Runtime Compatibility and Upgrade Workflow

**Parent skill:** [php-modern-standards](../SKILL.md)
**Use with:** the operations engine's `linux-webstack` skill for host/package/service changes. This reference governs application compatibility and release evidence; it does not authorise production mutation.

## Purpose and boundary

Upgrade an application to a newer PHP minor branch, such as 8.3 to 8.5, without confusing interpreter availability with application compatibility. Patch the currently serving runtime promptly through its OS/vendor security channel; carry out a minor-version migration as a separate staged release. Pin the PHP branch used for development, CI, build, CLI jobs and web runtime.

### Emergency security context (2026-10-21)

The PHP project published two Critical remote-code-execution advisories, CVE-2026-109618 (OOM memory-state corruption) and CVE-2026-109619 (stale worker-global state/use-after-free), each scored 9.2/10 under CVSS 4.0 in the upstream advisories. Treat the release as urgent and patch every externally reachable PHP runtime and long-lived worker. The advisories support calling this a critical emergency security release; they do not support the claim “biggest security vulnerability ever found,” which lacks a defined comparison and evidence.

Vendor-fixed package versions differ from upstream tags. On the publication date, Ubuntu USN-8948-1 listed Noble's fixed PHP 8.3 package `8.3.6-0ubuntu0.24.04.13`; Debian DSA-6574-1 listed Trixie's fixed PHP 8.4 package `8.4.27-1~deb13u1`. Verify current vendor advisories and installed package provenance at execution time.

## 1. Capture the compatibility baseline

Record:

- Current and target PHP versions, framework version and support statements.
- `composer.json`, `composer.lock`, root and transitive dependency constraints, PHP extensions and versions.
- `config.platform.php` and Composer version; distinguish simulated platform declarations from the actual interpreter.
- CLI, FPM/Apache/CGI, worker, scheduler and container runtimes; `php --ini`, loaded modules and relevant INI settings.
- Build/test commands, coverage, static-analysis baselines, application health checks, traffic/error baselines and rollback handler.

Do not infer the web PHP runtime from the CLI version. Ask the operations owner to map every vhost, worker and container to its actual binary/handler. Treat an unknown entry as `NOT ASSESSED`.

## 2. Check dependencies and migration guidance

Run the target PHP binary explicitly in CI/staging and use the committed lockfile first. When Composer is launched through a wrapper, arrange `PATH` so its PHP process resolves to the target CLI, then confirm `php -v` and `composer -V` in that same shell before running these checks:

```bash
composer validate --strict
composer prohibits php 8.5
composer check-platform-reqs
composer audit
```

The exact Composer subcommands/options depend on the installed Composer release; check its official manual. `prohibits` identifies constraints, while `check-platform-reqs` validates the real interpreter/extensions and ignores Composer's `config.platform` simulation. Neither predicts all runtime defects.

Read every PHP migration guide between the current branch and target (for 8.3 → 8.5, include both 8.4 and 8.5 guides), plus framework, extension and library upgrade notes. Search code for removed/deprecated behaviour surfaced by those guides; enable deprecation reporting in a controlled environment. Do not suppress failures with `--ignore-platform-reqs` or silently change dependency versions in production.

## 3. Test in an isolated target runtime

Create staging from a recent, sanitised production copy. Install the target PHP branch side by side using a trusted, maintained source, pin the build/image and match production extensions, INI configuration, services and worker commands. Keep the existing patched branch untouched. Do not make the target CLI the global default merely to make tests pass.

Run, under the explicit target binary:

- unit, integration, contract and end-to-end tests;
- static analysis, coding standards and framework boot/route/cache checks;
- Composer platform checks with required production and development extensions;
- representative web/FPM requests and queue/scheduler jobs;
- error-log/deprecation review, latency and memory comparison.

Exercise authentication and session lifecycle, database transactions/stored procedures, file/PDF/image generation, uploads, HTTP integrations, mail, scheduled reports, retries and idempotency. Use test records for operations that affect stock, accounting, tax or external integrations. Record test commands, result, environment/runtime, failures and fixes; a green test suite alone does not establish production behaviour.

## 4. Resolve compatibility changes reproducibly

If constraints block the target, identify the specific package and supported release. Update only necessary dependencies on a feature branch, review the full `composer.lock` diff, run the full suite and security audit, and deploy the reviewed lockfile. Avoid unrestricted `composer update` during a runtime cutover. Keep `config.platform` aligned with the declared deployment target but remember it does not replace checks against the real interpreter.

If a required extension has no trusted compatible build, or the framework does not support the target, stop the cutover and keep the patched current runtime. Do not install an unverified binary or downgrade below the security-fixed package.

## 5. Release one site at a time

Agree on an owner, maintenance impact, observation window, health indicators and recovery trigger. Operations should configure a separate FPM pool/socket or isolated container for the target and switch one vhost. For a shared Apache `mod_php` setup, plan the handler change explicitly; a global module change may switch unrelated sites.

Before the switch, test web-server and FPM configurations. After it, verify the actual web-executed PHP version/SAPI with a protected, temporary diagnostic or an existing health mechanism, test representative user flows, inspect logs/error rates, and restart long-running workers. Remove temporary diagnostics. Proceed to the next site only after the agreed observation window is healthy.

If a gate fails, route traffic back to the previous **security-patched** handler, retain evidence and investigate. Keep the release artifact, lockfile, config diff and tested recovery steps available. Do not treat an OS-package downgrade to a vulnerable build as rollback.

## 6. Lifecycle and security currency

Check [PHP supported versions](https://www.php.net/supported-versions.php) and the current framework/runtime policy when selecting the target. Record source, access date, support status and recheck date. Upstream lifecycle is not the same as vendor package availability: distributions may backport security fixes or maintain different package versions. Compare the OS vendor's advisory and full package revision for the currently running deployment.

For security advisories, update every public execution surface: web handler, CLI jobs, worker processes and container images. Confirm candidate repository, install the vendor-fixed revision, restart old workers, verify actual serving runtimes and check application health. Application-level authentication does not compensate for a runtime vulnerability reached before application code.

## Currentness record (2026-10-22)

| Claim ID / scope | Source ID; publication/version date | Access / verification date; freshness | Support status; confidence / uncertainty | Owner; review date |
|---|---|---|---|---|
| PHPAPP-001: both CVEs are Critical RCE advisories, CVSS 4.0 9.2/10; “biggest ever” is unsupported as a comparative superlative | PHP-GHSA-001 and PHP-GHSA-002 (Tier 1 primary); published 2026-10-21 | 2026-10-22 / 2026-10-22; incident-specific | Direct upstream project advisories; high confidence for score and impact; SAPI/app reachability varies | PHP skill maintainer; before incident response |
| PHPAPP-002: PHP 8.5 has upstream security support through 31 Dec 2029 at access time | PHP-supported-versions (Tier 1 primary); accessed 2026-10-22 | 2026-10-22 / 2026-10-22; lifecycle-sensitive | Official upstream schedule; high confidence, but OS package/extension availability differs | PHP skill maintainer; before target selection |
| PHPAPP-003: PHP 8.5.12 is the current upstream stable release at access time | PHP-downloads (Tier 1 primary); released 2026-10-21 | 2026-10-22 / 2026-10-22; volatile | Official upstream page; high confidence; vendor package revision may differ | PHP skill maintainer; before staging |
| PHPAPP-004: minor migration guides document backward-incompatible/deprecated changes to test | [PHP-migration-84](https://www.php.net/manual/en/migration84.php) and [PHP-migration-85](https://www.php.net/manual/en/migration85.php) (Tier 1 primary); accessed 2026-10-22 | 2026-10-22 / 2026-10-22; versioned manuals | Official guidance; high confidence; inspect all intervening branches and framework/extensions | PHP skill maintainer; before each migration |
| PHPAPP-005: Composer `check-platform-reqs` validates real PHP/extensions instead of `config.platform` | Composer-CLI (Tier 1 primary); accessed 2026-10-22 | 2026-10-22 / 2026-10-22; tooling-sensitive | Official docs; high confidence; command behavior depends on installed Composer version | PHP skill maintainer; before each migration |
| PHPAPP-006: Ubuntu 24.04 Noble's fixed package revision for the two CVEs is `8.3.6-0ubuntu0.24.04.13` | Ubuntu-USN-8948-1 (Tier 1 primary); published 2026-10-21 | 2026-10-22 / 2026-10-22; release-specific and time-sensitive | Canonical advisory; high confidence; check host's package origin and installed branch | Linux package maintainer; before patching |
| PHPAPP-007: Debian 13 Trixie's fixed package revision for the two CVEs is `8.4.27-1~deb13u1` | Debian-DSA-6574-1 (Tier 1 primary); published 2026-10-21 | 2026-10-22 / 2026-10-22; release-specific and time-sensitive | Debian Security Team advisory; high confidence; check host's package origin and installed branch | Linux package maintainer; before patching |
| PHPAPP-008: the upstream PHP fix is the complete mitigation; configuration workarounds are partial | PHP-GHSA-001 and PHP-GHSA-002 (Tier 1 primary); published 2026-10-21 | 2026-10-22 / 2026-10-22; incident-specific | Direct PHP project advisories; high confidence; mitigation coverage varies by exact exploit path | PHP security maintainer; before relying on an interim measure |

Ubuntu-specific example, not a universal requirement: [USN-8948-1](https://ubuntu.com/security/notices/USN-8948-1), published 2026-10-21, lists Ubuntu Noble's fixed PHP 8.3 package revision and separate PHP 8.5 package revisions for newer Ubuntu releases. This does not establish PHP 8.5 package availability on another OS or repository.

Debian-specific example, not a universal requirement: [DSA-6574-1](https://lists.debian.org/debian-security-announce/2026/msg00489.html), published 2026-10-21, fixes the same CVEs in Debian 13's `php8.4` package at `8.4.27-1~deb13u1`.

Interim INI workarounds in the upstream advisories are incomplete and context-specific. Use them only after reading the advisory and with operations approval; do not treat unlimited PHP memory as a safe shared-host default. Removing exposure from the public network while patching is preferable when an urgent package cannot be installed.

## Sources and limits

Digital Research Engine source-evaluation/source-verification skills and Kaizen currentness gate were retrieved from the canonical public repository on 2026-10-22 because the local checkout was unavailable. Sources were opened and the cited claims were checked against primary publisher text. Claim/source/date/freshness/support/uncertainty evidence is recorded above; source-tier metadata-manifest replay and local-engine execution remain `NOT ASSESSED`. No target application was upgraded as part of this procedure.
