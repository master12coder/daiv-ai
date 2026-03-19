"""Saham Points (Sensitive Points / Arabic Parts adapted for Vedic).

Traditional Tajaka/Varshphal sahams computed from lagna, planets,
and house cusps. Used primarily in annual chart interpretation.

Source: Tajaka Neelakanthi, Uttarakalamrita.
"""

from __future__ import annotations

from pydantic import BaseModel

from daivai_engine.constants import (
    DEGREES_PER_SIGN,
    FULL_CIRCLE_DEG,
    NAKSHATRA_SPAN_DEG,
    NAKSHATRAS,
    SIGNS_EN,
    SIGNS_HI,
)
from daivai_engine.models.chart import ChartData


class SahamPoint(BaseModel):
    """A single sensitive point."""

    name: str  # Punya, Vivaha, Putra, etc.
    name_hi: str
    longitude: float  # Sidereal, 0-360
    sign_index: int
    sign_hi: str
    sign_en: str
    degree_in_sign: float
    nakshatra: str


def compute_sahams(chart: ChartData) -> list[SahamPoint]:
    """Compute traditional Saham (sensitive) points.

    Formulas (Tajaka Neelakanthi):
    - Punya Saham (Fortune): Lagna + Moon - Sun (day), Lagna + Sun - Moon (night)
    - Vivaha (Marriage): Lagna + Venus - 7th cusp
    - Putra (Children): Lagna + Jupiter - 5th cusp
    - Karma (Career): Lagna + Saturn - 10th cusp
    - Vidya (Education): Lagna + Mercury - 5th cusp
    - Mrityu (Death): Lagna + 8th cusp - Moon

    Day/night determined by Sun above/below horizon (simplified: Sun in houses 7-12 = day).

    Args:
        chart: Computed birth chart.

    Returns:
        List of SahamPoint objects.
    """
    lagna_lon = chart.lagna_longitude
    sun = chart.planets["Sun"].longitude
    moon = chart.planets["Moon"].longitude
    venus = chart.planets["Venus"].longitude
    jupiter = chart.planets["Jupiter"].longitude
    saturn = chart.planets["Saturn"].longitude
    mercury = chart.planets["Mercury"].longitude

    # House cusps (whole sign, approximate)
    cusp_5 = (chart.lagna_sign_index + 4) * DEGREES_PER_SIGN
    cusp_7 = (chart.lagna_sign_index + 6) * DEGREES_PER_SIGN
    cusp_8 = (chart.lagna_sign_index + 7) * DEGREES_PER_SIGN
    cusp_10 = (chart.lagna_sign_index + 9) * DEGREES_PER_SIGN

    # Day/night: Sun in houses 7-12 = day birth (above horizon)
    sun_house = chart.planets["Sun"].house
    is_day = sun_house >= 7

    # Punya Saham — Tajaka Neelakanthi Ch.3
    if is_day:
        punya_lon = (lagna_lon + moon - sun) % FULL_CIRCLE_DEG
    else:
        punya_lon = (lagna_lon + sun - moon) % FULL_CIRCLE_DEG

    sahams = [
        _make("Punya Saham", "पुण्य सहम", punya_lon),
        _make("Vivaha Saham", "विवाह सहम", (lagna_lon + venus - cusp_7) % FULL_CIRCLE_DEG),
        _make("Putra Saham", "पुत्र सहम", (lagna_lon + jupiter - cusp_5) % FULL_CIRCLE_DEG),
        _make("Karma Saham", "कर्म सहम", (lagna_lon + saturn - cusp_10) % FULL_CIRCLE_DEG),
        _make("Vidya Saham", "विद्या सहम", (lagna_lon + mercury - cusp_5) % FULL_CIRCLE_DEG),
        _make("Mrityu Saham", "मृत्यु सहम", (lagna_lon + cusp_8 - moon) % FULL_CIRCLE_DEG),
    ]
    return sahams


def _make(name: str, name_hi: str, longitude: float) -> SahamPoint:
    """Build a SahamPoint from longitude."""
    sign_idx = int(longitude / DEGREES_PER_SIGN) % 12
    deg = longitude - sign_idx * DEGREES_PER_SIGN
    nak_idx = int(longitude / NAKSHATRA_SPAN_DEG)
    if nak_idx >= 27:
        nak_idx = 26
    return SahamPoint(
        name=name,
        name_hi=name_hi,
        longitude=round(longitude, 4),
        sign_index=sign_idx,
        sign_hi=SIGNS_HI[sign_idx],
        sign_en=SIGNS_EN[sign_idx],
        degree_in_sign=round(deg, 4),
        nakshatra=NAKSHATRAS[nak_idx],
    )
