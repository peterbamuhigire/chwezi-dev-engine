# PHP, Python, And JavaScript Container Delivery

## Container Design

- Model containers by runtime role: reverse proxy, PHP-FPM app, queue worker, scheduler, Python sidecar, Node/API service, asset builder, database, cache, and mail/test helpers.
- Use Compose locally to make multi-service dependencies repeatable. Do not expect developers to hand-run multiple `docker run` commands.
- Keep development and production concerns separate. Development may mount source, expose debug ports, and include Xdebug/watchers; production images should be lean and immutable.
- Keep configuration outside the image. Images should work across environments through environment variables, secrets, and mounted runtime config.
- Prefer Linux production parity even when developers work on Windows.

## Dockerfile Standards

- Pin base images by major/minor runtime where practical.
- Use multi-stage builds when dependencies or asset builds differ from runtime needs.
- Copy dependency manifests before source code to preserve layer caching.
- Install dependencies from lockfiles:
  - PHP: `composer.lock`
  - Python: `uv.lock` or equivalent pinned lockfile
  - Node/JS: `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock`
- Keep `.dockerignore` strict: exclude `.git`, local caches, tests where not needed, docs where not needed, `.env`, secrets, node_modules/vendor unless intentionally copied, and generated output.
- Run as a non-root user where the base image and platform allow it.
- Add health checks at the service level or orchestrator level.

## PHP Containers

- Choose Apache/PHP images for simple legacy apps; choose Nginx + PHP-FPM for production-grade separation and static asset handling.
- Put PHP INI and FPM pool settings under version control as container config.
- Keep Xdebug and profiling out of production builds. Add them only through a dev target or dev image.
- Composer should install deterministic dependencies from `composer.lock`; production builds should use optimized autoload and no dev packages.
- For PHP-FPM deployments, document OPcache settings, warm/reset procedure, file permissions, queue worker restart, and scheduler behavior.
- Use separate containers/processes for web, queue workers, and scheduled tasks.

## Python Containers

- Use `src/` layout and deterministic dependency sync with `uv`.
- Validate settings at startup using `pydantic-settings`; fail fast if required environment variables are missing.
- Keep build tools out of runtime images when possible.
- Expose structured logs and health endpoints for FastAPI/worker services.
- Separate API, worker, scheduler, and one-off migration/maintenance commands.

## JavaScript And Node Containers

- Separate asset build stage from web/API runtime when using bundlers.
- Use `npm ci`, `pnpm install --frozen-lockfile`, or equivalent deterministic install.
- Never run production containers through dev servers such as Vite/webpack dev server.
- For Node services, define `NODE_ENV=production`, health checks, graceful SIGTERM handling, and memory limits.
- Avoid copying host `node_modules` into images.

## Compose Standards

- Compose service names become internal DNS names. Use service names for app-to-db/cache connections, not host ports.
- Host ports are for developer access only; internal services should communicate over the Compose network.
- Use named volumes for databases and caches when state must persist across restarts.
- Use bind mounts for development source code only.
- Add `depends_on` only for startup ordering; still make applications retry dependencies because readiness is not guaranteed.
- Keep separate files or profiles for dev/test/production-like workflows.

## Build, Registry, And Promotion

- Build once in CI, tag with commit SHA and release version, scan, then promote the same image.
- Do not rebuild separately for staging and production.
- Store registry credentials in CI secrets, not repository files.
- Use immutable tags for deployments; `latest` may exist for convenience but must not be the deployment selector.
- Record image digest in the release evidence bundle.

## Operational Checks

- `docker compose up --build` starts the local stack from a clean checkout.
- App can connect to database/cache using service names.
- Logs go to stdout/stderr.
- Health check fails when the app cannot serve real traffic.
- `docker stop` gives the service enough time to finish in-flight work.
- File permissions work on Linux even when development happens on Windows.
- Secrets are absent from image layers, git history, and logs.
