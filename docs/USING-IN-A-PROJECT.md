# Using This Catalogue In A Real Project

This guide is for an integrator pointing an agent (Claude, Codex, or similar) at
this skills catalogue to do work in a *different* repository - a client app, an
internal product, an ERP. It answers one question: how do you get the value of
the catalogue into the work **without copying irrelevant doctrine into the
deliverable**?

## The one rule that matters

**Skills are guidance the agent reads, not code you vendor in.** A skill tells
the agent how to do a thing well; the *output* belongs to your project, the
*doctrine* stays here and is cited, not pasted. If finance doctrine, a house
style, or a reference file ends up copied verbatim into the target repo, that is
the failure mode this guide exists to prevent.

## Wiring options

| Option | When to use | Trade-off |
|---|---|---|
| Git submodule | The target repo is yours and you want versioned, updatable skills | Cleanest; updates pull through; needs submodule literacy |
| Sibling clone + path | One agent, many projects, on your machine | No coupling to the target repo; you manage the path |
| Read-only mount / MCP filesystem | CI or a sandbox agent | Enforces "read, do not vendor" by construction |
| Copy a single skill in | Almost never | Forks the skill; it goes stale and drifts from the gate. Avoid. |

Default to a submodule for a repo you own, or a sibling clone for ad-hoc work.
Expose only the active roots: `skills/`, `doctrine/skills/`, and
`00-meta-initialization/`. Do not expose `docs/`, `blog-posts/`, or
`book-extractions/` to the working agent - that is maintainer material and only
adds routing noise.

## Progressive disclosure - the loading discipline

This is how the catalogue stays cheap to route and keeps irrelevant doctrine out
of context:

1. The agent reads the relevant `SKILL.md` (one file, trigger-shaped
   description).
2. It loads **only** the `references/`, `templates/`, or `scripts/` files that
   that SKILL.md names, and only when the task needs them.
3. It never bulk-loads a domain. Loading all of `ai/` to answer one RAG question
   is the anti-pattern.

If you are routing manually, start from `docs/skill-routing-index.md` (old slug
-> retained skill) and `docs/skill-aliases.yml` (machine-readable).

## Keeping doctrine canonical, not copied

| Do | Do not |
|---|---|
| Cite the skill that informed a decision ("per `database-design-engineering`") | Paste the skill's prose into the target repo's docs |
| Produce the *artifact* (ADR, migration plan, threat model) into the target repo | Copy the *template* file in as if it were project content |
| Keep finance rules in `doctrine/skills/` and reference them | Duplicate IFRS doctrine into the app's codebase |
| Let the agent read the skill each run | Fork a skill into the project and let it drift |

Finance, accounting, and statutory doctrine is canonical under
`doctrine/skills/`. Deliverables reference it; they do not embed it.

## What good application looks like

The agent should, for meaningful work, route to `world-class-engineering` as the
baseline, pull in the specific domain skills the task needs, and close with the
**Delivery Definition of Done** pack
(`skill-composition-standards/references/delivery-definition-of-done.md`) so the
target team gets tests, a release plan, a rollback plan, a runbook, and
maintenance notes - not just code.

## Quick start

```text
1. Add the catalogue as a submodule (or clone it beside the target repo).
2. Tell the agent: "Use the skills catalogue at <path>. Route via its
   descriptions and skill-routing-index.md. Read a SKILL.md, then load only the
   references it names. Do not copy doctrine or templates into this repo - cite
   them and produce the artifacts instead."
3. For meaningful work, require the Delivery Definition of Done pack as the
   closing deliverable.
```

## Related

- `README.md` - catalogue overview and active roots.
- `docs/skill-routing-index.md` - routing policy and alias map.
- `docs/CLIENT-VALUE-BRIEF.md` - the plain-language value statement for clients.
