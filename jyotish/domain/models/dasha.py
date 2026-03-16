"""Domain models for Vimshottari Dasha periods."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class DashaPeriod:
    """Represents a single Vimshottari Dasha period (Mahadasha, Antardasha, or Pratyantardasha).

    Each period has a ruling planet (lord), a start and end datetime, a level
    indicating the dasha tier, and an optional parent lord for sub-periods.
    """

    level: str            # "MD", "AD", "PD"
    lord: str             # Planet name
    start: datetime
    end: datetime
    parent_lord: str | None = None  # For AD/PD — the parent dasha lord
