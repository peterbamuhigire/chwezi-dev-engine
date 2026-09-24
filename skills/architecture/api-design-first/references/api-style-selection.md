# API Style Selection

Parent skill: [`api-design-first`](../SKILL.md). Load this reference before the
design workflow whenever the interaction style is not already fixed by an
existing contract: REST vs GraphQL vs gRPC vs webhooks vs WebSocket vs
Server-Sent Events vs broker messaging vs feeds, or a mix of them.

The output of this reference is a recorded style decision per interaction
(not per system), with the rejected alternatives and the failure each rejection
avoids. A system usually needs two or three styles; one style for everything is
a smell, not a simplification.

## Inputs

| Input | Where it comes from | If missing |
| --- | --- | --- |
| Interaction list: who calls whom, direction, trigger | Critical-flow table (`system-architecture-design`) | Stop; styles cannot be chosen without directions |
| Consumer inventory: browser, native app, partner server, internal service, AI agent, data-science notebook | Consumer research / product | Assume the widest audience and mark `NOT_ASSESSED` |
| Latency and freshness budget per interaction | NFRs / SRS | Record as open risk; do not pick streaming "just in case" |
| Delivery guarantee needed: best-effort, at-least-once, ordered | Domain owner | Default to at-least-once plus idempotent consumer |
| Team and platform capability (proxies, gateways, broker ops, codegen CI) | Engineering lead | Penalise styles that need new operational skills |

## Step procedure

1. List every interaction as a row: `initiator -> receiver, trigger, payload size, frequency, freshness`.
2. Classify each row on four axes: direction (request-response, server push,
   bidirectional, fan-out), coupling (who must be online), consumer control
   over shape, and trust boundary (public internet, partner, private network).
3. Apply the decision matrix below. Pick the style whose "choose when" column
   matches and whose "reject when" column does not.
4. Record the decision in the API contract README or an ADR: chosen style, two
   rejected styles, the failure each rejection avoids, and the contract format
   (OpenAPI, GraphQL SDL, `.proto`, AsyncAPI, Standard Webhooks event catalogue).
5. Check the combination: every style you add must justify its operational
   cost (gateway rules, auth model, observability, docs toolchain, contract tests).
6. Hand the decision to the rest of `api-design-first` (contract, auth, errors,
   idempotency, observability) per style.

## Decision matrix

| Style | Choose when | Reject when | Contract format | Failure if chosen wrongly |
| --- | --- | --- | --- | --- |
| REST over HTTP | Public or partner API; resource-shaped data; broad client reach; HTTP caching/CDN wanted; unknown consumer stacks | Consumers need many differently shaped projections of a graph; high-rate internal RPC with strict latency | OpenAPI 3.1 (3.2 where tooling supports it) | Chatty clients doing N round trips; ad-hoc "action" endpoints that break the resource model |
| GraphQL | Several first-party clients (web, mobile, agent) needing different projections of the same graph; BFF or federation layer | Simple CRUD; public anonymous API; file upload heavy; team cannot operate query cost limits | GraphQL SDL + persisted operations | Query-complexity denial of service; cache misses at CDN; errors hidden in HTTP 200 bodies |
| gRPC | Internal service-to-service calls across languages; streaming between services; strict typed contract with codegen | Browser is a direct caller (needs a proxy such as grpc-web or Connect); partners without protobuf tooling | `.proto` files with a breaking-change linter | Browser integration via bolt-on proxies; codegen drift across repos |
| Webhooks (outbound callbacks) | Notify a partner system that an event happened; partner cannot hold a connection open; low-to-moderate event rate | Receiver is a browser or phone; ordering across events is mandatory; very high fan-out | Event catalogue + Standard Webhooks headers; OpenAPI 3.1+ `webhooks` section | Lost events with no replay; unsigned calls accepted; retries causing duplicate side effects |
| Server-Sent Events | One-way server-to-browser updates (progress, live status, token streaming from an LLM) over plain HTTP | Client must send frequent messages on the same channel; binary frames | OpenAPI 3.2 sequential media type `text/event-stream`, or prose + examples | Reinventing bidirectional messaging over two channels; proxies buffering the stream |
| WebSocket | Low-latency bidirectional traffic: chat, collaborative editing, live dispatch boards, multiplayer | Updates are one-way (use SSE); clients are intermittently connected phones on poor networks without a reconnect strategy | AsyncAPI 3.x | Stateful connection fleet that cannot scale; auth checked only at handshake |
| Broker messaging (queues, topics, event streams) | Decoupled, asynchronous workflows; guaranteed delivery between internal services; load levelling; many producers and consumers | The caller needs an answer to continue (payments authorisation at checkout); the team cannot operate a broker | AsyncAPI 3.x + schema registry | Cumulative latency, duplicates, ordering bugs, dead-letter queues nobody reads |
| Web feeds (Atom/RSS, JSON Feed) | Public, pull-based content syndication where consumers poll at their own pace | Personalised or private data; delivery guarantees needed | Feed format spec | No contract or delivery signal; polling load |
| Long-running operation over REST (`202 Accepted` + status resource) | A request triggers work longer than a sane HTTP timeout (report generation, model training, bulk import) | Work finishes within the latency budget | OpenAPI with an operation/task resource | Timeouts and client retries starting duplicate jobs |

### Tie-breakers

