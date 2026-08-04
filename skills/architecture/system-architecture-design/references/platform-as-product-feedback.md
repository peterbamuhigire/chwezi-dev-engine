<!-- Source basis: Platform Enterprise early release, chapters 1-2 only; XP 2026 decision autonomy and architecture uncertainty papers. Later chapters were unavailable. -->

# Platform-as-Product Feedback

Apply when designing an internal developer platform, shared service, component
library, data platform, AI platform, or delivery capability.

## Platform contract

Define the platform as a product with named internal users and a service owner.
Document:

- primary user journeys, golden paths, and supported escape hatches;
- the problem and toil reduced, not only the technology supplied;
- interface, version, compatibility, security, reliability, cost, and support
  commitments;
- adoption, task-success, time-to-first-success, cognitive-load, failure,
  satisfaction, and deprecation signals;
- decision rights for platform owners, consuming teams, security, and operations;
- feedback intake, prioritisation, change communication, migration, and rollback.

## Sociotechnical review

Review structure, process, people, technology, and external constraints together.
If a platform change removes local autonomy, identify the coordination benefit,
the new escalation path, and the smallest standard that preserves team agency.
Use consultative or group decisions where the consequence spans consumers; record
the decision-maker, participants, timing, affected artefacts, and unresolved risk.

## Lifecycle loop

Baseline consumer pain and platform health. Ship a thin reversible improvement.
Observe adoption and failure evidence. Review qualitative feedback with telemetry.
Standardise only when consumer outcomes improve without increasing unsafe coupling,
toil, or support load. Retain a sunset path and revisit the contract.

This is an operational synthesis from an incomplete early release, not a complete
platform engineering standard.
