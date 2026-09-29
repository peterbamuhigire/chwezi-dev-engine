# Delivery worker

## Record parser (`worker/parser.py`)

`parse_record(text) -> dict[str, str]` reads `key=value` pairs separated by `;`. Whitespace around
keys and values is trimmed; a trailing `;` is allowed. Keys match `[a-z][a-z0-9_]*`. Values may be
empty and may contain any character except `;`. Parsing must stay linear in the input length:
records arrive from partner systems and are untrusted.

Failures raise `ParseError` with a `code` and the 0-based `position` of the offending pair:

| code | meaning |
|---|---|
| `empty` | the record is empty or whitespace only |
| `missing_separator` | a pair has no `=` |
| `bad_key` | a key does not match the key pattern |
| `duplicate_key` | a key appears twice |

Operations dashboards group failures by `code`, so the codes are part of the contract.

## Retry state machine (`worker/retry.py`)

`RetryMachine(tracer, clock, max_attempts=4, delay=1.0).run(operation) -> str` calls `operation()`
and returns the terminal state name.

States: `IDLE`, `SENDING`, `BACKOFF`, `SUCCEEDED`, `FAILED_PERMANENT`, `EXHAUSTED`.

| from | event | to |
|---|---|---|
| IDLE | start | SENDING |
| SENDING | success | SUCCEEDED |
| SENDING | `PermanentFailure` | FAILED_PERMANENT |
| SENDING | `TransientFailure`, attempts left | BACKOFF |
| SENDING | `TransientFailure`, no attempts left | EXHAUSTED |
| BACKOFF | delay elapsed | SENDING |

Every transition calls `tracer.span("retry.transition", source=..., target=..., attempt=...)`. The
on-call runbook reads these spans; removing one blinds the runbook.
