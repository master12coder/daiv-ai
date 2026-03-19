"""Reusable divisional chart renderer — D9/D10/any varga as diamond image.

Same diamond layout as D1, but renders divisional chart positions.
Vargottam planets marked with a star. Accepts pre-computed DivisionalPosition
list from report.py (no engine calls inside this renderer).
"""

from __future__ import annotations

import io
from pathlib import Path
from typing import Any

import matplotlib


matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from jyotish_engine.constants import SIGNS_HI
from jyotish_engine.models.chart import ChartData
from jyotish_engine.models.divisional import DivisionalPosition
from jyotish_products.plugins.kundali.theme import (
    MPL_CREAM,
    MPL_GOLD,
    MPL_GRAY,
    MPL_INDIGO,
    MPL_SAFFRON,
    MPL_TEXT,
    PLANET_HI,
    get_font_path,
)


# Same diamond geometry as D1 chart
_CENTER_X, _CENTER_Y = 2.5, 2.5
_HOUSE_XY: dict[int, tuple[float, float]] = {
    12: (2.5, 4.2),
    1: (1.0, 3.3),
    11: (4.0, 3.3),
    2: (0.4, 2.5),
    10: (4.6, 2.5),
    3: (1.0, 1.7),
    9: (4.0, 1.7),
    4: (2.5, 0.8),
    5: (1.0, 0.4),
    7: (4.0, 0.4),
    6: (2.5, 0.0),
    8: (4.6, 1.0),
}


def render_divisional_chart(
    chart: ChartData,
    positions: list[DivisionalPosition],
    varga_name: str,
    varga_label_hi: str,
    output_path: str | Path | None = None,
) -> bytes | None:
    """Render a divisional chart as a diamond PNG image.

    Args:
        chart: Original birth chart (for metadata).
        positions: Pre-computed DivisionalPosition list from engine.
        varga_name: Chart name, e.g. "D9 Navamsha".
        varga_label_hi: Hindi label, e.g. "नवमांश".
        output_path: Save path or None for bytes.

    Returns:
        PNG bytes if output_path is None, else None.
    """
    fp_small = _get_font_props(size=7)
    fp_planet = _get_font_props(size=8.5)
    fp_title = _get_font_props(size=14)

    fig, ax = plt.subplots(figsize=(7.5, 8.0))
    fig.patch.set_facecolor(MPL_CREAM)
    ax.set_xlim(-0.8, 5.8)
    ax.set_ylim(-0.8, 5.8)
    ax.set_aspect("equal")
    ax.axis("off")

    # Saffron header
    ax.axhspan(5.2, 5.6, color=MPL_SAFFRON, alpha=0.9)
    ax.text(
        _CENTER_X,
        5.4,
        f"{varga_name} — {varga_label_hi} — {chart.name}",
        ha="center",
        va="center",
        fontproperties=fp_title,
        color="white",
    )

    # Diamond outline
    _draw_diamond(ax)

    # Group planets by divisional sign
    planets_by_sign = _group_by_sign(positions)
    vargottam_set = {p.planet for p in positions if p.is_vargottam}

    # Render each house
    for house in range(1, 13):
        x, y = _HOUSE_XY.get(house, (_CENTER_X, _CENTER_Y))
        # Divisional charts: house 1 = Aries (0), house 2 = Taurus (1), etc.
        sign_idx = house - 1
        sign_hi = SIGNS_HI[sign_idx]

        ax.text(
            x,
            y + 0.35,
            f"{house} {sign_hi}",
            ha="center",
            va="center",
            fontproperties=fp_small,
            color=MPL_GRAY,
        )

        # Planets in this sign
        sign_planets = planets_by_sign.get(sign_idx, [])
        for i, pos in enumerate(sign_planets):
            py = y + 0.05 - i * 0.18
            hi = PLANET_HI.get(pos.planet, pos.planet[:2])
            label = f"{hi}"
            if pos.is_vargottam:
                label += " *"
            color = MPL_GOLD if pos.is_vargottam else MPL_TEXT
            ax.text(x, py, label, ha="center", va="center", fontproperties=fp_planet, color=color)

    # Center label
    ax.text(
        _CENTER_X,
        _CENTER_Y + 0.1,
        varga_label_hi,
        ha="center",
        va="center",
        fontproperties=_get_font_props(size=13),
        color=MPL_INDIGO,
        alpha=0.3,
    )
    ax.text(
        _CENTER_X,
        _CENTER_Y - 0.15,
        f"Lagna: {chart.lagna_sign_hi}",
        ha="center",
        va="center",
        fontproperties=fp_small,
        color=MPL_INDIGO,
    )

    # Vargottam legend
    if vargottam_set:
        varg_names = ", ".join(PLANET_HI.get(p, p) for p in sorted(vargottam_set))
        ax.text(
            _CENTER_X,
            -0.45,
            f"* वर्गोत्तम: {varg_names}",
            ha="center",
            va="center",
            fontproperties=_get_font_props(size=7),
            color=MPL_GOLD,
        )

    # Footer
    ax.text(
        _CENTER_X,
        -0.65,
        f"{chart.dob} | {chart.tob} | vedic-ai-framework",
        ha="center",
        va="center",
        fontproperties=_get_font_props(size=6),
        color=MPL_GRAY,
    )

    plt.tight_layout(pad=0.5)
    return _save_or_bytes(fig, output_path)


# ── Helpers ──────────────────────────────────────────────────────────────


def _group_by_sign(positions: list[DivisionalPosition]) -> dict[int, list[DivisionalPosition]]:
    """Group DivisionalPosition by divisional_sign_index."""
    result: dict[int, list[DivisionalPosition]] = {}
    for p in positions:
        result.setdefault(p.divisional_sign_index, []).append(p)
    return result


def _draw_diamond(ax: Any) -> None:
    """Draw the diamond outline and grid."""
    dx = [_CENTER_X, 0, _CENTER_X, 5, _CENTER_X]
    dy = [4.8, _CENTER_Y, 0.2, _CENTER_Y, 4.8]
    ax.plot(dx, dy, color=MPL_INDIGO, linewidth=2.5)
    ax.plot([0, 5], [_CENTER_Y, _CENTER_Y], color=MPL_INDIGO, linewidth=1.2)
    ax.plot([_CENTER_X, _CENTER_X], [0.2, 4.8], color=MPL_INDIGO, linewidth=1.2)
    ax.plot([1.25, 3.75], [3.65, 3.65], color=MPL_INDIGO, linewidth=0.6)
    ax.plot([1.25, 3.75], [1.35, 1.35], color=MPL_INDIGO, linewidth=0.6)
    ax.plot([1.25, 1.25], [1.35, 3.65], color=MPL_INDIGO, linewidth=0.6)
    ax.plot([3.75, 3.75], [1.35, 3.65], color=MPL_INDIGO, linewidth=0.6)


def _get_font_props(size: float = 10) -> FontProperties:
    """Get matplotlib FontProperties with Devanagari support."""
    fp_path = get_font_path()
    if fp_path and fp_path.exists():
        return FontProperties(fname=str(fp_path), size=size)
    return FontProperties(size=size)


def _save_or_bytes(fig: Any, output_path: str | Path | None) -> bytes | None:
    """Save figure to file or return PNG bytes."""
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            str(path), dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none"
        )
        plt.close(fig)
        return None
    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
        dpi=150,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
        edgecolor="none",
    )
    plt.close(fig)
    buf.seek(0)
    return buf.read()
