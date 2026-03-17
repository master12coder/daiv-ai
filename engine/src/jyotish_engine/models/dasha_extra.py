"""Additional dasha system data models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class YoginiDashaPeriod(BaseModel):
    """A Yogini Dasha period."""

    model_config = ConfigDict(frozen=True)

    yogini_name: str       # Mangala, Pingala, Dhanya, etc.
    planet: str            # Associated planet
    years: int             # Duration in years
    start: datetime
    end: datetime


class AshtottariDashaPeriod(BaseModel):
    """An Ashtottari Dasha period."""

    model_config = ConfigDict(frozen=True)

    planet: str
    years: int
    start: datetime
    end: datetime


class CharaDashaPeriod(BaseModel):
    """A Chara (Jaimini) sign-based dasha period."""

    model_config = ConfigDict(frozen=True)

    sign: str
    sign_index: int = 0
    years: float
    start: datetime
    end: datetime
