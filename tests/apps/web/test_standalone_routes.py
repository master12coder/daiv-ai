"""Tests for standalone routes — match and muhurta pages.

These routes are standalone (no saved client needed) but still require auth.
Uses BYPASS_AUTH=true to skip Google OAuth for testing.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from jyotish_app.web.database import get_engine, reset_engine


@pytest.fixture(autouse=True)
def _setup(tmp_path, monkeypatch):
    """Fresh DB + auth bypass for every test."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/standalone.db")
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("BYPASS_AUTH", "true")
    reset_engine()
    get_engine()
    yield
    reset_engine()


@pytest.fixture
def client():
    """TestClient with auth bypass."""
    from jyotish_app.web.app import create_app

    return TestClient(create_app())


class TestMatchFormPage:
    """GET /match — compatibility form."""

    def test_match_form_renders(self, client: TestClient) -> None:
        """GET /match must render the two-person form."""
        resp = client.get("/match")
        assert resp.status_code == 200
        assert "अष्टकूट" in resp.text
        assert "गुण मिलान" in resp.text

    def test_match_form_has_two_person_sections(self, client: TestClient) -> None:
        """Form must have fields for both persons."""
        resp = client.get("/match")
        assert "name1" in resp.text
        assert "name2" in resp.text
        assert "dob1" in resp.text
        assert "dob2" in resp.text

    def test_match_form_has_default_person1_values(self, client: TestClient) -> None:
        """Person 1 should have Manish's default data."""
        resp = client.get("/match")
        assert "Manish Chaurasia" in resp.text
        assert "13/03/1989" in resp.text
        assert "12:17" in resp.text

    def test_match_form_has_sacred_header(self, client: TestClient) -> None:
        """Match page must have the sacred header from base template."""
        resp = client.get("/match")
        assert "गणेशाय" in resp.text

    def test_match_form_requires_auth(self, client: TestClient, monkeypatch) -> None:
        """GET /match must redirect if not authenticated."""
        monkeypatch.setenv("BYPASS_AUTH", "false")
        # Need a fresh app since BYPASS_AUTH was already read
        from jyotish_app.web.app import create_app

        reset_engine()
        get_engine()
        unauth_client = TestClient(create_app())
        resp = unauth_client.get("/match", follow_redirects=False)
        assert resp.status_code == 302


class TestMatchResult:
    """POST /match/result — compatibility computation."""

    _FORM_DATA = {
        "name1": "Manish Chaurasia",
        "dob1": "13/03/1989",
        "tob1": "12:17",
        "lat1": "25.3176",
        "lon1": "83.0067",
        "gender1": "Male",
        "name2": "Test Person",
        "dob2": "15/06/1992",
        "tob2": "08:30",
        "lat2": "28.6139",
        "lon2": "77.2090",
        "gender2": "Female",
    }

    def test_match_result_renders(self, client: TestClient) -> None:
        """POST /match/result must return 200 with result page."""
        resp = client.post("/match/result", data=self._FORM_DATA)
        assert resp.status_code == 200

    def test_match_result_shows_names(self, client: TestClient) -> None:
        """Result page must show both person names."""
        resp = client.post("/match/result", data=self._FORM_DATA)
        assert "Manish Chaurasia" in resp.text
        assert "Test Person" in resp.text

    def test_match_result_shows_score(self, client: TestClient) -> None:
        """Result page must show total score out of 36."""
        resp = client.post("/match/result", data=self._FORM_DATA)
        assert "/36" in resp.text

    def test_match_result_shows_koota_details(self, client: TestClient) -> None:
        """Result page must show all 8 kootas with Hindi names."""
        resp = client.post("/match/result", data=self._FORM_DATA)
        koota_hindi = ["वर्ण", "वश्य", "तारा", "योनि", "ग्रह मैत्री", "गण", "भकूट", "नाड़ी"]
        for name in koota_hindi:
            assert name in resp.text, f"Missing koota: {name}"

    def test_match_result_has_hindi_verdict(self, client: TestClient) -> None:
        """Result page must show Hindi verdict text."""
        resp = client.post("/match/result", data=self._FORM_DATA)
        text = resp.text
        # One of the verdict texts must be present
        verdicts = ["उत्तम मिलान", "अच्छा मिलान", "सामान्य मिलान", "मिलान कमजोर"]
        assert any(v in text for v in verdicts), "No Hindi verdict found"

    def test_match_result_shows_percentage(self, client: TestClient) -> None:
        """Result page must show match percentage."""
        resp = client.post("/match/result", data=self._FORM_DATA)
        assert "%" in resp.text


