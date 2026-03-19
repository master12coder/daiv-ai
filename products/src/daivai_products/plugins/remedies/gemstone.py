"""Multi-factor gemstone weight engine — 10 chart-based factors for personalized ratti.

Computes recommended gemstone weight using planetary strength indicators from the
birth chart. Each stone gets a base weight (body_weight_kg / divisor) modified by
10 astrological factors. Includes website comparison and free alternatives.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from daivai_engine.compute.ashtakavarga import compute_ashtakavarga
from daivai_engine.compute.dasha import find_current_dasha
from daivai_engine.models.chart import ChartData
from daivai_products.interpret.context import build_lordship_context


# ── Planet → base weight divisor (body_weight_kg / divisor) ──────────────
_BASE_DIVISOR: dict[str, float] = {
    "Sun": 10,
    "Moon": 10,
    "Mars": 10,
    "Mercury": 12,
    "Jupiter": 10,
    "Venus": 20,
    "Saturn": 15,
    "Rahu": 10,
    "Ketu": 12,
}

# ── Planet → stone name (EN, HI) ────────────────────────────────────────
PLANET_STONE: dict[str, tuple[str, str]] = {
    "Sun": ("Ruby", "माणिक्य"),
    "Moon": ("Pearl", "मोती"),
    "Mars": ("Red Coral", "मूंगा"),
    "Mercury": ("Emerald", "पन्ना"),
    "Jupiter": ("Yellow Sapphire", "पुखराज"),
    "Venus": ("Diamond", "हीरा"),
    "Saturn": ("Blue Sapphire", "नीलम"),
    "Rahu": ("Hessonite", "गोमेद"),
    "Ketu": ("Cat's Eye", "लहसुनिया"),
}

# ── Factor multiplier tables ────────────────────────────────────────────
AVASTHA_MULT = {"Bala": 0.80, "Kumara": 0.90, "Yuva": 1.00, "Vriddha": 0.75, "Mruta": 0.65}
DIGNITY_MULT = {
    "exalted": 0.75,
    "mooltrikona": 0.80,
    "own": 0.85,
    "neutral": 1.00,
    "enemy": 0.95,
    "debilitated": 0.90,
}
STONE_ENERGY = {"Diamond": 0.35, "Blue Sapphire": 0.75, "Cat's Eye": 0.90}
PURPOSE_MULT = {"protection": 0.60, "growth": 0.90, "maximum": 1.00}

# ── Free alternatives per planet ────────────────────────────────────────
_FREE_ALT: dict[str, dict[str, str]] = {
    "Sun": {
        "mantra": "ओम् सूर्याय नमः (7000x)",
        "daan": "Wheat + Jaggery on Sunday",
        "color": "Red/Orange",
    },
    "Moon": {
        "mantra": "ओम् नमः शिवाय (11000x)",
        "daan": "Rice + Milk on Monday",
        "color": "White/Silver",
    },
    "Mars": {"mantra": "ओम् भौमाय नमः (10000x)", "daan": "Red lentils on Tuesday", "color": "Red"},
    "Mercury": {
        "mantra": "ओम् बुधाय नमः (9000x)",
        "daan": "Green moong on Wednesday",
        "color": "Green",
    },
    "Jupiter": {
        "mantra": "ओम् गुरुवे नमः (19000x)",
        "daan": "Turmeric + Chana on Thursday",
        "color": "Yellow",
    },
    "Venus": {
        "mantra": "ओम् शुक्राय नमः (16000x)",
        "daan": "Rice + Ghee on Friday",
        "color": "White/Pastel",
    },
    "Saturn": {
        "mantra": "ओम् शनैश्चराय नमः (23000x)",
        "daan": "Black til + Iron on Saturday",
        "color": "Black/Blue",
    },
    "Rahu": {
        "mantra": "ओम् राहवे नमः (18000x)",
        "daan": "Coconut + Blanket on Saturday",
        "color": "Grey/Smoke",
    },
    "Ketu": {
        "mantra": "ओम् केतवे नमः (17000x)",
        "daan": "Blanket for dog on Tuesday",
        "color": "Brown/Grey",
    },
}

_GOOD_HOUSES = {1, 4, 5, 7, 9, 10}
_TRIK_HOUSES = {6, 8, 12}


# ── Result models ────────────────────────────────────────────────────────


class WeightFactor(BaseModel):
    """One factor contributing to the gemstone weight computation."""

    model_config = ConfigDict(frozen=True)
    name: str
    raw_value: str
    multiplier: float
    explanation: str


class GemstoneWeightResult(BaseModel):
    """Full gemstone weight recommendation for one stone."""

    model_config = ConfigDict(frozen=True)
    planet: str
    stone_name: str
    stone_name_hi: str
    status: str  # recommended / test_with_caution / prohibited
    base_ratti: float
    recommended_ratti: float
    factors: list[WeightFactor]
    website_comparisons: dict[str, float]
    pros_cons: dict[str, list[str]]
    free_alternatives: dict[str, str]
    prohibition_reason: str | None = None


# ── Core computation ─────────────────────────────────────────────────────


def compute_gemstone_weights(
    chart: ChartData,
    body_weight_kg: float,
    purpose: str = "growth",
) -> list[GemstoneWeightResult]:
    """Compute personalized gemstone weights for all 9 planetary stones.

    Args:
        chart: Computed birth chart.
        body_weight_kg: Native's body weight in kg.
        purpose: 'protection', 'growth', or 'maximum'.

    Returns:
        List of GemstoneWeightResult — one per planet, sorted: recommended first,
        then test_with_caution, then prohibited.
    """
    ctx = build_lordship_context(chart.lagna_sign)
    if not ctx:
        return []

    ashtakavarga = compute_ashtakavarga(chart)
    md, ad, _pd = find_current_dasha(chart)

    rec_map = _build_recommendation_map(ctx)
    benefics = {e["planet"] for e in ctx.get("functional_benefics", [])}
    malefics = {e["planet"] for e in ctx.get("functional_malefics", [])}
    houses_map = _build_houses_map(ctx)

    results: list[GemstoneWeightResult] = []
    for planet, (stone_en, stone_hi) in PLANET_STONE.items():
        status, reason = rec_map.get(planet, ("neutral", ""))
        if status == "prohibited":
            results.append(_prohibited_result(planet, stone_en, stone_hi, reason))
            continue

        p_data = chart.planets.get(planet)
        if p_data is None:
            continue

        base = body_weight_kg / _BASE_DIVISOR.get(planet, 10)
        factors = _compute_factors(
            p_data,
            planet,
            base,
            body_weight_kg,
            ashtakavarga,
            md,
            ad,
            benefics,
            malefics,
            houses_map.get(planet, []),
            stone_en,
            purpose,
        )
        total_mult = 1.0
        for f in factors:
            total_mult *= f.multiplier
        recommended = round(base * total_mult * 4) / 4  # round to nearest 0.25
        recommended = max(recommended, 1.0)  # absolute floor 1 ratti

        results.append(
            GemstoneWeightResult(
                planet=planet,
                stone_name=stone_en,
                stone_name_hi=stone_hi,
                status="recommended" if status == "recommended" else "test_with_caution",
                base_ratti=round(base, 2),
                recommended_ratti=recommended,
                factors=factors,
                website_comparisons=_website_estimates(body_weight_kg, planet),
                pros_cons=_pros_cons(recommended, base),
                free_alternatives=_FREE_ALT.get(planet, {}),
                prohibition_reason=None,
            )
        )

    order = {"recommended": 0, "test_with_caution": 1, "prohibited": 2}
    results.sort(key=lambda r: order.get(r.status, 9))
    return results


def _compute_factors(
    p: Any,
    planet: str,
    base: float,
    kg: float,
    sav: Any,
    md: Any,
    ad: Any,
    benefics: set,
    malefics: set,
    houses: list[int],
    stone: str,
    purpose: str,
) -> list[WeightFactor]:
    """Build all 10 weight factors for a single planet."""
    factors: list[WeightFactor] = []

    # 1. Body weight
    factors.append(
        WeightFactor(
            name="Body Weight",
            raw_value=f"{kg} kg",
            multiplier=1.00,
            explanation=f"Base = {kg} / {_BASE_DIVISOR.get(planet, 10)} = {base:.1f} ratti",
        )
    )
    # 2. Avastha
    av_m = AVASTHA_MULT.get(p.avastha, 1.0)
    factors.append(
        WeightFactor(
            name="Avastha",
            raw_value=f"{p.avastha} ({p.degree_in_sign:.0f}°)",
            multiplier=av_m,
            explanation=_avastha_note(p.avastha),
        )
    )
    # 3. Ashtakavarga
    bav_m, bav_v = _ashtakavarga_factor(planet, p.sign_index, sav)
    factors.append(
        WeightFactor(
            name="Ashtakavarga",
            raw_value=f"{bav_v} bindus",
            multiplier=bav_m,
            explanation="Strong planet needs less stone"
            if bav_m < 1
            else "Average"
            if bav_m == 1
            else "Weak — needs more support",
        )
    )
    # 4. Dignity
    dig_m = DIGNITY_MULT.get(p.dignity, 1.0)
    factors.append(
        WeightFactor(
            name="Dignity",
            raw_value=p.dignity,
            multiplier=dig_m,
            explanation=_dignity_note(p.dignity),
        )
    )
    # 5. Combustion
    comb_m = 0.85 if p.is_combust else 1.0
    factors.append(
        WeightFactor(
            name="Combustion",
            raw_value="combust" if p.is_combust else "clear",
            multiplier=comb_m,
            explanation="Combust — stone effectiveness reduced" if p.is_combust else "Not combust",
        )
    )
    # 6. Retrograde
    ret_m = 1.0
    factors.append(
        WeightFactor(
            name="Retrograde",
            raw_value="retrograde" if p.is_retrograde else "direct",
            multiplier=ret_m,
            explanation="Retrograde — delayed effect, standard weight"
            if p.is_retrograde
            else "Direct motion",
        )
    )
    # 7. Current Dasha
    dasha_m = 0.85 if md.lord == planet else (0.90 if ad.lord == planet else 1.0)
    dasha_label = f"MD={md.lord}, AD={ad.lord}"
    factors.append(
        WeightFactor(
            name="Current Dasha",
            raw_value=dasha_label,
            multiplier=dasha_m,
            explanation=f"Running own {'MD' if md.lord == planet else 'AD'} — planet amplified, less stone needed"
            if dasha_m < 1
            else "Not in own dasha period",
        )
    )
    # 8. Lordship quality
    lord_m = _lordship_factor(planet, benefics, malefics, houses)
    factors.append(
        WeightFactor(
            name="Lordship",
            raw_value=f"houses {houses}",
            multiplier=lord_m,
            explanation="Pure benefic houses"
            if lord_m <= 0.90
            else "Mixed lordship"
            if lord_m <= 1.0
            else "Has trik house",
        )
    )
    # 9. Stone energy density
    se_m = STONE_ENERGY.get(stone, 1.0)
    factors.append(
        WeightFactor(
            name="Stone Energy",
            raw_value=stone,
            multiplier=se_m,
            explanation="High potency per ratti — less needed"
            if se_m < 1
            else "Standard energy density",
        )
    )
    # 10. Purpose
    pu_m = PURPOSE_MULT.get(purpose, 0.9)
    factors.append(
        WeightFactor(
            name="Purpose",
            raw_value=purpose,
            multiplier=pu_m,
            explanation={
                "protection": "Minimal for protection",
                "growth": "Moderate for growth",
                "maximum": "Full strength",
            }.get(purpose, purpose),
        )
    )
    return factors


# ── Helpers ──────────────────────────────────────────────────────────────


def _build_recommendation_map(ctx: dict) -> dict[str, tuple[str, str]]:
    """Map planet name → (status, reason) from lordship context."""
    m: dict[str, tuple[str, str]] = {}
    for s in ctx.get("recommended_stones", []):
        m[s["planet"]] = ("recommended", s.get("reasoning", ""))
    for s in ctx.get("test_stones", []):
        m[s["planet"]] = ("test", s.get("reasoning", ""))
    for s in ctx.get("prohibited_stones", []):
        m[s["planet"]] = ("prohibited", s.get("reasoning", ""))
    return m


def _build_houses_map(ctx: dict) -> dict[str, list[int]]:
    """Map planet → list of houses owned from house_lords."""
    result: dict[str, list[int]] = {}
    for house_str, planet in ctx.get("house_lords", {}).items():
        result.setdefault(planet, []).append(int(house_str))
    return result


def _ashtakavarga_factor(planet: str, sign_idx: int, sav: Any) -> tuple[float, int]:
    """Return (multiplier, bindus) from Bhinnashtakavarga."""
    if planet in ("Rahu", "Ketu") or planet not in sav.bhinna:
        return 1.0, 0
    bindus = sav.bhinna[planet][sign_idx]
    if bindus <= 2:
        return 1.10, bindus
    if bindus <= 4:
        return 1.00, bindus
    if bindus <= 6:
        return 0.90, bindus
    return 0.80, bindus


def _lordship_factor(planet: str, benefics: set, malefics: set, houses: list[int]) -> float:
    """Determine lordship quality multiplier from house ownership."""
    good = all(h in _GOOD_HOUSES for h in houses) if houses else False
    has_trik = any(h in _TRIK_HOUSES for h in houses)
    if planet in benefics and not has_trik and good:
        return 0.85
    if planet in benefics:
        return 0.95
    if planet in malefics:
        return 1.05
    return 1.00


def _prohibited_result(
    planet: str, stone_en: str, stone_hi: str, reason: str
) -> GemstoneWeightResult:
    return GemstoneWeightResult(
        planet=planet,
        stone_name=stone_en,
        stone_name_hi=stone_hi,
        status="prohibited",
        base_ratti=0,
        recommended_ratti=0,
        factors=[],
        website_comparisons={},
        pros_cons={},
        free_alternatives=_FREE_ALT.get(planet, {}),
        prohibition_reason=reason[:120] if reason else f"{planet} stone prohibited for this lagna",
    )


def _website_estimates(kg: float, planet: str) -> dict[str, float]:
    """Static estimates from popular gemstone websites (body-weight-based)."""
    base = kg / _BASE_DIVISOR.get(planet, 10)
    return {
        "GemPundit": round(base, 1),
        "BrahmaGems": round(max(3.0, base * 0.9), 1),
        "GemsMantra": round(base + 1.0, 1),
        "ShubhGems": round(max(5.0, base * 1.2), 1),
        "MyRatna": round(base, 1),
    }


def _pros_cons(rec: float, base: float) -> dict[str, list[str]]:
    """Generate pros/cons for light, medium, heavy weight."""
    light = max(1.0, rec * 0.7)
    heavy = rec * 1.4
    return {
        f"Light ({light:.1f}r)": [
            "Lower cost, easier to source high quality",
            "Subtle effect — good for sensitive people",
            "May not be enough for severely afflicted planet",
        ],
        f"Medium ({rec:.1f}r)": [
            "Balanced cost and effectiveness",
            "Computed recommendation based on 10 chart factors",
            "Best starting point for most natives",
        ],
        f"Heavy ({heavy:.1f}r)": [
            "Stronger effect for severely weak planet",
            "Higher cost, quality harder to maintain",
            "Risk of over-activation if planet has mixed lordship",
        ],
    }


def _avastha_note(avastha: str) -> str:
    notes = {
        "Bala": "Child state — planet developing, moderate stone",
        "Kumara": "Youth state — planet growing, near standard",
        "Yuva": "Prime state — full strength, standard weight",
        "Vriddha": "Old state — energy declining, less stone effective",
        "Mruta": "Deceased state — minimal energy, reduce weight",
    }
    return notes.get(avastha, "Unknown state")


def _dignity_note(dignity: str) -> str:
    notes = {
        "exalted": "Exalted — already strong, needs less stone",
        "mooltrikona": "Mooltrikona — very strong, less needed",
        "own": "Own sign — strong, moderate stone suffices",
        "neutral": "Neutral — standard weight applies",
        "enemy": "Enemy sign — slightly weakened",
        "debilitated": "Debilitated — stone fights debilitation, reduced effectiveness",
    }
    return notes.get(dignity, "Unknown dignity")
