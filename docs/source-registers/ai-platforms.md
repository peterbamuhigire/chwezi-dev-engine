# AI, Platform, Security, and Framework Source Register

Last verified: 2026-07-08
Standard/version: Skills Web Dev July 2026 source-register protocol
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

| Area | Canonical source | Use for | Last verified | Next review |
|---|---|---|---:|---:|
| OpenAI API and agents | https://developers.openai.com/api/docs/ | Responses API, tools, Agents SDK, prompt caching, deployment checklist, model availability | 2026-07-08 | 2026-10-08 |
| OpenAI changelog | https://platform.openai.com/docs/changelog | Current model, API, and deprecation checks before naming OpenAI capabilities | 2026-07-08 | 2026-08-08 |
| Anthropic Claude Platform | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | Tool use, server tools, MCP, prompt caching, context management | 2026-07-08 | 2026-10-08 |
| Google Gemini API | https://ai.google.dev/gemini-api/docs/function-calling | Function calling, tool schemas, Gemini integration behavior | 2026-07-08 | 2026-10-08 |
| Amazon Bedrock Agents | https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html | Bedrock agent orchestration, knowledge bases, guardrails, AWS deployment facts | 2026-07-08 | 2026-10-08 |
| OWASP Top 10 | https://owasp.org/www-project-top-ten/ | Web application risk taxonomy and security-audit baseline | 2026-07-08 | 2026-10-08 |
| Kubernetes docs | https://kubernetes.io/docs/home/ | Kubernetes architecture, workloads, services, security, and operations facts | 2026-07-08 | 2026-10-08 |
| Next.js docs | https://nextjs.org/docs | App Router, rendering, caching, deployment, and framework behavior | 2026-07-08 | 2026-10-08 |
| React docs | https://react.dev/ | React component, hooks, compiler, and framework guidance | 2026-07-08 | 2026-10-08 |
| Apple Developer Documentation | https://developer.apple.com/documentation/ | iOS, Swift, Xcode, App Intents, StoreKit, privacy, and release facts | 2026-07-08 | 2026-09-08 |
| W3C WCAG | https://www.w3.org/TR/WCAG22/ | Accessibility conformance references when frontend skills touch usability | 2026-07-08 | 2026-10-08 |

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
