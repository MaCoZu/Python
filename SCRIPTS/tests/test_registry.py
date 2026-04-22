"""Tests for command registry."""

import sys
from pathlib import Path

scripts_path = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_path))

from registry import CommandRegistry


def test_registry_loads_commands():
    """Test that registry loads all commands from commands.yaml."""
    registry = CommandRegistry(scripts_path / "commands.yaml")

    commands = registry.get_commands()
    assert "Scripts" in commands
    assert "Scrapers" in commands


def test_scripts_group_has_all_commands():
    """Test that Scripts group has all 9 commands."""
    registry = CommandRegistry(scripts_path / "commands.yaml")

    scripts = registry.get_commands_in_group("Scripts")
    expected = [
        "email",
        "books",
        "ytrans",
        "ytdl",
        "epubmd",
        "ebooktxt",
        "watchpaper",
        "cleanfonts",
        "scipaper",
    ]

    for cmd in expected:
        assert cmd in scripts, f"Missing command: {cmd}"


def test_scrapers_group_has_all_commands():
    """Test that Scrapers group has both commands."""
    registry = CommandRegistry(scripts_path / "commands.yaml")

    scrapers = registry.get_commands_in_group("Scrapers")
    assert "happy" in scrapers
    assert "social" in scrapers


def test_load_command_module():
    """Test that we can load a command module."""
    registry = CommandRegistry(scripts_path / "commands.yaml")

    module = registry.load_command("Scripts", "email")
    assert hasattr(module, "ARG_SCHEMA")
    assert hasattr(module, "run")


def test_get_arg_schema():
    """Test extracting ARG_SCHEMA from module."""
    registry = CommandRegistry(scripts_path / "commands.yaml")

    module = registry.load_command("Scripts", "email")
    schema = registry.get_arg_schema(module)

    assert "mailbox_path" in schema
    assert schema["mailbox_path"]["type"] == "string"
