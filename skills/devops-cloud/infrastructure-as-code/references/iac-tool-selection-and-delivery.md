# IaC Tool Selection and Delivery Pipeline

Load this when choosing IaC tools for a new estate, deciding between Terraform
and OpenTofu, or designing how infrastructure changes move from pull request
to production. Module layout and state commands stay in
`terraform-modules-state.md`; Ansible roles in `ansible-debian.md`.

## 1. Match tool category to job

Most estates need two or three categories together. Using one category for
every job is the usual design error.

| Category | Good at | Wrong tool for | Typical choice |
|---|---|---|---|
| Ad hoc scripts (Bash, PowerShell, Python) | One-off tasks, glue, bootstrap | Managing long-lived infrastructure; they are rarely idempotent | Keep short, commit them, never the system of record |
| Configuration management | Converging packages, files, services on existing servers | Creating the servers, networks, and managed services themselves | Ansible for Debian/Ubuntu fleets |
| Server or image templating | Baking immutable machine or container images | Runtime configuration that changes per environment | Dockerfile, Packer |
| Provisioning | Declaring cloud and platform resources with a plan-apply cycle | Configuring software inside a running host | OpenTofu or Terraform, Pulumi, CloudFormation |
| Orchestration and GitOps | Continuously reconciling app workloads to declared state | Creating the cluster's own network and IAM | Kubernetes with Argo CD or Flux |

Decision rule: provisioning tool creates the box and its neighbours; image or
config tool decides what runs inside; orchestrator keeps it running. For a
single Debian VPS client, a provisioning module plus an Ansible role is enough;
Kubernetes is not a default (see `../../kubernetes-fundamentals/references/when-k8s-is-right.md`).

## 2. Terraform or OpenTofu

Licence facts (verified 2026-09-24): Terraform 1.6.0 and later is under the
Business Source License 1.1 with IBM as licensor; its additional-use grant
excludes offering Terraform to third parties on a hosted or embedded basis in
competition with the licensor's paid products. Terraform 1.5.7 was the last
MPL 2.0 release. OpenTofu is the MPL 2.0 fork under the Linux Foundation and a
CNCF Sandbox project.

| Condition | Choose | Reason |
|---|---|---|
| Agency building an internal platform, hosted IaC service, or self-service provisioning product for clients | OpenTofu | BSL use restrictions could apply to hosted or embedded offerings; take legal review if Terraform is still preferred |
| Client already standardised on HCP Terraform / Terraform Enterprise with support contract | Terraform | Tooling, policy, and support investment outweighs licence concern for internal use |
| Greenfield client estate, no vendor preference | OpenTofu by default; record the decision in an ADR | OSI licence, multi-vendor governance, provider-compatible |
| State must be encrypted client-side before it reaches the backend | OpenTofu state and plan encryption (key providers include AWS KMS, GCP KMS, OpenBao, PBKDF2) | Terraform relies on backend encryption only |
| Mixed estate | Pick one per state boundary; never run both CLIs against the same state | State format and features diverge over time |

Current releases at time of writing: OpenTofu 1.12.6, Terraform 1.16.4, AWS
provider 6.66.0. Pin `required_version` and provider constraints to the major
you have tested, and commit the dependency lock file.

## 3. Delivery pipeline for infrastructure

Infrastructure deploys are binary: a resource is created, changed, or
destroyed. There is no canary for dropping a database. Safety comes from
promotion, plan review, and privilege separation.

1. **PR opened.** Run format, validate, linters, policy checks (OPA/Conftest or
   equivalent), `tofu test` / `terraform test` for modules, and `plan` for each
   affected root module. The plan job assumes a **read-only** role bound to
   pull requests.
2. **Plan published to the PR** as a comment with resource counts
   (add/change/destroy) and any replace or destroy highlighted at the top.
3. **Review.** A second engineer approves; destroys or replacements of stateful
   resources require the recovery plan named in the SKILL decision rules.
4. **Merge.** Apply runs from the pipeline only, using a **write** role bound
   to a protected environment with required reviewers. Apply the saved plan
   from step 1 or re-plan and fail if it differs from the reviewed plan.
5. **Promote.** Same module version to dev, then staging, then production;
   environments differ by variables, never by forked code.
6. **Detect drift.** Scheduled read-only plan per root module; a non-empty plan
   opens a ticket with the owner. Console changes are incidents.

Why the role split matters: if plan and apply share credentials, anyone who
can open a PR can run arbitrary provider code with write access before review.

## 4. State isolation rules

- One state per environment per blast-radius unit (network, data, app), not one state for everything.
- Separate cloud accounts or projects per environment where the client can afford it; this is the strongest isolation.
- Backend with encryption at rest, versioning, locking, and access restricted to the pipeline roles plus break-glass.
- Secrets never written to state where avoidable; when a provider forces it, treat the state as a secret store.

## 5. Review gate

- [ ] Tool category matches each job; no provisioning done by ad hoc scripts.
- [ ] Terraform/OpenTofu choice recorded in an ADR with the licence rationale.
- [ ] Versions and providers pinned; lock file committed.
- [ ] Plan role read-only; apply role write and environment-protected.
- [ ] Destroy/replace of stateful resources flagged and paired with a recovery plan.
- [ ] Same module version promoted across environments.
- [ ] Drift detection scheduled with an owner.

## 6. Senior versus generic

Generic: "Use Terraform to provision infrastructure and store state in S3."
Senior: states which tool owns which layer, records the licence decision,
shows the plan/apply identity split, defines state boundaries by blast radius,
and names the drift owner. Worked example (original): an agency hosting ERPs
for Ugandan SACCOs offers "one-click new branch environment" to clients. That
is a hosted provisioning offering, so the ADR selects OpenTofu, encrypts state
with a KMS key per client, and gives each client its own state and account.

## Evidence and currentness

Accessed 2026-09-24. Primary sources: `hashicorp/terraform` LICENSE file
(BUSL 1.1 parameters) and releases; `opentofu/opentofu` licence (MPL-2.0) and
releases; `hashicorp/terraform-provider-aws` releases, all via the GitHub API;
OpenTofu docs "State and Plan Encryption" (opentofu.org/docs/language/state/encryption).
Secondary: CNCF Sandbox acceptance date (2025-04-23) reported by third-party
sources, `NOT_ASSESSED` against cncf.io. Legal interpretation of the BSL grant
for a specific client offering is `NOT_ASSESSED`; route to counsel. Freshness
class: volatile for version numbers, stable for category guidance.

Sources: Brikman (2025) *Fundamentals of DevOps and Software Delivery*;
OpenTofu and Terraform official documentation.
