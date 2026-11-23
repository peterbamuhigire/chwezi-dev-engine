# E05 implementation notes

Acceptance target: AC-E05, using casebook K3. This evidence describes the
public coding example and its self-checks; independent acceptance and review
are assigned to the operator.

## Entry point and persisted fixture

The public caller is
`skills/sdlc-meta/ai-assisted-development/examples/e05-k3/cli.py`. Initialize
a fresh SQLite database from that directory's `legacy_fixture.sql`. The
fixture includes ticket `T1` in `open` status and one pre-event-ID history row
with a null event reference. See the example README for the exact commands and
SQL observations.

The caller defaults to `--implementation fixed`; the explicit demonstration
variants are `baseline` and `ticket-level-dedupe`. All variants use the same
entry point and database fixture. The baseline duplicates history on replay.
The ticket-level alternative suppresses E7 due to the pre-existing legacy row
and suppresses distinct E8. The fixed path uses an event-ID primary key,
compares the full ticket/status payload, and commits the key, history and
ticket state together. Changed-payload reuse exits 3. Injected failure exits 4
and rolls back all event effects.

## Self-check record

| Check | Expected observation |
|---|---|
| Fixed E7, identical E7, then E8 | `created`, `replayed`, `created`; legacy row remains; exactly one history row per event. |
| Reuse E7 with another status | Exit 3 and unchanged persisted state. |
| `--fail-before-history` on new E7, then retry | Exit 4; no event key/history/state change after failure; retry commits one complete event. |
| Baseline E7 twice | Two E7 history rows. |
| Ticket-level dedupe E7 then E8 | Both suppressed by the legacy history; no new event history. |
| Unknown ticket | Exit 4 and no database mutation. |

The author ran the command scenarios against fresh temporary fixture
databases on 2026-11-23. Results are author self-checks, not independent
acceptance evidence. The operator owns black-box acceptance through the CLI,
separate diff review and any independent concurrent-delivery check.

## Scope and remaining limitations

Changed surfaces are the AI-assisted development skill, its K3 example and
delivery guide, the coding-agent optimization guidance, and this evidence
directory. The active JAD worktree and source repository were not modified; no
commit or push was performed. This minimal example does not establish a
production API contract, cross-process stress result, workload performance,
or behavior beyond the fixture schema. Those claims remain `NOT_ASSESSED`.
