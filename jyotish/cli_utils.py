"""Shared CLI utilities — chart loading, console, common options."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from rich.console import Console

from jyotish.compute.chart import ChartData, compute_chart
from jyotish.utils.logging_config import get_logger

logger = get_logger(__name__)
console = Console()


def load_chart_from_file(chart_path: str) -> ChartData:
    """Load and recompute a chart from a saved JSON file.

    Args:
        chart_path: Path to the chart JSON file.

    Returns:
        Recomputed ChartData.
    """
    path = Path(chart_path)
    if not path.exists():
        console.print(f"[red]Chart file not found: {chart_path}[/red]")
        sys.exit(1)

    data = json.loads(path.read_text())
    ci = data.get("chart", data)

    # Use lat/lon/tz if available (offline mode), otherwise use place
    lat = ci.get("latitude")
    lon = ci.get("longitude")
    tz = ci.get("timezone_name")
    gender = ci.get("gender", "Male")

    if lat is not None and lon is not None and tz:
        return compute_chart(
            name=ci["name"], dob=ci["dob"], tob=ci["tob"],
            lat=lat, lon=lon, tz_name=tz, gender=gender,
        )
    else:
        return compute_chart(
            name=ci["name"], dob=ci["dob"], tob=ci["tob"],
            place=ci.get("place", ""), gender=gender,
        )


def save_chart_to_file(chart: ChartData, output_path: str) -> None:
    """Save chart birth data to JSON for later reuse.

    Saves enough data for offline recomputation (includes lat/lon/tz).

    Args:
        chart: Computed chart data.
        output_path: Path to write JSON.
    """
    data = {
        "name": chart.name,
        "dob": chart.dob,
        "tob": chart.tob,
        "place": chart.place,
        "gender": chart.gender,
        "latitude": chart.latitude,
        "longitude": chart.longitude,
        "timezone_name": chart.timezone_name,
    }

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("Chart saved to %s", output_path)


def compute_or_load(
    name: str | None = None,
    dob: str | None = None,
    tob: str | None = None,
    place: str | None = None,
    gender: str = "Male",
    chart_file: str | None = None,
) -> ChartData:
    """Compute chart from birth data or load from file.

    Args:
        name: Full name (if computing fresh).
        dob: Date of birth DD/MM/YYYY.
        tob: Time of birth HH:MM.
        place: Place of birth.
        gender: Gender.
        chart_file: Path to saved chart JSON.

    Returns:
        ChartData.
    """
    if chart_file:
        return load_chart_from_file(chart_file)

    if not all([name, dob, tob, place]):
        console.print("[red]Provide either --chart or all of --name/--dob/--tob/--place[/red]")
        sys.exit(1)

    return compute_chart(name=name, dob=dob, tob=tob, place=place, gender=gender)
