# Detection Rules

This reference defines the deterministic rules the meta-initialization skill uses
to detect a project's characteristics from its files, configuration, and version
control history. These rules feed the methodology recommendation in
`methodology-decision-tree.md`; this file is the evidence-gathering layer, the
decision tree is the judgement layer.

This file is self-contained. It does not depend on any external document and can
be loaded on its own when you need to know exactly what to scan for and how to
score the result.

---

## How to Use

1. Run the scan rules in the order below and record raw evidence, not
   conclusions. Write down which files were found, not what they imply.
2. Convert evidence into the characteristic fields used by `project_profile.md`.
3. Pass the characteristics to the methodology decision tree.
4. Never infer a characteristic you did not observe. An absent signal is
   "unknown", not "no".

---

## Rule Set 1: Project Type and Stack

Detect the primary language and framework from manifest files at the project
root. Match the first manifest that exists; record all that match for polyglot
repositories.

| Signal file | Project type | Framework hint |
|-------------|--------------|----------------|
| `package.json` | Node.js / JavaScript | Read `dependencies` for react, next, express, nest |
| `composer.json` | PHP | Read `require` for laravel, symfony, slim |
| `requirements.txt` or `pyproject.toml` | Python | Look for django, flask, fastapi |
| `pom.xml` or `build.gradle` | Java / Kotlin | Spring, Micronaut, Quarkus |
| `*.sln` or `*.csproj` | C# / .NET | ASP.NET Core markers in csproj |
| `Cargo.toml` | Rust | actix, axum, rocket in dependencies |
| `go.mod` | Go | gin, echo, chi in require block |

Detection is evidence, not certainty. If two manifests exist (for example
`package.json` plus `composer.json`), record both and treat the repository as
polyglot rather than picking one silently.

### Database detection

| Signal | Inferred database |
|--------|-------------------|
| `migrations/` with MySQL DDL, `mysql:` in compose | MySQL or MariaDB |
| `migrations/` with `serial`, `jsonb`, `postgres:` in compose | PostgreSQL |
| `*.sqlite`, `database.sqlite` | SQLite |
| `mongoose`, `mongodb` in dependencies | MongoDB |

### Deployment detection

| Signal | Inferred deployment |
|--------|---------------------|
| `Dockerfile` | Containerised build |
| `docker-compose.yml` | Multi-service local or staging stack |
| `*.tf` | Terraform-managed infrastructure |
| `k8s/`, `*.yaml` with `kind: Deployment` | Kubernetes |
| `.github/workflows/`, `.gitlab-ci.yml` | CI/CD configured |

---

## Rule Set 2: Regulatory and Compliance Indicators

Scan `README.md`, `ARCHITECTURE.md`, and any `docs/**/*.md` for the keywords
below. Matching is case-insensitive but must be whole-word to avoid false
positives (for example, do not match "fda" inside "update").

| Keyword group | Inferred constraint | Confidence weight |
|---------------|---------------------|-------------------|
| FDA, FAA, DOD, medical device, aerospace | Regulated domain | High |
| HIPAA, GDPR, SOC2, PCI-DSS, ISO 27001 | Compliance regime required | High |
| safety-critical, life-safety, fail-safe | Formal V&V needed | High |
| audit, traceability, sign-off | Formal governance expected | Medium |

Record the exact phrase and the file it came from. A single high-weight match is
enough to flag the project as regulated; record it as evidence and let the
decision tree weigh it.

### Failure mode table

| Wrong choice | What goes wrong | Correct rule |
|--------------|-----------------|--------------|
| Treat any "secure" mention as compliance | Over-formalises a hobby project, wastes weeks on traceability matrices | Only match the explicit regime keywords listed above |
| Match keywords inside unrelated words | "fda" inside "update" flags a regulated domain falsely | Use whole-word, case-insensitive matching |
| Ignore docs outside README | Misses HIPAA noted only in `docs/compliance.md` | Scan all `docs/**/*.md`, not just the root README |
| Assume no keyword means no regulation | A regulated project with sparse docs is mislabelled Agile | Record as "unknown", prompt the user to confirm |

