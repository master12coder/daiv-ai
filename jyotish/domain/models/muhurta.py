"""Domain models for Muhurta (auspicious timing) candidates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MuhurtaCandidate:
    """Represents a candidate date evaluated for auspicious timing (Muhurta).

    Contains the date, day of week, key Panchang elements (nakshatra, tithi, yoga),
    the Rahu Kaal period to avoid, a computed favorability score, and the list
    of reasons explaining the score.
    """

    date: str
    day: str
    nakshatra: str
    tithi: str
    yoga: str
    rahu_kaal: str
    score: float
    reasons: list[str]
