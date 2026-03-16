"""Domain models for birth chart data."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlanetData:
    """Represents a single planet's position and attributes in a Vedic birth chart.

    Contains the sidereal longitude, sign, nakshatra, house placement, dignity,
    avastha, retrograde/combust status, and other key attributes for one graha.
    """

    name: str
    name_hi: str
    longitude: float          # Sidereal longitude (0-360)
    sign_index: int           # 0-11
    sign: str                 # Vedic sign name
    sign_en: str              # Western sign name
    sign_hi: str              # Hindi sign name
    degree_in_sign: float     # 0-30
    nakshatra_index: int      # 0-26
    nakshatra: str            # Nakshatra name
    nakshatra_lord: str       # Dasha lord of nakshatra
    pada: int                 # 1-4
    house: int                # 1-12 from lagna
    is_retrograde: bool
    speed: float              # deg/day
    dignity: str              # exalted/debilitated/own/mooltrikona/neutral
    avastha: str              # Bala/Kumara/Yuva/Vriddha/Mruta
    is_combust: bool
    sign_lord: str            # Lord of the sign planet is in


@dataclass
class ChartData:
    """Represents a complete Vedic birth chart (Kundali).

    Holds the native's birth details, location, computed ayanamsha, lagna (ascendant)
    information, and a dictionary of all planetary positions keyed by planet name.
    """

    name: str
    dob: str
    tob: str
    place: str
    gender: str
    latitude: float
    longitude: float
    timezone_name: str
    julian_day: float
    ayanamsha: float
    lagna_longitude: float
    lagna_sign_index: int
    lagna_sign: str
    lagna_sign_en: str
    lagna_sign_hi: str
    lagna_degree: float
    planets: dict[str, PlanetData] = field(default_factory=dict)
