"""Bhava Chalit vs Whole Sign house comparison.

When a planet shifts houses between whole sign and bhava chalit,
this creates a critical interpretive difference that must be flagged.

Source: BPHS — widely debated; both systems have merit.
"""

from __future__ import annotations

from pydantic import BaseModel

from daivai_engine.compute.bhava_chalit import get_bhava_shifted_planets
from daivai_engine.models.chart import ChartData


class HouseShift(BaseModel):
    """A planet that changes house between whole sign and bhava chalit."""

    planet: str
    rashi_house: int  # Whole sign house
    bhava_house: int  # Bhava chalit house
    explanation: str


def compare_whole_sign_vs_chalit(chart: ChartData) -> list[HouseShift]:
    """Find all planets that shift houses between systems.

    Args:
        chart: Computed birth chart.

    Returns:
        List of HouseShift for planets that differ. Empty if all match.
    """
    shifted = get_bhava_shifted_planets(chart)
    results: list[HouseShift] = []

    for bp in shifted:
        if bp.has_bhava_shift:
            results.append(
                HouseShift(
                    planet=bp.name,
                    rashi_house=bp.rashi_house,
                    bhava_house=bp.bhava_house,
                    explanation=(
                        f"{bp.name} is in house {bp.rashi_house} by whole sign "
                        f"but house {bp.bhava_house} by bhava chalit. "
                        f"Both houses' significations apply."
                    ),
                )
            )

    return results
