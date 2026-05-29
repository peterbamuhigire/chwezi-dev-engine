# Enterprise Override Model - Reference

Enterprise deals do not fit the plan catalogue. Acme signs for "unlimited storage, SSO, 250 seats, API at 5M calls/month, and a feature that is normally Scale-tier only - all at a negotiated price." If you encode that as `if tenant.id == 12345` branches in the codebase, you have forked your product for one customer, the branch is invisible to the entitlements resolver, and nobody can answer "who granted Acme unlimited seats and when does it expire?". This reference specifies the data-driven override model that lets enterprise contracts customise entitlements without touching code.

## section 1 The Rule: Overrides Are Data

Every deviation from a plan baseline is a row in an override table, applied at resolution time, audited, and (usually) expiring. There are exactly two override surfaces and one add-on surface:

- `tenant_feature_overrides` - grant or revoke a boolean feature for one tenant.
- `tenant_limit_overrides` - change a numeric limit for one tenant.
- `tenant_addons` - purchased capability bundles (modelled separately; see the parent skill's data model).

If a contract term cannot be expressed as a feature override, a limit override, or an add-on, that is a signal the catalogue itself needs a new feature or limit code - not a code branch.

## section 2 Precedence

The resolver merges sources in a fixed precedence. Higher wins.

```text
tenant override        (highest - the negotiated contract term)
   > add-on            (purchased capability)
      > plan baseline  (lowest - the catalogue default)
```

- A feature override with `enabled = false` revokes a feature the plan would otherwise grant (for example a tenant that contractually opted out of a data-sharing feature). A revoke override must beat an add-on grant - precedence makes that deterministic.
- A limit override replaces the plan value outright. An add-on limit is a `value_delta` added to the resolved base.
- Resolution order for a limit: `base = override OR plan_baseline; effective = base + sum(addon deltas)`. An override replaces the baseline; add-ons still stack on top unless the override explicitly says otherwise.

The wrong choice - ad-hoc precedence decided per call site - means feature X resolves "enterprise wins" in one handler and "plan wins" in another, and the same tenant sees the feature in the UI but is denied at the API.

## section 3 Resolution at Read Time

```python
def resolve_feature(tenant_id, feature_code):
    ov = tenant_feature_overrides.get(tenant_id, feature_code)
    if ov and not ov.expired():
        return ov.enabled                      # override wins (grant or revoke)
    if addon_grants_feature(tenant_id, feature_code):
        return True
    return plan_has_feature(plan_of(tenant_id), feature_code)

def resolve_limit(tenant_id, limit_code):
    ov = tenant_limit_overrides.get(tenant_id, limit_code)
    base = ov.value if (ov and not ov.expired()) else plan_limit(plan_of(tenant_id), limit_code)
    delta = sum_addon_deltas(tenant_id, limit_code)
    return None if base is None else base + delta   # None = unlimited
```

`None` means unlimited and must short-circuit limit checks (no counter comparison). Expired overrides are ignored at read time, not lazily deleted - so the moment an override lapses, the tenant silently reverts to plan baseline. Expiry is evaluated on every resolution, never cached past the expiry instant.

## section 4 Expiry - The Override That Outlives Its Contract

Every override carries `expires_at`. Promotional and contract-bound grants must expire; only a deliberate, documented permanent grant may set it null.

| Override origin | `expires_at` | Failure mode if missing |
|---|---|---|
| Promo / goodwill credit | Mandatory, short (30-90 days) | "Free for 60 days" silently becomes free forever; revenue leak |
| Contract term | Contract end date | Customer downgrades or churns but keeps Scale-tier features for free |
| Pilot / POC | Mandatory, pilot end | Failed pilot tenant retains paid capabilities indefinitely |
| Permanent negotiated grant | Null, but flagged `permanent = true` with sign-off | (Acceptable, but must be the explicit exception, not the default) |

Enforce at write time: reject an override creation that has neither `expires_at` nor an explicit `permanent` flag with a recorded approver. The system should make the safe choice (expiring) the easy one.

A `expires_at` reminder job notifies the account owner before a contract-bound override lapses, so renewal is a deliberate act and the customer is not surprised by a sudden downgrade mid-quarter.

## section 5 Who May Grant, and How

Overrides are commercial decisions and go through the back-office, never a raw SQL session.

```text
Admin Console -> POST /admin/tenants/123/entitlements
  body: {
    "type": "limit",
    "limit_code": "seats",
    "value": 250,
    "reason": "Q2 2026 contract, Acme Corp, SFDC opp 00891",
    "expires_at": "2027-04-01T00:00:00Z"
  }
  -> validate (limit_code exists; value sane; expiry-or-permanent present)
  -> write tenant_limit_overrides
  -> write audit_log (actor, target_tenant, before, after, reason)
  -> invalidate tenant entitlement cache / force JWT re-issue
  -> emit entitlements.changed event
```

- `reason` is mandatory free text and should reference the deal (contract id, opportunity number). A blank reason makes the override unattributable.
- Granting a feature or limit beyond the next tier up is a high-risk action requiring co-sign (a sales engineer should not unilaterally grant unlimited everything).
- Revoking or reducing an override (clawing back after a downgrade) is the same audited path.

## section 6 Audit

Every override write produces an audit row with actor, target tenant, the before and after state, the reason, and the expiry. This is what answers the questions that come up in a billing dispute or a SOC2 review:

- "Who gave Acme unlimited seats?" - actor + timestamp + reason.
- "Was this authorised?" - reason references the contract; co-sign recorded for high-value grants.
- "When does it lapse?" - `expires_at`.
- "What did they have before?" - before-state in the audit row.

Overrides without an audit trail are the difference between "we can prove every commercial exception" and "someone, at some point, gave this customer something for free and we cannot say who or why".

## section 7 Propagation and Caching

An override change must take effect promptly without a deploy.

- Write to the DB, then invalidate the tenant's resolved-entitlement cache and force a JWT re-issue (see the parent skill's hybrid resolution).
- Boolean feature changes can tolerate the JWT refresh interval (for example 15 minutes); limit changes that loosen a cap are safe to delay, but a change that *tightens* a cap (revoke, reduce) should invalidate immediately, or the tenant keeps using capability they no longer have.
- Emit `entitlements.changed` so downstream services (gateway, workers, analytics) drop their cached view.

