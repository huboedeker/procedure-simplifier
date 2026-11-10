"""Validate a recorded large-document execution plan; no agent dispatch."""
import argparse
import json
from pathlib import Path

def validate(plan):
    errors=[]
    if not isinstance(plan,dict): return ['Plan must be an object.']
    def need(value,message):
        if not value: errors.append(message)
    for key in ['run_id','task_ref','shared_context_ref','capacity_basis','estimation_method']:
        need(plan.get(key),'Missing '+key)
    cap=plan.get('context_budget',{})
    if not isinstance(cap,dict):return errors+['Context budget must be an object.']
    for k in ['window_tokens','reserved_tokens','safety_tokens']:
        need(type(cap.get(k)) is int and cap[k]>=0,'Invalid context budget: '+k)
    if errors:return errors
    available=cap['window_tokens']-cap['reserved_tokens']-cap['safety_tokens']
    need(available>0,'No usable packet capacity.')
    need(cap['reserved_tokens']>0 and cap['safety_tokens']>0,'Reserve working/output capacity and a positive safety margin.')
    strategy=plan.get('strategy')
    need(strategy in {'single','chunked_sequential','chunked_parallel'},'Invalid processing strategy.')
    parallel=plan.get('max_parallel')
    need(type(parallel) is int and parallel>=1,'Invalid concurrency limit.')
    need(type(plan.get('host_parallel_capacity')) is int and plan['host_parallel_capacity']>=1,'Record actual host concurrency capacity.')
    if errors:return errors
    need(parallel<=plan['host_parallel_capacity'],'Concurrency exceeds host capacity.')
    if strategy!='chunked_parallel':need(parallel==1,'Nonparallel strategy must use one worker at a time.')
    elements=plan.get('source_element_ids')
    if not isinstance(elements,list) or not elements or any(not isinstance(i,str) or not i for i in elements):
        return errors+['Source inventory needs nonempty element IDs.']
    need(len(elements)==len(set(elements)),'Duplicate source inventory IDs.')
    chunks=plan.get('chunks')
    if not isinstance(chunks,list) or not chunks or any(not isinstance(c,dict) for c in chunks):
        return errors+['Chunks must be nonempty objects.']
    byid={};owned={}
    def ids(item,key):
        xs=item.get(key)
        if not isinstance(xs,list) or any(not isinstance(i,str) or not i for i in xs):
            errors.append('Invalid ID list: '+key);return []
        need(len(xs)==len(set(xs)),'Duplicate IDs in '+key)
        return xs
    def estimate(item):
        n=item.get('packet_estimated_tokens')
        need(type(n) is int and 0<n<=available,'Packet or synthesis exceeds usable capacity or lacks estimate.')
    for c in chunks:
        cid=c.get('id')
        if not isinstance(cid,str) or not cid or cid in byid:
            errors.append('Missing or duplicate chunk ID.');continue
        byid[cid]=c
        for key in ['source_ref','boundary_rationale','task_ref','shared_context_ref']:
            need(c.get(key),'Chunk needs '+key)
        need(c.get('task_ref')==plan['task_ref'] and c.get('shared_context_ref')==plan['shared_context_ref'],'Worker task/shared context version mismatch.')
        primary=ids(c,'primary_ids');context=ids(c,'read_only_ids');ids(c,'depends_on')
        need(primary,'Chunk must own primary content.')
        need(not set(primary)&set(context),'Primary content duplicated as read-only in same chunk.')
        need(set(primary+context).issubset(set(elements)),'Unknown source element; external references belong in dependencies.')
        for eid in primary:owned.setdefault(eid,[]).append(cid)
        estimate(c)
    need(set(owned)==set(elements),'Source inventory coverage is incomplete.')
    need(all(len(v)==1 for v in owned.values()),'Primary source ownership must be unique.')
    if strategy=='single':need(len(chunks)==1,'Single processing must have one chunk.')
    for c in byid.values():
        deps=c.get('depends_on',[])
        if isinstance(deps,list):need(all(d in byid and d!=c['id'] for d in deps),'Unknown or self chunk dependency.')
    waves=plan.get('waves')
    if not isinstance(waves,list) or any(not isinstance(w,list) or any(not isinstance(x,str) for x in w) for w in waves):
        return errors+['Waves must be lists of chunk IDs.']
    done=set()
    for wave in waves:
        need(bool(wave) and len(wave)<=parallel,'Invalid wave size for concurrency cap.')
        need(len(wave)==len(set(wave)),'Duplicate chunk inside a wave.')
        for cid in wave:
            need(cid in byid and cid not in done,'Unknown or repeated chunk in waves.')
            if cid in byid and isinstance(byid[cid].get('depends_on'),list):
                need(set(byid[cid]['depends_on']).issubset(done),'Dependency must complete in an earlier wave; cycle or wrong sequence.')
        done.update(wave)
    need(done==set(byid),'Waves do not cover every chunk.')
    merges=plan.get('merges');coverage={cid:{cid} for cid in byid}
    if not isinstance(merges,list) or any(not isinstance(m,dict) for m in merges):
        return errors+['Merges must be a list of objects.']
    for m in merges:
        mid=m.get('id');inputs=ids(m,'input_ids')
        if not isinstance(mid,str) or not mid or mid in coverage:
            errors.append('Invalid or duplicate merge ID.');continue
        need(bool(inputs) and all(i in coverage for i in inputs),'Merge input must be a completed chunk or earlier merge.')
        estimate(m)
        coverage[mid]=set().union(*(coverage.get(i,set()) for i in inputs))
    final=plan.get('final_merge_id')
    need(final in coverage and coverage.get(final)==set(byid),'Final synthesis does not cover all chunks.')
    if strategy!='single':need(final not in byid,'Chunked processing requires a synthesis result.')
    need(plan.get('global_review_plan'),'Missing combined-document review plan.')
    return errors

def invalidated_chunks(plan, changed_ids=(), global_context_changed=False):
    if validate(plan): raise ValueError('Cannot invalidate an invalid chunk plan.')
    chunks=plan['chunks'];changed=set(changed_ids)
    if not changed.issubset(set(plan['source_element_ids'])):
        raise ValueError('Unknown changed source element.')
    affected={c['id'] for c in chunks if global_context_changed or changed & set(c['primary_ids']+c['read_only_ids'])}
    while True:
        more={c['id'] for c in chunks if set(c['depends_on']) & affected}
        if more.issubset(affected):break
        affected.update(more)
    return sorted(affected)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);a=p.parse_args()
    try:errors=validate(json.loads(a.plan.read_text()))
    except (OSError,ValueError,TypeError,KeyError) as exc:p.exit(2,str(exc)+'\n')
    if errors:p.exit(1,'\n'.join(errors)+'\n')
    print('PASS: recorded chunk coverage, sequencing, budgets and synthesis; semantic boundaries require review.')

if __name__=='__main__':main()
