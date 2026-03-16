"""Test dosha detection."""

import pytest
from jyotish.compute.dosha import (
    detect_mangal_dosha, detect_kaal_sarp_dosha,
    detect_sadesati, detect_pitra_dosha, detect_all_doshas,
)


class TestDoshaDetection:
    def test_detect_all_doshas_returns_four(self, manish_chart):
        doshas = detect_all_doshas(manish_chart)
        assert len(doshas) == 4

    def test_dosha_result_structure(self, manish_chart):
        doshas = detect_all_doshas(manish_chart)
        for d in doshas:
            assert isinstance(d.name, str)
            assert isinstance(d.name_hindi, str)
            assert isinstance(d.is_present, bool)
            assert d.severity in ("full", "partial", "cancelled", "none")
            assert isinstance(d.planets_involved, list)
            assert isinstance(d.description, str)

    def test_mangal_dosha(self, manish_chart):
        result = detect_mangal_dosha(manish_chart)
        mars = manish_chart.planets["Mars"]
        mangal_houses = {1, 2, 4, 7, 8, 12}
        if mars.house in mangal_houses:
            # Should detect some form of mangal dosha
            assert result.is_present or result.severity == "cancelled"
        else:
            assert not result.is_present

    def test_kaal_sarp_dosha(self, manish_chart):
        result = detect_kaal_sarp_dosha(manish_chart)
        assert result.name == "Kaal Sarp Dosha"
        # Just verify it runs without error

    def test_sadesati(self, manish_chart):
        result = detect_sadesati(manish_chart)
        assert result.name == "Sadesati"

    def test_sadesati_with_transit(self, manish_chart):
        """Test Sadesati detection with explicit transit Saturn sign."""
        moon_sign = manish_chart.planets["Moon"].sign_index
        # Saturn directly over Moon sign -> should detect Sadesati
        result = detect_sadesati(manish_chart, transit_saturn_sign=moon_sign)
        assert result.is_present
        assert "Peak" in result.description

    def test_pitra_dosha(self, manish_chart):
        result = detect_pitra_dosha(manish_chart)
        assert result.name == "Pitra Dosha"
