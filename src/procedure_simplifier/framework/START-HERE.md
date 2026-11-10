# Operating entry point — v0.8.0

At intake apply LARGE-DOCUMENTS.md: assess available context, build a source-owned chunk/dependency plan where needed, choose sequential or bounded parallel work, and reserve capacity for synthesis and final review. Validate the recorded plan with src/procedure_simplifier/chunks.py before dispatch. The coordinating host executes this plan; automatic dispatch remains future work.

The framework has four roles and one effective task definition. These documents govern an agent-operated run:

1. TASK-DEFINITION.md + templates/approach.json: intended use, scope, switches and decision provenance.
2. AUDIT-CONTRACT.md: one run location, inputs, immutable artifact copies and journal.
3. QUALITY-CONTROLS.md + templates/quality.json: independent completeness, meaning scenarios, dependencies, reductions and delivered-version checks.
4. VISUAL-CONSISTENCY.md: figures and graph/diagram meaning.
5. WORKFLOW.md + agents/: analysis, drafting, independent review and revision.
6. CLOSEOUT-AND-LEARNING.md: result summary, decisions, learning integration and completion.
7. EVALUATION-PROTOCOL.md: test quality on unseen cases and readers.

Run src/procedure_simplifier/validate.py on the transformation record, src/procedure_simplifier/quality.py on the quality record and delivery file, and src/procedure_simplifier/audit.py verify on the journal. The closed stage checks structured handover records. These are complementary checks, not a single autonomous workflow. The coordinating host executes and records the actual work.

Template approach fields, unit IDs and artifact references must be populated from real evidence. Templates are deliberately incomplete. New local quality checks do not certify historical pilots. Integrated role dispatch, automatic propagation/version invalidation and end-to-end evaluation remain future work.
