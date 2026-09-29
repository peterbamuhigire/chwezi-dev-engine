# Quality-Bar Guard

Load when a project needs a written quality bar, when you are about to change a test threshold,
skip marker, suppression or baseline file, or when a review must decide whether a diff quietly
lowers the bar. The rule is simple: the bar is written once, checks run where they are cheapest,
and measured values only ever move up.

## 1. Write the bar once

Keep one short file in the project (for example `docs/quality-bar.md`) that names every check and
its threshold. Everything else points to it. A bar that lives only in CI configuration is invisible
to the person writing the code; a bar that lives in several places drifts.

| Check | Tool (PHP/MySQL example) | Threshold | Where it runs |
|---|---|---|---|
| Unit and integration tests | PHPUnit or Pest | All pass | Edit loop (changed area), task end (full) |
| Static analysis | PHPStan | Level fixed in `phpstan.neon`; baseline may only shrink | Task end, CI |
| Coding standard | PHP_CodeSniffer or PHP-CS-Fixer | No new violations | Edit loop (pre-commit), CI |
| Coverage | PHPUnit with a driver | Floor in `coverage-baseline.json`; may only rise | CI |
| Mutation score | Infection | Minimum MSI in `infection.json5` for money and authorisation code | CI (nightly or pre-release) |
| Schema safety | Migration dry run on a copy | Runs forward and back | Task end for migrations, CI |

## 2. Place each check by cost

Run a check at the earliest point where it is cheap enough to run every time:

- **Edit loop** (seconds): formatter, linter, the tests for the file you changed.
- **Task end** (a minute or two): full test suite, static analysis, migration dry run.
- **CI** (minutes to hours): coverage, mutation testing, cross-version matrix, security scans.

A slow check pushed into the edit loop gets skipped. A fast check left only in CI wastes a
round trip. Record the placement in the bar file.

## 3. Diff guard: weakening patterns

Review every diff for changes that lower the bar. Each item below needs a stated reason and the
owner's approval in the pull request; "to make CI pass" is not a reason.

Lowered thresholds:

- a smaller coverage floor in `coverage-baseline.json` or in the coverage tool's settings;
- a lower PHPStan level, a lower Infection `minMsi` or `minCoveredMsi`;
- a raised allowed-failures count, or a test job marked "allowed to fail".

Skip markers:

- `markTestSkipped(`, `markTestIncomplete(`, `@group skip` (PHPUnit);
- `.skip(`, `xit(`, `xdescribe(`, `it.todo(`, `test.only(` left in (JavaScript);
- `@pytest.mark.skip`, `pytest.skip(` (Python).

Suppression comments:

- `@phpstan-ignore`, `@phpstan-ignore-next-line`, `@psalm-suppress`;
- `// eslint-disable`, `/* eslint-disable */`, `// @ts-ignore`, `// @ts-expect-error` without a reason;
- `@codeCoverageIgnore`, `@codeCoverageIgnoreStart`, `# pragma: no cover`, `# noqa`.

Baseline growth:

- new entries in `phpstan-baseline.neon` or `psalm-baseline.xml`;
- a regenerated baseline file in the same diff as a code change (it hides new errors);
- removed rows from a mutation or coverage baseline.

A quick way to see them in a diff:

```bash
git diff --unified=0 origin/main... | grep -nE "markTestSkipped|markTestIncomplete|\.skip\(|xit\(|@phpstan-ignore|eslint-disable|@codeCoverageIgnore|pragma: no cover"
git diff --stat origin/main... -- phpstan-baseline.neon coverage-baseline.json infection.json5
```

Treat a hit as a question for the author, not an automatic failure. Some suppressions are right;
all of them need a reason next to them.

## 4. Ratchet upwards only

When a measured value improves (coverage rises, a baseline shrinks, the mutation score climbs),
record the new value as the floor in the same pull request. The next change cannot fall below it.
Never ratchet down to absorb a regression; fix the regression or get an explicit, dated waiver from
the owner in the bar file.

## 5. Worked example: a PHP/MySQL ERP

An anonymised multi-tenant ERP (sales, stock, accounting) carries three guard files:

- `phpstan-baseline.neon` with 412 legacy entries at level 6;
- `coverage-baseline.json` with `{"lines": 61.4, "src/Accounting": 83.0}`;
- `infection.json5` with `minMsi: 70` scoped to `src/Accounting` and `src/Auth`.

A developer under deadline pressure opens a pull request that fixes a VAT rounding bug and also:

1. adds two entries to `phpstan-baseline.neon` for the new `VatCalculator` class;
2. lowers `src/Accounting` in `coverage-baseline.json` from 83.0 to 79.5;
3. adds `markTestSkipped('flaky')` to `PeriodLockTest::testRejectsPostIntoLockedPeriod`.

The guard review says:

- Baseline entries for new code are refused: new code meets the current level. Fix the two errors.
- The coverage floor stays at 83.0. The drop comes from the new class having no tests; add them.
- The skipped test guards a never-simplify safeguard (period locks, see `world-class-engineering`
  "Solution Selection"). It cannot be skipped. If it is flaky, fix the flakiness in this pull
  request or in a linked one that merges first.

After the fix the author's pull request raises `src/Accounting` coverage to 84.2, so the floor
moves to 84.2 in the same change.

## 6. Checklist

- [ ] The project has one quality-bar file, and CI settings point to it.
- [ ] Each check is placed at the cheapest point that still runs every time.
- [ ] The diff has no unexplained threshold change, skip marker, suppression or baseline growth.
- [ ] Improved measurements are recorded as the new floor.
- [ ] Any waiver is dated, owned and written in the bar file.

(Adapted from addyosmani/agent-skills, MIT, https://github.com/addyosmani/agent-skills, commit
`2686b62`. Paraphrased; no text copied.)
