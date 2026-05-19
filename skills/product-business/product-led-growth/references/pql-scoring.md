# PQL Scoring — Reference

PQL (Product-Qualified Lead) scoring identifies free / trial users who are showing buying intent through product usage. Engineering owns the score; growth and sales consume it.

## What a PQL Is

A user (or tenant) whose product behavior shows commercial intent. Not every active user is a PQL — only ones whose behavior predicts a high-probability upgrade.

## Signals

| Signal category | Examples |
|---|---|
| **Hitting limits** | Approached 80%+ of plan limit on any metered dimension |
| **Gated feature attempts** | Repeatedly tried features locked behind higher plan |
| **Engagement depth** | 5+ sessions in last 7 days, 3+ team members invited |
| **Activation** | Hit the "aha moment" event AND continued usage past day 7 |
| **Workflow completion** | Created first project / sent first invoice / shipped first email — the core value moment for the product |
| **Integration depth** | Connected 2+ external services (Slack, GitHub, Stripe, etc.) |
| **API usage** | Active API calls (signals technical buyer) |
| **Sustained activity** | Daily active for last 14 days |
| **Multi-user team** | 3+ users on the tenant |

## Score Calculation

Weighted sum. Tune weights per product based on which signals correlate with paid conversion historically.

```python
def compute_pql_score(user, tenant):
    score = 0
    if hit_limit_recently(tenant, threshold=0.8): score += 25
    if gated_feature_attempts(tenant, last_7d) >= 3: score += 20
    if sessions(user, last_7d) >= 5: score += 10
    if activated(user) and sustained_use(user, days=7): score += 15
    if completed_core_workflow(user): score += 20
    if integrations_connected(tenant) >= 2: score += 10
    if api_active(tenant): score += 10
    if team_size(tenant) >= 3: score += 10
    return min(100, score)
```

Thresholds:
- `< 30` — Not a PQL; standard lifecycle nudges.
- `30-60` — Warming up; lightweight upgrade prompts.
- `60-80` — Hot PQL; in-app upgrade prompt + lifecycle email.
- `> 80` — Sales-ready (for B2B); CRM creates Salesforce opportunity; AE outreach.

## Where It Lives

Materialise daily:
```sql
CREATE TABLE pql_scores_daily (
    tenant_id   BIGINT UNSIGNED NOT NULL,
    user_id     BIGINT UNSIGNED NOT NULL,
    day         DATE NOT NULL,
    score       INT NOT NULL,
    signals     JSON,
    PRIMARY KEY (tenant_id, user_id, day)
);
```

Real-time (Redis) for high-frequency triggers (gate hits → instant upgrade prompt).

## Consumers

| Consumer | What it does |
|---|---|
| In-app prompt service | Shows upgrade CTA when score crosses threshold |
| Lifecycle email engine | Triggers upgrade sequence |
| CRM reverse-ETL | Updates opportunity score in Salesforce/HubSpot |
| AE dashboard | Lists hot accounts |
| CSM dashboard | Notes expansion candidates among existing customers |

## Coordination With In-App and Email

Single rule: **one channel per user per upgrade context per day**. See `saas-lifecycle-email-orchestration` §10.

## Anti-Patterns

- Static threshold across all products — different products have different signal patterns.
- No backfill from historical conversion data — weights are guesses.
- Score in Mixpanel / Amplitude only — sales/CRM never sees it; not reverse-ETL'd to Salesforce.
- Daily materialization but hot events not real-time — gate denial fires the prompt 24 hours later, after the user has cooled off.
- Score is for the user but the upgrade is per tenant (B2B) — mix the right unit. PQL at tenant level is usually correct for B2B.

## Iteration

Quarterly: backtest weights against actual conversion in the prior quarter. Adjust to maximise conversion predictiveness.

## See Also

- `product-led-growth` — the umbrella skill.
- `saas-entitlements-and-plan-gating` — generates the `gate.denied` signal.
- `saas-lifecycle-email-orchestration` — consumes PQL signal for upgrade sequences.
- `saas-growth-metrics` — defines the aha event and activation rate.
