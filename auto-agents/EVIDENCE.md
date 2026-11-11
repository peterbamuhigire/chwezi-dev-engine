# Evidence and second review: 2026-11-11

Scope: the local unattended driver and its use by Codex and Claude Code. The user-provided driver-pattern PDF is the baseline, not evidence that a real long-running run has succeeded. The local files by Nicosia, Volkhover, Bhati and the Claude Code guide were inventoried and text-extracted; targeted passages informed task decomposition, feedback loops, constraints and verification. Comprehensive review of all book content is NOT_ASSESSED. They are not evidence for current vendor capabilities.

Current, primary sources accessed 2026-11-11 (review when the CLI changes; page publication date not established):

- https://developers.openai.com/blog/codex-as-a-platform : `codex exec` is described as a noninteractive interface. Local `codex exec --help` also exposes it. Scope: CLI entrypoint, not proof of runtime permissions.
- https://code.claude.com/docs/en/troubleshooting : noninteractive permission behavior can differ by configuration. Scope: permission failure diagnosis, not an unconditional grant.
- https://developers.openai.com/api/docs/guides/agents-api/environments/security : agent-generated code can access the environment granted to it. Scope: the documented environment; a Git worktree alone is not a sandbox.
- https://developers.openai.com/api/docs/models and https://docs.anthropic.com/en/docs/about-claude/model-deprecations were inspected for model currency. Account/runtime model catalogue and comparable task-fit, cost, latency and quality evidence were not established. Model-currentness: NOT_ASSESSED. No model-policy change is proposed. The local model-policy checker reported drift; no automated repair was applied because the engine's medium-effort setting conflicts with the user's high-effort policy.

Second-review findings and disposition:

1. A committed DONE marker after a failed independent gate could otherwise be mistaken for successful completion after restart. The driver records the accepted and pending commits, and directs a fresh session to repair a failed gate without treating the completion marker as accepted. Regression: failed gate followed by restart and repair. Unknown unverified commits still block.
2. Windows can resolve an extensionless npm shim that CreateProcess cannot execute. Prefer `.cmd` on Windows; `codex.cmd --version` was exercised locally. Live Codex and Claude agent sessions remain NOT_ASSESSED.
3. Existing driver branches without an accepted checkpoint must not be silently treated as verified. The driver blocks for inspection.
4. The worktree is isolation from the operator's checkout, not a permission boundary. Publishing is configurable and disabled by default; the runtime's own policy remains in force. A non-force push and command exit statuses do not prove that the verification commands are adequate or that external side effects were absent.
5. Completion, failure, stop, lock, rate-limit retry, gate failure/restart/repair and publication to a disposable local remote were exercised by deterministic tests. Production safety, process-tree termination, real login/quota recovery, multi-hour runtime, cross-process resource isolation and application-level test coverage remain NOT_ASSESSED.

Measure for a future supervised pilot: completed slices, failed checks, blocked runs, unverified commits and independently reviewed regressions per run. The EWMA idea in the supplied pattern is a candidate; retry backoff is implemented but has no measured live-run benefit. Do not claim speed or safety improvements without a comparable baseline.

## Managed update review (2026-11-11)

A versioned manifest and managed updater preserve project configuration and plans, reject changed managed files and occupied new paths, and share the driver lock. An interrupted update retains a journal and requires inspection. A second pass found that raw hashes drift under Git CRLF conversion; the manifest now records its hash mode and normalises supported text line endings, while accepting the previous raw mode for migration. Tests cover modified targets, new-file collisions, removals, interrupted journals, locks and Git checkout behavior. Hashes detect accidental drift and do not authenticate a source. Process-crash atomicity across all files, adversarial concurrent writes and live-agent deployment remain NOT_ASSESSED.

## Follow-up review (2026-11-11)

A verification command could previously create a clean commit or change branches after the agent session, causing a different revision to be published or checkpointed. The driver now blocks if a verification command changes HEAD or the driver branch, and pushes the verified commit by object ID. Regression fixtures exercise both cases. Configuration also rejects non-finite runtime and retry limits. These checks do not constrain an adversarial concurrent process or establish that a configured verification command is meaningful.

Volkhover (2026), *Agentic Spec-Driven Development*, Korostyshevskiy (2026), *Claude Code: The Definitive Guide to Agentic Development*, and Bhati (2026), *Agentic AI in the Software Development Lifecycle*, inform the plan template: persistent outcomes, boundaries, acceptance examples, ordered slices, and a compact recovery handoff. The Bhati work is an under-review preprint; quantitative claims and vendor capabilities were not adopted as facts. The Claude Markdown edition omits reference tables; check original and current official documentation for CLI behaviour. The separate optimization anthology has not been read in full.

As of 2026-11-11, the official [Claude programmatic-use documentation](https://code.claude.com/docs/en/headless) supports the non-interactive CLI entry point; runtime permissions and live unattended use remain unassessed. The [OpenAI model catalogue](https://developers.openai.com/api/docs/models) and [Anthropic model overview](https://platform.claude.com/docs/en/models/overview) were consulted; task-fit, cost, latency and quality comparisons for this portfolio are NOT_ASSESSED. Retain the owner-authorised model policy; no model change is proposed.
