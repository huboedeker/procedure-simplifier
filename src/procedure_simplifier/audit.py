"""Single-writer local run journal; integrity checks, not tamper-proof storage."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import importlib.util

_options_spec = importlib.util.spec_from_file_location('task_options', Path(__file__).with_name('task_options.py'))
_options_module = importlib.util.module_from_spec(_options_spec)
_options_spec.loader.exec_module(_options_module)
_closeout_spec = importlib.util.spec_from_file_location('closeout', Path(__file__).with_name('closeout.py'))
_closeout_module = importlib.util.module_from_spec(_closeout_spec)
_closeout_spec.loader.exec_module(_closeout_module)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()

def events(root):
    path = Path(root)/'events.jsonl'
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

def verify(root):
    root = Path(root)
    previous = '0'*64
    for seq, row in enumerate(events(root), 1):
        payload = {k:v for k,v in row.items() if k != 'hash'}
        if row.get('seq') != seq or row.get('previous') != previous or digest(encoded(payload)) != row.get('hash'):
            raise ValueError('Broken event chain.')
        previous = row['hash']
        if row['type'] == 'artifact':
            p = (root/row['path']).resolve()
            if not p.is_relative_to(root.resolve()) or digest(p.read_bytes()) != row['sha256']:
                raise ValueError('Missing or changed artifact: '+row['path'])
    return True

def append(root, event_type, **data):
    root = Path(root)
    verify(root)
    log = events(root)
    row = dict(seq=len(log)+1, timestamp=datetime.now(timezone.utc).isoformat(),
               type=event_type, previous=log[-1]['hash'] if log else '0'*64, **data)
    row['hash'] = digest(encoded(row))
    with (root/'events.jsonl').open('a') as f:
        f.write(json.dumps(row, ensure_ascii=False)+'\n')
    return row

KINDS = {'user_input', 'source', 'extraction', 'analysis', 'draft', 'review', 'changes', 'risk_assessment', 'comparison', 'validation', 'delivery', 'learning', 'approach', 'visual_source', 'visual_output', 'visual_brief', 'render_check', 'summary', 'framework_before', 'framework_after'}
KINDS.update({'quality','summary_text'})
KINDS.update({'processing_plan','chunk_analysis','chunk_draft','chunk_review','merge','coverage'})

def capture(root, source, kind, actor='coordinator', parents=None):
    root, source = Path(root), Path(source)
    if kind not in KINDS:
        raise ValueError('Unknown artifact kind.')
    verify(root)
    log = events(root)
    if kind in {'analysis', 'draft', 'review', 'changes', 'risk_assessment', 'comparison', 'delivery', 'visual_output', 'visual_brief', 'render_check', 'summary', 'framework_before', 'framework_after','quality','summary_text','chunk_analysis','chunk_draft','chunk_review','merge','coverage'}:
        approaches = [e for e in log if e['type']=='artifact' and e['kind']=='approach']
        if not approaches or any(e['type']=='artifact' and e['kind']=='user_input' and e['seq'] > approaches[-1]['seq'] for e in log):
            raise ValueError('Current recorded approach required before processing artifacts.')
    known = {e['artifact_id'] for e in log if e['type'] == 'artifact'}
    if not set(parents or []).issubset(known):
        raise ValueError('Unknown parent artifact.')
    aid = f'A{len(log)+1:05d}'
    target = root/'artifacts'/f'{aid}-{kind}{source.suffix}'
    target.parent.mkdir(exist_ok=True)
    blob = source.read_bytes()
    with target.open('xb') as f:
        f.write(blob)
    return append(root, 'artifact', artifact_id=aid, kind=kind, actor=actor,
                  path=str(target.relative_to(root)), sha256=digest(blob),
                  original_name=source.name, parents=parents or [])

def init(base, run_id, request):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', run_id):
        raise ValueError('Use a short run ID with letters, numbers, hyphens or underscores.')
    root = Path(base)/run_id
    root.mkdir(parents=True, exist_ok=False)
    append(root, 'run_created', run_id=run_id, actor='coordinator')
    capture(root, request, 'user_input')
    append(root, 'stage', stage='intake', actor='coordinator')
    return root

def set_approach(root, source):
    data = json.loads(Path(source).read_text())
    for key in ['objective', 'audience', 'scope', 'mode', 'allowed_transformations', 'format', 'non_negotiables', 'success_criteria', 'deliverables', 'decisions', 'gaps','output_role','decision_owner','adoption_authority','framework_version','skill_target']:
        if key not in data or (not data[key] and key not in {'non_negotiables', 'gaps'}):
            raise ValueError('Missing approach field: '+key)
    if data['mode'] not in {'language', 'structure', 'outcome'}:
        raise ValueError('Unknown approach mode.')
    if data['output_role'] not in {'explanatory_companion','proposed_replacement','formal_amendment'}:
        raise ValueError('Unknown intended output role.')
    known = {e['artifact_id'] for e in events(root) if e['type'] == 'artifact' and e['kind'] == 'user_input'}
    for d in data['decisions']:
        if not all(d.get(k) for k in ['id', 'choice', 'basis', 'input_refs']):
            raise ValueError('Decision needs ID, choice, basis and input references.')
        if d['basis'] not in {'explicit_user', 'authorized_default'} or not set(d['input_refs']).issubset(known):
            raise ValueError('Decision must reference recorded user input and a valid basis.')
    for gap in data['gaps']:
        if not all(k in gap for k in ['id', 'question', 'status', 'material', 'handling']):
            raise ValueError('Incomplete gap record.')
        if gap['material'] and gap['status'] != 'resolved':
            raise ValueError('Material approach gaps must be resolved before approach selection.')
    _options_module.validate_options(data)
    return capture(root, source, 'approach', parents=sorted(known))

def stage(root, name):
    if name not in {'intake', 'clarification', 'analysis', 'draft', 'review', 'revision', 'human_review', 'approved', 'learning', 'closed'}:
        raise ValueError('Unknown stage.')
    log = events(root)
    approaches = [e for e in log if e['type']=='artifact' and e['kind']=='approach']
    if name not in {'intake', 'clarification'}:
        if not approaches:
            raise ValueError('Select a recorded approach before processing.')
        # A new user instruction invalidates the gate until the approach is reconsidered.
        if any(e['type']=='artifact' and e['kind']=='user_input' and e['seq'] > approaches[-1]['seq'] for e in log):
            raise ValueError('New input requires an updated approach.')
    if name == 'approved':
        raise ValueError('Approval is a human decision against artifact hashes; use the documented approval process.')
    if name == 'closed':
        verify(root)
        _closeout_module.check_closeout(Path(root), log)
    return append(root, 'stage', stage=name, actor='coordinator')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='cmd', required=True)
    x=sub.add_parser('init'); x.add_argument('base'); x.add_argument('run_id'); x.add_argument('request')
    x=sub.add_parser('capture'); x.add_argument('root'); x.add_argument('kind', choices=sorted(KINDS-{'approach'})); x.add_argument('file'); x.add_argument('--actor', default='coordinator'); x.add_argument('--parents', nargs='*', default=[])
    x=sub.add_parser('approach'); x.add_argument('root'); x.add_argument('file')
    x=sub.add_parser('stage'); x.add_argument('root'); x.add_argument('name')
    x=sub.add_parser('verify'); x.add_argument('root')
    a=p.parse_args()
    try:
        if a.cmd=='init': print(init(a.base,a.run_id,a.request))
        elif a.cmd=='capture': print(json.dumps(capture(a.root,a.file,a.kind,a.actor,a.parents)))
        elif a.cmd=='approach': print(json.dumps(set_approach(a.root,a.file)))
        elif a.cmd=='stage': print(json.dumps(stage(a.root,a.name)))
        else: verify(a.root); print('PASS: event chain and artifact checksums.')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        p.exit(1, str(exc)+'\n')

if __name__=='__main__': main()
