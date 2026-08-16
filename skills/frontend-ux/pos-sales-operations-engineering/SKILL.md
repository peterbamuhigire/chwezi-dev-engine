---
name: pos-sales-operations-engineering
description: Use when implementing or reviewing a tenant-aware ERP POS, agent POS, or manual sales-entry workflow where customer defaults, product-to-stock identity, inventory timing, payments, permissions, and audit-safe posting must remain consistent. Use the design engine for visual craft.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# POS Sales Operations Engineering

This skill owns the application and service contract for operational point of
sale. It keeps fast sales entry aligned with tenant isolation, finished-stock
truth, manufacturing timing, payment idempotency, permissions, accounting
posting, and evidence. Visual hierarchy and typography remain owned by the
external `design-system-skills` engine.

<!-- dual-compat-start -->
## Prerequisites

Load `skills/frontend-ux/pos-sales-operations-engineering` for implementation
rules together with the external design engine's `pos-and-retail-operations`
skill for presentation decisions. For money, inventory value, or ledger work,
also route to `chwezi-accounting-doctrine` and the local `accounting-engine`.

## Use When

- Building or auditing `pos.php`, `agent-pos.php`, or `encode-sales.php` in an ERP.
- Defining a tenant-wide Walk-in/default customer and its administrator permission.
- Connecting products to finished stock, manufacturing recipes, batches, and sale deductions.
- Consolidating multiple sales writers, payment handlers, or retry paths into one boundary.
- Testing tenant, branch, sales-agent, plant, stock, invoice, payment, GL, and audit controls together.

## Do Not Use When

- The work is only visual composition, typography, colour, or interaction polish; use the external design engine.
- The workflow is quotation → customer order → delivery → invoice → payment collection; design that as separate order-to-cash, not POS.
- The task is a financial statement, statutory rule, or accounting policy judgement; use the accounting doctrine.
- The task is generic frontend architecture without POS-specific transaction or stock semantics.

## Required Inputs

| Input | Produced by | Required? | Why |
|---|---|---:|---|
| Surface inventory and user journeys | Product owner / route audit | required | Separates shop POS, agent POS, and manual encoding |
| Tenant, branch, store, agent, and plant access model | Architecture / security | required | Prevents accidental scope escalation |
| Product-to-finished-stock map | Inventory and manufacturing | required | Identifies the stock item a sale may deduct |
| Recipe and manufacturing posting rules | Manufacturing / accounting | when applicable | Keeps ingredient consumption at manufacture |
| Customer, tender, tax, invoice, and GL mappings | Sales / finance | required | Defines a complete posting boundary |
| Representative fixtures and replay expectations | QA / demo seeding | required | Proves normal, failed, retried, and isolated paths |

## Outputs

| Artefact | Consumed by | Template or acceptance condition |
|---|---|---|
| POS surface contract | Product, design, frontend, QA | Names the three operational pages and the separate order-to-cash workflow |
| Product-stock and manufacturing map | Inventory, manufacturing, sales | Every saleable product has one active finished-stock mapping |
| Default-customer configuration contract | Tenant administration and QA | One server-resolved active customer is shared by all POS surfaces |
| Canonical posting boundary | API, accounting, inventory, audit | One atomic/idempotent service owns invoice, payment, stock, GL, and audit effects |
| Test and evidence bundle | Release owner and finance review | Includes tenant, permission, failure, replay, stock-timing, and reconciliation evidence |

## Non-negotiables

1. Keep exactly three operational POS surfaces distinct: `pos.php` is the
   general shop POS; `agent-pos.php` posts sales strictly for a sales agent;
   `encode-sales.php` manually records an already-made sale.
2. Store one tenant-wide default customer, normally Walk-in, in a tenant-scoped
   configuration key such as `pos_default_customer_id`. Resolve it server-side
   on every POS page. Never choose the first active customer or infer a default
   from a name containing “cash” or “walk”.
3. Allow only super administrators, max administrators, or users with the
   dedicated tenant configuration permission to change that setting. Validate
   customer ownership and active status before saving.
4. If the setting is missing or inactive, stop the POS page before the selling
   interface opens. Show a clear, localised configuration state and route the
   authorised user to settings; do not post an unassigned sale.
5. Sell products, not arbitrary stock items. Each saleable product must map 1:1
   to a finished stock item. Ingredients and packaging are not POS catalogue
   cards.
6. Manufacturing consumes recipe ingredient stock and produces the finished
   stock item. Sale posting deducts only that finished stock item. Do not deduct
   recipe ingredients again at sale.
7. Use one canonical transaction service or explicit adapters into it. Enforce
   tenant scope, customer validation, mapped product identity, batch/FEFO
   availability, price, invoice, payment, stock movement, GL posting, audit
   lineage, and idempotency in the service boundary.
8. Keep branch-sales access, sales-agent access, and plant/job access as
   separate permissions. A user who can view branch sales does not automatically
   gain plant access.
9. Treat a timeout as an unknown result. Retry with the same idempotency key and
   reconcile persisted records before displaying a new success or creating a
   second invoice.
10. For fiscal POS deployments, apply the mandatory session-locking and receipt
    sequence controls in
    `skills/product-business/product-discovery/references/feature-planning/references/pos-mandatory-requirements.md`.

