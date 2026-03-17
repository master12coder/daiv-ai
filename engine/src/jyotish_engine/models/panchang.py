"""Domain models for Panchang (Hindu almanac) data."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PanchangData(BaseModel):
    """Represents the five limbs of the Hindu Panchang for a given date and location.

    Contains the Vara (weekday), Tithi (lunar day), Nakshatra (lunar mansion),
    Yoga (Sun-Moon combination), Karana (half-tithi), along with sunrise/sunset
    times and inauspicious periods (Rahu Kaal, Yamaghanda, Gulika).
    """

    model_config = ConfigDict(frozen=True)

    date: str
    place: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    vara: str                    # Day of week
    vara_hi: str
    vara_planet: str
    tithi_index: int = Field(ge=0, le=29)  # 0-29
    tithi_name: str
    paksha: str                  # Shukla/Krishna
    nakshatra_index: int = Field(ge=0, le=26)  # 0-26
    nakshatra_name: str
    yoga_index: int = Field(ge=0, le=26)  # 0-26
    yoga_name: str
    karana_index: int
    karana_name: str
    sunrise: str                 # HH:MM local time
    sunset: str                  # HH:MM local time
    rahu_kaal: str               # "HH:MM - HH:MM"
    yamaghanda: str
    gulika: str
