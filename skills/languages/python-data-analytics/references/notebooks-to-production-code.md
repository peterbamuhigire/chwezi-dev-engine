# From Notebook to Maintainable Data Code

Load when exploratory analysis or a model prototype in Jupyter must be rerun, handed over, scheduled, reviewed, or promoted into a service or pipeline; or when reviewing data-science code written by analysts. Pairs with `python-modern-standards` (layout, tooling, pytest) and `python-ml-predictive` (model pipelines).

## Inputs

| Input | If absent |
| --- | --- |
| The notebook(s) and the data they read | Stop; a notebook without its inputs cannot be verified |
| Who will run it next and how often (one-off, monthly report, nightly job, online service) | Ask; this decides how far to promote it |
| The figures or outputs stakeholders already rely on | Treat the current outputs as the regression baseline |

## Decide how far to promote

| Future use | Target form | Minimum bar |
| --- | --- | --- |
| Never rerun (true one-off) | Notebook, outputs cleared or archived with a date | Markdown header stating question, data source, date, conclusion |
| Rerun by the author occasionally | Notebook importing functions from a local package | Restart-and-run-all passes; no hidden state |
| Rerun by others or on a schedule (monthly board pack) | Package module + thin CLI entry point; notebook only for presentation | Tests for transformations; pinned environment; parameters not hard-coded |
| Part of a product (pipeline, API, model) | Package in `src/`, pipeline steps per `python-data-pipelines` / `python-ml-predictive` | Full service standards: types, logging, CI, contracts |

Promotion is triggered by the second rerun, not the tenth. Most "one-off" analyses are rerun.

## Refactoring procedure

1. **Freeze the baseline.** Restart the kernel, run all cells, save the key outputs (row counts, totals, metrics, a sample of predictions) to a baseline file. If run-all fails, fix ordering first; that failure is the most common notebook defect.
2. **Find the pipeline shape.** List the steps as a chain: load -> validate -> clean -> derive features -> analyse/train -> report. Each step becomes a function with an explicit input and output (usually a DataFrame in, DataFrame out). Keep argument lists short; bundle many settings into a typed config object.
3. **Lift, don't rewrite.** Move cells into functions in `src/<package>/` one step at a time, replacing the cell with an import and a call. Re-run and compare to the baseline after each move.
4. **Kill duplication.** Copy-pasted blocks that differ only by file name or column become one parameterised function. Preprocessing used at training and at scoring must be the same function (or the same fitted pipeline object) to prevent training-serving skew.
5. **Remove hidden state.** No reliance on cell execution order, no globals mutated across cells, no paths to someone's Downloads folder. Paths and dates come from parameters or config.
6. **Name things for readers.** `df`, `df2`, `x` become `loans`, `loans_clean`, `features`. Function names say what they return (`monthly_repayment_rate`), not how (`process_data`).
7. **Write the tests the baseline implies.** Small hand-built frames (5-10 rows) per transformation, including edge cases the real data showed: empty groups, missing values, duplicate keys, a leap day, a currency with no decimals (UGX).
8. **Keep the notebook as a client.** It imports the package, calls the steps, and shows charts and commentary. Logic lives in the package.

## Testing data code

- **Transformation tests:** input frame -> expected frame, compared with `pd.testing.assert_frame_equal` (set `check_dtype` deliberately, not by habit).
- **Invariant tests:** properties that must hold for any input: no duplicate keys after a merge, totals preserved through a reshape, probabilities in [0, 1], no future dates in training features.
- **Schema checks at boundaries:** validate columns, dtypes, ranges and nullability when data enters (pandera or a Pydantic row model for small volumes); fail loudly with the offending rows.
- **Regression test:** the frozen baseline from step 1 becomes a test on a committed sample dataset, so refactors cannot silently move a reported figure.
- Do not unit-test pandas itself. Test your business rules.

## Notebook hygiene in a repository

- Strip outputs before commit (`nbstripout` as a git filter or pre-commit hook). Outputs bloat diffs and can leak personal or client data.
- When notebooks need review, pair them with a text representation (`jupytext` percent-format `.py`) so diffs are readable.
- Ruff lints and formats `.ipynb` files by default; keep notebooks inside the same lint gate as the package.
- One notebook per question, named with date and purpose (`2026-09-18-arrears-by-branch.ipynb`), with a first markdown cell: question, data source and extract date, status (exploratory / superseded / final), conclusion.
- Markdown cells explain intent, caveats and decisions; they do not narrate what the next line of code does.

## Documenting experiments

For every modelling or analysis experiment, record where the next person will find it (an experiment tracker such as MLflow, or a dated markdown log in the repo):

- Question and hypothesis, stated before results.
- Data version: source, extract date, filters, row count, and the train/validation/test split (with seed or cut-off date).
- Feature choices, including those tried and rejected, and why.
- Hyperparameters and library versions (the lockfile hash is enough).
- Metrics on the agreed evaluation set, compared with the baseline.
- Decision and next step. Negative results are recorded; they prevent the same dead end being explored twice.

## Documentation levels

| Level | Content | Must stay current with |
| --- | --- | --- |
| Names | Carry meaning without comments | Every rename |
| Comments | Why, caveats, business rules with their source | The line they annotate |
| Docstrings | Purpose, parameters, return, raised errors; one agreed style (Google or NumPy) across the repo | The signature |
| README | What the project does, how to set up (`uv sync`), how to run, where data comes from, who owns it | The entry points |

Stale documentation is worse than none; delete what you will not maintain.

## Worked example

A Kampala microfinance analyst has `arrears_final_v3.ipynb` producing the monthly portfolio-at-risk (PAR30) figure for the board. It reads an export from the core banking system, repeats the same cleaning block for three branches, and hard-codes the month. Promotion: freeze last month's PAR30 per branch as the baseline; lift `load_loans(path)`, `clean_loans(df)`, `par30(df, as_of)` into `src/portfolio/`; replace the three cleaning copies with one function parameterised by branch; add tests for a loan exactly 30 days overdue (boundary), a fully repaid loan, and a restructured loan; expose `uv run portfolio-report --as-of 2026-08-31`. Acceptance: the CLI reproduces the baseline PAR30 per branch to the shilling; the notebook shrinks to imports, one call and the charts.

## Quality gate

- [ ] Restart-and-run-all passes, or the notebook has been retired.
- [ ] Logic lives in importable functions with tests; notebook contains no business rules.
- [ ] Baseline outputs reproduced exactly after refactoring.
- [ ] Parameters (dates, paths, thresholds) are inputs, not literals.
- [ ] Outputs stripped from committed notebooks; no client data in the repo.
- [ ] Experiment record exists for any model or figure a decision depends on.

## Senior vs generic output

Generic: a 90-cell notebook named `final_v3`, globals everywhere, "it works on my machine". Senior: a small package with tested transformations, a one-command rerun, a notebook that only presents, and a recorded experiment trail a successor can pick up.

## Evidence/currentness

Access date 2026-09-24. Ruff notebook linting/formatting default and the `ruff-check` hook from the astral-sh/ruff-pre-commit README. Tool activity via GitHub releases: nbstripout 0.9.1 (2026-02), jupytext 1.19.5 (2026-07), pandera 0.33.1 (2026-09), MLflow 3.16.1 (2026-09). Specific API details of these tools beyond the uses named here: `NOT_ASSESSED`; read their current docs before configuring.

Sources: Nelson (2024) *Software Engineering for Data Scientists* (early release); Chen (2023) *Pandas for Everyone*, 2nd ed.; ruff and pandas documentation.
