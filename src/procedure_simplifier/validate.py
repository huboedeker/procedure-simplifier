"""Structural integrity checks. This does NOT establish semantic equivalence."""
import argparse
import json
import re
import sys
import hashlib
from pathlib import Path

TRANSFORMS = {'language', 'presentation', 'consolidation', 'process_redesign', 'requirement_reduction'}
STAGES = {'brief', 'analysis', 'clarification', 'draft', 'review', 'revision', 'human_review', 'approved'}


def statement_digest(run):
    return hashlib.sha256(json.dumps(run['statements'], sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode()).hexdigest()


def validate_visuals(run):
    errors = []
    visual = run.get('visual_review')
    if not isinstance(visual, dict):
        return ['Schema 0.2 requires a visual inventory and consistency review.']
    if visual.get('inventory_status') not in {'pending', 'complete', 'incomplete'} or not visual.get('scope'):
        errors.append('Visual inventory needs a scope and valid status.')
    pages = visual.get('pages_inspected')
    if not isinstance(pages, list) or any(type(p) is not int or p < 1 for p in pages):
        errors.append('Visual inventory needs valid inspected page numbers.')
    elif visual.get('inventory_status') == 'complete' and not pages:
        errors.append('Complete visual inventory needs inspected pages, including when no visuals are found.')
    issues = {i['id'] for i in run['issues'] if isinstance(i.get('id'), str)}
    def links(item, key):
        value = item.get(key)
        if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
            errors.append('Visual field must be an ID list: '+key)
            return []
        return value
    inventory_issues = links(visual, 'issues')
    if not set(inventory_issues).issubset(issues):
        errors.append('Unknown visual inventory issue.')
    if visual.get('inventory_status') != 'complete':
        if run['stage'] in {'human_review', 'approved'} and not inventory_issues:
            errors.append('Incomplete visual inventory must be surfaced as an issue.')
        if run['stage'] == 'approved':
            errors.append('Incomplete visual inventory prevents approval.')
    items = visual.get('items')
    if not isinstance(items, list) or any(not isinstance(i, dict) for i in items):
        return errors + ['Visual items must be a list of objects.']
    unit_ids = {u['id'] for u in run['units'] if isinstance(u.get('id'), str)}
    seen = set()
    for item in items:
        vid = item.get('id')
        if not isinstance(vid, str) or not vid or vid in seen:
            errors.append('Missing or duplicate visual ID.')
        else: seen.add(vid)
        for field in ['kind', 'meaning', 'rationale']:
            if not item.get(field): errors.append('Visual needs '+field)
        if type(item.get('page')) is not int or item['page'] < 1:
            errors.append('Visual needs source page locator.')
        if not set(links(item, 'source_unit_ids')).issubset(unit_ids):
            errors.append('Unknown visual source unit.')
        if not links(item, 'source_artifact_ids'):
            errors.append('Visual needs a source artifact reference.')
        output_ids = links(item, 'output_artifact_ids')
        item_issues = links(item, 'issue_ids')
        if not set(item_issues).issubset(issues): errors.append('Unknown visual issue.')
        disposition = item.get('disposition')
        if disposition not in {'retain', 'revise', 'replace', 'remove'}:
            errors.append('Invalid visual disposition.')
        consistency = item.get('consistency')
        if consistency not in {'consistent', 'conflict', 'unresolved', 'not_applicable'}:
            errors.append('Invalid visual consistency verdict.')
        if consistency == 'not_applicable' and disposition != 'remove':
            errors.append('Only removed visuals may use not_applicable consistency.')
        if item.get('production_status') not in {'proposed', 'produced'}:
            errors.append('Visual must distinguish proposed and produced outputs.')
        if disposition == 'remove' and output_ids:
            errors.append('Removed visual must not link an output visual.')
        if disposition == 'remove':
            handling = item.get('content_handling')
            if handling not in {'decorative', 'preserved_elsewhere', 'reduced'}:
                errors.append('Removed visual needs an explicit content disposition.')
            if handling == 'preserved_elsewhere' and not item.get('source_unit_ids'):
                errors.append('Preserved visual information needs mapped source units.')
            if handling == 'reduced' and 'requirement_reduction' not in run['brief'].get('allowed_transformations', []):
                errors.append('Visual content reduction is outside the mandate.')
        if disposition != 'remove' and item.get('production_status') == 'produced' and not output_ids:
            errors.append('Produced or retained visual needs actual output artifact references.')
        if consistency in {'consistent', 'not_applicable'} and item.get('reviewed_text_sha256') != statement_digest(run):
            errors.append('Visual consistency check is stale or missing a text digest.')
        pending = consistency not in {'consistent', 'not_applicable'} or item.get('production_status') != 'produced'
        if pending and run['stage'] in {'human_review', 'approved'} and not item_issues:
            errors.append('Pending visual work must be surfaced as an issue.')
        if pending and run['stage'] == 'approved': errors.append('Pending or inconsistent visuals prevent approval.')
    return errors


def validate(run):
    errors = []
    if not isinstance(run, dict):
        return ['Run must be an object.']
    required = {'schema_version', 'run_id', 'stage', 'source', 'brief', 'context', 'units',
                'statements', 'changes', 'issues', 'review', 'approvals'}
    missing = required - run.keys()
    if missing:
        return ['Missing fields: ' + ', '.join(sorted(missing))]
    for field in ['source', 'brief', 'review']:
        if not isinstance(run[field], dict):
            errors.append(f'{field} must be an object.')
    for field in ['context', 'units', 'statements', 'changes', 'issues', 'approvals']:
        if not isinstance(run[field], list) or any(not isinstance(x, dict) for x in run[field]):
            errors.append(f'{field} must be a list of objects.')
    if errors:
        return errors
    if run['schema_version'] not in {'0.1', '0.2'}:
        errors.append('Unsupported schema version.')
    if not run['run_id'] or run['stage'] not in STAGES:
        errors.append('Missing run ID or invalid stage.')
    if not re.fullmatch(r'[a-f0-9]{64}', str(run['source'].get('sha256', ''))):
        errors.append('Source SHA-256 missing or invalid.')
    if not run['units'] or not run['statements']:
        errors.append('Source units and output statements must not be empty.')
    allowed = run['brief'].get('allowed_transformations', [])
    if not isinstance(allowed, list) or any(x not in TRANSFORMS for x in allowed):
        errors.append('Invalid transformation permissions.')
        allowed = []

    def index(field):
        result = {}
        for item in run[field]:
            key = item.get('id')
            if not isinstance(key, str) or not key or key in result:
                errors.append(f'{field}: missing/duplicate ID {key!r}.')
                continue
            result[key] = item
        return result

    units, statements, context, issues = [index(f) for f in ['units', 'statements', 'context', 'issues']]
    def refs(item, field, label):
        value = item.get(field)
        if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
            errors.append(f'{label}: {field} must be a list of IDs.')
            return []
        if len(value) != len(set(value)):
            errors.append(f'{label}: duplicate {field}.')
        return value

    for uid, u in units.items():
        if not u.get('quote') or not isinstance(u.get('page'), int) or u['page'] < 1:
            errors.append(f'{uid}: missing quote/page evidence.')
        if u.get('kind') not in {'informative', 'recommendation', 'mandatory', 'domain_binding', 'permission', 'exception'}:
            errors.append(f'{uid}: invalid source classification.')
        for key in ['actor', 'force', 'protected_details', 'assessment']:
            if not u.get(key):
                errors.append(f'{uid}: missing {key}.')
        for dep in refs(u, 'dependencies', uid):
            if dep not in units and dep not in context:
                errors.append(f'{uid}: unknown dependency {dep}.')

    for sid, s in statements.items():
        source_ids = refs(s, 'source_ids', sid)
        if not s.get('text'):
            errors.append(f'{sid}: empty statement.')
        if not source_ids and s.get('addition') is not True:
            errors.append(f'{sid}: unsupported statement is not marked as an addition.')
        if s.get('addition') is True and not s.get('rationale'):
            errors.append(f'{sid}: addition requires rationale.')
        if s.get('addition') is True and not ({'process_redesign', 'requirement_reduction'} & set(allowed)):
            errors.append(f'{sid}: substantive addition outside preservation mandate.')
        for uid in source_ids:
            if uid not in units:
                errors.append(f'{sid}: unknown source {uid}.')

    seen = set()
    for c in run['changes']:
        uid = c.get('unit_id')
        if not isinstance(uid, str):
            errors.append('Change has invalid unit ID.')
            continue
        if uid not in units or uid in seen:
            errors.append(f'{uid}: unknown or repeated change disposition.')
        seen.add(uid)
        outputs = refs(c, 'output_ids', uid)
        if c.get('disposition') not in {'retained', 'reworded', 'moved', 'merged', 'removed'}:
            errors.append(f'{uid}: invalid disposition.')
        if c.get('transformation') not in allowed:
            errors.append(f'{uid}: transformation outside mandate.')
        if not isinstance(c.get('substantive'), bool) or not c.get('rationale'):
            errors.append(f'{uid}: substantive flag and rationale required.')
        if c.get('substantive') and not ({'process_redesign', 'requirement_reduction'} & set(allowed)):
            errors.append(f'{uid}: substantive change outside mandate.')
        if c.get('disposition') == 'removed':
            if outputs:
                errors.append(f'{uid}: removed unit still has output links.')
            if units.get(uid, {}).get('kind') != 'informative':
                if c.get('substantive') is not True or 'requirement_reduction' not in allowed:
                    errors.append(f'{uid}: requirement removal must be substantive and permitted.')
        elif not outputs:
            errors.append(f'{uid}: retained content has no output.')
        for sid in outputs:
            if sid not in statements or uid not in refs(statements[sid], 'source_ids', sid):
                errors.append(f'{uid}: broken output backlink {sid}.')
    for uid in units.keys() - seen:
        errors.append(f'{uid}: no change disposition.')
    for sid, s in statements.items():
        for uid in refs(s, 'source_ids', sid):
            if not any(c.get('unit_id') == uid and sid in c.get('output_ids', []) for c in run['changes'] if isinstance(c.get('output_ids'), list)):
                errors.append(f'{sid}: source link lacks reciprocal change entry for {uid}.')

    review = run['review']
    if run['stage'] in {'human_review', 'approved'}:
        if review.get('status') != 'completed' or not review.get('reviewer'):
            errors.append('Independent review not recorded as completed.')
        if not isinstance(review.get('findings'), list):
            errors.append('Review findings must be a list.')
        else:
            for f in review['findings']:
                if not isinstance(f, dict) or f.get('status') not in {'resolved', 'escalated'}:
                    errors.append('Review finding must be resolved or explicitly escalated.')
    if run['stage'] == 'approved':
        if run['brief'].get('approval_status') != 'approved' or not run['approvals']:
            errors.append('Explicit human mandate and version approval required.')
        for approval in run['approvals']:
            if not all(approval.get(k) for k in ['approver','authority_basis','decision','timestamp','scope','artifact_sha256']):
                errors.append('Approval requires identity, authority, decision, time, scope and artifact hash.')
            if approval.get('decision') != 'approve' or not re.fullmatch(r'[a-f0-9]{64}',str(approval.get('artifact_sha256',''))):
                errors.append('Invalid adoption approval decision or artifact hash.')
        if any(q.get('blocking') and q.get('status') != 'resolved' for q in issues.values()):
            errors.append('Blocking issues prevent approval.')
        if any(c.get('substantive') and c.get('approval_status') != 'approved' for c in run['changes']):
            errors.append('Substantive changes require explicit approval.')
        if any(isinstance(f, dict) and f.get('status') != 'resolved' for f in review.get('findings', [])):
            errors.append('Unresolved review findings prevent approval.')
    if run['schema_version'] == '0.2' or 'visual_review' in run:
        errors.extend(validate_visuals(run))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.run.read_text()))
    except (OSError, json.JSONDecodeError) as exc:
        print(f'Cannot read run: {exc}', file=sys.stderr)
        return 2
    if errors:
        print('\n'.join('FAIL: ' + e for e in errors))
        return 1
    print('PASS: structural integrity. Semantic equivalence and human approval are separate checks.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
