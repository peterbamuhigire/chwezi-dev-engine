# Retrofit and rollout

Parent skill: [tenant-document-numbering](../SKILL.md). Self-contained; distilled from
the owner's numbering standard (5 Nov 2026) and the Maduuka reference plan
(`04-production-rollout.md` and `02-kaizen-findings.md`).

Goal: existing tenants notice only that new documents follow the new series. Every
historical number, total, stock figure and ledger line is unchanged.

## 1. Promises and their proofs

| Promise | How it is kept | How it is proved |
|---|---|---|
| No historical number changes | No migration runs `UPDATE` on a non-empty number column. New columns are backfilled only with the number the row already displayed (for example `PO-{id}` when the screen showed that). | Checksum of `(id, number, status, amount)` per tenant and registry table before and after; identical for existing columns, equal to the old display string for new ones |
| No totals, stock or ledger change | Numbering migrations touch no amount, quantity, status or date column | Same checksum over invoices, journals and stock movements |
| Nothing a user does fails | Counters seeded before any switch-on; probe and retry handle clashes; a failed unique-key creation is skipped and reported | Rehearsal on a production copy; endpoint error rates after each switch-on |
| Old numbers still found | Search reads the stored column, which the backfill filled with the old display string | Search tests with sampled real old numbers |
| Old app builds keep working | API responses only add fields | Contract fixtures; an old build against the new server |

## 2. Order of operations

1. Deploy the code with every per-type switch off. Legacy generators continue.
2. Run schema migrations: counter tables, new nullable number and idempotency columns,
   widening to `VARCHAR(40)`, batched backfills (for example 5,000 rows per batch with a
   resumable watermark). Use `ALGORITHM=INSTANT` or `INPLACE` where the engine allows,
   and fail rather than silently copy a large table.
3. Audit duplicates per table and record them. Add unique keys only where there are
   none (section 3).
4. Seed every counter for every real tenant and type with `GREATEST(last_number,
   seed)`. Re-running is harmless.
5. Switch on one type at a time, lowest risk first: internal counts, adjustments and
   transfers; purchasing; hospitality; money and ledger; pharmacy or other verticals;
   restaurant; POS sales and credit notes; platform invoices. Reseed the type
   immediately before the switch, and again after the switch cache has expired on every
   worker, to catch numbers the legacy generator wrote in the window.
6. Watch each group for 72 hours: clash skips, retry and exhaustion counts, counter lock
   waits, the gap report, endpoint error rates, support tickets mentioning numbers.
7. Retire legacy generators once every type has run 14 days with no gap and no clash
   failure. Drop dead procedures and triggers in the same step.

## 3. Safe unique-key migration (MySQL 8, idempotent)

MySQL has no `ADD UNIQUE KEY IF NOT EXISTS`; guard with `INFORMATION_SCHEMA`.

```sql
SET @has_uk := (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS
                 WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'purchase_orders'
                   AND INDEX_NAME = 'uk_po_number');
SET @dupes := (SELECT COUNT(*) FROM (SELECT tenant_id, po_number FROM purchase_orders
                 WHERE po_number IS NOT NULL AND po_number <> ''
                 GROUP BY tenant_id, po_number HAVING COUNT(*) > 1) d);
-- record each duplicate in the numbering audit table (guarded with NOT EXISTS so re-runs do not repeat it)
SET @sql := IF(@has_uk = 0 AND @dupes = 0,
  'ALTER TABLE purchase_orders ADD UNIQUE KEY uk_po_number (tenant_id, po_number)',
  'SELECT ''uk_po_number skipped: present or duplicates recorded''');
PREPARE s FROM @sql; EXECUTE s; DEALLOCATE PREPARE s;
```

PostgreSQL: `CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS ...` after the same
duplicate audit; a failed concurrent build leaves an invalid index to drop and retry.

- Duplicates never stop the rollout. They are history, stay untouched, are reported to
  the platform team, and the key is added later once a person has resolved them.
- Exclude `''` and NULL from the duplicate check; backfill `''` with the displayed
  string first.

## 4. Format changes and counters

- A type that keeps its format continues after its highest existing number.
- A type whose format changes gets a new counter key (`folio_v2`). The old row stays for
  rollback and history. A counter is never lowered or reset.
- Old numbers that embed internal ids stay as they are; new formats do not embed ids.

## 5. Rehearsal gate

Restore a production backup to a non-production environment, run steps 1 to 5 with
every switch on, replay a realistic peak (concurrency script at the measured till
count), and record migration time per table, duplicate audit, sampled seeds, checksum
comparison, gap report, p95 counter wait and errors per endpoint. Gate: checksums
identical, gap report empty, no new error type, lock wait within target. A failure
blocks production until fixed and rehearsed again.

## 6. Rollback

| Situation | Action | Effect on numbers |
|---|---|---|
| One type misbehaves | Switch that type off; the legacy generator resumes | Probe or unique key prevents duplicates; any gap while off is reported; reseed before switching on again |
| Whole release misbehaves | All switches off; redeploy the previous build if needed | Schema changes are additive, so old code runs; counters keep their high-water mark |
| Migration fails half-way | Fix and re-run; backfills resume from their watermark | None |

Counters only go up, so no rollback path can issue a number twice.

## 7. Telling clients

One plain sentence in the release notes and a short in-app notice, approved by the
owner, for example: "Document numbers now run in order. Every new invoice, receipt and
order gets the next number in its own series. Your earlier documents keep their
numbers."
