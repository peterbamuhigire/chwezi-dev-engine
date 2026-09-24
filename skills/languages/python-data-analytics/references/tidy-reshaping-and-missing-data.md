# Tidy Reshaping, Assembly, Type Repair, and Missing Data

Load when raw data arrives wide, split across many files, typed wrongly, or full of gaps, and must become an analysis-ready frame: survey exports, mobile-money statements, district-level spreadsheets, sensor dumps, or partner CSVs. Assumes pandas 3.0 (see `pandas-idioms.md`).

## Inputs

| Input | Why it matters | If absent |
| --- | --- | --- |
| Grain statement ("one row = one X per Y") | Decides every reshape | Write it before touching the data; stop if the owner cannot confirm it |
| Data dictionary or column samples | Reveals variables hidden in headers | Profile with `df.head()`, `df.dtypes`, `df.nunique()` |
| Expected row counts / control totals | Proves joins and concats are lossless | Mark reconciliation `NOT_ASSESSED` in the output |
| Missing-value codes used by the source (`""`, `-`, `N/A`, `999`, `0`) | Stops sentinels poisoning statistics | Ask; never guess that 0 means missing |

## The tidy target

A frame is analysis-ready when each variable is one column, each observation is one row, and each kind of observational unit is its own table. Most messy data breaks one of five ways; each has one fix:

| Symptom | Example | Fix |
| --- | --- | --- |
| Column headers are values | `jan_2026, feb_2026, ...` | `melt` to long (`id_vars` = identifiers) |
| One header encodes several variables | `cases_wakiso`, `deaths_gulu` | `melt`, then `str.split(..., expand=True)` into separate columns |
| A column holds variable names | `metric` column with `revenue`/`units` | `pivot_table` back to wide on that column |
| Several units in one table | customer attributes repeated on every order row | split into two tables keyed by `customer_id` |
| One unit spread over many files | one CSV per district per month | read each, tag with source, `concat` once |

```python
# Wide district sales -> tidy long, then split an encoded header
long = (
    wide.melt(id_vars=["district"], var_name="measure_period", value_name="value")
        .assign(
            measure=lambda d: d["measure_period"].str.split("_", n=1).str[0],
            period=lambda d: pd.PeriodIndex(d["measure_period"].str.split("_", n=1).str[1], freq="M"),
        )
        .drop(columns="measure_period")
)
tidy = long.pivot_table(index=["district", "period"], columns="measure",
                        values="value", aggfunc="sum").reset_index()
```

Decision rules:

- Reshape **long** for storage, grouping, plotting libraries and models; reshape **wide** only for human-facing tables and model feature matrices.
- `pivot` fails loudly on duplicate keys; `pivot_table` silently aggregates. Use `pivot` when duplicates would be a data error, and `pivot_table` with an explicit `aggfunc` only when aggregation is intended.
- After `melt`, re-type the value column; melting mixed columns produces an object/str column.

## Assembling many files

```python
from pathlib import Path

frames = [
    pd.read_csv(path, dtype=SCHEMA).assign(source_file=path.name)
    for path in sorted(Path("raw/district_returns").glob("*.csv"))
]
returns = pd.concat(frames, ignore_index=True)
assert len(returns) == sum(len(f) for f in frames)
```

- Build a list and `concat` once; appending in a loop is quadratic and `DataFrame.append` no longer exists.
- Always tag the source file or batch. When a figure is disputed, lineage is the first question.
- Pass the same `dtype` mapping to every read so one file with a stray text value cannot flip a column's type.
- Column-wise `concat(axis=1)` aligns on the index; misaligned indexes produce silent `NaN` blocks. Prefer `merge` on explicit keys.

## Joins that prove themselves

- Declare cardinality with `validate=` and record row counts before and after. A `many_to_one` left join must return exactly the left row count.
- Use `indicator=True` during development and report the `left_only`/`right_only` counts; unmatched keys are findings, not noise.
- Normalise keys first: strip whitespace, fix case, align types (`"0772..."` string vs integer phone numbers lose the leading zero).

## Type repair

