from pathlib import Path
import os
import sys
import yaml

EXPECTED_ENGINE = "skills-web-dev"
ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / ".skills-engine" / "engine-manifest.yaml"

def main() -> int:
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert data["engine_id"] == EXPECTED_ENGINE
    router = ROOT / data["router"]["path"]
    assert router.is_file(), f"router missing: {router}"
    assert list(ROOT.glob(data["skills"]["discovery_glob"])), "no SKILL.md found"
    for validator in data["validation"]:
        assert validator["working_directory"] == "."
        assert validator["platforms"]
        assert validator["command"]
    approval = set(data["agent_integration"]["approval_required_for"])
    safe = set(data["agent_integration"]["mcp_safe_tools"])
    assert not safe & approval
    assert not any(token in safe for token in ("shell", "arbitrary_command", "write_files", "pull", "publish"))
    catalog = ROOT.parent / "chwezi-engine-agents" / "catalog" / "engines.yaml"
    if catalog.is_file():
        entries = yaml.safe_load(catalog.read_text(encoding="utf-8"))["engines"]
        assert any(entry["id"] == EXPECTED_ENGINE for entry in entries)
    else:
        print("NOT ASSESSED: universal catalog is not available", file=sys.stderr)
    print(f"PASS: {EXPECTED_ENGINE} agent contract")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
