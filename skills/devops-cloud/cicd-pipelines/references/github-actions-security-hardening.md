# GitHub Actions Security Hardening

Load this when writing, reviewing, or auditing any `.github/workflows/*.yml`
change, when a workflow gains cloud or registry credentials, when a repository
accepts pull requests from forks, or when self-hosted runners are proposed. It
is task guidance: a threat model, decision rules, a procedure, and a review
gate. OIDC trust-policy detail stays in `oidc-federation.md`; provenance and
SLSA stay in `supply-chain-provenance.md`.

## 1. Threat model in one table

A CI server holds powerful credentials, is reachable by every contributor, and
exists to execute code from the repository. Treat it as a production system
with a larger attack surface than production itself.

| Attack path | What the attacker needs | Primary control |
|---|---|---|
| Compromised third-party action (tag repointed to malicious commit) | Write access to the action's repo | Pin every external action to a full-length commit SHA |
| Script injection via PR title, branch name, issue body, commit message | Ability to open a PR or issue | Never interpolate `${{ github.event.* }}` into `run:`; pass through `env:` |
| Fork PR runs with secrets (`pull_request_target`, `workflow_run`) | A fork | Do not check out or execute fork code in privileged triggers |
| Over-privileged `GITHUB_TOKEN` | Any code execution in the job | Default read-only; grant write per job |
| Long-lived cloud keys in secrets | Any secret exfiltration | OIDC federation with subject-bound trust policy |
| Persistent self-hosted runner | One malicious job | Ephemeral just-in-time runners; never on public repos |
| Workflow file edited to exfiltrate | Merge rights | `CODEOWNERS` + ruleset on `.github/workflows/**` |
| Plan step granted apply-level permissions | Opening a PR | Split read-only plan identity from write apply identity |

## 2. Decision rules

| Condition | Action |
|---|---|
| Workflow uses an action outside your organisation | Pin to the 40-character SHA with the version as a trailing comment; add the action to the org allow-list |
| Organisation owns more than a handful of repos | Turn on the Actions policy that requires full-SHA pinning and blocks unapproved actions (available since 2025-08-15) |
| Workflow needs PR metadata in a shell step | Map it to `env:` and quote the variable; never inline the expression |
| Workflow must comment on or label fork PRs | Use `pull_request` for untrusted build/test; move the privileged write to a separate `workflow_run` job that consumes only data artifacts, never executables |
| Someone proposes `allow-unsafe-pr-checkout: true` | Reject unless a named security owner signs off in the PR; record why the build cannot run under `pull_request` |
| Job deploys or reads cloud resources | `permissions: { id-token: write, contents: read }` plus OIDC; no static keys |
| IaC plan on PR, apply on merge | Two roles: plan role read-only and bound to `pull_request`; apply role write and bound to `environment:production` |
| One pipeline deploys apps, databases, and networking | Split into task-scoped pipelines, each with its own minimal role |
| Repository is public | GitHub-hosted runners only |
| Private repo needs self-hosted runners (GPU, on-prem network, macOS signing hardware) | Ephemeral JIT runners in a runner group restricted to named repos; host hardening routes to `linux-skills` |
| Production deploy | Runs only inside a protected environment with required reviewers who are not the requester, and `prevent self-review` enabled |

## 3. Procedure for a new or changed workflow

1. **Set the floor.** Top of file: `permissions: {}` or `contents: read`. Add
   write scopes on the specific job that needs them. Repository and
   organisation default token permission should also be read-only.
2. **Pin dependencies.** For each `uses:` outside your org, resolve the tag to
   a commit and pin it:

   ```yaml
   - uses: actions/checkout@<40-char-sha> # v7.0.1
   ```

   Resolve with `gh api repos/actions/checkout/git/ref/tags/v7.0.1 -q .object.sha`
   (dereference annotated tags with `git/tags/<sha>`). Keep a Dependabot config
   for the `github-actions` ecosystem so SHA pins are bumped by reviewed PRs.
   Known caveat: Dependabot security alerts cover actions referenced by
   semantic version, so SHA-pinned actions rely on the version-update PRs and
   on an advisory watch, not on alerts. Same-repository local actions may be
   referenced by path; they inherit the repo's review controls.
