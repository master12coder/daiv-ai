"""Tests for expanded scripture database."""

from __future__ import annotations

import pytest

from jyotish_engine.scriptures.query import (
    get_all_references,
    query_by_planet,
    query_by_topic,
    get_citation,
    reload,
)


class TestScriptureExpansion:
    """Tests for expanded BPHS chapters and Lal Kitab."""

    @pytest.fixture(autouse=True)
    def reload_db(self) -> None:
        """Ensure fresh load for each test."""
        reload()

    def test_total_rules_above_300(self) -> None:
        """Should have 300+ scripture rules after expansion."""
        refs = get_all_references()
        assert len(refs) >= 300, f"Only {len(refs)} rules, expected 300+"

    def test_planet_house_effects_present(self) -> None:
        """Chapter 11 planet-house effects should be loaded."""
        refs = query_by_topic("sun_in_houses")
        assert len(refs) > 0, "No planet-house effect rules found"

    def test_all_planets_have_house_effects(self) -> None:
        """Each planet should have house effect rules."""
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            refs = query_by_planet(planet)
            # At least the chapter 11 rules + chapter 3 nature rules
            assert len(refs) >= 5, f"{planet} has only {len(refs)} rules"

    def test_raja_yoga_rules_present(self) -> None:
        """Chapter 15 raja yoga rules should be loaded."""
        refs = query_by_topic("raja_yoga")
        assert len(refs) > 0, "No raja yoga rules found"

    def test_dasha_effect_rules_present(self) -> None:
        """Chapter 34 dasha effect rules should be loaded."""
        refs = query_by_topic("mahadasha")
        assert len(refs) > 0, "No mahadasha effect rules found"

    def test_muhurta_rules_present(self) -> None:
        """Chapter 81 muhurta rules should be loaded."""
        refs = query_by_topic("muhurta")
        assert len(refs) > 0, "No muhurta rules found"

    def test_remedy_rules_present(self) -> None:
        """Chapter 93 remedy rules should be loaded."""
        refs = [r for r in get_all_references() if r.rule_type == "remedy"]
        assert len(refs) >= 20, f"Only {len(refs)} remedy rules"

    def test_lal_kitab_rules_present(self) -> None:
        """Lal Kitab remedy rules should be loaded."""
        refs = [r for r in get_all_references() if r.book == "Lal Kitab"]
        assert len(refs) > 0, "No Lal Kitab rules found"

    def test_citations_format_correctly(self) -> None:
        """Citations should include book, chapter, and text."""
        refs = get_all_references()
        for ref in refs[:10]:
            citation = get_citation(ref)
            assert ref.book in citation
            assert str(ref.chapter) in citation

    def test_hindi_text_present(self) -> None:
        """Most rules should have Hindi text."""
        refs = get_all_references()
        with_hindi = sum(1 for r in refs if r.text_hindi)
        ratio = with_hindi / len(refs) if refs else 0
        assert ratio >= 0.5, f"Only {ratio:.0%} rules have Hindi text"

    def test_jupiter_in_12th_for_mithuna(self) -> None:
        """Should find rules for Jupiter in 12th house."""
        refs = query_by_planet("Jupiter", house=12)
        assert len(refs) > 0, "No rules for Jupiter in 12th house"

    def test_saturn_in_7th_marriage(self) -> None:
        """Should find rules about Saturn affecting 7th house."""
        refs = query_by_planet("Saturn", house=7)
        assert len(refs) > 0, "No rules for Saturn in 7th house"
