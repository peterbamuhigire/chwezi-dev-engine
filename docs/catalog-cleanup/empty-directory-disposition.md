# Empty Directory Disposition

Last verified: 2026-07-08

Backlog item: 1. Dimension: Architecture & Discoverability.

The July 2026 audit found empty legacy directories that could look like active capability. A fresh scan on 2026-07-08 found eight empty directories under `skills/`. This disposition resolves them without deleting compatibility paths during routine docs work.

## Policy

Empty directories under active roots are allowed only when one of these is true:

| Status | Meaning | Required evidence |
|---|---|---|
| Retained alias shell | The active skill was deactivated but the path is retained for compatibility | Listed in `docs/skill-aliases.yml` or `docs/skill-routing-index.md` |
| Pending parent absorption | Durable material has moved to a parent skill or external engine | Parent route named below |
| Generated asset mount | Tooling expects the directory but content is produced on demand | Owning script or skill named below |

No directory in this table should be treated as an active `SKILL.md` surface.

## Disposition Table

| Empty path | Disposition | Route or owner | Reviewer action |
|---|---|---|---|
| `skills/ai-entitlements-and-feature-gating/references` | Retained legacy shell | Active equivalent is `skills/ai/ai-entitlements-and-feature-gating` | Keep empty until the legacy top-level path is removed by a dedicated migration |
| `skills/ai-feature-rollout-and-experimentation/references` | Retained legacy shell | Active equivalent is `skills/ai/ai-feature-rollout-and-experimentation` | Keep empty; do not add references here |
| `skills/enterprise-ux-process/assets` | Externalized design shell | Canonical design content lives in `design-system-skills` | Keep only if route remains documented; otherwise remove in a migration PR |
| `skills/enterprise-ux-process/scripts` | Externalized design shell | Canonical design content lives in `design-system-skills` | Keep only if route remains documented; otherwise remove in a migration PR |
| `skills/fixed-assets-and-depreciation/references` | Finance doctrine shell | Canonical finance doctrine lives in `chwezi-accounting-doctrine` | Do not populate in this engine |
| `skills/inventory-costing/references` | Finance doctrine shell | Route to `doctrine/skills/inventory-costing-and-stock-accounting` or external finance engine | Do not populate in this engine |
| `skills/multicurrency-and-fx/references` | Finance doctrine shell | Route to external finance engine | Do not populate in this engine |
| `skills/payroll-postings-uganda/references` | Finance doctrine shell | Route to external finance engine and Uganda statutory pack | Do not populate in this engine |

## Validation

Run:

```powershell
Get-ChildItem -Directory -Recurse | Where-Object { -not (Get-ChildItem -LiteralPath $_.FullName -Force | Select-Object -First 1) } | Select-Object -ExpandProperty FullName
python -X utf8 scripts\skill_catalog_guardrails.py --report-only
```

Pass criteria:

- No empty path is presented as an active skill.
- Every empty path has a route, owner, or migration note.
- No finance or design doctrine is copied back into this engine.
