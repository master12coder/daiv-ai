"""Tests for Narayana Dasha computation."""

from __future__ import annotations

from daivai_engine.compute.narayana_dasha import compute_narayana_dasha
from daivai_engine.models.chart import ChartData


class TestNarayanaDasha:
    def test_returns_twelve_periods(self, manish_chart: ChartData) -> None:
        periods = compute_narayana_dasha(manish_chart)
        assert len(periods) == 12

    def test_all_periods_have_dates(self, manish_chart: ChartData) -> None:
        periods = compute_narayana_dasha(manish_chart)
        for p in periods:
            assert p.start is not None
            assert p.end is not None
            assert p.end > p.start

    def test_periods_consecutive(self, manish_chart: ChartData) -> None:
        """Each period starts when previous ends."""
        periods = compute_narayana_dasha(manish_chart)
        for i in range(1, len(periods)):
            assert abs((periods[i].start - periods[i - 1].end).total_seconds()) < 1

    def test_level_is_nd(self, manish_chart: ChartData) -> None:
        periods = compute_narayana_dasha(manish_chart)
        for p in periods:
            assert p.level == "ND"

    def test_duration_max_12_years(self, manish_chart: ChartData) -> None:
        periods = compute_narayana_dasha(manish_chart)
        for p in periods:
            years = (p.end - p.start).days / 365.25
            assert years <= 12.1  # Small tolerance for leap year
