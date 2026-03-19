"""Muhurta plugin engine — wraps engine muhurta computation."""

from __future__ import annotations

from datetime import datetime

from jyotish_engine.compute.muhurta import find_muhurta
from jyotish_engine.models.muhurta import MuhurtaCandidate


def find_dates(
    purpose: str,
    lat: float,
    lon: float,
    tz_name: str,
    from_date: str,
    to_date: str,
    max_results: int = 5,
) -> str:
    """Find auspicious dates and return formatted result.

    Args:
        purpose: Event type (marriage, business, travel, property).
        lat: Latitude of the location.
        lon: Longitude of the location.
        tz_name: Timezone name (e.g. Asia/Kolkata).
        from_date: Start date as DD/MM/YYYY.
        to_date: End date as DD/MM/YYYY.
        max_results: Maximum number of results to return.

    Returns:
        Formatted multi-line string with auspicious date candidates.
    """
    start = datetime.strptime(from_date, "%d/%m/%Y")
    end = datetime.strptime(to_date, "%d/%m/%Y")

    candidates = find_muhurta(
        purpose=purpose,
        lat=lat,
        lon=lon,
        start_date=start,
        end_date=end,
        tz_name=tz_name,
        max_results=max_results,
    )

    return format_candidates(candidates, purpose)


def format_candidates(candidates: list[MuhurtaCandidate], purpose: str) -> str:
    """Format muhurta candidates into a human-readable string.

    Args:
        candidates: List of MuhurtaCandidate results.
        purpose: The event purpose for the header.

    Returns:
        Formatted multi-line report string.
    """
    if not candidates:
        return f"No auspicious dates found for {purpose} in the given range."

    lines: list[str] = []
    lines.append(f"Auspicious Dates for {purpose.title()}")
    lines.append("=" * 45)
    lines.append("")

    for i, c in enumerate(candidates, 1):
        lines.append(f"{i}. {c.date} ({c.day}) — Score: {c.score}")
        lines.append(f"   Nakshatra: {c.nakshatra} | Tithi: {c.tithi} | Yoga: {c.yoga}")
        lines.append(f"   Rahu Kaal: {c.rahu_kaal}")
        for reason in c.reasons:
            lines.append(f"   - {reason}")
        lines.append("")

    return "\n".join(lines)
