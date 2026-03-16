"""Tests for interpretation context building and prompt rendering."""

from __future__ import annotations

import pytest

from jyotish.interpret.interpreter import _build_chart_context, _render_prompt


class TestChartContext:
    """Tests for _build_chart_context."""

    def test_context_has_chart_data(self, manish_chart) -> None:
        """Context should include all basic chart fields."""
        ctx = _build_chart_context(manish_chart)
        assert ctx["name"] == "Manish Chaurasia"
        assert ctx["lagna"] == "Mithuna"
        assert ctx["lagna_en"] == "Gemini"

    def test_context_has_lordship(self, manish_chart) -> None:
        """Context should include lordship data."""
        ctx = _build_chart_context(manish_chart)
        assert ctx["lordship"]
        assert ctx["lagnesh"] == "Mercury"
        assert "Panna" in ctx["lagnesh_stone"] or "Emerald" in ctx["lagnesh_stone"]

    def test_context_has_prohibited_stones(self, manish_chart) -> None:
        """Context should include prohibited stones."""
        ctx = _build_chart_context(manish_chart)
        prohibited = ctx["prohibited_stones"]
        assert len(prohibited) >= 2
        stone_names = [s["stone"] for s in prohibited]
        assert any("Pukhraj" in s or "Yellow Sapphire" in s for s in stone_names)

    def test_context_has_maraka_info(self, manish_chart) -> None:
        """Context should include maraka planet info."""
        ctx = _build_chart_context(manish_chart)
        maraka = ctx["maraka_planets"]
        maraka_names = [m["planet"] for m in maraka]
        assert "Jupiter" in maraka_names
        assert "Moon" in maraka_names

    def test_context_has_dasha_lord_status(self, manish_chart) -> None:
        """Context should indicate if MD lord is maraka."""
        ctx = _build_chart_context(manish_chart)
        # Jupiter is current MD and is maraka for Mithuna
        assert ctx["is_md_lord_maraka"] is True
        assert ctx["is_md_lord_benefic"] is False

    def test_context_has_scripture_citations(self, manish_chart) -> None:
        """Context should include scripture citations."""
        ctx = _build_chart_context(manish_chart)
        assert len(ctx["scripture_citations"]) > 0

    def test_context_has_friend_enemy_groups(self, manish_chart) -> None:
        """Context should include friend/enemy groups."""
        ctx = _build_chart_context(manish_chart)
        assert ctx["friend_group"]
        assert ctx["enemy_group"]
        assert "Mercury" in ctx["friend_group"]

    def test_context_has_planets(self, manish_chart) -> None:
        """Context should have planet summaries."""
        ctx = _build_chart_context(manish_chart)
        assert len(ctx["planets"]) >= 9

    def test_context_has_yogas(self, manish_chart) -> None:
        """Context should have detected yogas."""
        ctx = _build_chart_context(manish_chart)
        assert isinstance(ctx["yogas"], list)

    def test_context_has_doshas(self, manish_chart) -> None:
        """Context should have detected doshas."""
        ctx = _build_chart_context(manish_chart)
        assert isinstance(ctx["doshas"], list)


class TestPromptRendering:
    """Tests for Jinja2 prompt rendering."""

    def test_system_prompt_renders(self, manish_chart) -> None:
        """System prompt should render without errors."""
        ctx = _build_chart_context(manish_chart)
        rendered = _render_prompt("system_prompt.md", ctx)
        assert "Mithuna" in rendered
        assert "MANDATORY RULES" in rendered
        assert "PROHIBITED" in rendered

    def test_remedy_prompt_renders(self, manish_chart) -> None:
        """Remedy prompt should render with gemstone framework."""
        ctx = _build_chart_context(manish_chart)
        rendered = _render_prompt("remedy_generation.md", ctx)
        assert "DECISION FRAMEWORK" in rendered
        assert "NEVER RECOMMEND" in rendered
        assert "Pukhraj" in rendered or "Yellow Sapphire" in rendered

    def test_career_prompt_renders(self, manish_chart) -> None:
        """Career prompt should render with maraka info."""
        ctx = _build_chart_context(manish_chart)
        rendered = _render_prompt("career_analysis.md", ctx)
        assert "MARAKA" in rendered
