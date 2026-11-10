"""Agent-operated framework and local evidence checks."""
from pathlib import Path

__version__ = "0.8.0"

def framework_root():
    """Read-only location of the bundled instructions/templates/examples."""
    return Path(__file__).resolve().parent / "framework"
