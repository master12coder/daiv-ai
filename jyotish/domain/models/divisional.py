"""Domain models for divisional chart positions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DivisionalPosition:
    """Represents a planet's position in a divisional (Varga) chart.

    Maps a planet from its D1 (Rashi) sign to the computed divisional sign,
    and indicates whether the planet is vargottam (same sign in both D1 and
    the divisional chart).
    """

    planet: str
    d1_sign_index: int
    divisional_sign_index: int
    divisional_sign: str
    is_vargottam: bool  # Same sign in D1 and this divisional chart