| Problem | Repair | Never |
| --- | --- | --- |
| Numbers with thousands separators or currency text (`"UGX 1,250,000"`) | `str.replace(r"[^\d.\-]", "", regex=True)` then `pd.to_numeric` | `astype(float)` on the raw column |
| Mixed junk in numeric column | `pd.to_numeric(col, errors="coerce")`, then count what became `NaN` and report it | `errors="coerce"` without counting the casualties |
| Integers with gaps | `Int64` (nullable) | leave as float and round later |
| Low-cardinality labels | `category` | category on free text |
| Dates in several formats | parse per known format with `format=`; route failures to a reject table | `dayfirst` guessing on ambiguous dates like `03/04/2026` |

Coercion is a data-loss event. Every `errors="coerce"` must be followed by a count of newly missing values and, above a threshold agreed with the owner (for example 0.5%), a failure rather than a warning.

## Missing data policy

Decide per column, and write the decision down:

1. **Find the real missing values.** Replace source sentinels (`""`, `"-"`, `999`) with `NA` at load via `na_values=`; then `df.isna().sum()` and `value_counts(dropna=False)`.
2. **Ask why it is missing.** Not collected, not applicable, not yet arrived, or lost in a join. Only the first and last are candidates for imputation; "not applicable" is a category, not a gap.
3. **Choose the treatment:**

| Situation | Treatment |
| --- | --- |
| Ordered time series with short gaps | `ffill(limit=n)` or `interpolate(method="time", limit=n)`; never unlimited |
| Aggregates where missing should not count as zero | leave `NaN`; pandas reductions skip it by default (`skipna=True`) |
| Aggregates where missing genuinely means zero (no sales recorded) | `fillna(0)` with a comment citing the business rule |
| Model features | impute inside the model pipeline from training data only (see `python-ml-predictive` data prep) plus a `was_missing` indicator |
| Key or identifier missing | reject the row to a quarantine table |

4. **Report it.** Every analysis output states rows dropped, values imputed and the method. A mean computed after silently dropping 30% of rows is a different number.

## String cleanup

- Use vectorised `.str` methods (`strip`, `lower`, `replace`, `extract`, `split(expand=True)`); regex patterns as raw strings, compiled once when reused.
- `str.extract` with named groups produces typed, named columns in one step: `df["phone"].str.extract(r"^(?:\+?256|0)(?P<network>7[0-9])(?P<number>\d{7})$")`.
- Report the count of values the pattern failed to match; unmatched is a data-quality metric.

## Worked example

A Gulu agricultural cooperative sends one Excel workbook per sub-county with columns `member, maize_kg_2025, maize_kg_2026, beans_kg_2025, beans_kg_2026`, blanks for "did not plant", and `-` for "not recorded". Procedure: read each sheet with `na_values=["-"]` and `keep_default_na=False` so that blanks are preserved as a distinct value, tag `sub_county`, concat, melt to `member, sub_county, crop_year, kg`, split `crop_year` into `crop` and `year`, map blanks to `planted=False` with `kg=0`, leave `-` as `NaN`, and report per sub-county how many records are unrecorded. Acceptance: row count equals members x crops x years; no `NaN` in `member`/`sub_county`; the unrecorded count per sub-county appears in the output note.

## Quality gate

- [ ] Grain statement written and checked (`df.duplicated(subset=keys).sum() == 0`).
- [ ] Row counts reconciled across every concat and merge.
- [ ] Every coercion and dropped row counted and reported.
- [ ] Missing-data treatment documented per column, with the business reason.
- [ ] Output dtypes explicit (no accidental `object` columns).

## Senior vs generic output

Generic: `df.dropna()`, `df.fillna(0)`, `astype(float)` and a chart. Senior: states the grain, reshapes to tidy form, reconciles counts, distinguishes "not applicable" from "not recorded", and ships the data-quality note alongside the numbers.

## Evidence/currentness

Access date 2026-09-24. Behaviour checked against pandas 3.0 release notes (pandas.pydata.org/docs/whatsnew/v3.0.0.html): default `str` dtype, removed offset aliases, CoW. `DataFrame.append` removal dates from pandas 2.0. Exact `na_values`/`keep_default_na` interaction with the new `str` dtype for Excel input: `NOT_ASSESSED`; verify on a sample workbook.

Sources: Chen (2023) *Pandas for Everyone*, 2nd ed.; Wickham (2014) "Tidy Data", *Journal of Statistical Software*; pandas documentation.
