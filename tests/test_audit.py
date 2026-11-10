import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from procedure_simplifier import framework_root
from procedure_simplifier import audit
ROOT=framework_root()

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.request=self.base/'request.txt'
        self.request.write_text('Preserve content, allow a new structure.')
        self.run=audit.init(self.base/'runs','test',self.request)
        self.plan=json.loads((ROOT/'templates/approach.json').read_text())
        self.plan.update(objective='Readable procedure',audience='Engineers',scope='Section 4.2',format='Free',success_criteria=['Preserve obligations'])
        self.plan.update(output_role='proposed_replacement',decision_owner='Fixture owner',adoption_authority='Not approved; fixture only',framework_version='0.8.0',skill_target='Fixture instructions')
        self.plan['decisions'][0].update(choice='Content-preserving restructure',input_refs=['A00002'])
        values=dict(wording='plain', structure='reorganize', consolidation=True,
                    process_redesign=False, requirement_reduction='none', format_fidelity='free',
                    research='provided_only', clarification='material_gaps')
        self.plan['switches']={k:dict(value=v,decision_ref='D01') for k,v in values.items()}

    def select(self):
        f=self.base/'approach.json'; f.write_text(json.dumps(self.plan))
        return audit.set_approach(self.run,f)

    def test_blocks_draft_before_approach(self):
        with self.assertRaisesRegex(ValueError,'approach'):
            audit.capture(self.run,self.request,'draft')

    def test_material_gap_blocks_selection(self):
        self.plan['gaps']=[dict(id='Q1',question='Allow reductions?',status='open',material=True,handling='Ask user')]
        with self.assertRaisesRegex(ValueError,'Material'):
            self.select()

    def test_new_input_requires_reconsideration(self):
        self.select()
        audit.capture(self.run,self.request,'user_input')
        with self.assertRaisesRegex(ValueError,'updated approach'):
            audit.stage(self.run,'draft')
        with self.assertRaisesRegex(ValueError,'approach'):
            audit.capture(self.run,self.request,'draft')
        self.select()
        audit.stage(self.run,'draft')

    def test_artifact_revisions_and_integrity(self):
        self.select()
        first=audit.capture(self.run,self.request,'draft')
        second=audit.capture(self.run,self.request,'draft',parents=[first['artifact_id']])
        self.assertNotEqual(first['path'],second['path'])
        self.assertTrue(audit.verify(self.run))
        (self.run/first['path']).write_text('Changed')
        with self.assertRaisesRegex(ValueError,'changed artifact'):
            audit.verify(self.run)

    def test_event_mutation_detected(self):
        f=self.run/'events.jsonl';f.write_text(f.read_text().replace('run_created','run_altered'))
        with self.assertRaisesRegex(ValueError,'chain'):
            audit.verify(self.run)

    def test_unknown_input_decision_rejected(self):
        self.plan['decisions'][0]['input_refs']=['invented']
        with self.assertRaisesRegex(ValueError,'recorded user input'):
            self.select()

    def test_nonmaterial_gap_can_be_recorded(self):
        self.plan['gaps']=[dict(id='Q1',question='Exact heading style?',status='open',material=False,handling='Use stated default')]
        self.select()
        audit.stage(self.run,'analysis')
        self.assertTrue(audit.verify(self.run))

    def test_unknown_parent_rejected(self):
        self.select()
        with self.assertRaisesRegex(ValueError,'Unknown parent'):
            audit.capture(self.run,self.request,'draft',parents=['missing'])

    def test_missing_switch_is_not_silently_defaulted(self):
        self.plan['switches'].pop('research')
        with self.assertRaisesRegex(ValueError,'all supported choices'):
            self.select()

    def test_switch_requires_decision_provenance(self):
        self.plan['switches']['research']['decision_ref']='missing'
        with self.assertRaisesRegex(ValueError,'recorded decision'):
            self.select()

    def test_incompatible_format_and_structure(self):
        self.plan['switches']['format_fidelity']['value']='preserve'
        with self.assertRaisesRegex(ValueError,'conflicts'):
            self.select()

    def test_switch_cannot_silently_grant_reductions(self):
        self.plan['allowed_transformations'].append('requirement_reduction')
        with self.assertRaisesRegex(ValueError,'match selected'):
            self.select()

    def test_outcome_profile_allows_explicit_reduction(self):
        self.plan['switches']['requirement_reduction']['value']='assumption_based'
        self.plan['allowed_transformations'].append('requirement_reduction')
        self.plan['mode']='outcome'
        self.select()
        self.assertTrue(audit.verify(self.run))

    def test_bool_switch_rejects_text(self):
        self.plan['switches']['process_redesign']['value']='false'
        with self.assertRaisesRegex(ValueError,'invalid task switch'):
            self.select()

    def test_unselected_switch_blocks_processing(self):
        self.plan['switches']['wording']['value']=None
        with self.assertRaisesRegex(ValueError,'Unselected'):
            self.select()

    def closeout_fixture(self, candidates=None, disposition='no_change'):
        self.select()
        audit.capture(self.run,self.request,'draft')
        latest={e['kind']:e['artifact_id'] for e in audit.events(self.run) if e['type']=='artifact'}
        common=dict(run_id='test',draft_ref=latest['draft'],approach_ref=latest['approach'])
        def capture_json(kind,data):
            f=self.base/(kind+'.json');f.write_text(json.dumps(dict(common,**data)))
            return audit.capture(self.run,f,kind)
        capture_json('summary',dict(approach_summary='Synthetic preservation fixture',metrics={'status':'not_measured','reason':'Synthetic test'},major_omissions=[],additions=[],risks=[],visual_status='Synthetic fixture',review_status='Synthetic test only',limitations=[]))
        f=self.base/'learning.json'
        f.write_text(json.dumps(dict(run_id='test',feedback_basis='Synthetic regression fixture',target_skill_set='Fixture framework',overall_disposition=disposition,reason='Test disposition',candidates=candidates or [])))
        audit.capture(self.run,f,'learning')
        for kind in ['review','changes','risk_assessment','quality']:audit.capture(self.run,self.request,kind)
        capture_json('validation',dict(checks=[dict(name='Synthetic test',status='passed',evidence='Fixture only')]))
        latest={e['kind']:e['artifact_id'] for e in audit.events(self.run) if e['type']=='artifact'}
        capture_json('delivery',dict(status='proposal',artifact_refs=list(latest.values()),open_issues=[]))

    def test_closeout_requires_summary_and_learning(self):
        self.select()
        audit.capture(self.run,self.request,'draft')
        with self.assertRaisesRegex(ValueError,'requires summary'):
            audit.stage(self.run,'closed')

    def test_no_change_learning_can_close_without_policy_approval(self):
        self.closeout_fixture()
        audit.stage(self.run,'closed')
        self.assertEqual(audit.events(self.run)[-1]['stage'],'closed')

    def test_new_draft_invalidates_old_closeout(self):
        self.closeout_fixture()
        audit.capture(self.run,self.request,'draft')
        with self.assertRaisesRegex(ValueError,'predates'):
            audit.stage(self.run,'closed')

    def test_applied_learning_requires_actual_references(self):
        self.closeout_fixture([dict(id='L1',observation='Synthetic improvement',decision='applied',reason='Regression example',evidence_refs=['A00002'])],'applied')
        with self.assertRaisesRegex(ValueError,'before_refs'):
            audit.stage(self.run,'closed')

    def test_unresolved_learning_cannot_close(self):
        self.closeout_fixture([dict(id='L1',observation='Synthetic issue',decision='pending',reason='Not yet decided',evidence_refs=['A00002'])],'mixed')
        with self.assertRaisesRegex(ValueError,'final disposition'):
            audit.stage(self.run,'closed')

    def test_applied_learning_with_version_review_and_checks(self):
        self.select()
        before=audit.capture(self.run,self.request,'framework_before')
        after=audit.capture(self.run,self.request,'framework_after')
        review=audit.capture(self.run,self.request,'review')
        checks=audit.capture(self.run,self.request,'validation')
        self.closeout_fixture([dict(id='L1',observation='Synthetic reusable improvement',decision='applied',reason='Test record only',evidence_refs=[review['artifact_id']],before_refs=[before['artifact_id']],after_refs=[after['artifact_id']],review_refs=[review['artifact_id']],validation_refs=[checks['artifact_id']],rollback_refs=[before['artifact_id']])],'applied')
        audit.stage(self.run,'closed')

    def test_placeholder_cannot_satisfy_closeout(self):
        self.closeout_fixture()
        audit.capture(self.run,self.request,'summary')
        audit.capture(self.run,self.request,'delivery')
        with self.assertRaisesRegex(ValueError,'structured JSON'):
            audit.stage(self.run,'closed')

    def test_validation_needs_check_results(self):
        self.closeout_fixture()
        log=audit.events(self.run)
        latest={e['kind']:e for e in log if e['type']=='artifact'}
        f=self.base/'bad-validation.json'
        f.write_text(json.dumps(dict(run_id='test',draft_ref=latest['draft']['artifact_id'],approach_ref=latest['approach']['artifact_id'],checks=[])))
        audit.capture(self.run,f,'validation')
        audit.capture(self.run,self.request,'delivery')
        with self.assertRaisesRegex(ValueError,'actual check-result'):
            audit.stage(self.run,'closed')

if __name__=='__main__': unittest.main()
