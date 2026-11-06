# API, offline and guardrails

Parent skill: [tenant-document-numbering](../SKILL.md). Self-contained; distilled from
the owner's numbering standard (5 Nov 2026) and the Maduuka reference plan
(`03-architecture.md` sections 12 and 13, `05-verification-and-gates.md`).

## 1. API contract

- Every response carrying a numbered document keeps its existing named field (for
  example `invoice_number`) and adds `document_number` (string or null) and
  `number_status` (`issued`, `draft` or `void`). Add fields; never rename or remove
  them, so old mobile builds keep working.
- Numbers are JSON strings. RFC 8259 only guarantees integers within plus or minus
  2^53 - 1, and the number includes its prefix anyway. Counters exposed for diagnostics
  are strings too.
- **Idempotency.** Numbered create endpoints require an `Idempotency-Key` header
  (`400 IDEMPOTENCY_KEY_REQUIRED` when missing). The key is stored on the document row
  under `UNIQUE (tenant_id, idempotency_key)` and looked up inside the transaction
  before `allocate()`. A replay at any time, not only within a cache window, returns
  the stored document and number and never allocates again. Never invent fallback keys
  from time buckets or request hashes.
- **No client numbers.** On create, ignore any request field shaped like a number
  (`invoice_number`, `reference`, `kot_number`) unless it is a documented external
  reference column such as `supplier_reference`. A contract test sends one and asserts
  the server's number wins.
- The tenant id comes from the session or token, never from the body.

## 2. Mobile and offline

- The server issues every number. A device never invents an official number.
- An offline document shows **"Pending number"** and a short provisional tag from an
  unambiguous alphabet (no 0/O, 1/I/L), for example `Pending · 7F3KQ9`. It must not look
  like an issued number in the type's format.
- Printing or sharing before sync is allowed only when the printout says "Saved on this
  device, not yet confirmed. The official number will follow." and carries the tag.
- The tag-to-server mapping lives in a durable local table that survives sync cleanup
  and app restarts. The client-generated id stays as the internal idempotency key.
- On sync, store `document_number` and `number_status` from the server and replace the
  tag everywhere: lists, detail screens, reprints, shares.

## 3. CI ratchet and schema test

| Check | Fails when |
|---|---|
| Generator ratchet | New code builds a document number outside the allocator: `COUNT(*)+1`, `MAX(...)+1`, `uniqid`, random or hash numbers, `sprintf('PO-%06d', $id)`-style id-derived numbers, new triggers or procedures that set a number column |
| Delete ratchet | New `DELETE` on a registry table without a `number IS NULL` guard |
| Sort ratchet | `ORDER BY <registry number column>` with no other key |
| Unique-key schema test | A registry `(tenant_column, column)` pair has no unique key, or a numbered table lacks `UNIQUE (tenant_id, idempotency_key)` |
| Registry test | Format and pattern are not exact inverses; overlapping patterns in one table; missing tenant column for tenant scope; `len(fixed text) + 19 > 40` |

The ratchet keeps a baseline of known legacy generators that may only shrink.

## 4. Test checklist (every allocator and every module that adopts it)

- [ ] Sequential: N documents produce 1..N with no gap and no duplicate.
- [ ] Concurrent: at least 8 parallel connections issuing on one tenant and type
      produce a contiguous set; repeat at the tenant's measured peak.
- [ ] Rollback: a save that fails after `allocate()` leaves the counter unchanged; the
      next document takes the same number.
- [ ] Outside a transaction: `allocate()` throws.
- [ ] Clash probe: a pre-existing row at `last+1` is stepped over and logged; the
      series stays contiguous.
- [ ] Unique-key backstop: a row inserted by another writer between probe and insert
      triggers one full retry and a correct number; a second clash yields the
      plain-language failure and nothing saved.
- [ ] Deadlock and lock-wait: the retry wrapper retries up to 3 attempts and burns no
      number.
- [ ] Lock order: taking `journal_entry` before a business counter throws in strict mode.
- [ ] Draft lifecycle: drafts have NULL numbers, can be deleted; issuing assigns the
      number in the same commit; deleting an issued document is refused with the void
      message; voids keep their number and appear in lists and reports.
- [ ] Idempotency: a replay after commit, and after a long delay, returns the same
      number; a missing key returns 400.
- [ ] Tenant isolation: two tenants issuing concurrently each get their own 1..N; the
      tenant id in the body is ignored.
- [ ] Separate series: platform invoices and credit notes do not move the tenant
      invoice counter; supplier references never move any counter.
- [ ] Capacity: counter at `PHP_INT_MAX - 1` (or the language's 64-bit max) formats and
      fits `VARCHAR(40)`; the allocator throws before overflow; padding grows cleanly.
- [ ] API: numbers serialise as strings; client-supplied numbers are ignored.
- [ ] Offline: provisional tag shown and printed with the not-confirmed notice; replaced
      by the server number after sync and after app restart.
- [ ] Gap report: an injected gap and an injected duplicate are both reported; the
      watermark advances.

## 5. Review checklist (code review and design review)

- [ ] Every numbered write goes through the single allocator, inside the save
      transaction, immediately before the insert.
- [ ] No `COUNT`/`MAX`/random/id-derived/client/sequence/trigger generator remains or
      is added.
- [ ] Number column nullable for drafts, `VARCHAR(40)` or wider, with `UNIQUE
      (tenant_id, number)`.
- [ ] No delete path removes a numbered row; void keeps the number and is visible.
- [ ] Lock order respected; the unit of work is wrapped in the retry helper.
- [ ] Idempotency key on the row with its unique key; looked up before allocation.
- [ ] Platform invoices, credit notes and external references use their own series or
      columns.
- [ ] Lists sort by issue timestamp and id, not the number string.
- [ ] Migrations never `UPDATE` an issued number and never lower a counter.
- [ ] Journal descriptions end with `(NUMBER)` from one ledger-writer enforcement point;
      generated test covers every posting type; id-interpolating builders ratcheted
      down (see [journal descriptions](journal-descriptions.md)).
- [ ] Evidence recorded for each check; anything unrun is marked `NOT ASSESSED`.
