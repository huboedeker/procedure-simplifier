# Large-document processing — v0.8.0

## Decide before loading the full source into an agent

The coordinator performs a context-capacity check at intake. Compare the entire required packet—not only document text—with the host's available context: instructions, task definition, shared definitions, source text, visual inputs, dependencies, working/review space and expected output. Record the capacity basis, token-estimation method and uncertainty. Reserve explicit output/working space and a safety margin. Do not assume the advertised model limit is all available to the source or invent a model limit when the host cannot report it.

Choose single, chunked sequential or chunked parallel processing. A document can fit technically but still need chunks because of dense tables, numerous obligations or expensive visual inspection. Conversely, page count alone is not a reliable trigger. If capacity cannot be established, use conservative bounded packets and log the uncertainty; escalate an indivisible item that cannot be inspected reliably. Do not silently truncate or treat a short extraction as proof that a large source fits.

Record the execution choice, estimated load, source inventory, boundaries, dependencies, concurrency limit and synthesis plan in `templates/chunk-plan.json`. Link the plan from the task's `processing.plan_ref`, capture it in the audit journal, and validate it before dispatch. This is a coordinator planning obligation; the local helper does not measure the host window or automatically dispatch agents.

## Segment by meaning

Build the source/file/section inventory using bounded reads before detailed analysis. Assign stable IDs across the entire document set. Partition along sections, complete procedures or coherent requirement groups. Keep definitions with their uses as read-only context. Keep exceptions with their rules, table headers with rows, captions/legends/axes with graphs and all relevant flowchart branches together. Use continuation metadata for unavoidable physical splits; a split does not create permission to omit relationships.

Each selected source element has exactly one primary owner chunk. Neighboring text, definitions and cross-references may be repeated as read-only context, with their original IDs. Workers must not count, rewrite or dispose of these context elements as if they owned them. External/out-of-scope references remain dependencies, not silently included scope. Full coverage is checked against the independent original-source manifest, not merely against the chunk list.

Never split into fixed page blocks blindly. An oversized coherent unit needs a smaller source-linked substructure or a dedicated inspection; do not cut off a table/figure or erase a general exception to meet a token target.

## Sequence dependencies and use parallelism selectively

First establish shared definitions, normative status, terminology, protected constraints and cross-document precedence. Analyze foundational/dependent sections in dependency order. Detect cycles; resolve strongly connected sections jointly or supply their original source context in both packets, retaining explicit edges in the dependency register. Do not fake independence by dropping a cycle.

Parallel workers are appropriate for independent branches after shared context is available. Use the host's currently available worker concurrency capacity (after allowing for the coordinator/other active agents) and the task's recorded cap, whichever is lower. Sequential chunking remains valid when parallel workers are unavailable. Parallelism is an execution choice, not a relaxation of review, content permissions or audit requirements.

Use instances of the existing analyst/simplifier/reviewer roles, not a new permanent hierarchy. Start with analysis and conditional drafting in bounded chunks; avoid automatically spawning four agents for every chunk. A reviewer must not approve its own draft. Provide fresh bounded contexts rather than copying the entire parent conversation to every worker.

Every worker packet identifies the task/version, shared-context version, source hashes, primary IDs, read-only IDs, dependency results and exact deliverables. Workers return structured source maps, output statements, omissions/additions, risks, visual dispositions, questions and actual artifact references. They may not change global settings, edit another worker's files or approve adoption. Save separate chunk directories and immutable journal artifacts through a single coordinating writer; the current journal is not multi-writer safe.

Freeze each completed worker handoff before another agent reads it. Send immutable snapshot/hash references; mutable producer paths are not review targets. Later edits create new versions and explicitly invalidate affected review/merge results.

Workers do not recursively spawn more agents without coordinator assignment. The coordinator bounds retries and resource use, consolidates questions for the user and logs unresolved failures. A worker's uncertainty is not resolved by adding more workers without new evidence.

## Synthesize, then review the whole

Merge structured records before polishing the prose. Reconcile terminology, actor names, numbering, references, repetitions, conflicting instructions, exceptions, timing, modality and visual relationships. Keep an explicit merge ledger for source ownership and each cross-chunk change. Deduplicate overlapping context without deleting distinct controls. Every source unit retains a disposition through every merge level.

If the coordinator cannot fit all chunk results, use bounded hierarchical merge batches with source-linked registries. Each merge has its own capacity estimate. Compact summaries are navigation aids; original evidence remains retrievable and must be consulted for semantic judgments. Check that the final root merge includes every selected chunk. Do not solve context overflow by repeatedly summarizing away the evidence.

Independent final review checks the combined artifact, not just whether chunks passed separately. Cover boundary exceptions, definitions used elsewhere, distant approvals/constraints, cross-chunk visuals, duplicate or contradictory steps and cumulative procedural burden. For a large combined artifact, perform planned review passes over bounded regions plus targeted cross-boundary scenarios, retaining a global coverage register. Claim whole-document review only when all regions and material boundaries have evidence; a single global-context prompt is not required or sufficient.

## Resume and invalidate correctly

Log dispatches, dependencies, chunk versions, work starts/completions, retries, merges and review coverage. Reuse a result only when its source, effective task, shared context and upstream dependency versions are unchanged. A source edit invalidates its owner chunk, dependent chunks and downstream merges/reviews/summaries. A task or shared-definition change may invalidate all chunks. Failed/missing workers leave the run incomplete; never omit them from the final denominator. Aggregate word counts over unique primary source content, not duplicated overlap text.

The final summary includes processing strategy, number of chunks/workers/merge levels, unresolved boundaries, resource measurements actually available and any resulting limitations. Learning changes to shared instructions should be applied after the run or trigger explicit version invalidation; do not silently mix worker instruction versions in one synthesis.

## Local support and evaluation

`procedure-simplifier chunks /path/chunk-plan.json` checks coverage, ownership, dependency waves, packet estimates and merge coverage. It validates recorded estimates, not tokenization accuracy, semantic boundaries or real host capacity. The plan template is deliberately incomplete. `invalidated_chunks()` supports conservative rerun planning; actual role dispatch, recovery and automatic propagation remain host responsibilities.

The current approach-journal helper does not automatically cross-validate `processing.plan_ref`. The coordinator must run the plan checker, record its result and verify the reference before dispatch; a saved approach by itself is not evidence of a completed capacity check. Full integration should enforce this handoff automatically.

Test long-range exceptions, definitions in appendices, tables across pages, duplicate overlap, dependency cycles, changed shared context, failed workers and a synthesis batch that itself exceeds capacity. Compare single/serial/parallel runs on cases that fit all strategies; assess meaning, reader usefulness, elapsed time, cost and review effort. Do not assume more agents improve either quality or efficiency.
