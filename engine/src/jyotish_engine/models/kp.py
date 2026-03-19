"""KP (Krishnamurti Paddhati) data models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class KPPosition(BaseModel):
    """KP sub-lord position for a planet or cusp."""

    model_config = ConfigDict(frozen=True)

    name: str  # Planet name or cusp name
    longitude: float = Field(ge=0, lt=360)  # Sidereal longitude
    sign_lord: str  # Lord of the sign
    nakshatra_lord: str  # Star lord (nakshatra lord)
    sub_lord: str  # Sub lord
    sub_sub_lord: str  # Sub-sub lord
    nakshatra: str  # Nakshatra name
