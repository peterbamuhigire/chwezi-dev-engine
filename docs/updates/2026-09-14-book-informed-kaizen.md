# Book-informed portfolio Kaizen — 2026-09-14

## Outcome

The original supplied books were inspected from the authoritative local corpus
on 2026-09-14. The engineering catalogue now routes a concise synthesis into
world-class engineering, AI-assisted development, Git collaboration, advanced
testing, and system architecture. It preserves existing specialist ownership
instead of creating overlapping skills.

## Cross-engine adoption

- Design-system skills: source-of-truth token governance, token tiers and
  transforms, component state matrices, adoption scorecards, and behaviour-led
  handoff.
- Website skills: scenario-led page goals, whole-journey states, actionable
  diagnostics, friction logs, staged experiments, and post-launch learning.
- SRS skills: North Star scenarios, measurable requirements, NFR oracles,
  traceability, failure context, and change impact.
- Proposal skills: technical outcome-to-architecture logic, delivery evidence,
  acceptance/NFR proof, risks, operational ownership, and cost drivers.

## Evidence and exclusions

The ten source titles are recorded in the linked synthesis documents without
copying full text, OCR output, or source-file metadata. Vendor-specific pricing
and dated product details, generic JSON recipes, stale command examples, and
unsupported AI-training-data promises were excluded. The image-based System
Design at Google PDF was OCR-inspected for its contents and representative
architecture sections; its dated product claims were not adopted as doctrine.

## Model-policy currentness decision

The active Codex configuration and managed roles select `gpt-5.6-luna` with
`high` reasoning. Official evidence checked on 2026-09-14:

- [OpenAI Models](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4):
  lists `gpt-5.6-sol`, `gpt-5.6-terra` and `gpt-5.6-luna`; it describes Luna as
  the cost-sensitive tier and Sol as the flagship complex-work tier.
- [GPT-6 Astra safety overview](https://openai.com/index/safety-overview-gpt-6-astra/):
  confirms Astra as a newer, broadly deployed, higher-capability candidate.
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540):
  documents Codex model availability by plan and the Luna replacement path for
  older Codex defaults.

Local evidence: `codex-cli 0.154.0`, `C:\Users\Peter\.codex\config.toml`
(`gpt-5.6-luna`, `high`, review model Luna), and all eight engine policy
helpers pass. Effective account entitlement and runtime session readout are
`NOT_ASSESSED`. Decision: retain Luna/high as the active policy for cost,
latency and sufficient quality on this engine work; keep Astra opt-in only.
No automatic model switch was introduced. Any replacement requires a new
comparative quality/cost/latency review and explicit Peter authorisation.

## Re-measurement

Run each engine's native validator and routing smoke test after changes. Review
adoption and duplicate-guidance drift at the next portfolio Kaizen, with
unassessed production, stakeholder, and live-product evidence remaining
NOT_ASSESSED until supplied.
