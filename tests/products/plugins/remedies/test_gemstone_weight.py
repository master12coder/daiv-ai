"""Tests for the multi-factor gemstone weight engine."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.models.chart import ChartData
from jyotish_products.plugins.remedies.formatter import format_gemstone_report
from jyotish_products.plugins.remedies.gemstone import (
    AVASTHA_MULT,
    DIGNITY_MULT,
    PLANET_STONE,
    PURPOSE_MULT,
    GemstoneWeightResult,
    WeightFactor,
    compute_gemstone_weights,
)


@pytest.fixture
def manish_chart() -> ChartData:
    """Reference chart: Manish Chaurasia — Mithuna lagna."""
    return compute_chart(
        name="Manish Chaurasia",
        dob="13/03/1989",
        tob="12:17",
        lat=25.3176,
        lon=83.0067,
        tz_name="Asia/Kolkata",
        gender="Male",
    )


class TestGemstoneWeightComputation:
    """Core weight computation tests using Manish fixture."""

    def test_returns_list_of_results(self, manish_chart: ChartData) -> None:
        """compute_gemstone_weights returns a list of GemstoneWeightResult."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(r, GemstoneWeightResult) for r in results)

    def test_covers_all_nine_planets(self, manish_chart: ChartData) -> None:
        """All 9 planets should have a result."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        planets = {r.planet for r in results}
        expected = set(PLANET_STONE.keys())
        assert planets == expected

    @pytest.mark.safety
    def test_panna_recommended_for_mithuna(self, manish_chart: ChartData) -> None:
        """Emerald (Panna) MUST be recommended for Mithuna lagna."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        panna = next(r for r in results if r.planet == "Mercury")
        assert panna.status == "recommended"
        assert panna.stone_name == "Emerald"

    def test_panna_weight_in_expected_range(self, manish_chart: ChartData) -> None:
        """Panna should compute ~2.5-3.5 ratti (Mercury at 28° Mruta)."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        panna = next(r for r in results if r.planet == "Mercury")
        assert panna.recommended_ratti >= 2.0, f"Too low: {panna.recommended_ratti}"
        assert panna.recommended_ratti <= 4.5, f"Too high: {panna.recommended_ratti}"

    def test_panna_has_ten_factors(self, manish_chart: ChartData) -> None:
        """Each recommended stone must have exactly 10 weight factors."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        panna = next(r for r in results if r.planet == "Mercury")
        assert len(panna.factors) == 10
        factor_names = [f.name for f in panna.factors]
        assert "Body Weight" in factor_names
        assert "Avastha" in factor_names
        assert "Ashtakavarga" in factor_names
        assert "Dignity" in factor_names
        assert "Combustion" in factor_names
        assert "Retrograde" in factor_names
        assert "Current Dasha" in factor_names
        assert "Lordship" in factor_names
        assert "Stone Energy" in factor_names
        assert "Purpose" in factor_names

    def test_mercury_avastha_matches_chart(self, manish_chart: ChartData) -> None:
        """Mercury avastha should match computed chart data."""
        mercury = manish_chart.planets["Mercury"]
        # Mercury at ~10° → Kumara (6-12° range)
        assert mercury.avastha in AVASTHA_MULT

    def test_avastha_factor_matches_chart(self, manish_chart: ChartData) -> None:
        """Avastha factor multiplier should match planet's actual avastha."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        panna = next(r for r in results if r.planet == "Mercury")
        mercury = manish_chart.planets["Mercury"]
        avastha_factor = next(f for f in panna.factors if f.name == "Avastha")
        assert avastha_factor.multiplier == AVASTHA_MULT[mercury.avastha]
        assert avastha_factor.multiplier <= 1.0

    @pytest.mark.safety
    def test_pukhraj_prohibited_for_mithuna(self, manish_chart: ChartData) -> None:
        """Yellow Sapphire (Pukhraj) MUST be PROHIBITED for Mithuna lagna."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        pukhraj = next(r for r in results if r.planet == "Jupiter")
        assert pukhraj.status == "prohibited"
        assert pukhraj.recommended_ratti == 0
        assert pukhraj.prohibition_reason is not None
        assert len(pukhraj.prohibition_reason) > 0

    @pytest.mark.safety
    def test_moonga_prohibited_for_mithuna(self, manish_chart: ChartData) -> None:
        """Red Coral (Moonga) MUST be PROHIBITED — Mars is 6th lord."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        moonga = next(r for r in results if r.planet == "Mars")
        assert moonga.status == "prohibited"

    @pytest.mark.safety
    def test_moti_prohibited_for_mithuna(self, manish_chart: ChartData) -> None:
        """Pearl (Moti) MUST be PROHIBITED — Moon is 2nd lord (maraka)."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        moti = next(r for r in results if r.planet == "Moon")
        assert moti.status == "prohibited"

    def test_prohibited_stones_have_zero_weight(self, manish_chart: ChartData) -> None:
        """All prohibited stones must have 0 ratti."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        for r in results:
            if r.status == "prohibited":
                assert r.recommended_ratti == 0, f"{r.stone_name} should be 0"
                assert r.base_ratti == 0

    def test_prohibited_stones_have_free_alternatives(self, manish_chart: ChartData) -> None:
        """Prohibited stones should still list free alternatives."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        for r in results:
            if r.status == "prohibited":
                assert len(r.free_alternatives) > 0, f"{r.stone_name} missing alternatives"


