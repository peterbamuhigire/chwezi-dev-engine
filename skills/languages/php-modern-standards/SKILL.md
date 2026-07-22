---
name: php-modern-standards
description: Use when writing or reviewing PHP 8+ applications, object-oriented domain code, Laravel services, PSR-compliant packages, secure request handling, tests, or performance-sensitive PHP.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# PHP Modern Standards
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Modern PHP development standards for maintainable, testable, object-oriented code. Use when writing PHP 8+ applications, implementing OOP patterns, ensuring security, following PSR standards, optimizing performance, or building Laravel...

## Workflow

- For long-lived PHP application work, load `references/world-class-php-oop-clean-architecture.md` before designing controllers, services, repositories, or domain objects.
- For containerized PHP work, pair with `docker-development`.

## Evidence Produced

| Category | Artifact | Format | Example |
|----------|----------|--------|---------|
| Correctness | PHP test plan | Markdown doc per `skill-composition-standards/references/test-plan-template.md` covering unit, integration, and contract tests | `docs/php/test-plan-checkout.md` |
| Operability | PHP-FPM operations note | Markdown doc covering opcache, request lifecycle, and OPcache reset procedure | `docs/php/fpm-ops-note.md` |

## References

- Use the `references/` directory for deep detail after reading the core workflow below.
- Use the `examples/` directory for concrete patterns when implementation shape matters.
<!-- dual-compat-end -->
Production-grade PHP patterns for maintainable, testable, secure, high-performance applications.

**Core Principle:** Write type-safe, secure, performant PHP code following PSR standards with modern PHP 8+ features.

**References:**
- `references/performance-efficiency.md` — generators, OPcache, profiling, Fibers deep dive
- `references/code-quality-tooling.md` — PHPStan, Pint config, CI/CD patterns
- `references/rate-limiting.md` — rate limiting patterns
- `references/message-queues.md` — queue patterns
- `references/cache-invalidation.md` — cache invalidation patterns
- `references/resilience-patterns.md` — circuit breakers, retries
- `references/restful-api-patterns.md` — cURL client, Attribute routing, JWT, API versioning, testing
- `references/database-orm-patterns.md` — PDO, QueryBuilder, Active Record Model, soft delete, ORM concepts
- `references/attack-prevention.md` — SQL injection, XSS, CSRF, CSP, brute force, least privilege
- `references/world-class-php-oop-clean-architecture.md` — PHP 8 OOP, SOLID, clean architecture, repositories, adapters, and framework-independent domain rules
- `references/source-register-dev-engine.md` — local EPUB sources used for this development-engine upgrade
- `references/php-security.md` - absorbed PHP-specific security hardening, sessions, validation, crypto, upload, and deployment guidance
- `references/php-vs-nextjs.md` - absorbed PHP vs Next.js architecture decision guidance
- `references/javascript-php-integration.md` - absorbed integration patterns for PHP-rendered pages and JavaScript modules
**Examples:** `examples/modern-php-patterns.php`, `examples/laravel-patterns.php`
**Security:** Load `references/php-security.md` for comprehensive security patterns.

- Use for PHP 8+, OOP, security, testing, performance, and Laravel; do not use for legacy PHP below 7.4 or WordPress-specific work.

---

## File Structure

```php
<?php

declare(strict_types=1);

namespace App\Domain\User;

use App\Domain\Shared\ValueObject;

final readonly class User
{
    public function __construct(
        private int $id,
        private string $email,
    ) {
    }
}
```

**Rules:** Always `declare(strict_types=1)`, one class per file, namespace = directory, import all dependencies.

### Cross-Platform File Naming (MANDATORY)

Code runs on Windows (dev), Ubuntu (staging), and Debian (production). Linux is case-sensitive:

- **Class files:** PascalCase matching class name (`StaffService.php`)
- **Config dirs:** lowercase (`src/config/`, `src/lang/`)
- **Module dirs:** PascalCase matching namespace (`src/HR/Services/`)
- **require/include:** Must match EXACT case on disk
- **Paths:** Use `/` (forward slash). Never hardcode `C:\`. Use `sys_get_temp_dir()` for temp files.

---

## Additional Guidance

Extended guidance for `php-modern-standards` was moved to [references/skill-deep-dive.md](references/skill-deep-dive.md) to keep this entrypoint compact and fast to load.

### PHP DevOps Runtime Discipline

When PHP work affects deployment, Docker, or production operations, pair this skill with `docker-development` and `deployment-release-engineering`, then apply the PHP delivery notes in `../deployment-release-engineering/references/devops-book-patterns.md`:

- keep Composer lockfiles and dependency installation reproducible;
- run static analysis, coding standards, and tests in CI before packaging;
- manage `.env` and secrets outside version control;
- document PHP-FPM pool settings, OPcache reset or warm-up, queue worker restart, cache clear/warm, and file-permission steps;
- include database migration order, backup, verification queries, and rollback or compensating actions;
- verify server updates, unattended security updates, web server config, and backup/restore for uploaded files.

Use that deep dive for:
- `Type System`
- `Modern Features`
- `Performance`
- `SOLID Principles`
- `Control Flow`
- `Security (Essentials)`
- `Testing`
- `Laravel Conventions`
- `Code Quality Tooling`
- `PSR Standards`
- `Anti-Patterns`
- `Checklist`

## Decision Rules

| Condition | Action |
|---|---|
| Boundary accepts external data | Validate into typed input before domain logic |
| Framework convention is secure and testable | Prefer it over a custom abstraction |
| Change affects persistence or queues | Define transaction, retry, and idempotency behaviour |

## Degraded Mode

Fallback: without execution, provide exact Composer, static-analysis, and test commands. Do not assume framework support without dependency metadata.

## Domain Anti-Patterns

- Concatenating user input into SQL.
- Hiding domain behaviour in controllers.
- Catching `Throwable` without recovery policy.
- Adding mutable service-locator dependencies.
- Claiming compatibility without checking Composer constraints.
## Inputs
| Artefact | Required? | Purpose |
|---|---|---|
| PHP version, framework, code, and repository standards | yes | Apply compatible typing, security, and tooling rules |
## Outputs
- Produce PHP code or findings with static-analysis, test, security, and compatibility evidence.
## Capability contract
Read/search and local static checks are allowed. Dependency changes, migrations, deployment, and production execution require explicit task authority.
