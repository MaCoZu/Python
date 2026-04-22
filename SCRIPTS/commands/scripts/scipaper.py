"""Scientific paper renamer - wrapper for scripts.sci_paper_renamer."""

import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPTS_PATH = Path(__file__).parent.parent.parent.parent.parent / "Scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

ARG_SCHEMA: dict[str, Any] = {
    "folder": {
        "type": "string",
        "required": True,
        "help": "Folder containing scientific papers",
    },
    "dry_run": {
        "type": "bool",
        "required": False,
        "default": True,
        "help": "Preview changes without renaming",
    },
}


def run(args: dict) -> tuple[int, str, str]:
    cli_args = [args["folder"]] if args.get("folder") else []
    if args.get("dry_run"):
        cli_args.append("--dry-run")

    timeout = args.get("timeout", 300)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_PATH / "scripts.py"), "scipaper"] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
