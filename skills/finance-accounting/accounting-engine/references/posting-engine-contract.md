# Posting Engine Contract

## Required Write Path

All ledger writes pass through `LedgerPostingService::post(JournalEntry $entry)`.

The method MUST:

- Start a database transaction.
- Lock or validate the accounting period.
- Validate all accounts belong to the same tenant and are active.
- Validate the source document exists and is postable.
- Validate `sum(debits) == sum(credits)` in the journal currency.
- Validate the idempotency key has not already posted a different payload.
- Insert a journal header and journal lines.
- Commit atomically.
- Emit a durable domain event for downstream caches and reports.

## Reversals

Reversal means a new journal with opposite debits/credits and `reverses_journal_id` pointing to the original. The original remains immutable.

Bad:

```php
$line->amount = 0;
$line->deleted_at = now();
$line->save();
```

Good:

```php
$poster->post($reversalFactory->reverse($originalJournal, $reason, $actorId));
```

## Mapping Resolver

Business code asks for accounts by business meaning, not code:

```php
$accounts = $resolver->forSale(
    tenantId: $tenantId,
    productCategoryId: $categoryId,
    paymentMethodId: $paymentMethodId,
    taxRateId: $taxRateId,
);
```

If a mapping is missing, return a structured error naming the missing mapping and stop posting.

## Starter Skeletons

A PHP/MySQL starting point for this contract is kept in `chwezi-finance-engine-skeletons/`:

- `chwezi-finance-engine-skeletons/php-mysql/posting-service-skeleton.php`: a posting service with the transaction, period lock, balance and idempotency checks listed above.
- `chwezi-finance-engine-skeletons/php-mysql/schema.sql`: the ledger tables the skeleton expects.
- `chwezi-finance-engine-skeletons/reviewer-checklist.md`: the pull-request checklist for any change that touches money.

Treat them as starting points to review against this contract and the finance doctrine engine, not as finished code. (Moved here on 29 Sep 2026 from `skills/finance-accounting/_chwezi-finance-engine-skeletons/`, a folder with no `SKILL.md`.)
