# E05 evidence receipt

- **Acceptance ID:** AC-E05
- **Source revision:** `8d32481d567aed20bd6b6a8ff45d20ef4dc32adc` (detached isolated checkout).
- **Input:** Synthetic K3 in `docs/plans/ai-engine-kaizen/casebook.md`; fixture `skills/sdlc-meta/ai-assisted-development/examples/e05-k3/legacy_fixture.sql` contains T1/open and one legacy history row with a null event ID.
- **Scope:** `skills/sdlc-meta/ai-assisted-development/SKILL.md`, `skills/sdlc-meta/ai-assisted-development/examples/e05-k3/`, `skills/ai/coding-agent-optimization/SKILL.md`, and `docs/plans/ai-engine-kaizen/evidence/E05/`. No source repository or active JAD worktree edits, commit or push.
- **Receipt digest:** SHA-256 of this file is in `receipt.sha256`. SHA-256 of the machine-readable self-check sidecar `result.json` is recorded below after finalization.

## Reproduction

From repository root, initialize a fresh database from `legacy_fixture.sql` as shown in the example README, then use the public caller:

```powershell
python skills/sdlc-meta/ai-assisted-development/examples/e05-k3/cli.py --db PATH --event E7 --ticket T1 --status review
python skills/sdlc-meta/ai-assisted-development/examples/e05-k3/cli.py --db PATH --event E7 --ticket T1 --status review
python skills/sdlc-meta/ai-assisted-development/examples/e05-k3/cli.py --db PATH --event E8 --ticket T1 --status closed
```

The CLI selector `--implementation baseline|ticket-level-dedupe|fixed` runs the alternatives through the same caller; `fixed` is the default. `--fail-before-history` injects the failure in a new fixed event after its key insert. The example README documents fresh-fixture setup, SQL observations and each alternative's expected failure.

## Observed result

The author self-check passed: fixed E7/E7/E8 yielded `created`, `replayed`, `created`; three total history rows retained the original legacy row, and two event keys were stored. Changed-payload E7 reuse exited 3 with `conflict: event 'E7' was already used with a different payload`, leaving state unchanged. Injected failure exited 4 with `error: injected failure before history insert`; the transaction left no E7 key or history row and retained T1/open, and retry created one complete event. Baseline produced two E7 history rows. Ticket-level dedupe suppressed E7 and E8 due to the legacy row. Unknown ticket exited 4 without changing fixture state. Two concurrent identical E7 CLI processes both exited 0 and left one key and one event history row. `tests.txt` records the self-check outcomes; `result.json` and `negative-control.json` are observed-result sidecars.

The CLI variant selector is a demonstration seam, not a production option. The expected conflict and failure messages above were observed exactly. No unexpected error occurred during the self-check. Execution timings were 2.3 s for the scenario harness and 1.8 s for syntax plus concurrency checks, including process startup; these are not performance measurements.

## Independent review and limitations

Independent operator black-box acceptance through the public CLI, separate diff review and the E05 contract sidecar update remain pending. The author's self-check is not independent acceptance. The fixture is local and minimal: no external service, production data, load/performance trial or multi-host database was used. Concurrent identical delivery was exercised locally with two processes, but broader contention, crash recovery across real storage failures, and production database semantics remain `NOT_ASSESSED`. Python version and Windows build were not captured. No ordinary device/resource inventory was run for this repository coding change.

**Fallback:** the example uses only Python's standard-library SQLite interface; if that runtime is unavailable, no result should be claimed until the same public behavior and persisted-row oracle are run under an available Python interpreter. An independent reviewer can use direct SQL queries from the README as the state oracle. **Rework:** no behavioral repair cycle was needed in the author self-check. One Markdown link target was corrected after path inspection; that documentation-only correction is reflected in the final files. The independent verification below closes review for this fixture.

## Artifact digest

`result.json` SHA-256: `c98541396c20880d1c6a18dca397d6933451741a4b4892bfc5f4fbbcaea84407`

## Independent operator execution

The operator wrote the public CLI checks separately. Run python -B docs/plans/ai-engine-kaizen/evidence/E05/independent.py skills/sdlc-meta/ai-assisted-development/examples/e05-k3 and compare independent.json. The baseline duplicated the retry, the ticket-level suppression lost the distinct event, and the fixed version passed all seven checks. It preserved the seeded history, handled conflicting payloads and recovered from an injected failure. The first review harness run hit a Windows file lock on temporary database cleanup. Explicitly closing the reviewer connections allowed a clean rerun. The assertions and implementation did not change.
