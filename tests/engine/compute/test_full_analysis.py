"""Tests for the full chart analysis — all computations in one call."""

from __future__ import annotations

from daivai_engine.compute.full_analysis import compute_full_analysis
from daivai_engine.models.chart import ChartData


def _lordship(chart: ChartData) -> dict:
    """Build lordship context via products layer (test helper)."""
    from daivai_products.interpret.context import build_lordship_context

    return build_lordship_context(chart.lagna_sign)


class TestFullChartAnalysis:
    def test_all_core_fields(self, manish_chart: ChartData) -> None:
        ctx = _lordship(manish_chart)
        a = compute_full_analysis(manish_chart, lordship_context=ctx)
        assert a.chart.name == "Manish Chaurasia"
        assert len(a.mahadashas) == 9
        assert len(a.shadbala) == 7
        assert len(a.gandanta) == 9
        assert len(a.deeptadi_avasthas) == 7
        assert len(a.vimshopaka) == 7
        assert len(a.ishta_kashta) == 7
        assert len(a.double_transit) == 12
        assert len(a.double_transit_moon) == 12

    def test_new_section_a_fields(self, manish_chart: ChartData) -> None:
        """Narayana dasha, special lagnas, KP should be present."""
        a = compute_full_analysis(manish_chart)
        assert len(a.narayana_dasha) == 12
        assert "hora" in a.special_lagnas
        assert "bhava" in a.special_lagnas
        assert "ghatika" in a.special_lagnas

    def test_new_section_b_fields(self, manish_chart: ChartData) -> None:
        """Sudarshan, argala, sahams, house shifts should be present."""
        a = compute_full_analysis(manish_chart)
        assert a.sudarshan is not None
        assert len(a.argala) == 12
        assert len(a.sahams) == 6
        assert isinstance(a.house_shifts, list)

    def test_deterministic(self, manish_chart: ChartData) -> None:
        a1 = compute_full_analysis(manish_chart)
        a2 = compute_full_analysis(manish_chart)
        assert a1.shadbala == a2.shadbala
        assert a1.gandanta == a2.gandanta
        assert a1.upapada == a2.upapada

    def test_lordship_context(self, manish_chart: ChartData) -> None:
        ctx = _lordship(manish_chart)
        a = compute_full_analysis(manish_chart, lordship_context=ctx)
        assert "functional_benefics" in a.lordship_context

    def test_verification_clean(self, manish_chart: ChartData) -> None:
        a = compute_full_analysis(manish_chart)
        errors = [w for w in a.verification_warnings if w.startswith("L1")]
        assert len(errors) == 0

    def test_version(self, manish_chart: ChartData) -> None:
        a = compute_full_analysis(manish_chart)
        assert a.version == "2.0"

    def test_json_roundtrip(self, manish_chart: ChartData) -> None:
        a = compute_full_analysis(manish_chart)
        json_str = a.model_dump_json()
        from daivai_engine.models.analysis import FullChartAnalysis

        restored = FullChartAnalysis.model_validate_json(json_str)
        assert restored.chart.name == a.chart.name
        assert len(restored.shadbala) == len(a.shadbala)
