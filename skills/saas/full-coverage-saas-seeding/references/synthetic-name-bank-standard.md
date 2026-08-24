# Synthetic Name-Bank Standard

Use this standard whenever a replayable SaaS demo or system-test seeder needs
human-facing names with more variety than a short hard-coded list.

## Asset contract

Keep four UTF-8 CSV files in the seeder’s demo-data directory:

| File | Required columns | Required rows | Meaning |
|---|---|---:|---|
| `english.csv` | `name` | 100 | English/western family names |
| `arabic.csv` | `name` | 100 | Arabic/Muslim family-name forms |
| `male.csv` | `name,tradition` | 100 | 50 `western` and 50 `arabic` male given names |
| `female.csv` | `name,tradition` | 100 | 50 `western` and 50 `arabic` female given names |

The four files are a selection contract, not a claim that every culture uses
the same first-name/family-name structure. The initial asset set is
transliterated for predictable display and validation. A product may add a
different tradition only through a versioned extension with its own source
register and tests.

## Deterministic selection

1. Derive `gender` and `tradition` from a stable fixture key using a cryptographic hash or an equivalent deterministic function.
2. Select the first name from `male.csv` or `female.csv`, filtering by the selected tradition.
3. Select the surname from `english.csv` for `western` or `arabic.csv` for `arabic`.
4. Record the combined asset checksum in the manifest and run ledger.
5. Keep a collision registry scoped to the target fixture. If a generated full name is already used, advance deterministically and document the collision rule; never call a runtime random function.

## Validation gate

Before any business write, reject a bank when:

- a file is missing, not UTF-8, empty, has the wrong header, or has the wrong row count;
- a name is blank, duplicated case-insensitively, contains fixture markers, or is not suitable for the configured display encoding;
- a gender/tradition bucket is missing or does not have its declared 50 rows;
- the source register and asset checksum are absent from the manifest; or
- the target environment is production or otherwise outside the approved demo boundary.

## Research and fictional-data controls

The initial bank is a researched lexical fixture, not a ranking or a personal
identity dataset. Source notes should distinguish official popularity data
from tertiary name-reference catalogues, record access dates, and avoid claims
that the pool represents a whole population. Every resulting person remains
fictional; do not create national IDs, tax IDs, bank accounts, passports, or
other realistic regulated identifiers from a name bank.

Initial source register:

- [U.S. Social Security Administration popular baby-name data](https://www.ssa.gov/oact/babynames/limits.html?trk=public_post_comment-text)
- [Office for National Statistics surname reference](https://www.ons.gov.uk/aboutus/transparencyandgovernance/freedomofinformationfoi/500mostcommonsurnamesinenglandandwales)
- [Behind the Name Arabic names](https://www.behindthename.com/names/language/arabic)
- [Behind the Name Arabic surnames](https://surnames.behindthename.com/names/language/arabic)

The companion CSV assets in this reference directory are the portable starter
bank. A project may copy them into its own `scripts/database/demo-data/`
directory and must preserve this contract and checksum in its own manifest.
