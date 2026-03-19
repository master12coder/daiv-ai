"""Test panchang computation."""

from jyotish_engine.compute.panchang import compute_panchang


class TestPanchang:
    def test_panchang_returns_data(self):
        result = compute_panchang(
            date_str="13/03/1989",
            lat=25.3176,
            lon=83.0067,
            tz_name="Asia/Kolkata",
            place="Varanasi",
        )
        assert result.date == "13/03/1989"
        assert result.place == "Varanasi"

    def test_vara_valid(self):
        result = compute_panchang("13/03/1989", 25.3176, 83.0067)
        valid_days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        assert result.vara in valid_days

    def test_tithi_valid(self):
        result = compute_panchang("13/03/1989", 25.3176, 83.0067)
        assert 0 <= result.tithi_index <= 29
        assert len(result.tithi_name) > 0

    def test_paksha_valid(self):
        result = compute_panchang("13/03/1989", 25.3176, 83.0067)
        assert result.paksha in ("Shukla", "Krishna")

    def test_nakshatra_valid(self):
        from jyotish_engine.constants import NAKSHATRAS

        result = compute_panchang("13/03/1989", 25.3176, 83.0067)
        assert result.nakshatra_name in NAKSHATRAS

    def test_yoga_valid(self):
        from jyotish_engine.constants import PANCHANG_YOGA_NAMES

        result = compute_panchang("13/03/1989", 25.3176, 83.0067)
        assert result.yoga_name in PANCHANG_YOGA_NAMES

    def test_sunrise_sunset_format(self):
        result = compute_panchang("15/03/2026", 25.3176, 83.0067, place="Varanasi")
        # Should be HH:MM format or N/A
        if result.sunrise != "N/A":
            assert ":" in result.sunrise
            assert ":" in result.sunset

    def test_rahu_kaal_present(self):
        result = compute_panchang("15/03/2026", 25.3176, 83.0067)
        assert result.rahu_kaal != ""
