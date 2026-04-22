"""Social Progress Index scraper - wrapper for scraper.social_progress_scraper."""

import subprocess
import sys
from pathlib import Path
from typing import Any

SCRAPER_PATH = Path(__file__).parent.parent.parent.parent / "scraper"
if str(SCRAPER_PATH) not in sys.path:
    sys.path.insert(0, str(SCRAPER_PATH))

ARG_SCHEMA: dict[str, Any] = {
    "year": {
        "type": "int",
        "required": False,
        "default": 2024,
        "options": [2021, 2022, 2024],
        "help": "Year to scrape",
    },
    "all": {
        "type": "bool",
        "required": False,
        "default": False,
        "help": "Scrape all available years",
    },
    "output": {
        "type": "string",
        "required": False,
        "help": "Output CSV file path",
    },
}


def run(args: dict) -> tuple[int, str, str]:
    cli_args = []
    if args.get("all"):
        cli_args.append("--all")
    elif args.get("year"):
        cli_args.extend(["--year", str(args["year"])])
    if args.get("output"):
        cli_args.extend(["--output", args["output"]])

    timeout = args.get("timeout", 120)
    result = subprocess.run(
        [sys.executable, str(SCRAPER_PATH / "social_progress_scraper.py")] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
