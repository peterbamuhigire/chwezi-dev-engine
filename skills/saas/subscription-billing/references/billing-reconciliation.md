# Billing Reconciliation — Reference

Source-of-truth drift between the payment processor (Stripe / Paddle / Braintree) and the local platform mirror is **inevitable**. Reconciliation is the discipline that catches it.

## Why Drift Happens

- Webhook missed (network blip, signature mismatch after key rotation, replay-but-rejected).
- Webhook handler bug (typo on event type, off-by-one in date math).
- Direct edit in the Stripe Dashboard by ops (no local-mirror update).
- Manual SQL edit in production by an engineer.
- Stripe-side event ordering differs from local consume order.
- A subscription was created via the API and the webhook hasn't arrived yet.

## What to Reconcile

| Stripe entity | Local mirror | Reconcile cadence |
|---|---|---|
| `Customer` | `tenant_billing.stripe_customer_id` + name + email | nightly |
| `Subscription` | `tenant_billing.stripe_subscription_id` + status + plan + period_end | nightly |
| `Subscription.items[]` | line items / add-ons | nightly |
| `Invoice` | `invoices` mirror | hourly |
| `PaymentIntent` (for one-time) | `payments` mirror | hourly |
| `Refund` | `refunds` mirror | nightly |

## The Job

Nightly cron:
```python
def reconcile():
    cursor = None
    drift = []
    while True:
        page = stripe.Subscription.list(limit=100, starting_after=cursor, expand=['data.items'])
        for sub in page.data:
            local = TenantBilling.find_by_stripe_subscription_id(sub.id)
            if not local:
                drift.append({'kind': 'orphan_stripe_sub', 'stripe_id': sub.id})
                continue
            if local.status != sub.status:
                drift.append({'kind': 'status_drift', 'tenant': local.tenant_id, 'stripe': sub.status, 'local': local.status})
            if local.plan != map_price_to_plan(sub.items.data[0].price.id):
                drift.append({'kind': 'plan_drift', 'tenant': local.tenant_id, ...})
            if abs(local.current_period_end - sub.current_period_end) > 60:
                drift.append({'kind': 'period_end_drift', 'tenant': local.tenant_id, ...})
        if not page.has_more: break
        cursor = page.data[-1].id

    # Also check the other direction: local subs that no longer exist in Stripe
    for local in TenantBilling.where(stripe_subscription_id__not_null=True, status='active'):
        try:
            stripe.Subscription.retrieve(local.stripe_subscription_id)
        except stripe.error.InvalidRequestError as e:
            if 'No such subscription' in str(e):
                drift.append({'kind': 'orphan_local_sub', 'tenant': local.tenant_id, ...})

    persist(drift)
    if drift:
        alert(severity='warning' if len(drift) < 5 else 'critical', count=len(drift))
```

## Drift Dashboard

Surface:
- Count of drifts by kind, today / 7d / 30d.
- Each drift row with one-click "Refresh from Stripe" action (idempotent re-pull).
- Alert when daily drift > threshold (e.g., > 0.1% of subscriptions).

## Alert Thresholds

- **Warning**: > 5 drifts in one run.
- **Critical**: > 50 drifts OR drift count growing day-over-day.

A clean SaaS runs at < 0.1% drift after the initial reconciliation backfills the orphans from go-live.

## Resolution

For each drift kind:
- **Orphan Stripe sub** (Stripe has it, we don't): create local mirror by pulling Stripe → us. Investigate which tenant it belongs to (Stripe customer.metadata.tenant_id is the safety net — always set it).
- **Orphan local sub** (we have it, Stripe doesn't): mark local as `cancelled`, alert ops; investigate.
- **Status drift**: pull Stripe state; overwrite local. Stripe is truth.
- **Plan drift**: pull Stripe state; update local plan + entitlements.
- **Period-end drift**: pull Stripe state; update local.

## Idempotent Webhook Handler (Prevents Drift in the First Place)

```python
def handle_webhook(request):
    sig = request.headers['Stripe-Signature']
    try:
        event = stripe.Webhook.construct_event(request.body, sig, ENDPOINT_SECRET)
    except Exception:
        return 400

    # Idempotency
    if WebhookEvent.exists(event.id):
        return 200  # already processed

    with db.transaction():
        WebhookEvent.create(id=event.id, type=event.type, payload=event)
        dispatch(event)

    return 200
```

## Always Set `customer.metadata.tenant_id` in Stripe

When creating a Stripe Customer, set `metadata.tenant_id` to your local tenant ID. This is the bidirectional safety net — if a webhook is lost or processed out of order, you can always find your local tenant from the Stripe Customer.

## Anti-Patterns

- No reconciliation job at all — drift compounds.
- Reconciliation that writes to local without auditing — silent corrections lose traceability.
- Reconciliation that trusts local over Stripe (sometimes Stripe is the wrong source, e.g., Stripe Dashboard accidental edit, but **default to Stripe = truth**).
- Webhook handler not idempotent — retries duplicate state changes.
- No `metadata.tenant_id` on Stripe Customer — orphan reconciliation requires guesswork.
