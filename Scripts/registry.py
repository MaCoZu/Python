"""Dynamic command registry - loads commands from commands.yaml."""

import importlib
from pathlib import Path
from typing import Any

import yaml


class CommandRegistry:
    def __init__(self, commands_file: Path):
        with open(commands_file) as f:
            self._config = yaml.safe_load(f)
        self._commands: dict[str, dict[str, str]] = self._config.get("groups", {})
        self._loaded_modules: dict[str, Any] = {}

    def get_commands(self) -> dict[str, dict[str, str]]:
        """Returns all commands grouped as defined in commands.yaml."""
        return self._commands

    def get_groups(self) -> list[str]:
        """Returns list of group names."""
        return list(self._commands.keys())

    def get_commands_in_group(self, group: str) -> dict[str, str]:
        """Returns commands in a specific group."""
        return self._commands.get(group, {})

    def load_command(self, group: str, name: str):
        """Loads a command module by group and name."""
        key = f"{group}.{name}"
        if key in self._loaded_modules:
            return self._loaded_modules[key]

        commands = self._commands.get(group, {})
        module_path = commands.get(name)
        if not module_path:
            raise ValueError(f"Command {group}.{name} not found")

        module = importlib.import_module(module_path)
        self._loaded_modules[key] = module
        return module

    def get_arg_schema(self, module) -> dict:
        """Extracts ARG_SCHEMA from module, returns empty dict if missing."""
        return getattr(module, "ARG_SCHEMA", {})

    def run_command(self, group: str, name: str, args: dict) -> tuple[int, str, str]:
        """Runs a command with given args, returns (exit_code, stdout, stderr)."""
        module = self.load_command(group, name)
        run_func = getattr(module, "run", None)
        if not run_func:
            raise ValueError(f"Module {group}.{name} has no run() function")
        return run_func(args)


def get_registry() -> CommandRegistry:
    """Returns the global command registry instance."""
    commands_file = Path(__file__).parent / "commands.yaml"
    return CommandRegistry(commands_file)
