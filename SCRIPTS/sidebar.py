"""Sidebar navigation widget."""

from textual.widget import Widget
from textual.widgets import Button, Static


class Sidebar(Widget):
    """Sidebar with collapsible groups and command list."""

    def __init__(self, registry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registry = registry
        self.expanded_groups: dict[str, bool] = {}
        self.selected_item: str | None = None

    def compose(self):
        """Build the sidebar UI."""
        commands = self.registry.get_commands()

        for group_name, commands_dict in commands.items():
            if group_name not in self.expanded_groups:
                self.expanded_groups[group_name] = True

            header_id = f"group-{group_name}"
            yield Static(
                f"{'▼' if self.expanded_groups[group_name] else '▶'} {group_name}",
                id=header_id,
                classes="group-header",
            )

            if self.expanded_groups[group_name]:
                for cmd_name in commands_dict.keys():
                    item_id = f"cmd-{group_name}-{cmd_name}"
                    yield Button(
                        f"  {cmd_name}",
                        id=item_id,
                        classes="command-item",
                    )

    def on_button_pressed(self, event) -> None:
        """Handle command selection."""
        button_id = event.button.id
        if not button_id:
            return

        if button_id.startswith("group-"):
            group_name = button_id.replace("group-", "")
            self.expanded_groups[group_name] = not self.expanded_groups[group_name]
            self.refresh()
            return

        if button_id.startswith("cmd-"):
            parts = button_id.replace("cmd-", "").split("-", 1)
            if len(parts) == 2:
                group_name, cmd_name = parts
                self.app.select_command(group_name, cmd_name)
