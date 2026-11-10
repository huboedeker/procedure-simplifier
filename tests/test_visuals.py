"""Synthetic metadata fixtures; these tests do not inspect actual figures."""
import json
import unittest
from test_validation import ROOT, module

class VisualTests(unittest.TestCase):
    def setUp(self):
        self.run=json.loads((ROOT/'examples/demo/run.json').read_text())
        self.run['schema_version']='0.2'
        self.run['visual_review']=dict(inventory_status='complete',scope='Synthetic page fixture',pages_inspected=[5,6],issues=[],items=[])

    def figure(self):
        item=dict(id='V01',page=5,kind='flowchart',meaning='Synthetic approval flow',rationale='Retain equivalent logic',source_unit_ids=['R16'],source_artifact_ids=['A_SOURCE'],disposition='retain',consistency='consistent',production_status='produced',output_artifact_ids=['A_OUTPUT'],reviewed_text_sha256=module.statement_digest(self.run),issue_ids=[])
        self.run['visual_review']['items']=[item]
        return item

    def test_complete_no_figures(self):
        self.assertEqual(module.validate(self.run),[])

    def test_missing_visual_inventory(self):
        del self.run['visual_review']
        self.assertTrue(any('requires a visual inventory' in e for e in module.validate(self.run)))

    def test_complete_inventory_needs_inspected_pages(self):
        self.run['visual_review']['pages_inspected']=[]
        self.assertTrue(any('inspected pages' in e for e in module.validate(self.run)))

    def test_retained_visual_metadata(self):
        self.figure()
        self.assertEqual(module.validate(self.run),[])

    def test_text_revision_invalidates_visual_check(self):
        self.figure()
        self.run['statements'][0]['text']+=' Revised.'
        self.assertTrue(any('stale' in e for e in module.validate(self.run)))

    def test_modification_brief_is_not_completed_output(self):
        item=self.figure();item.update(disposition='revise',production_status='proposed',consistency='unresolved',output_artifact_ids=[])
        self.assertTrue(any('surfaced as an issue' in e for e in module.validate(self.run)))

    def test_produced_visual_needs_artifact(self):
        self.figure()['output_artifact_ids']=[]
        self.assertTrue(any('actual output artifact' in e for e in module.validate(self.run)))

    def test_pending_visual_can_be_flagged_for_review_not_approval(self):
        item=self.figure();item.update(consistency='conflict',issue_ids=['Q01'])
        self.assertEqual(module.validate(self.run),[])
        self.run['stage']='approved'
        self.assertTrue(any('inconsistent visuals prevent approval' in e for e in module.validate(self.run)))

    def test_unmapped_visual_content(self):
        self.figure()['source_unit_ids']=['UNKNOWN']
        self.assertTrue(any('Unknown visual source' in e for e in module.validate(self.run)))

    def test_removing_visual_content_needs_permission(self):
        item=self.figure();item.update(disposition='remove',content_handling='reduced',output_artifact_ids=[],consistency='not_applicable')
        self.assertTrue(any('outside the mandate' in e for e in module.validate(self.run)))

if __name__=='__main__': unittest.main()
