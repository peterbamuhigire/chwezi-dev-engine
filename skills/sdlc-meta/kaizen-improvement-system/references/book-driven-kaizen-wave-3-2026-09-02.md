# Book-driven Kaizen Wave 3: engineering application

Use this reference for software, AI, SaaS, security, product, UX, and technical-documentation
work across the engineering catalogue.

Owning skill: [Kaizen owner](../SKILL.md).

## Transfer controls

- Design explicit contracts for HTTP/API behavior, configuration, errors, retries, timeouts,
  observability, data structures, image handling, and deployment; verify them with tests and
  representative failed paths.
- Use Git state inspection, small branches/snapshots, reviewable commits, signed or otherwise
  attributable changes where policy requires, conflict recovery, and tested rollback.
- Prefer simple workflows over autonomous agents until evaluation demonstrates value. For agents,
  bound tools and inputs, least privilege, cost/latency budgets, human decision rights,
  circuit breakers, drift monitoring, and recovery evidence.
- Make testing information-seeking: select tests by risk and information value, test the test
  harness, retain honest data, and keep `NOT_ASSESSED` separate from pass.

## Boundaries

The books contain historical APIs, protocols, algorithms, commands, vulnerabilities, and model
claims. Do not copy unsafe exploit or shell procedures, old HTTP assumptions, or unverified
framework/MCP/cloud claims. Verify current primary sources through Digital Research.

## Measures and routing

Track defect escape, failed-path coverage, dependency currency, reproducible builds, change
failure/rollback, API contract conformance, agent eval quality, cost/latency, accessibility,
and time from finding to standardisation. Route to the owning domain skill and release gates.

## Currentness gate

At task time record current authority, access date, freshness class, support, uncertainty, and
review trigger for standards, APIs, frameworks, libraries, models, security, and lifecycle.
