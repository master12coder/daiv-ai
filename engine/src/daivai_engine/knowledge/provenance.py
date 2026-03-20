"""Provenance lookup — get source citation for any computation.

Every result in DaivAI must be traceable to a classical text.
This module loads computation_sources.yaml and provides lookups.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


_SOURCES_FILE = Path(__file__).parent / "computation_sources.yaml"
_CACHE: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    """Load and cache the computation sources YAML."""
    global _CACHE
    if _CACHE is None:
        with open(_SOURCES_FILE) as f:
            _CACHE = yaml.safe_load(f) or {}
    return _CACHE


def get_source(computation: str) -> dict[str, Any]:
    """Get the provenance for a computation by name.

    Args:
        computation: Name like 'gajakesari', 'mangal_dosha', 'shadbala', etc.

    Returns:
        Dict with source, rule, alternatives, invalidation, confidence.
        Empty dict if not found.
    """
    data = _load()
    result: dict[str, Any] = data.get(computation, {})
    return result


def get_all_sources() -> dict[str, Any]:
    """Get the complete provenance database."""
    return _load()


def explain(computation: str) -> str:
    """Get a human-readable explanation for a computation.

    Returns a formatted string a Pandit can read to understand
    the basis for any result.
    """
    info = get_source(computation)
    if not info:
        return f"No provenance found for '{computation}'."

    parts = [f"=== {computation.upper()} ==="]

    if "source" in info:
        parts.append(f"Source: {info['source']}")
    if "rule" in info:
        parts.append(f"Rule: {info['rule']}")
    if "alternatives" in info:
        parts.append("Alternatives:")
        for alt in info["alternatives"]:
            parts.append(f"  - {alt}")
    if "invalidation" in info:
        parts.append("When this might be wrong:")
        for inv in info["invalidation"]:
            parts.append(f"  - {inv}")
    if "confidence" in info:
        parts.append(f"Confidence: {info['confidence']}")

    return "\n".join(parts)
