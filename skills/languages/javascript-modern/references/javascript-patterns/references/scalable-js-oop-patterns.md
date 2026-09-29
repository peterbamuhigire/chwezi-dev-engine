# Scalable JavaScript OOP And Design Patterns

Use this reference when JavaScript code needs durable structure rather than ad hoc event handlers.

## OOP Ground Rules

- JavaScript classes are syntax over prototypes. Understand prototype lookup before designing inheritance-heavy APIs.
- Prefer object literals, modules, closures, and composition for most browser code.
- Use classes when they create a clearer public contract or when instances have meaningful state and behavior.
- Use private fields (`#field`) or closure scope for data that must not be reachable from callers.
- Do not define per-instance methods inside constructors unless each instance truly needs a unique function.
- Be deliberate with `this`: event handlers, extracted methods, arrow functions, and strict mode all affect binding.

## Pattern Selection

| Problem | Pattern | Use carefully because |
|---|---|---|
| Consistent object creation | Factory / Builder | Can hide too much if validation is weak |
| One shared runtime service | Singleton / module singleton | Can become global mutable state |
| Decouple notifications | Observer / PubSub | Can become hard to trace without event names and payload contracts |
| Swap algorithms | Strategy | Too many strategies can obscure simple branching |
| Undoable or queued actions | Command | Requires clear command lifecycle and error handling |
| Hide third-party API shape | Adapter / Facade | Must not become a dumping ground |
| Add behavior around an object | Decorator / Proxy | Can make debugging difficult if overused |
| Explicit workflow states | State machine | Requires clear state/event table |
| Coordinate UI modules | Mediator | Can become a central god object |

## Browser SaaS Module Rules

- One feature module owns one UI area or workflow.
- Modules expose a small public API: `init`, `destroy`, `refresh`, or domain-specific commands.
- Use event delegation for dynamic lists and tables.
- Use repositories or API clients for data access; do not scatter `fetch` calls inside every widget.
- Define event payload shapes for PubSub/Mediator flows.
- Provide teardown for listeners, intervals, observers, and third-party widgets.

## Async And Performance Patterns

- Use debouncing for typing/search inputs and throttling for resize/scroll.
- Use limited concurrency for bulk requests; do not fire unbounded `Promise.all` over large data sets.
- Use `AbortController` for requests tied to route changes, modals, or live search.
- Centralize error handling so UI states are consistent.
- Avoid memory leaks from retained DOM references, observers, global listeners, and never-cleared timers.

## Anti-Patterns

- God Object: one module owns users, payments, logging, UI, and API calls.
- Spaghetti events: string events with undocumented payloads and no ownership.
- Premature patterning: using five patterns where one small function would do.
- Exposed secrets or sensitive config through singleton accessors.
- XSS through observer/event payloads rendered with `innerHTML`.
- CSRF-prone request factories that skip token/header policy.

## Review Checklist

- [ ] Pattern choice is written down when it materially affects architecture.
- [ ] Module has a small public API and private implementation details.
- [ ] `this` binding is intentional and tested where callbacks are passed around.
- [ ] API access is centralized.
- [ ] Event names and payloads are documented.
- [ ] Listeners/timers/observers are cleaned up.
- [ ] Security-sensitive rendering avoids unsafe HTML injection.
