"""Test Ashtakoot (36 guna) matching."""

from jyotish_engine.compute.matching import compute_ashtakoot


class TestAshtakootMatching:
    def test_matching_returns_score_out_of_36(self):
        result = compute_ashtakoot(
            person1_nakshatra_index=3,  # Rohini
            person1_moon_sign=1,  # Taurus
            person2_nakshatra_index=12,  # Hasta
            person2_moon_sign=5,  # Virgo
        )
        assert result.total_max == 36.0
        assert 0 <= result.total_obtained <= 36.0

    def test_same_nakshatra_nadi_zero(self):
        """Same nakshatra should give 0 points for Nadi."""
        result = compute_ashtakoot(
            person1_nakshatra_index=3,  # Rohini
            person1_moon_sign=1,  # Taurus
            person2_nakshatra_index=3,  # Rohini (same)
            person2_moon_sign=1,  # Taurus
        )
        nadi = next(k for k in result.kootas if k.name == "Nadi")
        assert nadi.obtained == 0.0

    def test_different_nadi_full_points(self):
        """Different nadi nakshatras should give 8 points."""
        # Ashwini (Aadi) vs Rohini (Madhya)
        result = compute_ashtakoot(
            person1_nakshatra_index=0,  # Ashwini (Aadi)
            person1_moon_sign=0,  # Aries
            person2_nakshatra_index=3,  # Rohini (Madhya)
            person2_moon_sign=1,  # Taurus
        )
        nadi = next(k for k in result.kootas if k.name == "Nadi")
        assert nadi.obtained == 8.0

    def test_eight_kootas_present(self):
        result = compute_ashtakoot(0, 0, 3, 1)
        assert len(result.kootas) == 8

    def test_koota_names(self):
        result = compute_ashtakoot(0, 0, 3, 1)
        names = [k.name for k in result.kootas]
        expected = ["Varna", "Vasya", "Tara", "Yoni", "Graha Maitri", "Gana", "Bhakoot", "Nadi"]
        assert names == expected

    def test_percentage_in_range(self):
        result = compute_ashtakoot(0, 0, 3, 1)
        assert 0 <= result.percentage <= 100

    def test_recommendation_not_empty(self):
        result = compute_ashtakoot(0, 0, 3, 1)
        assert len(result.recommendation) > 0

    def test_same_sign_yoni_full_points(self):
        """Same animal should give full yoni points."""
        # Both Ashwini (Horse) -> same animal
        result = compute_ashtakoot(
            person1_nakshatra_index=0,  # Ashwini (Horse)
            person1_moon_sign=0,
            person2_nakshatra_index=23,  # Shatabhisha (Horse)
            person2_moon_sign=10,
        )
        yoni = next(k for k in result.kootas if k.name == "Yoni")
        assert yoni.obtained == 4.0

    def test_enemy_yoni_zero_points(self):
        """Enemy animals should give 0 yoni points."""
        # Horse (Ashwini=0) vs Buffalo (Hasta=12)
        result = compute_ashtakoot(
            person1_nakshatra_index=0,  # Ashwini (Horse)
            person1_moon_sign=0,
            person2_nakshatra_index=12,  # Hasta (Buffalo)
            person2_moon_sign=5,
        )
        yoni = next(k for k in result.kootas if k.name == "Yoni")
        assert yoni.obtained == 0.0