- North-south traffic (clients into the platform) defaults to REST; east-west
  traffic (service to service) may use gRPC or messaging. Do not expose the
  internal style to external consumers just because it exists.
- If the only argument for GraphQL is "clients might want different fields",
  offer sparse fieldsets or a BFF endpoint first.
- If the only argument for WebSocket is "real time", check whether the data
  flows one way. It usually does; SSE or webhooks are cheaper.
- Polling is acceptable when freshness tolerance exceeds the poll interval and
  the poll is cheap (conditional GET with `ETag`). Record the interval.
- A synchronous step that must return a business answer stays synchronous; move
  only its side effects (notifications, ledger projections) to messaging.

## Style-specific non-negotiables

| Style | Must have before release |
| --- | --- |
| REST | Versioning policy, error contract (RFC 9457 mapping), pagination, idempotency on side-effecting POST, rate-limit responses |
| GraphQL | Depth and cost limits, alias and batch limits, persisted/allow-listed operations in production, introspection disabled or gated in production, per-field authorisation |
| gRPC | mTLS or token auth between services, deadlines on every call, reflection disabled on externally reachable servers, breaking-change lint on `.proto` in CI |
| Webhooks | Signed payloads (HMAC or asymmetric), timestamp tolerance check, unique event ID for de-duplication, retry with backoff and jitter, replay endpoint or dashboard, SSRF-safe egress |
| SSE | Heartbeat comments to defeat idle timeouts, `id:` fields so reconnect resumes, auth via cookie or short-lived query token (EventSource cannot set custom headers) |
| WebSocket | Origin allow-list, TLS (`wss://`), per-message authorisation for privileged actions, reconnect with jittered backoff, application-level acknowledgement for messages that matter, max connections per node |
| Messaging | Message schema with version, idempotent consumers, dead-letter handling with an owner, correlation ID propagation, documented delivery guarantee |

## Original worked example: Kampala school-fees platform

A platform lets parents pay school fees by mobile money, lets bursars see
receipts, and lets a partner accounting package pull ledgers.

| Interaction | Decision | Rejected | Why |
| --- | --- | --- | --- |
| Parent app -> platform: create fees payment | REST `POST /v1/fee-payments` with `Idempotency-Key` | GraphQL mutation | Single resource, must be retry-safe on poor 3G; HTTP semantics and gateway rate limits fit |
| Mobile-money provider -> platform: payment result | Inbound webhook, signature verified, event ID de-duplicated | Polling the provider | Provider pushes; polling adds latency and cost |
| Platform -> bursar dashboard: live receipt list | SSE stream per school | WebSocket | One-way updates; SSE survives proxies and reconnects with `Last-Event-ID` |
| Payment service -> ledger and SMS services | Broker topic `fees.payment.settled.v1` | Synchronous REST fan-out | Ledger and SMS must not block the payment path; at-least-once plus idempotent consumers |
| Partner accounting package -> platform | REST with OAuth 2 client credentials, cursor pagination | gRPC | Partner stack unknown; REST tooling universal |

## Premium vs generic output

| Generic AI output | Senior-grade output |
| --- | --- |
| "We will use REST because it is the industry standard." | A per-interaction table with rejected alternatives and the failure each rejection avoids |
| Picks WebSocket for any "real-time" word | Separates one-way push (SSE/webhooks) from true bidirectional needs |
| One style for the whole system | North-south vs east-west split, justified by operational cost |
| No contract format named | Each style mapped to OpenAPI / SDL / proto / AsyncAPI / event catalogue |

## Quality gate

- [ ] Every interaction has exactly one chosen style and at least one rejected alternative with a stated failure mode.
- [ ] Each chosen style has its contract format and the non-negotiables above assigned to an owner.
- [ ] Delivery guarantee and idempotency rule stated for every asynchronous interaction.
- [ ] Browser, mobile-on-poor-network, partner, and AI-agent consumers each checked against the choice.
- [ ] Operational cost of every added style (gateway, broker, codegen, docs) acknowledged in the ADR.

## Evidence and currentness

Accessed 2026-09-24 (primary sources):

- OpenAPI Initiative, spec.openapis.org: 3.2.0 released 2025-09-19 (latest patch listed 3.2.1); 3.1 line current at 3.1.2. 3.2 adds `QUERY`/`additionalOperations`, sequential and streaming media types (SSE, JSON sequences), and the `querystring` parameter location. Tool support for 3.2 varies: verify your generator/validator before adopting it; `NOT_ASSESSED` per tool.
- AsyncAPI, asyncapi.com: latest specification 3.1.0 (channels plus `send`/`receive` operations; default Schema Object is a JSON Schema Draft 07 superset).
- Standard Webhooks specification (github.com/standard-webhooks): `webhook-id`, `webhook-timestamp`, `webhook-signature`; `v1` HMAC-SHA256 or `v1a` Ed25519; signed content `id.timestamp.payload`; payloads recommended under 20 KB; 2xx means delivered.
- WHATWG HTML Living Standard, Server-sent events: one-way, reconnect with `Last-Event-ID` and `retry`; `EventSource` cannot set custom request headers.
- Correction to older guidance: webhooks remain without an IETF standard; treat Standard Webhooks as a community specification, not an RFC.

Sources: Dynowski and Dulak (2025) *Learning API Styles*; Day (2024, early release) *Hands-On APIs for AI and Data Science*; engine skills `api-design-first`, `graphql-patterns`, `microservices-communication`.
