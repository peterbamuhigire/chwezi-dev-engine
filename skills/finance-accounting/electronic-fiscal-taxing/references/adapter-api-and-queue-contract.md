# Adapter, API, and Queue Contract

## Adapter boundary

```php
interface FiscalProviderAdapter
{
    public function submit(FiscalSubmission $submission): FiscalResult;
    public function query(FiscalQuery $query): FiscalResult;
}
```

The interface is illustrative: implementations must use the host language's
normal conventions. The domain must not know EFRIS envelope fields, encryption
codes, device installation paths, or provider-specific status numbers.

## Internal API contract

POST commands require an idempotency key scoped to authenticated tenant/profile
and source document. The server derives tenant scope. Responses expose stable
internal states and a safe retry decision; operator APIs expose redacted evidence
and permissioned replay only.

Required fields include source type/id, immutable source hash, document class,
profile ID resolved server-side, event time, currency, lines/tax summary,
correlation ID, and actor. Required response fields include state, provider
code/message, FDN/verification/QR if returned, attempt, timestamps, and links to
the ERP document/evidence.

## Queue contract

Use a transactional outbox or equivalent durable queue. Claim rows atomically,
lease them, and write attempt evidence. Retry only transient or unknown results
under bounded exponential backoff with jitter; do not retry deterministic
validation/auth failures without correction. Quarantine poison messages after
the configured cap and require permissioned replay.

The same idempotency key and immutable payload hash must survive retries. A
changed payload under the same key is a conflict, not a new submission.

## State mapping

```text
queued -> processing -> accepted -> reconciled
                 |-> retry_wait -> dead_letter/manual_review
                 |-> rejected -> correction/manual_review
```

Do not mark the ERP invoice fiscalized before provider acceptance evidence is
persisted atomically.
