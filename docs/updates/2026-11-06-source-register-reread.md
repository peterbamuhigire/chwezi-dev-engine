# Source register re-read, 5 and 6 November 2026

The source-register check began failing on 2026-11-04. On 2026-11-06 it exited 1 with 14 findings: five Next.js records with `review_after` 2026-11-03 and nine Android, Kotlin, PHP, PostgreSQL and MySQL records with `review_after` 2026-11-05. This record holds what was re-read, what each page now says, and what changed. No date was extended unread.

## Method

Each record's primary page was fetched with `curl` between 22:11 and 22:13 UTC on 2026-11-05 (01:11 to 01:13 on 6 November in East Africa), by three read-only workers, one per group. The dispatcher then checked the key findings against the primary pages again: the GitHub API's latest stable Next.js release and the November Next.js security post, the Android November bulletin, the AGP index redirect, the Compose BOM page, the PHP news archive and the Oracle October 2026 alert. The MySQL page was retried by the dispatcher with two user agents.

Record dates (`accessed`, `verified_at`, `as_of`) use the UTC date, 2026-11-05, so that a CI run in UTC never sees a future date. Exact times are in each `reverification_note`. Review dates follow the cadence: security advisories and bulletins 2026-11-13, releases, setup and migration pages 2026-11-20.

## Outcome for each record

| Record | What the page says now | Action |
|---|---|---|
| `nextjs-release-2026-10-29` | v16.4.5, published 2026-11-03, is the latest stable release (v16.4.3 is not) | Superseded by `nextjs-release-2026-11-05` |
| `next-security-november-notice-2026` | The planned release shipped on 2026-11-03: one High and six Medium advisories, fixed in v16.4.5 and v15.5.29 | Superseded by `next-security-november-2026-release-2026-11-05` |
| `next16-upgrade-2026-10-29` | Unchanged; page revision 2026-10-15 | Renewed in place, `revision_date` added |
| `nextjs-support-policy-2026-10-29` | Unchanged: 16.x Active LTS, 15.x Maintenance LTS | Renewed in place |
| `next-security-oct14-2026` | Unchanged; its uncertainty text now points at the November release | Renewed in place |
| `android-security-bulletin-october-2026` | Page unchanged apart from a 2026-10-08 revision; the November bulletin (published 2026-11-02, patch level 2026-11-05) is now the latest | Superseded by `android-security-bulletin-november-2026` |
| `android-agp-9-1-notes-2026-10-29` | The AGP index now redirects to AGP 9.5.0 (October 2026): Gradle 9.6.0 and JDK 17 minimum, API 37 | Superseded by `android-agp-9-5-notes-2026-11-05` |
| `android-17-release-2026-10-29` | Unchanged: API level 37, 2026-06-16 | Renewed in place |
| `compose-setup-2026-10-29` | Unchanged: latest Compose BOM 2026.09.00, page last updated 2026-10-28 | Renewed in place |
| `kotlin-compose-migration-2026-10-29` | Unchanged; page footer 12 August 2026 | Renewed in place, `revision_date` added |
| `php-security-oct21-2026` | Unchanged: CVE-2026-109618 and CVE-2026-109619, fixed in 8.5.12, 8.4.27, 8.3.36 and 8.2.35; nothing newer in those branches | Renewed in place |
| `php-windows-brotli-2026` | Unchanged: builds 8.5.12-1, 8.4.27-1, 8.3.36-1, 8.2.35-1, Brotli 1.2.1 | Renewed in place |
| `postgresql-security-2026-10-29` | Unchanged: CVE-2026-19385 is the newest row, fixed in 18.6, 17.11, 16.15, 15.19 and 14.24 | Renewed in place |
| `mysql-8413-security-2026-10-29` | **Unreadable.** The MySQL documentation site returns HTTP 403 ("Technical Difficulties") to every attempt | Quarantined (`NOT_ASSESSED`), reverify by 2026-11-13 |

## Added records

- `oracle-cpu-oct-2026-mysql-2026-11-05`: the Oracle October 2026 Critical Patch Update advisory, which was readable. Its MySQL rows list Server 8.4.0 to 8.4.12 as affected, so 8.4.13 is outside the listed range. It does not name 8.4.13 as the fix, states no publication date and is not the release notes. It replaces the quarantined record in `claim-database-currentness-security-2026-10-29`.
- `php-session-upload-progress-advisory-2026-11-05`: the PHP informational advisory of 2026-10-23 (CVE-2026-115560, full advisory to follow). Added to `claim-php-runtime-security-currentness-2026-10-29`.

## Claims

Six claims now name the new ids: the Next.js currentness and auth-boundary claim, the Next.js security advisory claim, the runtime support claim, the Android claim, the PHP runtime security claim and the database security claim. `check_source_register.py` rejects a claim that names a superseded or quarantined source, and exits 0.

## Skill text updated

- `skills/frontend-ux/nextjs-app-router/references/tenant-data-security.md`: the upgrade guide's access date and revision; a source entry for the November release naming the High-severity cross-tenant cache disclosure when `unstable_cache` and `use cache` are combined.
- `skills/android/android-development/SKILL.md`: the version and security currency snapshot is dated 2026-11-05 and names AGP 9.5.0; Kotlin 2.4.21 is labelled as from the earlier snapshot and not re-read.
- `skills/languages/php-modern-standards/references/php-runtime-upgrades.md`: a dated note that PHPAPP-003 still holds and that a separate informational advisory exists.

## Checks (2026-11-06, Linux, Python 3.14.10)

| Check | Before | After |
|---|---|---|
| `check_source_register.py` | exit 1, 14 findings | exit 0: 73 active sources, 0 findings, 16 warnings |
| Date-gate calendar | rows out of date | 12 rows recomputed; each verified with `--as-of` on its first failing date and the day before |

## Deliberate README correction

The README's date-gate example command was `python3 -X utf8 scripts/check_source_register.py --as-of 2026-11-04`, the first failing date of the old first row. That row no longer exists: the five Next.js records it covered were renewed or superseded. The example is now `--as-of 2026-11-14`, the first failing date of the new second row. `check_readme_preservation.py` reports the old command as lost; this is a deliberate correction, not a loss.

## Not assessed

- The MySQL 8.4.13 release date and security notes (page unreadable).
- Which of the seven November Next.js advisories apply to which version: the vendor post and the GitHub advisory pages disagree on severity and patched versions, and the post was treated as authoritative for fixed versions.
- Whether AGP 9.5.0 carries an explicit "stable" label; it is treated as current because the official AGP index redirects to it.
- The Ubuntu and Debian PHP package revisions (PHPAPP-006 and PHPAPP-007).

## Observations, not acted on

- `build-configuration.md` in the Android skill carries undated example values (compileSdk 35, AGP 8.13.2, Compose BOM 2025.01.01, Kotlin 2.1.0) and still applies `kotlin.android`, which the Kotlin guide says AGP 9.0.0 and later no longer need. They are examples, outside the 14 records.
- `postgresql-support-2026-10-29` (not overdue) will go stale after 2026-11-12, when the PostgreSQL versioning page lists PostgreSQL 14's final release.
- `mysql-84-release-index-2026-10-31` (not overdue) could not be re-read today either, because the same site returns HTTP 403.
