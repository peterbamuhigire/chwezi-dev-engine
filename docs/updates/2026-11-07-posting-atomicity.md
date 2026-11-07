# Posting skeleton atomicity repair

The illustrative PHP posting service committed journals before storing audit and
idempotency records. An injected audit failure reproduced a committed header
without its completion evidence. Audit and idempotency writes now precede commit;
both adapters must use the same PDO transaction. External sinks need a
transactional outbox. The file is explicitly incomplete illustrative code.

Run `php tests/posting-atomicity.php`. This loads the actual skeleton with typed
synthetic dependencies and SQLite in memory. Failures injected both before and after each audit/idempotency insert
roll back all four tables; retry and same-key replay yield one header,
two balanced lines, one audit and one key. Unbalanced input, system-only account access and missing evidence are also
rejected without ledger mutation. Blank keys are rejected before lookup. A changed-payload replay writes a
rejection audit while retaining the original posting and result.
Account permission is not tenant-isolation
proof. No persistent database is contacted.

PHP transaction behaviour was checked on 2026-11-07 against
https://www.php.net/manual/en/pdo.transactions.php (primary documentation,
context-bound to transactional PDO backends; publication date unspecified;
review before backend changes). MySQL storage-engine behaviour, concurrent
requests, tenant enforcement, production rejection-audit integration,
source-event state, downstream notifications, real account mapping and
production finance acceptance remain NOT_ASSESSED.
This bounded proof is partial D2.1 evidence, not completion of its full criteria.

Recovery: revert this skeleton diff and remove the synthetic test and this note.
No posted data or configuration changed. Doctrine owner remains the accounting
engine; no new accounting policy or statutory value was introduced.
