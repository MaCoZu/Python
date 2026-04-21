"""Happy Planet Index scraper - wrapper for scraper.happy_planet_scraper."""

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
        "default": 2021,
        "options": [2019, 2021],
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
    "json": {
        "type": "bool",
        "required": False,
        "default": False,
        "help": "Also save as JSON",
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
    if args.get("json"):
        cli_args.append("--json")

    timeout = args.get("timeout", 120)
    result = subprocess.run(
        [sys.executable, str(SCRAPER_PATH / "happy_planet_scraper.py")] + cli_args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr
