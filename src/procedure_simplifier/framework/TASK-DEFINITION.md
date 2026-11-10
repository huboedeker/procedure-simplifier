# Task definition and selectable switches — v0.8.0

Execution settings are recorded separately under `processing`: requested strategy (auto/single/chunked_sequential/chunked_parallel), selected strategy, concurrency cap, plan reference and capacity-check status. These are orchestration settings, not additional content-reduction switches. The coordinator resolves automatic selection from actual context capacity, semantic complexity and dependencies under LARGE-DOCUMENTS.md. Missing context capacity cannot be replaced with an invented limit. Single processing still requires a capacity check; source/task permissions apply identically to each worker.

Intake also requires `output_role` (explanatory_companion, proposed_replacement or formal_amendment), `decision_owner`, `adoption_authority`, `framework_version` and `skill_target`. Unknown adoption authority can be stated explicitly for an exploratory proposal; it cannot be converted into an approval claim. These are task fields, not additional simplification switches.

Closing summary and learning integration are required deliverables under CLOSEOUT-AND-LEARNING.md for every switch configuration. Identify the target skill/framework location and version in the task definition or a logged decision before applying reusable changes.

Every task also includes the mandatory inventory and text/visual consistency check in VISUAL-CONSISTENCY.md. The switches govern whether figures may be reformatted or substantively changed; they never waive the consistency check. Record visual scope and known asset/data limitations at intake.

The saved approach is the authoritative task definition for a run. It includes the user's objective, audience, scope, switch selections, protected requirements, acceptance criteria, expected artifacts, decisions and gaps. The coordinator presents this in plain language at intake and saves the resolved record using `templates/approach.json`.

## Switches

| Switch | Choices | Effect |
|---|---|---|
| Wording | Retain / Plain language / Condensed | How much the language may change. Condensation alone does not permit lost content. |
| Structure | Preserve / Reorganize / Free | Whether sections and logical grouping may change. |
| Consolidation | Off / On | Whether repeated or related statements may be combined while retaining their scope. |
| Process redesign | Off / On | Whether steps, handoffs, roles or approval routes may be redesigned. |
| Requirement reduction | None / Evidence-based / Assumption-based | Whether substantive obligations or details may be dropped and what justification is required. |
| Format fidelity | Preserve / Adapt / Free | Whether layout, numbering and presentation conventions must be retained. Specific protected identifiers remain constraints even with free format. |
| Research | Provided sources only / Approved internal sources / Public and approved internal sources | Which evidence sources the agents may consult. Existing access and destination permissions still apply. |
| Clarification | Material gaps / Stage checkpoints | Ask when a material gap arises, or also pause at agreed stages. Both choices require material gaps to be addressed before dependent work. |

The machine values are defined in `src/procedure_simplifier/task_options.py`. Output medium and style—document, checklist, role table, or agent-selected—are captured in the `format` field. Scope, exclusions and non-negotiable obligations remain explicit task fields rather than implicit consequences of a mode.

Evidence-based reduction requires evidence supporting the removal or adequate replacement of the control. Evidence of textual repetition alone may justify consolidation but does not establish substantive redundancy. Assumption-based reduction permits exploratory value hypotheses with explicit uncertainty, lost safeguards, consequences and owner decisions before adoption. Neither setting authorizes removing otherwise protected requirements.

Process redesign with reduction set to none must preserve substantive obligations while changing how they are fulfilled. If a proposed redesign would remove or weaken an obligation, clarify and revise the reduction setting before proceeding with that change.

## Choose independently, or start from a profile

| Suggested profile | Wording | Structure | Consolidation | Process redesign | Reduction | Format |
|---|---|---|---|---|---|---|
| Text simplification | Plain | Preserve | Off | Off | None | Adapt |
| Content-preserving restructure | Condensed | Free | On | Off | None | Free |
| Outcome-focused reduction | Condensed | Free | On | On | Assumption-based | Free |

Profiles are suggestions, not authorization. The user may combine choices independently. Research scope and clarification preference are always recorded separately. Profiles are illustrative; they do not establish an authorization decision.

## Selection and provenance

Each switch stores `value` and `decision_ref`. The referenced decision records the choice, its basis (`explicit_user` or `authorized_default`) and IDs of the actual user-input artifacts. One decision can cover several switches if its choice text names them. The coordinator must explain any defaults in the intake summary and identify the instruction authorizing their use. Do not label convenience defaults as explicit user choices.

The blank template uses null values so unselected options cannot masquerade as decisions. Use settled conversation context to populate it; ask only for material missing choices. A profile can reduce the number of questions but does not replace the saved individual settings.

The validator rejects missing/unselected choices, missing decision references, preserved format paired with changed structure, and permissions that disagree with the switches. `mode` is a summary derived from those choices, not a second source of authority: redesign/reduction implies outcome mode; other presentation/consolidation changes imply structure mode; otherwise language mode. A free structure never implicitly permits dropping content.

## Intake summary and downstream use

Before processing, summarize: “We will [objective] for [audience], covering [scope], with [selected switches], while preserving [constraints]. We will produce [deliverables] at [audit location]. Unresolved issues: [gaps and handling].” Log the summary as an artifact or event; do not request repeat approval for choices already authorized.

Pass the effective task definition to every agent. The analyst assesses permitted omissions under the selected evidence standard; the simplifier respects the structure/format boundaries; the reviewer tests the result against the selected mandate. Carry the derived transformation permissions into the transformation record. The coordinator must check those records agree; host-wide automatic propagation is not yet implemented.

Any change to a switch is a new decision and versioned task definition. Record why it changed, which input authorized it and which analysis/drafts must be revisited. New user steering invalidates the existing approach gate until reconsidered. Review, traceability and audit records are baseline workflow requirements across profiles.
