---
name: ios-ai-ml
description: iOS AI/ML standards for WWDC26 Apple intelligence work, including Foundation Models, Language Model providers, Dynamic Profiles, Core AI, Evaluations, Core ML, Vision, NaturalLanguage, Speech, SoundAnalysis, and privacy-first on-device inference.
metadata:
  portable: true
  compatible_with:
  - Codex
  - codex
---

# iOS AI/ML
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Building or reviewing iOS, iPadOS, or macOS AI/ML features using Foundation Models, Core AI, Core ML, Vision, NaturalLanguage, Speech, SoundAnalysis, Create ML, Evaluations, Private Cloud Compute, or a third-party Language Model provider.
- The work includes on-device inference, custom models, multimodal prompts, agentic model tool use, AI evaluation, model-provider selection, privacy-sensitive AI, or Apple Intelligence availability gates.

## Do Not Use When

- The task is plain iOS implementation with no AI/ML path; use `ios-development`.
- The task is AI product architecture outside Apple platforms; use `ai-app-architecture`, `ai-llm-integration`, or `ai-evaluation`.
- The task is only AI security, prompt injection, or action authorization; use this skill with `ios-security-and-rbac`.

## Required Inputs

- Feature goal, model/provider choices, target Apple platforms, device/OS floor, privacy constraints, offline expectations, data inputs, tools/actions the model may call, and evaluation criteria.
- Confirm whether the deliverable is design, implementation, migration, review, evaluation plan, or release evidence.

## Workflow

1. Load `ios-development` for Apple-platform implementation rules and availability policy.
2. Load `references/apple-intelligence-stack-wwdc26.md` for Foundation Models, Core AI, provider routing, Evaluations, and availability gates.
3. Load `references/skill-deep-dive.md` only when you need legacy Core ML, Vision, NaturalLanguage, Create ML, or model-optimization recipes.
4. Choose the lowest-risk model path that solves the task: deterministic API, Core ML/Core AI owned model, on-device Foundation Models, Private Cloud Compute, or third-party provider.
5. Define privacy, fallback, telemetry, evaluation, and security gates before writing production code.

## Quality Standards

- Every AI feature has a provider boundary, availability gate, privacy path, fallback state, and evaluation set.
- On-device claims must be true: no network dependency unless the code path is explicitly cloud or third-party.
- Agentic or tool-calling model features require authorization, audit logging, and security review.
- Model performance work must include device, latency, memory, battery, and thermal evidence.

## Anti-Patterns

- Treating Core ML, Core AI, and Foundation Models as interchangeable.
- Sending sensitive user data to a cloud model because the on-device path was harder.
- Shipping prompt-only tests for model behavior that changes by tool, locale, region, model, or data state.
- Logging prompts, model context, OCR text, tool payloads, or generated sensitive content without a privacy review.

## Outputs

- AI feature architecture, provider decision matrix, model integration plan, evaluation suite, privacy/fallback checklist, performance budget, or review findings.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | AI evaluation plan | Markdown doc covering prompts, providers, tools, unavailable states, and regression cases | `docs/ios/ai-evaluations-checkout.md` |
| Performance | On-device inference budget | Markdown doc covering per-device latency, memory, battery, and thermal budget | `docs/ios/ai-perf-budget.md` |
| Privacy | AI data-flow record | Markdown doc identifying on-device, PCC, third-party, logs, and retention | `docs/ios/ai-data-flow.md` |

## References

- `references/apple-intelligence-stack-wwdc26.md` for Foundation Models, Core AI, Evaluations, provider routing, availability gates, and security handoffs.
- `references/skill-deep-dive.md` for Core ML, Vision, NaturalLanguage, Create ML, model updates, optimization, privacy-preserving patterns, and older Apple ML recipes.
<!-- dual-compat-end -->

## Quick Apple AI Stack Map

| Layer | Use For |
| --- | --- |
| Foundation Models | LLM-backed app features using Apple Foundation Models, PCC, Claude, Gemini, or another Language Model provider. |
| Core AI | Bring-your-own model runtime on Apple Silicon, on-device. |
| Core ML | Packaged or downloaded `.mlmodel` inference, typed wrappers, batch prediction, classic ML. |
| Vision | OCR, barcode, image analysis, camera understanding, and model-callable visual tools. |
| NaturalLanguage | Deterministic language tagging/classification when an LLM is not needed. |
| Speech/SoundAnalysis/Music Understanding | Audio transcription, classification, and local audio understanding. |
