"""Tests for the pandit plugin engine."""

from __future__ import annotations

from pathlib import Path

from jyotish_products.plugins.pandit.engine import add_correction, list_corrections


class TestPanditPlugin:
    def test_add_correction_returns_confirmation(self, tmp_path: Path) -> None:
        """add_correction should persist a correction and return a confirmation."""
        result = add_correction(
            chart_name="Manish Chaurasia",
            category="gemstone",
            what="Emerald should be worn on little finger, not ring finger",
            reasoning="Traditional Varanasi practice for Mercury remedies",
            data_dir=tmp_path,
        )
        assert isinstance(result, str)
        assert "Correction added" in result
        assert "gemstone" in result
        assert "Manish Chaurasia" in result

    def test_list_corrections_after_add(self, tmp_path: Path) -> None:
        """list_corrections should return the correction we just added."""
        add_correction(
            chart_name="Test Chart",
            category="dasha",
            what="Jupiter MD brings mixed results for Mithuna",
            reasoning="Kendradhipati dosha makes Jupiter a functional malefic",
            data_dir=tmp_path,
        )
        result = list_corrections(data_dir=tmp_path)
        assert "1 found" in result
        assert "dasha" in result
        assert "Test Chart" in result

    def test_list_corrections_empty(self, tmp_path: Path) -> None:
        """list_corrections on empty store should report no corrections."""
        result = list_corrections(data_dir=tmp_path)
        assert "No corrections found" in result