## Decision rules

| Condition | Required action | Failure avoided |
|---|---|---|
| Active tenant default exists | Load it in all three POS pages before async catalogue work | Empty or divergent customer attribution |
| Default is absent or inactive | Block the POS interface and show configuration guidance | Unassigned or guessed customer sales |
| Operator selects a named customer | Preserve it through product, sales-point, review, and retry states | Silent reset to Walk-in |
| Product lacks an active 1:1 finished-stock mapping | Hide or reject it and report the data defect | Raw ingredient or phantom stock sale |
| Recipe ingredient is consumed | Post at manufacturing completion | Double consumption at sale |
| Finished stock is sold | Deduct the mapped finished item by batch | Ingredient deduction or negative stock leakage |
| User has branch rights but no plant rights | Keep plant records and job cards inaccessible | Permission transitivity breach |
| Payment response is unavailable | Reconcile by idempotency key before retrying | Duplicate payment or invoice |
| Any journal, stock, or invoice write fails | Roll back the atomic boundary or post an authorised reversal | Partial economic event |

## Workflow

1. **Inventory the surfaces.** Search routes, APIs, JavaScript, services,
   stored procedures, seeders, reports, and tests. Mark every writer and
   payment path; retire fake or random-ID writers rather than leaving them as
   competing authorities.
2. **Write the identity map.** Record product ID, finished stock-item ID,
   recipe ingredient IDs, batch ID, UOM, price, cost, and the direction of each
   manufacturing and sales movement. Keep customer-facing product identity
   separate from inventory identity.
3. **Define tenant configuration.** Add the setting, permission, settings UI,
   API validation, audit metadata, and a repeatable demo seeder. Verify the
   default belongs to the current tenant and is active.
4. **Gate and initialise all pages.** Resolve the default before rendering the
   sale interface or starting asynchronous catalogue calls. Show explicit
   loading, empty, error, disabled, and configuration-required states.
5. **Consolidate posting.** Route normal invoice sales, manual encoding,
   agent sales, and payment receipt through the canonical service. Preserve
   the same request/idempotency contract across retries and replay.
6. **Enforce stock timing.** Manufacture ingredient-to-finished movements at
   job completion; sell product-to-finished-stock movements at sale posting;
   lock and validate the relevant batch quantities in the same transaction.
7. **Verify boundaries.** Test tenant and branch scope, sales-agent scope,
   plant separation, permission changes, inactive defaults, unmapped products,
   insufficient stock, duplicate keys, payment timeouts, voids, and reversals.
8. **Reconcile evidence.** Confirm invoice lines, payments, stock ledger,
   batch balances, GL journals, customer balance, and audit entries agree. Run
   the seeder in dry-run/apply/verify modes and prove replay does not duplicate.

## Quality Standards

- Use server-derived tenant context and prepared statements; never trust a
  tenant ID, customer ID, stock ID, branch ID, or plant ID from the browser.
- Keep errors solution-bearing and localisable. Never return a green success
  state before the persisted result is known.
- Require focused unit/contract tests, a database-backed integration path where
  possible, PHP/JavaScript syntax checks, and a release evidence record.
- Keep the implementation separate from the visual system. Hand off spacing,
  type, colour, touch targets, and visual QA to the design engine.

## Anti-Patterns

- **Name heuristic default:** selecting the first customer matching “cash”.
  **Fix:** resolve the explicit tenant setting and block when invalid.
- **Terminal override:** letting a sales-point default silently replace the
  tenant default. **Fix:** keep compatibility fields secondary to the tenant key.
- **Raw-stock catalogue:** displaying bottles, jars, labels, or ingredients as
  products. **Fix:** expose only active product-to-finished-stock mappings.
- **Sale-time recipe deduction:** consuming ingredients when a product is sold.
  **Fix:** consume ingredients at manufacture and finished stock at sale.
- **Writer sprawl:** separate fake sale/payment writers for each screen.
  **Fix:** use one canonical transaction boundary and adapters.
- **Permission shortcut:** treating branch visibility as plant access.
  **Fix:** model and enforce plant permissions separately.
- **Retry duplication:** generating a new idempotency key after a timeout.
  **Fix:** query the original key and reconcile before retrying.
- **False success:** trusting a browser toast without invoice, stock, and GL
  evidence. **Fix:** verify persisted records and reconcile the posting.

## Read next

- External `design-system-skills/skills/06-sector-and-domain-ux/pos-and-retail-operations`
- `skills/architecture/api-design-first`
- `skills/finance-accounting/accounting-engine`
- `skills/backend-databases/database-design-engineering`
- `skills/security/vibe-security-skill`
- `skills/sdlc-meta/advanced-testing-strategy`
- `skills/sdlc-meta/reliability-engineering`
- `skills/sdlc-meta/skill-composition-standards`

## References

- `references/pos-operations-contract.md` — detailed identity, transaction,
  permissions, and evidence contract.
- `skills/product-business/product-discovery/references/feature-planning/references/pos-mandatory-requirements.md` — session and receipt controls.
- `skills/sdlc-meta/skill-composition-standards/references/test-plan-template.md` — test evidence shape.
- `skills/sdlc-meta/skill-composition-standards/references/rollback-plan-template.md` — rollback evidence shape.
<!-- dual-compat-end -->
