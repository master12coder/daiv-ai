"""Weekly pooja planner — personalized based on chart lordship.

Generates a 7-day worship/activity plan that accounts for which
planets are benefic, malefic, or maraka for the specific lagna.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from jyotish.compute.chart import ChartData
from jyotish.compute.dasha import find_current_dasha
from jyotish.interpret.knowledge_loader import build_lordship_context
from jyotish.utils.logging_config import get_logger

logger = get_logger(__name__)

_WEEKLY_YAML = Path(__file__).parent.parent / "knowledge" / "weekly_routine.yaml"
_REMEDY_YAML = Path(__file__).parent.parent / "knowledge" / "remedy_rules.yaml"

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

DAY_PLANETS = {
    "monday": "Moon", "tuesday": "Mars", "wednesday": "Mercury",
    "thursday": "Jupiter", "friday": "Venus", "saturday": "Saturn",
    "sunday": "Sun",
}


@dataclass
class DayPlan:
    """Plan for a single day of the week."""
    day: str
    day_hindi: str
    planet: str
    deity: str
    color: str
    food: str
    mantra: str
    daan: str
    activity: str
    avoid: str
    is_planet_benefic: bool
    lordship_note: str


@dataclass
class WeeklyPlan:
    """Complete weekly pooja and activity plan."""
    lagna: str
    lagna_en: str
    current_dasha_lord: str
    days: list[DayPlan]
    special_notes: list[str]


def _load_weekly_routine() -> dict[str, Any]:
    """Load weekly routine YAML."""
    if _WEEKLY_YAML.exists():
        with open(_WEEKLY_YAML) as f:
            return yaml.safe_load(f) or {}
    return {}


def generate_weekly_plan(chart: ChartData) -> WeeklyPlan:
    """Generate a personalized weekly pooja plan.

    Args:
        chart: Natal chart data.

    Returns:
        WeeklyPlan with 7 day plans personalized to the lagna.
    """
    lordship = build_lordship_context(chart.lagna_sign)
    routine = _load_weekly_routine()

    benefic_names = {b.get("planet", "") for b in lordship.get("functional_benefics", [])}
    malefic_names = {m.get("planet", "") for m in lordship.get("functional_malefics", [])}
    maraka_names = {m.get("planet", "") for m in lordship.get("maraka", [])}
    lagnesh = lordship.get("sign_lord", "")

    # Current dasha lord
    try:
        md, _, _ = find_current_dasha(chart)
        dasha_lord = md.lord
    except Exception:
        dasha_lord = "Unknown"

    day_hindi = {
        "monday": "सोमवार", "tuesday": "मंगलवार", "wednesday": "बुधवार",
        "thursday": "गुरुवार", "friday": "शुक्रवार", "saturday": "शनिवार",
        "sunday": "रविवार",
    }

    days: list[DayPlan] = []
    special_notes: list[str] = []

    for day_key in DAYS:
        planet = DAY_PLANETS[day_key]
        day_data = routine.get(day_key, {})

        is_benefic = planet in benefic_names or planet == lagnesh
        is_malefic = planet in malefic_names
        is_maraka = planet in maraka_names

        # Lordship note
        if planet == lagnesh:
            note = f"{planet} is LAGNESH — always strengthen. Priority day."
        elif is_benefic:
            note = f"{planet} is functional benefic — worship recommended."
        elif is_maraka and not is_benefic:
            note = f"{planet} is MARAKA — do daan/charity, NOT strengthening pooja."
        elif is_malefic:
            note = f"{planet} is functional malefic — do daan to pacify, avoid strengthening."
        else:
            note = f"{planet} is neutral for {chart.lagna_sign_en} lagna."

        # Adjust activity based on lordship
        activity = day_data.get("activity", "")
        daan = day_data.get("daan", "")

        if is_maraka and not is_benefic:
            activity = f"Daan for {planet} (maraka). {daan}"
            special_notes.append(
                f"{day_key.title()}: {planet} is maraka for {chart.lagna_sign_en}. "
                f"Do charity/daan, NOT strengthening pooja."
            )

        days.append(DayPlan(
            day=day_key.title(),
            day_hindi=day_hindi.get(day_key, ""),
            planet=planet,
            deity=day_data.get("deity", ""),
            color=day_data.get("color", ""),
            food=day_data.get("food", ""),
            mantra=day_data.get("mantra", ""),
            daan=daan,
            activity=activity,
            avoid=day_data.get("avoid", ""),
            is_planet_benefic=is_benefic,
            lordship_note=note,
        ))

    # Add dasha-specific note
    if dasha_lord in maraka_names and dasha_lord not in benefic_names:
        special_notes.insert(0,
            f"Current {dasha_lord} Mahadasha is MARAKA period. "
            f"Prioritize {lagnesh} (Lagnesh) strengthening on {lagnesh}'s day."
        )

    return WeeklyPlan(
        lagna=chart.lagna_sign,
        lagna_en=chart.lagna_sign_en,
        current_dasha_lord=dasha_lord,
        days=days,
        special_notes=special_notes,
    )
