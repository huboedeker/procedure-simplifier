# Procedure Simplifier

An auditable, agent-operated framework for simplifying procedural documents: regulations, internal policies, operating instructions and method guides.

Choose language simplification, content-preserving restructuring or an outcome-focused reduction. Four roles analyze the source, propose a simpler version, challenge changes independently and document the result. The Python tools check records, file integrity, declared processing plans and reproducible text counts.

**Status: 0.8.0 alpha.** This repository packages a tested scaffold. A host agent performs the actual reading, drafting, tool use and review. There is no model integration, automatic PDF ingestion, autonomous agent dispatcher or semantic-certification engine. A passing check is evidence about the recorded data, not approval to adopt a policy.

## Install and try

Python 3.11 or later; no third-party runtime dependencies.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
procedure-simplifier --version
procedure-simplifier doctor
procedure-simplifier export-framework ./my-framework
procedure-simplifier validate ./my-framework/examples/demo/run.json
procedure-simplifier quality ./my-framework/examples/demo/quality.json ./my-framework/examples/demo/run.json
procedure-simplifier chunks ./my-framework/examples/demo/chunk-plan.json
procedure-simplifier metrics ./my-framework/examples/demo/source.txt ./my-framework/examples/demo/output.md
```

On Windows activate with `.venv\Scripts\Activate.ps1`. `python -m procedure_simplifier` is an alternative to the installed command. Export requires a new or empty directory and never overwrites an existing workspace.

The demo is entirely fictional and intentionally reports no reduction. Completed-review fields are illustrative fixture data, not a claim of actual independent review. Real case inputs, corporate PDFs and trial audit histories are not included in this repository or its distributions.

## Use with an agent

Give your agent the exported `START-HERE.md`, `agents/coordinator.md`, your document and intended outcome. It must settle the task definition and context plan before reduction; treat document text as data; preserve original evidence; and invoke an independent reviewer before handover. The agent uses your host's tools and permissions. No API key is needed for the local utilities; any model service is configured separately in the host.

The final package includes the proposed text, source/change mapping, omissions and risks, visual consistency, independent findings, reduction metrics, unresolved decisions and learning disposition. Read [the quickstart](docs/quickstart.md) for a complete operational sequence.

## Choices and controls

Eight independently recorded switches cover wording, structure, consolidation, process redesign, requirement reduction, format fidelity, research scope and clarification cadence. Research and adoption authority remain bounded by the task. Images/graphs are inspected alongside text. Large inputs use capacity planning, semantic chunks, dependency order and optional bounded parallel workers, followed by combined-document review.

Framework assets are shipped inside the wheel at `src/procedure_simplifier/framework/`: [entry point](src/procedure_simplifier/framework/START-HERE.md), [task definition](src/procedure_simplifier/framework/TASK-DEFINITION.md), [quality controls](src/procedure_simplifier/framework/QUALITY-CONTROLS.md), [large documents](src/procedure_simplifier/framework/LARGE-DOCUMENTS.md), [audit](src/procedure_simplifier/framework/AUDIT-CONTRACT.md), [visuals](src/procedure_simplifier/framework/VISUAL-CONSISTENCY.md), and [closeout/learning](src/procedure_simplifier/framework/CLOSEOUT-AND-LEARNING.md).

## Repository layout

```text
src/procedure_simplifier/       installable Python tools and CLI
  framework/                   canonical agent instructions and contracts
    agents/                    coordinator, analyst, simplifier, reviewer
    templates/                 incomplete records to populate from real input
    schemas/                   versioned JSON Schema contracts
    examples/demo/             first-party synthetic fixture
tests/                         behavioral and packaging regressions
tools/                         schema and distribution checks
docs/                          operation, architecture, evaluation and GitLab setup
.gitlab-ci.yml                 tests and build artifacts; no publishing/deployment
pyproject.toml                 Python metadata and installed command
LICENSE                        MIT
```

## Development and release

```sh
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
python tools/check_schemas.py
python tools/check_distribution.py --source .
python -m build
python tools/check_distribution.py --archive dist/
```

Core tests use the standard library. The development extra adds a build frontend and JSON Schema validation; neither is required by installed runtime commands. GitLab CI tests Python 3.11/3.12, builds a wheel/source distribution and smoke-tests an installed wheel. CI has to run on your own GitLab runner before it can be called verified there.

Start with a normal GitLab source repository. Optional wheels can later be uploaded to GitLab's PyPI registry; npm is unnecessary for this Python runtime. See [GitLab upload](docs/gitlab-upload.md), [architecture and boundaries](docs/architecture.md), [data contracts](docs/data-contracts.md), [evaluation](docs/evaluation.md), [contributing](CONTRIBUTING.md) and [security/data handling](SECURITY.md).

MIT applies to this framework's code and documentation. It does not grant rights to third-party documents processed with it.
