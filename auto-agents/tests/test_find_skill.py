import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import find_skill


def skill(path, name, desc):
    path.mkdir(parents=True, exist_ok=True)
    (path / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: {desc}\n---\n\n# {name}\n', encoding='utf-8')


class FindSkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        dev = self.root / 'chwezi-development-engine'
        skill(dev / 'skills' / 'database-migration', 'database-migration', 'Use when implementing a database schema migration.')
        skill(dev / 'marketplace-plugin' / 'skills' / 'database-migration', 'database-migration', 'Projection copy of a database migration.')
        (dev / 'AGENTS.md').write_text('# Router\n', encoding='utf-8')
        writing = self.root / 'chwezi-writing-engine'
        skill(writing / 'skills' / 'grants' / 'grant-proposal', 'grant-proposal', 'Use when assembling a grant application.')
        skill(writing / 'dist' / 'agent-plugin' / 'grant-proposal', 'grant-proposal', 'Distribution copy.')
        orch = self.root / 'skills-engine-agents' / 'core' / 'instructions'
        orch.mkdir(parents=True)
        (orch / 'engine-orchestrator.md').write_text('---\ncanonical_id: engine-orchestrator\n---\n\n# Engine orchestrator\n\nUse this instruction when a request must be routed across engines.\n', encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = find_skill.main([*args, '--engines-root', str(self.root)])
        return code, out.getvalue(), err.getvalue()

    def test_searches_only_canonical_folders(self):
        code, out, _ = self.run_main('database', 'migration', '--limit', '9')
        self.assertEqual(code, 0)
        self.assertIn(str(Path('skills') / 'database-migration' / 'SKILL.md'), out)
        self.assertNotIn('marketplace-plugin', out)
        code, out, _ = self.run_main('grant', 'proposal', '--limit', '9')
        self.assertNotIn('dist', out)
        self.assertEqual(out.count('[writing]'), 1)

    def test_orchestrator_alias_and_prose_description(self):
        code, out, _ = self.run_main('route', 'request', 'across', 'engines', '--engine', 'orchestrator')
        self.assertEqual(code, 0)
        self.assertIn('[orchestrator] engine-orchestrator', out)
        self.assertIn('routed across engines', out)

    def test_missing_engine_is_reported_not_fatal(self):
        code, out, err = self.run_main('grant')
        self.assertEqual(code, 0)
        self.assertIn('accounting unavailable', err)

    def test_no_match_and_engine_list(self):
        self.assertEqual(self.run_main('zzzz')[0], 1)
        code, out, _ = self.run_main('--list-engines')
        self.assertIn('development: ' + str(self.root / 'chwezi-development-engine' / 'AGENTS.md'), out)
        self.assertIn('accounting: UNAVAILABLE', out)


if __name__ == '__main__':
    unittest.main()
