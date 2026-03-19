"""Extended dosha detection — Guru Chandal, Shrapit, Grahan, Angarak, Shakata, Daridra.

These are commonly checked doshas that every professional astrologer verifies.

Source: BPHS, Phaladeepika.
"""

from __future__ import annotations

from daivai_engine.compute.chart import ChartData, get_house_lord
from daivai_engine.constants import DUSTHANAS
from daivai_engine.models.dosha import DoshaResult


def detect_guru_chandal(chart: ChartData) -> DoshaResult:
    """Guru Chandal Dosha — Jupiter conjunct Rahu.

    Jupiter's wisdom is clouded by Rahu's illusions.
    Cancellation: Jupiter in own/exalted sign.

    Source: BPHS.
    """
    jup = chart.planets["Jupiter"]
    rahu = chart.planets["Rahu"]

    if jup.sign_index != rahu.sign_index:
        return _absent("Guru Chandal Dosha", "गुरु चण्डाल दोष")

    cancellations = []
    severity = "full"
    if jup.dignity in ("exalted", "own", "mooltrikona"):
        cancellations.append(f"Jupiter in {jup.dignity} sign — effect reduced")
        severity = "partial"

    return DoshaResult(
        name="Guru Chandal Dosha",
        name_hindi="गुरु चण्डाल दोष",
        is_present=True,
        severity=severity,
        planets_involved=["Jupiter", "Rahu"],
        houses_involved=[jup.house],
        description="Jupiter conjunct Rahu — wisdom clouded, unconventional beliefs",
        cancellation_reasons=cancellations,
    )


def detect_shrapit_dosha(chart: ChartData) -> DoshaResult:
    """Shrapit Dosha — Saturn conjunct Rahu.

    Indicates past-life karmic debt. Delays and obstacles.

    Source: Phaladeepika.
    """
    sat = chart.planets["Saturn"]
    rahu = chart.planets["Rahu"]

    if sat.sign_index != rahu.sign_index:
        return _absent("Shrapit Dosha", "शापित दोष")

    return DoshaResult(
        name="Shrapit Dosha",
        name_hindi="शापित दोष",
        is_present=True,
        severity="full",
        planets_involved=["Saturn", "Rahu"],
        houses_involved=[sat.house],
        description="Saturn conjunct Rahu — karmic debts, delays, repeated obstacles",
        cancellation_reasons=[],
    )


def detect_grahan_dosha(chart: ChartData) -> DoshaResult:
    """Grahan Dosha — Sun or Moon conjunct Rahu or Ketu.

    Eclipse-like effect on the luminary. Identity/emotional challenges.

    Source: BPHS.
    """
    sun = chart.planets["Sun"]
    moon = chart.planets["Moon"]
    rahu = chart.planets["Rahu"]
    ketu = chart.planets["Ketu"]

    affected: list[str] = []
    if sun.sign_index == rahu.sign_index:
        affected.extend(["Sun", "Rahu"])
    if sun.sign_index == ketu.sign_index:
        affected.extend(["Sun", "Ketu"])
    if moon.sign_index == rahu.sign_index:
        affected.extend(["Moon", "Rahu"])
    if moon.sign_index == ketu.sign_index:
        affected.extend(["Moon", "Ketu"])

    if not affected:
        return _absent("Grahan Dosha", "ग्रहण दोष")

    return DoshaResult(
        name="Grahan Dosha",
        name_hindi="ग्रहण दोष",
        is_present=True,
        severity="full",
        planets_involved=list(set(affected)),
        houses_involved=[],
        description=f"Luminary conjunct node ({', '.join(set(affected))}) — eclipse effect",
        cancellation_reasons=[],
    )


def detect_angarak_dosha(chart: ChartData) -> DoshaResult:
    """Angarak Dosha — Mars conjunct Rahu.

    Aggression amplified, accident-prone, sudden events.

    Source: Traditional Jyotish.
    """
    mars = chart.planets["Mars"]
    rahu = chart.planets["Rahu"]

    if mars.sign_index != rahu.sign_index:
        return _absent("Angarak Dosha", "अंगारक दोष")

    return DoshaResult(
        name="Angarak Dosha",
        name_hindi="अंगारक दोष",
        is_present=True,
        severity="full",
        planets_involved=["Mars", "Rahu"],
        houses_involved=[mars.house],
        description="Mars conjunct Rahu — amplified aggression, sudden events, accident risk",
        cancellation_reasons=[],
    )


def detect_shakata_dosha(chart: ChartData) -> DoshaResult:
    """Shakata Yoga/Dosha — Jupiter in 6/8/12 from Moon.

    Fortune fluctuates, ups and downs in life.
    Cancellation: Jupiter in kendra from Lagna.

    Source: Phaladeepika Ch.7.
    """
    jup = chart.planets["Jupiter"]
    moon = chart.planets["Moon"]
    distance = ((jup.sign_index - moon.sign_index) % 12) + 1

    if distance not in (6, 8, 12):
        return _absent("Shakata Dosha", "शकट दोष")

    cancellations = []
    severity = "full"
    if jup.house in (1, 4, 7, 10):  # Jupiter in kendra from Lagna
        cancellations.append("Jupiter in kendra from Lagna — Shakata cancelled")
        severity = "cancelled"

    return DoshaResult(
        name="Shakata Dosha",
        name_hindi="शकट दोष",
        is_present=True,
        severity=severity,
        planets_involved=["Jupiter", "Moon"],
        houses_involved=[distance],
        description=f"Jupiter in {distance}th from Moon — fortune fluctuates",
        cancellation_reasons=cancellations,
    )


def detect_daridra_dosha(chart: ChartData) -> DoshaResult:
    """Daridra Dosha — 11th lord in 6/8/12.

    Gains lord weakened, financial struggles.

    Source: BPHS.
    """
    lord_11 = get_house_lord(chart, 11)
    p = chart.planets.get(lord_11)

    if not p or p.house not in DUSTHANAS:
        return _absent("Daridra Dosha", "दरिद्र दोष")

    return DoshaResult(
        name="Daridra Dosha",
        name_hindi="दरिद्र दोष",
        is_present=True,
        severity="full",
        planets_involved=[lord_11],
        houses_involved=[11, p.house],
        description=f"11th lord ({lord_11}) in dusthana house {p.house} — financial difficulties",
        cancellation_reasons=[],
    )


def detect_extended_doshas(chart: ChartData) -> list[DoshaResult]:
    """Detect all 6 extended doshas."""
    return [
        detect_guru_chandal(chart),
        detect_shrapit_dosha(chart),
        detect_grahan_dosha(chart),
        detect_angarak_dosha(chart),
        detect_shakata_dosha(chart),
        detect_daridra_dosha(chart),
    ]


def _absent(name: str, name_hi: str) -> DoshaResult:
    return DoshaResult(
        name=name,
        name_hindi=name_hi,
        is_present=False,
        severity="none",
        planets_involved=[],
        houses_involved=[],
        description="Not present",
        cancellation_reasons=[],
    )
