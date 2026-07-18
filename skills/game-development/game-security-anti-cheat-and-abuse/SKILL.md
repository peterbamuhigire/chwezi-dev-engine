---
name: game-security-anti-cheat-and-abuse
description: Use when threat-modelling a game client/server, validating actions, protecting game economy and accounts, detecting tampering or cheats, limiting bots and abuse, investigating incidents, or designing proportionate enforcement and appeals.
metadata: {portable: true, compatible_with: [claude-code, codex]}
---
# Game Security, Anti-Cheat, and Abuse

Reduce exploitable authority and player harm without claiming that an untrusted client can be made trustworthy.

## Use When
- Protecting competitive results, inventory/economy, accounts, matchmaking, chat/community, or client integrity.

## Do Not Use When
- The task is general application security only; compose with the security family.
- A proposed control requires invasive collection without privacy/legal review.

## Required Inputs
Assets and abuse cases, topology/authority, data flows, target platforms, player populations, economy model, threat actors, privacy constraints, telemetry, enforcement policy, appeal/support owner, and acceptable false-positive cost.

## Workflow
1. Threat-model client, transport, server, APIs, content pipeline, account, economy, social surfaces, and operations.
2. Move consequential validation to authoritative services and constrain rate, sequence, range, inventory, and replay.
3. Layer prevention, detection, investigation, containment, recovery, and communication; record evidence provenance.
4. Separate anomaly from guilt; calibrate thresholds and human review against false positives and accessibility tools.
5. Exercise forged messages, replay, speed/range violations, duplicated purchases/items, bot load, credential theft, toxic content, compromised telemetry, and rollback.

## Outputs
Threat/abuse model; authority and validation controls; signal register; privacy review; investigation/runbook; enforcement and appeal policy; red-team and recovery evidence.

## References
- [Game trust and enforcement model](references/game-trust-enforcement-model.md)

