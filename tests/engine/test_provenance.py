"""Tests for computation provenance — every formula must have its source."""

from __future__ import annotations

from daivai_engine.knowledge.provenance import explain, get_all_sources, get_source


class TestProvenanceDatabase:
    def test_database_loads(self) -> None:
        sources = get_all_sources()
        assert len(sources) >= 10

    def test_every_major_computation_has_source(self) -> None:
        """ALL computations must have provenance entries — 47 total."""
        required = [
            # Core (16 original)
            "ayanamsha", "house_system", "exaltation", "mooltrikona",
            "natural_friendship", "combustion", "shadbala", "vimshottari",
            "kalachakra", "gajakesari", "budhaditya", "neech_bhanga",
            "mangal_dosha", "ashtakavarga", "gandanta", "double_transit",
            # Strength & Avasthas (4)
            "ishta_kashta", "bhava_bala", "deeptadi_avastha", "lajjitadi_avastha",
            # Dashas (5)
            "yogini_dasha", "ashtottari_dasha", "chara_dasha",
            "narayana_dasha", "dasha_sandhi",
            # Special checks (4)
            "graha_yuddha", "upapada", "argala", "gand_mool",
            # Transit (3)
            "sadesati", "vedha", "moorthy_nirnaya",
            # Special lagnas (3)
            "hora_lagna", "bhava_lagna", "ghatika_lagna",
            # KP (1)
            "kp_sublords",
            # Muhurta & Calendar (3)
            "muhurta_scoring", "choghadiya", "sankranti",
            # Namkaran (1)
            "namkaran_letters",
            # Varshphal & Prashna (2)
            "varshphal", "prashna",
            # Advanced (5)
            "sudarshan_chakra", "saham_points", "varga_analysis",
            "longevity_pindayu", "bhava_chalit",
        ]
        sources = get_all_sources()
        for name in required:
            assert name in sources, f"Missing provenance for '{name}'"

    def test_each_entry_has_source_and_rule(self) -> None:
        """Every entry must have at minimum a source and rule."""
        sources = get_all_sources()
        for name, info in sources.items():
            assert "source" in info or "sources" in info, f"'{name}' missing source"
            assert "rule" in info or "values" in info, f"'{name}' missing rule"

    def test_each_entry_has_alternatives(self) -> None:
        """Every entry should document alternative interpretations."""
        sources = get_all_sources()
        for name, info in sources.items():
            assert "alternatives" in info, f"'{name}' missing alternatives"

    def test_each_entry_has_confidence(self) -> None:
        """Every entry should have a confidence level."""
        sources = get_all_sources()
        for name, info in sources.items():
            assert "confidence" in info, f"'{name}' missing confidence"


class TestProvenanceLookup:
    def test_get_source_returns_dict(self) -> None:
        result = get_source("gajakesari")
        assert isinstance(result, dict)
        assert "rule" in result

    def test_get_source_missing_returns_empty(self) -> None:
        result = get_source("nonexistent_computation")
        assert result == {}

    def test_explain_returns_readable_string(self) -> None:
        text = explain("mangal_dosha")
        assert "MANGAL" in text or "mangal" in text.lower()
        assert "Source" in text
        assert "Rule" in text

    def test_explain_missing_returns_message(self) -> None:
        text = explain("nonexistent")
        assert "No provenance" in text


class TestCriticalSources:
    def test_rahu_ketu_exaltation_notes_alternative(self) -> None:
        """Rahu/Ketu exaltation is debated — must document both views."""
        info = get_source("exaltation")
        alts = " ".join(info.get("alternatives", []))
        assert "Gemini" in alts or "Nadi" in alts

    def test_combustion_has_retrograde_note(self) -> None:
        """Mercury/Venus combustion limits change when retrograde."""
        info = get_source("combustion")
        assert "retrograde" in str(info).lower()

    def test_kalachakra_notes_sensitivity(self) -> None:
        """Kalachakra must warn about birth time sensitivity."""
        info = get_source("kalachakra")
        inv = " ".join(info.get("invalidation", []))
        assert "birth time" in inv.lower() or "sensitive" in inv.lower()

    def test_shadbala_notes_kala_bala_limitation(self) -> None:
        """Kala Bala limitation must be documented."""
        info = get_source("shadbala")
        components = info.get("components", {})
        kala = components.get("kala_bala", {})
        assert "note" in kala or "missing" in str(kala).lower() or "5 of" in str(kala)