class TestWebsiteComparison:
    """Test website estimate comparison."""

    def test_five_websites_present(self, manish_chart: ChartData) -> None:
        """Each recommended stone should compare against 5 websites."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        panna = next(r for r in results if r.planet == "Mercury")
        assert len(panna.website_comparisons) == 5
        assert "GemPundit" in panna.website_comparisons
        assert "BrahmaGems" in panna.website_comparisons
        assert "GemsMantra" in panna.website_comparisons
        assert "ShubhGems" in panna.website_comparisons
        assert "MyRatna" in panna.website_comparisons

    def test_websites_use_body_weight_formula(self, manish_chart: ChartData) -> None:
        """Website estimates should be based on body weight."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        panna = next(r for r in results if r.planet == "Mercury")
        # GemPundit uses simple body_weight / divisor
        assert panna.website_comparisons["GemPundit"] == round(78.0 / 12, 1)

    def test_our_engine_lower_than_naive(self, manish_chart: ChartData) -> None:
        """10-factor adjusted weight should be LOWER than naive body weight formula."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        panna = next(r for r in results if r.planet == "Mercury")
        naive = 78.0 / 12  # 6.5
        assert panna.recommended_ratti < naive


class TestProsCons:
    """Test weight option pros/cons."""

    def test_three_weight_options(self, manish_chart: ChartData) -> None:
        """Pros/cons should cover light, medium, heavy."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        panna = next(r for r in results if r.planet == "Mercury")
        assert len(panna.pros_cons) == 3


class TestPurposeMultiplier:
    """Test that purpose affects weight."""

    def test_protection_less_than_growth(self, manish_chart: ChartData) -> None:
        """Protection purpose should yield lower weight than growth."""
        r_prot = compute_gemstone_weights(manish_chart, 78.0, "protection")
        r_grow = compute_gemstone_weights(manish_chart, 78.0, "growth")
        panna_p = next(r for r in r_prot if r.planet == "Mercury")
        panna_g = next(r for r in r_grow if r.planet == "Mercury")
        assert panna_p.recommended_ratti <= panna_g.recommended_ratti

    def test_maximum_highest(self, manish_chart: ChartData) -> None:
        """Maximum purpose should yield highest weight."""
        r_max = compute_gemstone_weights(manish_chart, 78.0, "maximum")
        r_grow = compute_gemstone_weights(manish_chart, 78.0, "growth")
        panna_m = next(r for r in r_max if r.planet == "Mercury")
        panna_g = next(r for r in r_grow if r.planet == "Mercury")
        assert panna_m.recommended_ratti >= panna_g.recommended_ratti


