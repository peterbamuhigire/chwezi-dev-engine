---
name: code-tour
description: Create CodeTour `.tour` files — persona-targeted, step-by-step walkthroughs with real file and line anchors. Use for onboarding tours, architecture walkthroughs, PR tours, RCA tours, and structured "explain how this works" requests.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  origin: "Adapted from affaan-m/ECC skills/code-tour/SKILL.md"
---

> Inactive alias. Route to `skills/sdlc-meta/doc-architect` through `docs/skill-aliases.yml`; this file is retained for historical content.

# Code Tour

Create **CodeTour** `.tour` files for codebase walkthroughs that open directly to real files and
line ranges. Tours live in `.tours/` in the target project and are meant for the CodeTour format
(`microsoft/codetour`), not ad hoc Markdown notes.

A good tour is a narrative for a specific reader: what they are looking at, why it matters, and
what path they should follow next.

Only create `.tour` JSON files. Do not modify source code as part of this skill.

## When to Use

- the user asks for a code tour, onboarding tour, architecture walkthrough, or PR tour
- the user says "explain how X works" and wants a reusable guided artifact, not a one-off answer
- the user wants a ramp-up path for a new engineer, reviewer, or client handover
- the task is better served by a guided sequence than a flat summary

Examples: onboarding a new maintainer onto a client's WAMP/PHP codebase; architecture tour for one
service or package; PR-review walkthrough anchored to changed files; RCA tour showing the failure
path; security review tour of trust boundaries and key checks.

## When NOT to Use

| Instead of code-tour | Use |
|---|---|
| A one-off explanation in chat is enough | answer directly |
| The user wants prose docs, not a `.tour` artifact | edit the project's own docs |
| The task is implementation or refactoring | do the implementation work |
| The task is broad codebase onboarding without a tour artifact | a written onboarding doc instead |

## Workflow

### 1. Discover

Explore the repo before writing anything: README and entry points, folder structure, relevant
config files, and the changed files if the tour is PR-focused. Do not start writing steps before
you understand the shape of the code.

### 2. Infer the reader

| Request shape | Persona | Suggested depth |
|---|---|---|
| "onboarding", "new joiner" | `new-joiner` | 9–13 steps |
| "quick tour", "vibe check" | `vibecoder` | 5–8 steps |
| "architecture" | `architect` | 14–18 steps |
| "tour this PR" | `pr-reviewer` | 7–11 steps |
| "why did this break" | `rca-investigator` | 7–11 steps |
| "security review" | `security-reviewer` | 7–11 steps |
| "explain how this feature works" | `feature-explainer` | 7–11 steps |
| "debug this path" | `bug-fixer` | 7–11 steps |

### 3. Read and verify anchors

Every file path and line anchor must be real: confirm the file exists, confirm line numbers are in
range, verify exact selection blocks, and prefer a pattern-based anchor for volatile files. Never
guess line numbers.

### 4. Write the `.tour`

Write to `.tours/<persona>-<focus>.tour`. Keep the path deterministic and readable.

### 5. Validate

Before finishing: every referenced path exists; every line/selection is valid; the first step is
anchored to a real file or directory; the `ref` points at a revision that actually has every file
the tour references (see below); the tour tells a coherent story rather than listing files.

## The `ref` Field

`ref` ties the tour to a git branch or commit. When `ref` is not the branch the reader has checked
out, CodeTour opens each step's file from that revision in git, not from disk. If a file is not in
that revision, the step will not open — the reader sees *"The editor could not be opened because the
file was not found"* even though the file exists on disk. The tour and its comments still render, so
the real cause is easy to miss.

| Tour type | Set `ref` to |
|---|---|
| PR tour | the PR branch — never the base branch |
| Onboarding / architecture | the branch the reader will be on (often `main`), or leave it out |
| Not sure | leave `ref` out, so CodeTour reads files straight from disk |

The PR case is the common trap: a PR usually adds new files that do not exist on the base branch
yet. Pointing `ref` at the base makes every step on a new file fail to open. Before finishing,
confirm each step's file actually exists at the chosen `ref`.

## Step Types

**Content** (use sparingly, usually only for a closing step):

```json
{ "title": "Next Steps", "description": "You can now trace the request path end to end." }
```

Do not make the first step content-only.

**Directory** (orient the reader to a module):

```json
{ "directory": "src/services", "title": "Service Layer", "description": "The core orchestration logic lives here." }
```

**File + line** (the default step type):

```json
{ "file": "src/auth/middleware.ts", "line": 42, "title": "Auth Gate", "description": "Every protected request passes here first." }
```

**Selection** (when one code block matters more than the whole file):

```json
{
  "file": "src/core/pipeline.ts",
  "selection": { "start": { "line": 15, "character": 0 }, "end": { "line": 34, "character": 0 } },
  "title": "Request Pipeline",
  "description": "This block wires validation, auth, and downstream execution."
}
```

**Pattern** (when exact lines may drift):

```json
{ "file": "src/app.ts", "pattern": "export default class App", "title": "Application Entry" }
```

**URI** (for PRs, issues, or docs when helpful):

```json
{ "uri": "https://github.com/org/repo/pull/456", "title": "The PR" }
```

## Writing Rule: SMIG

Each description should answer:
- **Situation**: what the reader is looking at
- **Mechanism**: how it works
- **Implication**: why it matters for this persona
- **Gotcha**: what a smart reader might miss

Keep descriptions compact, specific, and grounded in the actual code — never generic.

## Narrative Shape

Unless the task clearly needs something different: orientation → module map → core execution path
→ edge case or gotcha → closing/next move. The tour should feel like a path, not an inventory.

## Example

```json
{
  "$schema": "https://aka.ms/codetour-schema",
  "title": "API Service Tour",
  "description": "Walkthrough of the request path for the payments service.",
  "ref": "main",
  "steps": [
    { "directory": "src", "title": "Source Root", "description": "All runtime code for the service starts here." },
    { "file": "src/server.ts", "line": 12, "title": "Entry Point", "description": "The server boots here and wires middleware before any route is reached." },
    { "file": "src/routes/payments.ts", "line": 8, "title": "Payment Routes", "description": "Every payments request enters through this router before hitting service logic." },
    { "title": "Next Steps", "description": "You can now follow any payment request end to end with the main anchors in place." }
  ]
}
```

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| Flat file listing | Tell a story with dependency between steps |
| Generic descriptions | Name the concrete code path or pattern |
| Guessed anchors | Verify every file and line first |
| Too many steps for a quick tour | Cut aggressively |
| First step is content-only | Anchor the first step to a real file or directory |
| Persona mismatch | Write for the actual reader, not a generic engineer |

## Best Practices

- keep step count proportional to repo size and persona depth
- use directory steps for orientation, file steps for substance
- for PR tours, cover changed files first
- for monorepos, scope to the relevant packages instead of touring everything
- close with what the reader can now do, not a recap

## Related Skills

- `sdlc-meta/council` — when the tour's scope or audience is itself ambiguous
- official upstream format reference: `microsoft/codetour`
