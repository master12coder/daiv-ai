"""Tests for chart computation in the new engine package."""
from __future__ import annotations

import pytest

from jyotish_engine.compute.chart import compute_chart, get_house_lord, get_planets_in_house
from jyotish_engine.models.chart import ChartData, PlanetData


@pytest.fixture
def manish_chart() -> ChartData:
    """Reference chart: Manish Chaurasia."""
    return compute_chart(
        name="Manish Chaurasia", dob="13/03/1989", tob="12:17",
        lat=25.3176, lon=83.0067, tz_name="Asia/Kolkata", gender="Male",
    )


class TestComputeChart:
    """Tests for compute_chart function."""

    def test_returns_chart_data(self, manish_chart: ChartData) -> None:
        """compute_chart returns a ChartData instance."""
        assert isinstance(manish_chart, ChartData)

    def test_lagna_is_mithuna(self, manish_chart: ChartData) -> None:
        """Manish's lagna should be Mithuna (Gemini)."""
        assert manish_chart.lagna_sign == "Mithuna"
        assert manish_chart.lagna_sign_en == "Gemini"

    def test_has_nine_planets(self, manish_chart: ChartData) -> None:
        """Chart should have 9 planets."""
        assert len(manish_chart.planets) == 9

    def test_moon_in_rohini(self, manish_chart: ChartData) -> None:
        """Moon should be in Rohini nakshatra."""
        moon = manish_chart.planets["Moon"]
        assert moon.nakshatra == "Rohini"
        assert moon.pada == 2

    def test_moon_exalted(self, manish_chart: ChartData) -> None:
        """Moon in Taurus should be exalted."""
        moon = manish_chart.planets["Moon"]
        assert moon.sign == "Vrishabha"
        assert moon.dignity == "exalted"

    def test_planet_data_types(self, manish_chart: ChartData) -> None:
        """All planets should be PlanetData instances."""
        for name, planet in manish_chart.planets.items():
            assert isinstance(planet, PlanetData), f"{name} is not PlanetData"

    def test_house_numbers_valid(self, manish_chart: ChartData) -> None:
        """All planet houses should be 1-12."""
        for name, planet in manish_chart.planets.items():
            assert 1 <= planet.house <= 12, f"{name} house {planet.house} out of range"

    def test_rahu_ketu_opposite(self, manish_chart: ChartData) -> None:
        """Rahu and Ketu should be exactly opposite."""
        rahu = manish_chart.planets["Rahu"]
        ketu = manish_chart.planets["Ketu"]
        diff = abs(rahu.longitude - ketu.longitude)
        assert abs(diff - 180.0) < 0.01

    def test_get_house_lord(self, manish_chart: ChartData) -> None:
        """House lord should return valid planet names."""
        for h in range(1, 13):
            lord = get_house_lord(manish_chart, h)
            assert lord in manish_chart.planets

    def test_get_planets_in_house(self, manish_chart: ChartData) -> None:
        """Total planets across all houses should be 9."""
        total = sum(len(get_planets_in_house(manish_chart, h)) for h in range(1, 13))
        assert total == 9

    def test_pydantic_model_serialization(self, manish_chart: ChartData) -> None:
        """ChartData should serialize to JSON and back."""
        json_str = manish_chart.model_dump_json()
        restored = ChartData.model_validate_json(json_str)
        assert restored.lagna_sign == manish_chart.lagna_sign
        assert len(restored.planets) == len(manish_chart.planets)
