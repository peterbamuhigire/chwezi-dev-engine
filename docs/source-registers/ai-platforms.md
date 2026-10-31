# AI, Platform, Security, and Framework Source Register

Last reconciled: 2026-10-31 (row-level dates below; rows not re-read are marked NOT_ASSESSED)
Standard/version: Chwezi Dev Engine source-register protocol (July 2026 baseline, October 2026 reconciliation)
Research support: Digital Research Skills Engine `source-evaluation` and `source-verification`

This register is the first stop before writing or modifying skills that depend on fast-moving AI, Apple, cloud, security, or framework facts. Do not hardcode model names, prices, platform limits, preview statuses, or compliance claims in skill logic. Link to the current source, record the access date, and set a review date.

## Source Rules

| Rule | Pass condition |
|---|---|
| Current fact | Source is official vendor, standards body, or primary project documentation |
| Volatile fact | Next review date is no later than 90 days after last verification |
| Benchmark claim | Names a standard, firm, publication, or artifact and links to its source |
| Deprecated feature | Includes replacement path or migration note |
| Research gap | Logged as a gap, not filled by guesswork |

## Register

Each row records what was read on the access date, not a blanket claim about the product. A row
whose page could not be read keeps its old date and is marked `NOT_ASSESSED`. Dated records with
the full evidence fields are in `skills-engine-currentness-2026-09.json`; the machine check is
`scripts/check_source_register.py`.

| Area | Canonical source | Use for | Last verified | Next review | Read on 2026-10-31 |
|---|---|---|---:|---:|---|
| OpenAI API and agents | https://developers.openai.com/api/docs/ | Responses API, tools, Agents SDK, prompt caching, deployment checklist, model availability | 2026-10-31 | 2026-11-30 | Landing page lists Agents SDK, Responses API, tools, prompt caching, GPT-6 upgrade guides; Assistants API retired. |
| OpenAI Codex | https://learn.chatgpt.com/docs | Codex CLI/app behaviour, local configuration, skills, agents, and current product guidance | 2026-10-31 (redirect only) | 2026-11-30 | The old developers.openai.com/codex address answers 308 to this host. The skills context-budget page on this host was read on 2026-10-29; the landing page content was not re-read. |
| OpenAI changelog | https://developers.openai.com/api/docs/changelog | Current model, API, and deprecation checks before naming OpenAI capabilities | 2026-10-31 (redirect only) | 2026-11-30 | The old platform.openai.com address answers 301 to this page. Entries last read 2026-10-29. |
| Anthropic Claude Platform | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | Tool use, server tools, MCP, prompt caching, context management | 2026-10-31 | 2026-11-30 | Page "Tool use with Claude" read: client and server tools, tool search, MCP connector, pricing table. |
| Anthropic Claude Code | https://code.claude.com/docs/en/ | Claude Code installation, CLI, settings, permissions, and agent behaviour | 2026-10-31 | 2026-11-30 | The old docs.anthropic.com address answers 301 to this host. The best-practices page on this host was read (see register record). |
| Google Gemini API | https://ai.google.dev/gemini-api/docs/function-calling | Function calling, tool schemas, Gemini integration behavior | 2026-10-31 | 2026-11-30 | Page read; examples use gemini-3.8-flash; a banner announces Gemini 4 Argon. Model names change quickly: do not hard-code. |
| Amazon Bedrock Agents | https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html | Bedrock Agents Classic (maintenance mode) and its AgentCore successor | 2026-10-31 | 2026-11-30 | Page now says Bedrock Agents is "Agents Classic", closed to new customers, with Bedrock AgentCore as the successor. Existing customers continue as normal. |
| OWASP Top 10 | https://top10.owasp.org/2025 | Web application risk taxonomy and security-audit baseline | 2026-10-31 | 2026-12-31 | OWASP Top 10:2025, categories A01 to A10 (A01 Broken Access Control, A03 Software Supply Chain Failures, A10 Mishandling of Exceptional Conditions). The old owasp.org/Top10/2025 address answers 308 to this host. No day-level date shown. |
| Kubernetes docs | https://kubernetes.io/docs/home/ | Kubernetes architecture, workloads, services, security, and operations facts | 2026-10-31 | 2026-11-30 | Version selector lists v1.37 first; the page does not label it latest, so treat as inferred. |
| Next.js docs | https://nextjs.org/docs | App Router, rendering, caching, deployment, and framework behavior | 2026-10-29 | 2026-11-03 | Verified through the 2026-10-29 records (release v16.4.3, support policy, upgrade guide). Re-checked on 2026-10-31: latest stable still v16.4.3. The 2026-11-03 security notice is not yet published. |
| React docs | https://react.dev/ | React component, hooks, compiler, and framework guidance | 2026-10-31 | 2026-11-30 | Versions page lists React 19.3 (v19.3.0). |
| Apple Developer Documentation | https://developer.apple.com/documentation/ | iOS, Swift, Xcode, App Intents, StoreKit, privacy, and release facts | 2026-07-08 | 2026-09-08 (overdue) | `NOT_ASSESSED`: the pages are script-rendered and returned no version text to the fetch methods available. Re-check with a browser. |
| W3C WCAG | https://www.w3.org/TR/WCAG22/ | Accessibility conformance references when frontend skills touch usability | 2026-10-31 | 2026-12-01 | W3C Recommendation, 12 December 2024. |

## Skills That Must Link Here

- `skills/ai/*` when naming models, agent APIs, evaluation APIs, tool APIs, or provider-specific capabilities.
- `skills/ios/*` and `skills/mobile-cross/*` when naming Apple platform versions, APIs, release rules, or StoreKit behavior.
- `skills/devops-cloud/*` when naming cloud managed services, Kubernetes behavior, CI/CD permissions, or deployment limits.
- `skills/security/*` when naming OWASP, cloud identity, web vulnerability, or privacy-compliance baselines.
- `skills/frontend-ux/nextjs-app-router`, `react-development`, `frontend-performance`, and `tailwind-css` when naming framework behavior or accessibility standards.

## Re-Verification Triggers

Re-run Digital Research Skills Engine `source-verification` and update this file when:

- a vendor announces a new major model, SDK, API, platform version, or deprecation;
- a standard changes version or enforcement status;
- a skill adds provider-specific implementation guidance;
- an exemplar names a benchmark whose current practice may have changed;
- a user asks for latest, current, today, newest, recommended, pricing, availability, or compliance status.
