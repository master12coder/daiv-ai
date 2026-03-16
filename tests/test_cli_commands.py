"""Tests for CLI commands — verifies all major commands work."""

from __future__ import annotations

import json
import os
import tempfile

import pytest
from click.testing import CliRunner

from jyotish.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Click test runner."""
    return CliRunner()


@pytest.fixture
def chart_file(tmp_path) -> str:
    """Create a saved chart file for testing."""
    chart_data = {
        "name": "Manish Chaurasia",
        "dob": "13/03/1989",
        "tob": "12:17",
        "place": "Varanasi",
        "gender": "Male",
        "latitude": 25.3176,
        "longitude": 83.0067,
        "timezone_name": "Asia/Kolkata",
    }
    path = tmp_path / "test_chart.json"
    path.write_text(json.dumps(chart_data))
    return str(path)


class TestChartCommand:
    """Tests for jyotish chart."""

    def test_chart_basic(self, runner) -> None:
        """Chart command should produce output."""
        result = runner.invoke(main, [
            "chart", "--name", "Test", "--dob", "13/03/1989",
            "--tob", "12:17", "--place", "Varanasi", "--gender", "Male",
        ])
        assert result.exit_code == 0
        assert "Mithuna" in result.output or "Gemini" in result.output

    def test_chart_json_format(self, runner) -> None:
        """Chart command with --format json should produce JSON."""
        result = runner.invoke(main, [
            "chart", "--name", "Test", "--dob", "13/03/1989",
            "--tob", "12:17", "--place", "Varanasi", "--format", "json",
        ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "lagna" in data


class TestSaveCommand:
    """Tests for jyotish save."""

    def test_save_creates_file(self, runner, tmp_path) -> None:
        """Save command should create a JSON file."""
        output = str(tmp_path / "saved.json")
        result = runner.invoke(main, [
            "save", "--name", "Test", "--dob", "13/03/1989",
            "--tob", "12:17", "--place", "Varanasi", "-o", output,
        ])
        assert result.exit_code == 0
        assert os.path.exists(output)
        data = json.loads(open(output).read())
        assert data["name"] == "Test"
        assert data["latitude"] is not None

    def test_saved_chart_loadable(self, runner, tmp_path) -> None:
        """Saved chart should be loadable by daily command."""
        output = str(tmp_path / "saved.json")
        runner.invoke(main, [
            "save", "--name", "Test", "--dob", "13/03/1989",
            "--tob", "12:17", "--place", "Varanasi", "-o", output,
        ])
        result = runner.invoke(main, ["daily", "--chart", output])
        assert result.exit_code == 0


class TestDailyCommand:
    """Tests for jyotish daily."""

    def test_daily_with_chart(self, runner, chart_file) -> None:
        """Daily command should work with saved chart."""
        result = runner.invoke(main, ["daily", "--chart", chart_file])
        assert result.exit_code == 0
        assert "Daily Suggestion" in result.output


class TestPoojaCommand:
    """Tests for jyotish pooja."""

    def test_pooja_with_chart(self, runner, chart_file) -> None:
        """Pooja command should work with saved chart."""
        result = runner.invoke(main, ["pooja", "--chart", chart_file])
        assert result.exit_code == 0
        assert "Weekly Pooja Plan" in result.output

    def test_pooja_shows_maraka_warnings(self, runner, chart_file) -> None:
        """Pooja should warn about maraka planets for Mithuna."""
        result = runner.invoke(main, ["pooja", "--chart", chart_file])
        assert "MARAKA" in result.output


class TestTransitCommand:
    """Tests for jyotish transit."""

    def test_transit_with_chart(self, runner, chart_file) -> None:
        """Transit command should work with saved chart."""
        result = runner.invoke(main, ["transit", "--chart", chart_file, "--months", "6"])
        assert result.exit_code == 0
        assert "Transits" in result.output


class TestEventsCommand:
    """Tests for jyotish events."""

    def test_events_add(self, runner, chart_file) -> None:
        """Events add should store an event."""
        result = runner.invoke(main, [
            "events", "add", "--chart", chart_file,
            "--type", "career", "--date", "2020-01",
            "--desc", "Started new job",
        ])
        assert result.exit_code == 0
        assert "Event added" in result.output


class TestDashboardCommand:
    """Tests for jyotish dashboard."""

    def test_dashboard_runs(self, runner) -> None:
        """Dashboard command should run without errors."""
        result = runner.invoke(main, ["dashboard"])
        assert result.exit_code == 0
        assert "Prediction Accuracy" in result.output


class TestReportCommand:
    """Tests for jyotish report."""

    def test_report_llm_none(self, runner) -> None:
        """Report with --llm none should work offline."""
        result = runner.invoke(main, [
            "report", "--name", "Test", "--dob", "13/03/1989",
            "--tob", "12:17", "--place", "Varanasi", "--llm", "none",
        ])
        assert result.exit_code == 0

    def test_report_with_chart_file(self, runner, chart_file) -> None:
        """Report should work with --chart flag."""
        result = runner.invoke(main, [
            "report", "--chart", chart_file, "--llm", "none",
        ])
        assert result.exit_code == 0
