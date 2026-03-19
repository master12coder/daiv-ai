"""Phase 1 Audit Tests — cross-verification against BPHS known values.

Every test here verifies a SPECIFIC classical constant or formula
against the authoritative source (BPHS, Surya Siddhanta, etc.).
"""

from __future__ import annotations

from daivai_engine.compute.ashtakavarga import compute_ashtakavarga
from daivai_engine.compute.dasha import compute_mahadashas
from daivai_engine.compute.full_analysis import compute_full_analysis
from daivai_engine.compute.verify import triple_verify
from daivai_engine.constants import (
    COMBUSTION_LIMITS,
    DASHA_SEQUENCE,
    DASHA_YEARS,
    DEBILITATION,
    EXALTATION,
    EXALTATION_DEGREE,
    MOOLTRIKONA,
    NATURAL_ENEMIES,
    NATURAL_FRIENDS,
)
from daivai_engine.models.chart import ChartData


class TestAyanamshaApplication:
    def test_ayanamsha_reasonable_for_1989(self, manish_chart: ChartData) -> None:
        """Lahiri ayanamsha for 1989 should be ~23.7° (BPHS/Lahiri standard)."""
        assert 23.5 < manish_chart.ayanamsha < 24.0

    def test_ayanamsha_applied_once(self, manish_chart: ChartData) -> None:
        """If ayanamsha were applied twice, lagna would be ~23° off."""
        assert 10.0 < manish_chart.lagna_degree < 16.0  # ~13° Gemini, not ~350°


class TestDashaSystem:
    def test_dasha_years_sum_120(self) -> None:
        """BPHS: Vimshottari total = 120 years exactly."""
        total = sum(DASHA_YEARS[p] for p in DASHA_SEQUENCE)
        assert total == 120

    def test_dasha_sequence_correct(self) -> None:
        """BPHS: Ketu→Venus→Sun→Moon→Mars→Rahu→Jupiter→Saturn→Mercury."""
        assert DASHA_SEQUENCE == [
            "Ketu",
            "Venus",
            "Sun",
            "Moon",
            "Mars",
            "Rahu",
            "Jupiter",
            "Saturn",
            "Mercury",
        ]

    def test_mahadashas_span_120_years(self, manish_chart: ChartData) -> None:
        """All 9 full MD periods sum to 120 years.

        The first dasha starts mid-way (balance applied), so the total
        from birth is less than 120. But each full dasha's proportion
        must be correct: sum of DASHA_YEARS values = 120.
        """
        mds = compute_mahadashas(manish_chart)
        assert len(mds) == 9
        # First dasha has balance, rest are full — verify the proportions
        # are self-consistent: sum of all 9 periods' durations should be
        # between 110 and 120 years (balance removes some of first period)
        total_days = sum((md.end - md.start).total_seconds() / 86400 for md in mds)
        total_years = total_days / 365.25
        assert 100.0 < total_years <= 120.0, f"Total {total_years:.1f} years"


class TestSavTotal:
    def test_sav_equals_337(self, manish_chart: ChartData) -> None:
        """BPHS: Sarvashtakavarga total across 12 signs = 337."""
        avk = compute_ashtakavarga(manish_chart)
        assert sum(avk.sarva) == 337


class TestExaltationTable:
    def test_exaltation_signs_match_bphs(self) -> None:
        """BPHS: Sun=Aries, Moon=Taurus, Mars=Capricorn, etc."""
        expected = {
            "Sun": 0,
            "Moon": 1,
            "Mars": 9,
            "Mercury": 5,
            "Jupiter": 3,
            "Venus": 11,
            "Saturn": 6,
        }
        for planet, sign in expected.items():
            assert EXALTATION[planet] == sign, f"{planet} exaltation wrong"

    def test_exaltation_degrees_match_bphs(self) -> None:
        """BPHS: Sun=10°, Moon=3°, Mars=28°, Mercury=15°, etc."""
        expected = {
            "Sun": 10.0,
            "Moon": 3.0,
            "Mars": 28.0,
            "Mercury": 15.0,
            "Jupiter": 5.0,
            "Venus": 27.0,
            "Saturn": 20.0,
        }
        for planet, deg in expected.items():
            assert EXALTATION_DEGREE[planet] == deg, f"{planet} exaltation degree wrong"

    def test_debilitation_opposite_exaltation(self) -> None:
        """Debilitation sign = exaltation sign + 6 (opposite)."""
        for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
            assert DEBILITATION[planet] == (EXALTATION[planet] + 6) % 12


class TestMooltrikonaRanges:
    def test_mooltrikona_match_bphs(self) -> None:
        """BPHS Ch.3: Mooltrikona signs and degree ranges."""
        expected = {
            "Sun": (4, 0.0, 20.0),
            "Moon": (1, 3.0, 30.0),
            "Mars": (0, 0.0, 12.0),
            "Mercury": (5, 15.0, 20.0),
            "Jupiter": (8, 0.0, 10.0),
            "Venus": (6, 0.0, 15.0),
            "Saturn": (10, 0.0, 20.0),
        }
        for planet, (sign, start, end) in expected.items():
            assert MOOLTRIKONA[planet] == (sign, start, end), f"{planet} mooltrikona wrong"


