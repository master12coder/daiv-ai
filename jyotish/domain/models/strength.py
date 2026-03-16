"""Domain models for planetary strength (Shadbala) computation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlanetStrength:
    """Represents the computed strength of a planet based on simplified Shadbala factors.

    Includes positional strength (sthana bala), directional strength (dig bala),
    temporal strength (kala bala), a combined relative score, a rank among all
    planets, and a boolean indicating whether the planet is considered strong.
    """

    planet: str
    sthana_bala: float    # Positional strength (0-1)
    dig_bala: float       # Directional strength (0-1)
    kala_bala: float      # Temporal strength (0-1, simplified)
    total_relative: float # Combined relative strength (0-1)
    rank: int             # Rank among all planets (1=strongest)
    is_strong: bool
