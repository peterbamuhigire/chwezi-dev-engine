# Validation record

Access date: 2026-10-29. Commands ran in `/home/peter/.claude/skills/skills-web-dev`.
External prep artifacts are under `/tmp/chwezi-portfolio-kaizen/`. Commands below are
the observed run outputs for this cycle; they do not establish production behavior.

## Registered validators

| Command | Result |
|---|---|
| `python scripts/routing_smoke_test.py --lint-fixtures` | Exit 0; `167` active skills, `196` fixtures, precision@1 `177/196 (90.3%)`, precision@3 `196/196 (100.0%)`; `82` owned negatives, `78` pass, `0` fail, `4` `NOT_ASSESSED`; fixture lint `0`, failures `0`. This is a lexical proxy, not live routing. |
| `python -X utf8 scripts/skill_catalog_guardrails.py` | Exit 0; `167` active skills, `14` report-only warnings, `0` errors. Warnings are skill-size observations, not test failures. |
| `python scripts/validate_engine_control_plane.py --workspace-root ..` | Exit 1; registry contains `12` engine entries and parent alias layout reports missing routers for the installed set. This is an environment/path-layout failure, not recorded as a pass. Baseline details: `/tmp/chwezi-portfolio-kaizen/dev-prep/validator-1.log`. |
| `python scripts/validate_engine_control_plane.py --workspace-root /tmp/chwezi-portfolio-kaizen/workspace --engine accounting --engine business-plan --engine chwezi-dev-engine --engine design --engine digital-research --engine linux --engine proposal --engine social-media --engine srs --engine website --engine windows-admin` | Exit 0; registry shape valid and all `11` selected public engine contracts pass. The extra private `political` entry is excluded and `NOT_ASSESSED`; it is not a pass. |

## Automated and runtime checks

| Check | Result |
|---|---|
| `/tmp/linux-kaizen-checks/venv/bin/python -m pytest -q` | `218 passed, 3 skipped`. This includes the repository suite and new packaging/tenant-example tests. |
| `python scripts/validate_tenant_invoice_example.py` | Exit 0; required files and coded tenant/auth/cache invariants found. This is structural evidence. |
| `/tmp/linux-kaizen-checks/venv/bin/python -m pytest -q tests/test_tenant_invoice_example.py tests/test_plugin_packaging.py` | `11 passed`; includes valid cases, missing tenant predicate, role-cookie, lossy BIGINT, invalid-query and missing-review-artifact regressions, package path/shape, count exclusions and an over-cap CLI failure case. |
| `php examples/tenant-invoice-listing/php/test.php` | `15 checks passed`; synthetic PDO SQLite only. It exercises tenant isolation, auth/permission denial, bounds, bound query behavior, HTML escaping, empty result, and no journal mutation. It does not establish MySQL compatibility. |
| `python scripts/check_package_file_budget.py` | Exit 0; checkout `2778` entries including `.git`; package-oriented `2497` entries after documented directory exclusions. Both are at or below the official `5000` archive-entry limit documented in `openai-plugin-submission-errors-2026-10-29`. This is a local inventory, not a generated archive or directory acceptance test. |
| `python -m json.tool docs/source-registers/skills-engine-currentness-2026-09.json` | Exit 0; currentness register parses as JSON. |
| `git diff --check` | Exit 0 at the recorded run. |

The Digital Research metadata validator was also run on the full engine currentness
register. It reports `27` overdue pre-existing source records; these were not silently
renewed because this cycle did not re-verify their claims. A temporary subset containing
the `25` selected cycle sources and `8` matching claims reports zero metadata/date
findings, while explicitly retaining `claim support NOT ASSESSED` in the validator's
meaning. Subset path: `/tmp/chwezi-portfolio-kaizen/dev-prep/dev-cycle-currentness-subset.json`.

The earlier baseline inventory used a separately prepared method and reported `2552`
checkout entries and `2468` package-oriented entries in
`/tmp/chwezi-portfolio-kaizen/packaging-research.md`. The current checker is repository
owned and its exclusion/counting method is documented in
`scripts/check_package_file_budget.py`; the two measurements are not presented as a
before/after trend because the method is not shown to be identical.

## Native discovery and package evidence

The root-provided isolated offline experiment recorded default Codex prompt-input at
`130/165` declared paths, with `35` absent and an approximately `22000`-character
skills-section truncation. The explicit command

```sh
codex -m gpt-6-luna -c model_reasoning_effort="high" -c skills.max_context_tokens=10000 debug prompt-input
```

