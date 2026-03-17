"""Tests for the daily companion plugin — 3 levels."""
from __future__ import annotations

import pytest

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.models.chart import ChartData
from jyotish_products.plugins.daily.engine import (
    DailyLevel,
    run_daily,
    format_simple,
    format_medium,
    format_detailed,
)
from jyotish_engine.compute.daily import compute_daily_suggestion


@pytest.fixture
def manish_chart() -> ChartData:
    return compute_chart(
        name="Manish Chaurasia", dob="13/03/1989", tob="12:17",
        lat=25.3176, lon=83.0067, tz_name="Asia/Kolkata", gender="Male",
    )


class TestDailyLevels:
    def test_simple_is_one_line(self, manish_chart: ChartData) -> None:
        result = run_daily(manish_chart, DailyLevel.SIMPLE)
        assert isinstance(result, str)
        assert "|" in result  # Has pipe separators
        assert "/10" in result  # Has rating

    def test_medium_has_rating_and_mantra(self, manish_chart: ChartData) -> None:
        result = run_daily(manish_chart, DailyLevel.MEDIUM)
        assert "/10)" in result
        assert "Mantra" in result
        assert "Color" in result

    def test_detailed_has_transit_analysis(self, manish_chart: ChartData) -> None:
        result = run_daily(manish_chart, DailyLevel.DETAILED)
        assert "Transit Analysis" in result or "transit" in result.lower()
        assert "Rating" in result
        assert chart_name_in_output(result, "Manish")

    def test_simple_shorter_than_medium(self, manish_chart: ChartData) -> None:
        simple = run_daily(manish_chart, DailyLevel.SIMPLE)
        medium = run_daily(manish_chart, DailyLevel.MEDIUM)
        assert len(simple) < len(medium)

    def test_medium_shorter_than_detailed(self, manish_chart: ChartData) -> None:
        medium = run_daily(manish_chart, DailyLevel.MEDIUM)
        detailed = run_daily(manish_chart, DailyLevel.DETAILED)
        assert len(medium) < len(detailed)

    def test_rating_in_valid_range(self, manish_chart: ChartData) -> None:
        suggestion = compute_daily_suggestion(manish_chart)
        assert 1 <= suggestion.day_rating <= 10

    def test_default_level_is_medium(self, manish_chart: ChartData) -> None:
        result = run_daily(manish_chart)  # No level specified
        assert "Color" in result  # Medium format has Color line


def chart_name_in_output(output: str, name: str) -> bool:
    """Helper to check name appears in output."""
    return name in output
