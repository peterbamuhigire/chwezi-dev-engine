# GitHub Pages Deployment

Use when publishing a static site, SPA build, documentation site, or
Storybook to GitHub Pages; when attaching a custom domain; or when auditing an
existing Pages setup for takeover risk, stale actions, or broken routing.
Website content and design stay with the website and design engines; this
reference covers the repository, workflow, DNS, and verification steps.

## Decide first: is Pages the right host?

| Condition | Decision |
|---|---|
| Public static content: docs, portfolio, marketing page, open-source demo, Storybook | Pages is a good fit |
| Needs server code, secrets at request time, auth, forms that store data | Not Pages; use a platform with a backend |
| Commercial storefront, SaaS product, or handling passwords/card numbers | Not Pages; GitHub's terms prohibit these uses |
| Published output > 1 GB, or traffic likely above ~100 GB/month | Not Pages (published-site limit 1 GB; soft bandwidth limit 100 GB/month) |
| Private repository | Needs a paid plan; the published site is still public unless the org uses Enterprise Cloud private Pages |

## Inputs

- Repository and owner; site type: user/org site (`<owner>.github.io` repo,
  served at the root) or project site (served at `/<repo>/`).
- Build tool and output folder (Vite `dist/`, Astro `dist/`, Jekyll `_site/`,
  Storybook `storybook-static/`).
- Custom domain, if any, and who controls DNS.
- Authority: enabling Pages, changing DNS, and verifying domains are
  user-authorised actions; prepare them, do not perform them unasked.

## Procedure: deploy with GitHub Actions (default)

Prefer the Actions source over "Deploy from a branch" for anything with a
build step: no build output committed to the repo, no `gh-pages` branch
drift, and environment protection applies.

1. Repository Settings -> Pages -> Build and deployment -> Source:
   **GitHub Actions**.
2. Set the build's base path for project sites (Vite: `base: "/<repo>/"`;
   Astro: `base`; Next.js static export: `basePath`). User/org sites and
   custom domains use `/`.
3. Add `.github/workflows/pages.yml`:

```yaml
name: Deploy site to Pages
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false   # never cancel a deployment mid-flight

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: 22
          cache: npm
      - uses: actions/configure-pages@v6
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v5
        with:
          path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v5
```

4. For supply-chain hardening, pin each action to a full commit SHA with the
   version in a comment, and let Dependabot (`package-ecosystem:
   github-actions`) propose bumps.
5. Protect the `github-pages` environment: restrict deployment branches to
   `main` (or release tags), add required reviewers for production sites.
6. Push, then confirm with `gh run watch` and open the `page_url` output.

Rules:

- `upload-pages-artifact` v4+ excludes dotfiles by default. If the site
  needs `.well-known/` (for example app-links or security.txt), set
  `include-hidden-files: true` (v5 input).
- Keep the deploy job separate and dependent on build (`needs`); a deploy job
  without the artifact fails.
- Deployments time out after 10 minutes; keep the artifact lean.
- Actions-based deploys are exempt from the 10-builds-per-hour soft limit that
  applies to branch builds.

## Single-page app routing

Pages serves static files only; deep links to client routes return 404.

| Option | Use when | Trade-off |
|---|---|---|
| Pre-render every route to its own `index.html` (SSG) | Content is known at build time | Best for SEO and first load |
| Copy `index.html` to `404.html` after build | Pure SPA, few crawlable routes | Deep links render, but the HTTP status is 404; crawlers may skip them |
| Hash routing (`/#/orders`) | Internal tools on Pages | Ugly URLs, no server-side meaning |

Also set the router's basename to the project path for project sites.

## Procedure: custom domain with HTTPS

1. **Verify the domain first** (profile or organisation Settings -> Pages ->
   Add a domain -> add the TXT record). Verification stops other accounts
   claiming your subdomains.
2. Add the domain in the repository's Settings -> Pages -> Custom domain.
   With the Actions source, no `CNAME` file is created and any existing one is
   ignored; with branch publishing, the setting commits a `CNAME` file.
3. Create DNS records at the provider:

