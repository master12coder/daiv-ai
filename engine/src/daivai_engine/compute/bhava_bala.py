"""Bhava Bala (House Strength) — BPHS Chapter 24.

Different from Shadbala (planet strength). Measures how strong each
house is, based on its lord's strength, aspects received, and position.

3 components: Bhavadhipati Bala, Bhava Dig Bala, Bhava Drishti Bala.

Source: BPHS Chapter 24.
"""

from __future__ import annotations

from pydantic import BaseModel

from daivai_engine.compute.chart import get_house_lord
from daivai_engine.compute.strength import compute_shadbala
from daivai_engine.constants import SPECIAL_ASPECTS
from daivai_engine.models.chart import ChartData


_BENEFICS = {"Jupiter", "Venus"}
_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


class BhavaBalaResult(BaseModel):
    """Strength of a single house."""

    house: int  # 1-12
    bhavadhipati_bala: float  # Lord's Shadbala contribution
    bhava_dig_bala: float  # Directional strength of house
    bhava_drishti_bala: float  # Aspect strength
    total: float
    is_strong: bool  # total >= threshold
    rank: int  # 1 = strongest house


def compute_bhava_bala(chart: ChartData) -> list[BhavaBalaResult]:
    """Compute Bhava Bala for all 12 houses.

    Components (BPHS Ch.24):
    1. Bhavadhipati Bala: strength of the house lord (from Shadbala)
    2. Bhava Dig Bala: houses 1,4,7,10 (kendras) strongest,
       then 5,9 (trikonas), then others
    3. Bhava Drishti Bala: benefic aspects add strength,
       malefic aspects reduce it

    Returns:
        List of 12 BhavaBalaResult sorted by total descending, with ranks.
    """
    shadbala = compute_shadbala(chart)
    sb_map = {s.planet: s for s in shadbala}

    results: list[BhavaBalaResult] = []
    for house in range(1, 13):
        lord = get_house_lord(chart, house)
        sb = sb_map.get(lord)

        # 1. Bhavadhipati Bala: lord's total Shadbala / 10 (normalized)
        bhavadhipati = (sb.total / 10.0) if sb else 20.0

        # 2. Bhava Dig Bala — BPHS Ch.24 v5
        # Kendras=60, Trikonas=40, Upachaya(3,6,10,11)=30, Dusthana=15
        if house in (1, 4, 7, 10):
            dig = 60.0
        elif house in (5, 9):
            dig = 40.0
        elif house in (3, 6, 10, 11):
            dig = 30.0
        else:
            dig = 15.0

        # 3. Bhava Drishti Bala: aspects on the house
        drishti = _compute_house_aspects(chart, house)

        total = round(bhavadhipati + dig + drishti, 2)
        results.append(
            BhavaBalaResult(
                house=house,
                bhavadhipati_bala=round(bhavadhipati, 2),
                bhava_dig_bala=dig,
                bhava_drishti_bala=round(drishti, 2),
                total=total,
                is_strong=total >= 80.0,
                rank=0,
            )
        )

    # Assign ranks
    results.sort(key=lambda x: x.total, reverse=True)
    for i, r in enumerate(results):
        results[i] = r.model_copy(update={"rank": i + 1})

    # Re-sort by house number for consistent output
    results.sort(key=lambda x: x.house)
    return results


def _compute_house_aspects(chart: ChartData, house: int) -> float:
    """Compute net aspect strength on a house.

    +15 per benefic aspect, -15 per malefic aspect.
    Occupation counts as aspect too.
    """
    house_sign = (chart.lagna_sign_index + house - 1) % 12
    score = 0.0

    for name, p in chart.planets.items():
        if name in ("Rahu", "Ketu"):
            continue

        # Occupation
        if p.sign_index == house_sign:
            score += 10.0 if name in _BENEFICS else -5.0
            continue

        # 7th aspect (all planets)
        aspected_sign = (p.sign_index + 6) % 12
        if aspected_sign == house_sign:
            score += 15.0 if name in _BENEFICS else -10.0
            continue

        # Special aspects
        for asp_dist in SPECIAL_ASPECTS.get(name, []):
            asp_sign = (p.sign_index + asp_dist - 1) % 12
            if asp_sign == house_sign:
                score += 12.0 if name in _BENEFICS else -8.0
                break

    return score
