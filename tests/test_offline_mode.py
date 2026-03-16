"""Tests for offline mode — all features must work without API keys."""

from __future__ import annotations

import json
import pytest
from click.testing import CliRunner

from jyotish.cli import main


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def chart_file(tmp_path) -> str:
    data = {
        "name": "Manish Chaurasia", "dob": "13/03/1989", "tob": "12:17",
        "place": "Varanasi", "gender": "Male",
        "latitude": 25.3176, "longitude": 83.0067, "timezone_name": "Asia/Kolkata",
    }
    path = tmp_path / "chart.json"
    path.write_text(json.dumps(data))
    return str(path)


class TestOfflineChart:
    """Chart computation must work offline."""

    def test_chart_no_llm(self, runner) -> None:
        result = runner.invoke(main, [
            "chart", "--name", "Test", "--dob", "13/03/1989",
            "--tob", "12:17", "--place", "Varanasi",
        ])
        assert result.exit_code == 0

    def test_report_llm_none(self, runner) -> None:
        result = runner.invoke(main, [
            "report", "--name", "Test", "--dob", "13/03/1989",
            "--tob", "12:17", "--place", "Varanasi", "--llm", "none",
        ])
        assert result.exit_code == 0


class TestOfflineCompanion:
    """Companion features must work offline (no LLM)."""

    def test_daily_offline(self, runner, chart_file) -> None:
        result = runner.invoke(main, ["daily", "--chart", chart_file])
        assert result.exit_code == 0
        assert "Daily Suggestion" in result.output

    def test_pooja_offline(self, runner, chart_file) -> None:
        result = runner.invoke(main, ["pooja", "--chart", chart_file])
        assert result.exit_code == 0
        assert "Weekly Pooja" in result.output

    def test_transit_offline(self, runner, chart_file) -> None:
        result = runner.invoke(main, ["transit", "--chart", chart_file])
        assert result.exit_code == 0
        assert "Transits" in result.output

    def test_panchang_offline(self, runner) -> None:
        result = runner.invoke(main, ["panchang", "--place", "Varanasi"])
        assert result.exit_code == 0

    def test_dashboard_offline(self, runner) -> None:
        result = runner.invoke(main, ["dashboard"])
        assert result.exit_code == 0
