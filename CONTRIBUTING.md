# Contributing

Use Python3.11+, install `.[dev]`, run the complete test suite and tools/check_schemas.py. Keep behavioral changes small and add tests for real failure modes rather than tests that only restate the implementation.

The canonical agent instructions, templates, schemas and synthetic examples are under src/procedure_simplifier/framework/. They ship inside both wheel and source distribution. Exported workspaces are copies; changes there do not automatically update this repository. Promote reusable changes through the learning contract, with source evidence, independent review, regression checks and rollback.

Use only invented or explicitly authorized redistributable examples. Do not contribute source PDFs, private excerpts, run logs, personal paths, credentials or unreviewed user preferences. Avoid turning a case-specific accepted omission into a universal policy-removal rule.

Change package version in pyproject.toml and __init__.py together; update template framework_version and CHANGELOG.md. Change data-schema versions independently when compatibility requires it. Keep supported historical records readable without inventing retroactive audit evidence. Build and inspect wheel/sdist content and test the wheel from outside the source checkout before a release.
