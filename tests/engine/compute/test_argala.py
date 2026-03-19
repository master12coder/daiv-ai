"""Tests for Argala (Jaimini support/obstruction) computation."""

from __future__ import annotations

from daivai_engine.compute.argala import compute_argala
from daivai_engine.models.chart import ChartData


class TestArgala:
    def test_returns_twelve_results(self, manish_chart: ChartData) -> None:
        results = compute_argala(manish_chart)
        assert len(results) == 12

    def test_houses_numbered_1_to_12(self, manish_chart: ChartData) -> None:
        results = compute_argala(manish_chart)
        houses = {r.house for r in results}
        assert houses == set(range(1, 13))

    def test_net_argala_non_negative(self, manish_chart: ChartData) -> None:
        results = compute_argala(manish_chart)
        for r in results:
            assert r.net_argala_count >= 0

    def test_some_houses_supported(self, manish_chart: ChartData) -> None:
        """At least some houses should have argala support."""
        results = compute_argala(manish_chart)
        supported = [r for r in results if r.is_supported]
        assert len(supported) >= 3  # Realistic minimum
