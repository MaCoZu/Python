"""Scientific paper watcher - wrapper for scripts.watcher."""

import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPTS_PATH = Path(__file__).parent.parent.parent.parent.parent / "Scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

ARG_SCHEMA: dict[str, Any] = {
    "watch_dir": {
        "type": "string",
        "required": True,
        "help": "Directory to watch for papers",
    },
    "action": {
        "type": "string",
        "required": False,
        "default": "start",
        "options": ["start", "stop", "status"],
        "help": "Action: start, stop, or status",
    },
}

CONFIG_KEY = "scipapers"


def run(args: dict) -> tuple[int, str, str]:
    cli_args = []
    if args.get("watch_dir"):
        cli_args.append(args["watch_dir"])
    if args.get("action"):
        cli_args.extend(["--action", args["action"]])

    timeout = args.get("timeout", 60)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_PATH / "scripts.py"), "watchpaper"] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
