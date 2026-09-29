"""Keep a bare `pytest` run at the repository root from collecting fixture code.

The public tests under Fxx/public_tests/ run inside a composed workspace (fixture_kit.py), never
in place; CI runs `pytest tests` only.
"""
collect_ignore_glob = ["F*/*"]
