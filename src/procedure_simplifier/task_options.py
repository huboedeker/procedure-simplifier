"""Explicit user-selectable task switches and compatibility checks."""
OPTIONS = {
    'wording': ('retain', 'plain', 'condensed'),
    'structure': ('preserve', 'reorganize', 'free'),
    'consolidation': (False, True),
    'process_redesign': (False, True),
    'requirement_reduction': ('none', 'evidence_based', 'assumption_based'),
    'format_fidelity': ('preserve', 'adapt', 'free'),
    'research': ('provided_only', 'approved_internal', 'public_and_approved_internal'),
    'clarification': ('material_gaps', 'stage_checkpoints'),
}

def validate_options(data):
    switches = data.get('switches')
    if not isinstance(switches, dict) or set(switches) != set(OPTIONS):
        raise ValueError('Task switches must explicitly contain all supported choices.')
    decisions = {d['id']: d for d in data['decisions']}
    for name, choices in OPTIONS.items():
        item = switches[name]
        if not isinstance(item, dict):
            raise ValueError('Each task switch needs a value and decision_ref.')
        value = item.get('value')
        if not any(type(value) is type(v) and value == v for v in choices):
            raise ValueError('Unselected or invalid task switch: '+name)
        if item.get('decision_ref') not in decisions:
            raise ValueError('Task switch needs a recorded decision: '+name)
    values = {k:v['value'] for k,v in switches.items()}
    if values['format_fidelity'] == 'preserve' and values['structure'] != 'preserve':
        raise ValueError('Preserved format conflicts with changed structure; clarify the task.')
    transforms = set()
    if values['wording'] != 'retain': transforms.add('language')
    if values['structure'] != 'preserve' or values['format_fidelity'] != 'preserve': transforms.add('presentation')
    if values['consolidation']: transforms.add('consolidation')
    if values['process_redesign']: transforms.add('process_redesign')
    if values['requirement_reduction'] != 'none': transforms.add('requirement_reduction')
    mode = 'outcome' if transforms & {'process_redesign', 'requirement_reduction'} else 'structure' if transforms & {'presentation', 'consolidation'} else 'language'
    if set(data['allowed_transformations']) != transforms or data['mode'] != mode:
        raise ValueError('Mode and transformation permissions must match selected task switches.')
    return values
