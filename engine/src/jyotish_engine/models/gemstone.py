"""Domain models for gemstone recommendations and safety checks."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class GemstoneRecommendation(BaseModel):
    """Represents a gemstone recommendation for a native.

    Contains the stone name in English and Hindi, the associated planet,
    a status indicating whether the stone is recommended / to be tested
    with caution / prohibited, and the reasoning behind the recommendation.
    """

    model_config = ConfigDict(frozen=True)

    stone_name: str
    stone_name_hi: str
    planet: str
    status: str  # "recommended", "test_with_caution", "prohibited"
    reason: str


class ProhibitedStone(BaseModel):
    """Represents a stone that is prohibited for a specific lagna.

    Contains the stone name in English and Hindi, the associated planet,
    and the reason for prohibition (e.g., maraka lordship, functional malefic).
    """

    model_config = ConfigDict(frozen=True)

    stone_name: str
    stone_name_hi: str
    planet: str
    reason: str  # e.g., "Jupiter is MARAKA (7th lord) for Mithuna lagna"
