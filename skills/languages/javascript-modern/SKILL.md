---
name: javascript-modern
description: Use when writing or reviewing modern JavaScript for browser or PHP-backed SaaS applications, including modules, asynchronous flows, error handling, language features, and performance.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# javascript-modern
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Modern JavaScript (ES6+) patterns for PHP+JavaScript SaaS apps: modules, async/await, destructuring, Proxy/Reflect, generators, WeakMap/WeakSet, optional chaining, error handling, and performance patterns. Use when writing JavaScript for web...

## Workflow

- For OOP-heavy browser modules, reusable UI widgets, or complex stateful workflows, pair with `references/javascript-patterns.md` and load `references/javascript-patterns.md`.
- For Node/runtime container work, pair with `docker-development`.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | JavaScript module test plan | Markdown doc covering async, generators, Proxy, and module boundary tests | `docs/web/js-module-tests.md` |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
- Use `references/javascript-advanced.md` when the task needs deeper ES language mechanics, async patterns, metaprogramming, or performance.
- Use `references/javascript-patterns.md` when the task involves OOP, prototypes, design patterns, event modules, or maintainable browser architecture.
<!-- dual-compat-end -->
Expert-level ES6+ patterns for PHP+JavaScript SaaS developers. Assumes fluency with variables, loops, and functions.

## Architecture Rule (Non-Negotiable)

JavaScript belongs in its own `.js` files. PHP only emits a `<script src="...">` tag or passes config via a single JSON data attribute. No `<?php echo $var ?>` scattered through JS files.

```php
<!-- PHP emits one data attribute — no inline JS -->
<div id="app-config"
     data-config='<?= json_encode($config, JSON_HEX_APOS) ?>'
     data-user='<?= json_encode(['id' => $user->id, 'role' => $user->role]) ?>'>
</div>
```

```javascript
// assets/js/app.js — reads config cleanly from its own file
const config = JSON.parse(document.getElementById('app-config').dataset.config);
const user   = JSON.parse(document.getElementById('app-config').dataset.user);
```

---

## 1. Module Pattern (IIFE + ES Modules)

```javascript
// assets/js/modules/user-table.js
const UserTable = (() => {
    let tableInstance = null;           // private — unreachable from outside

    function init(config) { tableInstance = new DataTable('#users-table', config); }
    function refresh()    { tableInstance?.ajax.reload(); }

    return { init, refresh };           // public API only
})();

export default UserTable;

// Named exports for shared utilities: assets/js/core/utils.js
export function debounce(fn, delay) { /* ... */ }
export function throttle(fn, limit) { /* ... */ }
```

---

## Additional Guidance

Extended guidance for `javascript-modern` was moved to [references/skill-deep-dive.md](references/skill-deep-dive.md) to keep this entrypoint compact and fast to load.

Use that deep dive for:
- `2. Async/Await — The Right Patterns`
- `3. Production-Grade Fetch Wrapper`
- `4. Destructuring — Beyond the Basics`
- `5. Optional Chaining and Nullish Coalescing`
- `6. Generators for Pagination / Lazy Data`
- `7. WeakMap for Private Data and DOM Metadata`
- `8. Proxy for Validation and Reactivity`
- `9. Error Handling Strategy`
- `10. Event Delegation (Performance Pattern)`
- `11. Debounce and Throttle`
- `12. LocalStorage with Expiry`
- `13. `const` / `let` and Arrow Function `this``
- Additional deep-dive sections continue in the reference file.

## Decision Rules

| Condition | Action |
|---|---|
| Code is shared across features | Use explicit ES modules with narrow exports |
| Work is CPU-bound | Move it off the main thread or backend |
| Legacy IIFE is stable and isolated | Preserve it unless tested conversion adds value |

## Capability Contract

Read and search are required. Editing and browser or test execution require authorisation; network access is optional.

## Degraded Mode

Fallback: without execution, provide a patch plus exact lint, unit, and browser checks still required.

## Domain Anti-Patterns

- Starting asynchronous work without handling rejection.
- Using global mutable state instead of module scope.
- Adding a dependency for a native language operation.
- Blocking the main thread with large synchronous transforms.
- Changing module format without checking runtime compatibility.
## Inputs
| Artefact | Required? | Purpose |
|---|---|---|
| JavaScript target, runtime, code, and project conventions | yes | Select compatible language and module patterns |
## Outputs
- Produce reviewed JavaScript, findings, tests, and compatibility notes.
