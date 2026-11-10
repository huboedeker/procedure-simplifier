"""Validate recorded quality evidence; does not replace independent inspection."""
import argparse
import hashlib
import json
from pathlib import Path

def statement_digest(run):
    return hashlib.sha256(json.dumps(run['statements'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def validate(record, run, base):
    errors=[]
    def need(value, message):
        if not value: errors.append(message)
    need(record.get('run_id')==run.get('run_id'),'Quality record belongs to another run.')
    for key in ['effective_task_artifact','independent_reviewer']:
        need(record.get(key),'Missing '+key)
    need(record.get('reviewed_statement_sha256')==statement_digest(run),'Quality review is stale against statement record.')
    def file_hash(path, expected):
        try:
            actual=hashlib.sha256((base/path).read_bytes()).hexdigest()
            need(actual==expected,'Artifact hash mismatch: '+str(path))
        except (OSError,TypeError): errors.append('Missing readable artifact: '+str(path))
    file_hash(record.get('delivered_file',''),record.get('delivered_sha256'))
    file_hash(record.get('effective_task_file',''),record.get('effective_task_sha256'))
    try:
        task=json.loads((base/record.get('effective_task_file','')).read_text())
        need(set(task.get('allowed_transformations',[]))==set(run['brief']['allowed_transformations']),'Task and transformation permissions disagree.')
    except (OSError,ValueError,TypeError):errors.append('Missing readable effective task definition.')
    units={u['id'] for u in run['units']}
    blocks=record.get('source_manifest',[])
    need(bool(blocks),'Missing independent source manifest.')
    mapped=set()
    for block in blocks:
        for field in ['id','source_file','source_sha256','locator','expected_content','disposition']:
            need(block.get(field),'Manifest block needs '+field)
        file_hash(block.get('source_file',''),block.get('source_sha256'))
        ids=set(block.get('unit_ids',[]));mapped.update(ids)
        need(ids.issubset(units),'Manifest refers to missing source units.')
        need(block.get('disposition') in {'mapped','informative','decorative','excluded'},'Invalid source disposition.')
        if block.get('disposition')=='mapped': need(ids,'Mapped block has no units.')
    need(units.issubset(mapped),'Source units missing manifest links.')
    need(run['source']['sha256'] in {b.get('source_sha256') for b in blocks},'Manifest does not include the primary source version.')
    obligation_ids=set()
    for item in record.get('obligation_details',[]):
        need(item.get('unit_id') in units,'Obligation details reference missing units.')
        obligation_ids.add(item.get('unit_id'))
        for field in ['actor','action','force','trigger','scope','exceptions','timing','evidence','authority']:
            need(item.get(field),'Obligation details need '+field+' (use an explicit unknown where necessary).')
    required={u['id'] for u in run['units'] if u.get('kind')!='informative'}
    need(required.issubset(obligation_ids),'Missing structured obligation details.')
    need(record.get('completeness_status') in {'complete','incomplete'},'Independent source check not completed.')
    if record.get('completeness_status')=='incomplete': need(record.get('open_issues'),'Incomplete source check needs an open issue.')
    scenarios=record.get('scenarios',[])
    need(scenarios,'Missing semantic scenario evidence.')
    for s in scenarios:
        for key in ['id','unit_ids','situation','source_behavior','output_behavior','verdict','evidence']:
            need(s.get(key),'Scenario needs '+key)
        need(set(s.get('unit_ids',[])).issubset(units),'Scenario references missing units.')
        need(s.get('verdict') in {'match','intentional_change','unresolved'},'Invalid scenario verdict.')
        if s.get('verdict')=='unresolved':need(record.get('open_issues'),'Unresolved scenario needs an open issue.')
        if s.get('verdict')=='intentional_change':
            need(bool({'process_redesign','requirement_reduction'} & set(run['brief']['allowed_transformations'])),'Intentional semantic change outside mandate.')
    card_units=set()
    for c in record.get('reduction_cards',[]):
        for key in ['id','unit_ids','benefit_hypothesis','basis','evidence_or_assumption','lost_safeguard','affected_parties','dependency_impact','replacement','owner','burden_shift','disproof_test','risk_and_confidence','decision']:
            need(c.get(key),'Reduction card needs '+key)
        ids=set(c.get('unit_ids',[]));card_units.update(ids)
        need(ids.issubset(units),'Reduction card references missing units.')
        need(c.get('basis') in {'evidence','assumption'},'Invalid reduction evidence basis.')
    for c in run['changes']:
        if c.get('substantive'):need(c['unit_id'] in card_units,'Substantive change lacks a reduction/impact card: '+c['unit_id'])
    dependencies=record.get('dependencies')
    need(isinstance(dependencies,list),'Dependency register must be a list (explicitly empty if checked and none).')
    if isinstance(dependencies,list):
        for d in dependencies:
            for field in ['id','direction','source','version','status','impact']:
                need(d.get(field),'Dependency needs '+field)
            need(d.get('status') in {'checked','missing','unresolved'},'Invalid dependency status.')
            if d.get('status')!='checked':need(record.get('open_issues'),'Missing dependency needs an open issue.')
    export=record.get('export_check',{})
    need(export.get('status') in {'passed','incomplete','failed'} and export.get('evidence'),'Missing delivered-format inspection evidence.')
    if export.get('status')!='passed':need(record.get('open_issues'),'Incomplete export check needs an open issue.')
    if run.get('stage')=='approved':
        need(record.get('completeness_status')=='complete' and not record.get('open_issues') and export.get('status')=='passed','Unresolved quality issues prevent adoption approval.')
        need(bool(run.get('approvals')) and all(a.get('artifact_sha256')==record.get('delivered_sha256') for a in run.get('approvals',[])),'Approval does not identify the delivered artifact.')
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('quality',type=Path);p.add_argument('run',type=Path);a=p.parse_args()
    try:
        errors=validate(json.loads(a.quality.read_text()),json.loads(a.run.read_text()),a.quality.parent)
    except (OSError,ValueError,TypeError,KeyError) as exc:p.exit(2,str(exc)+'\n')
    if errors:p.exit(1,'\n'.join(errors)+'\n')
    print('PASS: recorded quality evidence and file hashes; semantic judgments require inspection.')

if __name__=='__main__':main()
