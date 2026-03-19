"""Tests for Saham (sensitive points) computation."""

from __future__ import annotations

from daivai_engine.compute.saham import compute_sahams
from daivai_engine.models.chart import ChartData


class TestSahams:
    def test_returns_six_sahams(self, manish_chart: ChartData) -> None:
        results = compute_sahams(manish_chart)
        assert len(results) == 6

    def test_names_correct(self, manish_chart: ChartData) -> None:
        results = compute_sahams(manish_chart)
        names = {r.name for r in results}
        expected = {
            "Punya Saham",
            "Vivaha Saham",
            "Putra Saham",
            "Karma Saham",
            "Vidya Saham",
            "Mrityu Saham",
        }
        assert names == expected

    def test_longitudes_valid(self, manish_chart: ChartData) -> None:
        results = compute_sahams(manish_chart)
        for s in results:
            assert 0 <= s.longitude < 360
            assert 0 <= s.sign_index <= 11
            assert s.nakshatra

    def test_has_hindi_names(self, manish_chart: ChartData) -> None:
        results = compute_sahams(manish_chart)
        for s in results:
            assert s.name_hi
