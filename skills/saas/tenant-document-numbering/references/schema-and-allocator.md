# Schema and allocator

Parent skill: [tenant-document-numbering](../SKILL.md). Self-contained; distilled from
the owner's numbering standard (5 Nov 2026) and the Maduuka reference plan
(`docs/plans/numbering/03-architecture.md` in that repository).

## 1. Counter tables

One row per (tenant, document type). The platform's own billing uses a second table
with no tenant column.

### MySQL 8

```sql
CREATE TABLE document_counters (
    tenant_id           BIGINT UNSIGNED NOT NULL,
    doc_type            VARCHAR(50)     NOT NULL,   -- stable registry key, never renamed
    last_number         BIGINT UNSIGNED NOT NULL DEFAULT 0,
    seeded_from         BIGINT UNSIGNED NULL,       -- counter value at seed time; gap report starts above it
    seeded_at           DATETIME        NULL,
    gap_checked_through BIGINT UNSIGNED NULL,       -- incremental gap-report watermark
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (tenant_id, doc_type)
) ENGINE=InnoDB;

CREATE TABLE platform_document_counters (
    doc_type    VARCHAR(50)     NOT NULL PRIMARY KEY,
    last_number BIGINT UNSIGNED NOT NULL DEFAULT 0,
    seeded_from BIGINT UNSIGNED NULL,
    seeded_at   DATETIME        NULL,
    updated_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;
```

### PostgreSQL

```sql
CREATE TABLE document_counters (
    tenant_id           bigint      NOT NULL,
    doc_type            varchar(50) NOT NULL,
    last_number         bigint      NOT NULL DEFAULT 0 CHECK (last_number >= 0),
    seeded_from         bigint      NULL,
    seeded_at           timestamptz NULL,
    gap_checked_through bigint      NULL,
    updated_at          timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, doc_type)
);
```

Do not use `CREATE SEQUENCE`, `IDENTITY`, `serial` or MySQL `AUTO_INCREMENT` for the
visible number. Both engines document that a value taken by a rolled-back transaction
is not reused, so those objects leave gaps by design. They remain correct for ids.

## 2. A numbered document table

```sql
-- MySQL 8; PostgreSQL is the same shape with bigint/timestamptz
CREATE TABLE purchase_orders (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,  -- untouched surrogate key
    tenant_id       BIGINT UNSIGNED NOT NULL,
    po_number       VARCHAR(40)     NULL,       -- NULL while draft; set at issue
    status          VARCHAR(20)     NOT NULL,   -- draft | issued | void
    issued_at       DATETIME        NULL,
    void_reason     VARCHAR(255)    NULL,
    idempotency_key VARCHAR(100)    NULL,
    supplier_reference VARCHAR(64)  NULL,       -- external numbers live here, never in po_number
    UNIQUE KEY uk_po_number (tenant_id, po_number),          -- many NULL drafts allowed
    UNIQUE KEY uk_po_idem   (tenant_id, idempotency_key),
    KEY ix_po_issued (tenant_id, issued_at, id)               -- list sort key
) ENGINE=InnoDB;
```

PostgreSQL treats NULLs as distinct in a unique index by default, which is what drafts
need. Do not add `NULLS NOT DISTINCT` to a number key.

## 3. Registry entry

The registry is data the allocator, the CI ratchet, the unique-key test, the seeder
and the gap report all read. Validate it when it loads: unknown keys, a duplicate type,
a pattern that does not parse what the format produces, or two types whose patterns can
match the same string in the same table all fail.

```php
[
  'type'      => 'purchase_order',        // stable; a format change gets a new key (purchase_order_v2)
  'scope'     => 'tenant',                // 'tenant' | 'platform'
  'tables'    => [['table' => 'purchase_orders', 'column' => 'po_number', 'tenant_column' => 'tenant_id']],
  'format'    => 'PO-{n:6}',              // {n:W} zero-padded counter; {yyyy} {mm} are labels only
  'pattern'   => '/^PO-(\d+)$/',          // group 1 is the counter; format and parse are exact inverses
  'tier'      => 1,                       // 1 = business documents, 2 = journal entry
  'lock_rank' => 40,                      // order inside the tier
  'issue_on'  => 'purchase order approved or first sent',
  'switch'    => 'numbering.purchase_order.v2',
  'label'     => 'Purchase order',        // plain-language name for messages and reports
]
```

## 4. Allocation algorithm

