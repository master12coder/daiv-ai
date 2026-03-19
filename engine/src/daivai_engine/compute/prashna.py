"""Prashna Kundli (Horary Chart) — chart for the moment of a question.

No birth data needed — computes chart for question time and place.
Analysis based on lagna lord strength, Moon condition, and relevant
house lord position.

Source: Prashna Marga, Prashna Tantra, Tajaka methods.
"""

from __future__ import annotations

from datetime import UTC, datetime

from daivai_engine.compute.chart import compute_chart
from daivai_engine.constants import KENDRAS, SIGN_LORDS, TRIKONAS


# Question type → relevant house
_QUESTION_HOUSES: dict[str, int] = {
    "general": 1,
    "health": 1,
    "wealth": 2,
    "siblings": 3,
    "property": 4,
    "education": 5,
    "children": 5,
    "enemies": 6,
    "marriage": 7,
    "partnership": 7,
    "longevity": 8,
    "fortune": 9,
    "career": 10,
    "gains": 11,
    "loss": 12,
    "travel": 12,
}


def compute_prashna(
    question: str,
    lat: float,
    lon: float,
    tz_name: str = "Asia/Kolkata",
    question_time: datetime | None = None,
    question_type: str = "general",
) -> dict:
    """Compute a Prashna (horary) chart and derive a verdict.

    Args:
        question: The question being asked.
        lat: Latitude of the place where question is asked.
        lon: Longitude of the place.
        tz_name: Timezone name.
        question_time: Exact time of question. Defaults to now.
        question_type: Category (marriage, career, etc.) for house selection.

    Returns:
        Dict with chart, answer, reasoning, and key factors.
    """
    if question_time is None:
        question_time = datetime.now(tz=UTC)

    # Compute chart for question moment
    dob = question_time.strftime("%d/%m/%Y")
    tob = question_time.strftime("%H:%M")
    chart = compute_chart(
        name="Prashna",
        dob=dob,
        tob=tob,
        lat=lat,
        lon=lon,
        tz_name=tz_name,
        gender="Male",
    )

    # Analysis
    relevant_house = _QUESTION_HOUSES.get(question_type, 1)
    lagna_lord = SIGN_LORDS[chart.lagna_sign_index]
    relevant_lord = SIGN_LORDS[(chart.lagna_sign_index + relevant_house - 1) % 12]
    moon = chart.planets["Moon"]

    # Lagna lord analysis
    ll_planet = chart.planets.get(lagna_lord)
    ll_strong = ll_planet is not None and ll_planet.house in KENDRAS + TRIKONAS[1:]

    # Relevant house lord analysis
    rl_planet = chart.planets.get(relevant_lord)
    rl_strong = rl_planet is not None and rl_planet.house in KENDRAS + TRIKONAS[1:]
    rl_in_dusthana = rl_planet is not None and rl_planet.house in (6, 8, 12)

    # Moon analysis
    moon_strong = moon.house in KENDRAS + TRIKONAS[1:]
    moon_waxing = moon.longitude > chart.planets["Sun"].longitude or (
        moon.longitude < chart.planets["Sun"].longitude
        and abs(moon.longitude - chart.planets["Sun"].longitude) > 180
    )

    # Verdict
    positive_factors = sum([ll_strong, rl_strong, moon_strong, moon_waxing])
    negative_factors = sum([not ll_strong, rl_in_dusthana, not moon_strong])

    if positive_factors >= 3:
        answer = "YES"
    elif negative_factors >= 3:
        answer = "NO"
    else:
        answer = "MAYBE"

    reasoning = _build_reasoning(
        lagna_lord,
        ll_strong,
        relevant_lord,
        rl_strong,
        rl_in_dusthana,
        moon_strong,
        moon_waxing,
        relevant_house,
        question_type,
    )

    return {
        "question": question,
        "question_time": question_time.isoformat(),
        "chart": chart,
        "answer": answer,
        "reasoning": reasoning,
        "lagna_lord": lagna_lord,
        "relevant_house": relevant_house,
        "relevant_lord": relevant_lord,
        "moon_strong": moon_strong,
        "moon_waxing": moon_waxing,
    }


def _build_reasoning(
    lagna_lord: str,
    ll_strong: bool,
    relevant_lord: str,
    rl_strong: bool,
    rl_in_dusthana: bool,
    moon_strong: bool,
    moon_waxing: bool,
    house: int,
    qtype: str,
) -> str:
    """Build human-readable reasoning for the verdict."""
    parts: list[str] = []

    if ll_strong:
        parts.append(f"Lagna lord {lagna_lord} is strong in kendra/trikona (positive).")
    else:
        parts.append(f"Lagna lord {lagna_lord} is not well-placed (negative).")

    if rl_strong:
        parts.append(f"House {house} lord {relevant_lord} is strong (positive for {qtype}).")
    elif rl_in_dusthana:
        parts.append(f"House {house} lord {relevant_lord} is in dusthana (negative for {qtype}).")
    else:
        parts.append(f"House {house} lord {relevant_lord} is moderately placed.")

    if moon_strong:
        parts.append("Moon is well-placed (positive emotional outcome).")
    if moon_waxing:
        parts.append("Moon is waxing (positive energy).")
    else:
        parts.append("Moon is waning (delays possible).")

    return " ".join(parts)
