# Price Versioning and Plan Migration

Load when a SaaS changes list prices, restructures tiers, retires a plan, or must move an existing
cohort of subscriptions from one price point to another without billing errors, entitlement drift,
or an unaudited customer-facing change.

The pricing decision (whether, how much, grandfather or not) belongs to `software-pricing-strategy`
and the commercial owner. This reference covers how the system makes that decision safe to execute.

## Inputs

- Approved price change record: old and new amounts per currency and interval, effective date,
  affected plans, grandfather/sunset policy, notice period, and the named approver.
- Current catalogue (products, prices, lookup keys, entitlement bundles) as code.
- Subscription inventory with plan, price, currency, interval, renewal date, schedule id,
  contract/override flag, and tax behaviour.
- Customer-notice requirements from legal/commercial owners (contract terms, consumer rules in each
  selling jurisdiction). Missing notice rules: stop; do not infer a default notice period.

## Model rules

1. **Catalogue is versioned data.** Keep a `plan_versions` table (or catalogue file in version
   control) keyed by `plan_code + version`, holding price ids per currency/interval and the
   entitlement bundle id. The pricing page, checkout, in-app upgrade screen, and sales quote tool
   all read this one source. A hand-edited marketing pricing page is a defect.
2. **Prices are append-only.** A processor price's amount is not edited in place; create a new
   price, then move traffic and subscriptions to it. Deactivate the old price for new purchases
   only after nothing new should reference it.
3. **Stable lookup keys route new purchases.** Checkout resolves `lookup_key = pro_monthly_ugx`
   rather than a hard-coded price id. Moving the key to the new price is the atomic cut-over for new
   buyers; existing subscriptions are untouched by that move.
4. **Subscriptions record their plan version.** Store `plan_version` on the local subscription
   mirror. Entitlements resolve from the version the tenant is actually paying for, so a
   grandfathered tenant keeps exactly what they bought, not whatever the current tier contains.
5. **Contract overrides win.** Tenants with negotiated terms (`customer_contracts`, see
   `saas-entitlements-and-plan-gating`) are excluded from bulk migration and routed to account
   owners.

## Cut-over procedure

1. **Create** new prices for every currency and interval in the change record. Verify amounts,
   currency minor units, tax behaviour, and interval in a test environment first.
2. **Publish** the new plan version to the catalogue; regenerate pricing page and quote tool from
   it. Run a parity test: every displayed price equals a live price id in the catalogue.
3. **Switch new purchases** by moving lookup keys. Record the switch time; the metrics layer uses it
   to separate old-price and new-price cohorts.
4. **Classify existing subscriptions** into: grandfathered indefinitely, grandfathered with sunset,
   migrate at next renewal, contract-excluded, and blocked (past due, paused, mid-dispute, or with an
   unreleased schedule). Persist the classification with the change-record id.
5. **Notify** the migrate cohort per the approved notice period, through the lifecycle messaging
   route. The notice carries the effective date, old and new amounts in the customer's currency,
   and the action available (switch to annual, change tier, cancel).
6. **Schedule, do not overwrite.** Apply the change at the renewal boundary using the processor's
   scheduling facility (Stripe: a subscription schedule with a second phase on the new price and an
   explicit proration choice) so the current paid period is honoured. Store the schedule id.
7. **Execute in waves** with a dry run first: compute the expected next invoice per subscription
   (processor invoice preview), compare to the change record, and only then write. Wave 1 is a small
   internal or friendly cohort; widen only when reconciliation is clean.
8. **Reconcile** after each renewal wave: mirror plan_version equals processor price, expected
   invoice equals actual, entitlements equal the version's bundle. Drift goes to the existing
   reconciliation dashboard (`billing-reconciliation.md`).
9. **Retire** the old price for new purchases once no new flow references it; keep it active for
   grandfathered subscriptions.

## Invoices after a price change

- A finalised invoice is a legal record. Never regenerate a PDF from current catalogue data; store
  the issued document (or processor invoice id and its immutable number) and render history from it.
