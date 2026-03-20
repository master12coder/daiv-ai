"""Kalachakra Dasha — "most respectable dasha" per Parashar (BPHS Ch.46).

The Wheel of Time dasha. Based on Moon's nakshatra PADA, not just nakshatra.
Uses a 9-sign cycle of 100 years with Savya (direct) and Apasavya (reverse)
directions. Each sign has a fixed duration. The cycle direction depends on
whether Moon's pada falls in an odd or even sign.

Key concepts:
- DEHA (Body): Cancer in Savya, Cancer in Apasavya — physical events
- JEEVA (Soul): Sagittarius in Savya, Sagittarius in Apasavya — spiritual events
- When DEHA or JEEVA dasha runs, those life areas are activated

Algorithm (BPHS Chapter 46):
1. Find Moon's longitude → determine sign (0-11) and pada within sign (0-8)
2. Odd sign (Aries=0, Gemini=2, Leo=4, Libra=6, Sag=8, Aquarius=10) → Savya
   Even sign (Taurus=1, Cancer=3, Virgo=5, Scorpio=7, Cap=9, Pisces=11) → Apasavya
3. The pada number (0-8) within the sign determines the STARTING position
   in the 9-sign dasha sequence
4. Balance = remaining fraction of the pada x years of that starting sign
5. Subsequent dashas follow the cycle from that starting position

Sign durations (BPHS Ch.46 v3-5):
  Savya:    Aries(7), Taurus(16), Gemini(9), Cancer(21), Leo(5),
            Virgo(9), Libra(16), Scorpio(7), Sagittarius(10) = 100 years
  Apasavya: Sagittarius(10), Scorpio(7), Libra(16), Virgo(9), Leo(5),
            Cancer(21), Gemini(9), Taurus(16), Aries(7) = 100 years

Source: BPHS Chapter 46 "Kalachakra Dasha Adhyaya"
Cross-reference: Girish Chand Sharma commentary, PVR Narasimha Rao interpretation
"""

from __future__ import annotations

from datetime import datetime, timedelta

from pydantic import BaseModel, ConfigDict

from daivai_engine.constants import DEGREES_PER_SIGN, SIGNS, SIGNS_HI
from daivai_engine.models.chart import ChartData


class KalachakraDashaPeriod(BaseModel):
    """One period in the Kalachakra Dasha sequence."""

    model_config = ConfigDict(frozen=True)

    sign_index: int  # 0-11
    sign_name: str  # Vedic sign name
    sign_hi: str  # Hindi sign name
    years: int  # Duration in years
    start: datetime
    end: datetime
    is_deha: bool  # Body — physical events activated
    is_jeeva: bool  # Soul — spiritual events activated
    cycle: str  # "savya" or "apasavya"


class KalachakraDashaResult(BaseModel):
    """Complete Kalachakra Dasha result."""

    model_config = ConfigDict(frozen=True)

    cycle_type: str  # "savya" or "apasavya"
    moon_sign_index: int
    pada_in_sign: int  # 0-8 (which of the 9 padas within the sign)
    starting_position: int  # Index in the 9-sign sequence
    balance_years: float  # Remaining years of first dasha
    periods: list[KalachakraDashaPeriod]
    deha_sign: int  # Sign index of DEHA point
    jeeva_sign: int  # Sign index of JEEVA point


# ── Kalachakra constants (BPHS Chapter 46 v3-5) ─────────────────────────

# Savya (direct/clockwise) cycle — for Moon pada in ODD signs
# Sign indices and their dasha durations in years
_SAVYA_SIGNS = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Aries → Sagittarius
_SAVYA_YEARS = [7, 16, 9, 21, 5, 9, 16, 7, 10]  # Total = 100

# Apasavya (reverse/counter-clockwise) cycle — for Moon pada in EVEN signs
_APASAVYA_SIGNS = [8, 7, 6, 5, 4, 3, 2, 1, 0]  # Sagittarius → Aries
_APASAVYA_YEARS = [10, 7, 16, 9, 5, 21, 9, 16, 7]  # Total = 100

# DEHA and JEEVA signs — BPHS Ch.46 v8-10
# DEHA (Body): Cancer (index 3) — physical health, material life
# JEEVA (Soul): Sagittarius (index 8) — spiritual growth, inner life
_DEHA_SIGN = 3  # Cancer
_JEEVA_SIGN = 8  # Sagittarius

