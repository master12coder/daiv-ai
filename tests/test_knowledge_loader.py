"""Tests for knowledge_loader module."""

from __future__ import annotations

import pytest

from jyotish.interpret.knowledge_loader import (
    build_lordship_context,
    build_gemstone_context,
    build_scripture_context,
    get_lordship_data,
    get_gemstone_data,
)


class TestLordshipDataLoading:
    """Tests for lordship rules YAML loading."""

    def test_loads_all_12_lagnas(self) -> None:
        """Should load rules for all 12 lagnas."""
        data = get_lordship_data()
        lagnas = data.get("lagnas", {})
        expected = [
            "mesha", "vrishabha", "mithuna", "karka", "simha", "kanya",
            "tula", "vrischika", "dhanu", "makara", "kumbha", "meena",
        ]
        for lagna in expected:
            assert lagna in lagnas, f"Missing lagna: {lagna}"

    def test_each_lagna_has_house_lords(self) -> None:
        """Each lagna should have 12 house lords."""
        data = get_lordship_data()
        for lagna_key, rules in data.get("lagnas", {}).items():
            house_lords = rules.get("house_lords", {})
            assert len(house_lords) == 12, f"{lagna_key}: has {len(house_lords)} house lords"

    def test_each_lagna_has_gemstone_recs(self) -> None:
        """Each lagna should have gemstone recommendations."""
        data = get_lordship_data()
        for lagna_key, rules in data.get("lagnas", {}).items():
            gem_recs = rules.get("gemstone_recommendations", {})
            assert len(gem_recs) >= 5, f"{lagna_key}: only {len(gem_recs)} gem recs"


class TestGemstoneDataLoading:
    """Tests for gemstone_logic.yaml loading."""

    def test_loads_all_9_gemstones(self) -> None:
        """Should have gemstone data for all 9 planets."""
        data = get_gemstone_data()
        gemstones = data.get("gemstones", {})
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            assert planet in gemstones, f"Missing gemstone for {planet}"

    def test_contraindications_exist(self) -> None:
        """Should have at least 3 contraindication rules."""
        data = get_gemstone_data()
        contras = data.get("contraindications", [])
        assert len(contras) >= 3

    def test_planetary_friendships_exist(self) -> None:
        """Should have friend/enemy mappings."""
        data = get_gemstone_data()
        friends = data.get("planetary_friendships", {})
        assert "friends" in friends
        assert "enemies" in friends


class TestScriptureContext:
    """Tests for scripture context building."""

    def test_builds_citations(self, manish_chart) -> None:
        """Should build scripture citations for a chart."""
        citations = build_scripture_context(manish_chart)
        assert len(citations) > 0
        assert all(isinstance(c, str) for c in citations)

    def test_citations_include_bphs(self, manish_chart) -> None:
        """Citations should reference BPHS."""
        citations = build_scripture_context(manish_chart)
        assert any("BPHS" in c for c in citations)


class TestLordshipContextBuilding:
    """Tests for build_lordship_context."""

    def test_mithuna_has_correct_structure(self) -> None:
        """Mithuna context should have all required keys."""
        ctx = build_lordship_context("Mithuna")
        required_keys = [
            "sign_lord", "yogakaraka", "functional_benefics",
            "functional_malefics", "maraka", "house_lords",
            "recommended_stones", "prohibited_stones",
        ]
        for key in required_keys:
            assert key in ctx, f"Missing key: {key}"

    def test_unknown_lagna_returns_empty(self) -> None:
        """Unknown lagna should return empty context."""
        ctx = build_lordship_context("Bogus")
        assert ctx == {}

    def test_case_insensitive(self) -> None:
        """Should work regardless of case."""
        ctx1 = build_lordship_context("Mithuna")
        ctx2 = build_lordship_context("mithuna")
        assert ctx1 == ctx2