The wrong choice - overrides that require a config redeploy or a token natural-expiry to take effect - means "we revoked Acme's access" is not true for up to 15 minutes, which matters when the revocation is a security or non-payment response.

## section 7a Worked Example - Acme's Enterprise Contract

Acme signs a 12-month Enterprise contract: 250 seats, unlimited storage, SSO (normally Scale-tier), API at 5M calls/month with soft overage, and the `advanced_reporting` feature (normally Scale-tier). None of this is a new plan; it is five override rows plus one policy change.

```text
POST /admin/tenants/789/entitlements  (one call per term, all co-signed, all expiring 2027-04-01)
  { "type": "limit",   "limit_code": "seats",            "value": 250 }
  { "type": "limit",   "limit_code": "storage_gb",       "value": null }            # null = unlimited
  { "type": "feature", "feature_code": "sso_saml",        "enabled": true }
  { "type": "limit",   "limit_code": "api_calls_monthly", "value": 5000000,
    "enforcement": "soft" }                                                          # hard-to-soft conversion
  { "type": "feature", "feature_code": "advanced_reporting", "enabled": true }
```

At read time the resolver merges these over Acme's base plan with no code branch anywhere. When the contract lapses on 2027-04-01 without renewal, every override expires on the same instant and Acme silently reverts to its base plan - which is exactly why the renewal-reminder job (section 4) fires 30 days before, so the account team renews deliberately rather than the customer discovering the downgrade in production.

## section 7b Resolution Trace

For `resolve_limit(789, 'api_calls_monthly')` while the contract is live:

```text
override?  yes, value=5,000,000, enforcement=soft, not expired   -> base = 5,000,000
addons?    none for api_calls_monthly                            -> delta = 0
effective  = 5,000,000 (soft)
```

After expiry, the same call:

```text
override?  expired -> ignored
plan?      base plan 'enterprise' api_calls_monthly = 1,000,000  -> base = 1,000,000 (hard)
effective  = 1,000,000 (hard)
```

The enforcement mode reverts with the value: a soft cap that was a negotiated term becomes a hard cap again the moment the term lapses. Storing enforcement on the override (not just on the limit definition) is what makes that revert correct.

## section 8 Anti-Patterns

- **`if tenant.id == 12345` branches** - invisible to the resolver, untestable, un-auditable, forks the product.
- **Override with no expiry by default** - promos and pilots become permanent free grants.
- **No reason field** - overrides become unattributable; disputes unanswerable.
- **Per-call-site precedence** - feature shows in UI, denied at API, or vice versa.
- **Overrides applied at write time into a denormalised flag** instead of merged at read time - stale once the plan or add-ons change underneath.
- **Granting via raw SQL** - bypasses validation, audit, cache invalidation, and the entitlements.changed event.
- **No co-sign on large grants** - a single salesperson grants unlimited everything to close a deal.
- **Revocation that waits for token expiry** - "we cut off access" is false for the cache window.

## See Also

- `saas-entitlements-and-plan-gating` section 2 (three inputs), section 4 (data model), section 8 (override workflow).
- `references/limit-enforcement-patterns.md` - how an overridden limit is enforced atomically.
- `references/entitlements-vs-feature-flags.md` - why a contract grant is an entitlement, not a flag.
- `subscription-billing` - the contract/Price primitives an override accompanies.
- `saas-admin-backoffice-tooling` - the console and audit spine that issues overrides.
