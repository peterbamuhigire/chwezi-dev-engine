"""Portfolio contract: every engine's Kaizen work requires a resolved currentness authority."""
from pathlib import Path
import unittest
import os


ROOT = Path(__file__).resolve().parents[1]
WWW = ROOT.parent
MARKER = "Mandatory Digital Research currentness gate for Kaizen"
ENGINES = (
    "chwezi-sdlc-documentation",
    "business-plan-skills",
    "website-skills",
    "social-media-skills",
    "linux-skills",
    "proposal-skills",
    "chwezi-accounting-doctrine",
    "chwezi-design-engine",
    "digital-research-engine",
    "chwezi-dev-engine",
    "windows-admin-engine-skills",
)
KAIZEN_SKILLS = (
    WWW / "chwezi-sdlc-documentation/09-governance-compliance/31-kaizen-engine-and-product-improvement/SKILL.md",
    WWW / "business-plan-skills/skills/meta-strategy/kaizen-improvement-system/SKILL.md",
    WWW / "website-skills/skills/quality-gates/kaizen-engine-and-product-improvement/SKILL.md",
    WWW / "social-media-skills/skills/meta-utility/kaizen-improvement-system/SKILL.md",
    WWW / "linux-skills/meta/kaizen-improvement-system/SKILL.md",
    WWW / "proposal-skills/skills/meta/kaizen-improvement-system/SKILL.md",
    WWW / "chwezi-accounting-doctrine/skills/10-controls-governance-and-fraud/kaizen-engine-and-product-improvement/SKILL.md",
    WWW / "chwezi-design-engine/skills/00-cross-cutting-ops-qa-a11y/design-engine-and-product-improvement/SKILL.md",
    WWW / "chwezi-dev-engine/skills/sdlc-meta/kaizen-improvement-system/SKILL.md",
)


class PortfolioCurrentnessPolicyTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get("SKILL_ENGINE_LIVE_TESTS") == "1", "NOT ASSESSED: installed-portfolio check; set SKILL_ENGINE_LIVE_TESTS=1")
    def test_every_engine_router_declares_mandatory_kaizen_gate(self):
        for engine in ENGINES:
            router = WWW / engine / "AGENTS.md"
            self.assertTrue(router.is_file(), router)
            text = router.read_text(encoding="utf-8").lower()
            if engine in {"chwezi-dev-engine", "chwezi-sdlc-documentation"}:
                self.assert_configured_authority(text, router)
            else:
                self.assertIn(MARKER.lower(), text, router)
                self.assertIn("digital-research", text, router)

    @unittest.skipUnless(os.environ.get("SKILL_ENGINE_LIVE_TESTS") == "1", "NOT ASSESSED: installed-portfolio check; set SKILL_ENGINE_LIVE_TESTS=1")
    def test_every_kaizen_owner_points_to_digital_research(self):
        for skill in KAIZEN_SKILLS:
            self.assertTrue(skill.is_file(), skill)
            text = skill.read_text(encoding="utf-8").lower()
            if skill.is_relative_to(ROOT) or skill.is_relative_to(WWW / "chwezi-sdlc-documentation"):
                self.assertIn("configured research route", text, skill)
                self.assertIn("not_assessed", text, skill)
            else:
                self.assertIn("digital-research", text, skill)
            self.assertIn("currentness", text, skill)

    def test_local_router_declares_currentness_gate(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
        self.assert_configured_authority(text, ROOT / "AGENTS.md")
        skill = (ROOT / "skills/sdlc-meta/kaizen-improvement-system/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("configured research route", skill)
        self.assertIn("NOT_ASSESSED", skill)
        prompt = (ROOT / "prompts/full-kaizen-operation.md").read_text(encoding="utf-8")
        self.assertIn("currentness workflow from the host routing table", prompt)

    def assert_configured_authority(self, text, router):
        for requirement in ("configured research route", "explicitly selected", "not_assessed",
                            "access date", "primary sources", "uncertainty"):
            self.assertIn(requirement, text, router)


if __name__ == "__main__":
    unittest.main()
