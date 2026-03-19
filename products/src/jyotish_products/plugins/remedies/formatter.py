"""Gemstone weight report formatter — text output for CLI and PDF."""

from __future__ import annotations

from jyotish_products.plugins.remedies.gemstone import GemstoneWeightResult


def format_gemstone_report(
    results: list[GemstoneWeightResult],
    body_weight_kg: float,
    lagna_sign: str,
    name: str,
) -> str:
    """Format gemstone weight results into a comprehensive text report.

    Args:
        results: List of GemstoneWeightResult from compute_gemstone_weights.
        body_weight_kg: Native's body weight in kg.
        lagna_sign: Lagna sign name.
        name: Native's name.

    Returns:
        Formatted multi-line report string.
    """
    lines: list[str] = []
    lines.append(f"GEMSTONE WEIGHT ANALYSIS — {name} ({lagna_sign} Lagna, {body_weight_kg} kg)")
    lines.append("=" * 70)
    lines.append("")

    rec = [r for r in results if r.status == "recommended"]
    test = [r for r in results if r.status == "test_with_caution"]
    prohibited = [r for r in results if r.status == "prohibited"]

    # Recommended stones with full breakdown
    if rec:
        lines.append("RECOMMENDED STONES")
        lines.append("-" * 40)
        for r in rec:
            lines.extend(_format_stone_detail(r))
            lines.append("")

    # Test with caution
    if test:
        lines.append("TEST WITH CAUTION")
        lines.append("-" * 40)
        for r in test:
            lines.extend(_format_stone_detail(r))
            lines.append("")

    # Prohibited
    if prohibited:
        lines.append("PROHIBITED STONES")
        lines.append("-" * 40)
        for r in prohibited:
            lines.append(f"  X {r.stone_name} ({r.stone_name_hi}) — {r.planet}")
            lines.append(f"    Reason: {r.prohibition_reason}")
            if r.free_alternatives:
                alt = r.free_alternatives
                lines.append(
                    f"    Free alt: mantra={alt.get('mantra', '-')}, daan={alt.get('daan', '-')}"
                )
        lines.append("")

    # Quality vs weight note
    lines.append("QUALITY vs WEIGHT")
    lines.append("-" * 40)
    lines.append("  A 2-ratti high-clarity, untreated stone outperforms a 5-ratti")
    lines.append("  heavily-included or treated stone. Prioritize: natural, eye-clean,")
    lines.append("  vivid color, no heat/oil treatment over raw carat weight.")
    lines.append("")

    # Shastra note
    lines.append("SHASTRA NOTE")
    lines.append("-" * 40)
    lines.append("  No classical text (BPHS, Ratna Prakash, Garuda Purana) prescribes")
    lines.append("  exact gemstone weight. The body_weight/10 formula is a modern")
    lines.append("  convention from the gemstone trade, not scripture. This engine")
    lines.append("  provides a data-driven starting point, not a definitive answer.")
    lines.append("")

    # Pandit Ji discussion questions
    lines.append("DISCUSS WITH YOUR PANDIT JI")
    lines.append("-" * 40)
    lines.append("  1. Should I test with a smaller stone (1-2 ratti) for 7 days first?")
    lines.append("  2. Given my current dasha, is timing right for this stone?")
    lines.append("  3. Is substitute stone (upratna) sufficient for my budget?")
    lines.append("  4. Should I combine stone with mantra recitation?")
    lines.append("  5. Any specific muhurta (day/hora) for wearing ceremony?")

    return "\n".join(lines)


def _format_stone_detail(r: GemstoneWeightResult) -> list[str]:
    """Format one stone with factor breakdown, comparison, and pros/cons."""
    lines: list[str] = []
    marker = "+" if r.status == "recommended" else "?"
    lines.append(f"  {marker} {r.stone_name} ({r.stone_name_hi}) — {r.planet}")
    lines.append(f"    Recommended: {r.recommended_ratti:.2f} ratti (base: {r.base_ratti:.1f})")
    lines.append("")

    # Factor breakdown table
    lines.append("    Factor Breakdown:")
    lines.append(f"    {'Factor':<20s} {'Value':<20s} {'Mult':>6s}  Note")
    lines.append(f"    {'─' * 20} {'─' * 20} {'─' * 6}  {'─' * 30}")
    for f in r.factors:
        lines.append(
            f"    {f.name:<20s} {f.raw_value:<20s} {f.multiplier:>5.2f}x  {f.explanation[:40]}"
        )
    lines.append("")

    # Website comparison
    if r.website_comparisons:
        lines.append("    Website Comparison (body-weight formula only):")
        for site, val in r.website_comparisons.items():
            diff = val - r.recommended_ratti
            arrow = "↑" if diff > 0.5 else "↓" if diff < -0.5 else "≈"
            lines.append(f"      {site:<15s} {val:>5.1f} ratti  {arrow}")
        lines.append(
            f"      {'This engine':<15s} {r.recommended_ratti:>5.2f} ratti  (10-factor adjusted)"
        )
        lines.append("")

    # Pros/cons for light/medium/heavy
    if r.pros_cons:
        lines.append("    Weight Options:")
        for label, notes in r.pros_cons.items():
            lines.append(f"      {label}:")
            for note in notes:
                lines.append(f"        • {note}")
        lines.append("")

    # Free alternatives
    if r.free_alternatives:
        alt = r.free_alternatives
        lines.append("    Free Alternatives:")
        for key, val in alt.items():
            lines.append(f"      {key.title()}: {val}")

    return lines
