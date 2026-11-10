"""Synthetic evidence fixtures; no claim of actual domain/reader evaluation."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from test_validation import ROOT

from procedure_simplifier import quality

class QualityTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.base=Path(t.name)
        self.run=json.loads((ROOT/'examples/demo/run.json').read_text())
        source='\n'.join(u['quote'] for u in self.run['units']).encode()
        (self.base/'source.txt').write_bytes(source)
        self.run['source']['sha256']=hashlib.sha256(source).hexdigest()
        output='\n'.join(s['text'] for s in self.run['statements']).encode()
        (self.base/'output.md').write_bytes(output)
        self.q=dict(run_id=self.run['run_id'],delivered_file='output.md',delivered_sha256=hashlib.sha256(output).hexdigest(),reviewed_statement_sha256=quality.statement_digest(self.run),effective_task_artifact='fixture-task',independent_reviewer='Synthetic fixture reviewer',completeness_status='complete',source_manifest=[dict(id='B1',source_file='source.txt',source_sha256=self.run['source']['sha256'],locator='Synthetic full excerpt',expected_content='Fixture source',unit_ids=[u['id'] for u in self.run['units']],disposition='mapped')],scenarios=[dict(id='S1',unit_ids=['R16'],situation='Deviation',source_behavior='Owner approval required',output_behavior='Owner approval required',verdict='match',evidence='Synthetic fixture')],dependencies=[],reduction_cards=[],export_check=dict(status='passed',evidence='Synthetic fixture only'),open_issues=[])
        task=json.dumps(dict(allowed_transformations=self.run['brief']['allowed_transformations'])).encode()
        (self.base/'task.json').write_bytes(task)
        self.q.update(effective_task_file='task.json',effective_task_sha256=hashlib.sha256(task).hexdigest())
        self.q['obligation_details']=[dict(unit_id=u['id'],actor=u['actor'],action='Synthetic fixture action',force=u['force'],trigger='unknown',scope='Synthetic fixture',exceptions='unknown',timing='unknown',evidence='Synthetic fixture',authority='unknown') for u in self.run['units'] if u['kind']!='informative']

    def test_valid_record(self):self.assertEqual(quality.validate(self.q,self.run,self.base),[])

    def test_inventory_detects_disappeared_requirement(self):
        self.run['units']=[u for u in self.run['units'] if u['id']!='R07']
        self.run['statements']=[s for s in self.run['statements'] if s['id']!='SR07']
        self.run['changes']=[c for c in self.run['changes'] if c['unit_id']!='R07']
        self.q['reviewed_statement_sha256']=quality.statement_digest(self.run)
        self.assertTrue(any('missing source units' in e for e in quality.validate(self.q,self.run,self.base)))

    def test_export_change_detected(self):
        (self.base/'output.md').write_text('Changed')
        self.assertTrue(any('hash mismatch' in e for e in quality.validate(self.q,self.run,self.base)))

    def test_statement_change_invalidates_review(self):
        self.run['statements'][0]['text']+=' Changed.'
        self.assertTrue(any('stale' in e for e in quality.validate(self.q,self.run,self.base)))

    def test_substantive_change_needs_impact_card(self):
        self.run['changes'][0]['substantive']=True
        self.assertTrue(any('impact card' in e for e in quality.validate(self.q,self.run,self.base)))

    def test_missing_dependency_must_be_disclosed(self):
        self.q['dependencies']=[dict(id='D1',direction='outbound',source='Missing attachment',version='unknown',status='missing',impact='Unknown')]
        self.assertTrue(any('needs an open issue' in e for e in quality.validate(self.q,self.run,self.base)))

    def test_task_permissions_must_match_record(self):
        self.run['brief']['allowed_transformations'].append('requirement_reduction')
        self.assertTrue(any('permissions disagree' in e for e in quality.validate(self.q,self.run,self.base)))

if __name__=='__main__':unittest.main()
