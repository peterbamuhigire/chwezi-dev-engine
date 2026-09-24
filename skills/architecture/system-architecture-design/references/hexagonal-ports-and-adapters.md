# Hexagonal Architecture (Ports and Adapters)

Absorbed from the retired `hexagonal-architecture` skill (origin: adapted from affaan-m/ECC
`skills/hexagonal-architecture/SKILL.md`). Load this reference once the system-level shape is
decided and the work is the internal boundary of one module or service: designing or refactoring
ports and adapters, dependency inversion, a composition root, or testable use-case orchestration
in TypeScript, PHP, Java, Kotlin, or Go.

Hexagonal architecture keeps business logic independent from frameworks, transport, and
persistence. The core depends on abstract ports; adapters implement those ports at the edges.

Boundaries: service topology stays with `skills/architecture/microservices-architecture`; the
shape of a public contract stays with `skills/architecture/api-design-first`. This reference
governs the internal ports/adapters structure behind that contract.

## Required inputs

- Domain use cases, boundary dependencies, and the target implementation language.

## Outputs

- Ports, adapters, module boundaries, composition root, and a migration or test record that
  verifies the dependency direction points inward.

## When to Use

- Building new features where long-term maintainability and testability matter
- Refactoring layered or framework-heavy code where domain logic is mixed with I/O concerns
- Supporting multiple interfaces for the same use case (HTTP, CLI, queue workers, cron jobs)
- Replacing infrastructure (database, external API, message bus) without rewriting business rules

## Core Concepts

- **Domain model**: business rules and entities/value objects. No framework imports.
- **Use cases (application layer)**: orchestrate domain behavior and workflow steps.
- **Inbound ports**: contracts describing what the application can do.
- **Outbound ports**: contracts for dependencies the application needs (repositories, gateways,
  event publishers, clock, UUID generator, etc.).
- **Adapters**: infrastructure and delivery implementations of ports (HTTP controllers, DB
  repositories, queue consumers, SDK wrappers).
- **Composition root**: single wiring location where concrete adapters are bound to use cases.

**Placement rule** (settles the usual argument): outbound port interfaces belong in the
**application** layer, not the domain — or in domain only when the abstraction is truly
domain-level (e.g. a `Clock` port a domain policy itself depends on).

Dependency direction is always inward: Adapters → application/domain; Application → port
interfaces; Domain → domain-only abstractions (no framework or infrastructure dependencies);
Domain → nothing external.

## How It Works

### Step 1: Model a use case boundary

Define a single use case with a clear input and output DTO. Keep transport details (an HTTP
request object, a queue payload wrapper, a CLI argv) outside this boundary.

### Step 2: Define outbound ports first

Identify every side effect as a port: persistence, external calls, cross-cutting concerns
(logger, clock). Ports model capabilities, not technologies.

### Step 3: Implement the use case with pure orchestration

The use case receives ports via constructor/arguments, validates application-level invariants,
coordinates domain rules, and returns plain data structures.

### Step 4: Build adapters at the edge

Inbound adapters convert protocol input to use-case input; outbound adapters map application
contracts to concrete APIs/ORM/query builders. Mapping stays in adapters, never inside use cases.

### Step 5: Wire everything in a composition root

Instantiate adapters, then inject them into use cases. Keep this wiring centralized to avoid a
hidden service-locator pattern.

### Step 6: Test per boundary

Unit test use cases with fake ports; integration test adapters with real infra; end-to-end test
user-facing flows through inbound adapters.

## Suggested Module Layout

```text
src/
  features/
    orders/
      domain/
        Order.ts
        OrderPolicy.ts
      application/
        ports/
          inbound/CreateOrder.ts
          outbound/OrderRepositoryPort.ts
                    PaymentGatewayPort.ts
        use-cases/CreateOrderUseCase.ts
      adapters/
        inbound/http/createOrderRoute.ts
        outbound/postgres/PostgresOrderRepository.ts
                  stripe/StripePaymentGateway.ts
      composition/ordersContainer.ts
```

## TypeScript Example

```typescript
export interface OrderRepositoryPort {
  save(order: Order): Promise<void>;
  findById(orderId: string): Promise<Order | null>;
}

export interface PaymentGatewayPort {
  authorize(input: { orderId: string; amountCents: number }): Promise<{ authorizationId: string }>;
}

export class CreateOrderUseCase {
  constructor(
    private readonly orderRepository: OrderRepositoryPort,
    private readonly paymentGateway: PaymentGatewayPort
  ) {}

  async execute(input: { orderId: string; amountCents: number }) {
    const order = Order.create({ id: input.orderId, amountCents: input.amountCents });
    const auth = await this.paymentGateway.authorize({ orderId: order.id, amountCents: order.amountCents });
    const authorizedOrder = order.markAuthorized(auth.authorizationId); // returns a new instance, no mutation
    await this.orderRepository.save(authorizedOrder);
    return { orderId: order.id, authorizationId: auth.authorizationId };
  }
}
```

