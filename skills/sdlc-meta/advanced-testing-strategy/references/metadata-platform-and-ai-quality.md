# Metadata-Driven Platform and AI Quality

This reference is a self-contained operational synthesis prepared from Niranjan
Gattupalli and RaviTeja Amerineni, *Mastering Salesforce Quality: A Strategic
Blueprint for Testing, Resilience, and AI-Ready Assurance*. It generalises the
book's quality-engineering patterns beyond Salesforce; platform-specific APIs
and current limits require separate verification.

## Quality layers

Map the change across user experience, business logic and automation, data model,
integrations, security, and operational dependencies. A small metadata or rule
change can trigger a distant workflow, event, integration, or access change.

## Evidence ladder

1. Fast unit or rule checks for local logic.
2. Integration and API checks at system seams.
3. Business-flow tests using safe, versioned data.
4. Exploratory testing for behaviour scripts cannot predict.
5. Performance, security, recovery, and release checks for the affected risk.

Keep test data synthetic or masked, provision it reproducibly, and retire it
under a defined lifecycle. Track leading indicators such as changed dependency
surface, failed checks, flaky tests, data drift, and untested metadata paths;
lagging indicators alone arrive after trust has already been lost.

## AI quality additions

Test permission alignment, unsafe or biased outputs, grounding and citations,
abstention, prompt/model version changes, drift, cost, latency, and human review.
For a non-deterministic result, assert safety and task invariants rather than
one exact string. Preserve audit evidence and a rollback or disable path.
