"""Matching plugin engine — thin wrapper around Ashtakoot matching."""

from __future__ import annotations

from jyotish_engine.compute.matching import compute_ashtakoot
from jyotish_engine.models.chart import ChartData
from jyotish_engine.models.matching import MatchingResult


def _extract_moon_data(chart: ChartData) -> tuple[int, int]:
    """Extract Moon nakshatra index and sign index from a chart.

    Returns:
        Tuple of (nakshatra_index, moon_sign_index).

    Raises:
        ValueError: If Moon is not found in the chart.
    """
    moon = chart.planets.get("Moon")
    if moon is None:
        raise ValueError(f"Moon not found in chart for {chart.name}")
    return moon.nakshatra_index, moon.sign_index


def run_match(chart1: ChartData, chart2: ChartData) -> str:
    """Run Ashtakoot matching and return formatted result.

    Args:
        chart1: First person's birth chart (boy by convention).
        chart2: Second person's birth chart (girl by convention).

    Returns:
        Formatted multi-line string with koota scores and recommendation.
    """
    result = compute_match(chart1, chart2)
    return format_result(result, chart1.name, chart2.name)


def compute_match(chart1: ChartData, chart2: ChartData) -> MatchingResult:
    """Compute Ashtakoot matching between two charts.

    Args:
        chart1: First person's birth chart.
        chart2: Second person's birth chart.

    Returns:
        MatchingResult with all koota scores.
    """
    nak1, sign1 = _extract_moon_data(chart1)
    nak2, sign2 = _extract_moon_data(chart2)
    return compute_ashtakoot(nak1, sign1, nak2, sign2)


def format_result(result: MatchingResult, name1: str, name2: str) -> str:
    """Format a MatchingResult into a human-readable string.

    Args:
        result: The computed matching result.
        name1: First person's name.
        name2: Second person's name.

    Returns:
        Formatted multi-line report string.
    """
    lines: list[str] = []
    lines.append(f"Ashtakoot Matching: {name1} & {name2}")
    lines.append("=" * 50)
    lines.append("")

    for koota in result.kootas:
        lines.append(
            f"  {koota.name} ({koota.name_hindi}): "
            f"{koota.obtained}/{koota.max_points} — {koota.description}"
        )

    lines.append("")
    lines.append(f"Total: {result.total_obtained}/{result.total_max} ({result.percentage}%)")
    lines.append(f"Recommendation: {result.recommendation}")
    return "\n".join(lines)