## PHP Example (this engine's shipped stack)

```php
<?php declare(strict_types=1);

interface OrderRepositoryPort
{
    public function save(Order $order): void;
    public function findById(string $orderId): ?Order;
}

interface PaymentGatewayPort
{
    public function authorize(string $orderId, int $amountCents): AuthorizationResult;
}

final class CreateOrderUseCase
{
    public function __construct(
        private readonly OrderRepositoryPort $orders,
        private readonly PaymentGatewayPort $payments,
    ) {}

    public function execute(CreateOrderInput $input): CreateOrderOutput
    {
        $order = Order::create($input->orderId, $input->amountCents);
        $auth = $this->payments->authorize($order->id(), $order->amountCents());
        $authorized = $order->markAuthorized($auth->authorizationId()); // immutable: new instance
        $this->orders->save($authorized);

        return new CreateOrderOutput($order->id(), $auth->authorizationId());
    }
}
```

A plain-PHP or WAMP-hosted project without a framework's container can still wire this: a small
`composition/` file constructs the concrete repository/gateway and injects them, invoked from the
front controller.

## Multi-Language Mapping

- **TypeScript/JavaScript**: ports as interfaces/types under `application/ports/*`; use cases as
  classes/functions with constructor/argument injection; explicit factory/container for composition.
- **PHP**: ports as interfaces; use cases as `final` classes with constructor-promoted, typed
  dependencies; composition via a small factory/container file, framework DI container if one exists.
- **Java**: packages `domain`, `application.port.in`, `application.port.out`,
  `application.usecase`, `adapter.in`, `adapter.out`; composition via framework config or a manual
  wiring class, kept out of domain/use-case classes.
- **Kotlin**: mirrors the Java package split; ports as interfaces; use cases with constructor
  injection; module definitions or dedicated composition functions, avoiding service-locator patterns.
- **Go**: packages `internal/<feature>/domain`, `application`, `ports`,
  `adapters/inbound`, `adapters/outbound`; small interfaces owned by the consuming package; explicit
  `New...` constructors; wiring in `cmd/<app>/main.go`.

## Anti-Patterns to Avoid

- Domain entities importing ORM models, web framework types, or SDK clients
- Use cases reading directly from a request object, response object, or queue metadata
- Returning raw database rows from use cases without domain/application mapping
- Adapters calling each other directly instead of flowing through use-case ports
- Dependency wiring spread across many files with hidden global singletons

## Migration Playbook

1. Pick one vertical slice (single endpoint/job) with frequent change pain.
2. Extract a use-case boundary with explicit input/output types.
3. Introduce outbound ports around existing infrastructure calls.
4. Move orchestration logic from controllers/services into the use case.
5. Keep old adapters, but make them delegate to the new use case.
6. Add tests around the new boundary (unit + adapter integration).
7. Repeat slice-by-slice; avoid full rewrites.

### Refactoring existing systems

Strangler approach: keep current endpoints, route one use case at a time through new ports/adapters.
No big-bang rewrites — migrate per feature slice and preserve behavior with characterization tests.
Facade first: wrap legacy services behind outbound ports before replacing internals. Freeze
composition early so new dependencies do not leak into domain/use-case layers. Prioritize
high-churn, low-blast-radius flows first, and keep a reversible toggle per migrated slice until
production behavior is verified.

## Testing Guidance

- **Domain tests**: pure business rules, no mocks, no framework setup
- **Use-case unit tests**: fakes/stubs for outbound ports; assert business outcomes and port interactions
- **Outbound adapter contract tests**: shared contract suites run against each adapter implementation
- **Inbound adapter tests**: protocol mapping in and error mapping back out
- **Adapter integration tests**: real infrastructure for serialization, schema/query behavior, retries, timeouts
- **End-to-end tests**: cover critical user journeys through inbound adapter → use case → outbound adapter
- **Refactor safety**: add characterization tests before extraction; keep them until the new boundary's behavior is proven equivalent

## Best Practices Checklist

- Domain and use-case layers import only internal types and ports
- Every external dependency is represented by an outbound port
- Validation occurs at boundaries (inbound adapter + use-case invariants)
- Immutable transformations — return new values/entities instead of mutating shared state
- Errors are translated across boundaries (infra errors → application/domain errors)
- Composition root is explicit and easy to audit
- Use cases are testable with simple in-memory fakes for ports
- Refactoring starts from one vertical slice with behavior-preserving tests
- Language/framework specifics stay in adapters, never in domain rules

Evidence/currentness: language-neutral design guidance; the PHP example uses constructor
promotion and `readonly` properties (PHP 8.1+) and should be checked against the project's PHP
version. No other version-specific claims (reviewed 2026-09-24).
