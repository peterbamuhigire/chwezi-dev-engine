# MCP Tool-Surface Evaluation

Load when you need evidence that an MCP server's tools are *usable* by a model, not only safe.
It is the usability sibling of
[least-privilege-tool-and-mcp-security.md](least-privilege-tool-and-mcp-security.md), which covers
whether a tool can be turned against its owner. This file covers whether a model that has only
the server's tools can answer realistic questions correctly.

Method adapted from anthropics/skills mcp-builder `reference/evaluation.md` (Apache-2.0,
https://github.com/anthropics/skills, commit 33375500bcea98d610eb30ce10ac4e59b89c390d).
Paraphrased for Chwezi use; no text copied.

## 1. What is being measured

The quality of an MCP server is judged by outcomes: can a model, given no other context and no
other tools, use the tool names, descriptions, input schemas and returned payloads to reach the
right answer? A server with many tools that the model misuses scores worse than a small server
whose tools are easy to chain. The evaluation therefore tests descriptions, schemas, error shapes
and payload size together.

## 2. Question design rules

| Rule | What it means in practice |
|---|---|
| About ten questions | Enough to show a pattern; few enough to freeze and verify by hand. |
| Read-only and idempotent | No question may need a state change to answer it. Any tool that mutates state is excluded from the run, not merely discouraged. |
| Independent | No question relies on another's answer or on an earlier write. Questions can run in any order or in parallel. |
| Multi-hop | Each needs at least two tool calls, where a later call depends on something learnt earlier (resolve a path to an engine, then inspect its upstream). |
| Not keyword-solvable | Phrase with synonyms or consequences, not with the literal field names the tool returns. |
| Stress the payloads | Ask about fields a model could misread: counts, booleans, error codes, identifiers, ordered lists. |
| Human-shaped | Ask what an operator would genuinely want to know, not trivia. |
| Some ambiguity allowed | A question may make tool choice hard, but must still have exactly one correct answer. |

## 3. Answer rules

- One verifiable value per question: a name, number, boolean, error code or short string. Not a
  paragraph, not an object.
- State the answer format inside the question ("answer yes or no", "give the integer") so a direct
  string comparison, after a declared normaliser (trim, lower-case), is enough.
- Answers must be stable. Build questions on a **pinned fixture workspace** (fixed commits, fixed
  identities and dates, a pinned catalogue), never on live repositories whose state drifts.
- Verify every answer once by calling the tools directly (no model), then freeze it with the date
  and the verifier command. A frozen answer changes only through a recorded review.

## 4. Running the evaluation

1. Build the pinned fixture workspace; record its build script and commit hashes.
2. Start the model with the server under test as its only tool source (for Claude Code:
   `--strict-mcp-config --mcp-config <server.json>`, with mutating tools listed in
   `--disallowedTools`). No other plugins, skills or MCP servers may load; confirm from the
   session's init record.
3. Ask each question in a fresh session. Record per question: the answer given, pass/fail by the
   declared normaliser, tool calls made, turns and errors.
4. Assert from the trace that no excluded tool was invoked. One invocation voids the run.
5. Record the model identifier, CLI or host version, server version, fixture build hash and UTC
   timestamp.

## 5. Status rules

| Situation | Status |
|---|---|
| Answer matches after normalisation | `PASS` for that pair |
| Wrong answer, no answer, or an excluded tool invoked | `FAIL` |
| Host, model, quota or credentials unavailable, or no spend authority | `NOT_ASSESSED` with the reason; never counted as pass |
| Frozen answer no longer reproduces with the direct verifier | Fix the fixture first; model results against a drifted fixture are void |

Report the pass count out of ten per model; do not mix models in one figure. Read failures as
evidence about tool descriptions, schema clarity or payload size, and change those, not the
questions.

## 6. Chwezi application

The coordinator MCP server in `chwezi-engine-agents/mcp-server` exposes `discover_engine`,
`inspect_engine`, `validate_engine` and `pull_engine_ff_only`. Its evaluation lives in
`chwezi-engine-agents/evals/mcp/`:

- `coordinator-qa.yaml` holds ten frozen QA pairs and the run configuration;
  `pull_engine_ff_only` is excluded.
- `build_fixture_workspace.py` builds the pinned workspace (synthetic repositories, fixed
  identities and dates, a pinned catalogue).
- `verify_answers.py` re-derives every frozen answer from the compiled server functions with no
  model call. Run it before any model-executed run.

Model-executed runs follow the portfolio zero-spend rule: until spend is explicitly authorised,
the model run is recorded `NOT_ASSESSED (zero-spend rule)`.