- Corrections after finalisation go through credit notes or void-and-reissue per the processor and
  the jurisdiction, not through editing. In Uganda, a SaaS that must issue fiscal documents through
  URA's EFRIS handles the fiscal credit-note path via `electronic-fiscal-taxing`.

## Worked example (original)

A Kampala school-management SaaS moves its "Pro" tier from UGX 180,000 to UGX 220,000 per month and
adds SMS fee reminders to the tier.

- `pro@v3` is published with new UGX and KES prices and bundle `pro_bundle_v3`; lookup key
  `pro_monthly_ugx` moves to the new price at 00:00 EAT on 1 February.
- 412 existing Pro schools are classified: 37 on negotiated district contracts (excluded), 9 past
  due (blocked until recovered), 366 migrate at their next renewal after a 60-day notice approved by
  the commercial owner.
- The 366 remain on `pro@v2` entitlements until their scheduled phase starts; SMS reminders unlock
  exactly when they start paying the v3 price, not on 1 February.
- Wave 1 is the 12 schools run by the founder's partner network; reconciliation shows two schedules
  with a stale coupon omitted from the phase update, so the job is fixed before wave 2.

## Quality gate

- [ ] Change record approved, with notice period and grandfather policy sourced from an owner.
- [ ] Pricing page, checkout, quote tool, and in-app upgrade read one catalogue; parity test passes.
- [ ] Every subscription carries `plan_version`; entitlements resolve from it.
- [ ] Contract and blocked subscriptions are excluded and listed for human follow-up.
- [ ] Dry-run invoice previews match the change record before any write.
- [ ] Changes are scheduled at renewal boundaries with an explicit proration decision.
- [ ] Post-wave reconciliation is clean before the next wave; rollback (release schedule) is tested.
- [ ] Every migration write emits an audited event with actor, change-record id, and old/new price.

## Anti-patterns

- Editing a live price amount or reusing a price id for a different amount.
- Updating the subscription item immediately and surprising the customer with a proration charge.
- Migrating entitlements on announcement day while billing moves at renewal (or the reverse).
- Updating a subscription directly while a schedule is attached, so the next phase silently
  overwrites the change; use the schedule API for scheduled subscriptions.
- Omitting discounts, tax rates, or metadata when rewriting schedule phases; omitted fields unset.
- Pricing page copy maintained separately from the catalogue.
- Treating a grandfathered cohort as "legacy" in metrics without a plan_version dimension.

## Evidence / currentness

Access date 2026-09-24. Review by 2027-03-24 or on processor API version change.

- Stripe API, Update a price (docs.stripe.com/api/prices/update): updatable fields are `active`,
  `currency_options`, `lookup_key`, `metadata`, `nickname`, `tax_behavior` (once set to inclusive or
  exclusive it cannot change), and `transfer_lookup_key` (atomically moves a lookup key). Amount is
  not an updatable field. Verified.
- Stripe, Subscription schedules (docs.stripe.com/billing/subscriptions/subscription-schedules):
  phases (up to 10 current/future), `from_subscription`, per-phase and update-level
  `proration_behavior` (`create_prorations` default, `none`, `always_invoice`), omitted parameters
  are unset on update, direct subscription edits may be overwritten by the next phase, invoice
  preview supports schedules. Verified.
- Stripe, How invoicing works (docs.stripe.com/invoicing/overview): most details of a finalised
  invoice cannot change; finalised invoices cannot be deleted; void or credit notes are the
  correction path; local regulation governs amendment. Verified.
- Notice periods and consumer-protection rules per jurisdiction: `NOT_ASSESSED`; obtain from the
  legal owner for each selling country.
- Processors other than Stripe: `NOT_ASSESSED`; map the same rules onto their documented primitives.

Sources: Walling (2023) *The SaaS Playbook*; Mersch (2022) *Hacking SaaS*; Stripe documentation as
listed above.
