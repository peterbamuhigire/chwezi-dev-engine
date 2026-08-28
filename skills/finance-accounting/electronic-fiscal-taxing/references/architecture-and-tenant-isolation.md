# Fiscal Taxing Architecture and Tenant Isolation

## Common domain port

Keep the core provider-neutral:

```text
FiscalProfileResolver -> FiscalDocumentBuilder -> FiscalGateway
       |                         |                    |
 tenant/TIN/device          source hash          adapter/authority
```

The port exposes `submit`, `query`, `correct`, `cancel`, `catalogue`, and
`reconcile`. It returns normalized state plus provider response code, message,
version, exchange ID, FDN/verification/QR where applicable, and evidence hashes.

## Fiscal profile

Minimum fields: tenant/client ID, legal name, TIN/tax ID, VAT status, currency,
environment, endpoint reference, credential/key references, branch/device map,
catalogue/dictionary versions, offline policy, sequence namespace, status,
source-register revision, and reviewer approval.

Every query uses profile scope. Composite uniqueness should include tenant where
the business concept is tenant-local, for example `(tenant_id, source_type,
source_id)` and `(tenant_id, idempotency_key)`.

## Single versus multi-tenant

Single-client mode is a deployment topology, not a different data model. It may
resolve the only active profile without a tenant claim, but must still reject
unconfigured or ambiguous profiles. Multi-tenant mode derives scope from auth,
checks ownership at every repository boundary, and returns 404 for inaccessible
resources.

Never share a local offline enabler between unrelated TINs unless the authority
has explicitly approved that topology. The supplied Uganda material points to
taxpayer/device-bound operation.

## Ownership

- Commercial service owns invoice/order/payment/stock truth.
- Fiscal gateway owns submission state and authority evidence.
- Provider adapter owns protocol-specific serialization/crypto.
- Mobile owns a cache/journal of ERP projections, not fiscal authority truth.
- Reconciliation owns exception classification and repair workflow.
