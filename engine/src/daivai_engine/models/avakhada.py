"""Avakhada Chakra model — 18 classical birth qualities.

The Avakhada Chakra (birth table) is derived from the Moon's nakshatra,
pada, and sign relative to the lagna. It encodes qualities used in birth
analysis, auspicious name selection, and Ashta Koota horoscope matching.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class AvakhadaChakra(BaseModel):
    """Complete Avakhada Chakra — 18 classical birth qualities.

    All fields are derived from the Moon's nakshatra, pada, sign, and the
    native's lagna. The model is informational (read-only analysis output).

    Sources: BPHS Ch.7 (friendship/gana), traditional Ashta Koota texts.
    """

    # ── Moon nakshatra ────────────────────────────────────────────────────────
    nakshatra: str = Field(description="Moon's nakshatra name (e.g., Rohini)")
    nakshatra_lord: str = Field(description="Dasha lord of Moon's nakshatra")
    nakshatra_number: int = Field(ge=1, le=27, description="Nakshatra index 1-27")

    # ── Moon sign ─────────────────────────────────────────────────────────────
    sign: str = Field(description="Moon's rashi (sign) name")
    sign_lord: str = Field(description="Lord of Moon's sign")

    # ── Pada (quarter) ────────────────────────────────────────────────────────
    charan: int = Field(ge=1, le=4, description="Nakshatra pada (quarter) 1-4")

    # ── Avakhada qualities ────────────────────────────────────────────────────
    tatva: str = Field(description="Panchamahabhuta element: Fire/Earth/Air/Water (from pada)")
    paya: str = Field(description="Base metal: Gold/Silver/Copper/Iron (from nakshatra number)")
    yunja: str = Field(
        description="Nakshatra group: Poorva/Madhya/Uttara (nakshatras 1-9/10-18/19-27)"
    )

    # ── Nakshatra-derived qualities ───────────────────────────────────────────
    gan: str = Field(description="Gana: Deva/Manushya/Rakshasa")
    nadi: str = Field(description="Nadi: Aadi/Madhya/Antya")
    yoni: str = Field(description="Animal type from nakshatra (e.g., Serpent)")
    varna: str = Field(
        description="Varna: Brahmin/Kshatriya/Vaishya/Shudra (from Moon's sign element)"
    )
    vashya: str = Field(description="Creature class: Manav/Chatushpad/Jalachara/Vanchar/Keet")

    # ── Panchang values ───────────────────────────────────────────────────────
    tithi: str = Field(description="Tithi (lunar day) at birth")
    karan: str = Field(description="Karana (half-tithi) at birth")

    # ── Lagna (ascendant) ─────────────────────────────────────────────────────
    ascendant: str = Field(description="Lagna (ascendant) sign name")
    ascendant_lord: str = Field(description="Lord of the lagna sign")

    # ── Name ──────────────────────────────────────────────────────────────────
    name_alphabet: str = Field(
        description="Suggested first syllable (Akshar) for the native's given name"
    )
