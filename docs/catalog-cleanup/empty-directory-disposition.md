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

## 2026-09-29 update (M10-01-T06)

- `scripts/skill_catalog_guardrails.py` now reports every file-less directory under `skills/` and
  `00-meta-initialization/` as an `empty-directory` **warning**. Warnings are printed but do not fail
  the run; errors still do.
- The 50 empty directories found on 2026-09-29 (none tracked by Git) were removed one at a time with
  `rmdir`, which refuses a non-empty directory. The path list and results are recorded in
  `chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-01/`.
- None of the eight paths in the table above existed on 2026-09-29; the table is kept as history.
- Directories that hold only `references/` or `templates/` files (for example
  `skills/sdlc-meta/plan-implementation/`) are not empty and were not touched. Their disposition
  belongs to Kaizen phase M10-06.

## 2026-09-29 update (M10-06): tracked orphan folders

M10-01 handed over the tracked folders under `skills/` that held files but no `SKILL.md` or
`ALIAS.md`. The May 2026 consolidation (`84d37a5`) had moved each retired `SKILL.md` into its
parent skill as `references/<name>.md` but left the retired skill's own `references/`,
`templates/` and `examples/` behind, so the moved entrypoints pointed at files that no longer sat
next to them. Each folder was dispositioned as follows (decided by the orchestrator under Peter's
delegated authority, 29 Sep 2026):

| Folder(s) | Disposition | New location |
|---|---|---|
| 35 retired-skill folders (API, microservices, orchestration, MySQL x5, PostgreSQL x3, CI/CD x3, Kubernetes x3, observability, GIS x3, JavaScript, language standards, PHP security, Python SaaS, TypeScript x2, e2e testing, plan implementation, SDLC design/planning/testing/user-deploy) | **Merge** into the parent that already holds the moved entrypoint; links repointed | `<parent>/references/<name>/` beside `<parent>/references/<name>.md` |
| `finance-accounting/_chwezi-finance-engine-skeletons` | **Merge** into `accounting-engine`; linked from `posting-engine-contract.md` | `accounting-engine/references/chwezi-finance-engine-skeletons/` |
| 8 `ios/` TODO folders (`macos-*`, `swift-concurrency-macos`, `xcode-*`) | **Quarantine** out of the active roots (planning notes, not skills) | `docs/plans/apple-todo-backlog/<name>.md` |
| `sdlc-meta/plan-implementation` | Merge (above) plus **alias**: `ALIAS.md` routed to `implementation-status-auditor` | `skills/sdlc-meta/plan-implementation/ALIAS.md` |
| `sdlc-meta/spec-architect` (removed empty by M10-01) | **Alias** recreated: `ALIAS.md` routed to `project-requirements` | `skills/sdlc-meta/spec-architect/ALIAS.md` |
| `finance-accounting/finance` | **Retained**: namespace for 17 routed finance aliases (`finance_canonical_duplicates`) | unchanged |
| `sdlc-meta/references` | **Retained**: shared reference folder linked from `ai-agent-runtime-architecture` | unchanged |

- 183 files moved; every emptied folder removed with `os.rmdir` (refuses non-empty); no file
  deleted. The move plan and the rmdir log are in the M10-06 evidence folder of
  `chwezi-engine-agents`.
- Relative links were rewritten by resolving each token against the file's old location. On the
  active roots, 348 previously broken relative file references now resolve and none newly break
  (checker in the evidence folder); about 420 older broken tokens elsewhere remain and are not
  part of this disposition.
- Alias files: 76 -> 78 (`docs/skill-routing-index.md`). Active skills: 167, unchanged.
