"""Pandit plugin engine — wraps the corrections store."""
from __future__ import annotations

from pathlib import Path

from jyotish_products.store.corrections import PanditCorrection, PanditCorrectionStore


def add_correction(
    chart_name: str,
    category: str,
    what: str,
    reasoning: str,
    data_dir: str | Path | None = None,
) -> str:
    """Add a pandit correction.

    Creates a new PanditCorrection record and persists it via the store.

    Args:
        chart_name: Name of the chart this correction applies to.
        category: Correction category (gemstone, house_reading, dasha, etc.).
        what: What the pandit says (the correction content).
        reasoning: Why the pandit disagrees with the AI interpretation.
        data_dir: Optional override for the corrections data directory.

    Returns:
        Confirmation string with the correction ID.
    """
    store = PanditCorrectionStore(data_dir=data_dir)
    correction = PanditCorrection(
        chart_name=chart_name,
        category=category,
        pandit_said=what,
        pandit_reasoning=reasoning,
    )
    correction_id = store.add_correction(correction)
    return f"Correction added: {correction_id} [{category}] for {chart_name}"


def list_corrections(
    data_dir: str | Path | None = None,
    status: str | None = None,
    category: str | None = None,
) -> str:
    """List pandit corrections with optional filters.

    Args:
        data_dir: Optional override for the corrections data directory.
        status: Filter by status (pending, validated, disputed, etc.).
        category: Filter by category (gemstone, dasha, etc.).

    Returns:
        Formatted string listing all matching corrections.
    """
    store = PanditCorrectionStore(data_dir=data_dir)
    corrections = store.list_corrections(status=status, category=category)

    if not corrections:
        return "No corrections found."

    lines: list[str] = []
    lines.append(f"Pandit Corrections ({len(corrections)} found)")
    lines.append("=" * 45)
    for c in corrections:
        lines.append(
            f"  [{c.id}] {c.category} | {c.chart_name} | "
            f"{c.status} | {c.pandit_said[:60]}"
        )
    return "\n".join(lines)
