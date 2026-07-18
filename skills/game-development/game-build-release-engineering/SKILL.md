---
name: game-build-release-engineering
description: Use when creating reproducible Unity, Godot, Unreal, Android, iOS, or macOS game build pipelines, manifests, symbols, signing boundaries, artifact promotion, patching, certification, or rollback rehearsals.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Build and Release Engineering

Produce one traceable game artefact, test it under release-like conditions, and promote that same artefact without hidden rebuilding.

## Use When
- Automating engine builds, packaging, signing, symbols, store/channel promotion, patches, or release trains.

## Do Not Use When
- Gameplay implementation is the task.
- A current platform requirement has not been verified from an official source.

## Required Inputs
Repository/tag, engine/toolchain locks, target matrix, build variants, dependencies/licences, secret/signing custody, test gates, distribution channels, patch/save policy, observability, and rollback objective.

## Workflow
1. Define a versioned build interface per engine and fail early on toolchain drift.
2. Build in a clean environment; produce artefact, symbols, dependency lock, SBOM/licence record, checksum, provenance, and machine-readable manifest.
3. Run automated, device, certification, install/upgrade, storage-pressure, offline, and crash-symbolication gates.
4. Keep signing in the narrowest controlled boundary; record signer and result without exposing credentials.
5. Promote the tested binary through environments/channels; never recompile after approval.
6. Rehearse rollback, save compatibility, revoked credential, failed upload, partial rollout, and unavailable dependency.

## Outputs
Build interface; CI configuration; release manifest; signed artefacts; symbols/checksums/SBOM; promotion ledger; certification evidence; rollback rehearsal.

## References
- [Reproducible game release contract](references/reproducible-game-release-contract.md)

