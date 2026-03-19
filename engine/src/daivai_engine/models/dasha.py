"""Domain models for Vimshottari Dasha periods."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DashaPeriod(BaseModel):
    """Represents a single Vimshottari Dasha period (Mahadasha, Antardasha, or Pratyantardasha).

    Each period has a ruling planet (lord), a start and end datetime, a level
    indicating the dasha tier, and an optional parent lord for sub-periods.
    """

    model_config = ConfigDict(frozen=True)

    level: str  # "MD", "AD", "PD"
    lord: str  # Planet name
    start: datetime
    end: datetime
    parent_lord: str | None = None  # For AD/PD — the parent dasha lord
