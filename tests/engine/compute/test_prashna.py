"""Tests for Prashna (horary chart) computation."""

from __future__ import annotations

from datetime import UTC, datetime

from daivai_engine.compute.prashna import compute_prashna


class TestPrashna:
    def test_prashna_chart_computes(self) -> None:
        result = compute_prashna(
            question="Will I get promoted?",
            lat=25.3176,
            lon=83.0067,
            question_type="career",
        )
        assert result["chart"] is not None
        assert result["answer"] in ("YES", "NO", "MAYBE")

    def test_answer_has_reasoning(self) -> None:
        result = compute_prashna(
            question="Is this a good time to marry?",
            lat=28.6139,
            lon=77.2090,
            question_type="marriage",
        )
        assert len(result["reasoning"]) > 20

    def test_relevant_house_for_career(self) -> None:
        result = compute_prashna(
            question="Career change?",
            lat=25.3176,
            lon=83.0067,
            question_type="career",
        )
        assert result["relevant_house"] == 10

    def test_relevant_house_for_marriage(self) -> None:
        result = compute_prashna(
            question="Marriage?",
            lat=25.3176,
            lon=83.0067,
            question_type="marriage",
        )
        assert result["relevant_house"] == 7

    def test_specific_time(self) -> None:
        """Test with a specific datetime."""
        fixed_time = datetime(2026, 3, 19, 12, 0, tzinfo=UTC)
        result = compute_prashna(
            question="Test",
            lat=25.3176,
            lon=83.0067,
            question_time=fixed_time,
        )
        assert result["chart"] is not None
        assert result["question_time"] == fixed_time.isoformat()

    def test_deterministic_with_fixed_time(self) -> None:
        """Same time should produce same answer."""
        fixed_time = datetime(2026, 1, 15, 10, 30, tzinfo=UTC)
        r1 = compute_prashna("Test", 25.3176, 83.0067, question_time=fixed_time)
        r2 = compute_prashna("Test", 25.3176, 83.0067, question_time=fixed_time)
        assert r1["answer"] == r2["answer"]