# Kalachakra total cycle = 100 years (not 120 like Vimshottari)
_TOTAL_YEARS = 100

# Each sign contains 9 nakshatra padas
# Pada span within a sign = 30° / 9 = 3.3333° = 3°20'
_PADA_SPAN = DEGREES_PER_SIGN / 9.0  # 3.3333...°

# Odd signs (0-indexed): Aries=0, Gemini=2, Leo=4, Libra=6, Sag=8, Aquarius=10
_ODD_SIGNS = {0, 2, 4, 6, 8, 10}


def compute_kalachakra_dasha(chart: ChartData) -> KalachakraDashaResult:
    """Compute Kalachakra Dasha for a birth chart.

    The "most respectable dasha" per Parashar. Based on Moon's nakshatra
    pada position within its sign. Uses a 100-year cycle through 9 signs.

    Algorithm:
    1. Moon's degree in sign → pada within sign (0-8)
    2. Sign odd/even → Savya/Apasavya cycle
    3. Pada number → starting position in the 9-sign sequence
    4. Balance from Moon's position within the pada
    5. Generate all 9 periods with dates

    Args:
        chart: Computed birth chart with Moon position.

    Returns:
        KalachakraDashaResult with all 9 periods and DEHA/JEEVA markers.

    Source: BPHS Chapter 46.
    """
    moon = chart.planets["Moon"]

    # Step 1: Find pada within sign (0-8)
    # Each sign has 9 padas of 3°20' each
    pada_in_sign = int(moon.degree_in_sign / _PADA_SPAN)
    if pada_in_sign > 8:
        pada_in_sign = 8

    # Step 2: Determine cycle direction
    # Odd signs (0,2,4,6,8,10) → Savya (direct)
    # Even signs (1,3,5,7,9,11) → Apasavya (reverse)
    is_savya = moon.sign_index in _ODD_SIGNS
    cycle_type = "savya" if is_savya else "apasavya"

    signs = _SAVYA_SIGNS if is_savya else _APASAVYA_SIGNS
    years = _SAVYA_YEARS if is_savya else _APASAVYA_YEARS

    # Step 3: Starting position = pada number within the sign
    # Pada 0 → start from position 0 (first sign in cycle)
    # Pada 4 → start from position 4 (5th sign in cycle)
    start_pos = pada_in_sign

    # Step 4: Calculate balance of first dasha
    # Moon's position within the current pada
    degree_in_pada = moon.degree_in_sign - pada_in_sign * _PADA_SPAN
    fraction_elapsed = degree_in_pada / _PADA_SPAN
    balance_fraction = 1.0 - fraction_elapsed
    first_dasha_years = years[start_pos]
    balance_years = first_dasha_years * balance_fraction

    # Step 5: Generate all 9 dasha periods
    from daivai_engine.compute.datetime_utils import parse_birth_datetime

    birth_dt = parse_birth_datetime(chart.dob, chart.tob, chart.timezone_name)
    periods: list[KalachakraDashaPeriod] = []
    current = birth_dt

    for i in range(9):
        pos = (start_pos + i) % 9
        sign_idx = signs[pos]
        dasha_years = years[pos]

        # First period uses balance, rest use full duration
        if i == 0:
            actual_years = balance_years
        else:
            actual_years = float(dasha_years)

        end = current + timedelta(days=actual_years * 365.25)

        periods.append(
            KalachakraDashaPeriod(
                sign_index=sign_idx,
                sign_name=SIGNS[sign_idx],
                sign_hi=SIGNS_HI[sign_idx],
                years=dasha_years,
                start=current,
                end=end,
                is_deha=sign_idx == _DEHA_SIGN,
                is_jeeva=sign_idx == _JEEVA_SIGN,
                cycle=cycle_type,
            )
        )
        current = end

    return KalachakraDashaResult(
        cycle_type=cycle_type,
        moon_sign_index=moon.sign_index,
        pada_in_sign=pada_in_sign,
        starting_position=start_pos,
        balance_years=round(balance_years, 4),
        periods=periods,
        deha_sign=_DEHA_SIGN,
        jeeva_sign=_JEEVA_SIGN,
    )
