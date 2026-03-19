"""Plugin auto-discovery and registry."""

from __future__ import annotations

import importlib
import logging
from pathlib import Path
from typing import Any


logger = logging.getLogger(__name__)

PLUGINS_DIR = Path(__file__).parent / "plugins"

_registry: dict[str, dict[str, Any]] = {}


def discover_plugins() -> dict[str, dict[str, Any]]:
    """Auto-discover all plugins in the plugins/ directory."""
    global _registry
    if _registry:
        return _registry

    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir() or plugin_dir.name.startswith("_"):
            continue
        try:
            module = importlib.import_module(f"daivai_products.plugins.{plugin_dir.name}")
            name = getattr(module, "PLUGIN_NAME", plugin_dir.name)
            _registry[name] = {
                "module": module,
                "name": name,
                "description": getattr(module, "DESCRIPTION", ""),
                "commands": getattr(module, "COMMANDS", {}),
            }
            logger.debug("Discovered plugin: %s", name)
        except Exception as e:
            logger.warning("Failed to load plugin %s: %s", plugin_dir.name, e)

    return _registry


def get_plugin(name: str) -> dict[str, Any] | None:
    """Get a specific plugin by name."""
    plugins = discover_plugins()
    return plugins.get(name)


def get_all_commands() -> dict[str, dict[str, Any]]:
    """Get all commands from all plugins."""
    plugins = discover_plugins()
    commands: dict[str, dict[str, Any]] = {}
    for plugin_info in plugins.values():
        for cmd_name, cmd_info in plugin_info["commands"].items():
            commands[cmd_name] = {**cmd_info, "plugin": plugin_info["name"]}
    return commands
