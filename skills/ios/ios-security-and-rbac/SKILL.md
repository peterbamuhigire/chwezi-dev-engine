---
name: ios-security-and-rbac
description: Use when designing or reviewing iOS authentication, Keychain, App Attest, privacy manifests, permissions, RBAC, tenant isolation, or AI security; use ios-development for general implementation.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# iOS Security And RBAC
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Securing an iOS app, reviewing mobile threat models, designing permission gates, protecting secrets, or implementing tenant-aware RBAC.
- The task mentions Keychain, Secure Enclave, App Attest, Trust Insights, Data Protection, ATS, certificate pinning, jailbreak/tamper checks, privacy manifests, roles, permissions, App Intents, AI tool use, prompt injection, or offline authorization caches.
- A retired iOS security or RBAC skill is referenced by name.

## Do Not Use When

- The task is general iOS implementation with no security, privacy, or authorization impact.
- The task is cross-platform Android-first RBAC; use `mobile-platform-operations` for the absorbed Android/mobile RBAC reference.

## Required Inputs

- Auth model, tenant model, roles/permissions, data sensitivity, offline requirements, API authorization contract, storage choices, and compliance/privacy constraints.

## Workflow

1. Load `ios-development` for baseline implementation standards.
2. Load `vibe-security-skill` for broader product threat modeling when the risk crosses backend, API, or web surfaces.
3. Load `references/agentic-ai-and-app-intents-security.md` when AI, Siri, App Intents, Spotlight, or model tool use touches private data or actions.
4. Load `references/ios-app-security.md` for device/app hardening and `references/ios-rbac.md` for permission gates.
5. Verify server-side authorization, local cache expiry, secret storage, privacy disclosure, and test evidence.

## Quality Standards

- Client RBAC must never replace server-side authorization.
- Secrets belong in Keychain or stronger platform storage, not UserDefaults or logs.
- Offline permission caches need expiry, invalidation, auditability, and conservative fallback behaviour.
- AI tools, App Intents, and Siri-mediated actions must re-check authorization and confirm high-risk actions.

## Anti-Patterns

- Trusting client-side role flags as the source of truth.
- Logging tokens, PII, Keychain errors, or authorization payloads.
- Adding jailbreak checks without a clear policy for detection, false positives, and support.

## Outputs

- iOS threat model, security checklist, RBAC matrix, permission-gate implementation notes, review findings, or verification evidence.

## Inputs

| Artefact | Produced by | Required? | Why |
|---|---|---|---|
| Threat model and abuse cases | Security owner | required | Sets trust boundaries |
| Role and tenant policy | Backend/product owner | required | Defines server-enforced authorisation |
| Data classification | Privacy owner | required | Controls storage, logging, and disclosure |

## Decision Rules

| Finding | Required action |
|---|---|
| Client role differs from server response | Server decision wins; deny and refresh policy |
| Secret must survive reinstall | Reassess requirement; use narrowly scoped Keychain only if justified |
| High-value request lacks attestation | Step up verification or reject according to risk policy |
| Privacy purpose or retention is undefined | Stop collection |

## Domain Anti-Patterns

- Enforcing RBAC only in the UI. Fix: authorise every backend operation server-side.
- Storing bearer tokens in UserDefaults. Fix: use constrained Keychain access controls.
- Logging credentials, prompts, or tenant identifiers. Fix: redact at the logging boundary.
- Treating App Attest as user authentication. Fix: combine device integrity with authenticated identity.
- Allowing cross-tenant cache keys. Fix: partition and clear storage by tenant and account.

- `references/ios-app-security.md` for Keychain, Secure Enclave, ATS, pinning, signing, privacy manifests, and tamper resistance.
- `references/ios-rbac.md` for permission models, SwiftUI gates, offline caches, and tenant-safe authorization UX.
- `references/agentic-ai-and-app-intents-security.md` for prompt/tool injection, App Intents authorization, semantic index privacy, App Attest, Trust Insights watch items, and AI action audit.
<!-- dual-compat-end -->
## Read next
- `ios-development` for implementation; `vibe-security-skill` for system-level threat modelling.