---

## Rule Set 3: Project Maturity

Maturity decides how much upfront documentation is worthwhile.

| Observation | Maturity classification |
|-------------|-------------------------|
| No source files, only manifests and README | Greenfield |
| Substantial source tree, git history present | Brownfield |
| Version below 1.0.0 in manifest, "MVP" in README | Startup / MVP |
| Mature version, formal process docs, CODEOWNERS | Enterprise |

Greenfield projects benefit from comprehensive upfront planning because there is
no implemented system to reverse-engineer. Brownfield projects need
documentation that captures the system as it already exists, so prioritise
discovery over speculative design.

---

## Rule Set 4: Team Structure and Development Pace

Infer from git history when `.git/` is present. If git history is absent, mark
these fields "unknown" and prompt the user; do not guess.

| Git signal | Inferred team / pace |
|------------|----------------------|
| Many distinct author emails | Team environment |
| Single author email | Solo developer |
| Pull-request merge commits present | Review-driven team workflow |
| More than ~10 commits per week (rolling average) | Rapid, iterative pace |
| Infrequent, large commits | Milestone or waterfall pace |
| Branch names `feature/*`, `sprint/*` | Agile branch strategy |
| Long-lived `release/*` branches with tags | Release-train or waterfall cadence |

### Failure mode table

| Wrong choice | What goes wrong | Correct rule |
|--------------|-----------------|--------------|
| Count commits without a time window | A repo imported in one bulk commit looks "rapid" | Use a rolling weekly average over real history |
| Treat bot commits as contributors | CI bots inflate the author count, falsely signalling a large team | Exclude known bot and CI author emails |
| Infer pace with no git history | Pure speculation drives the methodology choice | Mark "unknown" and ask the user |

---

## Rule Set 5: Existing Documentation and Context

Before generating anything, detect prior runs and existing artefacts so the
skill never silently overwrites work.

| Signal | Meaning | Required action |
|--------|---------|-----------------|
| `projects/<ProjectName>/_context/methodology.md` | Skill ran before | Confirm or update, do not blindly regenerate |
| `projects/<ProjectName>/_context/` exists, some files | Partial prior run | List present and missing files, fill gaps only |
| `README.md` mentions a methodology | User has a stated preference | Surface it; treat as a strong prior |
| `ARCHITECTURE.md` present | Design approach already chosen | Read it before recommending design depth |

---

## Scan Report Format

Emit one consolidated scan report before recommending a methodology. Keep it
factual and evidence-first.

```
[Scan Report]
- Project Type: PHP (composer.json detected)
- Framework: Laravel (composer.json require: laravel/framework)
- Database: MySQL (docker-compose.yml: mysql:8, migrations/ present)
- Deployment: Docker (docker-compose.yml), CI/CD (.github/workflows/ci.yml)
- Version Control: Git (3 authors, ~12 commits/week)
- Regulatory: HIPAA mentioned in docs/compliance.md
- Maturity: Brownfield (existing src/ tree, 400+ commits)
- Existing Context: methodology.md missing, vision.md present
```

---

## Confidence Scoring

Translate evidence into a confidence percentage for the decision tree. Score per
methodology, take the highest, and always show the runner-up so the user can see
the trade-off.

| Evidence strength | Contribution to score |
|-------------------|-----------------------|
| High-weight match (regulatory regime, safety-critical) | +30 each, capped at 60 |
| Medium-weight match (audit, sign-off language) | +15 each |
| Pace and branch-strategy alignment | +20 |
| Maturity alignment | +10 |
| Conflicting signals | -15 per conflict |

Never report a confidence above 95 percent. Detection works on indirect signals,
so leave room for the user to correct the recommendation. When the top two
methodologies are within 10 points of each other, recommend Hybrid and explain
the split.

---

## Related References

- `methodology-decision-tree.md` consumes these characteristics to choose
  Waterfall, Agile, or Hybrid.
- The `templates/` directory holds the output templates populated from this scan.
