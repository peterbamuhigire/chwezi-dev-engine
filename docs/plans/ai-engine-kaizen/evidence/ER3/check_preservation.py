from __future__ import annotations
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[5]
BASE = "7965083c0dedbfd5c6e52847d1c2db9ddfec3dba"

def slug(text: str) -> str:
    text = re.sub(r"[`*_]", "", text.strip().lower())
    text = re.sub(r"[^\w -]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", re.sub(r"-+", " ", text)).strip("-")

def anchors(text: str) -> set[str]:
    return {slug(h) for h in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M)}

def links(text: str):
    return re.findall(r"\]\(([^)]+)\)", text)

def main() -> int:
    current = (ROOT / "README.md").read_text(encoding="utf-8")
    old_bytes = subprocess.run(["git", "show", f"{BASE}:README.md"], cwd=ROOT, capture_output=True, check=True).stdout
    old = old_bytes.decode("utf-8")
    old_anchors = anchors(old)
    current_anchors = anchors(current)
    missing = old_anchors - current_anchors
    if missing:
        print("FAIL: removed baseline README anchors: " + ", ".join(sorted(missing)))
        return 1
    h2 = re.findall(r"^##\s+(.+?)\s*#*\s*$", current, re.M)
    if "capabilities" not in [slug(h) for h in h2[:4]]:
        print("FAIL: Capabilities is not among first four H2 headings")
        return 1
    inbound = []
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.split(b"\0")
    for raw in tracked:
        if not raw:
            continue
        path = ROOT / raw.decode("utf-8")
        if path == ROOT / "README.md" or path.suffix.lower() not in {".md", ".rst", ".txt"}:
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for target in re.findall(r"\]\(([^)]+)\)", body):
            target = target.strip().split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path, separator, ref = target.partition("#")
            if separator and Path(unquote(target_path)).as_posix() == "README.md":
                inbound.append((path.relative_to(ROOT).as_posix(), unquote(ref)))
    unresolved_inbound = [(path, ref) for path, ref in inbound if ref not in current_anchors]
    if unresolved_inbound:
        print("FAIL: unresolved inbound README anchors: " + repr(unresolved_inbound))
        return 1
    print(f"PASS: preserved {len(old_anchors)} baseline README heading anchors")
    print(f"PASS: {len(inbound)} tracked inbound README anchors resolve")
    print(f"PASS: Capabilities is H2 number {[slug(h) for h in h2].index('capabilities') + 1}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
