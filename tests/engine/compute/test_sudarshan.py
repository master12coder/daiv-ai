"""Tests for Sudarshan Chakra computation."""

from __future__ import annotations

from daivai_engine.compute.sudarshan import compute_sudarshan
from daivai_engine.models.chart import ChartData


class TestSudarshan:
    def test_returns_twelve_houses(self, manish_chart: ChartData) -> None:
        result = compute_sudarshan(manish_chart)
        assert len(result.houses) == 12

    def test_houses_numbered_1_to_12(self, manish_chart: ChartData) -> None:
        result = compute_sudarshan(manish_chart)
        houses = {h.house for h in result.houses}
        assert houses == set(range(1, 13))

    def test_strength_valid(self, manish_chart: ChartData) -> None:
        valid = {"triple_strong", "double_strong", "mixed", "weak"}
        result = compute_sudarshan(manish_chart)
        for h in result.houses:
            assert h.strength in valid

    def test_has_lords_and_occupants(self, manish_chart: ChartData) -> None:
        result = compute_sudarshan(manish_chart)
        for h in result.houses:
            assert h.lagna_lord
            assert h.moon_lord
            assert h.sun_lord
