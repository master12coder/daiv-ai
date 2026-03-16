"""PDF generation stub — requires reportlab (optional dependency)."""

from __future__ import annotations

from pathlib import Path

from jyotish.compute.chart import ChartData
from jyotish.interpret.formatter import format_chart_terminal


def generate_pdf_report(
    chart: ChartData,
    interpretations: dict[str, str] | None = None,
    output_path: str | Path = "report.pdf",
) -> Path:
    """Generate a PDF report for a chart.

    Requires: pip install reportlab
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import inch
    except ImportError:
        raise RuntimeError(
            "reportlab not installed. Run: pip install reportlab\n"
            "Or install with: pip install vedic-ai-framework[pdf]"
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"Vedic Birth Chart — {chart.name}", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        f"DOB: {chart.dob} | TOB: {chart.tob} | Place: {chart.place}",
        styles["Normal"],
    ))
    story.append(Paragraph(
        f"Lagna: {chart.lagna_sign} ({chart.lagna_sign_en})",
        styles["Normal"],
    ))
    story.append(Spacer(1, 0.3 * inch))

    # Planet table as text
    story.append(Paragraph("Planetary Positions", styles["Heading2"]))
    for p in chart.planets.values():
        retro = " [R]" if p.is_retrograde else ""
        combust = " [C]" if p.is_combust else ""
        line = (
            f"{p.name}: {p.sign} ({p.sign_en}), House {p.house}, "
            f"{p.degree_in_sign:.1f}°, {p.nakshatra} Pada {p.pada}, "
            f"{p.dignity}{retro}{combust}"
        )
        story.append(Paragraph(line, styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Interpretations if available
    if interpretations:
        for section, text in interpretations.items():
            title = section.replace("_", " ").title()
            story.append(Paragraph(title, styles["Heading2"]))
            # Split text into paragraphs
            for para in text.split("\n\n"):
                para = para.strip()
                if para:
                    story.append(Paragraph(para, styles["Normal"]))
                    story.append(Spacer(1, 0.1 * inch))
            story.append(Spacer(1, 0.2 * inch))

    doc.build(story)
    return output_path
