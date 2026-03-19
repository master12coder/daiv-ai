"""Narayana Dasha — Jaimini's most versatile rashi (sign-based) dasha.

Direction (forward/backward) depends on sign nature (odd/even).
Duration based on lord's distance from the sign.

Source: Jaimini Upadesa Sutras, PVR Narasimha Rao's interpretation.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from daivai_engine.constants import SIGN_LORDS
from daivai_engine.models.chart import ChartData
from daivai_engine.models.dasha import DashaPeriod


# Odd signs (count forward): Aries(0), Gemini(2), Leo(4), Libra(6), Sag(8), Aquarius(10)
_ODD_SIGNS = {0, 2, 4, 6, 8, 10}


def compute_narayana_dasha(chart: ChartData) -> list[DashaPeriod]:
    """Compute Narayana Dasha periods for a birth chart.

    Algorithm (Jaimini Sutras):
    1. Start from lagna sign
    2. Direction: odd lagna → forward, even lagna → backward
    3. Duration: count from sign to its lord's position
    4. Cycle through all 12 signs

    Args:
        chart: Computed birth chart.

    Returns:
        List of 12 DashaPeriod objects (one per sign).
    """
    lagna = chart.lagna_sign_index
    is_odd = lagna in _ODD_SIGNS
    start_dt = _birth_datetime(chart)

    periods: list[DashaPeriod] = []
    current = start_dt

    for i in range(12):
        # Sign index for this dasha
        if is_odd:
            sign_idx = (lagna + i) % 12
        else:
            sign_idx = (lagna - i) % 12

        duration_years = _sign_duration(sign_idx, chart)

        end = current + timedelta(days=duration_years * 365.25)
        periods.append(
            DashaPeriod(
                level="ND",  # Narayana Dasha
                lord=SIGN_LORDS[sign_idx],
                start=current,
                end=end,
                parent_lord=None,
            )
        )
        current = end

    return periods


def _sign_duration(sign_idx: int, chart: ChartData) -> int:
    """Compute dasha duration for a sign in years.

    Count from the sign to where its lord is placed.
    Odd signs: count forward. Even signs: count backward.
    Max 12 years. If lord in own sign: 12 years.

    Source: Jaimini Sutras, Narasimha Rao interpretation.
    """
    lord_name = SIGN_LORDS[sign_idx]
    lord_planet = chart.planets.get(lord_name)
    if lord_planet is None:
        return 1  # Fallback for Rahu/Ketu lords

    lord_sign = lord_planet.sign_index

    # If lord is in own sign → 12 years
    if lord_sign == sign_idx:
        return 12

    # Count distance
    if sign_idx in _ODD_SIGNS:
        # Forward count
        distance = (lord_sign - sign_idx) % 12
    else:
        # Backward count
        distance = (sign_idx - lord_sign) % 12

    # Distance 0 means same sign → 12
    if distance == 0:
        return 12

    return min(distance, 12)


def _birth_datetime(chart: ChartData) -> datetime:
    """Extract birth datetime from chart."""
    from daivai_engine.compute.datetime_utils import parse_birth_datetime

    return parse_birth_datetime(chart.dob, chart.tob, chart.timezone_name)
