# Solution-selection benchmark fixtures

`fixtures.json` is the original 16-case specification from the Kaizen protocol:
12 representative engineering cases plus four counterexamples. It covers
reuse, native controls, mature dependencies, new features, cross-component
bugs, refactoring, API validation, authentication/authorisation,
accessibility, migrations, asynchronous retry, money invariants, and cases
where native controls, compact code, or fewer dependencies are unsafe.

Each fixture carries a `short_prompt`: the doctrine in one sentence, written
from the title and public task rather than the oracles. It drives the
short-prompt control arm, which asks whether the skill beats one sentence.

Validate the specification without invoking a model:

```powershell
python -X utf8 tools/validate_benchmark_fixtures.py
python -X utf8 tools/validate_benchmark_fixtures.py --verify-commits
```

## Materialised fixtures (M10-05)

`materialised/Fxx/` holds, per fixture, `fixture.json`, `starter/` (the
repository the agent receives), `public_tests/`, a stdlib-only `checker.py`
that runs the produced code against adversarial input, and two overlays:
`reference_good/` (a correct solution) and `reference_bad/` (a plausible, lazy
solution that passes the happy path). `materialised/fixture_kit.py` composes a
workspace and computes `initial_commit`, a reproducible "fixture baseline"
commit of starter plus public tests (fixed identity and date, user git config
excluded). Withheld tests are kept outside version control in
`benchmarks-private/solution-selection/Fxx/` (that folder ignores itself); only
their `hidden_manifest_hash` is committed.

Prove that every checker can fail before any model is run:

```powershell
python -X utf8 benchmarks/solution-selection/materialised/run_selftests.py
python -X utf8 benchmarks/solution-selection/materialised/fixture_kit.py stamp --check
```

A self-test passes only when the checker passes `reference_good` and fails
`reference_bad` (discipline adapted from DietrichGebert/ponytail, MIT,
https://github.com/DietrichGebert/ponytail, commit e3ba2aa; paraphrased).

## Execution status

Execution runs through `chwezi-engine-agents/scripts/run_behavioural_eval.py
--suite solution-selection` (16 fixtures × baseline, engine and short-prompt
arms × n=3, one pinned model) and emits evidence that
`tools/solution_evidence.py validate` accepts. Under the zero-spend rule (29 Sep
2026) no model-executed cell has run: every cell is `NOT_ASSESSED (zero-spend
rule)` and scores 0. A materialised fixture is harness evidence, not a result.

## Reporting improvement claims

Any efficiency, savings or quality-delta claim drawn from this benchmark states
its evidence rung, is never summed across rungs and lists its confounders, per
the evidence-rung rule in digital-research-engine
`skills/ai-evaluation-and-data-flywheel/references/eval-flywheel.md`
("Evidence rungs for improvement claims"). A matched-arm run of these fixtures
on one pinned model is a `controlled_holdout`; a checker re-run on the same
workspace is a `deterministic_remeasure`.

`pressure-scenarios.json` (and the `pressure_scenarios` array in
`fixtures.json`) holds the pressure-scenario case type for discipline gates
(M10-04-T05, extended in M10-05-T08).
