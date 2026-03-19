"""Tests for Special Lagnas — Hora, Bhava, Ghatika."""

from __future__ import annotations

from daivai_engine.compute.special_lagnas import compute_special_lagnas
from daivai_engine.models.chart import ChartData


class TestSpecialLagnas:
    def test_returns_three_lagnas(self, manish_chart: ChartData) -> None:
        result = compute_special_lagnas(manish_chart)
        assert "hora" in result
        assert "bhava" in result
        assert "ghatika" in result

    def test_longitudes_valid(self, manish_chart: ChartData) -> None:
        result = compute_special_lagnas(manish_chart)
        for key in ("hora", "bhava", "ghatika"):
            lagna = result[key]
            assert 0 <= lagna.longitude < 360
            assert 0 <= lagna.sign_index <= 11
            assert 0 <= lagna.degree_in_sign < 30

    def test_has_hindi_names(self, manish_chart: ChartData) -> None:
        result = compute_special_lagnas(manish_chart)
        for key in ("hora", "bhava", "ghatika"):
            assert result[key].sign_hi
            assert result[key].sign_en

    def test_deterministic(self, manish_chart: ChartData) -> None:
        r1 = compute_special_lagnas(manish_chart)
        r2 = compute_special_lagnas(manish_chart)
        assert r1["hora"].longitude == r2["hora"].longitude
