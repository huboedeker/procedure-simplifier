# Closing summary and learning integration — v0.8.0

For chunked processing include execution strategy, chunk/worker count, synthesis levels, failed/retried work and global review coverage in the summary. Disclose capacity/estimation uncertainty and unresolved boundaries. Learning updates during a run must trigger explicit instruction-version reconciliation under LARGE-DOCUMENTS.md; otherwise apply them after the affected synthesis/review. Never silently combine worker results produced under incompatible global definitions.

Every run produces a concise closing summary for manual review and a learning-integration record. Both are baseline deliverables, independent of the selected simplification switches. Closing a run means its handover and learning disposition are documented; it does not mean the proposed policy was approved.

## Closing summary

Use `templates/closing-summary.md`. Present the summary alongside the modified document and link it from the delivery index. Include:

1. **Approach:** objective, audience, scope, selected switches and any changes to the initial mandate. Distinguish preservation from intentional content reduction.
2. **Measured result:** source/output word counts and percentage change, exact counting scope/method, baseline and output artifact IDs/hashes. Include previous-pass comparisons where useful. Report increases and unavailable measurements honestly. Keep review notes and surrounding commentary separate from replacement-text counts. Never treat fewer statement IDs as proof of fewer obligations or shorter text as proof of lower workload.
3. **Major changes:** structural changes, substantive omissions, weakened or replaced controls, and additions/broadened duties. Explicitly state when none occurred. Reference source units and the detailed change ledger.
4. **Likely risks:** lost safeguards, uncertain assumptions, affected parties, likelihood/severity where justified, and proposed mitigation or owner decision. Mark unmeasured risk judgments as hypotheses; do not invent numerical probabilities. Surface reviewer disagreements.
5. **Visuals:** retained/changed/removed figures, text/visual consistency and any unfinished modifications.
6. **Review and decisions:** checks actually performed, limitations, open questions and status of the proposed text. Clearly separate permission to explore from adoption approval.
7. **Learning outcome:** reusable changes applied, deferred/rejected candidates and reasons, or an explicit no-change result. Link the learning record and the updated skill/framework version.

Draft the summary at human-review handover; update it after subsequent decisions or feedback. Record every version in the run journal. A new draft invalidates a summary that describes an earlier one.

## Required learning step

The coordinator runs a retrospective after agent review and available human feedback. Do not wait indefinitely for feedback: record what is available and identify missing feedback. Consider extraction failures, unclear task settings, missed obligations, bad omissions, review corrections, visual mismatches, repeated user questions and misleading metrics.

Classify each observation as case-specific, reusable operational guidance, a user preference or an unresolved hypothesis. Case facts and confidential source content stay in the case record. An accepted omission is not automatically a general rule to delete similar controls elsewhere.

For every reusable candidate, record evidence, proposed target instructions/checks, expected benefit, possible regression and a decision:

- **Applied:** implement the justified improvement in the reusable role instructions, workflow, templates or validation layer; preserve before/after versions; review the change; run relevant regression checks; record target hashes, evidence and rollback location.
- **Deferred:** identify missing evidence, authority or capability and the next trigger for reconsideration. Do not label this as integrated.
- **Rejected:** explain why it does not generalize or conflicts with the mandate.
- **No change:** when the run yields no justified reusable change, state why; do not force a skill update to satisfy a checkbox.

Apply routine, reversible improvements within the recorded task authorization; preserve their review and rollback evidence. Decisions changing user intent, adoption authority or protected constraints require an explicit basis. Respect actual filesystem/access restrictions when applying changes. Never silently change installed skills outside the agreed framework destination; identify the active target location and version at intake or in a logged decision.

Here the reusable skill set is `agents/`, `WORKFLOW.md`, the supporting contracts, `templates/` and `src/procedure_simplifier/` within the framework folder. Updating an installed Codex skill is a separate target that must be identified if desired. The host executes these changes; the scaffold itself does not autonomously rewrite instructions.

Use `templates/learning.json` for the disposition record. `applied` entries require actual before/after instruction artifacts, reviewer evidence, validation results and rollback references. References are run-journal artifact IDs. Capture framework snapshots with `framework_before`/`framework_after`, change review with `review`, and regression output with `validation`. Capture the completed learning JSON as `learning`.

## Completion gate

Version 0.6 adds `templates/summary-record.json`, `validation-record.json` and `delivery-record.json`. Capture the machine-readable records as summary, validation and delivery; capture the readable closing summary as summary_text. All three records identify the current run, draft_ref and approach_ref. Summary records include the approach, measured/not-measured metrics, explicit omission/addition/risk/limitation lists and visual/review status. Measured metrics require a counting method and nonnegative word counts; do not calculate a percentage against a zero baseline. Validation records identify checks actually executed with status and evidence. Delivery records link the latest required artifacts and disclose incomplete/failed checks. The gate now also requires review, changes, risk_assessment and quality artifacts. Full approved-delivery verification remains outside this local proposal-closeout helper.

The final delivery index links source, effective task definition, modified document, change/risk/visual records, reviews, validation, closing summary and learning record. Before `closed`, the journal helper requires a summary, learning disposition, validation result and delivery index after the latest draft and approach, and checks learning references. It rejects pending candidates and unsupported claims of applied changes. Source integrity is checked separately with `verify`.

This gate verifies artifact presence/provenance and recorded dispositions. The coordinator/reviewer must still verify summary accuracy, substantive learning quality and whether the full delivery index is complete. Keep the transformation validator and visual checks in the process. Historical cases must not be represented as having completed later checks.
