"""Argala — Jaimini's intervention/support system.

Determines which planets support or obstruct each house's results
through specific positional relationships.

Source: Jaimini Sutras Chapter 1, Quarter 1.
"""

from __future__ import annotations

from pydantic import BaseModel

from daivai_engine.models.chart import ChartData


class ArgalaResult(BaseModel):
    """Argala analysis for one house."""

    house: int  # Target house (1-12)
    # Argala providers (planets supporting this house)
    dhana_argala: list[str]  # Planets in 2nd from house
    sukha_argala: list[str]  # Planets in 4th from house
    labha_argala: list[str]  # Planets in 11th from house
    putra_argala: list[str]  # Planets in 5th from house
    # Obstructors
    dhana_obstructed: bool  # Planet in 12th cancels dhana argala
    sukha_obstructed: bool  # Planet in 10th cancels sukha argala
    labha_obstructed: bool  # Planet in 3rd cancels labha argala
    # Net result
    net_argala_count: int  # Total unobstructed argalas
    is_supported: bool  # net > 0


# Argala positions relative to target house (Jaimini Sutras 1.1.10-15)
# (argala_offset, obstruction_offset, name)
_ARGALA_RULES = [
    (2, 12, "dhana"),  # 2nd supports, 12th obstructs
    (4, 10, "sukha"),  # 4th supports, 10th obstructs
    (11, 3, "labha"),  # 11th supports, 3rd obstructs
    (5, 0, "putra"),  # 5th supports, no standard obstruction
]


def compute_argala(chart: ChartData) -> list[ArgalaResult]:
    """Compute Argala for all 12 houses.

    For each house, checks which planets provide argala from
    the 2nd, 4th, 5th, and 11th positions, and whether planets
    in the 12th, 10th, or 3rd obstruct those argalas.

    Args:
        chart: Computed birth chart.

    Returns:
        List of 12 ArgalaResult objects, one per house.
    """
    # Build sign → planets mapping
    sign_planets: dict[int, list[str]] = {}
    for name, p in chart.planets.items():
        sign_planets.setdefault(p.sign_index, []).append(name)

    results: list[ArgalaResult] = []
    for house in range(1, 13):
        house_sign = (chart.lagna_sign_index + house - 1) % 12

        dhana = _planets_at_offset(house_sign, 2, sign_planets)
        sukha = _planets_at_offset(house_sign, 4, sign_planets)
        labha = _planets_at_offset(house_sign, 11, sign_planets)
        putra = _planets_at_offset(house_sign, 5, sign_planets)

        # Obstructions: planets in obstruction position with FEWER planets
        # than the argala position cancel the argala (Jaimini rule:
        # obstruction only works if obstructor has fewer/equal planets)
        obs_12 = _planets_at_offset(house_sign, 12, sign_planets)
        obs_10 = _planets_at_offset(house_sign, 10, sign_planets)
        obs_3 = _planets_at_offset(house_sign, 3, sign_planets)

        d_obstructed = len(obs_12) >= len(dhana) > 0 if dhana else False
        s_obstructed = len(obs_10) >= len(sukha) > 0 if sukha else False
        l_obstructed = len(obs_3) >= len(labha) > 0 if labha else False

        # Count unobstructed argalas
        net = 0
        if dhana and not d_obstructed:
            net += 1
        if sukha and not s_obstructed:
            net += 1
        if labha and not l_obstructed:
            net += 1
        if putra:
            net += 1  # Putra argala has no standard obstruction

        results.append(
            ArgalaResult(
                house=house,
                dhana_argala=dhana,
                sukha_argala=sukha,
                labha_argala=labha,
                putra_argala=putra,
                dhana_obstructed=d_obstructed,
                sukha_obstructed=s_obstructed,
                labha_obstructed=l_obstructed,
                net_argala_count=net,
                is_supported=net > 0,
            )
        )

    return results


def _planets_at_offset(
    base_sign: int, offset: int, sign_planets: dict[int, list[str]]
) -> list[str]:
    """Get planets at a given sign offset from base."""
    target_sign = (base_sign + offset - 1) % 12
    return sign_planets.get(target_sign, [])
