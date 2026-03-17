"""Tests for dasha computation."""
from __future__ import annotations

from datetime import datetime, timezone

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.compute.dasha import compute_mahadashas
from jyotish_engine.models.chart import ChartData
from jyotish_engine.models.dasha import DashaPeriod

import pytest


@pytest.fixture
def manish_chart() -> ChartData:
    return compute_chart(
        name="Manish", dob="13/03/1989", tob="12:17",
        lat=25.3176, lon=83.0067, tz_name="Asia/Kolkata", gender="Male",
    )


class TestMahadashas:
    def test_returns_nine_periods(self, manish_chart: ChartData) -> None:
        dashas = compute_mahadashas(manish_chart)
        assert len(dashas) == 9

    def test_periods_are_sequential(self, manish_chart: ChartData) -> None:
        dashas = compute_mahadashas(manish_chart)
        for i in range(1, len(dashas)):
            assert dashas[i].start >= dashas[i - 1].start

    def test_current_dasha_is_jupiter(self, manish_chart: ChartData) -> None:
        dashas = compute_mahadashas(manish_chart)
        # Use timezone-aware datetime to match dasha output
        now = dashas[0].start.replace(year=2026, month=3, day=17)
        current = [d for d in dashas if d.start <= now <= d.end]
        assert len(current) == 1
        assert current[0].lord == "Jupiter"

    def test_dasha_lords_valid(self, manish_chart: ChartData) -> None:
        dashas = compute_mahadashas(manish_chart)
        valid = {"Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"}
        for d in dashas:
            assert d.lord in valid
