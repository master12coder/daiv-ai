"""PDF kundali report generator using reportlab."""
from __future__ import annotations

import io
import logging
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image,
)
from reportlab.lib import colors

from jyotish_engine.models.chart import ChartData
from jyotish_engine.compute.dasha import compute_mahadashas, find_current_dasha
from jyotish_engine.compute.yoga import detect_all_yogas
from jyotish_engine.compute.dosha import detect_all_doshas
from jyotish_engine.compute.chart import get_house_lord
from jyotish_products.interpret.context import build_lordship_context

logger = logging.getLogger(__name__)

ACCENT = HexColor("#8B4513")  # Saddle brown — traditional feel
HEADER_BG = HexColor("#FFF8DC")  # Cornsilk


def _styles() -> dict[str, ParagraphStyle]:
    """Create custom paragraph styles."""
    ss = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=ss["Title"], fontSize=20,
                                textColor=ACCENT, spaceAfter=12),
        "h1": ParagraphStyle("H1", parent=ss["Heading1"], fontSize=14,
                             textColor=ACCENT, spaceAfter=6, spaceBefore=12),
        "h2": ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12,
                             textColor=ACCENT, spaceAfter=4),
        "body": ParagraphStyle("Body", parent=ss["Normal"], fontSize=10,
                               spaceAfter=4, leading=14),
        "small": ParagraphStyle("Small", parent=ss["Normal"], fontSize=8,
                                textColor=colors.gray),
    }


def generate_pdf(
    chart: ChartData,
    output_path: str | Path | None = None,
    chart_image_bytes: bytes | None = None,
) -> bytes | None:
    """Generate a complete kundali PDF report.

    Args:
        chart: Computed birth chart.
        output_path: Save to file if provided.
        chart_image_bytes: Optional pre-rendered chart image PNG bytes.

    Returns:
        PDF bytes if output_path is None, else None.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)

    st = _styles()
    story: list = []

    # ── Title Page ──
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("कुंडली — Kundali Report", st["title"]))
    story.append(Paragraph(f"<b>{chart.name}</b>", st["h1"]))
    story.append(Paragraph(
        f"DOB: {chart.dob} | TOB: {chart.tob} | Place: {chart.place}",
        st["body"],
    ))
    story.append(Paragraph(
        f"Lagna: {chart.lagna_sign} ({chart.lagna_sign_en} / {chart.lagna_sign_hi}) "
        f"at {chart.lagna_degree:.1f}°",
        st["body"],
    ))
    story.append(Spacer(1, 0.5 * inch))

    # Chart image if provided
    if chart_image_bytes:
        img_buf = io.BytesIO(chart_image_bytes)
        img = Image(img_buf, width=4 * inch, height=4 * inch)
        story.append(img)

    story.append(PageBreak())

    # ── Planetary Positions ──
    story.append(Paragraph("Planetary Positions (ग्रह स्थिति)", st["h1"]))

    planet_data = [["Planet", "Sign", "House", "Degree", "Nakshatra", "Pada", "Dignity"]]
    for p in chart.planets.values():
        flags = ""
        if p.is_retrograde:
            flags += " (R)"
        if p.is_combust:
            flags += " (C)"
        planet_data.append([
            p.name + flags, p.sign, str(p.house),
            f"{p.degree_in_sign:.1f}°", p.nakshatra, str(p.pada), p.dignity,
        ])

    t = Table(planet_data, colWidths=[80, 70, 40, 50, 90, 35, 60])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), ACCENT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#FAFAFA")]),
        ("ALIGN", (2, 0), (3, -1), "CENTER"),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3 * inch))

    # ── House Lords ──
    story.append(Paragraph("House Lords (भाव स्वामी)", st["h1"]))
    lord_data = [["House", "Lord", "Placed In"]]
    for h in range(1, 13):
        lord = get_house_lord(chart, h)
        lp = chart.planets.get(lord)
        placed = f"{lp.sign} (H{lp.house})" if lp else "—"
        lord_data.append([str(h), lord, placed])

    t2 = Table(lord_data, colWidths=[50, 80, 120])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.3 * inch))

    # ── Yogas ──
    story.append(Paragraph("Yogas (योग)", st["h1"]))
    yogas = detect_all_yogas(chart)
    for y in yogas:
        icon = "✅" if y.effect == "benefic" else "⚠️" if y.effect == "mixed" else "❌"
        story.append(Paragraph(
            f"{icon} <b>{y.name}</b> ({y.name_hindi}) — {y.description}",
            st["body"],
        ))

    # ── Doshas ──
    story.append(Paragraph("Doshas (दोष)", st["h1"]))
    doshas = detect_all_doshas(chart)
    for d in doshas:
        icon = "⚠️" if d.is_present else "✅"
        story.append(Paragraph(f"{icon} <b>{d.name}</b> — {d.description}", st["body"]))

    story.append(PageBreak())

    # ── Dasha Timeline ──
    story.append(Paragraph("Vimshottari Mahadasha (विंशोत्तरी महादशा)", st["h1"]))
    dashas = compute_mahadashas(chart)
    from datetime import datetime
    now = datetime.now(tz=dashas[0].start.tzinfo) if dashas else datetime.now()

    dasha_data = [["Planet", "Start", "End", "Status"]]
    for md in dashas:
        status = "← CURRENT" if md.start <= now <= md.end else ""
        dasha_data.append([
            md.lord, md.start.strftime("%Y-%m-%d"),
            md.end.strftime("%Y-%m-%d"), status,
        ])

    t3 = Table(dasha_data, colWidths=[70, 90, 90, 80])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(t3)
    story.append(Spacer(1, 0.3 * inch))

    # ── Gemstone Recommendations ──
    story.append(Paragraph("Gemstone Recommendations (रत्न सुझाव)", st["h1"]))
    ctx = build_lordship_context(chart.lagna_sign)

    for s in ctx.get("recommended_stones", []):
        story.append(Paragraph(
            f"✅ <b>RECOMMENDED:</b> {s['stone']} ({s['planet']})", st["body"],
        ))
    for s in ctx.get("test_stones", []):
        story.append(Paragraph(
            f"⚠️ <b>TEST:</b> {s['stone']} ({s['planet']})", st["body"],
        ))
    for s in ctx.get("prohibited_stones", []):
        story.append(Paragraph(
            f"❌ <b>PROHIBITED:</b> {s['stone']} ({s['planet']}) — {s['reasoning'][:100]}",
            st["body"],
        ))

    maraka = ctx.get("maraka", [])
    if maraka:
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("MARAKA Planets (मारक ग्रह)", st["h2"]))
        for m in maraka:
            story.append(Paragraph(
                f"⚠️ {m['planet']} — {m['house_str']}", st["body"],
            ))

    # ── Footer ──
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(
        "Generated by Jyotish AI — Vedic Astrology Framework | "
        "Computation: Swiss Ephemeris (NASA JPL DE431) | Lahiri Ayanamsha",
        st["small"],
    ))

    doc.build(story)
    pdf_bytes = buf.getvalue()

    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(pdf_bytes)
        logger.info("PDF saved to %s (%d bytes)", path, len(pdf_bytes))
        return None

    return pdf_bytes
