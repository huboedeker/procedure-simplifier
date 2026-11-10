"""Unified, model-independent command line interface."""
import argparse
import importlib
import json
from pathlib import Path
import shutil
import sys
from . import __version__, framework_root

COMMANDS = {
    "validate": "validate",
    "quality": "quality",
    "audit": "audit",
    "chunks": "chunks",
    "metrics": "metrics",
}

def export_framework(destination):
    source, target = framework_root(), Path(destination)
    if target.resolve().is_relative_to(source.resolve()):
        raise ValueError("Choose an export directory outside the installed framework.")
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise ValueError("Export destination must be new or empty; existing files are not overwritten.")
    shutil.copytree(source, target, dirs_exist_ok=True)
    return target.resolve()

def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    # Let each existing command retain its detailed parser/help and exit codes.
    if args and args[0] in COMMANDS:
        module = importlib.import_module("procedure_simplifier." + COMMANDS[args[0]])
        previous = sys.argv
        try:
            sys.argv = ["procedure-simplifier " + args[0]] + args[1:]
            return module.main() or 0
        finally:
            sys.argv = previous
    parser = argparse.ArgumentParser(description="Agent-operated procedural document simplification and evidence checks.")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Show capabilities without making network/model calls")
    export = sub.add_parser("export-framework", help="Copy bundled instructions, templates, schemas and synthetic example")
    export.add_argument("destination", type=Path)
    for command in COMMANDS:
        sub.add_parser(command, help="Use '" + command + " --help' for options")
    parsed = parser.parse_args(args)
    if parsed.command == "doctor":
        print(json.dumps(dict(version=__version__, python=sys.version.split()[0], framework_path=str(framework_root()),
                              framework_present=(framework_root()/"START-HERE.md").is_file(),
                              runtime_dependencies=[], model_api_calls=False,
                              automatic_agent_dispatch=False, automatic_pdf_ingestion=False,
                              checks="record structure, provenance, file integrity and declared plans; not semantic certification"), indent=2))
    elif parsed.command == "export-framework":
        try: print(export_framework(parsed.destination))
        except (ValueError, OSError) as exc: parser.exit(1, str(exc) + "\n")
    return 0
