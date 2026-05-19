# Cross-Platform Entitlement Reconciliation — Reference

When a SaaS has web (Stripe) + iOS (StoreKit2) + Android (Play Billing), entitlements come from **multiple sources of truth**. Reconciliation is the engineering that makes the customer's plan consistent across surfaces.

## The Problem

- A customer subscribes on iOS via StoreKit2 → Apple is source of truth for that subscription.
- The same customer logs into the web → must see the same Pro features.
- They cancel on iOS → web must reflect the cancellation by `current_period_end`.
- They upgrade on web via Stripe → iOS must not double-bill.
- Family sharing on iOS → multiple users share one entitlement.

Without reconciliation:
- Customer pays twice.
- Customer is downgraded one platform but premium on another.
- Cancellations are slow to propagate.
- Support tickets explode.

## The Architecture

```
                  ┌──────────────────────────────────────┐
                  │   Platform Entitlement Service        │
                  │   (the single source of truth         │
                  │    the app reads at runtime)          │
                  └──────────────────────────────────────┘
                       ▲           ▲            ▲
                       │           │            │
                  ┌────┴─────┐ ┌───┴────┐  ┌────┴────────┐
                  │  Stripe   │ │ Apple   │  │  Google     │
                  │  Webhooks │ │  S2S    │  │  RTDN       │
                  │           │ │ Notifs  │  │  / Pub/Sub  │
                  └───────────┘ └─────────┘  └─────────────┘
                       ▲           ▲            ▲
                       │           │            │
                    Stripe       App Store    Play Store
                    Billing      Connect      Console
```

## The Platform Entitlement Service

A control-plane service that exposes:
- `GET /entitlements?user_id=X` → `{ plan, features, limits, source, expires_at }`.
- Internally aggregates from three sources, with rules for which wins.

### Reconciliation rules
- Most-recently-paid-active wins.
- Manual platform override (back-office) wins over everything.
- Family-shared entitlements: tag with `source: apple_family_sharing`; same access as paid.
- Trial state per source preserved separately.

### Storage
```sql
CREATE TABLE user_entitlements_sources (
    id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id           BIGINT UNSIGNED NOT NULL,
    source            ENUM('stripe','apple','google','admin_override') NOT NULL,
    source_subscription_id VARCHAR(128),
    plan              VARCHAR(64),
    status            ENUM('active','grace','expired','cancelled','revoked') NOT NULL,
    started_at        DATETIME,
    current_period_end DATETIME,
    raw_payload       JSON,             -- last receipt / event payload for audit
    updated_at        DATETIME NOT NULL,
    UNIQUE KEY uq_user_source_sub (user_id, source, source_subscription_id),
    INDEX idx_user (user_id)
);

CREATE TABLE user_entitlements (
    user_id         BIGINT UNSIGNED PRIMARY KEY,
    effective_plan  VARCHAR(64),
    features        JSON,
    limits          JSON,
    expires_at      DATETIME,
    source          VARCHAR(32),
    last_resolved_at DATETIME NOT NULL
);
```

A resolver computes `user_entitlements` from `user_entitlements_sources` after every source-change event.

## Apple StoreKit2 → Platform

### Inbound webhooks (App Store Server Notifications V2)
- `SUBSCRIBED`, `DID_RENEW`, `DID_FAIL_TO_RENEW`, `EXPIRED`, `REFUND`, `REVOKE`, `GRACE_PERIOD_EXPIRED`, `DID_CHANGE_RENEWAL_PREF`, `DID_CHANGE_RENEWAL_STATUS`.

### Receipt validation
- Use the App Store Server API (JWT-signed) — preferred over the legacy verifyReceipt.
- Validate `originalTransactionId` and use it as the canonical subscription identifier.

### Family Sharing
- The same `originalTransactionId` may apply to multiple Apple IDs if family-shared.
- Treat family members as separate users; tag entitlement source as `apple_family_sharing`.

### Linking Apple ID to platform user
- Inside iOS app, after StoreKit purchase, send the `Transaction.deviceVerification` JWT + originalTransactionId to your platform with the user's auth.
- Platform stores `user_id ↔ original_transaction_id` mapping in `user_entitlements_sources`.

## Google Play Billing → Platform

### Real-Time Developer Notifications (RTDN)
- Pub/Sub topic that Google publishes events to.
- Subscribe with a consumer that updates `user_entitlements_sources`.

### Purchase verification
- Use the Google Play Developer API to verify `purchaseToken`.
- Link to platform user via package + purchaseToken sent from Android client.

### Subscription Lifecycle
- `SUBSCRIPTION_PURCHASED`, `SUBSCRIPTION_RENEWED`, `SUBSCRIPTION_CANCELED`, `SUBSCRIPTION_ON_HOLD`, `SUBSCRIPTION_IN_GRACE_PERIOD`, `SUBSCRIPTION_RECOVERED`, `SUBSCRIPTION_REVOKED`, `SUBSCRIPTION_EXPIRED`.

## Stripe → Platform

Use the standard Stripe webhook pipeline (see `subscription-billing`).

## The Resolver

```python
def resolve_entitlement(user_id):
    sources = db.fetch_all_active_sources(user_id)
    # Admin override wins
    admin = next((s for s in sources if s.source == 'admin_override'), None)
    if admin and admin.status == 'active':
        return admin

    # Most recent active among Stripe / Apple / Google
    paid = [s for s in sources if s.source in ('stripe','apple','google') and s.status in ('active','grace')]
    if not paid:
        return free_tier()

    # Pick the one with the latest current_period_end
    winner = max(paid, key=lambda s: s.current_period_end)
    return winner_to_effective(winner)
```

Run resolver on:
- Every source event (webhook / RTDN / Stripe event).
- Periodic batch (hourly) catch-all.

## Avoiding Double-Billing

When the user has an active Apple subscription and tries to subscribe via Stripe (or vice versa):
- App reads `GET /entitlements/conflict?source=stripe` — returns existing active source.
- App offers to cancel the existing one or refuses the second purchase.
- Best UX: gray out the "Subscribe" button if active in another source; explain why.

Apple specifically requires that any subscription purchased outside iOS still be honored within iOS for the same Apple ID — the platform must respect that.

## Receipt Storage

Keep last 12 months of raw receipts per subscription for support investigation. Encrypt at rest.

## Anti-Patterns

- Trusting Apple/Google receipts validated client-side only — bypassable. Always validate server-side.
- Using Apple's `applicationUsername` field as the only user link — it's not guaranteed to round-trip. Use Apple's S2S notifications + your own linking flow.
- Forgetting RTDN — silent subscription state changes; platform thinks user is still active.
- Polling instead of webhooks/RTDN — slow + expensive.
- Free tier entitlements computed by app — race conditions with paid upgrades. Resolver is the only authority.

## See Also

- `ios-monetization` — StoreKit2 specifics.
- `subscription-billing` — Stripe Billing specifics.
- `saas-entitlements-and-plan-gating` — the runtime that reads `user_entitlements`.
- `saas-control-plane-engineering` — where the entitlement service lives.
