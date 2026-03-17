"""Simple JSON-based chart save/load for persistent chart storage."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_DIR = Path("data/saved_charts")


class ChartStore:
    """JSON file-based chart persistence.

    Saves computed chart data as JSON files for later retrieval,
    enabling chart reuse across sessions without recomputation.
    """

    def __init__(self, data_dir: str | Path | None = None) -> None:
        """Initialize with directory path for chart storage.

        Args:
            data_dir: Directory to store chart JSON files. Defaults to data/saved_charts/.
        """
        self._dir = Path(data_dir) if data_dir else _DEFAULT_DIR
        self._dir.mkdir(parents=True, exist_ok=True)

    def _chart_path(self, chart_id: str) -> Path:
        """Get file path for a chart ID."""
        safe_id = chart_id.replace("/", "_").replace("\\", "_").replace(" ", "_")
        return self._dir / f"{safe_id}.json"

    def save(self, chart_id: str, chart_data: Any) -> Path:
        """Save chart data to JSON file.

        Args:
            chart_id: Unique identifier for the chart (typically name or hash).
            chart_data: ChartData dataclass or dict to persist.

        Returns:
            Path to the saved JSON file.
        """
        path = self._chart_path(chart_id)

        if hasattr(chart_data, "__dataclass_fields__"):
            data = asdict(chart_data)
        elif isinstance(chart_data, dict):
            data = chart_data
        else:
            raise TypeError(f"Cannot serialize chart_data of type {type(chart_data)}")

        # Add metadata
        data["_chart_id"] = chart_id

        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        logger.info("Chart saved: %s -> %s", chart_id, path)
        return path

    def load(self, chart_id: str) -> dict[str, Any] | None:
        """Load chart data from JSON file.

        Args:
            chart_id: The chart identifier used when saving.

        Returns:
            Chart data as dict, or None if not found.
        """
        path = self._chart_path(chart_id)
        if not path.exists():
            logger.debug("Chart not found: %s", chart_id)
            return None

        with open(path) as f:
            data = json.load(f)

        logger.debug("Chart loaded: %s", chart_id)
        return data

    def delete(self, chart_id: str) -> bool:
        """Delete a saved chart.

        Args:
            chart_id: The chart identifier to delete.

        Returns:
            True if deleted, False if not found.
        """
        path = self._chart_path(chart_id)
        if path.exists():
            path.unlink()
            logger.info("Chart deleted: %s", chart_id)
            return True
        return False

    def list_charts(self) -> list[dict[str, str]]:
        """List all saved charts with basic metadata.

        Returns:
            List of dicts with chart_id and file path.
        """
        charts: list[dict[str, str]] = []
        for path in sorted(self._dir.glob("*.json")):
            try:
                with open(path) as f:
                    data = json.load(f)
                charts.append({
                    "chart_id": data.get("_chart_id", path.stem),
                    "name": data.get("name", "Unknown"),
                    "dob": data.get("dob", ""),
                    "lagna": data.get("lagna_sign", data.get("lagna", "")),
                    "path": str(path),
                })
            except (json.JSONDecodeError, OSError):
                continue
        return charts

    def exists(self, chart_id: str) -> bool:
        """Check if a chart is saved."""
        return self._chart_path(chart_id).exists()
