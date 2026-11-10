# Evidence and evaluation

Development trials showed that the workflow can create shorter reviewable proposals, retain key controls on source-based review and expose process defects. They were exploratory examples, not a randomized study or a validated estimate of semantic reliability, human labor savings or parallel speedup. Private case text and audit histories are deliberately outside this repository.

The regression suite was ported to first-party synthetic fixtures. Its passing results establish behavior of local checks; they are not a percentage of meaning preserved. The supplied demo has zero reduction by design and labels review metadata as fictional.

Use the bundled EVALUATION-PROTOCOL.md for source omissions, seeded semantic defects, boundary dependencies, legitimate reductions, graph/diagram contradictions, missing data, reader scenarios, source-instruction attacks and held-out learning regressions. Actual large-document execution and concurrency have not been benchmarked by the plan tests.

For human-versus-AI comparison:

- Match source scope, intended output and acceptance criteria before production.
- Keep source orientation, drafting, review, corrections and full audit packaging separate.
- Measure human active labor separately from AI-run elapsed time, model compute and tool/model cost.
- Use the same exact counting method and register baseline/output hashes.
- Keep the human participant blind to the AI answer when testing manual production. Identify reviewer independence and prior document familiarity.
- Include correction/recheck effort and equivalent content quality before calculating labor savings. Similar review time may be a planning assumption; label it until measured.

An initial labor comparison with unmatched active/elapsed measures supports qualitative feasibility, not an asserted speedup. Review uncertainty and deficiencies as evidence for the next run, then promote only justified reusable learning.
