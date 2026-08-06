from pathlib import Path

from scripts.validate_engine_control_plane import validate_registry


def test_control_plane_registry_has_all_ten_engines():
    assert validate_registry() == []


def test_control_plane_registry_resolves_local_routers():
    workspace_root = Path(__file__).resolve().parents[2]
    assert validate_registry(workspace_root) == []


def test_control_plane_registry_resolves_local_adoption_documents():
    workspace_root = Path(__file__).resolve().parents[2]
    assert validate_registry(workspace_root) == []
