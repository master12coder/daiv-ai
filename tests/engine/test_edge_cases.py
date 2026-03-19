"""Edge case tests for the chart computation engine."""

from __future__ import annotations

from daivai_engine.compute.chart import compute_chart
from daivai_engine.compute.verify import verify_chart_accuracy


def _compute_and_verify(**kwargs: object) -> list[str]:
    """Compute chart and return verification warnings."""
    chart = compute_chart(**kwargs)  # type: ignore[arg-type]
    return verify_chart_accuracy(chart)


class TestEdgeCases:
    def test_birth_at_midnight(self) -> None:
        """00:00 edge case — start of day."""
        chart = compute_chart(
            "Midnight",
            "15/08/1947",
            "00:00",
            lat=28.6139,
            lon=77.209,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        assert chart.lagna_sign  # Should compute without error
        errors = [w for w in verify_chart_accuracy(chart) if w.startswith("L1")]
        assert len(errors) == 0

    def test_birth_at_noon(self) -> None:
        """12:00 — Sun at highest point."""
        chart = compute_chart(
            "Noon",
            "01/01/2000",
            "12:00",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        assert chart.planets["Sun"].house in range(9, 12)  # Near MC

    def test_very_old_date(self) -> None:
        """1900 — Swiss Ephemeris should still work."""
        chart = compute_chart(
            "Old",
            "01/01/1900",
            "06:00",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        assert 0 <= chart.planets["Sun"].longitude < 360

    def test_future_date(self) -> None:
        """2050 — verify Swiss Ephemeris handles future dates."""
        chart = compute_chart(
            "Future",
            "01/01/2050",
            "12:00",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        assert chart.lagna_sign

    def test_southern_hemisphere(self) -> None:
        """Sydney, Australia — southern hemisphere."""
        chart = compute_chart(
            "Sydney",
            "01/01/2000",
            "12:00",
            lat=-33.8688,
            lon=151.2093,
            tz_name="Australia/Sydney",
            gender="Female",
        )
        errors = [w for w in verify_chart_accuracy(chart) if w.startswith("L1")]
        assert len(errors) == 0

    def test_western_hemisphere(self) -> None:
        """New York, USA — western hemisphere."""
        chart = compute_chart(
            "NYC",
            "04/07/1990",
            "10:30",
            lat=40.7128,
            lon=-74.006,
            tz_name="America/New_York",
            gender="Male",
        )
        errors = [w for w in verify_chart_accuracy(chart) if w.startswith("L1")]
        assert len(errors) == 0

    def test_extreme_latitude(self) -> None:
        """Reykjavik, Iceland (64°N) — extreme latitude."""
        chart = compute_chart(
            "Iceland",
            "21/06/2000",
            "12:00",
            lat=64.1466,
            lon=-21.9426,
            tz_name="Atlantic/Reykjavik",
            gender="Male",
        )
        # May have house calculation oddities but should not crash
        assert chart.lagna_sign

    def test_planet_at_sign_boundary(self) -> None:
        """Verify planets near 0° or 30° of a sign are handled correctly."""
        chart = compute_chart(
            "Boundary",
            "13/03/1989",
            "12:17",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        for name, p in chart.planets.items():
            assert 0 <= p.degree_in_sign < 30, f"{name} degree {p.degree_in_sign} out of range"

    def test_mercury_venus_near_sun(self) -> None:
        """Mercury and Venus should always be close to Sun."""
        chart = compute_chart(
            "Proximity",
            "13/03/1989",
            "12:17",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        sun_lon = chart.planets["Sun"].longitude
        merc_lon = chart.planets["Mercury"].longitude
        venus_lon = chart.planets["Venus"].longitude

        merc_dist = abs(merc_lon - sun_lon)
        if merc_dist > 180:
            merc_dist = 360 - merc_dist
        venus_dist = abs(venus_lon - sun_lon)
        if venus_dist > 180:
            venus_dist = 360 - venus_dist

        assert merc_dist <= 28.0, f"Mercury {merc_dist:.1f}° from Sun (max 28°)"
        assert venus_dist <= 47.0, f"Venus {venus_dist:.1f}° from Sun (max 47°)"

    def test_rahu_ketu_always_retrograde(self) -> None:
        chart = compute_chart(
            "Retro",
            "13/03/1989",
            "12:17",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        assert chart.planets["Rahu"].is_retrograde
        assert chart.planets["Ketu"].is_retrograde

    def test_sun_never_retrograde(self) -> None:
        chart = compute_chart(
            "Solar",
            "13/03/1989",
            "12:17",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            gender="Male",
        )
        assert not chart.planets["Sun"].is_retrograde
