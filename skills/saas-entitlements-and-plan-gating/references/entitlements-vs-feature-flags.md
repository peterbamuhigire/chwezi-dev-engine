# Entitlements vs Feature Flags — Reference

Confusing these is one of the most common SaaS-engineering mistakes. They look similar (both gate code paths); they are profoundly different in purpose, lifetime, ownership, and source of truth.

## The Difference

| Dimension | Entitlements | Feature Flags |
|---|---|---|
| Purpose | Commercial gating (what plan allows) | Rollout / experimentation (who sees the new thing) |
| Lifetime | Years (tied to product plans) | Days to months (until rollout complete) |
| Audience | Tenants by plan / contract | Users / tenants / cohorts by criteria |
| Source of truth | Billing system + entitlements DB | Feature-flag service (LaunchDarkly, Unleash, PostHog, GrowthBook) |
| Default for new code | Inherit plan capabilities | Off (gradual rollout) |
| Who controls | Product + commercial + finance | Engineering + product |
| Audit trail | Yes — every override is a commercial decision | Light — flag state changes |
| Impact of being wrong | Customer billed for feature they can't use OR can use without paying | Bad UX during rollout; usually quickly fixed |

## Both Can Live in the Same App

But they should be **separate runtimes**:

```python
# Entitlement check (plan-tied, durable)
if not Entitlements.has(tenant_id, 'api_access'):
    return deny_with_upgrade_prompt('api_access')

# Feature flag check (rollout, experimental)
if FeatureFlags.is_on('new_dashboard_v2', tenant_id):
    return render(new_template)
else:
    return render(old_template)
```

## Common Mistakes

### Mistake 1: New feature gated only by a feature flag forever
A team builds "Advanced Reporting", puts it behind feature flag `advanced_reporting_v1`, marks it "on for all tenants on Pro plan." It works — but now the commercial gating lives in the feature-flag system, away from the billing system. When the team migrates feature-flag tool, the gating breaks. When the customer downgrades, they keep access until someone remembers to flip the flag.

**Fix:** if it's a permanent plan gate, it's an entitlement. Move it to the entitlements DB.

### Mistake 2: Feature flag controlling a paid feature
Same as above, in the other direction. A feature flag named `enable_billing` somewhere — and one day someone toggles it for testing and shuts off billing for all users.

**Fix:** commercial gates are entitlements, with audit trails and overrides only allowed via the back-office console.

### Mistake 3: A/B test on pricing
"Let's A/B test the Pro plan price." → feature flag `pricing_v2_treatment` on some cohort.

**Fix:** pricing experiments are special — they require careful Stripe Price versioning (see `subscription-billing`). The feature-flag system can pick *which Price ID to show* but should not encode the actual price.

## Recommended Stacks

| Use case | Tool |
|---|---|
| Entitlements | Custom DB-backed service (this skill) |
| Feature flags + experiments | LaunchDarkly, Unleash, PostHog feature flags, GrowthBook, ConfigCat |
| Both together | Some tools (LaunchDarkly, Statsig) try to do both — usable for small teams but draws the line less clearly |

## When the Lines Blur

- Beta program: a tenant gets early access to a feature. Is it an entitlement (commercial) or feature flag (rollout)?
  - If beta is tied to plan tier: entitlement with `beta_features` set.
  - If beta is hand-picked accounts: feature flag with explicit tenant list, time-bounded.
  - If beta is for paid users on any plan: feature flag.

- Trial features: during trial, the user has Pro entitlements. After trial, they downgrade.
  - Trial state is part of entitlement resolution; the entitlement query returns Pro until trial_end, then Free.

## Anti-Patterns

- Two systems with overlapping responsibility — sometimes entitlements decide, sometimes flags decide.
- Feature flags used to manage permanent commercial gating.
- Entitlements DB used for experimentation cohorts (slow + clumsy).
- No audit on entitlement changes — overrides untraceable.
- Audit on flag changes equally heavy as entitlement audit — overcompliance slowing rollout.

## See Also

- `saas-entitlements-and-plan-gating` — entitlements engine.
- `experiment-engineering` — experimentation patterns.
- `subscription-billing` — Price versioning for pricing tests.
- `product-led-growth` — using both in the upgrade-discovery flow.
