# ER1 front-door and claim inventory

Observed 2026-11-23 at local integrated revision `7965083c0dedbfd5c6e52847d1c2db9ddfec3dba`. This records the README state before the planned rewrite; it does not claim the README has been released or that the examples are production capabilities.

## Proposed AI journey claims

The structured claim register in [claim-inventory.json](claim-inventory.json) assigns each proposed claim an owning skill or script, a resolvable entry point, accepted implementation revision, observed result, environment, limitation and receipt. The four core AI implementation packets E01-E04 are accepted and present in this checkout. E05 covers the assisted-software journey; E06 covers public skill discovery. All six accepted commits are ancestors of the observed local integrated revision.

| Reader task | Public route | Evidence class | Limit to preserve in README |
|---|---|---|---|
| Choose a text-label baseline | [Python ML predictive](../../../../../skills/languages/python-ml-predictive/SKILL.md) | Fixture-tested | Tiny synthetic held-out set; no production quality or cost claim. |
| Diagnose retrieval and answer support | [RAG patterns](../../../../../skills/ai/ai-rag-patterns/SKILL.md) | Fixture-tested | Lexical example and literal support oracle; no semantic or production benchmark. |
| Review adaptation or generated media | [AI evaluation](../../../../../skills/ai/ai-evaluation/SKILL.md) | Fixture-tested metadata decision | Inference and training not run; real quality and rights unassessed. |
| Diagnose a failed release | [AI observability and debugging](../../../../../skills/ai/ai-observability-and-debugging/SKILL.md) | Fixture-tested simulation | No process-crash durability, production rollout, or real model quality. |
| Review an AI-authored code change | [AI-assisted development](../../../../../skills/sdlc-meta/ai-assisted-development/SKILL.md) | Fixture-tested local caller | Synthetic SQLite case; no production database or multi-host result. |
| Find the correct skill | [Routing fixtures](../E06/routing.json) | Fixture-tested lexical discovery | Not live model routing; four cross-engine negatives remain NOT_ASSESSED. |

## Preserve the existing README front door

The rewrite must retain resolvable routes for these existing sections and the inbound anchors they create: `#at-a-glance`, `#start-here`, `#capabilities`, `#find-the-right-skill`, `#chwezi-product-excellence-standard`, `#chwezi-reporting-and-dashboards-standard`, `#how-it-works`, `#what-is-inside`, `#catalogue-size`, `#what-the-skills-produce`, `#standards-applied`, `#beyond-the-skills`, `#installation`, `#claude-code-plugin-recommended`, `#codex`, `#standalone-installer`, `#manual-route`, `#verify`, `#checks-beyond-ci`, `#quality-and-improvement`, `#changes-after-the-october-kaizen-1-to-8-november-2026`, `#latest-published-score`, `#open-findings-that-matter-to-a-reader`, `#what-the-october-2026-kaizen-improved`, `#defects-fixed-in-guidance`, `#tooling-that-failed-on-this-host`, `#checks-that-only-tighten`, `#routing-and-examples`, `#overall-measures`, `#date-triggered-gates`, `#references`, and `#contributing-and-licence`.

Keep the Claude marketplace route (`/plugin marketplace add peterbamuhigire/chwezi-dev-engine`, `/plugin install engineering@chwezi-engineering`), Codex helper route (`python3 <engine-root>/.codex/ensure_model_policy.py --runtime codex --check`), explicit offline prompt-input invocation, standalone install/uninstall/doctor/list commands, Windows `install.ps1` route, manual wiring guide, catalogue command (`python3 -X utf8 scripts/skill_catalog_guardrails.py`), CI check list, and `NOT ASSESSED` semantics. The current README's exact headings, inline links, and commands are the source for the baseline; ER3 must recheck changed anchors and commands against the pre-rewrite revision.

The documented quick verification sequence is `pip install -r requirements-ci.txt`, catalogue guardrails, guardrail unit test, pytest suite, routing lint, routing coverage, collision gate, control-plane validation, source-register check, Node hook checks, skill contract gate, auto-agents unit tests, and `git diff --check`. These historical commands and dates must remain explicitly scoped to their recorded environments; ER3 owns replay or qualification after the rewrite.

## Preserve broader engine scope

The README describes the catalogue beyond AI. Keep an intentional route to the existing owners for architecture ([`skills/architecture/`](../../../../../skills/architecture/)), databases ([`skills/backend-databases/`](../../../../../skills/backend-databases/)), security ([`skills/security/`](../../../../../skills/security/)), programming languages ([`skills/languages/`](../../../../../skills/languages/)), web and mobile ([`skills/frontend-ux/`](../../../../../skills/frontend-ux/), [`skills/android/`](../../../../../skills/android/), [`skills/ios/`](../../../../../skills/ios/), [`skills/mobile-cross/`](../../../../../skills/mobile-cross/)), multi-tenant SaaS ([`skills/saas/`](../../../../../skills/saas/)), DevOps ([`skills/devops-cloud/`](../../../../../skills/devops-cloud/)), game development ([`skills/game-development/`](../../../../../skills/game-development/)), and GIS ([`skills/gis/`](../../../../../skills/gis/)). `LICENSE`, `CHANGELOG.md`, and `CONTRIBUTING.md` are present and must remain discoverable from the front door. Preserve the October kaizen history and open findings with their dated evidence links; do not imply that a historical check is a current pass.

## Model currentness and release limits

On 2026-11-23, the official OpenAI model release notes were rechecked. Their latest model entry located is the 2026-11-17 GPT-6.2 Astra/Sol announcement; the Work/Codex release notes describe preview availability, subject to plan, seat, workspace settings, and client version. The account/runtime catalogue is unavailable to this task (`NOT_ASSESSED`). The Codex policy helper reported `DRIFT: root model policy drift`; no host configuration was changed and no policy change is proposed. See the dated records and uncertainty fields in [claim-inventory.json](claim-inventory.json).

## ER1 result

The inventory passes its targeted local consistency check. It does not establish trained-model, hosted, production, account-access, or human-acceptance evidence. The next task is ER2; ER3 remains dependent on ER2 and the supervisor's final verification.
