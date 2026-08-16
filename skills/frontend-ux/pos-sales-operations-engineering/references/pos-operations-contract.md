# POS Operations Contract

Back to [`SKILL.md`](../SKILL.md). This reference is the engineering companion
to the visual POS contract in the external `design-system-skills` engine.

## 1. Surface ownership

| Surface | Purpose | Must not become |
|---|---|---|
| `pos.php` | General tenant/shop counter sale | Agent settlement or bulk order-to-cash |
| `agent-pos.php` | Sale posted on behalf of a selected sales agent | General shop cashier or plant operator |
| `encode-sales.php` | Manual recording of a sale already made | A quote, delivery, invoice-collection, or payment workflow |

Bulk quote → customer order → delivery → invoice → payment is a separate
workflow. Reuse the canonical posting services where appropriate, but do not
pretend that bulk order fulfilment is a POS state.

## 2. Default customer contract

Use one tenant-scoped setting, for example:

```text
system_settings(setting_key = 'pos_default_customer_id')
```

The value is a customer ID, not a name. Resolve it with both tenant and active
status predicates. A valid implementation must expose the same customer object
to all three page initialisers before product loading begins.

The settings workflow must:

1. require the dedicated tenant setting permission;
2. allow platform super administrators and tenant max administrators through
   the normal permission policy;
3. reject a customer from another tenant, an inactive customer, a malformed ID,
   or a missing CSRF token;
4. record the actor and setting change in the normal audit trail;
5. provide a repeatable dry-run/apply/verify seed path for non-production demo
   tenants;
6. never select the first active customer as a fallback.

When no active default exists, render a configuration-required state before the
selling interface. The state must provide a clear explanation, a settings
route for an authorised user, and a localised SweetAlert or equivalent notice.
The visible fallback card must remain useful if JavaScript fails to load.

## 3. Product and stock identity

The product is the sellable identity. The finished stock item is the inventory
identity. Store the relationship explicitly and require one active mapping for
each saleable product:

| Event | Source identity | Effect |
|---|---|---|
| Recipe definition | Ingredient stock items | Defines manufacture input |
| Manufacturing completion | Ingredient stock items | Decreases ingredients and creates finished stock |
| POS product search | Product joined to mapped finished item | Shows sellable product only |
| Batch availability | Mapped finished stock item | Supplies quantity, cost, and batch controls |
| Sale posting | Canonical product input resolved to mapped stock | Decreases finished stock only |

Packaging and raw ingredients may be valid recipe components, but they must not
appear as saleable product cards. A legacy stock-item input may be accepted only
inside a compatibility adapter that resolves it to a canonical product and
never changes the stored product identity.

## 4. Canonical transaction boundary

The service boundary should perform these checks and writes atomically:

```text
tenant and access context
  -> customer ownership and status
  -> product-to-finished-stock resolution
  -> batch/UOM/FEFO availability and price validation
  -> invoice and invoice lines
  -> payment or receivable effect
  -> finished-stock deduction and stock ledger
  -> COGS/inventory/revenue journal posting
  -> audit lineage and idempotency result
```

The normal POS, agent POS, and manual encoding adapters may differ in context
requirements, but they must converge before the economic event is written.
Payment receipt is also part of the canonical sales boundary; do not retain a
browser-only payment writer that bypasses the service.

## 5. Scope and permissions

Use a scope matrix instead of role-name shortcuts:

| Capability | Branch sales | Sales agent | Plant/job cards |
|---|---:|---:|---:|
| View branch sales | yes | optional | no |
| Post general shop sale | assigned point | no | no |
| Post agent sale | no | assigned agent/store | no |
| View plant production | no | no | explicit plant grant |
| Configure tenant default | explicit setting permission | explicit setting permission | no implicit grant |

Always derive tenant context on the server. Validate branch/store/sales-point
ownership in the same query or service boundary. A super or max administrator
may have a default bypass only through the central permission checker, not via
an unscoped route condition.

## 6. Failure and retry evidence

Every posting attempt needs a stable idempotency key. Test and preserve these
outcomes:

- validation failure leaves no invoice, payment, stock, or journal residue;
- insufficient stock identifies product, batch, required, available, and shortage;
- payment timeout can be reconciled by the original key;
- replay returns the original result without duplicate rows;
- a failed GL or stock write rolls back the economic event or creates an
  authorised linked reversal;
- tenant or plant scope failure returns a safe error without cross-scope data.

## 7. Minimum evidence bundle

Record the following before release:

1. a route and writer inventory for all three surfaces;
2. the setting, permission, tenant-scope, and inactive-default tests;
3. a product mapping fixture with recipe ingredients and finished stock;
4. manufacturing evidence showing ingredient deduction;
5. sale evidence showing finished-stock deduction only;
6. invoice, payment, stock ledger, journal, and audit reconciliation;
7. duplicate-key and timeout retry evidence;
8. dry-run/apply/verify seeder output with no secrets;
9. accessibility, localisation, and visual handoff evidence from the design engine;
10. rollback steps and the next review date.
