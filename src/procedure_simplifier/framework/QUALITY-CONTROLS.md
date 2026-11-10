# Quality controls before workflow integration — v0.8.0

For large inputs, apply LARGE-DOCUMENTS.md before analysis. Reconcile original-source completeness against the global inventory across all chunks. Add cross-boundary scenarios and combined-artifact checks; local chunk passes do not certify the whole. Capacity estimates and processing-plan validation are recorded evidence, not proof of semantic completeness.

These controls apply to agent-operated runs now. They do not depend on an orchestration service. Start at START-HERE.md and use `templates/quality.json` alongside the task and transformation records. Actual inspection, semantic judgment and user tests remain agent/human work; local validation checks the recorded evidence and its consistency.

## Intake: intended use and authority

Record whether the output is an explanatory companion, a proposed replacement, or a formal amendment; record intended readers, decision owner, adoption authority, protected constraints and the active framework version. Determine acceptance criteria for the selected mode. Exploratory omission may remain hypothetical if disclosed; a preservation claim requires no known unauthorized meaning change. No mode overrides a protected requirement.

## Independent source completeness

Create a source manifest from the original sources: file version/hash, selected ranges, headings, paragraphs, definitions, tables, rows, footnotes, attachments, figures and references. Record missing/unreadable materials and scope exclusions. At independently reviewable block granularity, record a locator, what the block contains, and mapped source-unit IDs or an explicit informative/decorative/excluded disposition. Several requirements can occur within one block; distinguish their protected details.

Use `templates/quality-components.json` for block, obligation, scenario, dependency and reduction-card shapes. These are blank record components, not evidence. Each noninformative source unit needs structured obligation details; compound units retain their distinct protected conditions and list members.

The reviewer first inspects the original relevant pages without the analyst's map, records their own expected elements, then reconciles them to the manifest and source-unit inventory. Resolve omissions or surface incomplete coverage as an issue. Do not infer completeness merely from a full source-ID/output-ID map. Hash and version the reconciled manifest. The local checker can detect a mapped unit disappearing later; it cannot prove the manifest was originally complete.

## Meaning and scenarios

Source-unit kinds include `recommendation` for method advice. Preserve and assess the advice's actual force/context without elevating it to institutional authority. Recommendations still need source coverage, structured action details, review and explicit reduction decisions; they are not exempt from traceability.

For each important obligation, record actor, action, force, trigger, scope, exception, timing, evidence and approval authority; use explicit unknowns instead of invention. For visual-only content, record a faithful observation and source locator, distinguishing it from a verbatim quotation. Link it to the actual visual/source-page artifact.

Derive normal, exception and failure scenarios from the source independently of the draft. Compare expected source behavior to output behavior. In preservation mode, differences must be repaired or escalated. In reduction mode, intended differences must match the reduction decision, risk record and protected constraints. Check negation, must/may/should, every/any, and numeric thresholds explicitly. List applicable scenarios rather than forcing irrelevant categories for every sentence.

## Dependencies and factual resolution

Record inbound/outbound dependencies, definitions, precedence, applicable versions and referenced external rules. Check the proposed changes against this graph, including requirements outside the selected section. Distinguish sources consulted from sources merely cited by the document. Log actual provenance, relevant passages, uncertainty and access failures. Missing evidence never becomes a positive finding of redundancy.

## Reduction decision card

For every substantive removal, weakening or replacement record: source units; intended benefit; value hypothesis; evidence or assumption; lost protective function; affected parties; dependency impact; substitute control; accountable owner; added or shifted burden; a scenario that would disprove the hypothesis; risk judgment and confidence; decision status. Evidence-based reductions require supporting evidence; assumption-based reductions may be proposals pending validation. Unresolved high-consequence assumptions must remain visible, with adoption deferred where appropriate. No arbitrary risk score automatically permits deletion.

## Check the delivered version

Review the actual exported document/visuals, not just the JSON statements. Bind semantic review, quality results, summary and any adoption approval to its hash and effective task revision. Recheck affected work after a change. Local quality validation reads the actual delivery file and checks its hash. It also binds evidence to the canonical statement digest so a record change invalidates the check. It cannot prove that the export faithfully represents the record; explicitly review that comparison.

Use structured validation/summary/delivery records for the journal completion gate. Their schemas are described in src/procedure_simplifier/closeout.py and the templates. A record of a failed or incomplete check may accompany an explicitly flagged proposal; it cannot claim PASS. Adoption approvals require identity, authority basis, time, scope, decision and exact artifact hash; permission to draft is not adoption approval.

The local quality record stores `effective_task_file` and `effective_task_sha256` as well as the audit artifact ID. Its checker verifies task/file hashes and transformation-permission agreement. The remaining task constraints require substantive review; automatic propagation through every agent call remains future work.

## Evaluate quality and promote learning

Use EVALUATION-PROTOCOL.md before claiming general reliability. Test source completeness, semantic detection, legitimate reductions, visuals, final rendering, reader performance and document-borne instruction attacks. Maintain held-out cases when changing reusable instructions. Compare before/after outcomes, confirm the reviewed version is active, and preserve rollback. Candidate learning that helps one case but damages another must be revised or deferred.

## Local check

`procedure-simplifier quality /absolute/path/quality.json /absolute/path/run.json`

File paths in quality records resolve relative to that record's directory; use portable relative references where practical. Hash checks bind evidence; they do not certify the truth of the inspection. Preserve the record as a `quality` audit artifact. Historical pilots remain unchanged and have not retroactively satisfied these controls.
