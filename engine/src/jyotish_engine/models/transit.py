"""Domain models for planetary transit data."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TransitPlanet(BaseModel):
    """Represents a single planet's transit position overlaid on a natal chart.

    Contains the current sidereal position, sign, nakshatra, retrograde status,
    and which natal house the transit activates.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    longitude: float = Field(ge=0, lt=360)
    sign_index: int = Field(ge=0, le=11)
    sign: str
    degree_in_sign: float = Field(ge=0, lt=30)
    nakshatra: str
    is_retrograde: bool
    natal_house_activated: int = Field(ge=1, le=12)  # Which natal house this transit activates


class TransitData(BaseModel):
    """Represents the complete transit picture for a natal chart at a given date.

    Contains the target date, natal chart reference information, a list of all
    transiting planet positions, and human-readable descriptions of the most
    significant transits (e.g., Sadesati, Jupiter transit, Rahu-Ketu axis).
    """

    model_config = ConfigDict(frozen=True)

    target_date: str
    natal_chart_name: str
    natal_lagna_sign: str
    transits: list[TransitPlanet]
    major_transits: list[str]  # Human-readable descriptions of significant transits
