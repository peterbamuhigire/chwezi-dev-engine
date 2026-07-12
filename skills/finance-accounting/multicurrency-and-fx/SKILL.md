---
name: multicurrency-and-fx
description: 'Use when implementing IAS 21 multicurrency accounting: functional currency, presentation currency, transaction currency, exchange-rate tables, settlement, realised and unrealised forex gains or losses, revaluation, and currency-safe ledger design.'
metadata:
  portable: true
  do_not_use_when: Do not use for single-currency systems or statutory policy questions without the external accounting doctrine.
  required_inputs: Provide functional and presentation currencies, rate sources, transaction dates, ledgers, and reporting requirements.
  workflow: Apply currency capture, translation, remeasurement, gain-loss, rounding, and reconciliation rules in order.
  quality_standards: Preserve rate provenance, balanced entries, deterministic rounding, period consistency, and audit trails.
  anti_patterns: Do not overwrite historical rates, mix functional and presentation currency, or hide rounding differences.
  references: Load the external accounting doctrine and local references named by this skill when the branch requires them.
  compatible_with:
  - claude-code
  - codex
---

# Multicurrency And FX

<!-- dual-compat-start --><!-- dual-compat-end -->

## Inputs

| Artefact | Required? | Purpose |
|---|---|---|
| Functional and presentation currencies | yes | Define measurement and reporting bases |
| Transaction dates and rate source | yes | Select traceable exchange rates |
| Monetary balances and reporting period | yes | Drive remeasurement and translation |

## Outputs

| Artefact | Consumer | Acceptance condition |
|---|---|---|
| FX policy, postings, and reconciliation | Ledger and reporting workflows | Rate provenance, balanced entries, explained differences |

## Capability contract

Read and search are required. Rate imports, remeasurement journals, translation entries, and historical corrections require explicit authority, period controls, and reconciliation evidence.

## Degraded mode

Fallback without verified rates or doctrine: stop posting, preserve source-currency amounts, and report the missing rate or policy decision.

## Decision rules

| Balance or event | Treatment | Failure avoided |
|---|---|---|
| Foreign-currency transaction | Initial recognition at approved transaction-date rate | Untraceable base amount |
| Monetary item at reporting date | Remeasure at closing rate | Stale carrying value |
| Non-monetary historical-cost item | Preserve historical rate | False FX gain or loss |
| Presentation-currency reporting | Translate under applicable doctrine | Mixing remeasurement and translation |

## Domain anti-patterns

- Overwriting historical rates. Fix: version rates and preserve provenance.
- Posting only the converted amount. Fix: retain source currency, rate, and base amount.
- Using one rate type for every event. Fix: select rate by event and policy.
- Hiding rounding in revenue or expense. Fix: use controlled rounding accounts and reconcile.
- Mixing functional and presentation currency logic. Fix: separate remeasurement from translation.
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

## Use When

- A tenant books in one functional currency but invoices, pays, or receives in another currency.
- A group needs presentation currency reporting.
- Month-end FX revaluation is required.

## Hard Rules

- MUST define one tenant functional currency.
- MUST store transaction currency and functional-currency equivalent on journal lines or linked valuation records.
- MUST not mix functional and presentation currency as if they are the same ledger amount.
- MUST revalue open monetary items at period end where required.
- MUST distinguish realised from unrealised forex gains/losses.

## Currency Model

Track:

- Functional currency: primary economic environment of the tenant.
- Transaction currency: currency of invoice/payment/document.
- Presentation currency: reporting currency where different from functional currency.
- Rate source, rate date, rate type, and approval status.

## Posting Patterns

Foreign currency invoice:

- Post AR/AP and revenue/expense using transaction-date rate in functional currency.
- Preserve transaction-currency amount for settlement and subledger ageing.

Settlement:

- Clear AR/AP at original functional-currency carrying amount.
- Post cash at settlement-date rate.
- Difference goes to realised forex gain/loss.

Month-end revaluation:

- Revalue open monetary items at closing rate.
- Difference goes to unrealised forex gain/loss and revaluation adjustment.
- Reverse or update according to the tenant close policy in the next period.

## Outputs

- Currency policy.
- FX-rate schema.
- Revaluation job design.
- Realised/unrealised FX posting matrix.
- FX reconciliation report.
