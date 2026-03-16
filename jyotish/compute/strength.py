"""Shadbala and Ashtakavarga — basic planetary strength computation."""

from __future__ import annotations

from dataclasses import dataclass

from jyotish.utils.constants import (
    EXALTATION, DEBILITATION, OWN_SIGNS, MOOLTRIKONA,
    NATURAL_FRIENDS, NATURAL_ENEMIES, NATURAL_NEUTRALS,
    KENDRAS, TRIKONAS, SIGN_LORDS, PLANETS,
)
from jyotish.compute.chart import ChartData


@dataclass
class PlanetStrength:
    planet: str
    sthana_bala: float    # Positional strength (0-1)
    dig_bala: float       # Directional strength (0-1)
    kala_bala: float      # Temporal strength (0-1, simplified)
    total_relative: float # Combined relative strength (0-1)
    rank: int             # Rank among all planets (1=strongest)
    is_strong: bool


def _sthana_bala(chart: ChartData, planet_name: str) -> float:
    """Positional strength based on dignity."""
    p = chart.planets[planet_name]
    dignity_scores = {
        "exalted": 1.0,
        "mooltrikona": 0.85,
        "own": 0.75,
        "neutral": 0.4,
        "debilitated": 0.1,
    }
    return dignity_scores.get(p.dignity, 0.4)


def _dig_bala(chart: ChartData, planet_name: str) -> float:
    """Directional strength — planets are strongest in certain houses.

    Jupiter/Mercury strongest in 1st (East)
    Sun/Mars strongest in 10th (South)
    Saturn strongest in 7th (West)
    Moon/Venus strongest in 4th (North)
    """
    p = chart.planets[planet_name]
    h = p.house

    best_houses = {
        "Sun": 10, "Mars": 10,
        "Jupiter": 1, "Mercury": 1,
        "Saturn": 7,
        "Moon": 4, "Venus": 4,
        "Rahu": 10, "Ketu": 4,
    }

    best = best_houses.get(planet_name, 1)
    distance = abs(h - best)
    if distance > 6:
        distance = 12 - distance

    # Max dig bala at best house, decreasing with distance
    return max(0.0, 1.0 - distance / 6.0)


def _kala_bala_simple(chart: ChartData, planet_name: str) -> float:
    """Simplified temporal strength based on house placement."""
    p = chart.planets[planet_name]
    h = p.house

    if h in KENDRAS:
        return 0.8
    elif h in TRIKONAS:
        return 0.7
    elif h in (3, 6, 10, 11):  # Upachaya
        return 0.5
    elif h in (6, 8, 12):  # Dusthana
        return 0.25
    return 0.4


def compute_planet_strengths(chart: ChartData) -> list[PlanetStrength]:
    """Compute relative strengths for all planets."""
    strengths = []

    for planet_name in PLANETS:
        sb = _sthana_bala(chart, planet_name)
        db = _dig_bala(chart, planet_name)
        kb = _kala_bala_simple(chart, planet_name)

        # Weighted combination
        total = sb * 0.5 + db * 0.25 + kb * 0.25
        strengths.append(PlanetStrength(
            planet=planet_name,
            sthana_bala=round(sb, 3),
            dig_bala=round(db, 3),
            kala_bala=round(kb, 3),
            total_relative=round(total, 3),
            rank=0,
            is_strong=total >= 0.55,
        ))

    # Assign ranks
    strengths.sort(key=lambda s: s.total_relative, reverse=True)
    for i, s in enumerate(strengths):
        s.rank = i + 1

    return strengths


def get_strongest_planet(chart: ChartData) -> str:
    """Return the name of the strongest planet in the chart."""
    strengths = compute_planet_strengths(chart)
    return strengths[0].planet


def get_weakest_planet(chart: ChartData) -> str:
    """Return the name of the weakest planet in the chart."""
    strengths = compute_planet_strengths(chart)
    return strengths[-1].planet
