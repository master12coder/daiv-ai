"""Domain models for planetary transit data."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TransitPlanet:
    """Represents a single planet's transit position overlaid on a natal chart.

    Contains the current sidereal position, sign, nakshatra, retrograde status,
    and which natal house the transit activates.
    """

    name: str
    longitude: float
    sign_index: int
    sign: str
    degree_in_sign: float
    nakshatra: str
    is_retrograde: bool
    natal_house_activated: int  # Which natal house this transit activates


@dataclass
class TransitData:
    """Represents the complete transit picture for a natal chart at a given date.

    Contains the target date, natal chart reference information, a list of all
    transiting planet positions, and human-readable descriptions of the most
    significant transits (e.g., Sadesati, Jupiter transit, Rahu-Ketu axis).
    """

    target_date: str
    natal_chart_name: str
    natal_lagna_sign: str
    transits: list[TransitPlanet]
    major_transits: list[str]  # Human-readable descriptions of significant transits
