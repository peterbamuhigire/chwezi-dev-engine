from tools.build_solution_bundle import build, verify


def test_bundle_manifest_detects_drift(tmp_path):
    root = __import__("pathlib").Path.cwd()
    bundle = tmp_path / "solution-selection.zip"
    result = build(root, bundle)
    assert len(result["files"]) == 10
    assert verify(bundle)["status"] == "PASS"
