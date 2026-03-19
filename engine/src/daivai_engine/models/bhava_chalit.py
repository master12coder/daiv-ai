"""Domain models for Bhava Chalit chart computation."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class BhavaPlanet(BaseModel):
    """Planet's Bhava Chalit position.

    Compares the planet's whole-sign (Rashi) house placement with its
    Placidus-based Bhava Chalit house placement, flagging any shift.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    rashi_house: int = Field(ge=1, le=12)  # House in Rashi chart (whole sign)
    bhava_house: int = Field(ge=1, le=12)  # House in Bhava Chalit
    has_bhava_shift: bool  # True if rashi_house != bhava_house
    cusp_longitude: float = Field(ge=0, lt=360)  # Nearest cusp longitude (sidereal)


class BhavaChalitResult(BaseModel):
    """Bhava Chalit house positions.

    Contains the 12 sidereal house cusp longitudes and per-planet
    Bhava Chalit placements derived from Placidus cusps.
    """

    model_config = ConfigDict(frozen=True)

    cusps: list[float]  # 12 house cusp longitudes (sidereal)
    planets: dict[str, BhavaPlanet]  # keyed by planet name
