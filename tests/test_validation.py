import copy
import importlib.util
import json
import unittest
from pathlib import Path

from procedure_simplifier import framework_root
from procedure_simplifier import validate as module
ROOT = framework_root()


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.run = json.loads((ROOT/'examples/demo/run.json').read_text())
        # A completed review is represented here for isolated gate tests.
        self.run['review'] = {'status': 'completed', 'reviewer': 'test fixture', 'findings': []}

    def test_baseline(self):
        self.assertEqual(module.validate(self.run), [])

    def test_lost_disposition(self):
        self.run['changes'].pop()
        self.assertTrue(any('no change disposition' in e for e in module.validate(self.run)))

    def test_duplicate_unit(self):
        self.run['units'].append(copy.deepcopy(self.run['units'][0]))
        self.assertTrue(any('duplicate ID' in e for e in module.validate(self.run)))

    def test_dangling_output(self):
        self.run['changes'][0]['output_ids'] = ['MISSING']
        self.assertTrue(any('broken output backlink' in e for e in module.validate(self.run)))

    def test_unsupported_statement(self):
        self.run['statements'].append({'id':'NEW','text':'Obtain annual approval.','source_ids':[]})
        self.assertTrue(any('unsupported statement' in e for e in module.validate(self.run)))

    def test_substantive_change_without_permission(self):
        self.run['changes'][1]['substantive'] = True
        self.assertTrue(any('substantive change outside mandate' in e for e in module.validate(self.run)))

    def test_disguised_requirement_removal(self):
        self.run['changes'][1].update(disposition='removed', output_ids=[])
        self.assertTrue(any('requirement removal must' in e for e in module.validate(self.run)))

    def test_unknown_dependency(self):
        self.run['units'][0]['dependencies'] = ['UNKNOWN']
        self.assertTrue(any('unknown dependency' in e for e in module.validate(self.run)))

    def test_missing_review(self):
        self.run['review']['status'] = 'pending'
        self.assertTrue(any('Independent review' in e for e in module.validate(self.run)))

    def test_unresolved_reviewer_finding(self):
        self.run['review']['findings'] = [{'id':'F1','status':'open'}]
        self.assertTrue(any('explicitly escalated' in e for e in module.validate(self.run)))

    def test_approval_bypass(self):
        self.run['stage'] = 'approved'
        errors = module.validate(self.run)
        self.assertTrue(any('Explicit human' in e for e in errors))
        self.assertTrue(any('Blocking issues' in e for e in errors))

    def test_wrong_record_shape(self):
        self.run['units'] = 'bad input'
        self.assertTrue(any('list of objects' in e for e in module.validate(self.run)))

    def test_semantic_limit_is_explicit(self):
        # Structural links still pass after semantic corruption. Review must catch this.
        self.run['statements'][1]['text'] = 'The team may skip all required checks.'
        self.assertEqual(module.validate(self.run), [])

    def test_empty_approval_object_rejected(self):
        self.run.update(stage='approved',issues=[],approvals=[{}])
        self.run['brief']['approval_status']='approved'
        self.assertTrue(any('Approval requires identity' in e for e in module.validate(self.run)))

    def test_method_recommendation_does_not_become_binding(self):
        self.run['units'][0]['kind']='recommendation'
        self.run['units'][0]['force']='should: historical method advice, not institutional obligation'
        self.assertEqual(module.validate(self.run), [])

    def test_recommendation_cannot_be_silently_removed(self):
        self.run['units'][0]['kind']='recommendation'
        self.run['changes'][0].update(disposition='removed',output_ids=[])
        self.assertTrue(any('requirement removal must' in e for e in module.validate(self.run)))


if __name__ == '__main__':
    unittest.main()
