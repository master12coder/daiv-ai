#!/usr/bin/env python3
"""Layer boundary enforcement — engine/ ← products/ ← apps/."""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RULES: dict[str, dict[str, set[str]]] = {
    "engine": {
        "allowed": set(),  # engine imports nothing from jyotish_products or jyotish_app
        "forbidden_prefixes": {"jyotish_products", "jyotish_app"},
    },
    "products": {
        "allowed": {"jyotish_engine"},
        "forbidden_prefixes": {"jyotish_app"},
    },
    "apps": {
        "allowed": {"jyotish_engine", "jyotish_products", "jyotish_app"},
        "forbidden_prefixes": set(),
    },
}

PACKAGE_MAP = {
    "engine": "jyotish_engine",
    "products": "jyotish_products",
    "apps": "jyotish_app",
}


def _get_package(filepath: Path) -> str | None:
    """Determine which package a file belongs to."""
    rel = str(filepath.relative_to(ROOT))
    for pkg in ("engine", "products", "apps"):
        if rel.startswith(f"{pkg}/"):
            return pkg
    return None


def check_file(filepath: Path) -> list[str]:
    """Check one Python file for import violations."""
    package = _get_package(filepath)
    if package is None:
        return []

    rules = RULES[package]
    violations: list[str] = []

    try:
        tree = ast.parse(filepath.read_text())
    except SyntaxError:
        return [f"{filepath}: SyntaxError"]

    for node in ast.walk(tree):
        modules: list[str] = []
        if isinstance(node, ast.Import):
            modules = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules = [node.module]

        for mod in modules:
            for forbidden in rules["forbidden_prefixes"]:
                if mod.startswith(forbidden):
                    rel = filepath.relative_to(ROOT)
                    violations.append(
                        f"[LAYER] {rel}:{node.lineno}: "
                        f"'{mod}' violates {package}/ boundary"
                    )

    return violations


def main() -> int:
    """Run import boundary checks."""
    print("=" * 60)
    print("IMPORT BOUNDARY CHECK")
    print("=" * 60)

    violations: list[str] = []
    for pkg_dir in ("engine", "products", "apps"):
        src_dir = ROOT / pkg_dir / "src"
        if not src_dir.exists():
            continue
        for py_file in sorted(src_dir.rglob("*.py")):
            if "__pycache__" in str(py_file):
                continue
            violations.extend(check_file(py_file))

    if violations:
        print(f"\nFOUND {len(violations)} VIOLATION(S):")
        for v in violations:
            print(f"  {v}")
        print(f"\nFAILED — {len(violations)} import violations")
        return 1

    print("PASSED — no import violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
