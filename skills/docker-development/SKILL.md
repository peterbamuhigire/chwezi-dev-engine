---
name: docker-development
description: Docker and Docker Compose standards for PHP, Python, JavaScript, and API services. Use when containerizing development environments, production images, CI builds, PHP-FPM/Nginx stacks, Python sidecars, Node/JS services, or multi-service SaaS deployments.
metadata:
  portable: true
  compatible_with:
  - claude-code
  - codex
---

# Docker Development
Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178.

<!-- dual-compat-start -->
## Use When

- Containerizing PHP, Python, Node.js, JavaScript build, API, worker, queue, database, cache, or reverse-proxy services.
- Creating or reviewing `Dockerfile`, `compose.yml`, CI build, registry, or runtime deployment patterns.
- A project needs repeatable development environments, environment parity, production images, or service orchestration.

## Do Not Use When

- The task only needs application code and has no container, runtime, deployment, or environment concern.
- Kubernetes-specific cluster design is the main task; use Kubernetes skills after this container baseline is correct.

## Required Inputs

- Application stack, local development needs, production runtime, ports, volumes, secrets/config, persistence services, and target OS.
- Existing `Dockerfile`, Compose files, CI scripts, and deployment constraints when available.

## Workflow

1. Identify runtime roles: web, app/FPM, worker, scheduler, database, cache, queue, reverse proxy, asset build, or test runner.
2. Choose separate development and production image strategies.
3. Build minimal, reproducible images with pinned base versions and deterministic dependency installation.
4. Use Docker Compose for local multi-service orchestration, networking, volumes, health checks, and developer commands.
5. Keep secrets and environment-specific config outside images.
6. Add CI image build, scan, tag, push, and promotion rules.
7. Verify startup, health checks, logs, permissions, volume behavior, and graceful shutdown.

## Quality Standards

- Images are reproducible, minimal, patched, scanned, and tagged with immutable release identifiers.
- Development Compose is ergonomic without leaking dev-only tools into production images.
- PHP, Python, and Node dependencies are installed deterministically from lockfiles.
- Runtime config comes from environment/secrets, not baked source edits.
- Containers expose health checks, structured logs, and graceful stop behavior.
- Volumes are explicit and do not hide built artifacts unexpectedly.

## Anti-Patterns

- One container running web server, database, queue worker, and scheduler because it is convenient.
- Using `latest` tags in production.
- Copying `.env`, secrets, test data, or host-specific paths into images.
- Installing debug tooling in production images.
- Rebuilding separate artifacts per environment instead of promoting one tested image.
- Assuming Windows file permissions and Linux container permissions behave the same.

## Outputs

- Dockerfile/Compose guidance, container architecture notes, review findings, CI image-build plan, or runtime checklist.

## References

- `references/php-python-js-container-delivery.md`
- `references/source-register.md`
<!-- dual-compat-end -->

## Pair With

- `php-modern-standards` for PHP app/FPM/Composer rules.
- `python-modern-standards` for Python services, workers, and dependency locking.
- `javascript-modern`, `nodejs-development`, or TypeScript skills for Node/runtime asset builds.
- `api-design-first` for API contract/runtime responsibilities.
- `deployment-release-engineering` for build-once promotion, rollout, and rollback.
