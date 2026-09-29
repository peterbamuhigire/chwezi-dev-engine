# Architecture as Code

Load when an architecture diagram or description must stay true to the code: a handover pack, an
as-built document, a design review, or any diagram that cites files. The idea is to keep the model
as text in the repository, give every element a stable ID, pin its evidence to a commit, and check
that evidence with a script instead of trusting that "the diagram agrees with the prose".

## 1. C4 as shared vocabulary

Use the C4 model's levels and abstractions as the vocabulary, whatever notation or tool draws the
picture. Source record (primary material, Simon Brown, accessed 29 Sep 2026; site licensed CC BY 4.0):

| Claim | Source |
|---|---|
| C4 was created by Simon Brown and has four core diagram levels: System Context, Container, Component and Code | https://c4model.com/ (accessed 29 Sep 2026) |
| C4 is notation independent and tooling independent | https://c4model.com/ (accessed 29 Sep 2026) |
| Supporting diagrams are system landscape, dynamic and deployment diagrams | https://c4model.com/ (accessed 29 Sep 2026) |
| A container is an application or a data store that must be running for the system to work; it is a runtime construct, not a Docker container, and not a JAR or DLL | https://c4model.com/abstractions/container (accessed 29 Sep 2026) |
| A component is a grouping of related functionality behind a well-defined interface; components are not separately deployable, the container is | https://c4model.com/abstractions/component (accessed 29 Sep 2026) |

Levels in practice for a PHP/MySQL SaaS:

- **System Context:** the ERP, its users (cashier, accountant, tenant admin) and the external
  systems it talks to (mobile-money provider, tax authority API, email service).
- **Container:** the web application, the API, the queue worker, the MySQL database, the file store.
- **Component:** inside the web application, the invoicing, posting, stock and authorisation
  components, each behind an interface.
- **Code:** only when a reader needs it; usually generated from the source or skipped.

Re-check these claims against c4model.com before quoting them in a client deliverable; the source
record above is dated for that reason.

## 2. Stable element IDs

Give every element an ID that does not change when its label, colour or position changes:

- lower-case, dotted by level: `erp`, `erp.web`, `erp.web.posting`, `erp.db`;
- relationships named by their ends: `erp.web.posting->erp.db`;
- never reuse a retired ID for a different element.

Prose, ADRs, tests and review comments cite the ID, so a renamed box does not break every reference
to it.

## 3. Evidence pinned to a commit

Each element or relationship that claims to exist in code carries evidence:

- `meta.repository.revision`: the full 40-character commit SHA the evidence was read at;
- `sources[]`: objects with a repository-relative `path` (forward slashes, no `..`, nothing inside
  `.git`), and a `line` and `end_line` range.

```json
{
  "meta": { "repository": { "revision": "3f9c2a7e5b1d4c8f9a0b6e2d7c1f4a8b9e0d3c5a" } },
  "elements": [
    { "id": "erp.web.posting", "label": "Posting service" }
  ],
  "sources": [
    { "element": "erp.web.posting", "path": "app/Services/InvoicePoster.php", "line": 14, "end_line": 38 }
  ]
}
```

Check it with the script in this skill:

```powershell
python -X utf8 skills/architecture/system-architecture-design/scripts/verify_diagram_evidence.py --repo-root <project> <model.json>
```

It fails with `evidence/revision-not-full` for a short SHA, `evidence/path-escape` for absolute,
backslash, `.`/`..` or `.git` paths, `evidence/missing-at-revision` when the file is not in that
commit, and `evidence/line-out-of-range` when the lines do not exist.

Keep the limit in mind: a verified citation proves the lines existed at that commit. It does not
prove they support the claim. A reviewer still reads the cited lines.

## 4. Drift between diagram and code as a fitness function

Treat "the architecture model still matches the code" as one of the fitness functions in
[practical-architecture-knowledge.md](practical-architecture-knowledge.md) (section "Fitness
Functions"):

- **Check:** run the evidence verifier against the current commit after re-pinning, or list changed
  files in the model's scope with `git diff --name-only <revision> HEAD -- <paths cited in sources>`.
- **Threshold:** zero failed citations; any cited file changed since the pinned revision is reviewed
  before release.
- **Owner and cadence:** the module owner, at each release or architecture change (the ARCHITECTURE
  and FULL classes in `doc-architect/references/doc-maintenance-after-change.md`).

When the check fails, update the model or the code; do not delete the citation to make it pass.

## 5. Requirements-traceable variant

For systems specified in the SRS engine, the requirements-traceable form of this model is the SRS
diagram intermediate representation planned in Kaizen phase M10-07. It adds requirement IDs to
elements and reuses the same evidence check. Use it when a diagram must trace to requirements; use
this reference for engineering-only diagrams.

## Checklist

- [ ] Levels and abstractions named in C4 terms; notation chosen separately.
- [ ] Every element and relationship has a stable ID.
- [ ] Evidence carries a full SHA and repository-relative paths with line ranges.
- [ ] `verify_diagram_evidence.py` passes; failures are fixed, not deleted.
- [ ] Drift check scheduled as a fitness function with an owner.

(Evidence pinning and the "a citation is not a proof" caution adapted from tt-a1i/archify, MIT,
https://github.com/tt-a1i/archify, commit `0e4949f910a8e390bd3b4933883a4dcabad571be`. Paraphrased;
no text copied.)
