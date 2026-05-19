#!/usr/bin/env python3
"""
One-time migration: reorganize skills/<slug>/ into skills/<category>/<slug>/.

Steps:
  1. git mv each top-level skill dir into its category bucket.
  2. Rewrite path references in docs/skill-routing-index.md,
     docs/skill-aliases.yml, AGENTS.md, README.md.

Idempotent: skips dirs already inside a category bucket.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "skills"

CATEGORIES = {
    "ios": [
        "ios-ai-ml", "ios-app-security", "ios-architecture", "ios-architecture-advanced",
        "ios-at-scale", "ios-biometric-login", "ios-bluetooth-printing", "ios-data-persistence",
        "ios-debugging-mastery", "ios-development", "ios-monetization", "ios-networking-advanced",
        "ios-pdf-export", "ios-platform-capabilities", "ios-production-patterns", "ios-project-setup",
        "ios-push-notifications", "ios-quality-and-release", "ios-rbac", "ios-security-and-rbac",
        "ios-stability-solutions", "ios-swiftdata", "ios-swift-design-patterns", "ios-swift-recipes",
        "ios-tdd", "ios-uikit-advanced", "ios-ui-ux-design",
        "swiftui-design", "swiftui-pro-patterns", "swift-concurrency-macos",
        "xcode-cloud-testflight", "xcode-instruments-performance", "xcode-project-engineering",
        "macos-appkit-interop", "macos-app-sandbox-security", "macos-git-libgit2",
        "macos-system-integrations",
    ],
    "android": [
        "android-ai-ml", "android-biometric-login", "android-data-persistence",
        "android-development", "android-pdf-export", "android-room", "android-tdd",
        "android-ui-ux-design", "jetpack-compose-ui",
    ],
    "mobile-cross": [
        "kmp-compose-multiplatform", "kmp-development", "kmp-tdd",
        "mobile-custom-icons", "mobile-platform-operations", "mobile-rbac",
        "mobile-reports", "mobile-report-tables", "mobile-saas-planning",
        "pwa-offline-first", "app-store-review", "google-play-store-review",
    ],
    "backend-databases": [
        "postgresql-administration", "postgresql-advanced-sql", "postgresql-ai-platform",
        "postgresql-engineering", "postgresql-fundamentals", "postgresql-operations",
        "postgresql-patterns", "postgresql-performance", "postgresql-server-programming",
        "mysql-administration", "mysql-advanced-sql", "mysql-best-practices",
        "mysql-data-modeling", "mysql-engineering", "mysql-operations", "mysql-query-performance",
        "database-design-engineering", "database-internals", "database-reliability",
        "vector-databases",
    ],
    "saas": [
        "saas-accounting-system", "saas-admin-backoffice-tooling", "saas-architecture-strategy",
        "saas-business-metrics", "saas-control-plane-engineering", "saas-deployment-models",
        "saas-entitlements-and-plan-gating", "saas-erp-system-design",
        "saas-lifecycle-email-orchestration", "saas-rate-limiting-and-quotas",
        "saas-sales-organization", "saas-seeder", "saas-sso-scim-enterprise-auth",
        "saas-subscription-mastery", "saas-tenant-data-portability-and-erasure",
        "saas-tenant-onboarding-automation",
        "multi-tenant-saas-architecture", "modular-saas-architecture",
        "subscription-billing", "stripe-payments",
    ],
    "ai": [
        "ai-agent-commercial-operations", "ai-agent-compliance-controls",
        "ai-agent-governance-and-limits", "ai-agent-multi-agent-coordination",
        "ai-agent-observability-evaluation", "ai-agent-runtime-architecture",
        "ai-agent-safety-and-red-team", "ai-agent-sla-and-customer-commitments",
        "ai-agent-tooling-and-hitl", "ai-agent-ux",
        "ai-analytics", "ai-app-architecture", "ai-cost-and-metering",
        "ai-economic-value-engine", "ai-entitlements-and-feature-gating",
        "ai-evaluation", "ai-feature-rollout-and-experimentation", "ai-feature-spec",
        "ai-incident-response", "ai-llm-integration", "ai-model-gateway",
        "ai-observability-and-debugging", "ai-opportunity-canvas", "ai-output-design",
        "ai-prompt-engineering", "ai-rag-patterns", "ai-security", "ai-web-apps",
        "openai-agents-sdk", "rag-implementation", "ux-for-ai",
        "ai-agent-approval-audit-completeness", "ai-agent-drill-evidence-and-cadence",
        "ai-agent-memory-erasure-proof", "ai-agent-revenue-recognition",
    ],
    "finance-accounting": [
        "_chwezi-finance-engine-skeletons", "accounting-engine",
        "accounting-finance-controller", "finance", "fixed-assets-and-depreciation",
        "multicurrency-and-fx", "inventory-costing", "inventory-management",
        "payroll-postings-uganda", "chart-of-accounts-templates", "demand-forecasting",
    ],
    "frontend-ux": [
        "react-development", "nextjs-app-router", "tailwind-css", "design-audit",
        "motion-design", "healthcare-ui-design", "pos-restaurant-ui-standard",
        "pos-sales-ui-design", "form-ux-design", "interaction-design-patterns",
        "enterprise-ux-process", "webapp-gui-design", "practical-ui-design",
        "frontend-performance", "premium-ui-ux-design", "image-compression",
        "data-visualization", "ux-content-strategy", "ux-principles-101",
    ],
    "devops-cloud": [
        "cicd-devsecops", "cicd-jenkins-debian", "cicd-pipeline-design", "cicd-pipelines",
        "kubernetes-fundamentals", "kubernetes-platform", "kubernetes-production",
        "kubernetes-saas-delivery", "docker-development", "infrastructure-as-code",
        "cloud-architecture", "deployment-release-engineering",
        "observability-monitoring", "observability-platform", "reliability-engineering",
    ],
    "architecture": [
        "microservices-ai-integration", "microservices-architecture",
        "microservices-architecture-models", "microservices-communication",
        "microservices-fundamentals", "microservices-resilience",
        "event-driven-architecture", "distributed-systems-patterns",
        "system-architecture-design", "realtime-systems",
        "api-design-first", "api-error-handling", "api-pagination",
        "api-testing-verification", "graphql-patterns",
        "orchestration-best-practices", "validation-contract",
    ],
    "languages": [
        "typescript-design-patterns", "typescript-effective", "typescript-full-stack",
        "typescript-mastery", "javascript-advanced", "javascript-modern",
        "javascript-patterns", "javascript-php-integration",
        "python-data-analytics", "python-data-pipelines", "python-ml-predictive",
        "python-modern-standards", "python-saas-integration",
        "php-modern-standards", "php-security", "php-vs-nextjs",
        "nodejs-development", "language-standards",
    ],
    "security": [
        "network-security", "linux-security-hardening", "code-safety-scanner",
        "vibe-security-skill", "dpia-generator", "uganda-dppa-compliance",
        "dual-auth-rbac", "web-app-security-audit", "graphql-security",
    ],
    "sdlc-meta": [
        "sdlc-design", "sdlc-documentation", "sdlc-maintenance", "sdlc-planning",
        "sdlc-post-deployment", "sdlc-testing", "sdlc-user-deploy",
        "skill-composition-standards", "skill-safety-audit", "skill-writing",
        "spec-architect", "doc-architect", "plan-implementation",
        "implementation-status-auditor", "update-claude-documentation",
        "custom-sub-agents", "project-requirements", "capability-matrix",
        "advanced-testing-strategy", "e2e-testing", "git-collaboration-workflow",
        "markdown-lint-cleanup", "ai-assisted-development", "world-class-engineering",
        "engineering-management-system", "engineering-strategy",
        "continuous-improvement-system",
    ],
    "gis": [
        "gis-enterprise-domain", "gis-mapping", "gis-maps-integration",
        "gis-platform-engineering", "gis-postgis-backend",
    ],
    "product-business": [
        "product-discovery", "product-led-growth", "product-strategy-vision",
        "software-business-models", "software-pricing-strategy",
        "premium-product-positioning", "premium-software-product-execution",
        "customer-service-excellence", "it-proposal-writing", "content-writing",
        "growth-telemetry-pipeline", "experiment-engineering",
        "excel-spreadsheets", "professional-word-output",
    ],
}


def build_slug_to_category() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for category, slugs in CATEGORIES.items():
        for slug in slugs:
            if slug in mapping:
                raise SystemExit(f"Duplicate slug in CATEGORIES: {slug}")
            mapping[slug] = category
    return mapping


def current_top_level_slugs() -> list[str]:
    return sorted(
        p.name for p in SKILLS.iterdir()
        if p.is_dir() and p.name not in set(CATEGORIES)
    )


def run_git_mv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "mv", str(src.relative_to(REPO)), str(dst.relative_to(REPO))],
        cwd=REPO, capture_output=True, text=True,
    )
    if result.returncode != 0:
        # Git refuses empty dirs (no tracked files). Fall back to plain rename.
        if "source directory is empty" in result.stderr:
            src.rename(dst)
            return
        sys.stderr.write(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, result.args)


def move_dirs(mapping: dict[str, str]) -> tuple[list[str], list[str]]:
    moved, unmapped = [], []
    for slug in current_top_level_slugs():
        category = mapping.get(slug)
        if category is None:
            unmapped.append(slug)
            continue
        src = SKILLS / slug
        dst = SKILLS / category / slug
        if dst.exists():
            continue
        run_git_mv(src, dst)
        moved.append(f"{slug} -> {category}/")
    return moved, unmapped


def rewrite_paths(mapping: dict[str, str]) -> list[Path]:
    """Replace `skills/<slug>` with `skills/<category>/<slug>` in doc files."""
    targets = [
        REPO / "docs" / "skill-routing-index.md",
        REPO / "docs" / "skill-aliases.yml",
        REPO / "AGENTS.md",
        REPO / "README.md",
    ]
    # Longest-first so e.g. `ios-architecture-advanced` rewrites before `ios-architecture`.
    slugs_sorted = sorted(mapping.keys(), key=len, reverse=True)
    rewritten = []
    for file_path in targets:
        if not file_path.exists():
            continue
        original = file_path.read_text(encoding="utf-8")
        updated = original
        for slug in slugs_sorted:
            category = mapping[slug]
            pattern = re.compile(
                r"(?<![A-Za-z0-9/_-])skills/" + re.escape(slug) + r"(?![A-Za-z0-9_-])"
            )
            updated = pattern.sub(f"skills/{category}/{slug}", updated)
        if updated != original:
            file_path.write_text(updated, encoding="utf-8")
            rewritten.append(file_path.relative_to(REPO))
    return rewritten


def main() -> int:
    mapping = build_slug_to_category()
    print(f"Categories: {len(CATEGORIES)}; slugs in map: {len(mapping)}")

    moved, unmapped = move_dirs(mapping)
    print(f"Moved {len(moved)} dirs.")
    if unmapped:
        print(f"UNMAPPED (left in place): {len(unmapped)}")
        for slug in unmapped:
            print(f"  - {slug}")

    rewritten = rewrite_paths(mapping)
    print(f"Rewrote path refs in {len(rewritten)} file(s):")
    for path in rewritten:
        print(f"  - {path}")

    return 0 if not unmapped else 2


if __name__ == "__main__":
    sys.exit(main())
