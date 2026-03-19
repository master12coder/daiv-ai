"""Tests for the reusable divisional chart renderer."""

from __future__ import annotations

import pytest

from daivai_engine.compute.chart import compute_chart
from daivai_engine.compute.divisional import (
    compute_dasamsha,
    compute_navamsha,
    get_vargottam_planets,
)
from daivai_engine.models.chart import ChartData
from daivai_products.plugins.kundali.divisional import render_divisional_chart


@pytest.fixture
def manish_chart() -> ChartData:
    """Reference chart: Manish Chaurasia — Mithuna lagna."""
    return compute_chart(
        name="Manish Chaurasia",
        dob="13/03/1989",
        tob="12:17",
        lat=25.3176,
        lon=83.0067,
        tz_name="Asia/Kolkata",
        gender="Male",
    )


class TestD9NavamshaChart:
    """Test D9 Navamsha rendering."""

    def test_renders_navamsha_png(self, manish_chart: ChartData) -> None:
        """D9 chart should render as valid PNG bytes."""
        positions = compute_navamsha(manish_chart)
        result = render_divisional_chart(
            manish_chart,
            positions,
            "D9 Navamsha",
            "नवमांश",
        )
        assert result is not None
        assert result[:4] == b"\x89PNG"
        assert len(result) > 1000

    def test_navamsha_has_nine_planets(self, manish_chart: ChartData) -> None:
        """D9 computation should return 9 planet positions."""
        positions = compute_navamsha(manish_chart)
        assert len(positions) == 9

    def test_vargottam_planets_detected(self, manish_chart: ChartData) -> None:
        """Should detect vargottam planets (same sign in D1 and D9)."""
        vargottam = get_vargottam_planets(manish_chart)
        assert isinstance(vargottam, list)
        # Vargottam planets may or may not exist — just verify it returns

    def test_navamsha_positions_valid(self, manish_chart: ChartData) -> None:
        """Each position should have valid sign indices."""
        positions = compute_navamsha(manish_chart)
        for pos in positions:
            assert 0 <= pos.d1_sign_index <= 11
            assert 0 <= pos.divisional_sign_index <= 11
            assert pos.divisional_sign != ""


class TestD10DasamashaChart:
    """Test D10 Dasamsha rendering."""

    def test_renders_dasamsha_png(self, manish_chart: ChartData) -> None:
        """D10 chart should render as valid PNG bytes."""
        positions = compute_dasamsha(manish_chart)
        result = render_divisional_chart(
            manish_chart,
            positions,
            "D10 Dasamsha",
            "दशमांश",
        )
        assert result is not None
        assert result[:4] == b"\x89PNG"

    def test_dasamsha_has_nine_planets(self, manish_chart: ChartData) -> None:
        """D10 should return 9 planet positions."""
        positions = compute_dasamsha(manish_chart)
        assert len(positions) == 9


class TestDivisionalChartReusability:
    """Test that the renderer works with any varga."""

    def test_renders_with_different_chart(self) -> None:
        """Should work with non-Mithuna charts."""
        chart = compute_chart(
            name="Test Person",
            dob="01/01/2000",
            tob="06:00",
            lat=28.6139,
            lon=77.2090,
            tz_name="Asia/Kolkata",
            gender="Female",
        )
        positions = compute_navamsha(chart)
        result = render_divisional_chart(chart, positions, "D9", "नवमांश")
        assert result is not None
        assert len(result) > 1000

    def test_handles_empty_positions(self, manish_chart: ChartData) -> None:
        """Should handle empty position list gracefully."""
        result = render_divisional_chart(manish_chart, [], "D9", "नवमांश")
        assert result is not None
        assert result[:4] == b"\x89PNG"
