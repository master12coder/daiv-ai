#!/usr/bin/env python3
"""Plugin contract verification — every plugin must have required attributes."""
from __future__ import annotations

import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "products" / "src" / "daivai_products" / "plugins"

REQUIRED_ATTRS = {"PLUGIN_NAME", "DESCRIPTION", "COMMANDS"}


def check_plugin(plugin_name: str) -> list[str]:
    """Verify a single plugin meets the contract."""
    errors: list[str] = []

    try:
        module = importlib.import_module(f"daivai_products.plugins.{plugin_name}")
    except ImportError as e:
        return [f"  {plugin_name}: cannot import — {e}"]

    for attr in REQUIRED_ATTRS:
        if not hasattr(module, attr):
            errors.append(f"  {plugin_name}: missing {attr}")

    if hasattr(module, "PLUGIN_NAME") and (
        not isinstance(module.PLUGIN_NAME, str) or not module.PLUGIN_NAME
    ):
            errors.append(f"  {plugin_name}: PLUGIN_NAME must be non-empty string")

    if hasattr(module, "COMMANDS"):
        if not isinstance(module.COMMANDS, dict):
            errors.append(f"  {plugin_name}: COMMANDS must be dict")
        else:
            for cmd_name, cmd_info in module.COMMANDS.items():
                if not isinstance(cmd_info, dict) or "help" not in cmd_info:
                    errors.append(f"  {plugin_name}: COMMANDS['{cmd_name}'] must have 'help' key")

    return errors


def main() -> int:
    """Verify all plugins."""
    print("=" * 60)
    print("PLUGIN CONTRACT CHECK")
    print("=" * 60)

    # Add source paths
    for pkg in ("engine", "products", "apps"):
        src = str(ROOT / pkg / "src")
        if src not in sys.path:
            sys.path.insert(0, src)

    all_errors: list[str] = []
    plugins_found = 0

    if not PLUGINS_DIR.exists():
        print("  No plugins directory found")
        return 1

    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir() or plugin_dir.name.startswith("_"):
            continue
        plugins_found += 1
        errors = check_plugin(plugin_dir.name)
        if errors:
            all_errors.extend(errors)
        else:
            print(f"  ✓ {plugin_dir.name}")

    print(f"\nPlugins found: {plugins_found}")

    if all_errors:
        print(f"\nFOUND {len(all_errors)} ERROR(S):")
        for e in all_errors:
            print(e)
        return 1

    print("PASSED — all plugins meet contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