```text
allocate(db, tenantId, type, ctx):
  t = registry.get(type)                          # unknown type -> exception
  require db.inTransaction()                      # outside a transaction -> exception
  assertLockOrder(t)                              # strict in tests; warning in production
  last = SELECT last_number FROM document_counters
          WHERE tenant_id=? AND doc_type=? FOR UPDATE
  if no row:                                      # rare when provisioning pre-seeds every type
     seed = maxExisting(db, tenantId, t)          # see seeding reference
     INSERT ... ON DUPLICATE KEY UPDATE last_number = GREATEST(last_number, VALUES(last_number))
        -- PostgreSQL: ON CONFLICT (tenant_id, doc_type) DO UPDATE SET last_number = GREATEST(...)
     last = SELECT ... FOR UPDATE                 # a deadlock here is retried by withRetry
  n = last + 1; skipped = 0
  loop:
     candidate = format(t, n, ctx)
     if not exists(db, tenantId, t, candidate): break      # probe every table in t.tables
     n += 1; skipped += 1
     if skipped > 10000: throw NumberingExhausted         # signals a broken seed
  UPDATE document_counters SET last_number = n WHERE tenant_id=? AND doc_type=?
  if skipped > 0: log numbering.clash_skipped {tenant, type, from: last+1, to: n}
  return IssuedNumber(type, candidate, n, skipped)
```

The probe is safe because it runs under the counter lock: every allocator call for the
same tenant and type is serialised. Only a writer that bypasses the allocator can race
it, and the unique key catches that writer.

## 5. PHP sketch (PDO, MySQL 8)

```php
final class DocumentNumbers
{
    public function allocate(PDO $db, int $tenantId, string $type, ?NumberContext $ctx = null): IssuedNumber
    {
        $t = $this->registry->get($type);
        if (!$db->inTransaction()) {
            throw new NumberingOutsideTransactionException($t->label);
        }
        $this->lockOrder->assert($db, $t);
        $last = $this->store->lockAndRead($db, $tenantId, $t)
            ?? $this->store->seedAndLock($db, $tenantId, $t, $this->seeder->maxExisting($db, $tenantId, $t));

        $n = $last + 1;
        $skipped = 0;
        while ($this->probe->exists($db, $tenantId, $t, $candidate = $this->formatter->format($t, $n, $ctx))) {
            if (++$skipped > 10000) {
                throw new NumberingExhaustedException($t->label);
            }
            $n++;
        }
        $this->store->write($db, $tenantId, $t, $n);
        return new IssuedNumber($t->type, $candidate, $n, $skipped);
    }
}

/** The only retry mechanism. Nested calls join the outer one. */
function withNumberingRetry(PDO $db, callable $unitOfWork, int $maxAttempts = 3): mixed
{
    $dupRetried = false;
    for ($attempt = 1; ; $attempt++) {
        $db->beginTransaction();
        try {
            $result = $unitOfWork($db);
            $db->commit();
            return $result;
        } catch (PDOException $e) {
            $db->rollBack();                       // undoes the counter update: no number burnt
            $code = (int) ($e->errorInfo[1] ?? 0); // 1062 duplicate, 1205 lock wait, 1213 deadlock
            $retryable = ($code === 1213 || $code === 1205)
                || ($code === 1062 && !$dupRetried && isNumberKey($e));
            if (!$retryable || $attempt >= $maxAttempts) {
                throw $code === 1062
                    ? new NumberingExhaustedException('Nothing was saved. Please try again.', previous: $e)
                    : $e;
            }
            $dupRetried = $dupRetried || $code === 1062;
        }
    }
}
```

PostgreSQL equivalents: `23505` unique violation, `40P01` deadlock, `40001`
serialization failure, `55P03` lock not available. Test the SQLSTATE, not the message.

## 6. Issue-time lifecycle

| State | Number column | Delete allowed | Notes |
|---|---|---|---|
| Draft | NULL | Yes | Shown as "Draft" or by its id, never as a number |
| Issued | Set in the same commit as the status change | No | Delete path returns: "This purchase order already has its number PO-000124, so it is kept. Void it instead." |
| Void | Kept | No | Status, reason, user and time recorded; shown struck through in lists and reports |

Each type names its issue event in the registry (POS sale paid, purchase order approved
or sent, payroll run approved, journal posted, credit note issued). The service method
for that event calls `allocate()` and writes the number with the status change.

## 7. Lock order

- Tier 1: business documents, ordered by `lock_rank`. Tier 2: `journal_entry` only.
- A sale takes `invoice` then `journal_entry`; a refund takes `credit_note` then
  `journal_entry`. No path may post a journal and then create a business document in the
  same transaction.
- In tests and the lab, a lock-order tracker throws when a lower tier or rank is taken
  after a higher one. In production it logs a warning, so there is no extra query.

## 8. Tenancy

- The tenant id comes from the authenticated context, never from the request body.
- Every probe, seed and gap query filters on the tenant column; the registry test fails
  an entry without one unless its scope is `platform`.
- Error messages never reveal another tenant's numbers or counts.
