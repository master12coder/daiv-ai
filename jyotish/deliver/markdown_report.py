"""Markdown report generation."""

from __future__ import annotations

from pathlib import Path

from jyotish.compute.chart import ChartData
from jyotish.interpret.formatter import format_report_markdown, format_chart_terminal


def generate_markdown_report(
    chart: ChartData,
    interpretations: dict[str, str] | None = None,
    output_path: str | Path | None = None,
) -> str:
    """Generate a markdown report for a chart.

    Args:
        chart: Computed chart data
        interpretations: LLM interpretation sections (optional)
        output_path: Where to save the report (optional)

    Returns:
        The markdown content
    """
    if interpretations:
        content = format_report_markdown(chart, interpretations)
    else:
        content = format_chart_terminal(chart)

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    return content


def generate_matching_report(
    matching_result: "MatchingResult",
    person1_name: str = "Person 1",
    person2_name: str = "Person 2",
    output_path: str | Path | None = None,
) -> str:
    """Generate a markdown report for Ashtakoot matching."""
    from jyotish.compute.matching import MatchingResult

    lines = []
    lines.append(f"# Ashtakoot Matching Report")
    lines.append(f"**{person1_name}** × **{person2_name}**")
    lines.append("")

    lines.append(f"## Score: {matching_result.total_obtained} / {matching_result.total_max} ({matching_result.percentage}%)")
    lines.append(f"**Recommendation:** {matching_result.recommendation}")
    lines.append("")

    lines.append("## Koota Breakdown")
    lines.append("| Koota | Hindi | Max | Obtained | Description |")
    lines.append("|-------|-------|-----|----------|-------------|")
    for k in matching_result.kootas:
        lines.append(f"| {k.name} | {k.name_hindi} | {k.max_points} | {k.obtained} | {k.description} |")
    lines.append("")

    content = "\n".join(lines)

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    return content
