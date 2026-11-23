# K3 ticket-import example

This original, local-only SQLite fixture demonstrates duplicate event delivery
through a public command-line caller. `cli.py` is the entry point. It accepts
`--db PATH --event ID --ticket ID --status STATUS`; `--fail-before-history`
injects a failure after the fixed implementation records the event key but
before it inserts history. Python's standard library is the only dependency.

## Fixture and variants

Create a fresh database for each run using `legacy_fixture.sql`. The schema is
`tickets(ticket_id, status)`, `history(history_id, ticket_id, status,
source_event_id, created_at)` and `delivered_events(event_id, ticket_id,
status)`. Ticket `T1` starts `open` and already has one history row whose
`source_event_id` is `NULL`; this is pre-existing history from before event IDs
were introduced.

The normal command uses the fixed implementation. To expose alternatives on
the same public path, pass `--implementation baseline` or
`--implementation ticket-level-dedupe`:

| Variant | Behavior | K3 finding |
|---|---|---|
| `baseline` | Appends a history row for every delivery. | Fails identical E7 retry by creating a duplicate row. |
| `ticket-level-dedupe` | Suppresses any delivery when the ticket already has history. | Incorrectly suppresses E7 because the fixture has legacy history; also cannot accept distinct E8. |
| `fixed` (default) | Stores the event key, payload, history row and ticket update in one transaction. | Replays identical data successfully; conflicts on key reuse with a changed payload. |

The alternative selector is solely for demonstrating incorrect implementations;
it is not an application configuration surface.

## Independent check procedure

Use a new fixture database for each scenario. Run commands from the repository
root; set `EXAMPLE` to this directory and `DB` to a new local path. For example,
on PowerShell:

```powershell
$EXAMPLE = 'skills/sdlc-meta/ai-assisted-development/examples/e05-k3'
$DB = Join-Path $env:TEMP 'k3-fixed.sqlite'
python -c "import sqlite3,sys; c=sqlite3.connect(sys.argv[1]); c.executescript(open(sys.argv[2], encoding='utf-8').read()); c.close()" $DB "$EXAMPLE/legacy_fixture.sql"
```

Invoke the normal caller:

```powershell
python "$EXAMPLE/cli.py" --db $DB --event E7 --ticket T1 --status review
python "$EXAMPLE/cli.py" --db $DB --event E7 --ticket T1 --status review
python "$EXAMPLE/cli.py" --db $DB --event E8 --ticket T1 --status closed
```

Expected: the first command reports `created`, the retry reports `replayed`,
and E8 reports `created`. Query `history` and `delivered_events`: history has
three rows total (the original legacy row, one E7 row and one E8 row), and the
two event rows have their matching payloads. The final ticket status is
`closed`.

Check changed-payload conflict by reusing E7 with `--status closed`. It exits
3, prints `conflict: event 'E7' was already used with a different payload`,
and leaves history, event key and ticket unchanged.

Check recovery with a separate fresh fixture. Run E7 with
`--fail-before-history`: it exits 4 with
`error: injected failure before history insert`. Query state: no E7 event key,
no E7 history row, one legacy history row, and ticket status `open`. Retry E7
without injection; it reports `created` and yields one E7 event and one E7
history row. This demonstrates rollback of the key and later completion.

Run the two negative controls against separate fresh fixture databases. For
`baseline`, submit E7 twice and query history: two E7 rows show the original
defect. For `ticket-level-dedupe`, submit E7 then E8: both report
`suppressed`, and the legacy row remains the only history row. The CLI is
intentionally public in both cases so a check cannot pass by calling a helper
that bypasses the entry point.

An independent reviewer should own the oracle and inspect persisted SQLite
rows, exit status and stderr, rather than accepting the JSON message alone.
Concurrent identical calls are serialized with SQLite `BEGIN IMMEDIATE`; this
fixture's command-level concurrency behavior is not independently stress
tested here. This example is a single-process local teaching fixture, not a
production service contract or a performance measurement.
