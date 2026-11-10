"""Recorded completion checks; semantic accuracy still requires review."""
import json

def check_closeout(root, log):
    artifacts = {e['artifact_id']:e for e in log if e['type']=='artifact'}
    latest = {}
    for item in artifacts.values(): latest[item['kind']] = item
    required=['approach', 'draft', 'summary', 'learning', 'validation', 'delivery','review','changes','risk_assessment','quality']
    for kind in required:
        if kind not in latest: raise ValueError('Closeout requires '+kind)
    boundary = max(latest[k]['seq'] for k in ['approach','draft'])
    for kind in ['summary','learning','validation','delivery']:
        if latest[kind]['seq'] <= boundary:
            raise ValueError('Closeout artifact predates current approach/draft: '+kind)
    if latest['delivery']['seq'] < max(latest[k]['seq'] for k in ['summary','learning','validation']):
        raise ValueError('Delivery index must follow summary, learning and checks.')
    run_id = next(e['run_id'] for e in log if e['type']=='run_created')
    def record(kind):
        try:
            data=json.loads((root/latest[kind]['path']).read_text())
        except (ValueError,OSError):raise ValueError('Closeout needs structured JSON: '+kind)
        if not isinstance(data,dict) or data.get('run_id')!=run_id:
            raise ValueError('Invalid closeout record: '+kind)
        if data.get('draft_ref')!=latest['draft']['artifact_id'] or data.get('approach_ref')!=latest['approach']['artifact_id']:
            raise ValueError('Stale closeout artifact links: '+kind)
        return data
    summary=record('summary')
    for key in ['approach_summary','metrics','visual_status','review_status']:
        if not summary.get(key):raise ValueError('Summary needs '+key)
    for key in ['major_omissions','additions','risks','limitations']:
        if not isinstance(summary.get(key),list):raise ValueError('Summary needs an explicit list: '+key)
    metrics=summary['metrics']
    if not isinstance(metrics,dict) or metrics.get('status') not in {'measured','not_measured'}:
        raise ValueError('Summary needs a valid measurement status.')
    if metrics['status']=='not_measured' and not metrics.get('reason'):
        raise ValueError('Unmeasured reduction needs a reason.')
    if metrics['status']=='measured':
        if not metrics.get('method') or any(type(metrics.get(k)) is not int or metrics[k]<0 for k in ['source_words','output_words']):
            raise ValueError('Measured reduction needs method and non-negative word counts.')
    validation=record('validation')
    checks=validation.get('checks')
    if not isinstance(checks,list) or not checks:raise ValueError('Validation needs actual check-result records.')
    for check in checks:
        if not isinstance(check,dict) or not check.get('name') or check.get('status') not in {'passed','failed','incomplete'} or not check.get('evidence'):
            raise ValueError('Invalid validation result.')
    delivery=record('delivery')
    refs=delivery.get('artifact_refs')
    if not isinstance(refs,list) or any(latest[k]['artifact_id'] not in refs for k in required if k!='delivery'):
        raise ValueError('Delivery index lacks required artifact links.')
    if delivery.get('status') not in {'proposal','approved'}:
        raise ValueError('Delivery needs an explicit status.')
    if any(c['status']!='passed' for c in checks) and not delivery.get('open_issues'):
        raise ValueError('Failed or incomplete checks must be disclosed in delivery.')
    if delivery['status']=='approved':
        raise ValueError('Approved delivery requires the future integrated approval verification; close proposals only.')
    learning = json.loads((root/latest['learning']['path']).read_text())
    for field in ['run_id','feedback_basis','target_skill_set','overall_disposition','reason']:
        if not learning.get(field): raise ValueError('Learning record needs '+field)
    if learning['run_id'] != run_id: raise ValueError('Learning record belongs to another run.')
    if learning['overall_disposition'] not in {'applied','deferred','rejected','no_change','mixed'}:
        raise ValueError('Learning disposition is unresolved.')
    candidates = learning.get('candidates')
    if not isinstance(candidates,list): raise ValueError('Learning candidates must be a list.')
    applied = False
    statuses = []
    for candidate in candidates:
        if not isinstance(candidate,dict): raise ValueError('Invalid learning candidate.')
        for key in ['id','observation','decision','reason','evidence_refs']:
            if not candidate.get(key): raise ValueError('Learning candidate needs '+key)
        decision = candidate['decision']; statuses.append(decision)
        if decision not in {'applied','deferred','rejected'}:
            raise ValueError('Learning candidate has no final disposition.')
        for ref in candidate['evidence_refs']:
            if ref not in artifacts: raise ValueError('Unknown learning evidence artifact.')
        if decision == 'applied':
            applied = True
            for field,kind in [('before_refs','framework_before'),('after_refs','framework_after'),('review_refs','review'),('validation_refs','validation'),('rollback_refs','framework_before')]:
                refs = candidate.get(field)
                if not isinstance(refs,list) or not refs:
                    raise ValueError('Applied learning needs '+field)
                if any(ref not in artifacts or artifacts[ref]['kind'] != kind for ref in refs):
                    raise ValueError('Applied learning has invalid '+field)
    overall = learning['overall_disposition']
    if overall == 'no_change' and candidates:
        raise ValueError('No-change outcome cannot hide candidate decisions.')
    if overall != 'no_change' and not candidates:
        raise ValueError('Learning outcome needs candidate decisions.')
    if overall in {'applied','deferred','rejected'} and any(s != overall for s in statuses):
        raise ValueError('Overall learning disposition disagrees with candidates.')
    if applied and overall not in {'applied','mixed'}:
        raise ValueError('Applied learning must be visible in overall disposition.')
    return True
