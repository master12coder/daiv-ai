"""Tests for chart save/load via Pydantic serialization."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.models.chart import ChartData


@pytest.fixture
def manish_chart() -> ChartData:
    return compute_chart(
        name="Manish Chaurasia",
        dob="13/03/1989",
        tob="12:17",
        lat=25.3176,
        lon=83.0067,
        tz_name="Asia/Kolkata",
        gender="Male",
    )


class TestChartStore:
    def test_save_creates_json(self, manish_chart: ChartData, tmp_path: Path) -> None:
        output = tmp_path / "test.json"
        output.write_text(manish_chart.model_dump_json(indent=2))
        assert output.exists()
        data = json.loads(output.read_text())
        assert data["name"] == "Manish Chaurasia"

    def test_save_includes_coordinates(self, manish_chart: ChartData, tmp_path: Path) -> None:
        output = tmp_path / "test.json"
        output.write_text(manish_chart.model_dump_json(indent=2))
        data = json.loads(output.read_text())
        assert "latitude" in data
        assert "longitude" in data
        assert "timezone_name" in data

    def test_load_reproduces_chart(self, manish_chart: ChartData, tmp_path: Path) -> None:
        output = tmp_path / "test.json"
        output.write_text(manish_chart.model_dump_json(indent=2))
        loaded = ChartData.model_validate_json(output.read_text())
        assert loaded.lagna_sign == manish_chart.lagna_sign
        assert loaded.name == manish_chart.name

    def test_roundtrip_planet_count(self, manish_chart: ChartData, tmp_path: Path) -> None:
        output = tmp_path / "test.json"
        output.write_text(manish_chart.model_dump_json(indent=2))
        loaded = ChartData.model_validate_json(output.read_text())
        assert len(loaded.planets) == len(manish_chart.planets)

    def test_load_from_dict(self) -> None:
        data = {
            "name": "Test",
            "dob": "13/03/1989",
            "tob": "12:17",
            "place": "Varanasi",
            "gender": "Male",
            "latitude": 25.3176,
            "longitude": 83.0067,
            "timezone_name": "Asia/Kolkata",
            "julian_day": 2447600.0,
            "ayanamsha": 23.7,
            "lagna_longitude": 43.0,
            "lagna_sign_index": 2,
            "lagna_sign": "Mithuna",
            "lagna_sign_en": "Gemini",
            "lagna_sign_hi": "मिथुन",
            "lagna_degree": 13.0,
            "planets": {},
        }
        chart = ChartData.model_validate(data)
        assert chart.lagna_sign == "Mithuna"
