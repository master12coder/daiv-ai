"""Domain models for Ashtakoot (36 Guna) marriage matching."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class KootaScore:
    """Represents the score for a single koota (compatibility factor) in Ashtakoot matching.

    Each koota has a name, maximum possible points, obtained points, and a
    description of how the score was determined.
    """

    name: str
    name_hindi: str
    max_points: float
    obtained: float
    description: str


@dataclass
class MatchingResult:
    """Represents the complete Ashtakoot (36 Guna) matching result between two persons.

    Contains the Moon sign and nakshatra indices for both persons, the list of
    individual koota scores, the aggregate totals, percentage, and a human-readable
    recommendation.
    """

    person1_nakshatra_index: int
    person1_moon_sign: int
    person2_nakshatra_index: int
    person2_moon_sign: int
    kootas: list[KootaScore]
    total_obtained: float
    total_max: float
    percentage: float
    recommendation: str
