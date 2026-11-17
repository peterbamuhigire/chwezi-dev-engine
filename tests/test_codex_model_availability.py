"""Behaviour checks for the availability-aware Codex adapter; no provider calls."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('codex_policy', ROOT/'.codex/ensure_model_policy.py')
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


class CodexPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.catalogue('gpt-6.2-sol', 'gpt-6.1-terra')

    def catalogue(self, *models, age=0, effort='medium'):
        data = {'fetched_at': (dt.datetime.now(dt.timezone.utc)-dt.timedelta(hours=age)).isoformat(),
                'models': [{'slug': model, 'visibility': 'list',
                            'supported_reasoning_levels': [{'effort': effort}]} for model in models]}
        (self.home/'models_cache.json').write_text(json.dumps(data), encoding='utf-8')

    def config(self):
        return tomllib.loads((self.home/'config.toml').read_text())

    def test_preferred_default_roles_and_idempotence(self):
        policy.apply(self.home, ROOT)
        policy.check(self.home, ROOT)
        before = {p.relative_to(self.home): p.read_bytes() for p in self.home.rglob('*') if p.is_file()}
        policy.apply(self.home, ROOT)
        self.assertEqual(before, {p.relative_to(self.home): p.read_bytes() for p in self.home.rglob('*') if p.is_file()})
        self.assertEqual(self.config()['model'], 'gpt-6.2-sol')
        for role in (self.home/'agents').glob('*.toml'):
            self.assertEqual(tomllib.loads(role.read_text())['model'], 'gpt-6.2-sol')

    def test_fallback_and_upgrade_when_sol_appears(self):
        self.catalogue('gpt-6.1-terra')
        policy.apply(self.home, ROOT)
        policy.check(self.home, ROOT)
        self.assertEqual(self.config()['model'], 'gpt-6.1-terra')
        self.catalogue('gpt-6.2-sol', 'gpt-6.1-terra')
        policy.apply(self.home, ROOT)
        policy.check(self.home, ROOT)
        self.assertEqual(self.config()['model'], 'gpt-6.2-sol')

    def test_unavailable_or_stale_catalogue_writes_nothing(self):
        cases = [([], 0, 'medium'), (['gpt-6.2-sol'], 25, 'medium'),
                 (['gpt-6.2-sol'], -1, 'medium'), (['gpt-6.2-sol'], 0, 'low')]
        for models, age, effort in cases:
            with self.subTest(models=models, age=age, effort=effort):
                self.catalogue(*models, age=age, effort=effort)
                with self.assertRaises(policy.PolicyError):
                    policy.apply(self.home, ROOT)
                self.assertFalse((self.home/'config.toml').exists())

    def test_missing_or_malformed_catalogue_writes_nothing(self):
        cache = self.home/'models_cache.json'
        cache.unlink()
        with self.assertRaises(policy.PolicyError):
            policy.apply(self.home, ROOT)
        cache.write_text('{bad json')
        with self.assertRaises(policy.PolicyError):
            policy.apply(self.home, ROOT)
        self.assertFalse((self.home/'config.toml').exists())

    def test_explicit_astra_is_preserved(self):
        for model in ('gpt-6-astra', 'gpt-6.2-astra'):
            for effort in ('medium', 'high'):
                with self.subTest(model=model, effort=effort):
                    (self.home/'config.toml').write_text(
                        f'model = "{model}"\nmodel_reasoning_effort = "{effort}"\n')
                    policy.apply(self.home, ROOT)
                    policy.check(self.home, ROOT)
                    self.assertEqual(self.config()['model'], model)
                    self.assertEqual(self.config()['model_reasoning_effort'], effort)
                    self.assertEqual(self.config()['review_model'], 'gpt-6.2-sol')

    def test_unrelated_settings_and_custom_role_preserved(self):
        (self.home/'config.toml').write_text('approval_policy = "never"\n[agents.specialist]\nconfig_file = "custom.toml"\n')
        (self.home/'AGENTS.md').write_text('Keep this user instruction.\n')
        policy.apply(self.home, ROOT)
        self.assertEqual(self.config()['approval_policy'], 'never')
        self.assertEqual(self.config()['agents']['specialist']['config_file'], 'custom.toml')
        self.assertTrue((self.home/'AGENTS.md').read_text().startswith('Keep this user instruction.'))

    def test_known_terra_template_migrates(self):
        policy.apply(self.home, ROOT)
        for p in (self.home/'agents').glob('*.toml'):
            p.write_text(p.read_text().replace('gpt-6.2-sol', 'gpt-6.1-terra'))
        policy.apply(self.home, ROOT)
        policy.check(self.home, ROOT)

    def test_custom_instructions_block_without_partial_write(self):
        policy.apply(self.home, ROOT)
        role = self.home/'agents/worker.toml'
        role.write_text(role.read_text().replace('Implement only', 'Custom restriction: Implement only'))
        before = (self.home/'config.toml').read_bytes()
        with self.assertRaises(policy.PolicyError):
            policy.apply(self.home, ROOT)
        self.assertEqual((self.home/'config.toml').read_bytes(), before)
        self.assertIn('Custom restriction', role.read_text())

    def test_custom_role_path_blocks(self):
        (self.home/'config.toml').write_text('[agents.worker]\nconfig_file = "custom-worker.toml"\n')
        with self.assertRaises(policy.PolicyError):
            policy.apply(self.home, ROOT)
        self.assertFalse((self.home/'agents').exists())

    def test_claude_mode_does_not_touch_codex(self):
        self.assertEqual(policy.main(['--runtime', 'claude', '--apply', '--codex-home', str(self.home)]), 0)
        self.assertFalse((self.home/'config.toml').exists())


if __name__ == '__main__':
    unittest.main()
