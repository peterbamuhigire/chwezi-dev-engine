# Kaizen Model-Currentness Check — 11 September 2026

## Result

**Decision:** retain the pinned policy and make Astra the new-session default. Keep `gpt-5.6-luna`
for execution roles. Do not silently replace either pin on a future release; re-evaluate at the
next Kaizen start.

## Evidence

| Item | Evidence | Assessment |
|---|---|---|
| Official catalogue | [OpenAI Models](https://developers.openai.com/api/docs/models) lists `gpt-6-astra` as the flagship for complex reasoning/coding and `gpt-5.6-luna` for cost-sensitive, high-volume work. | Both remain task-fit for their assigned roles. |
| Astra capability | [GPT-6 Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra) lists computer use, code interpreter, hosted shell, apply patch, skills, MCP, web search, and a 1.05M context window. | Strong fit for the root orchestrator and final review. |
| Luna capability and cost | [GPT-5.6 Luna model page](https://developers.openai.com/api/docs/models/gpt-5.6-luna) lists a 1.05M context window and $0.20/$1.20 per million input/output tokens. | Strong fit for bounded execution; materially cheaper than Astra. |
| Local runtime | `codex-cli 0.154.0`; `C:\Users\Peter\.codex\models_cache.json` fetched 11 September 2026 and includes `gpt-6-astra` with visibility `list`; local policy pins Astra root/reviewer and Luna execution. | Runtime catalogue evidence is present. |
| Active base configuration | Before this change, `C:\Users\Peter\.codex\config.toml` selected `gpt-5.6-sol`; `astra-on.config.toml` selected Astra and `astra-off.config.toml` selected Sol. | This was the availability/default mismatch, not proof of account entitlement. |

## Change and uncertainty

The base config now selects `gpt-6-astra` for newly started sessions. `-p astra-on` explicitly turns
Astra on and `-p astra-off` turns it off to Sol. A running session does not change because a file was
edited. The local cache proves catalogue visibility, not that every account, project, plan, or
rollout can successfully start Astra; a new-session smoke test is still required to establish that.

## Retain/change decision

- **Retain:** `gpt-6-astra` for root orchestration and final review: strongest fit for multi-engine synthesis and complex coding/document work.
- **Retain:** `gpt-5.6-luna` for bounded workers and testers: lower cost and adequate task fit.
- **Change:** default new-session model from `gpt-5.6-sol` to `gpt-6-astra`, because the local catalogue exposes Astra and the user requested it as an option.
- **Do not change:** role pins or model policy from a newer name alone; current release, access, quality, latency, and cost evidence must be rechecked.
