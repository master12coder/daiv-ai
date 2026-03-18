"""Tests for the PDF assembler — 3 format modes."""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from jyotish_engine.compute.chart import compute_chart
from jyotish_engine.models.chart import ChartData
from jyotish_products.plugins.kundali.pdf import generate_pdf


@pytest.fixture
def manish_chart() -> ChartData:
    return compute_chart(
        name="Manish Chaurasia", dob="13/03/1989", tob="12:17",
        lat=25.3176, lon=83.0067, tz_name="Asia/Kolkata", gender="Male",
    )


class TestPdfSummaryFormat:
    def test_summary_returns_bytes(self, manish_chart: ChartData) -> None:
        result = generate_pdf(manish_chart, fmt="summary")
        assert result is not None
        assert result[:5] == b"%PDF-"
        assert len(result) > 5000

    def test_summary_saves_to_file(self, manish_chart: ChartData) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "summary.pdf"
            generate_pdf(manish_chart, output_path=str(path), fmt="summary")
            assert path.exists()
            assert path.stat().st_size > 5000


class TestPdfDetailedFormat:
    def test_detailed_returns_bytes(self, manish_chart: ChartData) -> None:
        result = generate_pdf(manish_chart, fmt="detailed")
        assert result is not None
        assert result[:5] == b"%PDF-"

    def test_detailed_larger_than_summary(self, manish_chart: ChartData) -> None:
        summary = generate_pdf(manish_chart, fmt="summary")
        detailed = generate_pdf(manish_chart, fmt="detailed")
        assert summary is not None and detailed is not None
        assert len(detailed) > len(summary)

    def test_detailed_with_gemstones(self, manish_chart: ChartData) -> None:
        result = generate_pdf(manish_chart, fmt="detailed", body_weight_kg=78.0)
        assert result is not None
        assert len(result) > 10000


class TestPdfPanditFormat:
    def test_pandit_returns_bytes(self, manish_chart: ChartData) -> None:
        result = generate_pdf(manish_chart, fmt="pandit")
        assert result is not None
        assert result[:5] == b"%PDF-"

    def test_pandit_largest_format(self, manish_chart: ChartData) -> None:
        """Pandit format should be the largest (most charts)."""
        detailed = generate_pdf(manish_chart, fmt="detailed")
        pandit = generate_pdf(manish_chart, fmt="pandit")
        assert detailed is not None and pandit is not None
        assert len(pandit) >= len(detailed)


class TestPdfEndToEnd:
    def test_full_kundali_with_all_features(self, manish_chart: ChartData) -> None:
        """Full end-to-end test with gemstones and all sections."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "kundali_manish.pdf"
            generate_pdf(
                manish_chart,
                output_path=str(path),
                fmt="detailed",
                body_weight_kg=78.0,
            )
            assert path.exists()
            pdf_bytes = path.read_bytes()
            assert pdf_bytes[:5] == b"%PDF-"
            assert len(pdf_bytes) > 20000  # Full report should be substantial

    def test_different_chart(self) -> None:
        """Should work with non-Mithuna charts."""
        chart = compute_chart(
            name="Test Person", dob="01/01/2000", tob="06:00",
            lat=28.6139, lon=77.2090, tz_name="Asia/Kolkata", gender="Female",
        )
        result = generate_pdf(chart, fmt="summary")
        assert result is not None
        assert result[:5] == b"%PDF-"
