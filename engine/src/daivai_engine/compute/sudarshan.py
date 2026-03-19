"""Sudarshan Chakra — triple chart analysis from Lagna, Moon, and Sun.

Simultaneously analyzes houses from three reference points to give
a comprehensive strength assessment for each house.

Source: BPHS, widely used in traditional North Indian practice.
"""

from __future__ import annotations

from pydantic import BaseModel

from daivai_engine.constants import SIGN_LORDS
from daivai_engine.models.chart import ChartData


class SudarshanHouse(BaseModel):
    """Triple-reference analysis for one house."""

    house: int  # 1-12
    # From Lagna
    lagna_lord: str
    lagna_occupants: list[str]
    # From Moon
    moon_lord: str
    moon_occupants: list[str]
    # From Sun
    sun_lord: str
    sun_occupants: list[str]
    # Aggregate
    strength: str  # triple_strong / double_strong / mixed / weak


class SudarshanChakra(BaseModel):
    """Complete Sudarshan Chakra analysis for all 12 houses."""

    houses: list[SudarshanHouse]


def compute_sudarshan(chart: ChartData) -> SudarshanChakra:
    """Compute Sudarshan Chakra — triple chart analysis.

    For each house 1-12:
    - Check lord and occupants from Lagna sign
    - Check lord and occupants from Moon sign
    - Check lord and occupants from Sun sign
    - Classify aggregate strength

    Args:
        chart: Computed birth chart.

    Returns:
        SudarshanChakra with all 12 houses analyzed.
    """
    lagna_idx = chart.lagna_sign_index
    moon_idx = chart.planets["Moon"].sign_index
    sun_idx = chart.planets["Sun"].sign_index

    houses: list[SudarshanHouse] = []
    for house in range(1, 13):
        l_sign = (lagna_idx + house - 1) % 12
        m_sign = (moon_idx + house - 1) % 12
        s_sign = (sun_idx + house - 1) % 12

        l_occ = _occupants(chart, l_sign)
        m_occ = _occupants(chart, m_sign)
        s_occ = _occupants(chart, s_sign)

        # Strength: count how many references have benefic planets/lords
        strong_count = sum(
            [
                _is_strong(l_occ, SIGN_LORDS[l_sign]),
                _is_strong(m_occ, SIGN_LORDS[m_sign]),
                _is_strong(s_occ, SIGN_LORDS[s_sign]),
            ]
        )

        if strong_count == 3:
            strength = "triple_strong"
        elif strong_count == 2:
            strength = "double_strong"
        elif strong_count == 1:
            strength = "mixed"
        else:
            strength = "weak"

        houses.append(
            SudarshanHouse(
                house=house,
                lagna_lord=SIGN_LORDS[l_sign],
                lagna_occupants=l_occ,
                moon_lord=SIGN_LORDS[m_sign],
                moon_occupants=m_occ,
                sun_lord=SIGN_LORDS[s_sign],
                sun_occupants=s_occ,
                strength=strength,
            )
        )

    return SudarshanChakra(houses=houses)


def _occupants(chart: ChartData, sign_idx: int) -> list[str]:
    """Get planet names occupying a given sign."""
    return [name for name, p in chart.planets.items() if p.sign_index == sign_idx]


def _is_strong(occupants: list[str], lord: str) -> bool:
    """Check if a house reference is strong (has benefic or natural benefic lord)."""
    # Natural benefics: Jupiter, Venus, well-placed Mercury, Moon (Shukla)
    benefics = {"Jupiter", "Venus"}
    return bool(
        (occupants and any(p in benefics for p in occupants))
        or lord in benefics
        or len(occupants) >= 2
    )
