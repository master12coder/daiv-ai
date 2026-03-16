"""Output formatting — markdown, JSON, terminal display."""

from __future__ import annotations

import json
from typing import Any

from jyotish.compute.chart import ChartData
from jyotish.compute.dasha import compute_mahadashas, find_current_dasha
from jyotish.compute.yoga import detect_all_yogas
from jyotish.compute.dosha import detect_all_doshas
from jyotish.compute.strength import compute_planet_strengths


def format_chart_terminal(chart: ChartData) -> str:
    """Format chart data for terminal display using rich-compatible markdown."""
    lines = []
    lines.append(f"# Vedic Birth Chart — {chart.name}")
    lines.append(f"**DOB:** {chart.dob}  **TOB:** {chart.tob}  **Place:** {chart.place}")
    lines.append(f"**Lagna:** {chart.lagna_sign} ({chart.lagna_sign_en}) — {chart.lagna_degree:.1f}°")
    lines.append("")

    # Planet table
    lines.append("## Planetary Positions")
    lines.append("| Planet | Sign | House | Degree | Nakshatra | Pada | Dignity | R | C |")
    lines.append("|--------|------|-------|--------|-----------|------|---------|---|---|")
    for p in chart.planets.values():
        retro = "R" if p.is_retrograde else ""
        combust = "C" if p.is_combust else ""
        lines.append(
            f"| {p.name:8s} | {p.sign:12s} | {p.house:5d} | "
            f"{p.degree_in_sign:6.1f}° | {p.nakshatra:16s} | {p.pada} | "
            f"{p.dignity:12s} | {retro} | {combust} |"
        )
    lines.append("")

    # Yogas
    yogas = detect_all_yogas(chart)
    present_yogas = [y for y in yogas if y.is_present]
    if present_yogas:
        lines.append("## Yogas Detected")
        for y in present_yogas:
            emoji = "+" if y.effect == "benefic" else "-" if y.effect == "malefic" else "~"
            lines.append(f"  [{emoji}] {y.name} ({y.name_hindi}) — {y.description}")
        lines.append("")

    # Doshas
    doshas = detect_all_doshas(chart)
    present_doshas = [d for d in doshas if d.is_present]
    if present_doshas:
        lines.append("## Doshas")
        for d in present_doshas:
            lines.append(f"  [{d.severity}] {d.name} ({d.name_hindi}) — {d.description}")
        lines.append("")

    # Dasha
    try:
        md, ad, pd = find_current_dasha(chart)
        lines.append("## Current Dasha")
        lines.append(f"  Mahadasha:       {md.lord} ({md.start.strftime('%d/%m/%Y')} - {md.end.strftime('%d/%m/%Y')})")
        lines.append(f"  Antardasha:      {ad.lord} ({ad.start.strftime('%d/%m/%Y')} - {ad.end.strftime('%d/%m/%Y')})")
        lines.append(f"  Pratyantardasha: {pd.lord} ({pd.start.strftime('%d/%m/%Y')} - {pd.end.strftime('%d/%m/%Y')})")
        lines.append("")
    except Exception:
        pass

    return "\n".join(lines)


def format_chart_json(chart: ChartData) -> str:
    """Format chart data as JSON."""
    data = chart_to_dict(chart)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


def chart_to_dict(chart: ChartData) -> dict[str, Any]:
    """Convert ChartData to a serializable dictionary."""
    yogas = detect_all_yogas(chart)
    doshas = detect_all_doshas(chart)
    strengths = compute_planet_strengths(chart)

    try:
        md, ad, pd = find_current_dasha(chart)
        current_dasha = {
            "mahadasha": {"lord": md.lord, "start": md.start.isoformat(), "end": md.end.isoformat()},
            "antardasha": {"lord": ad.lord, "start": ad.start.isoformat(), "end": ad.end.isoformat()},
            "pratyantardasha": {"lord": pd.lord, "start": pd.start.isoformat(), "end": pd.end.isoformat()},
        }
    except Exception:
        current_dasha = {}

    mahadashas = compute_mahadashas(chart)

    return {
        "chart": {
            "name": chart.name,
            "dob": chart.dob,
            "tob": chart.tob,
            "place": chart.place,
            "gender": chart.gender,
            "latitude": chart.latitude,
            "longitude": chart.longitude,
            "timezone": chart.timezone_name,
            "ayanamsha": round(chart.ayanamsha, 4),
        },
        "lagna": {
            "sign": chart.lagna_sign,
            "sign_en": chart.lagna_sign_en,
            "sign_hi": chart.lagna_sign_hi,
            "degree": round(chart.lagna_degree, 2),
        },
        "planets": {
            p.name: {
                "sign": p.sign,
                "sign_en": p.sign_en,
                "house": p.house,
                "degree_in_sign": round(p.degree_in_sign, 2),
                "nakshatra": p.nakshatra,
                "nakshatra_lord": p.nakshatra_lord,
                "pada": p.pada,
                "dignity": p.dignity,
                "is_retrograde": p.is_retrograde,
                "is_combust": p.is_combust,
                "sign_lord": p.sign_lord,
            }
            for p in chart.planets.values()
        },
        "yogas": [
            {"name": y.name, "name_hindi": y.name_hindi, "effect": y.effect, "description": y.description}
            for y in yogas if y.is_present
        ],
        "doshas": [
            {"name": d.name, "name_hindi": d.name_hindi, "severity": d.severity, "description": d.description}
            for d in doshas if d.is_present
        ],
        "strengths": [
            {"planet": s.planet, "rank": s.rank, "total_relative": s.total_relative}
            for s in strengths
        ],
        "current_dasha": current_dasha,
        "dasha_timeline": [
            {"lord": md.lord, "start": md.start.isoformat(), "end": md.end.isoformat()}
            for md in mahadashas
        ],
    }


def format_report_markdown(chart: ChartData, interpretations: dict[str, str]) -> str:
    """Format a full report with chart data and LLM interpretations."""
    lines = []
    lines.append(f"# Vedic Astrology Report — {chart.name}")
    lines.append(f"*DOB: {chart.dob} | TOB: {chart.tob} | Place: {chart.place}*")
    lines.append(f"*Lagna: {chart.lagna_sign} ({chart.lagna_sign_en} / {chart.lagna_sign_hi})*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Chart overview
    lines.append(format_chart_terminal(chart))
    lines.append("---")
    lines.append("")

    section_titles = {
        "chart_overview": "Chart Overview",
        "career_analysis": "Career Analysis",
        "financial_analysis": "Financial Analysis",
        "health_analysis": "Health Analysis",
        "relationship_analysis": "Relationship Analysis",
        "spiritual_profile": "Spiritual Profile",
        "remedy_generation": "Remedies & Recommendations",
        "life_event_validation": "Life Event Validation",
    }

    for section, text in interpretations.items():
        title = section_titles.get(section, section.replace("_", " ").title())
        lines.append(f"## {title}")
        lines.append("")
        lines.append(text)
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)
