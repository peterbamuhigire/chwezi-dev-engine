# CodeTour Walkthroughs

Parent skill: [doc-architect](../SKILL.md). Absorbed from the retired `code-tour` skill
(2026-09-24; originally adapted from `affaan-m/ECC` `skills/code-tour/SKILL.md`). The original
text is retained in `skills/sdlc-meta/code-tour/ALIAS.md`.

Load this reference when the user wants a reusable, guided walkthrough of a codebase:
onboarding tours, architecture walkthroughs, PR-review tours, root-cause tours, security-review
tours, or an "explain how this works" answer that should persist as an artefact.

Output is CodeTour `.tour` JSON in the target project's `.tours/` directory, in the format of
the `microsoft/codetour` VS Code extension. Create only `.tour` files; never modify source code
as part of a tour.

## When not to build a tour

| Situation | Do instead |
|---|---|
| A one-off chat explanation is enough | Answer directly |
| The user wants prose documentation | Edit the project's docs (see the parent skill) |
| The task is implementation or refactoring | Do the implementation work |
| Broad onboarding without a tour artefact | Write an onboarding document |

## Workflow

1. **Discover.** Read the README, entry points, folder structure, relevant configuration, and,
   for PR tours, the changed files. Do not write steps before you understand the code's shape.
2. **Infer the reader.**

   | Request | Persona | Steps |
   |---|---|---|
   | onboarding, new joiner | `new-joiner` | 9-13 |
   | quick tour | `vibecoder` | 5-8 |
   | architecture | `architect` | 14-18 |
   | tour this PR | `pr-reviewer` | 7-11 |
   | why did this break | `rca-investigator` | 7-11 |
   | security review | `security-reviewer` | 7-11 |
   | explain a feature | `feature-explainer` | 7-11 |
   | debug this path | `bug-fixer` | 7-11 |

3. **Read and verify anchors.** Every path must exist and every line or selection must be in
   range. Prefer a `pattern` anchor for volatile files. Never guess line numbers.
4. **Write** `.tours/<persona>-<focus>.tour`.
5. **Validate.** Every path exists; every line or selection is valid; the first step is anchored
   to a real file or directory; `ref` names a revision that contains every referenced file; the
   steps form a narrative rather than an inventory.

## The `ref` field

`ref` ties the tour to a branch or commit. When it differs from the reader's checked-out branch,
CodeTour opens each file from that revision in git, not from disk; a file absent from that
revision fails to open ("The editor could not be opened because the file was not found") while
the tour text still renders, which hides the cause.

| Tour type | `ref` |
|---|---|
| PR tour | The PR branch, never the base branch |
| Onboarding or architecture | The branch the reader will use (often `main`), or omit |
| Unsure | Omit it so files are read from disk |

## Step types

```json
{ "directory": "src/services", "title": "Service Layer", "description": "Core orchestration lives here." }
```

```json
{ "file": "src/auth/middleware.ts", "line": 42, "title": "Auth Gate", "description": "Every protected request passes here first." }
```

```json
{
  "file": "src/core/pipeline.ts",
  "selection": { "start": { "line": 15, "character": 0 }, "end": { "line": 34, "character": 0 } },
  "title": "Request Pipeline",
  "description": "This block wires validation, auth, and downstream execution."
}
```

```json
{ "file": "src/app.ts", "pattern": "export default class App", "title": "Application Entry" }
```

```json
{ "uri": "https://github.com/org/repo/pull/456", "title": "The PR" }
```

Content-only steps (title and description, no anchor) are for the closing step; never make the
first step content-only.

## Topology-ordered tour

Order steps by how the code is wired, not by folder name or by what you happened to read first.

1. **Score entry points.** Conventional entry files score highest: for PHP `public/index.php`,
   `index.php` and the route files (`routes/web.php`, `routes/api.php`); for Node `server.js` or
   the `main` in `package.json`; for Python `manage.py` or `__main__.py`. Add weight for files at
   the repository root and for files in the top tenth by fan-out (they import or call many
   others). A root README is the natural first stop when it explains how to run the system.
