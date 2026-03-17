"""Tests for the predictions plugin engine."""
from __future__ import annotations

import tempfile
from pathlib import Path

from jyotish_products.plugins.predictions.engine import get_dashboard_stats, format_dashboard
from jyotish_products.store.predictions import PredictionTracker, Prediction


class TestPredictionsPlugin:
    def test_empty_dashboard_returns_zeros(self, tmp_path: Path) -> None:
        """get_dashboard_stats on an empty DB should return zero-filled stats."""
        db_path = tmp_path / "test_predictions.db"
        stats = get_dashboard_stats(db_path=str(db_path))
        assert stats["total_predictions"] == 0
        assert stats["pending"] == 0
        assert stats["overall_accuracy"] == 0.0
        assert stats["categories"] == {}

    def test_dashboard_with_data(self, tmp_path: Path) -> None:
        """Dashboard should reflect logged predictions with outcomes."""
        db_path = tmp_path / "test_predictions.db"

        # Seed some predictions
        tracker = PredictionTracker(db_path=str(db_path))
        pid1 = tracker.log_prediction(Prediction(
            prediction_date="2024-01-01", category="career",
            prediction="Promotion expected", confidence=0.8,
        ))
        pid2 = tracker.log_prediction(Prediction(
            prediction_date="2024-01-01", category="career",
            prediction="Job change", confidence=0.6,
        ))
        tracker.update_outcome(pid1, "confirmed")
        tracker.update_outcome(pid2, "not_occurred")
        tracker.close()

        stats = get_dashboard_stats(db_path=str(db_path))
        assert stats["total_predictions"] == 2
        assert stats["pending"] == 0
        career = stats["categories"]["career"]
        assert career["confirmed"] == 1
        assert career["total_decided"] == 2
        assert career["accuracy"] == 50.0

    def test_format_dashboard_output(self) -> None:
        """format_dashboard should produce a readable string."""
        stats = {
            "total_predictions": 5,
            "pending": 2,
            "overall_accuracy": 66.7,
            "categories": {
                "career": {"accuracy": 66.7, "confirmed": 2, "total_decided": 3},
            },
        }
        text = format_dashboard(stats)
        assert "Prediction Accuracy Dashboard" in text
        assert "66.7%" in text
        assert "career" in text
