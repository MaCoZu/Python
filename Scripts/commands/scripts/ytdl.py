"""YouTube downloader - wrapper for scripts.yt_dlp."""

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
        "help": "YouTube video/playlist URL",
    },
    "format": {
        "type": "string",
        "required": False,
        "default": "mp3",
        "options": ["mp3", "audio", "video"],
        "help": "Download format",
    },
    "quality": {
        "type": "string",
        "required": False,
        "default": "320",
        "options": ["320", "256", "128"],
        "help": "Audio quality (kbps)",
    },
}

CONFIG_KEY = "ytdl"


def run(args: dict) -> tuple[int, str, str]:
    cli_args = [args["url"]] if args.get("url") else []
    if args.get("format"):
        cli_args.extend(["--format", args["format"]])
    if args.get("quality"):
        cli_args.extend(["--quality", args["quality"]])

    timeout = args.get("timeout", 600)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_PATH / "scripts.py"), "ytdl"] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
