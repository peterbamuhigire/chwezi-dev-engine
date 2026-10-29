# Backlog and retained decisions

Date: 2026-10-29. Scope is this Dev Engine checkout. Due dates are review targets, not
claims that a future action has been scheduled or completed.

| ID / priority | Observed gap and cause | Kept change and acceptance evidence | Risk / rollback | Owner / target |
|---|---|---|---|---|
| D01 / P0 | Next.js examples trusted a role cookie, used a global users cache and unscoped read, and showed an unchecked mutation. The examples made UI-level and routing checks look decisive. | Replace unsafe examples with server-only DAL guidance and a tenant invoice example; structural validator rejects the known unsafe patterns; positive and owned-negative routing fixtures. | Illustrative schema may not match an application. Roll back only if the reference remains fail-closed; update examples and tests together. | Dev Engine / 2026-11-03 advisory review |
| D02 / P1 | Next examples used synchronous request params and removed `request.ip` / `request.geo` fields. Guidance had not followed the Next.js 16 upgrade. | Use async request APIs and `proxy.ts`; cite the official version guide and retain missing framework build as `NOT_ASSESSED`. | Framework contracts can change; re-check the official guide before adoption. | Dev Engine / 2026-11-03 |
| D03 / P1 | Android guidance named API 35 as the current Play target and asserted that omitting one helper necessarily crashes. | Separate Play submission target from compatibility API, remove unsupported crash assertion, cite official Android/Kotlin/Compose source records, and provide a screen excerpt. | No Gradle project or emulator test; keep those claims unassessed. | Dev Engine / 2026-11-29 |
| D04 / P1 | The reviewed PHP task lacked a reproducible cross-layer tenant listing proof. | Add synthetic PHP/OpenAPI/Next.js/Compose slice, illustrative MySQL DDL, and PDO SQLite test. Preserve the explicit SQLite-versus-MySQL limitation. | Fixture is not production-ready. Remove the slice as a unit if its boundary assertions fail. | Dev Engine / 2026-11-05 |
| D05 / P1 | Runtime release guidance did not make exact package/build advisory applicability an explicit check. | Add PHP and PostgreSQL currentness steps and official advisory/support sources; record package-specific applicability as unassessed. | Advisories are time-sensitive and package backports vary. Re-check the listed official pages before runtime selection. | Dev Engine / 2026-11-05 |
| D06 / P1 | Native Codex prompt-input default did not expose all plugin manifest paths in the recorded offline check. | Document verified invocation-level `skills.max_context_tokens=10000` and preserve the default-load limitation; do not mutate user configuration ([native check and official source](04-validation-record.md)). | Host/account behavior can differ. Re-run native prompt-input for the target package/runtime. | Dev Engine / 2026-11-29 |
| D07 / P1 | Portable Codex package/marketplace shape and the hard checkout/package count had no repository-owned regression checks. | Add root `plugin.json`, local marketplace entry, path/manifest assertions and a budget checker with an over-cap failure test. | Shape tests do not establish public listing acceptance or an archive build. Roll back manifest with its tests if native validation rejects it. | Dev Engine / 2026-11-29 |
| D08 / P2 | Routing needed task-positive and task-negative coverage for the changed PHP/Next routes. | Add five PHP and four Next routing cases, including owned negatives; routing lint and full lexical proxy run are clean (counts are in the [validation record](04-validation-record.md)). | Lexical routing is not a live model evaluation. Revisit if a later runtime benchmark disagrees. | Dev Engine / next route-fixture review |
| D09 / P1 | The full historical source register still has `27` overdue records, and the metadata gate reports them ([validation record](04-validation-record.md)). The cycle re-verified only selected sources, preserving historical records and avoiding invented refreshes. | In a later bounded source-reconciliation pass, verify each overdue claim or mark it superseded/`NOT_ASSESSED`, preserve provenance, then rerun the full validator. The selected cycle-source subset already has zero metadata/date findings; it does not make the full register current. | Refreshing records without checking source content would create false currency. Keep old snapshots and narrow any unsupported skill wording. | Dev Engine / 2026-11-05 |

Nine items were retained; no unrelated engine or canonical doctrine files were changed.
Priority labels are ordering decisions, not measured risk probabilities.

## Root-cause trail (D01; inference)

1. Why could a tenant example be copied unsafely? It treated a role cookie as authority,
   read private rows without tenant scoping, and cached users under a global key.
2. Why were those decisions presented? The snippets compressed an end-to-end flow without
   preserving the trust boundary at each server entry point.
3. Why did review not stop them earlier? The skill had no focused, owned negative fixture
   for the role-cookie and global-cache patterns.
4. Why was the skill gap actionable now? The practitioner task and flawed review specimen
   exposed these exact paths in the frozen preparation record.
5. Why was the remediation scoped to examples and guards? The observed failure was in
   copyable guidance; no live application was available to validate a broader code change.

This chain is a causal interpretation of the source and fixture observations, not a
measured proof of why a human or model produced those examples.

## Target ratchet

The user's `95/100` aspiration remains a later target. The [final assessment](05-final-report.md)
shows the measured opinion scores and the user's `45`-point reporting cap; backlog
acceptance is local and does not imply that the overall target is met.
