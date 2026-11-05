# MCP HTTP+SSE deprecation dating, 6 November 2026

Two statements in the engine presented revision 2026-07-28 of the Model Context Protocol (MCP) specification as the point at which the HTTP+SSE transport was deprecated. A comparison of the engine's currentness notes with the specification, prompted by a 2026 reading of CODE Magazine articles, found that the specification dates the deprecation earlier and treats 2026-07-28 as a reclassification. The statements were imprecise, not false.

## Baseline (2026-11-05, branch point `a4d037a`)

Search of the tracked tree for `HTTP+SSE`, `SEP-2596` and `2026-07-28` (historical records under `docs/kaizen/` excluded). Three statements concern HTTP+SSE:

| File and line | Statement | Dates the deprecation to 2026-07-28? |
|---|---|---|
| `skills/ai/ai-web-apps/references/mcp-integration.md:7` | The revision "deprecates Roots, Sampling, Logging, and the HTTP+SSE transport" | Yes |
| `skills/architecture/api-design-first/references/apis-for-ai-agents-and-data.md:164` | The changelog records "deprecation of Roots, Sampling, Logging, and the HTTP+SSE transport" | Yes |
| `skills/architecture/api-design-first/references/apis-for-ai-agents-and-data.md:124` | "the old HTTP+SSE transport is deprecated in favour of Streamable HTTP" | No (undated; left unchanged) |

No other file in the tree restates the dating. The source registers hold no MCP record: the earlier check date (2026-09-24) lived only in the prose of the two files.

## Primary sources read

All read with `curl` on 2026-11-05 at 21:25 UTC (00:25 on 6 November, East Africa Time). Each page shows "Version 2026-07-28 (latest)". The revision identifier is the only date the pages show; no page publication date appears in the text. Freshness class: time-sensitive (protocol lifecycle). Tier: the specification owner's own site.

| Page | What it supports | Quoted wording |
|---|---|---|
| `https://modelcontextprotocol.io/specification/2026-07-28/changelog` | HTTP+SSE deprecated since 2025-03-26; reclassified in this revision under SEP-2596 | "Reclassify the HTTP+SSE transport (deprecated since protocol version 2025-03-26) as Deprecated under the feature lifecycle policy (SEP-2596)." |
| the same changelog | Roots, Sampling and Logging are deprecated in this revision | "Deprecate the Roots, Sampling, and Logging features (SEP-2577)." |
| the same changelog | Sessions and the handshake are removed | "Remove protocol-level sessions and the `Mcp-Session-Id` header from the Streamable HTTP transport." and "Make MCP stateless: remove the `initialize`/`notifications/initialized` handshake." |
| the same changelog | The previous revision is 2025-11-25 | "since the previous revision, 2025-11-25" |
| `https://modelcontextprotocol.io/specification/2026-07-28/deprecated` | Registry row: HTTP+SSE, SEP-2596, deprecated in 2025-03-26, migrate to Streamable HTTP | "already described as deprecated before the lifecycle policy existed" |
| `https://modelcontextprotocol.io/specification/2026-07-28/server/tools` | The default schema dialect | "Defaults to 2020-12 if no `$schema` field is present" |
| `https://modelcontextprotocol.io/specification/2026-07-28/basic/transports` | The standard transports are stdio and Streamable HTTP; the page does not date HTTP+SSE | (no HTTP+SSE text) |

`https://modelcontextprotocol.io/specification/latest/changelog` redirected to the 2026-07-28 changelog at the time of reading.

## Other clauses of the line 164 bullet, checked against the changelog

| Clause | Result |
|---|---|
| `latest` resolves to 2026-07-28, previous 2025-11-25 | Matches |
| Removal of protocol sessions and the initialise handshake | Matches (SEP-2567, SEP-2575) |
| `server/discover` | Matches: the changelog says servers MUST implement it. It is an addition, not a removal |
| `subscriptions/listen` | Matches: replaces the HTTP GET endpoint and `resources/subscribe`. An addition |
| Multi Round-Trip Request pattern; required `resultType` | Matches (SEP-2322) |
| 2020-12 schema loosening for tool schemas | Matches: `inputSchema` and `outputSchema` may use any JSON Schema 2020-12 keywords (SEP-2106) |
| Deprecation of Roots, Sampling and Logging | Matches (SEP-2577) |
| Deprecation of HTTP+SSE | Did not match; corrected below |

