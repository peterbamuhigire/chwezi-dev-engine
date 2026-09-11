# Source Inventory

## Identity and coverage

The comparison source contains 164 files. Every relative path was compared with a fresh upstream
clone; all content matched after CRLF/LF normalisation. The study inventoried all 37 skills and all
support-file relationships, structurally checked all 37 Codex adapters and 25 promoted docs pages,
and directly inspected the critical workflow bodies and their decision-rich supporting files.

| Class | Count | Coverage |
| --- | ---: | --- |
| `SKILL.md` | 37 | All inventoried and dispositioned |
| Promoted skills | 25 | All matched to plugin entry, docs page, and adapter |
| Human docs pages | 25 | All section-scanned; representative pages read directly |
| `agents/openai.yaml` | 37 | All invocation states checked; zero mismatches |
| Total Markdown files | 112 | Path and role inventory complete |
| Total repository files | 164 | Exact fresh-clone content comparison complete |

## Root and governance files inspected

- `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `README.md`, `CHANGELOG.md`, `LICENSE`.
- `package.json`, `package-lock.json`.
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`.
- `.agents/install-block.md`, `.agents/invocation.md`, `.agents/writing-docs.md`.
- `.agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md`.
- `.agents/adr/0002-ship-as-a-claude-code-plugin.md`.
- `.out-of-scope/mainstream-issue-trackers-only.md`.
- `.out-of-scope/question-limits.md`.
- `.out-of-scope/setup-skill-verify-mode.md`.
- `.github/workflows/release.yml` and `.changeset/*`.
- `scripts/list-skills.sh`, `scripts/link-skills.sh`, `scripts/sync-plugin-version.mjs`.

## Engineering skills and support files

| Skill | Decision-rich support files |
| --- | --- |
| `ask-matt` | `PHASE-BOUNDARIES.md`, Codex adapter |
| `codebase-design` | `DEEPENING.md`, `DESIGN-IT-TWICE.md`, adapter |
| `code-review` | Adapter |
| `diagnosing-bugs` | `scripts/hitl-loop.template.sh`, adapter |
| `domain-modeling` | `CONTEXT-FORMAT.md`, `ADR-FORMAT.md`, adapter |
| `grill-with-docs` | Adapter |
| `implement` | Adapter |
| `improve-codebase-architecture` | `HTML-REPORT.md`, adapter |
| `prototype` | `LOGIC.md`, `UI.md`, adapter |
| `research` | Adapter |
| `resolving-merge-conflicts` | Adapter |
| `setup-matt-pocock-skills` | tracker templates for GitHub, GitLab and local Markdown; `domain.md`; `triage-labels.md`; adapter |
| `tdd` | `tests.md`, `mocking.md`, adapter |
| `to-spec` | Adapter |
| `to-tickets` | Adapter |
| `triage` | `AGENT-BRIEF.md`, `OUT-OF-SCOPE.md`, adapter |
| `wayfinder` | Adapter |
| `wizard` | `template.sh`, adapter |

## Productivity skills and support files

| Skill | Decision-rich support files |
| --- | --- |
| `grilling` | Adapter |
| `grill-me` | Adapter |
| `handoff` | Adapter |
| `teach` | `MISSION-FORMAT.md`, `LEARNING-RECORD-FORMAT.md`, `GLOSSARY-FORMAT.md`, `RESOURCES-FORMAT.md`, adapter |
| `to-questionnaire` | Adapter |
| `wait-what` | Adapter |
| `writing-for-agents` | `SKILL-MECHANICS.md`, adapter |

## In-progress skills

- `claude-handoff`
- `implement-spec`
- `loop-me`
- `retro`
- `setup-ts-deep-modules` plus `dependency-cruiser.config.cjs`
- `writing-fragments`
- `writing-beats`
- `writing-shape`

Each has a Codex adapter. These are public beta capabilities but are excluded from the promoted
Claude plugin set.

## Miscellaneous skills

- `git-guardrails-claude-code` plus `scripts/block-dangerous-git.sh`
- `migrate-to-shoehorn`
- `scaffold-exercises`
- `setup-pre-commit`

These are installable source capabilities but deliberately omitted from the promoted plugin and
root public routing.

## Human documentation mechanism

The `docs/engineering/` and `docs/productivity/` trees contain one page per promoted skill. The
repository contract requires `What it does`, `When to reach for it`, `Common questions`, `It's
working if`, and `Where it fits`. Structural scan found one exception: `docs/productivity/wait-what.md`
lacks `Common questions`.

The pages act as a distributed human router and use absolute published URLs. This is valuable for a
small catalogue. Chwezi should generate routine index material and hand-write only decision-rich
guidance to avoid multiplying maintenance across 179 active skills.

## Source repository verification result

```text
download_files=164
fresh_files=164
normalised_differences=0
upstream_head=3cca18b368ae95cdbdebbff572ccafa662551015
upstream_date=2026-09-04T09:43:27+01:00
upstream_subject=Merge pull request #1025 from mattpocock/chore/link-skills-exclude-misc
```

The temporary verification clone was created under the user's OS temporary directory. It is not a
canonical engine checkout and must not be registered as an active skill root.
