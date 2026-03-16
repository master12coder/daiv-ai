"""Domain models for Vedic dosha detection results."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DoshaResult:
    """Represents the result of detecting a specific dosha in a chart.

    Contains the dosha name, presence flag, severity level, involved planets
    and houses, a description of the finding, and any cancellation reasons
    that may mitigate the dosha's effects.
    """

    name: str
    name_hindi: str
    is_present: bool
    severity: str          # "full", "partial", "cancelled", "none"
    planets_involved: list[str]
    houses_involved: list[int]
    description: str
    cancellation_reasons: list[str]
