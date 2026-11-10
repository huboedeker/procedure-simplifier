import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from procedure_simplifier import __version__,framework_root
from procedure_simplifier.cli import export_framework

class CliTests(unittest.TestCase):
    def invoke(self,*args):
        return subprocess.run([sys.executable,'-m','procedure_simplifier',*args],text=True,capture_output=True)

    def test_version(self):
        result=self.invoke('--version');self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(result.stdout.strip(),__version__)

    def test_doctor_is_explicit_about_capabilities(self):
        result=self.invoke('doctor');self.assertEqual(result.returncode,0,result.stderr)
        info=json.loads(result.stdout);self.assertTrue(info['framework_present']);self.assertFalse(info['model_api_calls']);self.assertFalse(info['automatic_agent_dispatch'])

    def test_export_contains_roles_templates_schemas_and_demo(self):
        with tempfile.TemporaryDirectory() as base:
            target=export_framework(Path(base)/'framework')
            for name in ['START-HERE.md','LICENSE','agents/coordinator.md','templates/approach.json','schemas/run-0.2.schema.json','examples/demo/quality.json']:
                self.assertEqual((target/name).read_bytes(),(framework_root()/name).read_bytes())

    def test_export_does_not_overwrite_work(self):
        with tempfile.TemporaryDirectory() as base:
            target=Path(base)/'framework';target.mkdir();(target/'user.txt').write_text('Keep')
            with self.assertRaises(ValueError):export_framework(target)
            self.assertEqual((target/'user.txt').read_text(),'Keep')

    def test_export_cannot_recurse_into_installed_assets(self):
        with self.assertRaises(ValueError):export_framework(framework_root()/'nested')

    def test_complete_demo_checks(self):
        with tempfile.TemporaryDirectory() as base:
            target=export_framework(Path(base)/'framework');demo=target/'examples/demo'
            commands=[['validate',str(demo/'run.json')],['quality',str(demo/'quality.json'),str(demo/'run.json')],['chunks',str(demo/'chunk-plan.json')],['metrics',str(demo/'source.txt'),str(demo/'output.md')]]
            for command in commands:
                result=self.invoke(*command);self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_invalid_record_has_nonzero_exit(self):
        with tempfile.TemporaryDirectory() as base:
            p=Path(base)/'bad.json';p.write_text('{}');result=self.invoke('validate',str(p));self.assertEqual(result.returncode,1)

    def test_version_metadata_agrees(self):
        template=json.loads((framework_root()/'templates/approach.json').read_text());self.assertEqual(template['framework_version'],__version__)
