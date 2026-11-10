# Versions and data contracts

Package version **0.8.0** describes this repository/distribution. Transformation schema versions **0.1** and **0.2** are independent. Schema0.2 adds required visual-review records; historical0.1 support does not imply retrospective visual checks.

Versioned JSON Schemas live in the bundled framework's schemas/ directory. They provide portable structural contracts. The Python validators perform additional cross-record/permission/hash checks. Neither layer proves completeness, meaning or authority. Schemas intentionally allow extra fields for evidence and host metadata; supported enumerations still need to be respected.

| Record | Schema | Example/source |
|---|---|---|
| Transformation | run-0.1 / run-0.2 | Synthetic examples/demo/run.json; templates/run.json |
| Task | approach-0.8.0 | examples/demo/approach.json |
| Quality | quality-0.8.0 | examples/demo/quality.json |
| Processing | chunk-plan-0.8.0 | examples/demo/chunk-plan.json |
| Handover | summary / validation / delivery-0.8.0 | templates/*-record.json |
| Learning | learning-0.8.0 | templates/learning.json |

Blank templates are scaffolds, not completed instances; they should fail full validation. The schema-check utility verifies schema definitions, supported examples and expected template incompleteness. It performs no network resolution.

Quality paths are relative to the quality file; audit artifact IDs refer to that run's journal. Copying a quality record to a different directory may require relinking paths and a new audited version. Task/source/output changes invalidate affected downstream results. The canonical statement digest is not a substitute for inspecting the delivered export.

The move from the earlier loose framework to0.8.0 changes command/package locations, packaging and examples; it does not rewrite historical audit records. Existing recorded runs stay in their original local workspace. To adopt the package for a new run, export its framework and populate a new task/records. Do not relabel old runs as0.8.0.
