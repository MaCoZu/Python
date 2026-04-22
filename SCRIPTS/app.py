"""Main Textual application for Scripts TUI."""

import asyncio

from dashboard import Dashboard
from registry import get_registry
from sidebar import Sidebar
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header


class ScriptsApp(App):
    """Unified Scripts TUI Dashboard."""

    CSS = """
    Screen {
        layout: horizontal;
    }

    #main {
        width: 100%;
        height: 100%;
    }

    Sidebar {
        width: 25;
        background: $surface;
        border-right: solid $border;
    }

    .group-header {
        text-style: bold;
        padding: 1 2;
        background: $panel;
    }

    .command-item {
        width: 100%;
        margin: 0;
    }

    #dashboard-content {
        width: 100%;
        padding: 1;
    }

    #input-panel, #output-panel, #status-panel {
        height: auto;
        border: solid $border;
        margin: 1;
        padding: 1;
    }

    .panel-title {
        text-style: bold;
    }

    #output-area {
        height: 20;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.registry = get_registry()
        self.selected_command: tuple[str, str] | None = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        with Horizontal(id="main"):
            yield Sidebar(self.registry)
            yield Dashboard(self.registry)
        yield Footer()

    def select_command(self, group: str, name: str) -> None:
        """Handle command selection from sidebar."""
        self.selected_command = (group, name)
        dashboard = self.query_one(Dashboard)
        dashboard.load_command(group, name)

    def run_command(self, args: dict) -> None:
        """Run the selected command with given arguments."""
        if not self.selected_command:
            return
        group, name = self.selected_command
        dashboard = self.query_one(Dashboard)
        asyncio.create_task(dashboard.execute_command(group, name, args))


def app() -> ScriptsApp:
    """Create and return the Scripts app."""
    return ScriptsApp()


if __name__ == "__main__":
    app().run()
