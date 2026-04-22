"""Book filename cleaner - wrapper for scripts.clean_book_filenames."""

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
        "help": "Folder containing book files",
    },
    "recursive": {
        "type": "bool",
        "required": False,
        "default": False,
        "help": "Process subfolders recursively",
    },
}

CONFIG_KEY = "books"


def run(args: dict) -> tuple[int, str, str]:
    cli_args = [args["folder"]] if args.get("folder") else []
    if args.get("recursive"):
        cli_args.append("--recursive")

    timeout = args.get("timeout", 300)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_PATH / "scripts.py"), "books"] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
