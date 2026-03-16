"""Domain models for Vedic yoga detection results."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class YogaResult:
    """Represents the result of detecting a specific Vedic yoga in a chart.

    Contains the yoga name (English and Hindi), whether it is present, which
    planets and houses are involved, a human-readable description, and the
    overall effect classification (benefic, malefic, or mixed).
    """

    name: str
    name_hindi: str
    is_present: bool
    planets_involved: list[str]
    houses_involved: list[int]
    description: str
    effect: str  # benefic, malefic, mixed
