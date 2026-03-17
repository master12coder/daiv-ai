"""North Indian diamond chart — matplotlib image renderer."""
from __future__ import annotations

import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

from jyotish_engine.models.chart import ChartData
from jyotish_engine.constants import SIGNS, SIGNS_HI

# Planet abbreviations
_ABBREV = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa",
    "Rahu": "Ra", "Ketu": "Ke",
}

# North Indian house positions (x, y centers for 12 houses in diamond layout)
# Diamond: house 1 at top-left, going clockwise
_HOUSE_POSITIONS: dict[int, tuple[float, float]] = {
    1:  (0.25, 0.75),   # Top-left
    2:  (0.0,  0.5),    # Left-top
    3:  (0.25, 0.25),   # Bottom-left
    4:  (0.5,  0.0),    # Bottom
    5:  (0.75, 0.25),   # Bottom-right
    6:  (1.0,  0.5),    # Right-bottom
    7:  (0.75, 0.75),   # Top-right (opposite lagna)
    8:  (1.0,  0.5),    # Right-top (shared with 6)
    9:  (0.75, 0.75),   # Shared
    10: (0.5,  1.0),    # Top
    11: (0.25, 0.75),   # Shared
    12: (0.0,  0.5),    # Shared
}

# Simplified: use triangular grid positions
_GRID: dict[int, tuple[float, float]] = {
    12: (2.5, 4.5),
    1:  (1.0, 3.5),
    11: (4.0, 3.5),
    2:  (0.0, 2.5),
    10: (5.0, 2.5),
    3:  (1.0, 1.5),
    9:  (4.0, 1.5),
    4:  (2.5, 0.5),
    8:  (5.0, 2.5),
    5:  (1.0, 1.5),
    7:  (4.0, 1.5),
    6:  (2.5, 0.5),
}

# Better layout: 4 rows, each cell identified
_CELLS: dict[int, tuple[float, float]] = {
    12: (2.5, 4.0),
    1:  (1.0, 3.0),  11: (4.0, 3.0),
    2:  (0.0, 2.0),  10: (5.0, 2.0),
    3:  (1.0, 1.0),  9:  (4.0, 1.0),
    4:  (2.5, 0.0),
    5:  (1.0, -0.5), 7:  (4.0, -0.5),
    6:  (2.5, -1.0),
    8:  (5.0, 0.5),
}


def _get_planets_text(chart: ChartData) -> dict[int, str]:
    """Get planet text per house."""
    houses: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    for p in chart.planets.values():
        label = _ABBREV.get(p.name, p.name[:2])
        if p.is_retrograde:
            label += "ᴿ"
        if p.is_combust:
            label += "ᶜ"
        houses[p.house].append(label)
    return {h: "\n".join(planets) for h, planets in houses.items()}


def render_chart_image(
    chart: ChartData,
    output_path: str | Path | None = None,
) -> bytes | None:
    """Render North Indian diamond chart as PNG image.

    Args:
        chart: Computed birth chart.
        output_path: If provided, save to file. Otherwise return bytes.

    Returns:
        PNG bytes if output_path is None, else None (saved to file).
    """
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.set_xlim(-0.5, 6)
    ax.set_ylim(-1.5, 5.5)
    ax.set_aspect("equal")
    ax.axis("off")

    # Title
    ax.text(2.75, 5.2, f"Kundali — {chart.name}",
            ha="center", va="center", fontsize=16, fontweight="bold",
            fontfamily="serif")
    ax.text(2.75, 4.8,
            f"Lagna: {chart.lagna_sign} ({chart.lagna_sign_en}) | "
            f"{chart.dob} {chart.tob}",
            ha="center", va="center", fontsize=10, color="gray")

    # Draw diamond outline
    diamond_x = [2.5, 0, 2.5, 5, 2.5]
    diamond_y = [4.5, 2, -0.5, 2, 4.5]
    ax.plot(diamond_x, diamond_y, "k-", linewidth=2)

    # Cross lines
    ax.plot([0, 5], [2, 2], "k-", linewidth=1)      # Horizontal
    ax.plot([2.5, 2.5], [-0.5, 4.5], "k-", linewidth=1)  # Vertical
    ax.plot([1.25, 3.75], [3.25, 3.25], "k-", linewidth=0.5)  # Upper inner
    ax.plot([1.25, 3.75], [0.75, 0.75], "k-", linewidth=0.5)  # Lower inner

    # House positions for text
    positions: dict[int, tuple[float, float]] = {
        12: (2.5, 3.8),
        1:  (1.2, 3.0),  11: (3.8, 3.0),
        2:  (0.5, 2.0),  10: (4.5, 2.0),
        3:  (1.2, 1.0),  9:  (3.8, 1.0),
        4:  (2.5, 0.2),
        5:  (1.2, -0.1), 7:  (3.8, -0.1),
        6:  (2.5, -0.8),
        8:  (4.5, 0.5),
    }

    planets_text = _get_planets_text(chart)

    for house_num in range(1, 13):
        x, y = positions.get(house_num, (2.5, 2.0))
        sign_idx = (chart.lagna_sign_index + house_num - 1) % 12
        sign_hi = SIGNS[sign_idx][:3]
        sign_abbr = SIGNS[sign_idx][:3]

        # House number + sign
        ax.text(x, y + 0.25, f"{house_num}",
                ha="center", va="center", fontsize=8, color="gray")
        ax.text(x, y + 0.1, sign_hi,
                ha="center", va="center", fontsize=7, color="darkblue")

        # Planets
        pt = planets_text.get(house_num, "")
        if pt:
            ax.text(x, y - 0.15, pt,
                    ha="center", va="center", fontsize=9, fontweight="bold",
                    color="darkred")

    # Lagna marker
    ax.text(2.5, 2.0, "Lagna",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color="green",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow",
                      edgecolor="green", linewidth=2))

    plt.tight_layout()

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(path), dpi=150, bbox_inches="tight",
                    facecolor="white", edgecolor="none")
        plt.close(fig)
        return None
    else:
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                    facecolor="white", edgecolor="none")
        plt.close(fig)
        buf.seek(0)
        return buf.read()
