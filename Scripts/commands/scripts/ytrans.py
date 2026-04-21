"""YouTube transcript downloader - wrapper for scripts.get_yt_transcripts."""

import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPTS_PATH = Path(__file__).parent.parent.parent.parent.parent / "Scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

ARG_SCHEMA: dict[str, Any] = {
    "url": {
        "type": "string",
        "required": True,
        "help": "YouTube video URL",
    },
    "output_dir": {
        "type": "string",
        "required": False,
        "help": "Output directory",
    },
}

CONFIG_KEY = "youtube"


def run(args: dict) -> tuple[int, str, str]:
    cli_args = [args["url"]] if args.get("url") else []
    if args.get("output_dir"):
        cli_args.extend(["--output-dir", args["output_dir"]])

    timeout = args.get("timeout", 300)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_PATH / "scripts.py"), "ytrans"] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
