"""Offline JSON Schema checks against first-party fixtures."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'src/procedure_simplifier/framework'

def main():
    schemas={p.name:json.loads(p.read_text()) for p in (ASSETS/'schemas').glob('*.json')}
    for schema in schemas.values(): Draft202012Validator.check_schema(schema)
    pairs={'run-0.2.schema.json':'run.json','approach-0.8.0.schema.json':'approach.json','quality-0.8.0.schema.json':'quality.json','chunk-plan-0.8.0.schema.json':'chunk-plan.json'}
    for name,fixture in pairs.items():
        Draft202012Validator(schemas[name]).validate(json.loads((ASSETS/'examples/demo'/fixture).read_text()))
    old=copy.deepcopy(json.loads((ASSETS/'examples/demo/run.json').read_text()))
    old['schema_version']='0.1';old.pop('visual_review')
    Draft202012Validator(schemas['run-0.1.schema.json']).validate(old)
    common={'run_id':'fixture','draft_ref':'A_DRAFT','approach_ref':'A_TASK'}
    closeout={
      'summary-0.8.0.schema.json':dict(common,approach_summary='Synthetic',metrics={'status':'not_measured','reason':'Fixture'},major_omissions=[],additions=[],risks=[],visual_status='Fixture',review_status='Fixture',limitations=[]),
      'validation-0.8.0.schema.json':dict(common,checks=[{'name':'Synthetic','status':'passed','evidence':'Fixture only'}]),
      'delivery-0.8.0.schema.json':dict(common,status='proposal',artifact_refs=['A_DRAFT'],open_issues=[]),
      'learning-0.8.0.schema.json':dict(run_id='fixture',feedback_basis='Synthetic',target_skill_set='Fixture',overall_disposition='no_change',reason='Fixture',candidates=[]),
    }
    for name,fixture in closeout.items(): Draft202012Validator(schemas[name]).validate(fixture)
    for schema,template in [('run-0.2.schema.json','run.json'),('approach-0.8.0.schema.json','approach.json'),('quality-0.8.0.schema.json','quality.json'),('chunk-plan-0.8.0.schema.json','chunk-plan.json')]:
        if Draft202012Validator(schemas[schema]).is_valid(json.loads((ASSETS/'templates'/template).read_text())):
            raise ValueError('Incomplete template unexpectedly passed: '+template)
    print('PASS: nine schema definitions, nine supported fixture records, and four expected incomplete-template failures. Offline only.')

if __name__=='__main__':main()