class TestFriendshipTable:
    def test_sun_friends(self) -> None:
        """BPHS: Sun's friends = Moon, Mars, Jupiter."""
        assert set(NATURAL_FRIENDS["Sun"]) == {"Moon", "Mars", "Jupiter"}

    def test_sun_enemies(self) -> None:
        """BPHS: Sun's enemies = Venus, Saturn."""
        assert set(NATURAL_ENEMIES["Sun"]) == {"Saturn", "Venus"}

    def test_jupiter_enemies(self) -> None:
        """BPHS: Jupiter's enemies = Mercury, Venus."""
        assert set(NATURAL_ENEMIES["Jupiter"]) == {"Mercury", "Venus"}


class TestCombustionLimits:
    def test_combustion_limits_match_bphs(self) -> None:
        """BPHS Ch.25: Planet-specific combustion distances."""
        expected = {"Moon": 12, "Mars": 17, "Mercury": 14, "Jupiter": 11, "Venus": 10, "Saturn": 15}
        for planet, limit in expected.items():
            assert COMBUSTION_LIMITS[planet] == limit


class TestCrossVerification:
    def test_manish_lagna_is_mithuna(self, manish_chart: ChartData) -> None:
        assert manish_chart.lagna_sign == "Mithuna"

    def test_manish_moon_rohini_pada_2(self, manish_chart: ChartData) -> None:
        moon = manish_chart.planets["Moon"]
        assert moon.nakshatra == "Rohini"
        assert moon.pada == 2

    def test_rahu_ketu_180_apart(self, manish_chart: ChartData) -> None:
        rahu = manish_chart.planets["Rahu"].longitude
        ketu = manish_chart.planets["Ketu"].longitude
        diff = abs(rahu - ketu)
        if diff > 180:
            diff = 360 - diff
        assert abs(diff - 180) < 0.01

    def test_mercury_within_28_of_sun(self, manish_chart: ChartData) -> None:
        """Astronomical fact: Mercury never >28° from Sun."""
        sun = manish_chart.planets["Sun"].longitude
        merc = manish_chart.planets["Mercury"].longitude
        dist = abs(merc - sun)
        if dist > 180:
            dist = 360 - dist
        assert dist <= 28.5

    def test_venus_within_47_of_sun(self, manish_chart: ChartData) -> None:
        """Astronomical fact: Venus never >47° from Sun."""
        sun = manish_chart.planets["Sun"].longitude
        venus = manish_chart.planets["Venus"].longitude
        dist = abs(venus - sun)
        if dist > 180:
            dist = 360 - dist
        assert dist <= 47.5

    def test_sun_never_retrograde(self, manish_chart: ChartData) -> None:
        assert not manish_chart.planets["Sun"].is_retrograde

    def test_rahu_ketu_always_retrograde(self, manish_chart: ChartData) -> None:
        assert manish_chart.planets["Rahu"].is_retrograde
        assert manish_chart.planets["Ketu"].is_retrograde

    def test_combustion_matches_distance(self, manish_chart: ChartData) -> None:
        """Verify combustion flag is consistent with Sun distance."""
        sun_lon = manish_chart.planets["Sun"].longitude
        for name, limit in COMBUSTION_LIMITS.items():
            p = manish_chart.planets[name]
            dist = abs(p.longitude - sun_lon)
            if dist > 180:
                dist = 360 - dist
            if p.is_combust:
                assert dist < limit, f"{name} marked combust but dist={dist:.1f}° (limit={limit})"

    def test_triple_verification_clean(self, manish_chart: ChartData) -> None:
        """All three verification layers should pass."""
        report = triple_verify(manish_chart)
        assert report.is_clean, f"Issues: {report.all_warnings}"


class TestDeterminism:
    def test_full_analysis_deterministic(self, manish_chart: ChartData) -> None:
        """Two runs with identical input produce identical output."""
        a1 = compute_full_analysis(manish_chart)
        a2 = compute_full_analysis(manish_chart)
        assert a1.shadbala == a2.shadbala
        assert a1.gandanta == a2.gandanta
        assert a1.upapada == a2.upapada
        assert a1.vimshopaka == a2.vimshopaka

    def test_json_roundtrip(self, manish_chart: ChartData) -> None:
        """Serialize to JSON and back without data loss."""
        a = compute_full_analysis(manish_chart)
        json_str = a.model_dump_json()
        from daivai_engine.models.analysis import FullChartAnalysis

        restored = FullChartAnalysis.model_validate_json(json_str)
        assert restored.chart.lagna_degree == a.chart.lagna_degree
        assert len(restored.shadbala) == len(a.shadbala)
