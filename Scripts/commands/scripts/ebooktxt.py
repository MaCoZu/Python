"""EPUB to Text converter - wrapper for scripts.epub_to_txt."""

import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPTS_PATH = Path(__file__).parent.parent.parent.parent.parent / "Scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

ARG_SCHEMA: dict[str, Any] = {
    "input_path": {
        "type": "string",
        "required": True,
        "help": "Input EPUB file path",
    },
    "output_path": {
        "type": "string",
        "required": False,
        "help": "Output text file path",
    },
}


def run(args: dict) -> tuple[int, str, str]:
    cli_args = []
    if args.get("input_path"):
        cli_args.append(args["input_path"])
    if args.get("output_path"):
        cli_args.extend(["--output", args["output_path"]])

    timeout = args.get("timeout", 300)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_PATH / "scripts.py"), "ebooktxt"] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
