"""Tests for the muhurta plugin engine."""

from __future__ import annotations

from daivai_engine.models.muhurta import MuhurtaCandidate
from daivai_products.plugins.muhurta.engine import find_dates, format_candidates


class TestMuhurtaPlugin:
    def test_find_dates_returns_string(self) -> None:
        """find_dates should return a formatted string with results or a no-results message."""
        result = find_dates(
            purpose="business",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            from_date="01/01/2025",
            to_date="07/01/2025",
        )
        assert isinstance(result, str)
        # Either found dates or the "no dates found" message
        assert "Business" in result or "business" in result

    def test_format_candidates_empty(self) -> None:
        """format_candidates with empty list should return a no-results message."""
        result = format_candidates([], "marriage")
        assert "No auspicious dates found" in result
        assert "marriage" in result

    def test_format_candidates_with_data(self) -> None:
        """format_candidates should list each candidate with score and reasons."""
        candidates = [
            MuhurtaCandidate(
                date="15/01/2025",
                day="Wednesday",
                nakshatra="Rohini",
                tithi="Shukla Panchami",
                yoga="Siddhi",
                rahu_kaal="12:00-13:30",
                score=4.5,
                reasons=["Favorable nakshatra: Rohini", "Auspicious yoga: Siddhi"],
            ),
        ]
        result = format_candidates(candidates, "business")
        assert "15/01/2025" in result
        assert "Rohini" in result
        assert "4.5" in result
        assert "Siddhi" in result
        assert "Business" in result
