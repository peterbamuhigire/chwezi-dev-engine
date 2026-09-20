# Book-informed implementation notes — 2026-09-20

The implementation began by reading the seven local Markdown book files Peter
specified. They are durable concept inputs, not current platform authority, and
no book text or copied examples were added to the engine.

| Book | Implementation principle used |
|---|---|
| Martin Fowler, *Refactoring* | Make small behaviour-preserving changes, keep independent tests green, and use explicit seams before structural cleanup. |
| Karl Wiegers, *Software Requirements Essentials* | Preserve problem, requirement, acceptance, traceability and change context across the SRS-to-engineering handoff. |
| *Building Secure and Reliable Systems* | Treat security, reliability, recovery, ownership and evidence as one operating contract; fail closed when proof is missing. |
| Martin Kleppmann, *Designing Data-Intensive Applications* | Bind decisions to data invariants, scope, consistency and recovery evidence rather than line-count claims. |
| Michael Nygard, *Release It!* | Make timeouts, retries, idempotency, degradation, observability and rollback explicit in high-risk decisions. |
| *Software Engineering at Google* | Prefer shared ownership, reviewable changes, documentation, measurable signals and sustainable maintenance over heroics. |
| Neal Ford et al., *Building Evolutionary Architectures* | Protect important architecture characteristics with executable fitness functions and make incremental change reversible. |

These principles led to the solution-decision schema, risk-scaled negative
proof, explicit SRS QC verdicts, scoped mode state, and hash-bound evidence.
They do not replace the local routers, Digital Research currentness gate,
design-system review, or Chwezi accounting doctrine.
