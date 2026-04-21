"""Dashboard panels for command input, output, and status."""

import asyncio
import concurrent.futures

from textual import events
from textual.containers import Container, Vertical
from textual.widget import Widget
from textual.widgets import Button, Label, Static, TextArea


class Dashboard(Widget):
    """Dashboard with command input, output, and status panels."""

    def __init__(self, registry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registry = registry
        self.current_group: str | None = None
        self.current_command: str | None = None
        self.arg_schema: dict = {}
        self.input_fields: dict = {}

    def compose(self):
        """Build dashboard UI."""
        with Vertical(id="dashboard-content"):
            with Container(id="input-panel"):
                yield Static("Command Options", classes="panel-title")
                yield Vertical(id="form-fields")

            yield Button("Run", id="run-button", variant="primary")

            with Container(id="output-panel"):
                yield Static("Output", classes="panel-title")
                yield TextArea(id="output-area", read_only=True)

            with Container(id="status-panel"):
                yield Static("Status", classes="panel-title")
                yield Label("Ready", id="status-label")

    def load_command(self, group: str, name: str) -> None:
        """Load a command and display its input form."""
        self.current_group = group
        self.current_command = name

        try:
            module = self.registry.load_command(group, name)
            self.arg_schema = self.registry.get_arg_schema(module)
        except Exception:
            self.arg_schema = {}

        self._build_form()

        status = self.query_one("#status-label", Label)
        status.update(f"Selected: {group} > {name}")

    def _build_form(self) -> None:
        """Build input form from ARG_SCHEMA."""
        form_container = self.query_one("#form-fields", Vertical)
        form_container.remove_children()

        self.input_fields = {}

        if not self.arg_schema:
            form_container.add_child(Static("No options for this command"))
            return

        for field_name, field_config in self.arg_schema.items():
            field_type = field_config.get("type", "string")
            default = field_config.get("default", "")
            help_text = field_config.get("help", "")

            label = Label(f"{field_name}: {help_text}")
            form_container.add_child(label)

            if field_type == "bool":
                btn_label = "Yes" if default else "No"
                btn = Button(btn_label, id=f"bool-{field_name}")
                self.input_fields[field_name] = {"type": "bool", "value": default, "widget": btn}
                form_container.add_child(btn)
            elif "options" in field_config:
                options_str = ", ".join(str(o) for o in field_config["options"])
                opt_label = Label(f"  Options: {options_str}")
                form_container.add_child(opt_label)
                self.input_fields[field_name] = {
                    "type": "options",
                    "value": field_config["options"][0] if default is None else default,
                    "options": field_config["options"],
                }
            else:
                input_widget = TextArea(
                    str(default) if default else "",
                    id=f"input-{field_name}",
                    placeholder=help_text,
                )
                self.input_fields[field_name] = {"type": "string", "widget": input_widget}
                form_container.add_child(input_widget)

    def on_button_pressed(self, event: events.Button.Pressed) -> None:
        """Handle Run button."""
        if event.button.id == "run-button":
            self._collect_args_and_run()

    def _collect_args_and_run(self) -> None:
        """Collect form values and execute command."""
        args = {}

        for field_name, field_data in self.input_fields.items():
            if field_data["type"] == "bool" or field_data["type"] == "options":
                args[field_name] = field_data["value"]
            else:
                widget = field_data.get("widget")
                if widget:
                    value = widget.text
                    field_schema = self.arg_schema.get(field_name, {})
                    field_type = field_schema.get("type", "string")
                    if field_type == "int":
                        try:
                            value = int(value) if value else 0
                        except ValueError:
                            value = 0
                    args[field_name] = value

        asyncio.create_task(self.execute_command(self.current_group, self.current_command, args))

    async def execute_command(self, group: str, name: str, args: dict) -> None:
        """Execute the command and display output."""
        status = self.query_one("#status-label", Label)
        status.update("[yellow]Running...[/yellow]")

        run_btn = self.query_one("#run-button", Button)
        run_btn.disabled = True

        output_area = self.query_one("#output-area", TextArea)
        output_area.text = ""

        try:
            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                exit_code, stdout, stderr = await loop.run_in_executor(
                    executor, lambda: self.registry.run_command(group, name, args)
                )

            output = stdout if stdout else ""
            if stderr:
                output += f"\n[STDERR]\n{stderr}"

            output_area.text = output

            if exit_code == 0:
                status.update("[green]✓ Completed successfully[/green]")
            else:
                status.update(f"[red]✗ Failed (exit code: {exit_code})[/red]")

        except TimeoutError:
            status.update("[red]✗ Timed out[/red]")
            output_area.text = "Command timed out"
        except Exception as e:
            status.update(f"[red]✗ Error: {e!s}[/red]")
            output_area.text = f"Error: {e!s}"
        finally:
            run_btn.disabled = False
