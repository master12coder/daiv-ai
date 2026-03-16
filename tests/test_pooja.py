"""Tests for weekly pooja planner."""

from __future__ import annotations

import pytest

from jyotish.interpret.pooja_planner import generate_weekly_plan, WeeklyPlan


class TestPoojaPlanner:
    """Tests for generate_weekly_plan."""

    def test_returns_weekly_plan(self, manish_chart) -> None:
        """Should return a WeeklyPlan dataclass."""
        result = generate_weekly_plan(manish_chart)
        assert isinstance(result, WeeklyPlan)

    def test_has_7_days(self, manish_chart) -> None:
        """Should have exactly 7 days."""
        result = generate_weekly_plan(manish_chart)
        assert len(result.days) == 7

    def test_mithuna_lagna_detected(self, manish_chart) -> None:
        """Should correctly identify Mithuna lagna."""
        result = generate_weekly_plan(manish_chart)
        assert result.lagna == "Mithuna"
        assert result.lagna_en == "Gemini"

    def test_mercury_day_is_benefic(self, manish_chart) -> None:
        """Mercury (lagnesh) should be marked as benefic for Mithuna."""
        result = generate_weekly_plan(manish_chart)
        wednesday = [d for d in result.days if d.planet == "Mercury"][0]
        assert wednesday.is_planet_benefic
        assert "LAGNESH" in wednesday.lordship_note

    def test_jupiter_day_is_maraka(self, manish_chart) -> None:
        """Jupiter should be marked as maraka for Mithuna."""
        result = generate_weekly_plan(manish_chart)
        thursday = [d for d in result.days if d.planet == "Jupiter"][0]
        assert not thursday.is_planet_benefic
        assert "MARAKA" in thursday.lordship_note

    def test_moon_day_is_maraka(self, manish_chart) -> None:
        """Moon (2nd lord) should be maraka for Mithuna."""
        result = generate_weekly_plan(manish_chart)
        monday = [d for d in result.days if d.planet == "Moon"][0]
        assert not monday.is_planet_benefic
        assert "MARAKA" in monday.lordship_note

    def test_venus_day_is_benefic(self, manish_chart) -> None:
        """Venus (5th lord, yogakaraka) should be benefic for Mithuna."""
        result = generate_weekly_plan(manish_chart)
        friday = [d for d in result.days if d.planet == "Venus"][0]
        assert friday.is_planet_benefic

    def test_saturn_day_is_benefic(self, manish_chart) -> None:
        """Saturn (9th lord) should be benefic for Mithuna."""
        result = generate_weekly_plan(manish_chart)
        saturday = [d for d in result.days if d.planet == "Saturn"][0]
        assert saturday.is_planet_benefic

    def test_special_notes_for_maraka_dasha(self, manish_chart) -> None:
        """Should have special note about Jupiter maraka mahadasha."""
        result = generate_weekly_plan(manish_chart)
        assert any("MARAKA" in note for note in result.special_notes)
        assert any("Mercury" in note or "Lagnesh" in note for note in result.special_notes)

    def test_each_day_has_deity(self, manish_chart) -> None:
        """Each day should have deity and mantra."""
        result = generate_weekly_plan(manish_chart)
        for d in result.days:
            assert d.deity or d.mantra  # At least one should be present
