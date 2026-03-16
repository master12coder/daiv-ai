"""Tests for chart save/load utilities."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from jyotish.cli_utils import save_chart_to_file, load_chart_from_file


class TestChartStore:
    """Tests for chart save and load."""

    def test_save_creates_json(self, manish_chart, tmp_path) -> None:
        """save_chart_to_file should create a valid JSON."""
        output = str(tmp_path / "test.json")
        save_chart_to_file(manish_chart, output)
        assert Path(output).exists()
        data = json.loads(Path(output).read_text())
        assert data["name"] == "Manish Chaurasia"

    def test_save_includes_coordinates(self, manish_chart, tmp_path) -> None:
        """Saved chart should include lat/lon/tz for offline use."""
        output = str(tmp_path / "test.json")
        save_chart_to_file(manish_chart, output)
        data = json.loads(Path(output).read_text())
        assert "latitude" in data
        assert "longitude" in data
        assert "timezone_name" in data
        assert data["latitude"] is not None
        assert data["longitude"] is not None

    def test_load_reproduces_chart(self, manish_chart, tmp_path) -> None:
        """Loading a saved chart should produce same lagna."""
        output = str(tmp_path / "test.json")
        save_chart_to_file(manish_chart, output)
        loaded = load_chart_from_file(output)
        assert loaded.lagna_sign == manish_chart.lagna_sign
        assert loaded.name == manish_chart.name

    def test_save_creates_parent_dirs(self, manish_chart, tmp_path) -> None:
        """Should create parent directories if they don't exist."""
        output = str(tmp_path / "sub" / "dir" / "chart.json")
        save_chart_to_file(manish_chart, output)
        assert Path(output).exists()

    def test_load_with_lat_lon(self, tmp_path) -> None:
        """Should load using lat/lon/tz when available."""
        data = {
            "name": "Test",
            "dob": "13/03/1989",
            "tob": "12:17",
            "gender": "Male",
            "latitude": 25.3176,
            "longitude": 83.0067,
            "timezone_name": "Asia/Kolkata",
        }
        path = tmp_path / "test.json"
        path.write_text(json.dumps(data))
        chart = load_chart_from_file(str(path))
        assert chart.lagna_sign == "Mithuna"
