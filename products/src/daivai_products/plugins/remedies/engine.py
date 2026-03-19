"""Remedies plugin engine — gemstone recommendations with safety checks."""

from __future__ import annotations

from daivai_engine.models.chart import ChartData
from daivai_products.interpret.context import build_lordship_context


def get_gemstone_recommendations(chart: ChartData) -> str:
    """Get personalized gemstone recommendations with safety checks.

    Loads lordship rules for the chart's lagna and classifies gemstones into
    RECOMMENDED, TEST WITH CAUTION, and PROHIBITED categories. Maraka planets
    are always flagged with dual-nature warnings per Vedic safety rules.

    Args:
        chart: Computed birth chart.

    Returns:
        Formatted multi-line string with gemstone recommendations.
    """
    ctx = build_lordship_context(chart.lagna_sign)
    if not ctx:
        return f"No lordship rules found for lagna: {chart.lagna_sign}"

    return _format_recommendations(ctx, chart.name, chart.lagna_sign)


def _format_recommendations(
    ctx: dict[str, object],
    name: str,
    lagna_sign: str,
) -> str:
    """Format lordship context into a gemstone recommendation report.

    Args:
        ctx: Lordship context dict from build_lordship_context.
        name: Native's name.
        lagna_sign: Lagna sign name.

    Returns:
        Formatted multi-line report string.
    """
    lines: list[str] = []
    lines.append(f"Gemstone Recommendations for {name} ({lagna_sign} Lagna)")
    lines.append("=" * 55)
    lines.append("")

    recommended = ctx.get("recommended_stones", [])
    test_stones = ctx.get("test_stones", [])
    prohibited = ctx.get("prohibited_stones", [])

    if recommended:
        lines.append("RECOMMENDED:")
        for s in recommended:  # type: ignore[union-attr]
            lines.append(f"  + {s['stone']} ({s['planet']}) — {s['reasoning'][:80]}")
        lines.append("")

    if test_stones:
        lines.append("TEST WITH CAUTION:")
        for s in test_stones:  # type: ignore[union-attr]
            lines.append(f"  ? {s['stone']} ({s['planet']}) — {s['reasoning'][:80]}")
        lines.append("")

    if prohibited:
        lines.append("PROHIBITED:")
        for s in prohibited:  # type: ignore[union-attr]
            lines.append(f"  X {s['stone']} ({s['planet']}) — {s['reasoning'][:80]}")
        lines.append("")

    maraka = ctx.get("maraka", [])
    if maraka:
        lines.append("MARAKA WARNINGS:")
        for m in maraka:  # type: ignore[union-attr]
            lines.append(
                f"  ! {m['planet']} — {m['house_str']} — "
                f"dual-nature: acknowledge both positive and negative effects"
            )

    return "\n".join(lines)
