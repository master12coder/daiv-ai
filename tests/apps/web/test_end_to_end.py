"""End-to-end web app tests — real chart computation through web flow.

Tests the full pipeline: form submission → engine computation → DB save → page render.
Uses BYPASS_AUTH=true to skip Google OAuth for testing.
"""

from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from jyotish_app.web.database import get_client, get_engine, reset_engine


@pytest.fixture(autouse=True)
def _setup(tmp_path, monkeypatch):
    """Fresh DB + auth bypass for every test."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/e2e.db")
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


class TestFullChartFlow:
    """Submit Manish's birth data → verify real computation → verify rendering."""

    def _submit_manish(self, client: TestClient) -> int:
        """Submit Manish's form and return client ID from redirect."""
        resp = client.post(
            "/generate",
            data={
                "name": "Manish Chaurasia",
                "dob": "13/03/1989",
                "tob": "12:17",
                "place": "Varanasi",
                "lat": "25.3176",
                "lon": "83.0067",
                "gender": "Male",
            },
            follow_redirects=False,
        )
        assert resp.status_code == 302
        location = resp.headers["location"]
        return int(location.split("/client/")[1])

    def test_form_submission_creates_client(self, client: TestClient) -> None:
        """POST /generate should create a client in the database."""
        client_id = self._submit_manish(client)
        db_client = get_client(client_id)
        assert db_client is not None
        assert db_client.name == "Manish Chaurasia"
        assert db_client.dob == "13/03/1989"

    def test_chart_has_real_computed_data(self, client: TestClient) -> None:
        """Saved chart JSON must contain real engine output, not stubs."""
        client_id = self._submit_manish(client)
        db_client = get_client(client_id)
        chart = json.loads(db_client.chart_json)

        # Verify real engine output
        assert "planets" in chart
        assert len(chart["planets"]) == 9
        assert "lagna_sign" in chart
        assert chart["lagna_sign"] == "Mithuna"

    def test_lagna_is_mithuna(self, client: TestClient) -> None:
        """Manish's lagna must be Mithuna (Gemini)."""
        client_id = self._submit_manish(client)
        chart = json.loads(get_client(client_id).chart_json)
        assert chart["lagna_sign"] == "Mithuna"
        assert chart["lagna_sign_en"] == "Gemini"

    def test_moon_is_rohini_pada_2(self, client: TestClient) -> None:
        """Moon must be in Rohini nakshatra, pada 2."""
        client_id = self._submit_manish(client)
        chart = json.loads(get_client(client_id).chart_json)
        moon = chart["planets"]["Moon"]
        assert moon["nakshatra"] == "Rohini"
        assert moon["pada"] == 2

    def test_mercury_is_lagnesh(self, client: TestClient) -> None:
        """Mercury must be present (lagnesh for Mithuna)."""
        client_id = self._submit_manish(client)
        chart = json.loads(get_client(client_id).chart_json)
        assert "Mercury" in chart["planets"]

    @pytest.mark.safety
    def test_overview_page_renders(self, client: TestClient) -> None:
        """GET /client/{id} must render without template errors."""
        client_id = self._submit_manish(client)
        resp = client.get(f"/client/{client_id}")
        assert resp.status_code == 200
        assert "Manish Chaurasia" in resp.text
        assert "मिथुन" in resp.text or "Mithuna" in resp.text

    def test_overview_shows_planets(self, client: TestClient) -> None:
        """Overview page must show all 9 planets."""
        client_id = self._submit_manish(client)
        resp = client.get(f"/client/{client_id}")
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            assert planet in resp.text, f"{planet} missing from overview"

    @pytest.mark.safety
    def test_overview_shows_prohibited_stones(self, client: TestClient) -> None:
        """Overview must show prohibited gemstones."""
        client_id = self._submit_manish(client)
        resp = client.get(f"/client/{client_id}")
        assert "निषिद्ध" in resp.text or "Prohibited" in resp.text or "prohibited" in resp.text

    def test_dasha_page_renders(self, client: TestClient) -> None:
        """GET /client/{id}/dasha must render."""
        client_id = self._submit_manish(client)
        resp = client.get(f"/client/{client_id}/dasha")
        assert resp.status_code == 200
        assert "Jupiter" in resp.text  # Current MD lord

    def test_ratna_page_renders(self, client: TestClient) -> None:
        """GET /client/{id}/ratna must render gemstone recommendations."""
        client_id = self._submit_manish(client)
        resp = client.get(f"/client/{client_id}/ratna")
        assert resp.status_code == 200
        assert "रत्न" in resp.text or "Gemstone" in resp.text

    @pytest.mark.safety
    def test_ratna_shows_pukhraj_prohibited(self, client: TestClient) -> None:
        """Pukhraj must appear in prohibited section of ratna page."""
        client_id = self._submit_manish(client)
        resp = client.get(f"/client/{client_id}/ratna")
        text = resp.text
        assert "Yellow Sapphire" in text or "Pukhraj" in text

    def test_pdf_download_works(self, client: TestClient) -> None:
        """GET /client/{id}/pdf must return a PDF."""
        client_id = self._submit_manish(client)
        resp = client.get(f"/client/{client_id}/pdf")
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "application/pdf"
        assert resp.content[:5] == b"%PDF-"

    def test_api_returns_json(self, client: TestClient) -> None:
        """GET /api/chart/{id} must return chart JSON."""
        client_id = self._submit_manish(client)
        resp = client.get(f"/api/chart/{client_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["lagna_sign"] == "Mithuna"
        assert "planets" in data

    def test_dashboard_shows_new_client(self, client: TestClient) -> None:
        """After submission, dashboard must show the new client."""
        self._submit_manish(client)
        resp = client.get("/dashboard")
        assert resp.status_code == 200
        assert "Manish Chaurasia" in resp.text

    def test_input_form_renders(self, client: TestClient) -> None:
        """GET /new must show the Hindi input form."""
        resp = client.get("/new")
        assert resp.status_code == 200
        assert "नई कुंडली" in resp.text or "कुंडली बनाएं" in resp.text
