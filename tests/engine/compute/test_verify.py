"""Tests for triple-layer chart accuracy verification."""

from __future__ import annotations

from daivai_engine.compute.verify import triple_verify, verify_chart_accuracy
from daivai_engine.models.chart import ChartData


class TestTripleVerification:
    def test_manish_chart_passes_all_layers(self, manish_chart: ChartData) -> None:
        report = triple_verify(manish_chart)
        assert report.is_clean, f"Issues: {report.all_warnings}"

    def test_layer1_mathematical(self, manish_chart: ChartData) -> None:
        report = triple_verify(manish_chart)
        assert len(report.mathematical) == 0

    def test_layer2_astronomical(self, manish_chart: ChartData) -> None:
        report = triple_verify(manish_chart)
        assert len(report.astronomical) == 0

    def test_layer3_jyotish(self, manish_chart: ChartData) -> None:
        report = triple_verify(manish_chart)
        # L3 may contain AYANAMSHA SENSITIVE alerts (informational, not errors)
        errors = [w for w in report.jyotish if "SENSITIVE" not in w]
        assert len(errors) == 0

    def test_backward_compat(self, manish_chart: ChartData) -> None:
        """verify_chart_accuracy() still returns flat list."""
        warnings = verify_chart_accuracy(manish_chart)
        assert isinstance(warnings, list)

    def test_sample_chart_passes(self, sample_chart: ChartData) -> None:
        report = triple_verify(sample_chart)
        l1_errors = [w for w in report.mathematical if "ERROR" in w]
        assert len(l1_errors) == 0

    def test_mercury_within_28_of_sun(self, manish_chart: ChartData) -> None:
        """Layer 2 checks Mercury-Sun distance."""
        report = triple_verify(manish_chart)
        merc_warnings = [w for w in report.astronomical if "Mercury" in w and "28" in w]
        assert len(merc_warnings) == 0

    def test_venus_within_47_of_sun(self, manish_chart: ChartData) -> None:
        report = triple_verify(manish_chart)
        venus_warnings = [w for w in report.astronomical if "Venus" in w and "47" in w]
        assert len(venus_warnings) == 0
