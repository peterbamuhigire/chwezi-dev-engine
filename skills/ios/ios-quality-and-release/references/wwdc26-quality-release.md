# WWDC26 Quality And Release

Use this reference for latest Apple-platform quality gates introduced or raised
at WWDC26.

## Swift Testing 6.4 Migration

- Use Swift Testing for new unit and integration tests.
- Keep XCTest for UI tests and legacy suites until migration is justified.
- Use Swift Testing/XCTest interoperability to migrate helpers gradually.
- Use issue severity for visible non-blocking diagnostics; do not downgrade real
  product defects to warnings.
- Use dynamic cancellation/skips only for unavailable hardware, locale, region,
  beta service, or Apple Intelligence conditions.

## Device Hub Matrix

Every release candidate should record:

- minimum supported iPhone/iPad runtime;
- latest iOS/iPadOS runtime;
- resized simulator run for adaptive layout;
- iPhone Mirroring check when relevant;
- physical device run for hardware capabilities;
- accessibility settings sweep.

## Xcode 27 Agent Evidence

If Xcode agents contributed code, require:

- prompt/task summary;
- files changed;
- tests run by agent and by human/CI;
- diff review note;
- no secrets or credentials in agent context;
- human approval for signing, billing, authorization, deletion, privacy, or
  data migration changes.

## AI And App Intents Gates

- Foundation Models/Core AI features need Evaluations, not just unit tests.
- App Intents/Siri integrations need App Intents Testing for entity lookup,
  action invocation, permission denial, and unavailable states.
- Tool-calling AI needs authorization and security test cases.
- Record provider/model/profile versions in release evidence.

## Instruments And MetricKit

- Use the Swift Concurrency instrument for async task scheduling, actor
  contention, and thread usage.
- Use Time Profiler and System Trace for CPU and system-level regressions.
- Use MetricKit during beta/TestFlight for launch, hang, memory, and crash
  signals where the app supports it.
- Keep before/after traces for performance claims.

## Xcode Cloud And TestFlight

- Verify Xcode Cloud workflows run on the intended Xcode version.
- Record build number, git SHA, scheme, signing identity, artifact, and test
  summary.
- Include Metal and visionOS build lanes only when the product actually uses
  those platforms.
- Localized releases should include string catalog review, plural variants, and
  locale screenshots where required.
