import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import execution  # noqa: E402


class WorktreeRootTest(unittest.TestCase):
    def test_default_stays_under_git_common_dir(self):
        cfg = {'runner': 'claude'}
        self.assertEqual(execution.worktree_path(Path('/repo'), cfg, Path('/repo/.git/auto-agents')),
                         Path('/repo/.git/auto-agents/worktrees/claude'))

    def test_relative_root_resolves_against_repository(self):
        cfg = {'runner': 'claude', 'worktree_root': '../Repo-autorun'}
        got = execution.worktree_path(Path('/x/repo'), cfg, Path('/x/repo/.git/auto-agents'))
        self.assertEqual(got, (Path('/x/repo') / '../Repo-autorun').resolve() / 'claude')

    def test_lanes_get_distinct_folders_under_the_root(self):
        cfg = {'runner': 'codex', 'worktree_root': '../Repo-autorun', 'lane': 'api'}
        got = execution.worktree_path(Path('/x/repo'), cfg, Path('/x/repo/.git/auto-agents/lanes/api'))
        self.assertEqual(got, (Path('/x/repo') / '../Repo-autorun').resolve() / 'lane-api-codex')

    def test_location_key_does_not_change_run_digest(self):
        cfg = {'runner': 'claude', 'plan': 'p.md'}
        self.assertEqual(execution.config_digest(cfg),
                         execution.config_digest({**cfg, 'worktree_root': '../elsewhere'}))
        self.assertNotEqual(execution.config_digest(cfg), execution.config_digest({**cfg, 'plan': 'q.md'}))

    def test_digest_matches_earlier_releases_without_location_keys(self):
        # Runs started by earlier releases (plain sha256 of the whole config) must still resume.
        import hashlib
        import json
        cfg = {'runner': 'claude', 'plan': 'p.md', 'max_hours': 24}
        self.assertEqual(execution.config_digest(cfg),
                         hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest())


if __name__ == '__main__':
    unittest.main()
