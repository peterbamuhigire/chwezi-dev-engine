# Verification Loop (Six-Phase Completion Gate)

Load immediately before claiming a feature, fix, or refactor is complete, before opening a PR,
or at a checkpoint in a long agentic session. It is the mechanical, per-change gate that
produces the evidence `rules/common/verification.md` demands and that the Delivery Definition
of Done pack links to.

Absorbed from the retired `sdlc-meta/verification-loop` skill (origin: adapted from affaan-m/ECC
`skills/verification-loop/SKILL.md`). Command examples are illustrative; use the project's own
scripts and confirm tool flags against the installed versions.

A fixed, ordered gate: build, types, lint, tests, security scan, diff review. Each phase gates
the next. A build failure stops the sequence; type or lint results for code that does not
compile are meaningless.

## How This Differs From `advanced-testing-strategy`

`sdlc-meta/advanced-testing-strategy` answers *what tests should exist* for a given
risk profile — test-layer selection, determinism, contract tests, release evidence
by risk class. It is a design-time framework, consulted while planning coverage.

This skill answers a narrower, later-stage question: *is the work in front of me
right now actually ready to ship*, mechanically, phase by phase, with a fixed report
shape and a single verdict. It assumes the test suite already exists (built per
`advanced-testing-strategy`) and runs it as one gate among six. Use both together:
design coverage with `advanced-testing-strategy`; gate a specific change with this
skill immediately before claiming completion or opening a PR.

This skill also supplies the mechanism that `rules/common/verification.md`'s "a
claim of done requires evidence produced by running something" rule requires you to
produce. The rule states the discipline; this skill is the concrete pipeline that
satisfies it.

## When to Use

- Before stating that a feature, fix, or refactor is complete
- Before opening a PR
- After a nontrivial refactor, before moving to the next task
- At session checkpoints in long-running agentic work (see `rules/common/agentic-engineering.md`
  on 15-minute units — this gate is a natural checkpoint at unit or phase boundaries)

## The Six Phases, in Order

Each phase gates the next. **Do not proceed past a failed phase** except where noted.

### Phase 1: Build

```bash
npm run build 2>&1 | tail -20
# or: pnpm build / composer install --no-dev --dry-run / go build ./...
```

If the build fails, **stop**. Fix the build before running any further phase — type,
lint, and test results are meaningless against code that does not compile or bundle.

### Phase 2: Types

```bash
# TypeScript
npx --no-install tsc --noEmit 2>&1 | head -30
# Python
pyright . 2>&1 | head -30
# PHP (if using a type checker)
vendor/bin/phpstan analyse 2>&1 | head -30
```

Report every type error found. Fix errors that affect the changed surface before
continuing; pre-existing unrelated errors may be noted and deferred, but say so
explicitly rather than silently excluding them.

### Phase 3: Lint

```bash
npm run lint 2>&1 | head -30
ruff check . 2>&1 | head -30
vendor/bin/phpcs 2>&1 | head -30
```

Per `rules/common/coding-style.md` and the agentic-engineering review-focus doctrine:
do not spend review cycles re-litigating style the linter already enforces
mechanically — fix what it flags, move on.

### Phase 4: Tests

```bash
npm run test -- --coverage 2>&1 | tail -50
pytest --cov 2>&1 | tail -50
vendor/bin/phpunit --coverage-text 2>&1 | tail -50
```

Report total / passed / failed / coverage. A failing test blocks the verdict — do
not report NOT READY items as pre-existing without checking whether the current
change caused them.

### Phase 5: Security Scan

```bash
# Secrets and obvious leakage
grep -rn "sk-\|api_key\|api[_-]secret\|password.*=.*['\"]" --include="*.ts" --include="*.js" --include="*.php" --include="*.py" . 2>/dev/null | head -10
# Debug/leftover output
grep -rn "console.log\|dd(\|var_dump\|print(" --include="*.ts" --include="*.tsx" --include="*.php" . 2>/dev/null | head -10
```

For anything beyond this fast local check — dependency CVEs, SAST, `.claude/`
config audit — hand off to `security/security-scanning` or `security/code-safety-scanner`'s
agent-harness config scan mode (audits `.claude/` itself) rather than expanding this phase.

### Phase 6: Diff Review

```bash
git diff --stat
git diff HEAD~1 --name-only
```

Read each changed file's diff (not just the stat) for:
- unintended changes outside the stated scope
- missing error handling on new code paths
- edge cases the tests do not cover

## Output Format

Always produce the report in this fixed shape — do not paraphrase it into prose:

```
VERIFICATION REPORT
====================

Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

`Overall` is READY only if every phase that ran is PASS. If Phase 1 (Build) failed,
report only that phase — the rest are N/A, not skipped-and-hidden.

## Continuous Mode

For long agentic sessions, do not wait until the very end. Run this gate at natural
checkpoints — after each 15-minute unit (`rules/common/agentic-engineering.md`),
after finishing a component, before moving to the next task — rather than only once
before a final PR. Catching a Phase 1 failure early is cheap; catching it after ten
more units have built on top of the broken one is not.


## Relationship to Hooks

This engine's PostToolUse hooks (`hooks/`) catch some of this mechanically and
immediately (e.g. the destructive-bash gate). Hooks are fast and narrow; this skill
is deliberately broader and only runs on request — it is the deeper gate you invoke
before a completion claim, not a replacement for hook-level enforcement.
