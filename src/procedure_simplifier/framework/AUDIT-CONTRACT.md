# Run approach and audit contract — v0.8.0

LARGE-DOCUMENTS.md adds processing_plan, chunk_analysis, chunk_draft, chunk_review, merge and coverage artifact kinds. The coordinator is the single journal writer; parallel agents write separate assigned directories and return artifact references. Record chunk/dependency versions, dispatches, failures/retries, merge lineage and review coverage. Global summaries count unique source ownership rather than duplicated overlap.

Version 0.6 uses structured summary/validation/delivery records and adds the quality artifact and readable summary_text. See QUALITY-CONTROLS.md and CLOSEOUT-AND-LEARNING.md for the current local checks. Historical prose closeout fixtures must not be treated as complete under the newer contract.

CLOSEOUT-AND-LEARNING.md adds the closing summary and learning-integration record to every delivery. Register skill/framework before/after snapshots and update review/check evidence when changes are applied. `stage ... closed` checks these records without implying policy approval.

VISUAL-CONSISTENCY.md adds source/output visual assets, modification briefs, render checks and consistency verdicts to the audit trail. Capture these with the corresponding artifact kinds and parent references; include pending visual changes in delivery.

The approach is the task definition. TASK-DEFINITION.md specifies its independently selectable switches, provenance, profiles and compatibility rules; all switches must be resolved and recorded before the approach gate passes.

## One defined location

The coordinator chooses and reports an absolute audit base at intake. Default: `./runs/<run-id>/` under the working directory; choose a writable location outside the installed package. Each run has its own directory; a later approach or comparison run references its predecessor rather than overwriting it. The user may specify another destination at intake.

```
runs/<run-id>/
  events.jsonl                 chronological flow and artifact inventory
  artifacts/
    A00002-user_input.txt      exact user request
    A00004-source.pdf          source snapshot
    A00005-approach.json       approach, decision log and gap register
    ...-analysis.json          source map, assumptions and interpretation
    ...-draft.md               each saved revision
    ...-review.md              independent findings and rechecks
    ...-changes.json           unit-level dispositions
    ...-risk_assessment.md     omissions, assumptions and consequences
    ...-validation.txt         actual check results
    ...-delivery.md            human-readable run index and status
```

Names are illustrative; IDs follow event sequence. Files are copied into new artifact paths with original filename, actor, timestamp, checksum and parent artifact references in the journal. Never overwrite a registered file. Correct a mistake by adding a new revision and documenting what it supersedes. Preserve actual messages and author identity; never label an agent interpretation as user input or approval.

## Decide before processing

At intake, record the request and inventory sources. Establish:

- Intended outcome, audience and selected document scope.
- Mode: language simplification, content-preserving structural redesign, or outcome-focused reduction.
- Allowed transformations, protected requirements, format freedom and acceptance criteria.
- Expected deliverables and audit destination.
- Decisions and their basis: explicit user instruction or an authorized, stated default.
- Missing information, questions, materiality and handling.

Use existing user instructions; do not ask again for settled choices. Ask about material uncertainty in the objective, permitted losses, protected constraints or scope before doing affected work. Research can resolve factual source questions; user intent and risk choices require user answers. Unresolved nonmaterial issues may proceed with an explicit assumption and review flag. Source gaps can remain open for an exploratory proposal when the agreed approach permits it; that permission and the adoption limitation must be recorded. Intake, extraction and question preparation may continue while the approach is unsettled.

Save a dated approach revision before analysis/drafting. User steering later in the run is a new input: record it, revise the approach and log its impact before dependent processing resumes. Approval to explore a redesign is distinct from approval to adopt its results.

## Every handoff and decision

Record who acted, when, why, input artifact IDs, output artifact IDs and disposition. Log stage starts/completions, clarification requests and answers, research provenance, agent handoffs, review cycles, failed checks, retries and escalations. For narrative flow events use `append()` from the journal module with explicit event types and input/output references. Stage events alone do not document the work inside a stage.

The approach snapshot contains the decision/gap log at that point. Later decisions require a new snapshot. Preserve source-to-output mappings, reduction rationales, risk findings and review resolutions. Exact source units and their original locators remain necessary in addition to file hashes.

At handover, create `delivery` with links/IDs to the effective approach, source inventory, latest draft, analysis, change/risk records, independent review, validation results and unresolved decisions. Identify superseded drafts. State proposal/approval status and required next decisions. Human approvals must name the approver, decision, time and exact artifact hash/version; never fabricate them. An approved version can remain historically approved while later revisions need their own approval.

## Local support and limits

`src/procedure_simplifier/audit.py` initializes runs, captures artifacts, saves approach decisions, logs stages and verifies checksums and event chaining. It blocks processing artifacts until an approach is recorded, and invalidates that gate after new user input. It rejects unresolved material approach gaps. Use it with `src/procedure_simplifier/validate.py`, which checks the document transformation records.

This is single-writer local storage. The hash chain detects accidental changes against the retained journal; it is not an independently anchored, tamper-proof archive. Role calls, questions, decisions and narrative flow must still be recorded by the coordinator. Completeness and human authority are reviewed against this contract; the utility does not automatically prove them. Multi-writer locking, signed approvals, access control and automatic host integration remain future work.

Historical cases must not be backfilled with invented audit events.