class TestFormatReport:
    """Test report formatting."""

    def test_report_contains_key_sections(self, manish_chart: ChartData) -> None:
        """Report should contain all required sections."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        report = format_gemstone_report(results, 78.0, "Mithuna", "Manish Chaurasia")
        assert "RECOMMENDED STONES" in report
        assert "PROHIBITED STONES" in report
        assert "QUALITY vs WEIGHT" in report
        assert "SHASTRA NOTE" in report
        assert "DISCUSS WITH YOUR PANDIT JI" in report

    def test_report_includes_factor_breakdown(self, manish_chart: ChartData) -> None:
        """Report should include factor breakdown table."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        report = format_gemstone_report(results, 78.0, "Mithuna", "Manish Chaurasia")
        assert "Factor Breakdown" in report
        assert "Avastha" in report
        assert "Dignity" in report

    def test_report_includes_website_comparison(self, manish_chart: ChartData) -> None:
        """Report should include website comparison."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        report = format_gemstone_report(results, 78.0, "Mithuna", "Manish Chaurasia")
        assert "GemPundit" in report
        assert "BrahmaGems" in report

    def test_report_includes_pukhraj_prohibited(self, manish_chart: ChartData) -> None:
        """Pukhraj must appear in prohibited section of report."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        report = format_gemstone_report(results, 78.0, "Mithuna", "Manish Chaurasia")
        prohibited_idx = report.index("PROHIBITED STONES")
        assert "Yellow Sapphire" in report[prohibited_idx:]

    def test_report_includes_free_alternatives(self, manish_chart: ChartData) -> None:
        """Report should include free alternatives for prohibited stones."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        report = format_gemstone_report(results, 78.0, "Mithuna", "Manish Chaurasia")
        assert "Free alt" in report or "Free Alternatives" in report


class TestSortOrder:
    """Test result ordering."""

    def test_recommended_first_prohibited_last(self, manish_chart: ChartData) -> None:
        """Results should be sorted: recommended, test, prohibited."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=78.0)
        statuses = [r.status for r in results]
        # All recommended should come before test_with_caution
        rec_indices = [i for i, s in enumerate(statuses) if s == "recommended"]
        test_indices = [i for i, s in enumerate(statuses) if s == "test_with_caution"]
        prohib_indices = [i for i, s in enumerate(statuses) if s == "prohibited"]
        if rec_indices and test_indices:
            assert max(rec_indices) < min(test_indices)
        if test_indices and prohib_indices:
            assert max(test_indices) < min(prohib_indices)
        if rec_indices and prohib_indices:
            assert max(rec_indices) < min(prohib_indices)


class TestEdgeCases:
    """Test edge cases."""

    def test_low_body_weight(self, manish_chart: ChartData) -> None:
        """Low body weight should still produce valid results."""
        results = compute_gemstone_weights(manish_chart, body_weight_kg=40.0)
        panna = next(r for r in results if r.planet == "Mercury")
        assert panna.recommended_ratti >= 1.0

    def test_high_body_weight(self, manish_chart: ChartData) -> None:
        """High body weight should produce proportionally larger weight."""
        r_low = compute_gemstone_weights(manish_chart, body_weight_kg=50.0)
        r_high = compute_gemstone_weights(manish_chart, body_weight_kg=100.0)
        p_low = next(r for r in r_low if r.planet == "Mercury")
        p_high = next(r for r in r_high if r.planet == "Mercury")
        assert p_high.recommended_ratti > p_low.recommended_ratti

    def test_multiplier_constants_valid(self) -> None:
        """All multiplier constants should be positive and <= 1.5."""
        for val in AVASTHA_MULT.values():
            assert 0 < val <= 1.5
        for val in DIGNITY_MULT.values():
            assert 0 < val <= 1.5
        for val in PURPOSE_MULT.values():
            assert 0 < val <= 1.5

    def test_weight_factor_model_immutable(self) -> None:
        """WeightFactor should be frozen."""
        f = WeightFactor(name="test", raw_value="x", multiplier=1.0, explanation="y")
        with pytest.raises(ValidationError):
            f.name = "changed"  # type: ignore[misc]
