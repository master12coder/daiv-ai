"""Tests for the graha (planet) position table renderer."""
from __future__ import annotations

import pytest

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.compute.strength import compute_shadbala
from jyotish_engine.models.chart import ChartData
from jyotish_products.interpret.context import build_lordship_context
from jyotish_products.plugins.kundali.graha_table import render_graha_table


@pytest.fixture
def manish_chart() -> ChartData:
    return compute_chart(
        name="Manish Chaurasia", dob="13/03/1989", tob="12:17",
        lat=25.3176, lon=83.0067, tz_name="Asia/Kolkata", gender="Male",
    )


@pytest.fixture
def mithuna_ctx() -> dict:
    return build_lordship_context("Mithuna")


class TestGrahaTable:
    def test_returns_flowable_elements(self, manish_chart: ChartData, mithuna_ctx: dict) -> None:
        """Should return a list of ReportLab flowables."""
        shadbala = compute_shadbala(manish_chart)
        elements = render_graha_table(manish_chart, shadbala, mithuna_ctx)
        assert isinstance(elements, list)
        assert len(elements) >= 2  # heading + table + spacer

    def test_table_has_header_plus_nine_rows(
        self, manish_chart: ChartData, mithuna_ctx: dict,
    ) -> None:
        """Table should have 1 header row + 9 planet rows."""
        shadbala = compute_shadbala(manish_chart)
        elements = render_graha_table(manish_chart, shadbala, mithuna_ctx)
        # The Table element is second in the list
        table = elements[1]
        # ReportLab Table stores data in _cellvalues
        assert len(table._cellvalues) == 10  # 1 header + 9 planets

    def test_works_with_empty_lordship_ctx(self, manish_chart: ChartData) -> None:
        """Should handle missing lordship context."""
        shadbala = compute_shadbala(manish_chart)
        elements = render_graha_table(manish_chart, shadbala, {})
        assert len(elements) >= 2

    def test_works_with_empty_shadbala(self, manish_chart: ChartData, mithuna_ctx: dict) -> None:
        """Should handle empty shadbala list (Rahu/Ketu have no Shadbala)."""
        elements = render_graha_table(manish_chart, [], mithuna_ctx)
        assert len(elements) >= 2
