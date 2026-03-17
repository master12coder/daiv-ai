"""Domain models for daily suggestion computation."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TransitImpact(BaseModel):
    """Impact of a single transiting planet on the natal chart."""

    model_config = ConfigDict(frozen=True)

    planet: str
    transit_sign: str
    natal_house: int = Field(ge=1, le=12)
    bindus: int = Field(ge=0, le=8)
    is_favorable: bool
    description: str


class DailySuggestion(BaseModel):
    """Complete daily suggestion computed without LLM."""

    model_config = ConfigDict(frozen=True)

    date: str
    vara: str
    vara_planet: str
    recommended_color: str
    recommended_mantra: str
    good_for: list[str]
    avoid: list[str]
    transit_impacts: list[TransitImpact]
    health_focus: str
    day_rating: int = Field(ge=1, le=10)  # 1-MAX_DAY_RATING
    rahu_kaal: str
    nakshatra: str
    tithi: str