| Domain type | Records |
|---|---|
| Subdomain (`www.example.ug`, `docs.example.ug`) | `CNAME` -> `<owner>.github.io` (never include the repo name) |
| Apex (`example.ug`) | `A`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `AAAA`: 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153; or `ALIAS`/`ANAME` to `<owner>.github.io` |

   Configure both apex and `www` so GitHub redirects between them.
4. Never create wildcard records (`*.example.ug`) pointing at Pages; they
   invite takeover even with a verified domain.
5. Check resolution: `dig www.example.ug +noall +answer` (or
   `Resolve-DnsName www.example.ug` on Windows) shows the CNAME chain to
   `<owner>.github.io`; the apex returns the four A records.
6. Tick **Enforce HTTPS** once available (certificate issuance can take up to
   24 hours). Remove any CAA record that excludes Let's Encrypt.
7. If the site is later unpublished or the domain removed from Pages, delete
   the DNS records the same day to close the takeover window.

## Verification gate

- [ ] `page_url` loads over HTTPS with a valid certificate; HTTP redirects.
- [ ] Apex and `www` both resolve and redirect to the canonical host.
- [ ] Deep link to a client route renders (or the chosen trade-off is
      documented).
- [ ] Assets load under the base path (no 404s in the network panel).
- [ ] Domain shows as verified; no wildcard DNS records.
- [ ] Workflow uses current action majors (or SHA pins) and least-privilege
      permissions; environment protection set.
- [ ] Lighthouse or equivalent run recorded if the site is public-facing;
      otherwise performance is `NOT_ASSESSED`.

## Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Blank page, JS 404s | Missing `base` for project site | Set base to `/<repo>/` |
| "Get Pages site failed" in `configure-pages` | Pages not enabled or source not set to Actions | Enable Pages with Actions source (or `enablement: true` with an admin token) |
| Deploy job cannot find artifact | Deploy not `needs: build`, or artifact name changed | Link jobs; keep default artifact name |
| Custom domain resets after deploy | Relying on a `CNAME` file with Actions source | Set the domain in repository settings |
| Enforce HTTPS greyed out | Certificate pending, DNS wrong, or CAA blocks issuer | Fix DNS/CAA, wait, re-save the domain |
| `.well-known` missing | Dotfiles excluded by default | `include-hidden-files: true` |

## Premium vs. generic

Generic output copies a 2021 `peaceiris/actions-gh-pages` workflow that
pushes build output to a `gh-pages` branch, adds a wildcard DNS record "to be
safe", and never verifies the domain. Senior output uses the official Pages
actions at current majors with least-privilege permissions, protects the
environment, verifies the domain before pointing DNS, handles SPA routing
deliberately, and records the verification gate.

## Worked example (original)

A Gulu-based agritech NGO publishes its Astro documentation site from
`docs-site` to `docs.agrilink.ug`. The org verifies `agrilink.ug`, adds a
CNAME `docs` -> `agrilink-org.github.io`, sets `base: "/"` because of the
custom domain, includes hidden files so `/.well-known/security.txt` ships,
and restricts the `github-pages` environment to `main`. The first run
publishes in under two minutes; HTTPS is enforced the next morning.

## Evidence/currentness

Accessed 2026-09-24: docs.github.com Pages articles "Using custom workflows
with GitHub Pages", "Managing a custom domain for your GitHub Pages site",
and "GitHub Pages limits"; GitHub releases API for actions/deploy-pages
(v5.0.1, 2026-09-01; v5.0.0 moved to Node 24), actions/upload-pages-artifact
(v5.0.0, 2026-04-10; v4.0.0 excluded dotfiles), actions/configure-pages
(v6.0.0, 2026-03-25), actions/checkout (v7.0.1, 2026-07-20),
actions/setup-node (v7.0.0, 2026-07-14). The GitHub docs example still shows
older majors (checkout v6, configure-pages v5, upload-pages-artifact v4,
deploy-pages v4); the workflow above uses the latest release majors.
`NOT_ASSESSED`: whether the docs will change the recommended majors; private
Pages availability per plan beyond Enterprise Cloud; the CAA note is general
TLS practice, not quoted from GitHub docs.

Sources: Bin Uzayr (2022) *Mastering GitHub Pages: A Beginner's Guide*
(concept input for site types, publishing sources, and custom domains;
branch-publishing and Jekyll-first guidance superseded by the Actions
source); docs.github.com.