3. **Close injection sinks.**

   ```yaml
   # Unsafe: title is attacker-controlled and becomes shell code
   - run: echo "Deploying ${{ github.event.pull_request.title }}"
   # Safe: value arrives as data
   - env: { PR_TITLE: "${{ github.event.pull_request.title }}" }
     run: echo "Deploying $PR_TITLE"
   ```

   Treat as untrusted: titles, bodies, branch and tag names, commit messages,
   author names and emails, labels, review comments, and any artifact produced
   by an untrusted run.
4. **Choose triggers deliberately.** `pull_request` for untrusted code;
   `push` / `workflow_dispatch` / `release` for trusted paths. If
   `pull_request_target` or `workflow_run` is unavoidable, the job must not
   build, install, or run anything from the fork. `actions/checkout` v7 blocks
   fork checkouts in these triggers by default, and the protection was
   backported to floating major tags from 2026-07-20; workflows pinned to an
   older SHA do not get it, which is one more reason to keep pins current.
5. **Federate credentials.** OIDC trust bound to exact `sub` claims
   (`repo:org/repo:environment:production`), audience checked, session short.
   Detail in `oidc-federation.md`.
6. **Scope secrets.** Production secrets live only in the production
   environment. Nothing that a fork PR can reach holds a secret.
7. **Serialise and gate deploys.** `concurrency` group per environment with
   `cancel-in-progress: false`; required reviewers; deployment-branch policy
   restricted to `main` or release tags.
8. **Protect the pipeline definition.** `CODEOWNERS` entry for
   `.github/workflows/` and `.github/actions/` owned by a platform group; a
   ruleset requiring that review; the deploy workflow file path restricted
   from direct pushes.
9. **Lint.** `actionlint` for syntax and expression errors and a workflow
   security linter such as `zizmor` for injection, excessive permissions,
   unpinned uses, and dangerous triggers. Both run as required checks on
   workflow changes.
10. **Record evidence.** Keep the lint output, the permissions table, and the
    list of pinned SHAs in the pipeline configuration record.

## 4. Secrets in and around pipelines

Classify before choosing storage. Mixing classes in one tool is the common
failure.

| Class | Examples | Store | Pipeline rule |
|---|---|---|---|
| Personal | Engineer passwords, SSH keys, recovery codes | Team password manager | Never in CI |
| Infrastructure | DB passwords, API keys, TLS keys, signing keys | Cloud secret manager, Vault, KMS (envelope encryption for bulk data) | Prefer short-lived dynamic credentials fetched at run time via OIDC |
| Customer | End-user passwords, PII, health or financial records | Application data store with the right primitive (salted slow hash for passwords; field encryption for PII) | CI must never see production customer data |

Rules: the best secret is one you do not store (federation, managed identity);
the second best expires quickly. Never build a secret into an image or
artifact. Masking is a last line: a secret transformed (base64, URL-encoded,
split) is not masked, so do not print derived values.

## 5. Current action majors (verified 2026-09-24)

Examples elsewhere in this engine show current major tags (bulk-updated
2026-09-24) for readability only. When writing real workflows use the current
major, then pin to its full commit SHA.

| Action | Current release | Upgrade notes that matter |
|---|---|---|
| `actions/checkout` | v7.0.1 | v5 moved to the Node 24 runtime (runner >= 2.327.1); v6 persists credentials to a separate file; v7 refuses fork checkouts in `pull_request_target`/`workflow_run` unless explicitly overridden |
| `actions/setup-node` | v7.0.0 | v5 introduced automatic caching when `packageManager` is set; v6 limited auto-cache to npm; disable with `package-manager-cache: false` |
| `actions/setup-python` | v7.0.0 | Node 24 runtime; check self-hosted runner version |
| `actions/cache` | v6.1.0 | v5 Node 24 runtime; v6 ESM packaging, no key-format change |
| `actions/upload-artifact` | v7.0.1 | v6 Node 24; v7 can upload a single file unzipped (`archive: false`) |
| `actions/download-artifact` | v8.0.1 | v5 changed output path for single download by ID; v8 fails on digest mismatch by default and skips unzipping non-zip content |
| `actions/attest` | v4.2.2 | Preferred over `actions/attest-build-provenance`, which is now a wrapper |
| `aws-actions/configure-aws-credentials` | v6.3.0 | Read the release notes before bumping majors |
| `docker/build-push-action` | v7.4.0 | Keep `provenance` and `sbom` enabled for release images |

