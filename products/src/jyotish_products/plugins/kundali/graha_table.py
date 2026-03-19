"""Graha Sthiti table renderer — planet positions with full metadata.

Generates a ReportLab Table with columns:
Planet | Sign | Degree | Nakshatra | Pada | House | Motion | Avastha | Bala | Lordship Role
All text uses Hindi-English mix per the Sanatan Dharma theme.
"""

from __future__ import annotations

from typing import Any

from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from jyotish_engine.models.chart import ChartData, PlanetData
from jyotish_engine.models.strength import ShadbalaResult
from jyotish_products.plugins.kundali.theme import (
    INDIGO,
    LIGHT_SAFFRON,
    PLANET_HI,
    SAFFRON,
    register_fonts,
)


# Column headers (Hindi + English mix)
_HEADERS = [
    "ग्रह\nPlanet",
    "राशि\nSign",
    "अंश\nDegree",
    "नक्षत्र\nNakshatra",
    "पाद\nPada",
    "भाव\nHouse",
    "गति\nMotion",
    "अवस्था\nAvastha",
    "बल\nBala",
    "लग्न-फल\nRole",
]

_AVASTHA_HI = {
    "Bala": "बाल",
    "Kumara": "कुमार",
    "Yuva": "युवा",
    "Vriddha": "वृद्ध",
    "Mruta": "मृत",
}


def render_graha_table(
    chart: ChartData,
    shadbala: list[ShadbalaResult],
    lordship_ctx: dict[str, Any],
) -> list[Any]:
    """Render planet position table as ReportLab flowable elements.

    Args:
        chart: Computed birth chart.
        shadbala: Pre-computed Shadbala results for 7 planets.
        lordship_ctx: Lordship context for functional role classification.

    Returns:
        List of ReportLab flowable elements (Paragraph heading + Table).
    """
    register_fonts()
    font = "NotoDevanagari" if _font_available() else "Helvetica"

    benefics = {e["planet"] for e in lordship_ctx.get("functional_benefics", [])}
    malefics = {e["planet"] for e in lordship_ctx.get("functional_malefics", [])}
    yk = lordship_ctx.get("yogakaraka", {})
    yogakaraka = yk.get("planet", "") if isinstance(yk, dict) else ""
    maraka_planets = {m["planet"] for m in lordship_ctx.get("maraka", [])}

    # Build strength lookup
    bala_map: dict[str, float] = {}
    for sb in shadbala:
        bala_map[sb.planet] = sb.ratio

    # Build table data
    data = [_HEADERS]
    for p in chart.planets.values():
        row = _planet_row(p, bala_map, benefics, malefics, yogakaraka, maraka_planets, lordship_ctx)
        data.append(row)

    # Column widths (total ~18cm for A4)
    col_w = [
        1.6 * cm,
        1.8 * cm,
        1.4 * cm,
        2.2 * cm,
        0.8 * cm,
        0.9 * cm,
        1.3 * cm,
        1.4 * cm,
        1.0 * cm,
        3.2 * cm,
    ]

    table = Table(data, colWidths=col_w, repeatRows=1)
    table.setStyle(_table_style(len(data), font))

    from reportlab.lib.styles import ParagraphStyle

    heading = Paragraph(
        "ग्रह स्थिति — Planetary Positions",
        ParagraphStyle(
            "GrahaH", fontName=font, fontSize=14, textColor=INDIGO, spaceAfter=8, spaceBefore=12
        ),
    )
    return [heading, table, Spacer(1, 0.3 * cm)]


def _planet_row(
    p: PlanetData,
    bala_map: dict[str, float],
    benefics: set[str],
    malefics: set[str],
    yogakaraka: str,
    maraka: set[str],
    ctx: dict[str, Any],
) -> list[str]:
    """Build one table row for a planet."""
    hi = PLANET_HI.get(p.name, p.name[:2])
    planet_cell = f"{hi} {p.name}"

    sign_cell = f"{p.sign}"
    deg_cell = f"{p.degree_in_sign:.1f}°"
    nak_cell = p.nakshatra
    pada_cell = str(p.pada)
    house_cell = str(p.house)

    # Motion: direct / retro / combust
    motion_parts = []
    if p.is_retrograde:
        motion_parts.append("वक्री")
    if p.is_combust:
        motion_parts.append("अस्त")
    motion_cell = " ".join(motion_parts) if motion_parts else "→"

    # Avastha
    avastha_cell = _AVASTHA_HI.get(p.avastha, p.avastha)

    # Shadbala ratio
    ratio = bala_map.get(p.name, 0)
    bala_cell = f"{ratio:.1f}" if ratio > 0 else "—"

    # Functional role
    role_cell = _role_label(p.name, benefics, malefics, yogakaraka, maraka, ctx)

    return [
        planet_cell,
        sign_cell,
        deg_cell,
        nak_cell,
        pada_cell,
        house_cell,
        motion_cell,
        avastha_cell,
        bala_cell,
        role_cell,
    ]


def _role_label(
    name: str,
    benefics: set[str],
    malefics: set[str],
    yogakaraka: str,
    maraka: set[str],
    ctx: dict[str, Any],
) -> str:
    """Generate functional role label for a planet."""
    parts: list[str] = []
    # House lordships
    houses_owned = _get_houses(name, ctx)
    if houses_owned:
        parts.append("+".join(str(h) for h in houses_owned))

    if name == yogakaraka:
        parts.append("योगकारक")
    elif name in maraka:
        parts.append("मारक")
    elif name in benefics:
        parts.append("शुभ")
    elif name in malefics:
        parts.append("अशुभ")

    return " ".join(parts) if parts else "—"


def _get_houses(planet: str, ctx: dict[str, Any]) -> list[int]:
    """Get house numbers owned by a planet from lordship context."""
    result: list[int] = []
    for h_str, lord in ctx.get("house_lords", {}).items():
        if lord == planet:
            result.append(int(h_str))
    return sorted(result)


def _table_style(num_rows: int, font: str) -> TableStyle:
    """Build ReportLab TableStyle for the graha table."""
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), SAFFRON),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, -1), font),
            ("FONTSIZE", (0, 0), (-1, 0), 7),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_SAFFRON]),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]
    )


def _font_available() -> bool:
    """Check if NotoDevanagari is registered."""
    try:
        from reportlab.pdfbase.pdfmetrics import getFont

        getFont("NotoDevanagari")
        return True
    except KeyError:
        return False
