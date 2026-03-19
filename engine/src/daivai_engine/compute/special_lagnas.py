"""Special Lagnas — Hora Lagna, Bhava Lagna, Ghatika Lagna.

All three are computed from the time elapsed since sunrise.
They provide specialized ascendant points for wealth, personality,
and timing analysis respectively.

Source: BPHS Chapter 5.
"""

from __future__ import annotations

from pydantic import BaseModel

from daivai_engine.compute.datetime_utils import compute_sunrise
from daivai_engine.constants import DEGREES_PER_SIGN, FULL_CIRCLE_DEG, SIGNS_EN, SIGNS_HI
from daivai_engine.models.chart import ChartData


class SpecialLagna(BaseModel):
    """A special ascendant point (Hora/Bhava/Ghatika)."""

    name: str
    longitude: float  # Sidereal longitude 0-360
    sign_index: int
    sign_hi: str
    sign_en: str
    degree_in_sign: float


def compute_special_lagnas(chart: ChartData) -> dict[str, SpecialLagna]:
    """Compute Hora Lagna, Bhava Lagna, and Ghatika Lagna.

    All require sunrise time at birth location on birth date.
    1 ghatika = 24 minutes = 1/60th of a day.

    Args:
        chart: Computed birth chart (needs julian_day, lat, lon).

    Returns:
        Dict with keys 'hora', 'bhava', 'ghatika'.
    """
    birth_jd = chart.julian_day
    sunrise_jd = compute_sunrise(birth_jd, chart.latitude, chart.longitude)

    # Time elapsed from sunrise in ghatikas (1 ghatika = 24 min = 1/60 day)
    elapsed_days = birth_jd - sunrise_jd
    if elapsed_days < 0:
        # Born before sunrise → use previous day's sunrise
        elapsed_days += 1.0
    ghatikas = elapsed_days * 60.0  # 60 ghatikas per day

    # Sun longitude at sunrise (approximate: use birth chart Sun)
    sun_lon = chart.planets["Sun"].longitude
    lagna_lon = chart.lagna_longitude

    # HORA LAGNA (BPHS Ch.5): advances 1 sign per 2.5 ghatikas
    # Hora Lagna = Sun longitude + (ghatikas x 15°)
    # Each ghatika advances by half a sign (15°)
    hora_lon = (sun_lon + ghatikas * 15.0) % FULL_CIRCLE_DEG

    # BHAVA LAGNA (BPHS Ch.5): advances 1 sign per 5 ghatikas
    # Bhava Lagna = Sunrise Lagna + (ghatikas x 6°)
    bhava_lon = (lagna_lon + ghatikas * 6.0) % FULL_CIRCLE_DEG

    # GHATIKA LAGNA (BPHS Ch.5): advances 1 sign per ghatika (24 min)
    # Ghatika Lagna = Sunrise Lagna + (ghatikas x 30°)
    ghatika_lon = (lagna_lon + ghatikas * DEGREES_PER_SIGN) % FULL_CIRCLE_DEG

    return {
        "hora": _make_lagna("Hora Lagna", hora_lon),
        "bhava": _make_lagna("Bhava Lagna", bhava_lon),
        "ghatika": _make_lagna("Ghatika Lagna", ghatika_lon),
    }


def _make_lagna(name: str, longitude: float) -> SpecialLagna:
    """Build a SpecialLagna from a longitude."""
    sign_idx = int(longitude / DEGREES_PER_SIGN) % 12
    deg = longitude - sign_idx * DEGREES_PER_SIGN
    return SpecialLagna(
        name=name,
        longitude=round(longitude, 4),
        sign_index=sign_idx,
        sign_hi=SIGNS_HI[sign_idx],
        sign_en=SIGNS_EN[sign_idx],
        degree_in_sign=round(deg, 4),
    )