2. **Prefer fan-in on the path.** Among files reached from the entry point, visit first the ones
   many others depend on (high fan-in): the base controller, the tenant resolver, the posting
   service. A reader who understands them understands most callers.
3. **Dependency depth sets the band.** Measure depth from the chosen entry point: depth 0 to 1 is
   orientation, depth 2 to 3 is the core execution path, deeper files appear only for the edge
   case or gotcha the persona needs.
4. **Merge tight coupling.** Files that always change together or call each other in a cycle (a
   controller and its form request, a model and its observer) become one step, with a `selection`
   or `pattern` anchor in the most important file and the others named in the description.
5. **Place non-code stops after the code they explain.** Schema files, migrations, deployment
   manifests and configuration follow the code path that uses them, not the front of the tour.

Reconcile the resulting order with the persona budget in the Workflow table rather than any fixed
range: map the bands onto the persona's step count (for a `new-joiner` tour of 9 to 13 steps,
roughly 2 orientation, 6 to 8 core, 1 to 2 edge-case and 1 closing step). If the topology needs
more steps than the budget, cut the deepest band first; if it needs fewer, stop early.

(Topology ordering adapted from Egonex-AI/Understand-Anything, MIT,
https://github.com/Egonex-AI/Understand-Anything, commit
`b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0`. Paraphrased; no text copied.)

## Writing rule: SMIG

Each description answers **Situation** (what the reader is looking at), **Mechanism** (how it
works), **Implication** (why it matters to this persona), and **Gotcha** (what a capable reader
would miss). Name the concrete code path; generic descriptions are a defect.

Narrative shape: orientation -> module map -> core execution path -> edge case or gotcha ->
closing next move.

## Worked example (PHP/WAMP client handover)

```json
{
  "$schema": "https://aka.ms/codetour-schema",
  "title": "Invoice Posting Tour",
  "description": "New-joiner walkthrough of how a sales invoice reaches the ledger.",
  "steps": [
    { "directory": "app", "title": "Application Root", "description": "Runtime PHP lives here; public/ is the only web root." },
    { "file": "public/index.php", "line": 8, "title": "Front Controller", "description": "Every request boots here; tenant is resolved before routing, so no controller runs without a tenant context." },
    { "file": "app/Services/InvoicePoster.php", "pattern": "public function post", "title": "Posting Service", "description": "Wraps journal lines in one transaction. Gotcha: VAT lines are derived here, not in the controller." },
    { "title": "Next Steps", "description": "You can now trace an invoice from the form to its journal entry." }
  ]
}
```

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| Flat file listing | Tell a story where each step depends on the last |
| Generic descriptions | Name the concrete path or pattern |
| Guessed anchors | Verify every file and line |
| Too many steps for a quick tour | Cut aggressively |
| Content-only first step | Anchor it to a real file or directory |
| Persona mismatch | Write for the actual reader |
| PR tour `ref` on the base branch | Point at the PR branch |

Cover changed files first in PR tours; scope monorepo tours to the relevant packages; close with
what the reader can now do, not a recap.

## Evidence and currentness

Validate a tour mechanically before handing it over:

```powershell
python -X utf8 skills/sdlc-meta/doc-architect/scripts/validate_tour.py .tours/new-joiner-invoicing.tour --repo-root <project>
```

The script checks that every file exists at the tour's `ref` (or on disk when `ref` is absent),
that line and selection ranges are in range, that step 1 is anchored to a file or directory, and
that the step count sits inside the persona budget. Failures carry distinct codes such as
`tour/missing-file` and `tour/line-out-of-range`. Record a `generated_from_commit` (full SHA) in
the tour's description or handover note so staleness can be checked later (see
`doc-maintenance-after-change.md`).


Format source: `microsoft/codetour` repository and its `https://aka.ms/codetour-schema` schema.
Step types and `ref` behaviour carried over from the absorbed skill; not re-verified against the
live schema on 2026-09-24 (NOT_ASSESSED). Check the schema before relying on newer fields.
