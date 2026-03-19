#!/usr/bin/env python3
"""Gemstone safety audit — scan for prohibited stone recommendations."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# Find lordship rules in engine
LORDSHIP_PATH = ROOT / "engine" / "src" / "daivai_engine" / "knowledge" / "lordship_rules.yaml"
# Fallback to old location
if not LORDSHIP_PATH.exists():
    LORDSHIP_PATH = ROOT / "jyotish" / "knowledge" / "lordship_rules.yaml"


def load_prohibited_stones() -> dict[str, list[str]]:
    """Load prohibited stones per lagna from lordship_rules.yaml."""
    if not LORDSHIP_PATH.exists():
        print(f"WARNING: {LORDSHIP_PATH} not found")
        return {}

    with open(LORDSHIP_PATH) as f:
        data = yaml.safe_load(f) or {}

    prohibited: dict[str, list[str]] = {}
    for lagna, info in data.items():
        if not isinstance(info, dict):
            continue
        stones = []
        for stone_info in info.get("prohibited_stones", []):
            if isinstance(stone_info, dict):
                stones.append(stone_info.get("name", "").lower())
            elif isinstance(stone_info, str):
                stones.append(stone_info.lower())
        prohibited[lagna] = stones

    return prohibited


def scan_prompts_for_safety(prohibited: dict[str, list[str]]) -> list[str]:
    """Scan prompt templates for hardcoded stone recommendations."""
    issues: list[str] = []

    # Scan all prompt templates
    for prompts_dir in [
        ROOT / "products" / "src" / "daivai_products" / "interpret" / "prompts",
        ROOT / "jyotish" / "interpret" / "prompts",
    ]:
        if not prompts_dir.exists():
            continue
        for template in prompts_dir.glob("*.md*"):
            content = template.read_text().lower()
            # Check for hardcoded "wear" + stone name without Jinja2 conditional
            recommend_pattern = re.compile(r"(?:wear|recommend|use)\s+(\w+)")
            for match in recommend_pattern.finditer(content):
                stone = match.group(1)
                # Check if this is inside a Jinja2 block (acceptable)
                if "{{" in content[max(0, match.start() - 50):match.start()]:
                    continue
                for lagna, stones in prohibited.items():
                    if stone in stones:
                        issues.append(
                            f"[SAFETY] {template.name}: hardcoded '{stone}' "
                            f"(prohibited for {lagna})"
                        )

    return issues


def main() -> int:
    """Run safety audit."""
    print("=" * 60)
    print("GEMSTONE SAFETY AUDIT")
    print("=" * 60)

    prohibited = load_prohibited_stones()
    if not prohibited:
        print("  No lordship rules found — skipping")
        print("PASSED (no rules to check)")
        return 0

    print(f"  Loaded prohibited stones for {len(prohibited)} lagnas")

    issues = scan_prompts_for_safety(prohibited)

    if issues:
        print(f"\nFOUND {len(issues)} SAFETY ISSUE(S):")
        for issue in issues:
            print(f"  {issue}")
        return 1

    print("PASSED — no safety issues found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
