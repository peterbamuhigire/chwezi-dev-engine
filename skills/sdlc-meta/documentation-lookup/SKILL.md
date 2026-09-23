---
name: documentation-lookup
description: Use when answering setup, configuration, or API-reference questions about a specific library or framework, or writing code that depends on current behavior. Fetch live docs via an MCP documentation server instead of relying on stale training data.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
  origin: "Adapted from affaan-m/ECC skills/documentation-lookup/SKILL.md"
---

# Documentation Lookup

Training data is a snapshot frozen at a point in time. A library's API surface,
config format, or recommended pattern can change across major versions released
after that snapshot — and the model has no way to know, from inside a single
answer, whether what it "remembers" is still current. When a live documentation
MCP server (Context7 or an equivalent your environment has configured) is
available, use it instead of guessing from memory for anything version-sensitive.

<!-- dual-compat-start -->

## Use When
Use when an answer or implementation depends on a library's current documented behaviour.

## Do Not Use When
Do not use for durable language or architecture guidance that does not require live documentation.

## Required Inputs
- Library or framework name, version scope, exact question, and documentation provider.

## Workflow
1. Resolve the live documentation source, read the relevant page, and record its scope before answering.

## Quality Standards
Separate verified documentation from inference and stale or unavailable evidence.

## Anti-Patterns
- Relying on memory for current APIs. Fix: retrieve and cite the live documentation.

## Outputs
- A source-backed answer or implementation note with unresolved gaps retained.

## References
- The documentation lookup method and engine relationships are documented below.

## When to Use

- Setup or configuration questions ("how do I configure Laravel's rate limiter?")
- Code that depends on a specific library or framework's current API
  ("write a Symfony validator for...", "write a Prisma query with a relation")
- API or reference questions ("what are Stripe's current webhook event types?")
- The user names a specific framework, library, or package version
- Anything where being wrong about current behavior would produce code that
  fails to compile, run, or pass review against the real, installed version

Do not use it for language-level fundamentals that do not drift (control flow,
general algorithm design) — only for library- and framework-specific surface
that a new release can change.

## How It Works

1. **Resolve the library ID.** Call the resolve tool (e.g. `resolve-library-id`)
   with the library name and the user's question as the query. Do not skip this
   — querying docs without a resolved, valid library ID risks pulling the wrong
   project's documentation (name collisions are common: e.g. multiple packages
   named `core` or `client`).
2. **Select the best match.** Prefer an exact name match, higher documentation
   quality/benchmark score where the tool reports one, an officially maintained
   source over a community fork, and a version-specific ID when the user named
   a version.
3. **Fetch the docs.** Call the query tool (e.g. `query-docs`) with the resolved
   library ID and a specific query — the user's actual question, not a generic
   one. Cap lookups at roughly 3 calls per question; if the answer is still
   unclear after that, state the uncertainty explicitly rather than guessing
   past it.
4. **Answer using the fetched content**, citing the library and version when it
   matters for correctness ("In Laravel 11...").

## Guardrails

- **No secrets in the query.** Redact API keys, tokens, connection strings, and
  passwords from any question text sent to a documentation MCP server before
  the call — the query text leaves this session's trust boundary.
- **Prefer official sources** when a resolve step returns multiple candidates.
- **If no documentation MCP is configured** in the current environment, say so
  and fall back to training data explicitly, flagging that the answer may be
  stale for a fast-moving library rather than presenting it with the same
  confidence as a live-verified answer.

<!-- dual-compat-end -->

## Relationship to This Engine

This complements, not replaces, this engine's language and framework skills
(`skills/languages/*`, `skills/frontend-ux/*`) — those carry durable idiom and
architecture guidance; this skill exists specifically for the part of an answer
that depends on a library's *current, exact* API surface, which no static skill
file can keep up to date across every dependency this engine's users touch.