loaded `165/165` paths with none missing in the measured offline run. The underlying
summary files are outside the repository:
`/tmp/chwezi-portfolio-kaizen/native-discovery/chwezi-dev-engine/summary.json` and
`/tmp/chwezi-portfolio-kaizen/native-discovery-budget/chwezi-dev-engine/summary.json`.
This is invocation evidence for that runtime, not universal host/account behavior.
Official context-budget details are in the source register as
`openai-skills-context-budget-2026-10-29`.

Claude and Codex native installation/load were reported by the orchestrator as passing
in isolated Podman checks without host config mutation. This agent did not independently
repeat those runtime checks; final integration evidence remains with the root reviewer.
Portable package and repo-marketplace manifest shape have local tests. Public directory
submission/acceptance and account-specific availability are `NOT_ASSESSED`.

## Currency, advisories and execution limits

Official currentness records were accessed on 2026-10-29 and are in
[`skills-engine-currentness-2026-09.json`](../../source-registers/skills-engine-currentness-2026-09.json).
Relevant records include:

- [Next.js v16.4.3 release](https://github.com/vercel/next.js/releases/tag/v16.4.3),
  [support policy](https://nextjs.org/support-policy), [version 16 upgrade guide](https://nextjs.org/docs/app/guides/upgrading/version-16),
  [authentication](https://nextjs.org/docs/app/guides/authentication) and
  [data security](https://nextjs.org/docs/app/guides/data-security) records
  (`next16-upgrade-2026-10-29`, `next-authentication-2026-10-29`,
  `next-data-security-2026-10-29`, `nextjs-release-2026-10-29`,
  `nextjs-support-policy-2026-10-29`). The release page listed v16.4.3 as latest stable;
  the support page listed 16.x as Active LTS and 15.x in Maintenance LTS through
  2027-01-31, all as accessed 2026-10-29.
- The [14 October Next.js security update](https://nextjs.org/blog/nextjs-security-update-october-14-2026)
  and [27 October advance notice](https://nextjs.org/blog/upcoming-nextjs-security-release-november-2026).
  The notice announces `7` medium findings for 2026-11-03; at this access date the
  affected versions and fixes were unavailable, so applicability is `NOT_ASSESSED`.
- [PHP security archive](https://www.php.net/archive/2026.php#2026-10-21-5),
  [PHP support table](https://www.php.net/supported-versions.php), and the separate
  [Windows Brotli rebuild notice](https://www.php.net/archive/2026.php#2026-10-26-1).
`php -v` identified the Linux CLI runtime as `8.5.12`, and `php -m` showed PDO SQLite
modules. The Windows rebuild suffix is not evidence about that Linux installation.
- [PostgreSQL version support](https://www.postgresql.org/support/versioning/),
  [PostgreSQL security](https://www.postgresql.org/support/security/), and
  [MySQL 8.4.13 release notes](https://dev.mysql.com/doc/relnotes/mysql/8.4/en/news-8-4-13.html).
  No database package or deployed database was inspected.
- [Android Play target requirements](https://support.google.com/googleplay/android-developer/answer/11926878),
  [Android 17 release](https://developer.android.com/about/versions/17),
  [October 2026 Android Security Bulletin](https://source.android.com/docs/security/bulletin/2026/2026-10-01),
  [Kotlin releases](https://kotlinlang.org/docs/releases.html), and
  [Compose setup](https://developer.android.com/develop/ui/compose/setup).
  The checked records distinguish Play target from compatibility API (synthesis) and do not prove
  a Gradle/AGP combination or that a particular OEM device has applied the bulletin's
  fixes.
- The [OpenAI model catalogue](https://developers.openai.com/api/docs/models),
  [API changelog](https://developers.openai.com/api/docs/changelog), and
  [model-selection guidance](https://developers.openai.com/api/docs/guides/model-selection)
  were checked for the model-policy gate. The changelog records `gpt-6.1-terra` on
  2026-10-26; the catalog lists `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, and
  `gpt-6-luna`. Provider task-positioning is guidance, not an independent comparison.
  The local Codex cache `/home/peter/.codex/models_cache.json` reported fetch time
  `2026-10-29T06:57:01.252184381Z` and all four IDs with `high` reasoning available.
  Decision: retain the authorized `gpt-6-luna` / `high` pin; release recency alone is
  not task-fit evidence. Comparative quality, latency, cost, account entitlement, and
  current-session model are `NOT_ASSESSED`; see external detail in
  `/tmp/chwezi-portfolio-kaizen/packaging-research.md`.

No full Next.js dependency install/build, real DB migration, Android Gradle build or
emulator, deployed security assessment, archive submission, or stakeholder sign-off was
performed. Those states remain `NOT_ASSESSED`.
