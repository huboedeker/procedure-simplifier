# Workflow and data contract — v0.8.0

LARGE-DOCUMENTS.md adds context-capacity planning before analysis, semantic chunk ownership, dependency sequencing, optional parallel role instances, bounded hierarchical synthesis and combined-document review. Record execution strategy under `processing` in the task and save the full plan as a processing_plan audit artifact. Chunk/merge results remain source-linked and versioned; overlapping context is not counted twice.

START-HERE.md is the operational entry point. QUALITY-CONTROLS.md requires independent original-source reconciliation, semantic scenarios, cross-document dependency checks, substantive-change impact cards and review of the actual exported version. EVALUATION-PROTOCOL.md defines evaluation and learning-regression challenges.

CLOSEOUT-AND-LEARNING.md requires a closing summary and a completed learning-integration disposition for every run. The summary states approach, measured reduction, major omissions/additions, risks, visuals and review limitations. Justified reusable improvements are applied, reviewed, versioned and checked; deferred/rejected/no-change outcomes are explicit.

VISUAL-CONSISTENCY.md governs visual inventory, visual-only meaning, text/figure consistency, modification and independent review. New transformation records use schema 0.2 with a required visual review; historical schema 0.1 records remain supported without a retrospective visual-check claim.

TASK-DEFINITION.md makes the user-selectable switches explicit in the saved approach. Derived mode and permissions must agree with them, and all agent handoffs use the same effective task definition.

AUDIT-CONTRACT.md governs intake, approach selection, decision provenance, the defined run directory and versioned artifact/flow records. Use its journal alongside the transformation record below.

## Mandate

Record audience, purpose, source inventory, scope, excluded sections, source hierarchy, transformation permissions and format constraints. Permissions are independent: language, presentation, consolidation, process redesign, requirement reduction. A proposal is not approval. Record whether each mandate choice came from the user or is a provisional default.

Default: preserve substantive obligations; preserve source identifiers; permit clearer wording and navigational structure; no implied authority to retire controls. Format constraints and target reduction are preferences, never reasons to silently drop meaning.

## Stages and gates

1. `brief`: record user input and sources at the defined run location; select and save the approach. Clarify material approach gaps before dependent work; log authorized defaults and nonmaterial assumptions. Reconsider the approach after new user steering.
2. `analysis`: verify extraction against relevant pages; separate informative intent, mandatory content, domain provisions, exceptions and source instructions. Capture source units at independently reviewable statement granularity. Lists may remain together only when their members are explicit protected details of one action.
3. `clarification`: consolidate questions. Research only factual gaps using appropriate authorized sources; log provenance. Ask the user about intent and authority. Continue unaffected work. Do not silently resolve ambiguity.
4. `draft`: map every source unit to an output statement or an explicit disposition. Record actor, force, conditions, timing, protective function, burden, dependencies and uncertainty. Mark unsupported new statements as proposed additions.
5. `review`: independent reviewer first assesses source and draft without author's rationale; then compares the ledger. Findings carry severity, affected IDs, evidence, repair and status.
6. `revision`: preserve the previous draft and review findings; allow two review/revision cycles, then escalate unresolved conflicts.
7. `human_review`: validation passes; all findings are resolved or explicitly surfaced. Produce the closing summary alongside the text and delivery index. Open issues may accompany a clearly provisional draft. They cannot be hidden behind a release claim.
8. `approved`: record explicit owner approval and decisions on blocking issues. Approval is scoped to a particular version and checksum. Publication/effectiveness is a separate action.
9. `learning`: assess available evidence/feedback, classify case-specific versus reusable observations, and record candidate decisions. Apply justified improvements to the identified framework/skill target with review, before/after versions, rollback and relevant checks. Document deferred/rejected/no-change outcomes; never infer policy adoption approval from silence. Learning can occur at proposal handover even when policy approval is pending.
10. `closed`: update the summary and delivery index, capture learning outcome and checks, and verify audit integrity. Closing a handover does not approve the proposed document.

## Required run fields

See `templates/run.json` and the populated example. JSON records are intentionally small and readable.

- `source`: document identity, version, file checksum, selected sections, pages and unavailable references.
- `brief`: audience, objective, allowed transformations, formatting, provenance of mandate, approval status.
- `units`: unique ID, source page and verbatim quote, classification, actor, force, protected details, dependency IDs, assessment.
- `statements`: unique output ID, text, source IDs (or explicit addition marker).
- `changes`: exactly one disposition for each source unit, linked output IDs, transformation class, substantive flag, rationale, approval status.
- `issues`: unresolved matters, blocking flag and handling decision.
- `review`: status, reviewer identity/context, findings with resolutions.
- `approvals`: explicit human decisions only; never fabricated.
- `visual_review`: inspected scope/pages, visual inventory, source/output links, disposition, consistency verdict tied to the current text digest, and open modification issues. Check visuals again after relevant revisions; see VISUAL-CONSISTENCY.md.

Meaning checks are performed by agents and humans. The validator enforces identifiers, coverage, links, permission compatibility and basic approval gates. It cannot detect an omitted condition hidden inside a rewritten sentence. Preserve protected details in the record to make that review possible.

## Acceptance

Preservation mode: no known unauthorized substantive change; all source units accounted for; actor, force, scope, conditions, timing, exceptions and lists preserved; no new unsupported duties. Redesign mode: every substantive change labeled with consequences, dependencies, authority and decision status. Both modes: readable review package, explicit unresolved issues and independent review history.
