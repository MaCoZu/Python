"""Font cleaner - wrapper for scripts.clean_fonts."""

import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPTS_PATH = Path(__file__).parent.parent.parent.parent.parent / "Scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

ARG_SCHEMA: dict[str, Any] = {
    "font_dir": {
        "type": "string",
        "required": True,
        "help": "Directory containing font files",
    },
    "keep_formats": {
        "type": "string",
        "required": False,
        "default": "ttf woff2 otf",
        "help": "Font formats to keep (space separated)",
    },
}

CONFIG_KEY = "fonts"


def run(args: dict) -> tuple[int, str, str]:
    cli_args = [args["font_dir"]] if args.get("font_dir") else []
    if args.get("keep_formats"):
        cli_args.extend(["--keep-formats", args["keep_formats"]])

    timeout = args.get("timeout", 300)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_PATH / "scripts.py"), "cleanfonts"] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
