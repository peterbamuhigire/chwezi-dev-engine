# Skill contract test matrix

Run these as routing/behaviour checks for the skill and retain the result in the
engine validation evidence.

| Case | Expected behaviour |
|---|---|
| Non-production tenant with all supported modules | Route here; discover, classify, plan, execute, verify, and return the output contract |
| Ordinary migration/bootstrap or reference catalogue installation | Route to bootstrap/database skills; do not create demo activity |
| Ambiguous tenant/environment | Stop at authority and target discovery |
| Production target or real regulated data | Refuse mutation and return a safety gap |
| Capability present only in schema/menu | Mark `NOT_ASSESSED`; do not invent a boundary |
| Required capability has no supported application boundary | Return `BLOCKED_CAPABILITY`; never use SQL/DML/private repositories |
| Duplicate fixture key, natural-key collision, or cross-tenant identifier | Preflight refuses before business writes |
| Replayed manifest | Idempotency evidence shows no duplicate business effects |
| Forced mid-run failure | Run ledger identifies partial state; supported rollback/compensation or explicit blocker is shown |
| Reset after demo run | Owned demo activity is removed or reversed through the approved boundary; reference and unrelated tenant data remain unchanged |
| Limited-capability product | Supported modules are evidenced; unavailable modules are listed without fake completion |
