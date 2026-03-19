"""Upagraha (shadow planet) data models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class UpagrahaPosition(BaseModel):
    """Position of an Upagraha (shadow planet)."""

    model_config = ConfigDict(frozen=True)

    name: str
    name_hi: str
    longitude: float = Field(ge=0, lt=360)
    sign_index: int = Field(ge=0, le=11)
    sign: str
    degree_in_sign: float = Field(ge=0, lt=30)
    house: int = Field(ge=1, le=12)
    source_planet: str  # Which planet generates this upagraha
