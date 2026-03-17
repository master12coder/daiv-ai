"""Post-generation safety validator — checks LLM output for dangerous
gemstone recommendations, maraka misclassifications, and harmful advice."""

from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

# Regex words that indicate a POSITIVE recommendation context
_RECOMMEND_WORDS = re.compile(
    r"\b(recommend|wear|beneficial|auspicious|strengthen|suitable|advised|should wear|must wear)\b",
    re.IGNORECASE,
)
# Words that indicate the text is already cautioning AGAINST the stone
_AVOID_WORDS = re.compile(
    r"\b(avoid|never|prohibited|harmful|dangerous|do not|don\'t|maraka|malefic|contraindicated)\b",
    re.IGNORECASE,
)


def _is_recommended_context(text: str, stone_name: str) -> bool:
    """Check if a stone name appears in a recommendation context.

    Uses word-boundary matching to avoid false positives like
    "Moti" inside "emotional".

    Returns True if the stone appears as a whole word near
    'recommend/wear' words WITHOUT nearby 'avoid/never/prohibited' words.
    """
    stone_pattern = re.compile(r"\b" + re.escape(stone_name) + r"\b", re.IGNORECASE)

    for match in stone_pattern.finditer(text):
        pos = match.start()
        window_start = max(0, pos - 150)
        window_end = min(len(text), pos + len(stone_name) + 150)
        window = text[window_start:window_end]

        has_recommend = bool(_RECOMMEND_WORDS.search(window))
        has_avoid = bool(_AVOID_WORDS.search(window))

        if has_recommend and not has_avoid:
            return True

    return False


def validate_interpretation(
    text: str,
    lagna_sign: str,
    lordship_ctx: dict[str, Any],
) -> tuple[str, list[str]]:
    """Check LLM output for dangerous errors before showing to user.

    Checks:
    1. Prohibited stones recommended in positive context
    2. Maraka planets called "benefic" or "auspicious"
    3. Worship/strengthening recommended for maraka planets

    Returns:
        (possibly_amended_text, list_of_error_strings)
    """
    errors: list[str] = []

    prohibited = lordship_ctx.get("prohibited_stones", [])
    maraka_list = lordship_ctx.get("maraka", [])

    # Check 1: Did LLM recommend a prohibited stone?
    for entry in prohibited:
        stone = entry.get("stone", "")
        planet = entry.get("planet", "")
        stone_names = [stone]
        if "(" in stone:
            parts = stone.replace(")", "").split("(")
            stone_names = [p.strip() for p in parts if p.strip()]

        for sn in stone_names:
            sn_pattern = re.compile(r"\b" + re.escape(sn) + r"\b", re.IGNORECASE)
            if sn_pattern.search(text) and _is_recommended_context(text, sn):
                errors.append(
                    f"DANGER: {stone} ({planet}'s stone) appears to be RECOMMENDED "
                    f"but is PROHIBITED for {lagna_sign} lagna. "
                    f"{planet} is a functional malefic/maraka."
                )
                break

    # Check 2: Did LLM call a maraka planet "benefic" or "auspicious"?
    text_lower = text.lower()
    for m in maraka_list:
        planet = m.get("planet", "")
        if not planet:
            continue
        p_lower = planet.lower()
        bad_patterns = [
            f"{p_lower} is benefic",
            f"{p_lower} is auspicious",
            f"{p_lower} is a benefic",
            f"{p_lower} as benefic",
            f"benefic {p_lower}",
        ]
        for pat in bad_patterns:
            if pat in text_lower:
                houses = m.get("house_str", "")
                errors.append(
                    f"ERROR: {planet} called benefic/auspicious but is MARAKA "
                    f"({houses}) for {lagna_sign} lagna."
                )
                break

    # Check 3: Did LLM recommend worshipping a maraka planet?
    for m in maraka_list:
        planet = m.get("planet", "")
        if not planet:
            continue
        p_lower = planet.lower()
        worship_patterns = [
            f"worship {p_lower}",
            f"pray to {p_lower}",
            f"strengthen {p_lower}",
            f"propitiate {p_lower}",
        ]
        for pat in worship_patterns:
            if pat in text_lower:
                errors.append(
                    f"WARNING: Recommended strengthening/worshipping {planet} "
                    f"which is MARAKA for {lagna_sign} lagna. "
                    f"Propitiating a maraka can activate harmful effects."
                )
                break

    if errors:
        warning_block = (
            "\n\n---\n"
            "## SAFETY VALIDATION WARNINGS\n"
            "The following issues were detected by the Parashari rule engine:\n\n"
        )
        for err in errors:
            warning_block += f"- {err}\n"
        warning_block += (
            "\nPlease consult the lordship rules for your lagna before "
            "following any flagged recommendation above.\n"
        )
        return text + warning_block, errors

    return text, []
