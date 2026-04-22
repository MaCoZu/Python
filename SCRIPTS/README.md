# Scripts TUI

A Textual-based Terminal User Interface (TUI) dashboard for running various scripts and scrapers.

## Overview

Scripts TUI provides a unified interface to run:
- **Scripts**: Email deduplication, book/ebook converters, YouTube downloader, academic paper tools
- **Scrapers**: Happy Planet Index, Social Progress Index

## Requirements

- Python 3.14+
- See `pyproject.toml` for dependencies

## Installation

```bash
pip install -e Scripts/
```

Or install dependencies only:

```bash
pip install textual pyyaml beautifulsoup4 ebooklib httpx pymupdf4llm pypdf requests typer watchdog youtube-transcript-api
```

## Running

```bash
# Run from the Scripts directory
cd Scripts && python app.py

# Or install as a package (requires textual in main environment)
pip install -e .
scripts
```

## Usage

1. Launch the app: `scripts`
2. Navigate groups using arrow keys
3. Select a command from the sidebar
4. Configure options in the input panel
5. Click "Run" to execute

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit |
| `Ctrl+q` | Quit |

## Available Commands

### Scripts

| Command | Description |
|---------|-------------|
| `email` | Remove duplicate emails from mailbox |
| `books` | Book management utilities |
| `ytrans` | YouTube transcript downloader |
| `ytdl` | YouTube video/audio downloader |
| `epubmd` | Convert EPUB to Markdown |
| `ebooktxt` | Convert ebook to text |
| `watchpaper` | Watch arXiv for new papers |
| `cleanfonts` | Clean font files |
| `scipaper` | Scientific paper utilities |

### Scrapers

| Command | Description |
|---------|-------------|
| `happy` | Scrape Happy Planet Index data |
| `social` | Scrape Social Progress Index data |

## Configuration

Commands are defined in `commands.yaml`. Edit to add/remove commands:

```yaml
groups:
  Scripts:
    mycommand: "commands.scripts.mymodule"
  Scrapers:
    myscraper: "commands.scrapers.mymodule"
```

Each command module must export:
- `run(args: dict) -> tuple[int, str, str]` - Returns (exit_code, stdout, stderr)
- `ARG_SCHEMA: dict` (optional) - Defines command options

## Project Structure

```
Scripts/
├── app.py           # Main Textual app
├── dashboard.py     # Command execution UI
├── sidebar.py       # Command navigation
├── registry.py      # Dynamic command loader
├── commands.yaml    # Command definitions
├── pyproject.toml   # Dependencies
├── commands/
│   ├── scripts/     # Script implementations
│   └── scrapers/   # Scraper implementations
└── tests/           # Unit tests
```

## Development

Run tests:

```bash
cd Scripts && pytest
```

## License

MIT
