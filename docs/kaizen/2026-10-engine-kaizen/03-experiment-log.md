# Experiment and change log

## Frozen setup

The baseline was frozen at `22b8e7d0a9db642a0714c09c1716cdb21e6a5ae9` before source
changes. Prepared command output and observations are retained outside the repository
under `/tmp/chwezi-portfolio-kaizen/dev-prep/`. See [scope](00-scope-and-evidence.md)
and [baseline scorecard](01-baseline-scorecard.md).

## Hypotheses, outcomes and reversibility

| Experiment | Hypothesis | Outcome | Evidence / disposition |
|---|---|---|---|
| Next.js tenant boundary | Replacing role-cookie and global-cache examples with server-owned membership authorization, tenant predicates, DTO projection and private responses will make unsafe patterns less copyable. | Structural regression and failure-path tests pass; the route fixtures lint and route. No live Next build or app schema was available. | Retain as reference-only. See `tests/test_tenant_invoice_example.py`, `scripts/validate_tenant_invoice_example.py`, and `examples/tenant-invoice-listing/README.md`. |
| PHP read-only slice | A small executable PHP fixture can prove its own tenant/auth/input/escaping invariants while keeping database deployment limits explicit. | PHP CLI run reports `15 checks passed` on PDO SQLite; the synthetic test does not prove MySQL behavior. | Retain with SQLite limitation and illustrative MySQL migration. Revert the example as one unit if its test fails. |
| Android state presentation | A UI excerpt with explicit loading, denied, failed and ready states is more actionable than generic layout advice. | Source and structural checks only; Gradle build, Compose preview and emulator behavior were not assessed. | Retain as an excerpt, not a verified Android application. |
| Native discovery budget | Explicit invocation-level context budget can test whether the plugin manifest inventory fits initial prompt input without changing user configuration. | Default run loaded `130/165` declared paths; explicit Luna/high + `skills.max_context_tokens=10000` loaded `165/165` in the isolated offline run. | Document invocation and default limitation; no raw prompt body stored in the repo. Logs: `/tmp/chwezi-portfolio-kaizen/native-discovery/chwezi-dev-engine/summary.json` and `/tmp/chwezi-portfolio-kaizen/native-discovery-budget/chwezi-dev-engine/summary.json`. |
| File cap guard | The package-oriented inventory and checkout inventory can both be checked at the repository boundary, and an over-cap test can verify failure behavior. | Current checkout run passes both counts; test creates an over-cap throwaway tree and expects nonzero exit. A checkout count including `.git` is distinct from an archive count. | Retain. Public archive acceptance remains unassessed. |
| Official currentness | Current framework/runtime guidance and advisories can be tied to exact official snapshots before changing examples. | Records added for Next.js, Android/Play, Kotlin/Compose, PHP, PostgreSQL, MySQL, and Codex package/context guidance. Future advisory details and environment-specific package applicability remain open. | Retain selected records; re-check short review dates in the source register. |

## Rollback map

The Next.js skill/reference/fixture changes can be reverted together. The synthetic slice
is self-contained under `examples/tenant-invoice-listing/` and can be removed with its
validator and test if it proves misleading. Package manifests and file-budget code are
independent of the runtime examples. The source register and dated report should remain
if any source-backed guidance is rolled back, with the disposition recorded.
