"""Predictions plugin engine — dashboard stats from the prediction tracker."""
from __future__ import annotations

from typing import Any

from jyotish_products.store.predictions import PredictionTracker


def get_dashboard_stats(db_path: str | None = None) -> dict[str, Any]:
    """Get prediction accuracy statistics.

    Opens the prediction tracker database, retrieves the accuracy dashboard,
    and returns it as a plain dict. The database connection is closed after use.

    Args:
        db_path: Optional path to the SQLite database. Uses default if None.

    Returns:
        Dict with keys: categories, overall_accuracy, total_predictions, pending.
    """
    kwargs: dict[str, Any] = {}
    if db_path is not None:
        kwargs["db_path"] = db_path

    tracker = PredictionTracker(**kwargs)
    try:
        return tracker.get_accuracy_dashboard()
    finally:
        tracker.close()


def format_dashboard(stats: dict[str, Any]) -> str:
    """Format dashboard stats into a human-readable string.

    Args:
        stats: Dashboard dict from get_dashboard_stats.

    Returns:
        Formatted multi-line report string.
    """
    lines: list[str] = []
    lines.append("Prediction Accuracy Dashboard")
    lines.append("=" * 40)
    lines.append("")
    lines.append(f"Total predictions: {stats.get('total_predictions', 0)}")
    lines.append(f"Pending: {stats.get('pending', 0)}")
    lines.append(f"Overall accuracy: {stats.get('overall_accuracy', 0.0)}%")
    lines.append("")

    categories = stats.get("categories", {})
    if categories:
        lines.append("By Category:")
        for cat, data in categories.items():
            lines.append(
                f"  {cat}: {data['accuracy']}% "
                f"({data['confirmed']}/{data['total_decided']} confirmed)"
            )

    return "\n".join(lines)
