"""Test chart computation against known verified values."""

from jyotish_engine.compute.chart import compute_chart, get_house_lord


class TestManishChart:
    """Test against Manish Chaurasia's verified chart."""

    def test_lagna_is_mithuna(self, manish_chart):
        assert manish_chart.lagna_sign == "Mithuna"
        assert manish_chart.lagna_sign_en == "Gemini"

    def test_moon_in_vrishabha(self, manish_chart):
        moon = manish_chart.planets["Moon"]
        assert moon.sign == "Vrishabha"
        assert moon.sign_en == "Taurus"

    def test_moon_rohini_nakshatra(self, manish_chart):
        moon = manish_chart.planets["Moon"]
        assert moon.nakshatra == "Rohini"

    def test_moon_pada_2(self, manish_chart):
        moon = manish_chart.planets["Moon"]
        assert moon.pada == 2

    def test_all_planets_present(self, manish_chart):
        expected = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        assert list(manish_chart.planets.keys()) == expected

    def test_planet_signs_valid(self, manish_chart):
        from jyotish_engine.constants import SIGNS

        for p in manish_chart.planets.values():
            assert p.sign in SIGNS
            assert 0 <= p.sign_index <= 11

    def test_planet_houses_valid(self, manish_chart):
        for p in manish_chart.planets.values():
            assert 1 <= p.house <= 12

    def test_planet_degrees_valid(self, manish_chart):
        for p in manish_chart.planets.values():
            assert 0 <= p.degree_in_sign < 30.0

    def test_planet_nakshatras_valid(self, manish_chart):
        from jyotish_engine.constants import NAKSHATRAS

        for p in manish_chart.planets.values():
            assert p.nakshatra in NAKSHATRAS
            assert 1 <= p.pada <= 4

    def test_rahu_ketu_opposite(self, manish_chart):
        rahu = manish_chart.planets["Rahu"]
        ketu = manish_chart.planets["Ketu"]
        diff = abs(rahu.longitude - ketu.longitude)
        assert abs(diff - 180.0) < 1.0  # Within 1 degree of exact opposition

    def test_rahu_ketu_retrograde(self, manish_chart):
        assert manish_chart.planets["Rahu"].is_retrograde
        assert manish_chart.planets["Ketu"].is_retrograde

    def test_whole_sign_houses(self, manish_chart):
        """Verify whole sign house system: lagna sign = 1st house."""
        lagna_sign = manish_chart.lagna_sign_index
        for p in manish_chart.planets.values():
            expected_house = ((p.sign_index - lagna_sign) % 12) + 1
            assert p.house == expected_house

    def test_house_lord(self, manish_chart):
        # Mithuna lagna: 1st lord = Mercury
        assert get_house_lord(manish_chart, 1) == "Mercury"

    def test_ayanamsha_positive(self, manish_chart):
        assert manish_chart.ayanamsha > 23.0  # Lahiri ~ 23-24 degrees

    def test_moon_dignity_exalted(self, manish_chart):
        """Moon in Taurus should be exalted."""
        moon = manish_chart.planets["Moon"]
        assert moon.dignity == "exalted"


class TestChartWithPlace:
    """Test chart computation using place name geocoding."""

    def test_varanasi_chart(self):
        chart = compute_chart(
            name="Test", dob="13/03/1989", tob="12:17", place="Varanasi", gender="Male"
        )
        assert chart.lagna_sign == "Mithuna"
        assert chart.latitude > 25.0
        assert chart.longitude > 82.0
