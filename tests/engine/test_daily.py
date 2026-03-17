"""Tests for daily suggestion engine."""

from __future__ import annotations

from datetime import date

import pytest

from jyotish_engine.compute.daily import compute_daily_suggestion, DailySuggestion


class TestDailySuggestion:
    """Tests for compute_daily_suggestion."""

    def test_returns_daily_suggestion(self, manish_chart) -> None:
        """Should return a DailySuggestion dataclass."""
        result = compute_daily_suggestion(manish_chart)
        assert isinstance(result, DailySuggestion)

    def test_has_required_fields(self, manish_chart) -> None:
        """Should have all required fields populated."""
        result = compute_daily_suggestion(manish_chart)
        assert result.date
        assert result.vara
        assert result.vara_planet
        assert result.recommended_color
        assert result.good_for
        assert result.avoid
        assert result.health_focus
        assert 1 <= result.day_rating <= 10

    def test_transit_impacts_populated(self, manish_chart) -> None:
        """Should have transit impacts for all 9 planets."""
        result = compute_daily_suggestion(manish_chart)
        assert len(result.transit_impacts) >= 7  # At least 7 traditional planets

    def test_specific_date(self, manish_chart) -> None:
        """Should compute for a specific date."""
        result = compute_daily_suggestion(manish_chart, target_date=date(2026, 3, 16))
        assert result.date == "16/03/2026"
        assert result.vara == "Monday"
        assert result.vara_planet == "Moon"
        assert result.recommended_color == "White/Cream"

    def test_transit_impact_has_bindus(self, manish_chart) -> None:
        """Each transit impact should have bindu rating."""
        result = compute_daily_suggestion(manish_chart)
        for t in result.transit_impacts:
            assert 0 <= t.bindus <= 8
            assert isinstance(t.is_favorable, bool)

    def test_rahu_kaal_present(self, manish_chart) -> None:
        """Should include Rahu Kaal timing."""
        result = compute_daily_suggestion(manish_chart)
        assert result.rahu_kaal != "Unknown"
