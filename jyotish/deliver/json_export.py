"""JSON export for integrations."""

from __future__ import annotations

import json
from pathlib import Path

from jyotish.compute.chart import ChartData
from jyotish.interpret.formatter import chart_to_dict


def export_chart_json(
    chart: ChartData,
    output_path: str | Path | None = None,
    pretty: bool = True,
) -> str:
    """Export chart data as JSON.

    Args:
        chart: Computed chart data
        output_path: Where to save (optional)
        pretty: Pretty-print JSON

    Returns:
        JSON string
    """
    data = chart_to_dict(chart)
    indent = 2 if pretty else None
    content = json.dumps(data, indent=indent, ensure_ascii=False, default=str)

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    return content


def export_matching_json(
    matching_result: "MatchingResult",
    person1_name: str = "Person 1",
    person2_name: str = "Person 2",
    output_path: str | Path | None = None,
) -> str:
    """Export matching result as JSON."""
    from jyotish.compute.matching import MatchingResult

    data = {
        "person1": person1_name,
        "person2": person2_name,
        "total_obtained": matching_result.total_obtained,
        "total_max": matching_result.total_max,
        "percentage": matching_result.percentage,
        "recommendation": matching_result.recommendation,
        "kootas": [
            {
                "name": k.name,
                "name_hindi": k.name_hindi,
                "max_points": k.max_points,
                "obtained": k.obtained,
                "description": k.description,
            }
            for k in matching_result.kootas
        ],
    }

    content = json.dumps(data, indent=2, ensure_ascii=False)

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    return content
