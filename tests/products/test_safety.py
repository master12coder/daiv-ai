"""Safety tests — gemstone recommendations, maraka detection, validation.

These are the most critical tests in the entire project. They verify
that the system never recommends dangerous gemstones.
"""

from __future__ import annotations

import pytest

from jyotish_products.interpret.context import build_lordship_context
from jyotish_products.interpret.validator import validate_interpretation


# All 12 lagnas with their known maraka and prohibited data
LAGNA_MARAKA = {
    "Mesha": {"maraka": ["Venus"], "prohibited_planets": ["Mercury", "Venus"]},
    "Vrishabha": {"maraka": ["Mars"], "prohibited_planets": ["Sun", "Mars"]},
    "Mithuna": {"maraka": ["Moon", "Jupiter"], "prohibited_planets": ["Moon", "Mars", "Jupiter"]},
    "Karka": {"maraka": ["Saturn"], "prohibited_planets": ["Mercury", "Venus"]},
    "Simha": {"maraka": ["Saturn"], "prohibited_planets": ["Venus", "Saturn"]},
    "Kanya": {"maraka": ["Jupiter", "Mars"], "prohibited_planets": ["Mars", "Jupiter"]},
    "Tula": {"maraka": ["Mars"], "prohibited_planets": ["Sun", "Mars", "Jupiter"]},
    "Vrischika": {"maraka": ["Venus", "Jupiter"], "prohibited_planets": ["Mercury", "Venus"]},
    "Dhanu": {"maraka": ["Saturn", "Mercury"], "prohibited_planets": ["Venus", "Saturn"]},
    "Makara": {"maraka": ["Moon"], "prohibited_planets": ["Mars", "Jupiter"]},
    "Kumbha": {"maraka": ["Sun"], "prohibited_planets": ["Mars", "Jupiter"]},
    "Meena": {"maraka": ["Mercury"], "prohibited_planets": ["Saturn", "Venus"]},
}


class TestLordshipContext:
    """Tests for lordship context loading."""

    @pytest.mark.parametrize("lagna", [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena",
    ])
    def test_lordship_context_loads_for_all_lagnas(self, lagna: str) -> None:
        """Every lagna should have lordship context."""
        ctx = build_lordship_context(lagna)
        assert ctx, f"No lordship context for {lagna}"
        assert ctx.get("sign_lord"), f"No sign lord for {lagna}"
        assert ctx.get("functional_benefics"), f"No benefics for {lagna}"
        assert ctx.get("maraka"), f"No maraka for {lagna}"

    @pytest.mark.parametrize("lagna", [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena",
    ])
    def test_prohibited_stones_exist_for_all_lagnas(self, lagna: str) -> None:
        """Every lagna should have at least one prohibited stone."""
        ctx = build_lordship_context(lagna)
        assert ctx.get("prohibited_stones"), f"No prohibited stones for {lagna}"

    @pytest.mark.parametrize("lagna", [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena",
    ])
    def test_recommended_stones_exist_for_all_lagnas(self, lagna: str) -> None:
        """Every lagna should have at least one recommended stone."""
        ctx = build_lordship_context(lagna)
        assert ctx.get("recommended_stones"), f"No recommended stones for {lagna}"


class TestMithunaSpecific:
    """Safety tests specific to Mithuna (Gemini) lagna."""

    def test_mithuna_jupiter_is_maraka(self) -> None:
        """Jupiter MUST be maraka for Mithuna."""
        ctx = build_lordship_context("Mithuna")
        maraka_names = [m["planet"] for m in ctx["maraka"]]
        assert "Jupiter" in maraka_names

    def test_mithuna_moon_is_maraka(self) -> None:
        """Moon MUST be maraka for Mithuna."""
        ctx = build_lordship_context("Mithuna")
        maraka_names = [m["planet"] for m in ctx["maraka"]]
        assert "Moon" in maraka_names

    def test_mithuna_pukhraj_prohibited(self) -> None:
        """Yellow Sapphire (Pukhraj) MUST be prohibited for Mithuna."""
        ctx = build_lordship_context("Mithuna")
        prohibited_stones = [s["stone"] for s in ctx["prohibited_stones"]]
        assert any("Pukhraj" in s or "Yellow Sapphire" in s for s in prohibited_stones)

    def test_mithuna_panna_recommended(self) -> None:
        """Emerald (Panna) MUST be recommended for Mithuna."""
        ctx = build_lordship_context("Mithuna")
        recommended_stones = [s["stone"] for s in ctx["recommended_stones"]]
        assert any("Panna" in s or "Emerald" in s for s in recommended_stones)

    def test_mithuna_mercury_is_lagnesh(self) -> None:
        """Mercury MUST be sign lord (lagnesh) for Mithuna."""
        ctx = build_lordship_context("Mithuna")
        assert ctx["sign_lord"] == "Mercury"

    def test_mithuna_mars_is_malefic(self) -> None:
        """Mars MUST be functional malefic for Mithuna."""
        ctx = build_lordship_context("Mithuna")
        malefic_names = [m["planet"] for m in ctx.get("functional_malefics", [])]
        assert "Mars" in malefic_names


