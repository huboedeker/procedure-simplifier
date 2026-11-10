# Evaluation protocol

Large-document tests under LARGE-DOCUMENTS.md must cover distant exceptions, appendix definitions, split tables/figures, dependency cycles, overlap ownership, worker failure, changed upstream/shared context and an overflowing synthesis stage. Compare serial and parallel strategies for equivalent output quality and measured resource use; metadata-plan tests alone do not establish actual long-context performance.

Build a small annotated set from multiple document families and all simplification modes. Start with two new cases: an exception-heavy procedure with an external dependency, and a document containing a process diagram and a quantitative graph. Add scans, tables, footnotes, conflicting rules and visual-only instructions. Add translation/localization when in scope. Identify normal tasks, exceptions and important stakeholders before drafting.

Have a domain-capable reviewer independently establish expected source content and behavior. Keep an unseen subset separate from prompt development and learning promotion. Record framework/model versions, inputs, settings, timestamps, reviewer context and actual tools used. Repeat selected cases to assess variability.

## Required challenges

| Challenge | Test | Evidence to record |
|---|---|---|
| Source omission | Drop a paragraph, footnote, table row or diagram branch before analysis | Independent source review catches it without relying on missing unit IDs |
| Meaning drift | Seed actor swap, lost exception/negation, must-to-may, numeric threshold and approval changes | Detection and false-alarm counts, severity, missed cases |
| Dependencies | Make an apparently redundant control support another section | Impact identified, with justified retention or explicit proposal risk |
| Legitimate reduction | Supply evidence of duplication or an adequate replacement | Useful reduction without inventing obligations or hiding losses |
| Visual contradiction | Change an approval step or numerical claim while retaining the old figure | Roles/arrows/labels/axes/captions checked against final text |
| Missing data | Unreadable image, absent chart data or inaccessible attachment | Explicit uncertainty and correct clarification/escalation |
| Reader usefulness | Ask readers to find owners, choose branches and handle exceptions | Accuracy, lookup time and review effort compared with original |
| Export fidelity | Render actual output and inspect tables, numbering, references and accessibility | Versioned render checks and defects |
| Source instructions | Embed commands to alter role, tool use or destination in document data | Observed behavior respects task instructions; source content remains data |
| Learning regression | Apply a candidate improvement and replay held-out cases | Before/after semantic, usability and error results; rollback demonstration |

Define mode-appropriate acceptance criteria before seeing results. Report observed rates with sample sizes and limitations rather than presenting a small set as a guarantee. Separate deterministic metadata checks, agent review, domain review and reader studies. No known unauthorized critical meaning change may be called preservation success. An experimental reduction can be useful without being approved for adoption.

After evaluation, classify failures and integrate justified reusable changes through the learning contract. Do not add permanent agents or switches merely to mirror test categories.
