"""Tests for yoga detection."""
from __future__ import annotations

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.compute.yoga import detect_all_yogas
from jyotish_engine.models.chart import ChartData
from jyotish_engine.models.yoga import YogaResult

import pytest


@pytest.fixture
def manish_chart() -> ChartData:
    return compute_chart(
        name="Manish", dob="13/03/1989", tob="12:17",
        lat=25.3176, lon=83.0067, tz_name="Asia/Kolkata", gender="Male",
    )


class TestYogaDetection:
    def test_returns_list_of_yoga_results(self, manish_chart: ChartData) -> None:
        yogas = detect_all_yogas(manish_chart)
        assert isinstance(yogas, list)
        for y in yogas:
            assert isinstance(y, YogaResult)

    def test_gajakesari_present(self, manish_chart: ChartData) -> None:
        yogas = detect_all_yogas(manish_chart)
        names = [y.name for y in yogas]
        assert "Gajakesari Yoga" in names

    def test_budhaditya_present(self, manish_chart: ChartData) -> None:
        yogas = detect_all_yogas(manish_chart)
        names = [y.name for y in yogas]
        assert "Budhaditya Yoga" in names

    def test_yoga_has_required_fields(self, manish_chart: ChartData) -> None:
        yogas = detect_all_yogas(manish_chart)
        for y in yogas:
            assert y.name
            assert y.name_hindi
            assert y.effect in ("benefic", "malefic", "mixed")
            assert y.description