Runtime note: Node.js 20 reached end of life on 2026-04-30. Build matrices
should target Node 22 (maintenance LTS) and 24 (active LTS); Node 26 enters LTS
on 2026-10-28. Self-hosted runners must be at least 2.327.1 for the Node 24
action runtime.

## 6. Review gate

- [ ] Top-level `permissions` is empty or read-only; every write scope is job-level and justified.
- [ ] Every external `uses:` is a full SHA with a version comment; Dependabot covers `github-actions`.
- [ ] No `${{ github.event.* }}` or other untrusted context inside `run:`.
- [ ] No privileged trigger builds or executes fork content; no `allow-unsafe-pr-checkout` without a signed exception.
- [ ] Cloud access uses OIDC with an exact subject; no static cloud keys in secrets.
- [ ] Plan and apply identities are separate; apply runs only from a protected environment.
- [ ] Self-hosted runners are ephemeral, grouped, and absent from public repos.
- [ ] Workflow paths are code-owned and ruleset-protected.
- [ ] `actionlint` and a workflow security linter pass as required checks.
- [ ] Production deploy has a concurrency group, required reviewers, and a deployment record.

## 7. What senior work looks like

Generic output: a workflow with `@v4` tags, no `permissions` block, secrets
available to every job, a `pull_request_target` "to make comments work", and a
one-line note saying "follow security best practices".

Senior output: a permissions table per job, SHA pins with version comments, an
explicit trigger rationale, a threat-to-control mapping for the repository's
real exposure (public or private, forks or not), separate plan and apply
identities, a lint report, and a named owner for exceptions.

## 8. Worked example (original)

A Kampala mobile-money reconciliation service is open-sourced so partner banks
can audit it. Risk: forks now exist, and the old workflow used
`pull_request_target` to post test coverage comments while running
`npm test` on the PR head with an AWS key in scope. Fix: tests move to
`pull_request` with `contents: read` and no secrets; a second workflow on
`workflow_run` downloads only the coverage JSON, validates its schema, and
posts the comment with `pull-requests: write`; the AWS key is deleted and the
staging deploy assumes a role bound to `repo:org/recon:environment:staging`;
all actions are SHA-pinned; `.github/workflows/` becomes owned by the platform
group. Acceptance: a test fork PR containing `curl` in a test file produces no
outbound call from a job holding any credential, and `zizmor` reports zero
high findings.

## 9. Failure modes

- Pinning to a SHA but never updating it: the pin freezes known vulnerabilities. Pair pins with scheduled update PRs.
- Pinning the action but not its transitive `uses:` (composite actions calling other actions by tag). Review the action's own `action.yml`.
- Declaring `permissions` at workflow level with write scopes "for convenience", so every job inherits them.
- Caches shared across trust levels: a PR-branch cache restored on `main` can poison a release build. Scope cache keys by branch for release jobs.
- Treating the redactor as protection and logging environment dumps.

## Evidence and currentness

Accessed 2026-09-24. Primary sources: GitHub Docs "Secure use reference"
(docs.github.com/en/actions/reference/security/secure-use); GitHub Changelog
2025-08-15 (policy for blocking and SHA pinning actions), 2026-06-18 (safer
`pull_request_target` defaults for checkout), 2025-10-28 (immutable releases
GA); release pages of each action listed in section 5, queried through the
GitHub Releases API; Node.js release schedule (github.com/nodejs/Release,
schedule.json). Freshness class: volatile; re-verify action majors each Kaizen
cycle. `NOT_ASSESSED`: exact Dependabot alert coverage for SHA-pinned actions
beyond the documented caveat; zizmor rule names (tool evolves quickly; confirm
against its current docs before citing a rule ID).

Sources: Brikman (2025) *Fundamentals of DevOps and Software Delivery*;
Laster (2023) *Learning GitHub Actions* (early release); GitHub Docs as above.
