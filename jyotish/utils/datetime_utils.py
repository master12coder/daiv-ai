"""IST conversion, Julian Day helpers."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta

import swisseph as swe
import pytz


IST = timezone(timedelta(hours=5, minutes=30))


def to_jd(dt: datetime) -> float:
    """Convert a datetime to Julian Day (UT)."""
    utc_dt = dt.astimezone(timezone.utc)
    hour_frac = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour_frac)
    return jd


def from_jd(jd: float) -> datetime:
    """Convert Julian Day to UTC datetime."""
    year, month, day, hour_frac = swe.revjul(jd)
    hours = int(hour_frac)
    remainder = (hour_frac - hours) * 60
    minutes = int(remainder)
    seconds = int((remainder - minutes) * 60)
    return datetime(year, month, day, hours, minutes, seconds, tzinfo=timezone.utc)


def parse_birth_datetime(
    dob: str,
    tob: str,
    tz_name: str = "Asia/Kolkata",
) -> datetime:
    """Parse DOB (DD/MM/YYYY) and TOB (HH:MM) into timezone-aware datetime."""
    day, month, year = dob.split("/")
    hour, minute = tob.split(":")
    tz = pytz.timezone(tz_name)
    naive = datetime(int(year), int(month), int(day), int(hour), int(minute))
    return tz.localize(naive)


def now_ist() -> datetime:
    """Current time in IST."""
    return datetime.now(IST)


def compute_sunrise(jd: float, lat: float, lon: float) -> float:
    """Compute sunrise Julian Day for a given date and location."""
    # swe.rise_trans(tjdut, body, rsmi, geopos, atpress, attemp)
    rsmi = swe.CALC_RISE | swe.BIT_DISC_CENTER
    result = swe.rise_trans(
        jd - 0.5,  # Start searching from previous noon
        swe.SUN,
        rsmi,
        (lon, lat, 0),  # geopos: lon, lat, altitude
        1013.25,  # atmospheric pressure
        15.0,  # atmospheric temperature
    )
    return result[1][0]


def compute_sunset(jd: float, lat: float, lon: float) -> float:
    """Compute sunset Julian Day for a given date and location."""
    rsmi = swe.CALC_SET | swe.BIT_DISC_CENTER
    result = swe.rise_trans(
        jd - 0.5,
        swe.SUN,
        rsmi,
        (lon, lat, 0),
        1013.25,
        15.0,
    )
    return result[1][0]
