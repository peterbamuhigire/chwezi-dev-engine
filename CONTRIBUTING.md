# Contributing

Read `AGENTS.md` (or its `CLAUDE.md` bridge) first: it is the router and states
the engine's rules, including the catalogue cap (150–180 active skills), the
skill-authoring standard (`skills/sdlc-meta/skill-writing`) and the
no-book-extraction rule.

## Before you open a pull request

Install the pinned dependencies once (`python3 -m pip install -r
requirements-ci.txt`: pytest and PyYAML; Node.js is needed for the hook tests).
Then run the checks the CI workflow (`.github/workflows/skill-guardrails.yml`)
runs, from the repository root, and paste the real results:

```
python3 -X utf8 scripts/skill_catalog_guardrails.py
python3 -X utf8 -m unittest tests/test_skill_catalog_guardrails.py
python3 -X utf8 -m pytest tests -q -p no:cacheprovider
python3 -X utf8 scripts/routing_smoke_test.py --min-rank1 89 --lint-fixtures
python3 -X utf8 scripts/routing_smoke_test.py --coverage --max-zero-positive 1
python3 -X utf8 scripts/routing_smoke_test.py --collisions --collision-gate --threshold 0.5
python3 -X utf8 scripts/validate_engine_control_plane.py
python3 -X utf8 scripts/check_source_register.py
node hooks/test-destructive-bash-gate.js && node hooks/test-plugin-hook-config.js
python3 -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --all
git diff --check
```

The README section "Verify" lists what each check needs and the results measured
on Linux. Adding a skill also needs a positive routing fixture in
`scripts/routing_fixtures.yml`; the ratchets in `docs/quality-gates/` may only
shrink. A check you could not run is reported as `NOT ASSESSED` with the reason,
never as a pass. Use British English.

## If you are an AI agent

1. **Disclose** in the pull request your model or runtime label, the harness
   (for example Claude Code or Codex CLI) and the plugins or skill packs loaded
   in the session.
2. **Search first.** Look through open and closed pull requests and issues for
   the same problem, and link what you found.
3. **One problem per pull request.** No bundled fixes, renames or formatting
   sweeps.
4. **Run the validators above** and report any you could not run as
   `NOT ASSESSED`.
5. **No book extractions and no copied third-party text.** Paraphrase ideas and
   attribute them with licence, URL and commit.

Model policy is not reopened by contributions: Codex runs on GPT-6 Luna with
high reasoning, Astra only when Peter selects it explicitly, and other runtimes
keep their own configuration (`.codex/model-policy.md`).

The pull request template (`.github/pull_request_template.md`) carries the
disclosure block.

Adapted in paraphrase from obra/superpowers `AGENTS.md` (MIT,
https://github.com/obra/superpowers, commit
8ca22dba9a94f28898bbce59f2537ff4d87c747d). No text copied.