class TestMuhurtaFormPage:
    """GET /muhurta — muhurta search form."""

    def test_muhurta_form_renders(self, client: TestClient) -> None:
        """GET /muhurta must render the muhurta form."""
        resp = client.get("/muhurta")
        assert resp.status_code == 200
        assert "मुहूर्त" in resp.text

    def test_muhurta_form_has_purpose_dropdown(self, client: TestClient) -> None:
        """Form must have purpose options in Hindi."""
        resp = client.get("/muhurta")
        assert "विवाह" in resp.text
        assert "गृह प्रवेश" in resp.text
        assert "व्यापार" in resp.text
        assert "यात्रा" in resp.text

    def test_muhurta_form_has_date_fields(self, client: TestClient) -> None:
        """Form must have from_date and to_date fields."""
        resp = client.get("/muhurta")
        assert "from_date" in resp.text
        assert "to_date" in resp.text

    def test_muhurta_form_has_location_fields(self, client: TestClient) -> None:
        """Form must have lat/lon inputs."""
        resp = client.get("/muhurta")
        assert 'name="lat"' in resp.text
        assert 'name="lon"' in resp.text

    def test_muhurta_form_requires_auth(self, client: TestClient, monkeypatch) -> None:
        """GET /muhurta must redirect if not authenticated."""
        monkeypatch.setenv("BYPASS_AUTH", "false")
        from jyotish_app.web.app import create_app

        reset_engine()
        get_engine()
        unauth_client = TestClient(create_app())
        resp = unauth_client.get("/muhurta", follow_redirects=False)
        assert resp.status_code == 302


class TestMuhurtaResult:
    """POST /muhurta/result — muhurta computation."""

    _FORM_DATA = {
        "purpose": "marriage",
        "from_date": "01/04/2026",
        "to_date": "15/04/2026",
        "lat": "25.3176",
        "lon": "83.0067",
    }

    def test_muhurta_result_renders(self, client: TestClient) -> None:
        """POST /muhurta/result must return 200."""
        resp = client.post("/muhurta/result", data=self._FORM_DATA)
        assert resp.status_code == 200

    def test_muhurta_result_shows_purpose_hindi(self, client: TestClient) -> None:
        """Result page must show Hindi purpose label."""
        resp = client.post("/muhurta/result", data=self._FORM_DATA)
        assert "विवाह" in resp.text

    def test_muhurta_result_has_date_cards(self, client: TestClient) -> None:
        """Result page must show date cards with nakshatra and tithi."""
        resp = client.post("/muhurta/result", data=self._FORM_DATA)
        text = resp.text
        # Should have either result cards or the "no results" message
        has_results = "Score:" in text
        has_no_results = "कोई शुभ मुहूर्त नहीं" in text
        assert has_results or has_no_results

    def test_muhurta_result_best_date_highlighted(self, client: TestClient) -> None:
        """If results found, the best date card should have gold border."""
        resp = client.post("/muhurta/result", data=self._FORM_DATA)
        if "Score:" in resp.text:
            assert "सर्वोत्तम" in resp.text

    def test_muhurta_business_purpose(self, client: TestClient) -> None:
        """Muhurta should work for business purpose too."""
        data = {**self._FORM_DATA, "purpose": "business"}
        resp = client.post("/muhurta/result", data=data)
        assert resp.status_code == 200
        assert "व्यापार" in resp.text

    def test_muhurta_travel_purpose(self, client: TestClient) -> None:
        """Muhurta should work for travel purpose."""
        data = {**self._FORM_DATA, "purpose": "travel"}
        resp = client.post("/muhurta/result", data=data)
        assert resp.status_code == 200
        assert "यात्रा" in resp.text
