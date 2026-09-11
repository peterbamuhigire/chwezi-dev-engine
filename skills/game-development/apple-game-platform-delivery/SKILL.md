---
name: apple-game-platform-delivery
description: Use when delivering a game on iOS, iPadOS, or macOS with Apple-native services, Metal diagnostics, controllers, haptics, cloud saves, signing, notarisation, sandboxing, or Mac window and display behaviour.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Apple Game Platform Delivery

Own the Apple-specific boundary between a game engine or SpriteKit project and a tested, distributable iPhone, iPad, or Mac game.

## Use When
- Integrating Apple game services or diagnosing Apple-only runtime, input, graphics, save, signing, or distribution failures.
- Choosing Mac App Store, direct notarised distribution, or another approved storefront.

## Do Not Use When
- The task is general iOS application work; use the iOS family.
- Current Apple requirements and the pinned Xcode/OS/engine versions cannot be verified.

## Required Inputs
Game/engine version, Xcode version, target OS and hardware matrix, distribution channel, bundle identifiers, entitlements, service/data map, signing ownership, save model, input/display requirements, and acceptance criteria.

## Workflow
1. Pin the toolchain and verify current Apple requirements from official sources.
2. Define platform adapters for identity, Game Center, controllers, haptics, cloud saves, purchases, lifecycle, and diagnostics; keep gameplay independent.
3. Specify Mac windowed/full-screen behaviour, Retina scaling, multi-display changes, keyboard/mouse/controller remapping, focus loss, and safe save locations.
4. Test Metal-relevant failures on representative Apple hardware and retain captures with build, device, OS, scene, and conditions.
5. Rehearse certificate/provisioning failure, entitlement mismatch, offline service failure, save conflict, suspend/terminate, and controller disconnect.
6. Archive once, retain symbols/checksums, and promote the tested artefact through signing, hardened-runtime, sandbox, notarisation, and channel gates as applicable.

## Quality Standards
- Never transplant obsolete Swift, SpriteKit, Game Center, or Xcode APIs from a book; preserve only the architectural lesson and verify the current API.
- Apple services degrade without corrupting local state or blocking offline-capable play.
- No signing key or service secret enters the client repository.

## Anti-Patterns

- Treating simulator success as device proof. Fix: exercise representative physical devices.
- Rebuilding after release approval. Fix: promote the identical tested archive by checksum.
- Assuming an entitlement is available. Fix: verify account, target, capability, and denied state.
- Hiding save or service failure. Fix: define offline, retry, conflict, and recovery behaviour.
- Storing signing material in source. Fix: use named custodians and recoverable secret storage.

## Outputs
Apple platform contract; service adapters; device/display/input matrix; entitlement and signing register; tested archive with symbols/checksum; distribution and rollback record.

## References
- [Apple game delivery gates](references/apple-game-delivery-gates.md)

<!-- dual-compat-start -->
## Evidence Produced

| Category | Artifact | Format | Example |
| --- | --- | --- | --- |
| Release evidence | Apple game platform release pack | Markdown plus build/test output | device, entitlement, controller, save, signing, notarisation, failure, and recovery |
<!-- dual-compat-end -->

