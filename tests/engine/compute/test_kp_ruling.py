"""Tests for KP Ruling Planets computation."""

from __future__ import annotations

from datetime import date

from daivai_engine.compute.kp_ruling import compute_kp_ruling


class TestKPRuling:
    def test_returns_five_planets(self) -> None:
        result = compute_kp_ruling(target_date=date(2026, 3, 19))
        assert result.day_lord
        assert result.moon_sign_lord
        assert result.moon_star_lord
        assert result.moon_sub_lord
        assert result.lagna_sub_lord

    def test_ruling_list_not_empty(self) -> None:
        result = compute_kp_ruling(target_date=date(2026, 3, 19))
        assert len(result.ruling_planets) >= 1

    def test_day_lord_matches_weekday(self) -> None:
        """2026-03-19 is Thursday → Jupiter."""
        result = compute_kp_ruling(target_date=date(2026, 3, 19))
        assert result.day_lord == "Jupiter"

    def test_valid_planet_names(self) -> None:
        valid = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
        result = compute_kp_ruling(target_date=date(2026, 1, 15))
        for p in result.ruling_planets:
            assert p in valid

    def test_deterministic(self) -> None:
        r1 = compute_kp_ruling(target_date=date(2026, 6, 1))
        r2 = compute_kp_ruling(target_date=date(2026, 6, 1))
        assert r1.ruling_planets == r2.ruling_planets
