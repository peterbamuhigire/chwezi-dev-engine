import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('receipt_runtime', Path(__file__).resolve().parents[1] / 'durable.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


class ReceiptReads(unittest.TestCase):
    def test_transient_windows_denial_recovers_read(self):
        with patch.object(d, 'os', SimpleNamespace(name='nt')), patch.object(
                Path, 'read_text', side_effect=[PermissionError('busy'), '{"state":"passed"}']) as read, patch.object(d.time, 'sleep'):
            self.assertEqual(d.read_json('result.json'), {'state': 'passed'})
            self.assertEqual(read.call_count, 2)

    def test_persistent_denial_remains_failure(self):
        with patch.object(d, 'os', SimpleNamespace(name='nt')), patch.object(
                Path, 'read_text', side_effect=PermissionError('denied')) as read, patch.object(d.time, 'sleep') as sleep:
            with self.assertRaises(PermissionError):
                d.read_json('result.json')
            self.assertEqual(read.call_count, 8)
            self.assertEqual(sleep.call_count, 7)

    def test_non_windows_denial_is_not_retried(self):
        with patch.object(d, 'os', SimpleNamespace(name='posix')), patch.object(
                Path, 'read_text', side_effect=PermissionError('denied')) as read, patch.object(d.time, 'sleep') as sleep:
            with self.assertRaises(PermissionError):
                d.read_json('result.json')
            self.assertEqual(read.call_count, 1)
            sleep.assert_not_called()

    def test_missing_and_corrupt_receipts_fail_without_retry(self):
        for failure in (FileNotFoundError('missing'), json.JSONDecodeError('invalid', '!', 0)):
            with self.subTest(error=type(failure).__name__), patch.object(
                    Path, 'read_text', side_effect=failure) as read, patch.object(d.time, 'sleep') as sleep:
                with self.assertRaises(type(failure)):
                    d.read_json('result.json')
                self.assertEqual(read.call_count, 1)
                sleep.assert_not_called()

    @unittest.skipUnless(os.name == 'nt', 'Windows receipt contention')
    def test_receipt_retry_does_not_relaunch_completed_job(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            job = root / 'job'
            marker = root / 'effect.txt'
            d.prepare(job, [sys.executable, '-c',
                f'from pathlib import Path; p=Path({str(marker)!r}); p.write_text(p.read_text()+"x" if p.exists() else "x")'], root, 10)
            self.assertEqual(d.wait(job)['state'], 'passed')
            original = Path.read_text
            denied = []
            def read(path, *args, **kwargs):
                if path.name == 'result.json' and not denied:
                    denied.append(True)
                    raise PermissionError('simulated transient sharing denial')
                return original(path, *args, **kwargs)
            with patch.object(Path, 'read_text', read), patch.object(d, 'launch') as launch:
                self.assertEqual(d.wait(job)['state'], 'passed')
                launch.assert_not_called()
            self.assertEqual(denied, [True])
            self.assertEqual(marker.read_text(), 'x')
