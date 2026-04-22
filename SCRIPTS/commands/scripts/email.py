"""Email duplicate removal - wrapper for scripts.remove_duplicate_emails."""

import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPTS_PATH = Path(__file__).parent.parent.parent.parent.parent / "Scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))

ARG_SCHEMA: dict[str, Any] = {
    "mailbox_path": {
        "type": "string",
        "required": False,
        "help": "Path to mailbox file",
    },
    "backup_dir": {
        "type": "string",
        "required": False,
        "help": "Backup directory",
    },
    "keep_backups": {
        "type": "int",
        "required": False,
        "default": 1,
        "help": "Number of backups to keep",
    },
}

CONFIG_KEY = "email"


def run(args: dict) -> tuple[int, str, str]:
    """Execute email deduplication."""
    cli_args = []
    if args.get("mailbox_path"):
        cli_args.append(args["mailbox_path"])
    if args.get("backup_dir"):
        cli_args.extend(["--backup-dir", args["backup_dir"]])
    if args.get("keep_backups"):
        cli_args.extend(["--keep", str(args["keep_backups"])])

    timeout = args.get("timeout", 300)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_PATH / "scripts.py"), "email"] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
