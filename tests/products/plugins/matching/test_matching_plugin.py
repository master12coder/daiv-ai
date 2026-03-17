"""Tests for the matching plugin engine."""
from __future__ import annotations

import pytest

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.models.chart import ChartData
from jyotish_products.plugins.matching.engine import run_match, compute_match, format_result


@pytest.fixture
def manish_chart() -> ChartData:
    """Reference chart: Manish Chaurasia."""
    return compute_chart(
        name="Manish Chaurasia", dob="13/03/1989", tob="12:17",
        lat=25.3176, lon=83.0067, tz_name="Asia/Kolkata", gender="Male",
    )


@pytest.fixture
def second_chart() -> ChartData:
    """Second chart for matching tests."""
    return compute_chart(
        name="Test Person", dob="15/06/1990", tob="08:30",
        lat=28.6139, lon=77.2090, tz_name="Asia/Kolkata", gender="Female",
    )


class TestMatchingPlugin:
    def test_run_match_returns_formatted_string(
        self, manish_chart: ChartData, second_chart: ChartData,
    ) -> None:
        """run_match should return a string with both names and a score."""
        result = run_match(manish_chart, second_chart)
        assert isinstance(result, str)
        assert "Manish Chaurasia" in result
        assert "Test Person" in result
        assert "Total:" in result

    def test_compute_match_returns_valid_result(
        self, manish_chart: ChartData, second_chart: ChartData,
    ) -> None:
        """compute_match should return a MatchingResult with 8 kootas."""
        result = compute_match(manish_chart, second_chart)
        assert len(result.kootas) == 8
        assert 0 <= result.total_obtained <= 36
        assert 0 <= result.percentage <= 100
        assert result.recommendation != ""

    def test_format_result_contains_all_kootas(
        self, manish_chart: ChartData, second_chart: ChartData,
    ) -> None:
        """format_result should list all 8 koota names."""
        result = compute_match(manish_chart, second_chart)
        text = format_result(result, "A", "B")
        for koota_name in ["Varna", "Vasya", "Tara", "Yoni", "Graha Maitri", "Gana", "Bhakoot", "Nadi"]:
            assert koota_name in text
