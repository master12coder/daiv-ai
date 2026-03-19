"""KP Ruling Planets — the 5 planets that rule the current moment.

For any given moment, identifies:
1. Day Lord (weekday ruler)
2. Moon Sign Lord (lord of Moon's current transit sign)
3. Moon Star Lord (nakshatra lord of Moon's position)
4. Moon Sub Lord (KP sub-lord of Moon's position)
5. Lagna Sub Lord (KP sub-lord of current ascending degree)

When a significator becomes a ruling planet, its events activate.

Source: KP Reader 1-6 by K.S. Krishnamurti.
"""

from __future__ import annotations

from datetime import date, datetime

import swisseph as swe
from pydantic import BaseModel

from daivai_engine.compute.kp import get_kp_position
from daivai_engine.constants import (
    DAY_PLANET,
    DEGREES_PER_SIGN,
    SIGN_LORDS,
)


class KPRulingPlanets(BaseModel):
    """The 5 ruling planets for a given moment."""

    day_lord: str
    moon_sign_lord: str
    moon_star_lord: str
    moon_sub_lord: str
    lagna_sub_lord: str
    ruling_planets: list[str]  # Unique list, most frequent first


def compute_kp_ruling(
    target_date: date | None = None,
    lat: float = 25.3176,
    lon: float = 83.0067,
) -> KPRulingPlanets:
    """Compute the 5 KP ruling planets for a given moment.

    Args:
        target_date: Date to compute for. Defaults to today.
        lat: Latitude for lagna computation.
        lon: Longitude for lagna computation.

    Returns:
        KPRulingPlanets with all 5 rulers and the unique list.
    """
    if target_date is None:
        target_date = date.today()

    jd = swe.julday(target_date.year, target_date.month, target_date.day, 12.0)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # 1. Day Lord — weekday ruler
    # Python: Monday=0, Sunday=6. Convert to our mapping (Sunday=0)
    dt = datetime(target_date.year, target_date.month, target_date.day)
    weekday = dt.weekday()  # Monday=0
    day_idx = (weekday + 1) % 7  # Sunday=0
    day_lord = DAY_PLANET.get(day_idx, "Sun")

    # 2-4. Moon position for sign lord, star lord, sub lord
    flags = swe.FLG_SIDEREAL | swe.FLG_SWIEPH
    moon_result = swe.calc_ut(jd, swe.MOON, flags)
    moon_lon: float = moon_result[0][0]  # type: ignore[index]

    moon_sign = int(moon_lon / DEGREES_PER_SIGN) % 12
    moon_sign_lord = SIGN_LORDS[moon_sign]

    moon_star_lord, moon_sub_lord, _ = get_kp_position(moon_lon)

    # 5. Lagna sub lord — compute lagna for this moment
    # Use swe.houses_ex for sidereal lagna
    _cusps, ascs = swe.houses_ex(jd, lat, lon, b"P", flags)  # type: ignore[arg-type]
    lagna_lon: float = ascs[0]  # type: ignore[index]
    _, lagna_sub_lord, _ = get_kp_position(lagna_lon)

    # Compile unique ruling planets (most frequent first)
    all_five = [day_lord, moon_sign_lord, moon_star_lord, moon_sub_lord, lagna_sub_lord]
    from collections import Counter

    counts = Counter(all_five)
    unique = sorted(counts.keys(), key=lambda p: (-counts[p], all_five.index(p)))

    return KPRulingPlanets(
        day_lord=day_lord,
        moon_sign_lord=moon_sign_lord,
        moon_star_lord=moon_star_lord,
        moon_sub_lord=moon_sub_lord,
        lagna_sub_lord=lagna_sub_lord,
        ruling_planets=unique,
    )
