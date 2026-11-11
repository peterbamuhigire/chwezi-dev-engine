import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

FILE=Path(__file__).resolve().parents[1]/'upgrade.py'
spec=importlib.util.spec_from_file_location('upgrade',FILE)
u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)

def write_tree(path, version, files):
    path.mkdir(parents=True,exist_ok=True)
    for name,text in files.items():
        f=path/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text,encoding='utf8')
    (path/'manifest.json').write_text(json.dumps({'version':version,'files':{name:u.digest(path/name) for name in files}}),encoding='utf8')

class UpgradeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.repo=self.root/'repo';self.repo.mkdir();subprocess.run(['git','init','-q',str(self.repo)],check=True)
        self.old=self.repo/'auto-agents';self.new=self.root/'source'
        write_tree(self.old,'1',{'driver.py':'old','tests/x.py':'test'})
        write_tree(self.new,'2',{'driver.py':'new','tests/x.py':'test','new.py':'added'})
        (self.old/'config.json').write_text('my settings');(self.old/'PLAN.md').write_text('my plan')
    def tearDown(self): self.tmp.cleanup()
    def test_preview_and_apply_preserve_project_files(self):
        self.assertFalse(u.upgrade(self.new,self.old)['applied']);self.assertEqual((self.old/'driver.py').read_text(),'old')
        self.assertTrue(u.upgrade(self.new,self.old,True)['applied']);self.assertEqual((self.old/'driver.py').read_text(),'new')
        self.assertEqual((self.old/'config.json').read_text(),'my settings');self.assertEqual((self.old/'PLAN.md').read_text(),'my plan')
        self.assertEqual((self.old/'new.py').read_text(),'added')
    def test_local_change_prevents_any_update(self):
        (self.old/'driver.py').write_text('local change')
        with self.assertRaises(u.UpgradeError):u.upgrade(self.new,self.old,True)
        self.assertFalse((self.old/'new.py').exists());self.assertEqual((self.old/'driver.py').read_text(),'local change')
    def test_existing_new_path_prevents_overwrite(self):
        (self.old/'new.py').write_text('user file')
        with self.assertRaises(u.UpgradeError):u.upgrade(self.new,self.old,True)
        self.assertEqual((self.old/'new.py').read_text(),'user file')
    def test_obsolete_managed_file_is_removed_only_when_unchanged(self):
        manifest=json.loads((self.new/'manifest.json').read_text())
        manifest['files'].pop('tests/x.py')
        (self.new/'manifest.json').write_text(json.dumps(manifest),encoding='utf8')
        result=u.upgrade(self.new,self.old,True)
        self.assertIn('tests/x.py',result['removed'])
        self.assertFalse((self.old/'tests/x.py').exists())
        self.assertEqual((self.old/'PLAN.md').read_text(),'my plan')
    def test_lock_and_interrupted_update_block(self):
        lock=self.repo/'.git'/'auto-agents'/'run.lock';lock.parent.mkdir();lock.write_text('occupied')
        with self.assertRaises(u.UpgradeError):u.upgrade(self.new,self.old,True)
        self.assertEqual(lock.read_text(),'occupied')
        lock.unlink(); (self.old/'update-in-progress.json').write_text('{}')
        with self.assertRaises(u.UpgradeError):u.upgrade(self.new,self.old,True)
    def test_manifest_cannot_own_configuration_or_escape(self):
        for name in ('config.json','PLAN.md','../escape','C:/outside','a\\b','bad\x00path'):
            self.assertFalse(u.safe_name(name))
    def test_git_line_endings_do_not_look_like_a_local_edit(self):
        (self.old/'driver.py').write_bytes(b'old\r\nline\r\n')
        manifest=json.loads((self.old/'manifest.json').read_text())
        (self.old/'driver.py').write_bytes(b'old\nline\n')
        manifest['files']['driver.py']=u.digest(self.old/'driver.py')
        manifest['hash_mode']='sha256-text-lf-v1'
        (self.old/'manifest.json').write_text(json.dumps(manifest),encoding='utf8')
        (self.old/'driver.py').write_bytes(b'old\r\nline\r\n')
        self.assertTrue(u.upgrade(self.new,self.old,True)['applied'])
    def test_manifest_survives_git_checkout_with_autocrlf(self):
        subprocess.run(['git','config','user.name','Fixture'],cwd=self.repo,check=True)
        subprocess.run(['git','config','user.email','fixture@example.test'],cwd=self.repo,check=True)
        subprocess.run(['git','config','core.autocrlf','true'],cwd=self.repo,check=True)
        m=json.loads((self.old/'manifest.json').read_text())
        m['hash_mode']='sha256-text-lf-v1'
        (self.old/'manifest.json').write_text(json.dumps(m),encoding='utf8')
        subprocess.run(['git','add','auto-agents'],cwd=self.repo,check=True,capture_output=True)
        subprocess.run(['git','commit','-qm','fixture'],cwd=self.repo,check=True)
        (self.old/'driver.py').unlink()
        subprocess.run(['git','checkout','--','auto-agents/driver.py'],cwd=self.repo,check=True)
        self.assertEqual(u.validate_tree(self.old)['version'],'1')

if __name__=='__main__':unittest.main()
