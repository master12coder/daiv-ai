"""Performance and determinism tests for the engine."""

from __future__ import annotations

import time

from daivai_engine.compute.chart import compute_chart
from daivai_engine.compute.full_analysis import compute_full_analysis
from daivai_engine.models.chart import ChartData


class TestPerformance:
    def test_full_analysis_under_3_seconds(self, manish_chart: ChartData) -> None:
        start = time.perf_counter()
        compute_full_analysis(manish_chart)
        elapsed = time.perf_counter() - start
        assert elapsed < 3.0, f"Full analysis took {elapsed:.1f}s, limit is 3s"

    def test_chart_computation_under_1_second(self) -> None:
        start = time.perf_counter()
        compute_chart(
            name="Perf Test",
            dob="13/03/1989",
            tob="12:17",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"Chart computation took {elapsed:.1f}s"


class TestDeterminism:
    def test_full_analysis_deterministic(self, manish_chart: ChartData) -> None:
        """Two runs with same input must produce identical JSON."""
        a1 = compute_full_analysis(manish_chart)
        a2 = compute_full_analysis(manish_chart)
        # Compare key fields (full JSON comparison may fail due to transit date)
        assert a1.shadbala == a2.shadbala
        assert a1.gandanta == a2.gandanta
        assert a1.graha_yuddha == a2.graha_yuddha
        assert a1.deeptadi_avasthas == a2.deeptadi_avasthas
        assert a1.vimshopaka == a2.vimshopaka
        assert a1.ishta_kashta == a2.ishta_kashta
        assert a1.upapada == a2.upapada

    def test_chart_deterministic(self) -> None:
        c1 = compute_chart(
            "Test",
            "13/03/1989",
            "12:17",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        c2 = compute_chart(
            "Test",
            "13/03/1989",
            "12:17",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        for name in c1.planets:
            assert c1.planets[name].longitude == c2.planets[name].longitude
