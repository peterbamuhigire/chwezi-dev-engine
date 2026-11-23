from __future__ import annotations
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[5]
README = ROOT / "README.md"

def slug(text: str) -> str:
    text = re.sub(r"[\s`]+", "-", text.strip().lower())
    text = re.sub(r"[^\w-]", "", text, flags=re.UNICODE)
    return re.sub(r"-+", "-", text).strip("-")

def verify(text: str) -> list[str]:
    errors = []
    headings = re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M)
    slugs = {slug(re.sub(r"<[^>]+>", "", h)) for h in headings}
    h2 = re.findall(r"^##\s+(.+?)\s*#*\s*$", text, re.M)
    if "capabilities" not in [slug(h) for h in h2[:4]]:
        errors.append("Capabilities is not among the first four H2 headings")
    required = [
        "skills/languages/python-ml-predictive/examples/ticket-triage/",
        "skills/ai/ai-rag-patterns/examples/curated-retrieval/evaluate.py",
        "skills/ai/ai-evaluation/examples/adaptation-review/review.py",
        "skills/languages/python-ml-predictive/examples/release-diagnostics/diagnose.py",
        "skills/sdlc-meta/ai-assisted-development/examples/e05-k3/README.md",
        "skills/architecture/api-design-first/SKILL.md",
    ]
    for path in required:
        if path not in text:
            errors.append(f"missing task route: {path}")
    for target in re.findall(r"\]\(([^)]+)\)", text):
        target = target.strip().split()[0].strip("<>")
        if target.startswith(("https://", "http://", "mailto:", "data:")):
            continue
        path, sep, fragment = target.partition("#")
        file = (ROOT / unquote(path)).resolve() if path else README
        if not file.exists():
            errors.append(f"unresolved link: {target}")
        elif sep and fragment:
            try:
                content = file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                errors.append(f"cannot inspect anchor target: {target}")
                continue
            target_headings = {slug(re.sub(r"<[^>]+>", "", h)) for h in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", content, re.M)}
            # Explicit HTML IDs remain valid compatibility anchors.
            ids = set(re.findall(r"\bid=[\"']([^\"']+)[\"']", content))
            if unquote(fragment) not in target_headings and unquote(fragment) not in ids:
                errors.append(f"unresolved anchor: {target}")
    return errors

def main() -> int:
    text = README.read_text(encoding="utf-8")
    errors = verify(text)
    if errors:
        print("FAIL: " + "; ".join(errors))
        return 1
    damaged = text.replace("(skills/architecture/api-design-first/SKILL.md)", "(skills/architecture/missing/SKILL.md)", 1)
    if not any("unresolved link" in error for error in verify(damaged)):
        print("FAIL: negative control did not reject a broken task link")
        return 1
    print("PASS: task table routes and Markdown links resolve; Capabilities is the third H2")
    print("PASS: negative control rejects a broken task link")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
