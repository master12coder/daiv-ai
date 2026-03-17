"""Tests for the remedies plugin engine."""
from __future__ import annotations

import pytest

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.models.chart import ChartData
from jyotish_products.plugins.remedies.engine import get_gemstone_recommendations


@pytest.fixture
def manish_chart() -> ChartData:
    """Reference chart: Manish Chaurasia — Mithuna lagna."""
    return compute_chart(
        name="Manish Chaurasia", dob="13/03/1989", tob="12:17",
        lat=25.3176, lon=83.0067, tz_name="Asia/Kolkata", gender="Male",
    )


class TestRemediesPlugin:
    def test_returns_formatted_string(self, manish_chart: ChartData) -> None:
        """get_gemstone_recommendations should return a non-empty report."""
        result = get_gemstone_recommendations(manish_chart)
        assert isinstance(result, str)
        assert "Manish Chaurasia" in result
        assert "Mithuna" in result

    @pytest.mark.safety
    def test_pukhraj_prohibited_for_mithuna(self, manish_chart: ChartData) -> None:
        """Pukhraj (Yellow Sapphire) MUST be PROHIBITED for Mithuna lagna.

        Jupiter is a functional malefic and maraka for Gemini lagna due to
        Kendradhipati dosha (7th + 10th lord). This is a critical safety check.
        """
        result = get_gemstone_recommendations(manish_chart)
        assert "PROHIBITED" in result
        assert "Pukhraj" in result or "Yellow Sapphire" in result
        # Pukhraj must appear in PROHIBITED section, not RECOMMENDED
        prohibited_start = result.index("PROHIBITED")
        pukhraj_pos = result.index("Pukhraj") if "Pukhraj" in result else result.index("Yellow Sapphire")
        assert pukhraj_pos > prohibited_start

    def test_emerald_recommended_for_mithuna(self, manish_chart: ChartData) -> None:
        """Emerald (Panna) should be RECOMMENDED for Mithuna lagna.

        Mercury is the lagna lord and 4th lord — always beneficial.
        """
        result = get_gemstone_recommendations(manish_chart)
        assert "RECOMMENDED" in result
        assert "Emerald" in result or "Panna" in result
