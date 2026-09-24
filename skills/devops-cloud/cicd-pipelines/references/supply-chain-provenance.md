# Supply-Chain Provenance and Verified Promotion

Load this when a pipeline publishes a release artifact (container image,
package, mobile binary, installer, IaC module), when a client or regulator asks
"how do you know production runs what you reviewed", or when a deploy gate
should refuse unverified artifacts. Container signing mechanics with Cosign and
admission control live in
`../../cicd-devsecops/references/container-runtime-security.md`; hardening of
the workflow that produces the artifact lives in
`github-actions-security-hardening.md`.

## 1. The question provenance answers

Provenance is a signed statement: this artifact digest was produced by this
build platform, from this source commit, by this workflow, with these inputs.
It does not say the artifact is safe. It lets a consumer refuse artifacts that
did not come from the expected place, and lets an investigator trace a bad
artifact back to its commit and run.

## 2. SLSA Build track as a decision (spec v1.2)

| Level | What must be true | Practical meaning on GitHub | Choose when |
|---|---|---|---|
| Build L0 | Nothing | Laptop builds, unsigned | Never for anything shipped to a client |
| Build L1 | Provenance exists and names the output by digest | Any generated provenance, even unsigned | Internal tools; first step for a team with no provenance |
| Build L2 | Build runs on a hosted platform; provenance signed by the platform so tenants cannot forge it | Artifact attestation generated in a GitHub-hosted workflow | Default for client-facing apps and SaaS |
| Build L3 | Signing material unreachable from user build steps; builds isolated and ephemeral; no cross-build cache influence | Attestation generated from a reusable workflow the calling repo cannot alter | Payments, health, government, anything distributed to third parties or regulated |

The SLSA v1.2 specification also defines a Source track; treat source-side
claims (branch protection, two-person review) as separate evidence rather than
folding them into a build level. GitHub documents that its attestations reach
Build L2 alone and Build L3 when produced through a reusable workflow; those
statements reference SLSA v1.0 levels, whose Build track definitions carry into
v1.2.

## 3. Procedure: produce, publish, verify, deploy

1. **Build once** in a hosted, ephemeral job. Record the digest as a job
   output; never re-derive it later from a tag.
2. **Attest** in the same job that built the artifact:

   ```yaml
   permissions:
     contents: read
     id-token: write        # mint OIDC token for the Sigstore certificate
     attestations: write    # store the attestation
     artifact-metadata: write
   steps:
     # ... build step that outputs steps.build.outputs.digest
     - uses: actions/attest@<sha> # v4.2.2
       with:
         subject-name: ghcr.io/example/recon-api
         subject-digest: ${{ steps.build.outputs.digest }}
         push-to-registry: true
   ```

   With no SBOM or predicate inputs the action emits SLSA build provenance.
   Run it a second time with `sbom-path:` (SPDX or CycloneDX JSON) to attach an
   SBOM attestation to the same digest.
3. **Move to L3 when required** by putting build and attest steps in a
   reusable workflow owned by the platform repo and pinning the caller to that
   workflow's SHA. Verification then checks the signer workflow, not only the
   repository.
4. **Verify before deploy** in the promotion job, on the digest being
   deployed:

   ```bash
   gh attestation verify oci://ghcr.io/example/recon-api@"$DIGEST" \
     --repo example/recon-api \
     --signer-workflow example/platform/.github/workflows/build.yml
   ```

   Fail the deploy on any verification error. Log the verified signer, source
   commit, and run URL into the deployment record.
5. **Protect published releases.** Enable immutable releases on repositories
   that publish downloadable assets so assets cannot be replaced and tags
   cannot be moved after publication.
6. **Retain evidence**: attestation bundle, SBOM, verification output, and the
   deployment record, for the retention period the client contract or
   regulator requires.

## 4. Decision rules

| Condition | Action |
|---|---|
| Private repository on Free, Pro, or Team plan | GitHub artifact attestations are unavailable; use Cosign keyless signing plus `cosign attest` from the workflow's OIDC identity, and record the gap |
| GitHub Enterprise Server | Attestations are not supported there; use Cosign with a self-hosted or public Sigstore instance per policy |
| Consumer is Kubernetes | Enforce verification at admission (policy controller or Kyverno image verification), not only in the pipeline |
| Consumer is a VPS or PaaS without admission control | Verify in the deploy job and refuse to run the deploy script without a passing verification step |
| Artifact built outside CI (hotfix from a laptop) | Treat as L0; it cannot be promoted to production without a rebuild in CI |
| Third-party dependency or base image | Verify its published provenance or signature where offered; pin by digest; record where none exists |

## 5. Review gate

- [ ] Every production artifact is referenced by digest end to end.
- [ ] Provenance is produced by the hosted platform in the job that built the artifact.
- [ ] The deploy job verifies provenance against expected repository and signer workflow and fails closed.
- [ ] SBOM attestation exists for release artifacts and matches the deployed digest.
- [ ] Target SLSA Build level is stated in the release plan with the reason.
- [ ] Release assets are immutable after publication.
- [ ] Gaps (plan limits, GHES, external dependencies) are listed, not hidden.

## 6. Senior versus generic

Generic output says "we sign our images and follow SLSA". Senior output states
the target level per artifact, shows the attest step and the verify command
with the exact signer identity, proves a tampered or unattested digest is
rejected in a rehearsal, and lists every unverifiable dependency with an owner.

Worked example (original): a Ugandan district health-records vendor ships an
Android app and a Laravel API to a ministry. The API image targets Build L3
through a platform-owned reusable workflow; the Android AAB targets L2 with an
attestation on the AAB digest; the deploy job for the ministry's on-premises
cluster runs `gh attestation verify` before `helm upgrade`, and a rehearsal
with an image pushed from a developer laptop is rejected. The ministry's
acceptance letter cites the verification log rather than a vendor assurance.

## 7. Failure modes

- Attesting a tag instead of a digest, so the claim floats.
- Generating provenance in a later job that re-pulls the artifact, which lets a swapped artifact be attested.
- Verifying only the repository name: any workflow in that repo, including a malicious one, could have signed. Verify the signer workflow for L3 claims.
- Treating provenance as a vulnerability scan. Keep scanning gates separate.

## Evidence and currentness

Accessed 2026-09-24. Primary sources: SLSA specification v1.2, Build track
requirements (slsa.dev/spec/v1.2/build-requirements); GitHub Docs "Artifact
attestations" concept page; `actions/attest` and
`actions/attest-build-provenance` READMEs (plan availability, GHES
limitation, required permissions, v4 wrapper note); GitHub Changelog
2025-10-28 (immutable releases GA). Freshness class: volatile for GitHub plan
availability and action inputs; stable for SLSA level semantics.
Also verified 2026-09-24: `push-to-registry` and `sbom-path` inputs in the
current `actions/attest` `action.yml` (runtime node24), and the `--repo`,
`--owner`, and `--signer-workflow` flags in `gh attestation verify --help`.
`NOT_ASSESSED`: flag availability on older `gh` CLI versions installed on
self-hosted runners; confirm on the runner image.

Sources: Brikman (2025) *Fundamentals of DevOps and Software Delivery*; SLSA
v1.2 specification; GitHub Docs as above.
