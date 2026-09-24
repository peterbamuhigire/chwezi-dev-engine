# Live Documentation Lookup

Load when an answer or implementation depends on a library or framework's current documented
behaviour (setup, configuration, API reference, version-specific surface) and a live
documentation source is available. Training data is a frozen snapshot; a hallucinated or stale
API is one of the main AI-coding risks this skill's risk-control table names.

Absorbed from the retired `sdlc-meta/documentation-lookup` skill (origin: adapted from
affaan-m/ECC `skills/documentation-lookup/SKILL.md`). Tool names such as `resolve-library-id`
and `query-docs` are examples from one documentation MCP server (Context7); confirm the names
exposed in the current environment before calling them.

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

## Relationship to This Engine

This complements, not replaces, this engine's language and framework skills
(`skills/languages/*`, `skills/frontend-ux/*`) — those carry durable idiom and
architecture guidance; this skill exists specifically for the part of an answer
that depends on a library's *current, exact* API surface, which no static skill
file can keep up to date across every dependency this engine's users touch.

When no documentation MCP is configured, fetch the vendor's official documentation directly
(for example with a web fetch tool) and, for evidence-backed claims, apply the
`digital-research-engine` source-evaluation and source-verification skills.
