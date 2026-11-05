# Seeding, clashes and capacity

Parent skill: [tenant-document-numbering](../SKILL.md). Self-contained; distilled from
the owner's numbering standard (5 Nov 2026) and the Maduuka reference plan
(`03-architecture.md` sections 4, 5 and 11, and `07-capacity-and-field-sizing.md`).

## 1. Seeding the counter

The seed is the highest numeric part of numbers that match the type's own pattern, over
every table in the type's series, for that tenant.

```sql
-- MySQL 8: type PO-{n}, pattern ^PO-[0-9]+$
SELECT COALESCE(MAX(CAST(SUBSTRING(po_number, 4) AS UNSIGNED)), 0) AS seed
  FROM purchase_orders
 WHERE tenant_id = ? AND po_number REGEXP '^PO-[0-9]+$';

-- PostgreSQL
SELECT COALESCE(MAX(substring(po_number FROM '^PO-([0-9]+)$')::bigint), 0) AS seed
  FROM purchase_orders
 WHERE tenant_id = $1 AND po_number ~ '^PO-[0-9]+$';
```

Rules:

- **Never seed from `COUNT(*)`.** Counts include other formats, platform rows and
  deleted history, so they jump the series ahead and open a gap on day one.
- Seed only from the type's own tables. Probing or seeding from tables outside the
  series skips numbers for no reason.
- Apply the seed with `GREATEST(last_number, seed)`. A counter only ever goes up, so
  re-running the seeder is harmless and no issued number can be reissued.
- A label-bearing format (`JE-{yyyy}-{n}`) seeds from the highest counter whatever the
  label.
- A new format whose old numbers do not match the new pattern seeds at 0 under a **new
  type key**. Old and new numbers cannot collide because they have different shapes.
- Record `seeded_from` and `seeded_at` on the counter row for the evidence trail.
- When: in the rollout migration for every real tenant and type; lazily the first time a
  tenant uses a type; and again when a type's switch is turned back on.

## 2. Clash handling, three layers

| Layer | Catches | Behaviour |
|---|---|---|
| Seed past what exists | Normal running | Next number is always above every existing one |
| Probe under the counter lock | Numbers written after seeding by imports, legacy code still on, manual repairs | Step to the next free number; log `numbering.clash_skipped`. The skipped number belongs to an existing document of the same type, so the series has no gap. |
| `UNIQUE (tenant_id, number)` | A writer that bypassed the allocator between probe and insert | Duplicate-key error; roll back the whole transaction (which undoes the counter update), retry once; a second clash fails with "Nothing was saved. Please try again." and logs both candidates |

Cross-type clashes are prevented by distinct prefixes per type and by the registry
validator rejecting overlapping patterns in one table.

## 3. Column widths

- Every number column, and every column that copies a number (void audit, stock-movement
  reference, payment reference, gap records), is at least `VARCHAR(40)`.
- Why 40: the longest fixed text plus the longest counter. A 64-bit signed counter has
  at most 19 digits (`PHP_INT_MAX`, Kotlin `Long.MAX_VALUE`), so a 12-character prefix
  such as `SAL-YYYY-MM-` plus 19 digits is 31, with room to spare. The registry validator
  enforces `len(fixed text) + 19 <= 40` for every type.
- Widening from 20 or 32 to 40 on `utf8mb4` keeps a 1-byte length prefix (up to 63
  characters), so MySQL can do it in place. State `ALGORITHM=INPLACE, LOCK=NONE` so the
  migration errors instead of silently copying a large table; verify on the target
  version before production.
- Never shrink a column that is already wider.
- Keep the table's existing collation; mixing collations on joined columns causes
  errors.
- `idempotency_key` columns are `VARCHAR(100)`.

## 4. Padding by volume

The counter grows past its padding automatically (`PO-999999` is followed by
`PO-1000000`). Padding only decides how long numbers stay one width.

| Volume class | Examples | Padding | Room before width changes |
|---|---|---|---|
| Very high, per sale or ticket | invoice, receipt, credit note, kitchen ticket, order, journal entry | 8 | 100 million |
| Daily operations | expense, deposit, withdrawal, transfer, goods receipt, adjustment | 6 | 1 million |
| Lower | everything else | 6 | 1 million |

An existing type that keeps its format keeps its padding.

## 5. Sorting

- Never `ORDER BY` the number string alone: `PO-1000000` sorts before `PO-999999`, and
  labels change with dates and renames.
- Lists and reports sort by issue timestamp, then id, on an index such as
  `(tenant_id, issued_at, id)`.
- A "sort by number" option within one type uses `ORDER BY CHAR_LENGTH(col), col`
  (PostgreSQL `length(col), col`).
- Do not add a parallel numeric sequence column to every table for sorting; it adds a
  second unique index to the hottest write path.

## 6. Query cost at scale

| Query | Index | Cost at 100 million rows per tenant |
|---|---|---|
| Probe `WHERE tenant_id=? AND number=?` | the number unique key | One B-tree lookup |
| Counter lock | counter primary key | One row |
| Idempotency lookup | `(tenant_id, idempotency_key)` unique key | One lookup |
| Search by number | number unique key, equality or prefix | No leading-wildcard `LIKE '%123'` on large tables |
| Seeding | tenant slice of the number key | Linear; off-peak, never on a user path |
| Gap report | range above the watermark | Must be incremental (below) |

## 7. Incremental gap and duplicate report

```text
for each enabled type and tenant:
  from = max(seeded_from, gap_checked_through)       # history before the seed is not judged
  to   = last_number minus a settling margin for in-flight transactions
  counters = parse(numbers in t.tables matching t.pattern with counter in (from, to])
  report missing values (gaps), values used more than once (duplicates),
         and values above last_number (a writer outside the allocator: reseed)
  write findings to the numbering audit table and alert channel
  gap_checked_through = to
```

A full re-scan is a manual flag for investigations, never the nightly job.

## 8. Throughput

One counter row per tenant and type serialises that type's allocations; the lock is
held until the save commits. Measure p95 counter wait at the tenant's real peak of
concurrent writers (for example 40 tills) and set a gate (the reference plan uses
p95 <= 50 ms and 5 times the peak rate). If it fails, shorten the work between the
allocation and commit. Per-branch counters and allocation outside the transaction are
not remedies: both break the standard.
