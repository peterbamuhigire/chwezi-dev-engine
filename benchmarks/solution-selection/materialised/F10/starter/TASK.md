# Migration m002: customer foreign keys on orders

Orders reference customers only through the nullable text column
`orders.legacy_customer_code`. The data holds duplicates (codes that differ only by case or
surrounding spaces) and unmapped values (unknown codes, blanks and NULLs). Version 1 of the
application (`shop/app_v1.py`) must keep reading and writing while the change is rolled out.

Create `migrations/m002_customer_fk.py` exposing:

- `expand(conn)` - idempotent. Adds a nullable `orders.customer_id` referencing `customers(id)`
  and whatever bookkeeping tables the migration needs. App v1 keeps working unchanged.
- `backfill(conn, batch_size=50)` - maps orders to customers in batches. A legacy code maps
  when exactly one customer has the same code after trimming spaces and ignoring case.
  Otherwise the order goes to the exception path: a row in table
  `customer_fk_exceptions(order_id, legacy_code, reason)` with `reason` `'unmapped'` (no
  match, blank or NULL) or `'ambiguous'` (more than one match). Safe to re-run at any time,
  including after an interruption part-way through; it never changes
  `legacy_customer_code` or deletes rows, and it clears an exception once the data is fixed.
- `verify(conn) -> dict` with integer keys `total`, `mapped`, `unmapped`, `ambiguous`,
  `pending` (orders neither mapped nor in the exception table) and `legacy_checksum`: the
  SHA-256 hex digest of the lines `"<order id>:<legacy code or empty>\n"` in order-id order.
- `contract(conn)` - raises `MigrationBlocked` unless `verify` reports zero `unmapped`,
  `ambiguous` and `pending`; otherwise installs triggers that reject orders without a
  `customer_id` from then on.
- `rollback(conn)` - undoes expand and contract (a nullable `customer_id` column may stay,
  emptied). It must never delete or change customers, orders, legacy codes or amounts.
- `class MigrationBlocked(RuntimeError)`.

Connections come from `shop.schema.connect` (autocommit); the migration manages its own
transactions.
