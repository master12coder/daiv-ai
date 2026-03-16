"""Muhurta / auspicious timing finder."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from jyotish.utils.constants import (
    MUHURTA_FAVORABLE_NAKSHATRAS, NAKSHATRAS, DAY_NAMES,
)
from jyotish.compute.panchang import compute_panchang, PanchangData
from jyotish.domain.models.muhurta import MuhurtaCandidate


def find_muhurta(
    purpose: str,
    lat: float,
    lon: float,
    start_date: datetime,
    end_date: datetime,
    tz_name: str = "Asia/Kolkata",
    max_results: int = 5,
) -> list[MuhurtaCandidate]:
    """Find auspicious dates for a given purpose.

    Args:
        purpose: marriage, business, travel, property
        lat: Latitude
        lon: Longitude
        start_date: Start of search range
        end_date: End of search range
        tz_name: Timezone
        max_results: Maximum number of results
    """
    favorable_naks = MUHURTA_FAVORABLE_NAKSHATRAS.get(
        purpose, MUHURTA_FAVORABLE_NAKSHATRAS.get("business", [])
    )

    # Unfavorable tithis (4th, 9th, 14th, Amavasya, Purnima for some)
    unfavorable_tithis = {3, 8, 13, 29}  # 0-indexed

    # Unfavorable days per purpose
    unfavorable_days_map = {
        "marriage": {"Tuesday", "Saturday"},
        "business": {"Sunday"},
        "travel": {"Tuesday", "Saturday"},
        "property": {"Tuesday"},
    }
    unfavorable_days = unfavorable_days_map.get(purpose, set())

    candidates: list[MuhurtaCandidate] = []
    current = start_date

    while current <= end_date:
        date_str = current.strftime("%d/%m/%Y")
        try:
            panchang = compute_panchang(date_str, lat, lon, tz_name)
        except Exception:
            current += timedelta(days=1)
            continue

        score = 0.0
        reasons = []

        # Check nakshatra
        if panchang.nakshatra_name in favorable_naks:
            score += 3.0
            reasons.append(f"Favorable nakshatra: {panchang.nakshatra_name}")

        # Check tithi
        if panchang.tithi_index not in unfavorable_tithis:
            score += 1.0
            reasons.append(f"Favorable tithi: {panchang.tithi_name}")
        else:
            score -= 2.0
            reasons.append(f"Unfavorable tithi: {panchang.tithi_name}")

        # Check day of week
        if panchang.vara in unfavorable_days:
            score -= 1.5
            reasons.append(f"Unfavorable day: {panchang.vara}")
        else:
            score += 0.5
            reasons.append(f"Day: {panchang.vara}")

        # Favorable panchang yogas
        favorable_yogas = {
            "Siddhi", "Shiva", "Siddha", "Sadhya", "Shubha",
            "Priti", "Ayushman", "Saubhagya", "Shobhana",
        }
        if panchang.yoga_name in favorable_yogas:
            score += 1.5
            reasons.append(f"Auspicious yoga: {panchang.yoga_name}")

        if score > 0:
            candidates.append(MuhurtaCandidate(
                date=date_str,
                day=panchang.vara,
                nakshatra=panchang.nakshatra_name,
                tithi=panchang.tithi_name,
                yoga=panchang.yoga_name,
                rahu_kaal=panchang.rahu_kaal,
                score=round(score, 1),
                reasons=reasons,
            ))

        current += timedelta(days=1)

    # Sort by score descending, take top results
    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates[:max_results]