Wording finding, not changed: the bullet reads "records removal of protocol sessions and the initialise handshake, `server/discover`, `subscriptions/listen`, ..." and a reader can take the whole list as removals. Only the first two items are removals. The edit was limited to statements that date the deprecation, so this phrasing is left for the owner to decide.

For `mcp-integration.md` line 7, the clause "defaults tool schemas to JSON Schema 2020-12" is supported by the tools page quoted above. Whether the default is new in this revision was not checked.

## Edits

| Commit | File | Change |
|---|---|---|
| `284b0f2` | `skills/ai/ai-web-apps/references/mcp-integration.md` line 7 | "deprecates Roots, Sampling, Logging, and the HTTP+SSE transport" became "deprecates Roots, Sampling, and Logging, reclassifies the HTTP+SSE transport (deprecated since protocol version 2025-03-26) as Deprecated under the feature lifecycle policy (SEP-2596)". Check date 2026-09-24 became 2026-11-05. |
| `f44848c` | `skills/architecture/api-design-first/references/apis-for-ai-agents-and-data.md` line 164 | The same correction, plus "The changelog clauses in this bullet were re-read on 2026-11-05." The block heading "Accessed 2026-09-24" is unchanged, because the other bullets under it (package versions, survey figures) were not re-read. |

Line 124 is unchanged (undated). The SDK snippets stay `NOT_ASSESSED`. The `ToolAnnotations` check in `schema.ts` keeps its 2026-09-24 date.

## Validators

Run from the repository root on Linux (Python 3.14.10, pytest 9.2.0, Node 22), before the first edit and after the second. Results are identical.

| Step | Before | After |
|---|---|---|
| `scripts/skill_catalog_guardrails.py` | exit 0; 168 active skills; 14 warnings | exit 0; same |
| `unittest tests/test_skill_catalog_guardrails.py` | exit 0 | exit 0 |
| `pytest tests -q -p no:cacheprovider` | exit 0; 273 passed, 3 skipped | exit 0; same |
| `routing_smoke_test.py --min-rank1 89 --lint-fixtures` | exit 0; 242 fixtures; precision@1 222/242; precision@3 242/242 | same |
| `routing_smoke_test.py --coverage` and `--collisions` | exit 0 | exit 0 |
| `validate_engine_control_plane.py` | exit 0 | exit 0 |
| `check_source_register.py` | **exit 1**; 14 findings | **exit 1**; the same 14 records |
| hook tests (2 files) | exit 0 | exit 0 |
| `contract_gate.py --all` | exit 0; 162 scanned, 0 errors | same |
| `git diff --check` | exit 0 | exit 0 |

The 14 source-register findings are five Next.js records with `review_after` 2026-11-03 and nine Android, Kotlin, PHP, PostgreSQL and MySQL records with `review_after` 2026-11-05. None was touched: re-reading them is a separate step, and a date is never extended unread.

## Search after the edits

Only one statement mentions HTTP+SSE without a date (line 124). Both statements that carry a date now give 2025-03-26 and SEP-2596. A search for lines that mention HTTP+SSE and 2026-07-28 but not 2025-03-26 returns 0 lines.

## Not assessed

- Whether SEP-2596 has reached Final status. The registry says earliest removal is "Three months after SEP-2596 reaches Final"; the SEP itself was not read.
- Whether the SDK snippets match the current SDKs.
- The `ToolAnnotations` fields in the published `schema.ts` (not re-read).
- Whether the 2020-12 default is new in this revision.
- No MCP record exists in `docs/source-registers/`, so none was updated. Adding one would add a `review_after` date and change the register counts quoted in the README. That is left for the owner.