class TestPostValidation:
    """Tests for post-generation safety validation."""

    def test_catches_prohibited_stone_recommendation(self) -> None:
        """Should catch when a prohibited stone is recommended."""
        ctx = build_lordship_context("Mithuna")
        text = "I recommend wearing Yellow Sapphire (Pukhraj) for career growth."
        _, errors = validate_interpretation(text, "Mithuna", ctx)
        assert len(errors) > 0
        assert any("DANGER" in e for e in errors)

    def test_allows_correct_recommendation(self) -> None:
        """Should not flag correct stone recommendations."""
        ctx = build_lordship_context("Mithuna")
        text = "Wear Emerald (Panna) for Mercury strengthening."
        _, errors = validate_interpretation(text, "Mithuna", ctx)
        assert len(errors) == 0

    def test_catches_maraka_called_benefic(self) -> None:
        """Should catch maraka planet called benefic."""
        ctx = build_lordship_context("Mithuna")
        text = "Jupiter is benefic and will bring prosperity."
        _, errors = validate_interpretation(text, "Mithuna", ctx)
        assert len(errors) > 0

    def test_no_false_positive_on_emotional(self) -> None:
        """Should NOT flag 'emotional' as containing 'Moti'."""
        ctx = build_lordship_context("Mithuna")
        text = "The Moon-Mars conjunction brings emotional strength and beneficial courage."
        _, errors = validate_interpretation(text, "Mithuna", ctx)
        assert len(errors) == 0

    def test_catches_pearl_recommendation(self) -> None:
        """Should catch Pearl recommendation for Mithuna."""
        ctx = build_lordship_context("Mithuna")
        text = "Wear Pearl (Moti) to strengthen your Moon for emotional balance."
        _, errors = validate_interpretation(text, "Mithuna", ctx)
        assert len(errors) > 0

    def test_allows_pearl_in_avoid_context(self) -> None:
        """Should not flag Pearl when it's in an 'avoid' context."""
        ctx = build_lordship_context("Mithuna")
        text = "Avoid wearing Pearl (Moti) as Moon is maraka for your lagna."
        _, errors = validate_interpretation(text, "Mithuna", ctx)
        assert len(errors) == 0

    def test_catches_red_coral_recommendation(self) -> None:
        """Should catch Red Coral recommendation for Mithuna."""
        ctx = build_lordship_context("Mithuna")
        text = "I recommend wearing Red Coral to strengthen Mars."
        _, errors = validate_interpretation(text, "Mithuna", ctx)
        assert len(errors) > 0

    def test_catches_worship_maraka(self) -> None:
        """Should catch worshipping a maraka planet."""
        ctx = build_lordship_context("Mithuna")
        text = "Worship Jupiter on Thursdays for career success."
        _, errors = validate_interpretation(text, "Mithuna", ctx)
        assert len(errors) > 0

    def test_validation_appends_warnings(self) -> None:
        """Should append safety warnings to flagged text."""
        ctx = build_lordship_context("Mithuna")
        text = "Wear Yellow Sapphire for career."
        validated, errors = validate_interpretation(text, "Mithuna", ctx)
        assert len(errors) > 0
        assert "SAFETY VALIDATION WARNINGS" in validated
        assert "Parashari rule engine" in validated
