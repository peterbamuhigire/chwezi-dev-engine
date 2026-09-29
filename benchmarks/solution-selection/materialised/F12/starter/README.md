# Receipts for synthetic entity K (fixture)

Entity K keeps one book (`MAIN`). All figures are synthetic fixture data: no tax, FX or statutory
rates are involved. Amounts are stored as integer minor units (USD: 2 decimals, UGX: 0 decimals).

## Existing code

- `ledger/db.py` - schema, connection (autocommit; callers manage transactions) and fixture seed.
- `ledger/money.py` - `to_minor`, the house rounding rule (ROUND_HALF_EVEN at the currency exponent).
- `ledger/posting_service.py` - posting controls (`validate`), `insert_journal`, `post_journal`,
  `record_audit`.
- `receipts/handler.py` - to implement.

## Receipt callback contract

The provider sends a raw JSON body and a signature header: the lower-case hex HMAC-SHA256 of the
raw body with the shared secret. Body fields: `idempotency_key`, `entity`, `book`, `value_date`
(`YYYY-MM-DD`), `currency`, `amount` (decimal string), `receivable_ref`, `evidence_ref`, `version`.

A receipt debits bank (1000) and credits trade receivables (1100). It clears the receivable; it
must not recognise revenue again.

## Task

Implement `process_receipt` and `reverse_receipt` so that receipts are processed idempotently,
atomically and with source evidence, and so that a correction uses a linked reversal.

Run the tests with `python -m unittest discover -s public_tests -t .`.
