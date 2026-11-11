import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

DRIVER = Path(__file__).resolve().parents[1] / 'driver.py'

def git(root, *args):
    return subprocess.run(['git',*args],cwd=root,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).stdout.strip()

class DriverTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)/'repo'; self.root.mkdir()
        git(self.root,'init','-q'); git(self.root,'config','user.email','fixture@example.test'); git(self.root,'config','user.name','Fixture')
        (self.root/'auto-agents').mkdir()
        (self.root/'auto-agents'/'PLAN.md').write_text('# Plan\n',encoding='utf8')
        git(self.root,'add','.'); git(self.root,'commit','-qm','initial')
        spec=importlib.util.spec_from_file_location('driver_fixture',DRIVER)
        self.d=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.d)
        self.d.ROOT=self.root
        self.base=self.root/'.git'/'auto-agents'
        self.fake=self.root.parent/'fake.py'
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\np=pathlib.Path("auto-agents/PLAN.md")\np.write_text("STATUS: DONE\\n",encoding="utf8")\nsubprocess.run(["git","add",str(p)],check=True)\nsubprocess.run(["git","commit","-qm","finish slice"],check=True)\n''',encoding='utf8')
        self.d.agent_command=lambda cfg:[sys.executable,str(self.fake)]
        self.cfg={'runner':'codex','plan':'auto-agents/PLAN.md','verify':[[sys.executable,'-c','pass']],'session_timeout_seconds':20,'max_hours':1,'max_sessions':2,'publish':False,'remote':'origin','target_branch':'main'}
    def tearDown(self): self.tmp.cleanup()
    def test_accepts_committed_slice_and_completes(self):
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        self.assertEqual(json.loads((self.base/'status.json').read_text())['state'],'done')
        self.assertEqual((self.root/'auto-agents'/'PLAN.md').read_text(),'# Plan\n')
    def test_failed_gate_blocks_and_does_not_publish(self):
        self.cfg['verify']=[[sys.executable,'-c','import sys;sys.exit(7)']]
        self.cfg['max_sessions']=1
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        s=json.loads((self.base/'status.json').read_text())
        self.assertEqual(s['state'],'stopped')
        events=(self.base/'events.jsonl').read_text(); self.assertNotIn('published',events)
        self.cfg['verify']=[[sys.executable,'-c','pass']]
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        s=json.loads((self.base/'status.json').read_text())
        self.assertNotEqual(s['state'],'done')
    def test_failed_gate_can_be_repaired_in_next_session(self):
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\np=pathlib.Path("auto-agents/PLAN.md")\np.write_text("STATUS: DONE\\n",encoding="utf8")\nf=pathlib.Path("fixed.txt")\nif f.exists(): f.write_text("yes",encoding="utf8")\nelse: f.write_text("no",encoding="utf8")\nsubprocess.run(["git","add",str(p),str(f)],check=True)\nsubprocess.run(["git","commit","-qm","slice or repair"],check=True)\n''',encoding='utf8')
        self.cfg['max_sessions']=3
        self.cfg['verify']=[[sys.executable,'-c','from pathlib import Path; import sys; sys.exit(0 if Path("fixed.txt").read_text()=="yes" else 1)']]
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        s=json.loads((self.base/'status.json').read_text())
        self.assertEqual(s['state'],'done')
        self.assertFalse((self.base/'pending-codex.json').exists())
    def test_stop_and_lock_block_execution(self):
        self.base.mkdir(parents=True); (self.base/'STOP').write_text('stop')
        self.assertEqual(self.d.run(self.cfg,self.base),2)
        self.assertFalse((self.base/'run.lock').exists())
        (self.base/'run.lock').write_text('existing')
        with self.assertRaises(self.d.Stop): self.d.run(self.cfg,self.base)
        self.assertEqual((self.base/'run.lock').read_text(),'existing')
    def test_verified_push_to_local_remote(self):
        remote=self.root.parent/'remote.git'
        subprocess.run(['git','init','--bare','-q',str(remote)],check=True)
        git(self.root,'remote','add','origin',str(remote))
        self.cfg['publish']=True
        self.cfg['target_branch']='delivery'
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        sent=git(remote,'rev-parse','refs/heads/delivery')
        worker=self.base/'worktrees'/'codex'
        self.assertEqual(sent,git(worker,'rev-parse','HEAD'))
        self.assertIn('published',(self.base/'events.jsonl').read_text())
    def test_rate_limit_retries_without_changes(self):
        marker=self.root.parent/'attempted'
        self.fake.write_text('''import pathlib,subprocess,sys\nsys.stdin.read()\nm=pathlib.Path(%r)\nif not m.exists():\n m.write_text('once')\n print('usage limit')\n sys.exit(1)\np=pathlib.Path('auto-agents/PLAN.md')\np.write_text('STATUS: DONE\\n',encoding='utf8')\nsubprocess.run(['git','add',str(p)],check=True)\nsubprocess.run(['git','commit','-qm','finish'],check=True)\n''' % str(marker),encoding='utf8')
        self.cfg.update(max_sessions=3,initial_backoff_seconds=0.01,max_backoff_seconds=0.01,max_rate_retries=2)
        self.assertEqual(self.d.run(self.cfg,self.base),0)
        self.assertEqual(json.loads((self.base/'status.json').read_text())['state'],'done')
        self.assertIn('rate_wait',(self.base/'events.jsonl').read_text())
    def test_empty_verify_rejected(self):
        self.cfg['verify']=[]; self.d.CFG=self.root/'auto-agents'/'config.json'
        self.d.CFG.write_text(json.dumps(self.cfg),encoding='utf8')
        with self.assertRaises(self.d.Stop): self.d.config()

if __name__=='__main__': unittest.main()
