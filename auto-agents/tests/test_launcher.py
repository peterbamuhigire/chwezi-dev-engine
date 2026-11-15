"""Windows launcher behavior using a fake driver in a disposable fixture."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
AUTO_AGENTS = ROOT / "auto-agents"


@unittest.skipUnless(os.name == "nt", "PowerShell launcher tests require Windows")
class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="auto agents launcher ")
        self.root = Path(self.temp.name)
        self.auto_agents = self.root / "auto-agents"
        self.auto_agents.mkdir()
        shutil.copy2(AUTO_AGENTS / "run.ps1", self.auto_agents / "run.ps1")
        shutil.copy2(AUTO_AGENTS / "run.cmd", self.auto_agents / "run.cmd")
        (self.auto_agents / "driver.py").write_text(
            "import json, os, sys\n"
            "if '--help' in sys.argv:\n"
            " print('usage: driver {check,start,watch,status,run,resume,stop,cancel,recover}')\n"
            " raise SystemExit(0)\n"
            "action=sys.argv[1]\n"
            "print('VISIBLE-'+action)\n"
            "with open(os.environ['FAKE_DRIVER_LOG'], 'a', encoding='utf-8') as f:\n"
            " f.write(json.dumps(sys.argv[1:])+'\\n')\n"
            "raise SystemExit(int(os.environ.get('FAKE_'+action.upper()+'_EXIT','0')))\n",
            encoding="utf-8",
        )
        self.log = self.root / "calls.jsonl"
        self.env = os.environ.copy()
        self.env["FAKE_DRIVER_LOG"] = str(self.log)
        self.powershell = shutil.which("powershell.exe") or shutil.which("pwsh.exe")
        if not self.powershell:
            self.skipTest("Windows PowerShell executable is unavailable")
        if Path(sys.executable).suffix.lower() != ".exe":
            self.skipTest("Python executable path is not a Windows .exe")

    def tearDown(self):
        self.temp.cleanup()

    def invoke(self, *args, cwd=None):
        return subprocess.run(
            [self.powershell, "-NoProfile", "-File", str(self.auto_agents / "run.ps1"),
             *args, "-PythonPath", sys.executable],
            cwd=cwd or self.root,
            env=self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines() if line]

    def test_default_checks_starts_and_watches_from_other_working_directory(self):
        self.env["FAKE_WATCH_EXIT"] = "17"
        result = self.invoke(cwd=Path(tempfile.gettempdir()))
        self.assertEqual(result.returncode, 17, result.stdout)
        self.assertEqual(self.calls(), [["check"], ["start"], ["watch"]])
        for action in ("check", "start", "watch"):
            self.assertIn("VISIBLE-" + action, result.stdout)

    def test_no_watch_and_check_failure_prevents_start(self):
        self.env["FAKE_CHECK_EXIT"] = "2"
        result = self.invoke("-NoWatch", cwd=self.auto_agents)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertEqual(self.calls(), [["check"]])
        self.assertIn("VISIBLE-check", result.stdout)
        self.assertNotIn("VISIBLE-start", result.stdout)

    def test_direct_action_passes_real_exit_code_and_help_never_calls_driver(self):
        self.env["FAKE_STOP_EXIT"] = "9"
        result = self.invoke("-Action", "Stop", cwd=self.auto_agents)
        self.assertEqual(result.returncode, 9, result.stdout)
        self.assertEqual(self.calls(), [["stop"]])
        self.assertIn("VISIBLE-stop", result.stdout)

        self.log.unlink()
        result = subprocess.run(
            [self.powershell, "-NoProfile", "-File", str(self.auto_agents / "run.ps1"),
             "-Action", "Help", "-PythonPath", "Z:\\missing\\python.exe"],
            cwd=self.root,
            env=self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.calls(), [])

if __name__ == "__main__":
    unittest.main()
