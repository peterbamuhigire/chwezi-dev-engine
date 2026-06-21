# Apple Intelligence Stack WWDC26

Self-contained AI/ML guidance for iOS, iPadOS, macOS, and Apple-platform apps
after WWDC26. Source basis: Apple Developer WWDC26 iOS/macOS guides, Xcode page,
and the local WWDC26 developer impact report.

## Decision Matrix

| Need | Preferred Apple path | Notes |
| --- | --- | --- |
| LLM feature using Apple or third-party models | Foundation Models framework | Native Swift API; supports Apple Foundation Models, cloud providers, multimodal prompts, tools, and Dynamic Profiles. |
| Own model running on-device | Core AI | Apple Silicon-optimized runtime for loading, specializing, and running models locally. |
| Existing Core ML model inference | Core ML | Keep for typed `.mlmodel` workflows, batch prediction, and classic ML models. |
| Image/text extraction tools for model use | Vision + Foundation Models tools | OCR, barcode, and visual analysis can run on-device. |
| Natural-language classification/tokenization | NaturalLanguage or Core ML | Use deterministic APIs before adding an LLM. |
| Audio/music understanding | Music Understanding, Speech, SoundAnalysis | Keep user audio local where possible. |
| Training or conversion | Create ML, Core ML Tools, MLX | Mac-side authoring/conversion lane; verify release status per project. |

## Provider Boundary

Every AI feature must define a provider boundary:

- `LocalAppleModelProvider` for on-device Foundation Models.
- `PrivateCloudProvider` for Apple Foundation Models on Private Cloud Compute.
- `ThirdPartyModelProvider` for Claude, Gemini, or another Language Model
  protocol implementation.
- `OwnedModelProvider` for Core AI/Core ML models packaged or downloaded by the
  app.

The UI and domain layers depend on the app's protocol, not on a provider SDK.
Log provider choice, model/profile version, prompt template version, and
evaluation version for reproducibility without logging user secrets.

## Dynamic Profiles

Use Dynamic Profiles to change model, tools, and instructions inside a
continuous session only when the user task changes. Do not use them as hidden
global personalization. Record which profile was active for each high-risk
response.

## Evaluations Gate

Use Evaluations for behavior that can change by prompt, model, tool, device,
locale, data state, or region. Minimum evaluation set:

- allowed and disallowed requests;
- tool-call authorization;
- privacy-sensitive inputs;
- offline/unavailable provider fallback;
- locale and language variants;
- hallucination-prone domain questions;
- regression cases from production defects.

Unit tests still cover deterministic code. Evaluations cover model behavior.

## Core AI Gate

Use Core AI when you own or adapt the model and need local privacy, offline
operation, or token-cost avoidance. Before shipping:

- set model memory and latency budgets;
- test first-run compilation/load time;
- verify hardware specialization on supported devices;
- confirm fallback for unsupported hardware;
- keep large downloaded models signed, versioned, and revocable;
- measure battery and thermal impact on real devices.

## Availability And Cost Gates

Apple Intelligence and Siri AI availability depends on device, language,
region, law, and service state. Foundation Models server access also depends on
program eligibility and operational terms. Every feature needs:

- device and OS capability check;
- region/language check;
- provider availability check;
- quota/cost policy;
- user-visible fallback that preserves the core task.

Do not promise no cloud API cost unless the app qualifies under Apple's stated
Small Business Program and download thresholds and the current terms have been
verified.

## Security Handoff

Load `ios-security-and-rbac/references/agentic-ai-and-app-intents-security.md`
when an AI feature can call tools, access user content, trigger App Intents,
write data, spend money, send messages, or expose tenant data.
