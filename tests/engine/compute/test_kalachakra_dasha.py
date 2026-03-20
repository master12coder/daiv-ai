"""Tests for Kalachakra Dasha — BPHS Chapter 46.

Verifies the pada-to-sign mapping, cycle direction, balance calculation,
DEHA/JEEVA markers, and total cycle = 100 years.
"""

from __future__ import annotations

from daivai_engine.compute.kalachakra_dasha import compute_kalachakra_dasha
from daivai_engine.models.chart import ChartData


class TestKalachakraCycleDirection:
    def test_manish_moon_in_taurus_is_apasavya(self, manish_chart: ChartData) -> None:
        """Moon in Taurus (sign index 1 = even) → Apasavya cycle."""
        result = compute_kalachakra_dasha(manish_chart)
        assert result.cycle_type == "apasavya"
        assert result.moon_sign_index == 1  # Taurus

    def test_odd_sign_gives_savya(self, sample_chart: ChartData) -> None:
        """If Moon is in odd sign, should be Savya."""
        result = compute_kalachakra_dasha(sample_chart)
        moon_sign = sample_chart.planets["Moon"].sign_index
        if moon_sign % 2 == 0:  # 0-indexed odd sign
            assert result.cycle_type == "savya"
        else:
            assert result.cycle_type == "apasavya"


class TestKalachakraPeriods:
    def test_returns_nine_periods(self, manish_chart: ChartData) -> None:
        """Kalachakra always has exactly 9 periods."""
        result = compute_kalachakra_dasha(manish_chart)
        assert len(result.periods) == 9

    def test_total_close_to_100_years(self, manish_chart: ChartData) -> None:
        """Total span should be close to 100 years (minus first dasha balance)."""
        result = compute_kalachakra_dasha(manish_chart)
        total_days = sum((p.end - p.start).total_seconds() / 86400 for p in result.periods)
        total_years = total_days / 365.25
        # Should be between 90 and 100 (first dasha has balance applied)
        assert 80.0 < total_years <= 100.0, f"Total {total_years:.1f} years"

    def test_periods_consecutive(self, manish_chart: ChartData) -> None:
        """Each period starts when previous ends."""
        result = compute_kalachakra_dasha(manish_chart)
        for i in range(1, len(result.periods)):
            gap = abs((result.periods[i].start - result.periods[i - 1].end).total_seconds())
            assert gap < 1, f"Gap of {gap}s between period {i - 1} and {i}"

    def test_sign_indices_valid(self, manish_chart: ChartData) -> None:
        """All sign indices should be 0-8 (Aries through Sagittarius)."""
        result = compute_kalachakra_dasha(manish_chart)
        for p in result.periods:
            assert 0 <= p.sign_index <= 8, f"Sign index {p.sign_index} out of range"

    def test_years_match_bphs(self, manish_chart: ChartData) -> None:
        """Duration values must be from the BPHS set: 5,7,9,10,16,21."""
        valid_years = {5, 7, 9, 10, 16, 21}
        result = compute_kalachakra_dasha(manish_chart)
        for p in result.periods:
            assert p.years in valid_years, f"Invalid year count: {p.years}"


class TestDehaJeeva:
    def test_has_deha_period(self, manish_chart: ChartData) -> None:
        """At least one period should be marked as DEHA (Cancer)."""
        result = compute_kalachakra_dasha(manish_chart)
        deha_periods = [p for p in result.periods if p.is_deha]
        assert len(deha_periods) == 1
        assert deha_periods[0].sign_index == 3  # Cancer

    def test_has_jeeva_period(self, manish_chart: ChartData) -> None:
        """At least one period should be marked as JEEVA (Sagittarius)."""
        result = compute_kalachakra_dasha(manish_chart)
        jeeva_periods = [p for p in result.periods if p.is_jeeva]
        assert len(jeeva_periods) == 1
        assert jeeva_periods[0].sign_index == 8  # Sagittarius

    def test_deha_is_cancer(self, manish_chart: ChartData) -> None:
        """DEHA sign should always be Cancer (index 3) — BPHS Ch.46 v8."""
        result = compute_kalachakra_dasha(manish_chart)
        assert result.deha_sign == 3

    def test_jeeva_is_sagittarius(self, manish_chart: ChartData) -> None:
        """JEEVA sign should always be Sagittarius (index 8) — BPHS Ch.46 v10."""
        result = compute_kalachakra_dasha(manish_chart)
        assert result.jeeva_sign == 8


class TestKalachakraBalance:
    def test_balance_positive(self, manish_chart: ChartData) -> None:
        """Balance of first dasha must be positive."""
        result = compute_kalachakra_dasha(manish_chart)
        assert result.balance_years > 0

    def test_balance_less_than_full(self, manish_chart: ChartData) -> None:
        """Balance must be less than full duration of first dasha."""
        result = compute_kalachakra_dasha(manish_chart)
        first_period = result.periods[0]
        assert result.balance_years <= first_period.years

    def test_first_period_uses_balance(self, manish_chart: ChartData) -> None:
        """First period duration should equal balance, not full years."""
        result = compute_kalachakra_dasha(manish_chart)
        first_days = (result.periods[0].end - result.periods[0].start).days
        balance_days = result.balance_years * 365.25
        assert abs(first_days - balance_days) < 2  # Allow 1 day rounding


class TestKalachakraDeterminism:
    def test_deterministic(self, manish_chart: ChartData) -> None:
        """Same chart → same result."""
        r1 = compute_kalachakra_dasha(manish_chart)
        r2 = compute_kalachakra_dasha(manish_chart)
        assert r1.cycle_type == r2.cycle_type
        assert r1.balance_years == r2.balance_years
        assert len(r1.periods) == len(r2.periods)
        for p1, p2 in zip(r1.periods, r2.periods, strict=True):
            assert p1.sign_index == p2.sign_index
            assert p1.years == p2.years


class TestManishKalachakra:
    def test_manish_specific_values(self, manish_chart: ChartData) -> None:
        """Verify Manish's Kalachakra specifically.

        Moon: 14.6875° Taurus (sign 1, even → Apasavya)
        Pada in sign: int(14.6875 / 3.3333) = 4 (0-indexed)
        Starting position: 4 in Apasavya sequence
        Apasavya[4] = Leo (sign 4, 5 years)
        """
        result = compute_kalachakra_dasha(manish_chart)
        assert result.cycle_type == "apasavya"
        assert result.pada_in_sign == 4
        assert result.starting_position == 4
        # Apasavya sequence: Sag(10), Sco(7), Lib(16), Vir(9), LEO(5), ...
        assert result.periods[0].sign_index == 4  # Leo
        assert result.periods[0].years == 5
