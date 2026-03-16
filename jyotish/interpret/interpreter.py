"""Main interpretation orchestrator — combines chart data with LLM prompts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Template

from jyotish.compute.chart import ChartData
from jyotish.compute.dasha import compute_mahadashas, find_current_dasha
from jyotish.compute.yoga import detect_all_yogas
from jyotish.compute.dosha import detect_all_doshas
from jyotish.compute.strength import compute_planet_strengths
from jyotish.compute.divisional import compute_navamsha, get_vargottam_planets
from jyotish.interpret.llm_backend import LLMBackend, get_backend


PROMPTS_DIR = Path(__file__).parent / "prompts"


def _load_prompt(template_name: str) -> str:
    """Load a prompt template from the prompts directory."""
    path = PROMPTS_DIR / template_name
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")
    return path.read_text()


def _render_prompt(template_name: str, context: dict[str, Any]) -> str:
    """Load and render a Jinja2 prompt template."""
    raw = _load_prompt(template_name)
    template = Template(raw)
    return template.render(**context)


def _build_chart_context(chart: ChartData) -> dict[str, Any]:
    """Build a context dictionary from chart data for prompt rendering."""
    yogas = detect_all_yogas(chart)
    doshas = detect_all_doshas(chart)
    strengths = compute_planet_strengths(chart)
    vargottam = get_vargottam_planets(chart)
    mahadashas = compute_mahadashas(chart)

    try:
        md, ad, pd = find_current_dasha(chart)
        current_dasha = {
            "mahadasha": md.lord,
            "antardasha": ad.lord,
            "pratyantardasha": pd.lord,
            "md_start": md.start.strftime("%d/%m/%Y"),
            "md_end": md.end.strftime("%d/%m/%Y"),
            "ad_start": ad.start.strftime("%d/%m/%Y"),
            "ad_end": ad.end.strftime("%d/%m/%Y"),
        }
    except Exception:
        current_dasha = {"mahadasha": "Unknown", "antardasha": "Unknown", "pratyantardasha": "Unknown"}

    planet_summary = []
    for p in chart.planets.values():
        planet_summary.append({
            "name": p.name,
            "sign": p.sign,
            "sign_en": p.sign_en,
            "house": p.house,
            "degree": f"{p.degree_in_sign:.1f}°",
            "nakshatra": p.nakshatra,
            "pada": p.pada,
            "dignity": p.dignity,
            "retrograde": p.is_retrograde,
            "combust": p.is_combust,
            "sign_lord": p.sign_lord,
        })

    yoga_summary = [
        {"name": y.name, "name_hindi": y.name_hindi, "description": y.description, "effect": y.effect}
        for y in yogas if y.is_present
    ]

    dosha_summary = [
        {"name": d.name, "name_hindi": d.name_hindi, "severity": d.severity, "description": d.description}
        for d in doshas if d.is_present
    ]

    strength_summary = [
        {"planet": s.planet, "rank": s.rank, "strength": s.total_relative, "is_strong": s.is_strong}
        for s in strengths
    ]

    return {
        "name": chart.name,
        "dob": chart.dob,
        "tob": chart.tob,
        "place": chart.place,
        "gender": chart.gender,
        "lagna": chart.lagna_sign,
        "lagna_en": chart.lagna_sign_en,
        "lagna_hi": chart.lagna_sign_hi,
        "lagna_degree": f"{chart.lagna_degree:.1f}°",
        "planets": planet_summary,
        "yogas": yoga_summary,
        "doshas": dosha_summary,
        "strengths": strength_summary,
        "vargottam_planets": vargottam,
        "current_dasha": current_dasha,
        "mahadashas": [
            {"lord": md.lord, "start": md.start.strftime("%d/%m/%Y"), "end": md.end.strftime("%d/%m/%Y")}
            for md in mahadashas
        ],
    }


def interpret_chart(
    chart: ChartData,
    backend: LLMBackend | None = None,
    sections: list[str] | None = None,
) -> dict[str, str]:
    """Generate full chart interpretation using LLM.

    Args:
        chart: Computed chart data
        backend: LLM backend to use (default from config)
        sections: Specific sections to interpret (default: all)

    Returns:
        Dictionary of section_name -> interpreted text
    """
    if backend is None:
        backend = get_backend()

    context = _build_chart_context(chart)
    system_prompt = _render_prompt("system_prompt.md", context)

    all_sections = [
        "chart_overview",
        "career_analysis",
        "financial_analysis",
        "health_analysis",
        "relationship_analysis",
        "spiritual_profile",
        "remedy_generation",
    ]

    if sections:
        all_sections = [s for s in sections if s in all_sections]

    results: dict[str, str] = {}

    for section in all_sections:
        template_name = f"{section}.md"
        try:
            user_prompt = _render_prompt(template_name, context)
            response = backend.generate(system_prompt, user_prompt)
            results[section] = response
        except FileNotFoundError:
            results[section] = f"[Template {template_name} not found]"
        except Exception as e:
            results[section] = f"[Error generating {section}: {e}]"

    return results


def interpret_with_events(
    chart: ChartData,
    events: list[dict[str, str]],
    backend: LLMBackend | None = None,
) -> str:
    """Interpret chart with life event validation.

    Args:
        chart: Computed chart data
        events: List of {"date": "DD/MM/YYYY", "event": "description"}
        backend: LLM backend
    """
    if backend is None:
        backend = get_backend()

    context = _build_chart_context(chart)
    context["life_events"] = events

    system_prompt = _render_prompt("system_prompt.md", context)
    user_prompt = _render_prompt("life_event_validation.md", context)

    return backend.generate(system_prompt, user_prompt)


def get_daily_suggestion(
    chart: ChartData,
    backend: LLMBackend | None = None,
) -> str:
    """Get daily suggestion based on transits."""
    if backend is None:
        backend = get_backend()

    from jyotish.compute.transit import compute_transits
    transit_data = compute_transits(chart)

    context = _build_chart_context(chart)
    context["transits"] = [
        {"name": t.name, "sign": t.sign, "house": t.natal_house_activated, "retrograde": t.is_retrograde}
        for t in transit_data.transits
    ]
    context["major_transits"] = transit_data.major_transits
    context["transit_date"] = transit_data.target_date

    system_prompt = _render_prompt("system_prompt.md", context)
    user_prompt = _render_prompt("daily_suggestion.md", context)

    return backend.generate(system_prompt, user_prompt)
